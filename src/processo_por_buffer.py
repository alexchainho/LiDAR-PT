# Este ficheiro foi renomeado para processo_por_buffer.py conforme solicitado.
# O conteúdo original deve ser transferido para o novo ficheiro se necessário.
import os
import sys

# Configurar encoding UTF-8 para o stdout no Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import config_loader

# Carregar configurações
CONFIG = config_loader.load_config()

import math
import requests
import json
import time
import sys
import argparse
import urllib.parse
from html.parser import HTMLParser
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import shapefile  # pip install pyshp
import sys

from pyproj import CRS, Transformer
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# Global state for session management
username, password = config_loader.get_credentials()
auth_state = {
    "session": None,
    "username": username,
    "password": password,
    "last_auth_time": 0,
    "download_counter": 0,
}
SESSION_TIMEOUT = 25 * 60  # 25 minutes in seconds

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass

class KeycloakFormParser(HTMLParser):
    """HTML parser to extract form data from Keycloak login page"""
    def __init__(self):
        super().__init__()
        self.form_action = None
        self.form_data = {}
        self.in_form = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'form' and attrs_dict.get('id') == 'kc-form-login':
            self.in_form = True
            self.form_action = attrs_dict.get('action')
        elif tag == 'input' and self.in_form:
            input_name = attrs_dict.get('name')
            input_value = attrs_dict.get('value', '')
            input_type = attrs_dict.get('type', 'text')
            if input_name and input_type == 'hidden':
                self.form_data[input_name] = input_value

    def handle_endtag(self, tag):
        if tag == 'form' and self.in_form:
            self.in_form = False

# Session validation helper functions
def is_session_expired():
    """Check if session has likely expired based on time."""
    return (time.time() - auth_state["last_auth_time"]) > SESSION_TIMEOUT

def is_session_valid(stac_url):
    """Check if the current session is still valid by making a test API call."""
    try:
        test_payload = {"bbox": [-9.0, 38.0, -8.0, 39.0], "limit": 1}
        response = auth_state["session"].post(stac_url, json=test_payload, timeout=15)
        return response.status_code == 200
    except Exception as e:
        print(f"\n[Session validation check failed: {e}]")
        return False

# --- Authenticate() to update global state ---
def authenticate(username, password):
    """
    Authenticates with DGT using username and password and updates the global state.
    """
    # Constants for authentication
    urls = config_loader.get_all_urls()
    auth_base_url = urls['auth_base']
    redirect_uri = urls['redirect_uri']
    client_id = "aai-oidc-dgt"
    main_site = urls['main_site']
    stac_url = urls['stac_search']
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8", "Connection": "keep-alive"
    }

    try:
        print("Starting authentication process...")
        session = requests.Session()
        session.headers.update(headers)

        # 1: Visit main site to get initial session
        print("Visiting main site...")
        response = session.get(main_site, timeout=30)
        response.raise_for_status()
        auth_params = {'client_id': client_id, 'response_type': 'code', 'redirect_uri': redirect_uri, 'scope': 'openid profile email'}
        full_auth_url = f"{auth_base_url}/auth?" + urllib.parse.urlencode(auth_params)
        print("Getting authentication page...")
        response = session.get(full_auth_url, timeout=30)
        response.raise_for_status()

        # 3: Parse the login form
        parser = KeycloakFormParser()
        parser.feed(response.text)
        if not parser.form_action: raise AuthenticationError("Could not find login form on the authentication page.")
        print("Found login form, submitting credentials...")

        # 4: Submit login form
        login_data = parser.form_data.copy()
        login_data.update({'username': username, 'password': password})
        login_url = parser.form_action if not parser.form_action.startswith('/') else f"https://auth.cdd.dgterritorio.gov.pt{parser.form_action}"
        login_headers = headers.copy()
        login_headers.update({'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://auth.cdd.dgterritorio.gov.pt', 'Referer': response.url})
        response = session.post(login_url, data=login_data, headers=login_headers, allow_redirects=True, timeout=30)
        response.raise_for_status()
        
        # 5: Check if login was successful by testing the STAC API
        if response.url.startswith(main_site):
            print("Successfully redirected to main site. Verifying session...")
            test_response = session.post(stac_url, json={"bbox": [-9.0, 38.0, -8.0, 39.0], "limit": 1}, timeout=30)
            if test_response.status_code == 200:
                print("Authentication successful! Session is valid.")
                auth_state.update({"session": session, "username": username, "password": password, "last_auth_time": time.time()})
                return True
            else:
                raise AuthenticationError(f"Authentication test failed. STAC API returned status {test_response.status_code}. Please check credentials.")
        else:
            raise AuthenticationError("Authentication failed. Unexpected redirection URL.")

    except requests.RequestException as e:
        print(f"Network error during authentication: {e}")
        return False
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
        return False

