import os
os.environ['PROJ_LIB'] = r"C:\Users\UEPS_AC\AppData\Local\Programs\Python\Python313\Lib\site-packages\pyproj\proj_dir\share\proj"
import tkinter as tk
from tkinter import simpledialog, messagebox
import geopandas as gpd
from shapely.geometry import Point
from pyproj import CRS
# --- Dependências para download DGT ---
import requests
import time
import sys
import urllib.parse
import pandas as pd
from html.parser import HTMLParser
import laspy
import rasterio
from rasterio.merge import merge

# Caminho para a camada censos
CENSOS_PATH = r"D:\CSTE\DGT_Rasters\dados\Lugares_2021.shp"

# Função para criar pasta do projeto

def criar_pasta_localidade(nome_localidade, base_path):
    pasta = os.path.join(base_path, 'localidades', nome_localidade)
    os.makedirs(pasta, exist_ok=True)
    return pasta

# Função principal do processo por localidade

def processo_por_localidade():
    import sys
    tipo = None
    for arg in sys.argv:
        if arg.startswith('--tipo='):
            tipo = arg.split('=')[1].upper()
    root = tk.Tk()
    root.withdraw()
    # Pedir coordenadas ao utilizador
    lat_str = simpledialog.askstring("Latitude", "Insira a latitude (coordenadas decimais):", parent=root)
    if not lat_str:
        messagebox.showerror("Erro", "Latitude é obrigatória!")
        return
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

    # Ler camada censos
    censos_gdf = gpd.read_file(CENSOS_PATH)
    # Garantir que a camada censos está em 3763
    if censos_gdf.crs is None or censos_gdf.crs.to_epsg() != 3763:
        censos_gdf = censos_gdf.to_crs(epsg=3763)

    # Converter ponto para 3763
    ponto = Point(lon, lat)
    ponto_gdf = gpd.GeoDataFrame(geometry=[ponto], crs="EPSG:4326").to_crs(epsg=3763)

    # Intersetar ponto com censos
    intersec = gpd.sjoin(censos_gdf, ponto_gdf, how='inner', predicate='intersects')
    if intersec.empty:
        messagebox.showerror("Erro", "O ponto não intersecta nenhuma localidade.")
        return
    poligono = intersec.iloc[0]
    nome_localidade = poligono['LUG21DESIG']


    # Pasta base do projeto (ajustar conforme necessário)
    base_path = r"D:\CSTE\DGT_Rasters"
    pasta_localidade = criar_pasta_localidade(nome_localidade, base_path)
    shp_path = os.path.join(pasta_localidade, f"{nome_localidade}.shp")
    # Exportar shapefile no SRC 3763 (sem passar 'crs')
    intersec[[*censos_gdf.columns]].to_file(shp_path)



    # Extrair bbox da extensão da localidade (em WGS84)
    gdf_poly = gpd.read_file(shp_path)
    if gdf_poly.crs is None or gdf_poly.crs.to_epsg() != 3763:
        gdf_poly = gdf_poly.to_crs(epsg=3763)
    bbox = list(gdf_poly.to_crs(epsg=4326).total_bounds)


    # --- Processo de download DGT ---
    # Funções essenciais do downloader (copiadas de dgt_cdd_downloader.py)
    # (Para manter independente, não faz import cruzado)
    auth_state = {
        "session": None,
        "username": 'chainho.ac@gnr.pt',
        "password": 'G_nr2050086',
        "last_auth_time": 0,
        "download_counter": 0,
    }
    SESSION_TIMEOUT = 25 * 60
    class AuthenticationError(Exception): pass
    class KeycloakFormParser(HTMLParser):
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
    def is_session_expired():
        return (time.time() - auth_state["last_auth_time"]) > SESSION_TIMEOUT
    def is_session_valid(stac_url):
        try:
            test_payload = {"bbox": [-9.0, 38.0, -8.0, 39.0], "limit": 1}
            response = auth_state["session"].post(stac_url, json=test_payload, timeout=15)
            return response.status_code == 200
        except Exception:
            return False
    def authenticate(username, password):
        auth_base_url = "https://auth.cdd.dgterritorio.gov.pt/realms/dgterritorio/protocol/openid-connect"
        redirect_uri = "https://cdd.dgterritorio.gov.pt/auth/callback"
        client_id = "aai-oidc-dgt"
        main_site = "https://cdd.dgterritorio.gov.pt"
        stac_url = "https://cdd.dgterritorio.gov.pt/dgt-be/v1/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        try:
            session = requests.Session()
            session.headers.update(headers)
            session.get(main_site, timeout=30)
            auth_params = {'client_id': client_id, 'response_type': 'code', 'redirect_uri': redirect_uri, 'scope': 'openid profile email'}
            full_auth_url = f"{auth_base_url}/auth?" + urllib.parse.urlencode(auth_params)
            response = session.get(full_auth_url, timeout=30)
            parser = KeycloakFormParser()
            parser.feed(response.text)
            if not parser.form_action: raise AuthenticationError("Could not find login form.")
            login_data = parser.form_data.copy()
            login_data.update({'username': username, 'password': password})
            login_url = parser.form_action if not parser.form_action.startswith('/') else f"https://auth.cdd.dgterritorio.gov.pt{parser.form_action}"
            login_headers = headers.copy()
            login_headers.update({'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://auth.cdd.dgterritorio.gov.pt', 'Referer': response.url})
            response = session.post(login_url, data=login_data, headers=login_headers, allow_redirects=True, timeout=30)
            if response.url.startswith(main_site):
                test_response = session.post(stac_url, json={"bbox": [-9.0, 38.0, -8.0, 39.0], "limit": 1}, timeout=30)
                if test_response.status_code == 200:
                    auth_state.update({"session": session, "username": username, "password": password, "last_auth_time": time.time()})
                    return True
                else:
                    raise AuthenticationError(f"STAC API returned status {test_response.status_code}.")
            else:
                raise AuthenticationError("Authentication failed. Unexpected redirection URL.")
        except Exception as e:
            print(f"Erro de autenticação: {e}")
            return False
    def search_stac_api(stac_url, bbox, collections=None, delay=0.2):
        payload = {"bbox": bbox, "limit": 1000}
        if collections:
            payload["collections"] = collections
        time.sleep(delay)
        try:
            response = auth_state["session"].post(stac_url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro na query da API STAC: {e}")
            return {"features": []}
    def get_file_extension(mime_type):
        mime_to_extension = {
            "image/tiff; application=geotiff": ".tif",
            "image/tiff": ".tif",
            "application/vnd.laszip": ".laz",
        }
        return mime_to_extension.get(mime_type, ".bin")

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
                is_mds = ("MDS-50cm" in asset_title or "MDS-50cm" in asset_key or "MDS-50cm" in item_id)
                is_laz = (asset_type == "application/vnd.laszip" or asset_key.lower().endswith("laz") or ".laz" in url or ".laz" in asset_title.lower())
                # Filtro conforme argumento --tipo
                if tipo == "MDS" and not is_mds:
                    continue
                if tipo == "LAZ" and not is_laz:
                    continue
                if not (is_mds or is_laz):
                    continue
                if url and url not in seen_urls:
                    ext = get_file_extension(asset_type)
                    if is_laz and ext != ".laz":
                        ext = ".laz"
                    if is_mds and ext == ".bin":
                        ext = ".tif"
                    urls_per_collection.setdefault(collection, []).append((url, item_id, ext))
                    seen_urls.add(url)
        return urls_per_collection
    def download_file(stac_url, url, item_id, extension, output_dir, delay=5.0):
        auth_state["download_counter"] += 1
        if auth_state["download_counter"] % 10 == 0:
            if is_session_expired() or not is_session_valid(stac_url):
                if not authenticate(auth_state["username"], auth_state["password"]):
                    raise AuthenticationError("Re-authentication failed.")
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
                return True
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError, requests.exceptions.Timeout) as e:
                sys.stdout.write("\n")
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
                sys.stdout.write("\n")
                print(f"Erro no download {url}: {e}")
                return False
        return False
    def choose_collections(stac_url, bbox):
        payload = {"bbox": bbox, "limit": 1000}
        try:
            response = auth_state["session"].post(stac_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Filtrar apenas coleções relevantes
            collections = sorted({item.get("collection") for item in data.get("features", []) if item.get("collection") and ("MDS-50cm" in item.get("collection") or "LAZ" in item.get("collection"))})
            if not collections:
                return None
            return collections
        except Exception as e:
            print(f"Erro ao obter coleções: {e}")
            return None
    def main_download(bbox, output_dir, delay=5.0):
        STAC_SEARCH_URL = "https://cdd.dgterritorio.gov.pt/dgt-be/v1/search"
        username = auth_state["username"]
        password = auth_state["password"]
        if not authenticate(username, password):
            messagebox.showerror("Erro", "Falha na autenticação DGT!")
            return
        collections = choose_collections(STAC_SEARCH_URL, bbox)
        stac_response = search_stac_api(STAC_SEARCH_URL, bbox, collections=collections)
        urls_per_collection = collect_urls_per_collection(stac_response)
        for collection, url_id_ext_pairs in urls_per_collection.items():
            collection_output_dir = os.path.join(output_dir, collection)
            for url, item_id, extension in url_id_ext_pairs:
                download_file(STAC_SEARCH_URL, url, item_id, extension, collection_output_dir, delay)
                # Descompactar LAZ para LAS se necessário
                if extension == ".laz":
                    laz_path = os.path.join(collection_output_dir, f"{item_id}.laz")
                    las_path = os.path.join(collection_output_dir, f"{item_id}.las")
                    try:
                        import importlib
                        if importlib.util.find_spec("lazrs") is None:
                            print(f"Backend 'lazrs' não está instalado. Não é possível descompactar {laz_path}.")
                        else:
                            with laspy.open(laz_path) as lazf:
                                las = lazf.read()
                            las.write(las_path)
                            print(f"Descompactado {laz_path} para {las_path}")
                    except Exception as e:
                        print(f"Erro ao descompactar {laz_path}: {e}")

        # Recorte dos rasters e camadas deve ser feito pelo bbox (extent), não pelo polígono
        # Exemplo para recorte de raster:
        # import rasterio
        # with rasterio.open(raster_path) as src:
        #     out_image, out_transform = rasterio.mask.mask(src, [shapely.geometry.box(*gdf_poly.total_bounds)], crop=True)
        #     # ou usar bbox diretamente
        #     window = rasterio.windows.from_bounds(*gdf_poly.total_bounds, transform=src.transform)
        #     out_image = src.read(window=window)
        #     # salvar...
        print("Processo concluído com sucesso.")

        # --- Merge dos rasters MDS-50cm ---
        try:
            mds_dir = os.path.join(output_dir, 'MDS-50cm')
            if os.path.exists(mds_dir):
                tif_files = [os.path.join(mds_dir, f) for f in os.listdir(mds_dir) if f.lower().endswith('.tif')]
                if len(tif_files) > 1:
                    print(f"A unir {len(tif_files)} rasters MDS-50cm...")
                    src_files_to_mosaic = [rasterio.open(fp) for fp in tif_files]
                    mosaic, out_trans = merge(src_files_to_mosaic)
                    out_meta = src_files_to_mosaic[0].meta.copy()
                    out_meta.update({
                        "driver": "GTiff",
                        "height": mosaic.shape[1],
                        "width": mosaic.shape[2],
                        "transform": out_trans,
                        "crs": "EPSG:3763"  # Força ETRS89 / Portugal TM06
                    })
                    # Herdar nodata se existir
                    if hasattr(src_files_to_mosaic[0], 'nodata') and src_files_to_mosaic[0].nodata is not None:
                        out_meta["nodata"] = src_files_to_mosaic[0].nodata
                    nome_raster = f"{nome_localidade}_mds-50cm.tif"
                    out_path = os.path.join(mds_dir, nome_raster)
                    # Garantir que o array tem 3 dimensões [bands, rows, cols]
                    if mosaic.ndim == 2:
                        mosaic = mosaic[None, ...]
                    with rasterio.open(out_path, "w", **out_meta) as dest:
                        dest.write(mosaic)
                    print(f"Raster unido salvo em: {out_path}")
                elif len(tif_files) == 1:
                    print("Só existe um raster MDS-50cm, não é necessário unir.")
                else:
                    print("Nenhum raster MDS-50cm encontrado para unir.")
        except Exception as e:
            print(f"Erro ao unir rasters MDS-50cm: {e}")

        # Só mostrar popup no fim real
        messagebox.showinfo("Download concluído", f"Download de dados DGT (apenas MDS-50cm e LAZ) concluído para a localidade '{nome_localidade}'.")
        print("Processo concluído com sucesso.")

    # Chamar o download automático
    main_download(bbox, pasta_localidade)

if __name__ == "__main__":
    processo_por_localidade()