def get_file_extension(mime_type):
    mime_to_extension = {
        "image/tiff; application=geotiff": ".tif",
        "image/tiff": ".tif",
        "application/vnd.laszip": ".laz",
    }
    return mime_to_extension.get(mime_type, ".bin")

def divide_bbox(bbox, max_area_km2=200):
    min_lon, min_lat, max_lon, max_lat = bbox
    deg_to_km = 111
    width_km = (max_lon - min_lon) * deg_to_km * math.cos(math.radians((min_lat + max_lat) / 2))
    height_km = (max_lat - min_lat) * deg_to_km
    if width_km * height_km <= max_area_km2: return [bbox]
    splits_x = math.ceil(width_km / math.sqrt(max_area_km2))
    splits_y = math.ceil(height_km / math.sqrt(max_area_km2))

    delta_lon = (max_lon - min_lon) / splits_x
    delta_lat = (max_lat - min_lat) / splits_y

    small_bboxes = []
    for i in range(splits_x):
        for j in range(splits_y):
            small_min_lon = min_lon + i * delta_lon
            small_max_lon = min(small_min_lon + delta_lon, max_lon)
            small_min_lat = min_lat + j * delta_lat
            small_max_lat = min(small_min_lat + delta_lat, max_lat)
            small_bboxes.append([small_min_lon, small_min_lat, small_max_lon, small_max_lat])
    
    return small_bboxes

def search_stac_api(stac_url, bbox, collections=None, delay=0.2):
    payload = {
        "bbox": bbox,
        "limit": 1000
    }
    if collections:
        payload["collections"] = collections

    print(f"A esperar {delay}s antes de procurar...")
    time.sleep(delay)
    
    try:
        # Use session from global state
        response = auth_state["session"].post(stac_url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro na query da API STAC para a bbox {bbox}: {e}")
        return {"features": []}

def collect_urls_per_collection(stac_response):
    urls_per_collection = {}
    seen_urls = set()

    for item in stac_response.get("features", []):
        collection = item.get("collection", "unknown")
        item_id = next((link.get("href").split("/")[-1] for link in item.get("links", []) if link.get("rel") == "self"), item.get("id", "unknown"))
        for asset_key, asset in item.get("assets", {}).items():
            url = asset.get("href")
            asset_type = asset.get("type", "")
            asset_title = asset.get("title", "")
            # MDS-50cm: pelo nome/título
            is_mds = ("MDS-50cm" in asset_title or "MDS-50cm" in asset_key or "MDS-50cm" in item_id)
            # LAZ: apenas se type for application/vnd.laszip
            is_laz = (asset_type == "application/vnd.laszip")
            if is_mds or is_laz:
                if url and url not in seen_urls:
                    ext = get_file_extension(asset_type)
                    # fallback para .tif se for MDS-50cm mas não detetado pelo tipo
                    if is_mds and ext == ".bin":
                        ext = ".tif"
                    urls_per_collection.setdefault(collection, []).append((url, item_id, ext))
                    seen_urls.add(url)
    
    return urls_per_collection
def collect_urls_per_collection(stac_response, produtos_selecionados=None):
    """
    Coleta URLs dos produtos selecionados.
    produtos_selecionados: dict com chaves 'LAZ', 'MDS-2m', 'MDS-50cm', 'MDT-2m', 'MDT-50cm', 'Todos'
    'Todos' significa apenas: LAZ, MDS-2m, MDS-50cm, MDT-2m, MDT-50cm (sem ortofotomapas)
    """
    urls_per_collection = {}
    seen_urls = set()
    
    # Definir produtos permitidos (apenas os 5 produtos LiDAR)
    PRODUTOS_PERMITIDOS = ['LAZ', 'MDS-2m', 'MDS-50cm', 'MDT-2m', 'MDT-50cm']
    
    # Se Todos=True, aceitar todos os 5 produtos
    aceitar_tudo = (produtos_selecionados is None or 
                    produtos_selecionados.get('Todos', False) or
                    not any(produtos_selecionados.values()))
    
    for item in stac_response.get("features", []):
        collection = item.get("collection", "unknown")
        item_id = next((link.get("href").split("/")[-1] for link in item.get("links", []) if link.get("rel") == "self"), item.get("id", "unknown"))
        for asset_key, asset in item.get("assets", {}).items():
            url = asset.get("href")
            asset_type = asset.get("type", "")
            asset_title = asset.get("title", "")
            collection_lower = collection.lower()
            
            # Identificar tipo de produto baseado no nome da coleção
            is_laz = ("laz" in collection_lower)
            is_mds_2m = ("mds-2m" in collection_lower)
            is_mds_50cm = ("mds-50cm" in collection_lower)
            is_mdt_2m = ("mdt-2m" in collection_lower)
            is_mdt_50cm = ("mdt-50cm" in collection_lower)
            
            # Verificar se é um dos 5 produtos permitidos
            is_produto_permitido = is_laz or is_mds_2m or is_mds_50cm or is_mdt_2m or is_mdt_50cm
            
            # Se não for produto permitido, ignorar (mesmo com Todos=True)
            if not is_produto_permitido:
                continue
            
            # Se aceitar_tudo=True, aceita todos os produtos permitidos
            if aceitar_tudo:
                aceitar = True
            else:
                # Filtrar baseado nas seleções específicas
                aceitar = False
                if produtos_selecionados.get('LAZ', False) and is_laz:
                    aceitar = True
                if produtos_selecionados.get('MDS-2m', False) and is_mds_2m:
                    aceitar = True
                if produtos_selecionados.get('MDS-50cm', False) and is_mds_50cm:
                    aceitar = True
                if produtos_selecionados.get('MDT-2m', False) and is_mdt_2m:
                    aceitar = True
                if produtos_selecionados.get('MDT-50cm', False) and is_mdt_50cm:
                    aceitar = True
            
            if not aceitar:
                continue
            
            # Adicionar URL
            if url and url not in seen_urls:
                ext = get_file_extension(asset_type)
                if (is_mds_2m or is_mds_50cm or is_mdt_2m or is_mdt_50cm) and ext == ".bin":
                    ext = ".tif"
                urls_per_collection.setdefault(collection, []).append((url, item_id, ext))
                seen_urls.add(url)
    
    return urls_per_collection

# Check global session validity periodically
def download_file(stac_url, url, item_id, extension, output_dir, delay=5.0):

    auth_state["download_counter"] += 1
    if auth_state["download_counter"] % 10 == 0:
        if is_session_expired() or not is_session_valid(stac_url):
            print("\n[Session expired or invalid, re-authenticating...]")
            if not authenticate(auth_state["username"], auth_state["password"]):
                raise AuthenticationError("Re-authentication failed. Aborting.")

    filename = f"{item_id}{extension}" if item_id else f"{url.split('/')[-1]}{extension}"
    file_path = os.path.join(output_dir, filename)

    if os.path.exists(file_path):
        print(f"Ignorar {filename}: ficheiro já existe")
        return True

    print(f"A esperar {delay}s antes do download do {filename}...")
    time.sleep(delay)

    max_retries, retry_delay = 3, 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = auth_state["session"].get(url, stream=True, timeout=60)
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type.startswith("text/html"):
                raise AuthenticationError(f"Authentication error for {url} (received HTML).")
            response.raise_for_status()

            total = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 8192
            bar_length = 30

            os.makedirs(output_dir, exist_ok=True)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            done = int(bar_length * downloaded / total)
                            percent = int(100 * downloaded / total)
                            bar = f"[{'#' * done}{'-' * (bar_length - done)}] {percent}%"
                            sys.stdout.write(f"\rDownloading {filename} {bar}")
                            sys.stdout.flush()
            
            if total > 0:
                sys.stdout.write("\n")
            else:
                print(f"Download do {filename} realizado! (tamanho desconhecido)")
            
            return True # Success
        
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, requests.exceptions.Timeout) as e:
            sys.stdout.write("\n") # Clean up line from progress bar
            retry_count += 1
            if retry_count < max_retries:
                print(f"Erro de rede no download {filename} (tentativa {retry_count}/{max_retries}): {e}")
                print(f"A esperar {retry_delay}s antes de tentar novamente...")
                time.sleep(retry_delay)
                continue
            else:
                print(f"Falha no download {filename} após {max_retries} tentativas: {e}")
                return False
        except Exception as e:
            sys.stdout.write("\n") # Clean up line from progress bar
            print(f"Erro no download {url}: {e}")
            return False
    return False

def get_available_collections_fallback(stac_url):
    print("A obter as coleções via a API do STAC...")
    payload = {
        "bbox": [-9.5, 36.5, -6.0, 42.5],  # Portugal mainland
        "limit": 1000
    }
    try:
        response = auth_state["session"].post(stac_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return sorted({c for feature in data.get("features", []) if (c := feature.get("collection"))})
    except Exception as e:
        print(f"Erro a obter as coleções: {e}")
        return []

def interactive_mode(stac_url):
    print("\n--- DGT CDD Downloader (Interactive Mode) ---")
    try:
        username = input("DGT Username (Email):\n> ").strip()
        password = input("DGT Password:\n> ").strip()
        

        if not authenticate(username, password):
            sys.exit(1)

        bbox_input = input("Define a bounding box (WGS84) separada por virgulas, como (min_lon,min_lat,max_lon,max_lat):\n> ")
        input_bbox = [float(x.strip()) for x in bbox_input.split(",")]
        output_dir = input("Diretoria de output (default: ./downloaded_files):\n> ").strip() or "./downloaded_files"
        download_delay = float(input("Tempo de espera em segundos entre cada request/download (default: 5.0):\n> ").strip() or 5.0)
        available = get_available_collections_fallback(stac_url)
        if not available:
            print("AVISO: Não foi possível obter as coleções. A processar sem esse filtro.")
            selected_collections = None
        else:
            print("\nColeções disponíveis:")
            for i, name in enumerate(available, 1):
                print(f"  {i}. {name}")
            selected_input = input("Seleciona o número da coleção (ex: 1,3 ou Enter para todas na BBox):\n> ").strip()
            selected_collections = None
            if selected_input:
                try:
                    indices = [int(i) - 1 for i in selected_input.split(",")]
                    selected_collections = [available[i] for i in indices if 0 <= i < len(available)]
                except Exception:
                    print("Input inválido. A processar sem esse filtro.")
                    
        print("\nInício do processo de download...\n")

        return input_bbox, output_dir, download_delay, selected_collections
    except Exception as e:
        print(f"Erro no modo interativo: {e}")
        sys.exit(1)

def select_shapefile_and_get_bbox_and_dir():
    """Seleciona shapefile, extrai bbox, converte para WGS84 se necessário, e devolve bbox e diretório."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Selecione o ficheiro Shapefile (.shp)",
        filetypes=[("Shapefile", "*.shp")]
    )
    if not file_path:
        raise ValueError("Nenhum ficheiro selecionado.")
    sf = shapefile.Reader(file_path)
    bbox = list(sf.bbox)
    dir_path = os.path.dirname(file_path)

    # Verifica e converte para WGS84 se necessário
    prj_path = os.path.splitext(file_path)[0] + ".prj"
    if os.path.exists(prj_path):
        with open(prj_path) as prj_file:
            prj_txt = prj_file.read()
        crs = CRS.from_wkt(prj_txt)
        if not crs.is_geographic:
            print("A converter bbox para WGS84...")
            transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
            minx, miny, maxx, maxy = bbox
            min_lon, min_lat = transformer.transform(minx, miny)
            max_lon, max_lat = transformer.transform(maxx, maxy)
            bbox = [min_lon, min_lat, max_lon, max_lat]
    print(f"Bounding box extraída do shapefile (WGS84): {bbox}")
    print(f"Output será na mesma pasta do shapefile: {dir_path}")
    return bbox, dir_path

def choose_collections(stac_url, bbox):
    """Permite ao utilizador escolher as coleções disponíveis na bbox."""
    # Não pedir coleções ao utilizador, filtrar apenas MDS-50cm e LAZ
    return None

def main(bbox, stac_url, output_dir, delay, collections=None, produtos_selecionados=None, nome_id=None, merge_rasters=True):
    # Apenas pesquisar na bbox do shapefile, sem dividir
    print(f"A pesquisar apenas na bbox do shapefile: {bbox}")
    
    # Mostrar produtos selecionados
    if produtos_selecionados:
        selecionados = [k for k, v in produtos_selecionados.items() if v and k != 'Todos']
        if produtos_selecionados.get('Todos'):
            print("Produtos selecionados: TODOS (LAZ, MDS-2m, MDS-50cm, MDT-2m, MDT-50cm)")
        elif selecionados:
            print(f"Produtos selecionados: {', '.join(selecionados)}")
        else:
            print("Produtos selecionados: TODOS (LAZ, MDS-2m, MDS-50cm, MDT-2m, MDT-50cm)")
    
    stac_response = search_stac_api(stac_url, bbox, collections=collections)
    urls_per_collection = collect_urls_per_collection(stac_response, produtos_selecionados=produtos_selecionados)
    all_urls_per_collection = urls_per_collection

    print(f"Encontrados {sum(len(urls) for urls in urls_per_collection.values())} items na bbox do shapefile")

    total_urls = sum(len(urls) for urls in all_urls_per_collection.values())
    print(f"Total de URLs únicos para download: {total_urls}")
    downloaded, skipped = 0, 0
    auth_state["download_counter"] = 0
    for collection, url_id_ext_pairs in all_urls_per_collection.items():
        print(f"\nDownloading da coleção: {collection}")
        collection_output_dir = os.path.join(output_dir, collection)
        for j, (url, item_id, extension) in enumerate(url_id_ext_pairs, 1):
            print(f"A processar o URL {j}/{len(url_id_ext_pairs)} : {url}")
            if download_file(stac_url, url, item_id, extension, collection_output_dir, delay):
                if not os.path.exists(os.path.join(collection_output_dir, f"{item_id}{extension}")):
                    downloaded += 1
                else:
                    skipped += 1
            else:
                pass 
    print(f"\nResumo: Download de {downloaded} ficheiros, ignorados {skipped} ficheiros")

    # --- Função genérica para merge de rasters ---
    def fazer_merge_raster(produto_nome, output_dir):
        """Merge múltiplos rasters de um produto numa única imagem"""
        import rasterio
        from rasterio.merge import merge
        import glob
        from datetime import datetime
        
        produto_dir = os.path.join(output_dir, produto_nome)
        if not os.path.exists(produto_dir):
            return
        
        tif_files = glob.glob(os.path.join(produto_dir, '*.tif'))
        if len(tif_files) > 1:
            print(f"A unir {len(tif_files)} rasters {produto_nome}...")
            
            # Abrir ficheiros de origem
            src_files_to_mosaic = [rasterio.open(fp) for fp in tif_files]
            
            # Fazer merge
            mosaic, out_trans = merge(src_files_to_mosaic)
            out_meta = src_files_to_mosaic[0].meta.copy()
            
            # Fechar ficheiros de origem ANTES de criar o output
            for src in src_files_to_mosaic:
                src.close()
            
            out_meta.update({
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_trans,
                "crs": "EPSG:3763"
            })
            # Herdar nodata se existir
            if src_files_to_mosaic[0].nodata is not None:
                out_meta["nodata"] = src_files_to_mosaic[0].nodata
            
            # Nome do raster unido: apenas o nome do produto (ex: MDS-50cm.tif)
            nome_raster = f"{produto_nome}.tif"
            out_path = os.path.join(produto_dir, nome_raster)
            
            # Verificar se ficheiro já existe e tentar eliminar
            if os.path.exists(out_path):
                try:
                    os.remove(out_path)
                    print(f"⚠️ Ficheiro existente removido: {out_path}")
                except PermissionError:
                    # Se não conseguir eliminar (ficheiro aberto), adicionar timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nome_raster = f"{produto_nome}_{timestamp}.tif"
                    out_path = os.path.join(produto_dir, nome_raster)
                    print(f"⚠️ Ficheiro anterior está aberto. A criar novo: {nome_raster}")
            
            if mosaic.ndim == 2:
                mosaic = mosaic[None, ...]
            
            with rasterio.open(out_path, "w", **out_meta) as dest:
                dest.write(mosaic)
            
            print(f"✅ Raster unido salvo em: {out_path}")
        elif len(tif_files) == 1:
            print(f"Só existe um raster {produto_nome}, não é necessário unir.")
        else:
            print(f"Nenhum raster {produto_nome} encontrado para unir.")
    
    # --- Merge dos rasters para cada produto selecionado ---
    if not merge_rasters:
        print("\n⏭️ Merge de rasters desativado. Ficheiros individuais mantidos.")
        print("\n" + "="*80)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*80)
        print(f"📁 Pasta do projeto: {output_dir}")
        print("\nA encerrar em 5 segundos...")
        import time
        time.sleep(5)
        return
    
    aceitar_tudo = produtos_selecionados is None or produtos_selecionados.get('Todos', False)
    
    if aceitar_tudo or produtos_selecionados.get('MDS-50cm', False):
        fazer_merge_raster('MDS-50cm', output_dir)
    
    if aceitar_tudo or produtos_selecionados.get('MDS-2m', False):
        fazer_merge_raster('MDS-2m', output_dir)
    
    if aceitar_tudo or produtos_selecionados.get('MDT-50cm', False):
        fazer_merge_raster('MDT-50cm', output_dir)
    
    if aceitar_tudo or produtos_selecionados.get('MDT-2m', False):
        fazer_merge_raster('MDT-2m', output_dir)
    
    # Mensagem final
    print("\n" + "="*80)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print(f"📁 Pasta do projeto: {output_dir}")
    print("\nA encerrar em 5 segundos...")
    import time
    time.sleep(5)

def query_database(sado_input):
    """
    Pesquisa o número SADO no CSV e devolve Localidade, Concelho, Latitude, Longitude.
    """
    csv_path = config_loader.get_path('csv_ocorrencias')
    try:
        df = pd.read_csv(csv_path, dtype=str)
        # Tenta encontrar o SADO na coluna 'Numero' (ajuste se o nome da coluna for diferente)
        row = df.loc[df['Numero'] == str(sado_input)]
        if not row.empty:
            row = row.iloc[0]
            return {
                'localidade': row.get('Localidade', ''),
                'concelho': row.get('Concelho', ''),
                'latitude': float(row.get('Latitude', '').replace(',', '.')) if row.get('Latitude') else None,
                'longitude': float(row.get('Longitude', '').replace(',', '.')) if row.get('Longitude') else None
            }
        else:
            print(f"Nenhum registo encontrado para SADO {sado_input} no CSV")
            return None
    except Exception as e:
        print(f"Erro ao consultar CSV: {e}")
        return None

def create_folder(sado_number, localidade, concelho):
    """Create folder with compiled name. Uses tkinter to select base path if not provided."""
    # Pedir ao utilizador para selecionar a pasta de output
    root = tk.Tk()
    root.withdraw()
    base_path = filedialog.askdirectory(
        title="Selecione a pasta base para o projeto",
        initialdir=config_loader.get_path('base_path_tos')
    )
    root.destroy()
    
    if not base_path:
        print("Nenhuma pasta selecionada. Usando pasta padrão.")
        base_path = config_loader.get_path('base_path_tos')

    # Clean strings for folder name (remove invalid characters)
    clean_sado = str(sado_number).replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    clean_localidade = str(localidade).replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_') if localidade else ''
    clean_concelho = str(concelho).replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

    # Create folder name
    if clean_localidade:
        folder_name = f"{clean_sado}_{clean_localidade}_{clean_concelho}"
    else:
        folder_name = f"{clean_sado}_{clean_concelho}"

    folder_path = os.path.join(base_path, folder_name)

    try:
        if os.path.exists(folder_path):
            print(f"Pasta já existe: {folder_name}")
            return folder_path

        os.makedirs(folder_path, exist_ok=True)
        shp_dir = os.path.join(folder_path, 'shp')
        os.makedirs(shp_dir, exist_ok=True)
        print(f"Pasta criada: {folder_name}")
        return folder_path
    except Exception as e:
        print(f"Erro ao criar pasta: {e}")
        return None

def create_shapefiles(lat, lon, folder, sado_input):
    """
    Cria shapefiles de ponto e buffer de 10km em torno do ponto.
    """
    try:
        shp_dir = os.path.join(folder, 'shp')
        os.makedirs(shp_dir, exist_ok=True)
        # Cria shapefile de ponto
        point = Point(lon, lat)
        gdf_point = gpd.GeoDataFrame({'SADO': [sado_input]}, geometry=[point], crs="EPSG:4326")
        point_shp = os.path.join(shp_dir, f'ponto_{sado_input}.shp')
        gdf_point.to_file(point_shp)
        # Cria buffer de 3km (projeta para UTM para precisão)
        utm_crs = CRS.from_epsg(32629)  # Portugal mainland UTM zone 29N
        gdf_utm = gdf_point.to_crs(utm_crs)
        buffer = gdf_utm.buffer(1000)  # 1km
        gdf_buffer = gpd.GeoDataFrame({'SADO': [sado_input]}, geometry=buffer, crs=utm_crs)
        buffer_shp = os.path.join(shp_dir, f'buffer_{sado_input}_1km.shp')
        gdf_buffer.to_crs("EPSG:4326").to_file(buffer_shp)
        return True
    except Exception as e:
        print(f"Erro ao criar shapefiles: {e}")
        return False

def main_popup_and_shapefile():

    # Processar argumentos de linha de comando
    produtos_args = None
    lat_arg = None
    lon_arg = None
    buffer_arg = None
    output_arg = None
    nome_arg = None
    
    # Parse de argumentos
    produtos_args = None
    lat_arg = None
    lon_arg = None
    buffer_arg = None
    output_arg = None
    nome_arg = None
    merge_arg = False  # Nova flag para merge
    
    for arg in sys.argv:
        if arg.startswith('--produtos='):
            produtos_str = arg.split('=')[1]
            if produtos_str == 'TODOS':
                produtos_args = {'Todos': True, 'MDS-50cm': False, 'LAZ': False, 'MDT': False, 'Ortofotomapas': False}
            else:
                produtos_lista = produtos_str.split(',')
                produtos_args = {
                    'Todos': False,
                    'MDS-50cm': 'MDS-50cm' in produtos_lista,
                    'LAZ': 'LAZ' in produtos_lista,
                    'MDT': 'MDT' in produtos_lista,
                    'Ortofotomapas': 'Ortofotomapas' in produtos_lista
                }
        elif arg.startswith('--lat='):
            lat_arg = float(arg.split('=')[1])
        elif arg.startswith('--lon='):
            lon_arg = float(arg.split('=')[1])
        elif arg.startswith('--buffer='):
            buffer_arg = int(arg.split('=')[1])
        elif arg.startswith('--output='):
            output_arg = arg.split('=')[1]
        elif arg.startswith('--nome='):
            nome_arg = arg.split('=')[1]
        elif arg == '--merge':
            merge_arg = True
    # Se coordenadas foram passadas via argumentos, usar fluxo direto
    if lat_arg is not None and lon_arg is not None and buffer_arg and output_arg and nome_arg:
        print(f"✅ Coordenadas recebidas: {lat_arg}, {lon_arg}")
        print(f"✅ Buffer: {buffer_arg}m")
        print(f"✅ Pasta: {output_arg}")
        
        # Criar dict de produtos
        if produtos_args:
            produtos_dict = produtos_args
        else:
            produtos_dict = {'MDS-50cm': True, 'LAZ': True, 'MDT': False, 'Ortofotomapas': False, 'Todos': False}
        
        # Extrair bbox do buffer shapefile
        buffer_shp = os.path.join(output_arg, 'shp', f'buffer_{nome_arg}*.shp')
        import glob
        buffer_files = glob.glob(buffer_shp)
        if buffer_files:
            gdf = gpd.read_file(buffer_files[0])
            bbox = list(gdf.to_crs(epsg=4326).total_bounds)
            
            # Iniciar download
            username, password = config_loader.get_credentials()
            delay = config_loader.get_setting('download_delay')
            STAC_SEARCH_URL = config_loader.get_url('stac_search')
            
            if not authenticate(username, password):
                sys.exit(1)
            
            print("\n🚀 Iniciando download...\n")
            main(bbox, STAC_SEARCH_URL, output_arg, delay, collections=None, produtos_selecionados=produtos_dict, nome_id=nome_arg, merge_rasters=merge_arg)
        else:
            print(f"❌ Shapefile buffer não encontrado em: {buffer_shp}")
        return

    # 1. Janela popup para escolher método de input
    root = tk.Tk()
    root.withdraw()
    
    # Variáveis para checkboxes de produtos (usar args se fornecidos pelo seletor_projeto.py)
    if produtos_args:
        produtos_vars = {k: tk.BooleanVar(value=v) for k, v in produtos_args.items()}
    else:
        # Se executado diretamente (sem passar pelo seletor), valores padrão
        produtos_vars = {
            'MDS-50cm': tk.BooleanVar(value=True),
            'LAZ': tk.BooleanVar(value=True),
            'MDT': tk.BooleanVar(value=False),
            'Ortofotomapas': tk.BooleanVar(value=False),
            'Todos': tk.BooleanVar(value=False)
        }

    # Ir diretamente para input de coordenadas (sem diálogo de escolha SADO/Coords)
    root = tk.Tk()
    root.withdraw()
    
    # 1. Input de latitude
    lat_str = simpledialog.askstring("Latitude", "Insira a latitude (coordenadas decimais):", parent=root)
    if not lat_str:
        messagebox.showerror("Erro", "Latitude é obrigatória!")
        return
    
    # 2. Input de longitude
    lon_str = simpledialog.askstring("Longitude", "Insira a longitude (coordenadas decimais):", parent=root)
    if not lon_str:
        messagebox.showerror("Erro", "Longitude é obrigatória!")
        return
    
    try:
        lat = float(lat_str.replace(',', '.'))
        lon = float(lon_str.replace(',', '.'))
    except ValueError:
        messagebox.showerror("Erro", "Coordenadas devem ser números válidos!")
        return
    
    # 3. Pedir tamanho do buffer
    while True:
        buffer_size_str = simpledialog.askstring(
            "Tamanho do Buffer",
            "Introduza o tamanho do buffer em metros (1000 a 100000):",
            parent=root,
            initialvalue="1000"
        )
        if buffer_size_str is None:
            messagebox.showerror("Erro", "Tamanho do buffer é obrigatório!")
            return
        try:
            buffer_size = int(buffer_size_str)
            if 1000 <= buffer_size <= 100000:
                break
            else:
                messagebox.showerror("Erro", "O valor deve estar entre 1000 e 100000 metros.")
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número inteiro válido.")

    # 4. Selecionar pasta de destino
    base_path = filedialog.askdirectory(
        title="Selecione a pasta onde guardar o projeto", 
        initialdir=config_loader.get_path('base_path_tos')
    )
    if not base_path:
        messagebox.showerror("Erro", "Pasta de destino é obrigatória!")
        return
    
    # 5. Nome do projeto
    project_name = simpledialog.askstring(
        "Nome do Projeto", 
        "Insira o nome da pasta do projeto:", 
        initialvalue=f"Projeto_{lat:.4f}_{lon:.4f}", 
        parent=root
    )
    if not project_name:
        messagebox.showerror("Erro", "Nome do projeto é obrigatório!")
        return
    
    # 6. Criar estrutura de pastas e shapefiles
    folder_name = project_name
    project_folder = os.path.join(base_path, folder_name)
    shp_folder = os.path.join(project_folder, 'shp')
    os.makedirs(shp_folder, exist_ok=True)
    
    # Criar ponto
    point = Point(lon, lat)
    gdf_point = gpd.GeoDataFrame({'ID': [project_name]}, geometry=[point], crs="EPSG:4326")
    point_shp = os.path.join(shp_folder, f'ponto_{project_name}.shp')
    gdf_point.to_file(point_shp)
    
    # Criar buffer
    utm_crs = CRS.from_epsg(3763)
    gdf_utm = gdf_point.to_crs(utm_crs)
    buffer = gdf_utm.buffer(buffer_size)
    gdf_buffer = gpd.GeoDataFrame({'ID': [project_name]}, geometry=buffer, crs=utm_crs)
    buffer_shp = os.path.join(shp_folder, f'buffer_{project_name}_{buffer_size//1000}km.shp')
    gdf_buffer.to_crs("EPSG:4326").to_file(buffer_shp)
    
    output_dir = project_folder
    nome_id = project_name

    # 7. Verificar se o buffer foi criado
    if not os.path.exists(buffer_shp):
        messagebox.showerror("Erro", f"Shapefile buffer não encontrado: {buffer_shp}")
        return

    # 8. Extrair bbox do buffer shapefile e usar como limite para o downloader
    gdf = gpd.read_file(buffer_shp)
    bbox = list(gdf.to_crs(epsg=4326).total_bounds)  # [minx, miny, maxx, maxy] em WGS84

    # --- Continua o fluxo normal do downloader ---
    username, password = config_loader.get_credentials()
    delay = config_loader.get_setting('download_delay')
    STAC_SEARCH_URL = config_loader.get_url('stac_search')

    print("\n--- DGT CDD Downloader (Modo Coordenadas/SADO) ---")
    print(f"ID: {nome_id}")
    print(f"Bounding box: {bbox}")
    print(f"Output directory: {output_dir}")
    print(f"Delay: {delay}s")

    if not authenticate(username, password):
        sys.exit(1)

    # Converter BooleanVar para dict normal
    produtos_dict = {k: v.get() for k, v in produtos_vars.items()}
    
    print("\nInício do processo de download...\n")
    main(bbox, STAC_SEARCH_URL, output_dir, delay, collections=None, produtos_selecionados=produtos_dict, nome_id=nome_id)

# Substitua o bloco principal por:
if __name__ == "__main__":
    main_popup_and_shapefile()