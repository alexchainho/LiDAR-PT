import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import subprocess
import os
import json
import config_loader
import webbrowser
import sys

# Função para validar e solicitar credenciais se necessário
def validar_credenciais():
    """
    Valida se as credenciais estão configuradas corretamente.
    Se estiverem vazias ou com valores padrão, solicita ao utilizador.
    Retorna True se as credenciais foram validadas/configuradas com sucesso.
    """
    try:
        config = config_loader.load_config()
        username = config.get('credentials', {}).get('username', '')
        password = config.get('credentials', {}).get('password', '')
        
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # Erro de encoding ou JSON inválido
        root = tk.Tk()
        root.withdraw()
        
        resposta = messagebox.askyesno(
            "Erro no Ficheiro de Configuração",
            f"Erro ao ler o ficheiro config\\caminhos.json:\n\n"
            f"{str(e)}\n\n"
            f"Possível problema de encoding UTF-8.\n\n"
            f"Deseja recriar o ficheiro a partir do template?",
            icon='error'
        )
        
        root.destroy()
        
        if resposta:
            # Recriar a partir do template
            try:
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                config_path = os.path.join(script_dir, 'config', 'caminhos.json')
                template_path = os.path.join(script_dir, 'config', 'caminhos.json.template')
                
                if os.path.exists(template_path):
                    import shutil
                    # Fazer backup
                    backup_path = config_path + '.backup'
                    if os.path.exists(config_path):
                        shutil.copy2(config_path, backup_path)
                    
                    # Copiar template
                    shutil.copy2(template_path, config_path)
                    
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showinfo(
                        "Ficheiro Recriado",
                        f"Ficheiro recriado a partir do template.\n\n"
                        f"Backup guardado em:\n{backup_path}\n\n"
                        f"Por favor, configure as credenciais novamente."
                    )
                    root.destroy()
                    
                    # Recarregar e continuar com validação
                    config = config_loader.load_config()
                    username = config.get('credentials', {}).get('username', '')
                    password = config.get('credentials', {}).get('password', '')
                else:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror(
                        "Erro",
                        "Template não encontrado.\n\n"
                        "Por favor, corrija manualmente:\n"
                        "config\\caminhos.json"
                    )
                    root.destroy()
                    return False
                    
            except Exception as fix_error:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível recriar o ficheiro:\n{str(fix_error)}"
                )
                root.destroy()
                return False
        else:
            return False
    
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Erro",
            f"Erro ao validar credenciais:\n{str(e)}\n\n"
            "Verifique o ficheiro config\\caminhos.json"
        )
        root.destroy()
        return False
    
    # Verificar se credenciais são válidas (não vazias e não valores padrão)
    credenciais_invalidas = (
        not username or 
        not password or
        username.strip() == '' or
        password.strip() == '' or
        username == 'SEU_EMAIL@AQUI.PT' or
        password == 'SUA_PASSWORD_AQUI'
    )
    
    if credenciais_invalidas:
        # Tentar executar o script PowerShell de configuração de credenciais
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ps_script = os.path.join(script_dir, 'config', 'setup_inicial.ps1')
        
        # Mostrar aviso
        root = tk.Tk()
        root.withdraw()
        
        resposta = messagebox.askokcancel(
            "Credenciais DGT Necessárias",
            "As credenciais de acesso ao Centro de Descargas da DGT não estão configuradas ou são inválidas.\n\n"
            "É necessário configurar:\n"
            "• Username (Email de registo)\n"
            "• Password\n\n"
            "Deseja configurar agora?\n\n"
            "Nota: Sem credenciais válidas não é possível descarregar dados.",
            icon='warning'
        )
        
        root.destroy()
        
        if not resposta:
            return False
        
        # Executar popup de credenciais PowerShell
        try:
            ps_command = f'''
$scriptPath = "{ps_script}"
. $scriptPath
$creds = Show-CredentialsDialog
if ($creds) {{
    $configPath = "{os.path.join(script_dir, 'config', 'caminhos.json')}"
    if (Test-Path $configPath) {{
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        $config.credentials.username = $creds.Username
        $config.credentials.password = $creds.Password
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
        exit 0
    }} else {{
        exit 2
    }}
}} else {{
    exit 1
}}
'''
            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_command],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Credenciais configuradas com sucesso
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo(
                    "Sucesso",
                    "Credenciais configuradas com sucesso!\n\nA aplicação será iniciada."
                )
                root.destroy()
                return True
            elif result.returncode == 1:
                # Utilizador cancelou
                return False
            else:
                # Erro ao configurar
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Erro",
                    "Não foi possível configurar as credenciais.\n\n"
                    "Por favor, edite manualmente o ficheiro:\n"
                    "config\\caminhos.json"
                )
                root.destroy()
                return False
                
        except Exception as e:
            # Fallback: solicitar via Tkinter simples
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showinfo(
                "Configuração de Credenciais",
                "Por favor, insira suas credenciais de acesso ao Centro de Descargas da DGT.\n\n"
                "Se não tem conta, crie em:\nhttps://cdd.dgterritorio.gov.pt/dgt-fe"
            )
            
            username = simpledialog.askstring(
                "Username DGT",
                "Insira o username (email):",
                parent=root
            )
            
            if not username:
                root.destroy()
                return False
            
            password = simpledialog.askstring(
                "Password DGT",
                "Insira a password:",
                parent=root,
                show='*'
            )
            
            root.destroy()
            
            if not password:
                return False
            
            # Guardar credenciais
            try:
                script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                config_path = os.path.join(script_dir, 'config', 'caminhos.json')
                config['credentials']['username'] = username.strip()
                config['credentials']['password'] = password
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo(
                    "Sucesso",
                    "Credenciais configuradas com sucesso!"
                )
                root.destroy()
                return True
                
            except Exception as save_error:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Erro",
                    f"Erro ao guardar credenciais:\n{str(save_error)}"
                )
                root.destroy()
                return False
    
    # Credenciais válidas
    return True
# Função para mostrar ajuda
def mostrar_ajuda():
    """Mostra informações de ajuda"""
    ajuda_texto = """
    🚀 DGT Rasters - Guia Rápido
    
    📋 COMO USAR:
    
    1️⃣ CONFIGURAÇÕES (⚙️)
       • Edite credenciais DGT
       • Configure caminhos do sistema
       • Ajuste timeouts e delays
    
    2️⃣ TIPO DE DADOS
       • MDS-50cm: Modelo Digital de Superfície
       • LAZ: Nuvem de pontos (LiDAR)
       • Pode selecionar ambos
    
    3️⃣ TIPO DE PROJETO
       • Buffer: Usa SADO ou coordenadas
         → Cria buffer automático
       • Localidade: Usa coordenadas
         → Identifica localidade nos censos
    
    💡 DICAS:
    • Configure credenciais antes do 1º uso
    • Verifique caminhos em Configurações
    • Password fica guardada localmente
    
    📖 Documentação completa: GUIA_RAPIDO.md
    """
    
    messagebox.showinfo("Ajuda - DGT Rasters", ajuda_texto)

# Função para abrir configurações
def abrir_configuracoes():
    """Abre janela para editar configurações"""
    config = config_loader.load_config()
    
    config_win = tk.Toplevel()
    config_win.title("Configurações")
    config_win.geometry("600x700")
    
    # Frame com scroll
    canvas = tk.Canvas(config_win)
    scrollbar = tk.Scrollbar(config_win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # === CREDENCIAIS ===
    tk.Label(scrollable_frame, text="CREDENCIAIS", font=("Arial", 12, "bold")).pack(pady=(10,5))
    
    tk.Label(scrollable_frame, text="Username:").pack(anchor='w', padx=20)
    username_var = tk.StringVar(value=config['credentials']['username'])
    tk.Entry(scrollable_frame, textvariable=username_var, width=50).pack(padx=20, pady=2)
    
    tk.Label(scrollable_frame, text="Password:").pack(anchor='w', padx=20)
    password_var = tk.StringVar(value=config['credentials']['password'])
    tk.Entry(scrollable_frame, textvariable=password_var, width=50, show="*").pack(padx=20, pady=2)
    
    # === CAMINHOS ===
    tk.Label(scrollable_frame, text="CAMINHOS", font=("Arial", 12, "bold")).pack(pady=(15,5))
    
    path_vars = {}
    path_labels = {
        'base_path_tos': 'Pasta Base TOs:',
        'csv_ocorrencias': 'CSV Ocorrências:',
        'geopackage': 'GeoPackage DGT:',
        'localidades_base': 'Pasta Localidades:'
    }
    
    for key, label in path_labels.items():
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(frame, text=label).pack(anchor='w')
        path_var = tk.StringVar(value=config['paths'].get(key, ''))
        path_vars[key] = path_var
        
        entry_frame = tk.Frame(frame)
        entry_frame.pack(fill='x')
        
        entry = tk.Entry(entry_frame, textvariable=path_var, width=40)
        entry.pack(side='left', fill='x', expand=True)
        
        def browse_path(var=path_var, is_file='csv' in key or 'geopackage' in key):
            if is_file:
                path = filedialog.askopenfilename(initialdir=os.path.dirname(var.get()) if var.get() else '/')
            else:
                path = filedialog.askdirectory(initialdir=var.get() if var.get() else '/')
            if path:
                var.set(path)
        
        tk.Button(entry_frame, text="...", command=browse_path, width=3).pack(side='left', padx=5)
    
    # === CONFIGURAÇÕES ===
    tk.Label(scrollable_frame, text="CONFIGURAÇÕES", font=("Arial", 12, "bold")).pack(pady=(15,5))
    
    settings_frame = tk.Frame(scrollable_frame)
    settings_frame.pack(fill='x', padx=20, pady=5)
    
    tk.Label(settings_frame, text="Download Delay (s):").grid(row=0, column=0, sticky='w', pady=2)
    delay_var = tk.DoubleVar(value=config['settings']['download_delay'])
    tk.Entry(settings_frame, textvariable=delay_var, width=10).grid(row=0, column=1, sticky='w', padx=5)
    
    tk.Label(settings_frame, text="Session Timeout (s):").grid(row=1, column=0, sticky='w', pady=2)
    timeout_var = tk.IntVar(value=config['settings']['session_timeout'])
    tk.Entry(settings_frame, textvariable=timeout_var, width=10).grid(row=1, column=1, sticky='w', padx=5)
    
    def salvar_configuracoes():
        """Salva as configurações no ficheiro JSON"""
        try:
            config['credentials']['username'] = username_var.get()
            config['credentials']['password'] = password_var.get()
            
            for key, var in path_vars.items():
                config['paths'][key] = var.get()
            
            config['settings']['download_delay'] = delay_var.get()
            config['settings']['session_timeout'] = timeout_var.get()
            
            config_path = os.path.join(os.path.dirname(__file__), 'caminhos.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Sucesso", "Configurações guardadas com sucesso!")
            config_win.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar configurações: {e}")
    
    # Botões
    button_frame = tk.Frame(scrollable_frame)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Guardar", command=salvar_configuracoes, width=15, bg="green", fg="white").pack(side='left', padx=5)
    tk.Button(button_frame, text="Cancelar", command=config_win.destroy, width=15).pack(side='left', padx=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# --- Seletor de coordenadas via mapa ---
def open_map_picker(parent=None, produtos_vars=None):
    """Abre mapa para selecionar coordenadas e inicia processo de download.
    Fluxo completo: Mapa → Coordenadas → Buffer → Pasta → Download
    """
    try:
        from tkintermapview import TkinterMapView
        import subprocess
        import geopandas as gpd
        from shapely.geometry import Point
        from pyproj import CRS
    except Exception as e:
        messagebox.showerror(
            "Dependência ausente",
            f"Erro ao importar dependências: {e}\n\n"
            "Certifique-se que tkintermapview e geopandas estão instalados.")
        return None

    win = tk.Toplevel(parent if parent else None)
    win.title("Selecionar Localização no Mapa")
    win.geometry("900x700")

    # Frame para o mapa
    map_frame = tk.Frame(win)
    map_frame.pack(fill="both", expand=True, padx=5, pady=5)

    map_widget = TkinterMapView(map_frame, width=890, height=620, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    
    # Configurar mapa base ESRI World Imagery
    map_widget.set_tile_server(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
        max_zoom=20
    )
    
    win.update_idletasks()
    
    # Carregar limite de Portugal
    try:
        gpkg_path = config_loader.get_path("geopackage")
        gdf_portugal = gpd.read_file(gpkg_path, layer="portugal")
        
        if gdf_portugal.crs and gdf_portugal.crs.to_epsg() != 4326:
            gdf_portugal = gdf_portugal.to_crs(epsg=4326)
        
        for idx, row in gdf_portugal.iterrows():
            geom = row.geometry
            if geom.geom_type == 'Polygon':
                coords = [(lat, lon) for lon, lat in geom.exterior.coords]
                map_widget.set_polygon(coords, outline_color="yellow", border_width=3, fill_color=None, name=f"Portugal_{idx}")
            elif geom.geom_type == 'MultiPolygon':
                for poly in geom.geoms:
                    coords = [(lat, lon) for lon, lat in poly.exterior.coords]
                    map_widget.set_polygon(coords, outline_color="yellow", border_width=3, fill_color=None, name=f"Portugal_{idx}")
    except Exception as e:
        print(f"⚠️ Erro ao carregar limite de Portugal: {e}")
    
    # Centrar em Portugal
    map_widget.set_position(39.5, -8.0)
    map_widget.set_zoom(7)

    selected = {"marker": None, "coords": None}

    def on_map_click(coords):
        lat, lon = coords
        if selected["marker"]:
            selected["marker"].delete()
        selected["marker"] = map_widget.set_marker(lat, lon, text="📍 Selecionado")
        selected["coords"] = (lat, lon)

    map_widget.add_left_click_map_command(on_map_click)

    btn_frame = tk.Frame(win)
    btn_frame.pack(fill='x', pady=5)

    def iniciar_download():
        if not selected["coords"]:
            messagebox.showwarning("Aviso", "Selecione uma localização no mapa primeiro!")
            return
        
        lat, lon = selected["coords"]
        win.destroy()  # Fechar mapa
        
        # Pedir tamanho do buffer
        while True:
            buffer_km_str = simpledialog.askstring(
                "Tamanho do Buffer",
                f"Coordenadas: {lat:.6f}, {lon:.6f}\n\n"
                "Introduza o tamanho do buffer:\n"
                "• Em metros: 100 a 999 (ex: 500)\n"
                "• Em km: 1 a 15 (ex: 5.5):",
                initialvalue="1"
            )
            if buffer_km_str is None:
                return  # Cancelado
            try:
                buffer_value = float(buffer_km_str.replace(',', '.'))
                
                # Se valor < 100, assumir que é em km
                if buffer_value < 100:
                    buffer_km = buffer_value
                    if 0.1 <= buffer_km <= 15:
                        buffer_metros = int(buffer_km * 1000)
                        break
                    else:
                        messagebox.showerror("Erro", "O buffer em km deve estar entre 0.1 e 15 km.")
                # Se valor >= 100, assumir que é em metros
                else:
                    buffer_metros = int(buffer_value)
                    if 100 <= buffer_metros <= 15000:
                        buffer_km = buffer_metros / 1000
                        break
                    else:
                        messagebox.showerror("Erro", "O buffer em metros deve estar entre 100 e 15000 m.")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido. Use apenas números.")
        
        # Perguntar se pretende unir rasters MDS/MDT
        unir_rasters = messagebox.askyesno(
            "Unir Rasters",
            "Pretende unir automaticamente os rasters MDS e MDT?\n\n"
            "Se SIM: Cria ficheiros únicos (ex: MDS-50cm.tif, MDT-2m.tif)\n"
            "Se NÃO: Mantém ficheiros individuais da grelha DGT"
        )
        
        # Pedir pasta de destino
        base_path = filedialog.askdirectory(
            title="Selecione a pasta onde guardar o projeto",
            initialdir=config_loader.get_path('base_path_tos')
        )
        if not base_path:
            messagebox.showwarning("Aviso", "Nenhuma pasta selecionada. Processo cancelado.")
            return
        
        # Pedir nome do projeto
        project_name = simpledialog.askstring(
            "Nome do Projeto",
            "Insira o nome da pasta do projeto:",
            initialvalue=f"Projeto_{lat:.4f}_{lon:.4f}"
        )
        if not project_name:
            messagebox.showwarning("Aviso", "Nome do projeto é obrigatório!")
            return
        
        # Criar estrutura de pastas
        project_folder = os.path.join(base_path, project_name)
        shp_folder = os.path.join(project_folder, 'shp')
        os.makedirs(shp_folder, exist_ok=True)
        
        # Criar shapefile de ponto
        point = Point(lon, lat)
        gdf_point = gpd.GeoDataFrame({'ID': [project_name]}, geometry=[point], crs="EPSG:4326")
        point_shp = os.path.join(shp_folder, f'ponto_{project_name}.shp')
        gdf_point.to_file(point_shp)
        
        # Criar buffer
        utm_crs = CRS.from_epsg(3763)
        gdf_utm = gdf_point.to_crs(utm_crs)
        buffer_geom = gdf_utm.buffer(buffer_metros)
        gdf_buffer = gpd.GeoDataFrame({'ID': [project_name]}, geometry=buffer_geom, crs=utm_crs)
        buffer_shp = os.path.join(shp_folder, f'buffer_{project_name}_{buffer_km}km.shp')
        gdf_buffer.to_crs("EPSG:4326").to_file(buffer_shp)
        
        messagebox.showinfo(
            "Projeto Criado",
            f"📁 Pasta: {project_folder}\n"
            f"📍 Coordenadas: {lat:.6f}, {lon:.6f}\n"
            f"⭕ Buffer: {buffer_km} km\n\n"
            "Iniciando download..."
        )
        
        # Preparar argumentos para processo_por_buffer.py
        script_path = os.path.join(os.path.dirname(__file__), 'processo_por_buffer.py')
        args = ['python', script_path]
        
        # Passar produtos selecionados
        if produtos_vars:
            if produtos_vars['Todos'].get():
                args.append('--produtos=TODOS')
            else:
                selecionados = [k for k, v in produtos_vars.items() if v.get() and k != 'Todos']
                if selecionados:
                    args.append(f'--produtos={",".join(selecionados)}')
        
        # Passar coordenadas, buffer, pasta e opção de merge
        args.extend([
            f'--lat={lat}',
            f'--lon={lon}',
            f'--buffer={buffer_metros}',
            f'--output={project_folder}',
            f'--nome={project_name}'
        ])
        
        # Adicionar flag de merge se selecionado
        if unir_rasters:
            args.append('--merge')
        
        # Lançar processo de download
        subprocess.Popen(args)
        
        # Fechar janela do mapa
        win.destroy()
        
        # Fechar janela principal do seletor (parent)
        if parent:
            parent.destroy()

    def cancelar():
        win.destroy()

    tk.Button(btn_frame, text="✅ Iniciar Download", command=iniciar_download, 
              bg="#28a745", fg="white", width=20, height=2).pack(side='left', padx=10)
    tk.Button(btn_frame, text="❌ Cancelar", command=cancelar, 
              width=15, height=2).pack(side='left', padx=10)

    return None

# Função para abrir a janela de seleção de projeto

def selecionar_processo():
    # Validar credenciais antes de iniciar a interface
    if not validar_credenciais():
        # Utilizador cancelou ou houve erro - encerrar aplicação
        return
    
    root = tk.Tk()
    root.withdraw()
    
    # Variáveis para checkboxes de produtos
    produtos_vars = {
        'LAZ': tk.BooleanVar(value=True),
        'MDS-2m': tk.BooleanVar(value=False),
        'MDS-50cm': tk.BooleanVar(value=True),
        'MDT-2m': tk.BooleanVar(value=False),
        'MDT-50cm': tk.BooleanVar(value=False),
        'Todos': tk.BooleanVar(value=False)
    }

    def toggle_todos():
        """Marca/desmarca todos os produtos"""
        todos_value = produtos_vars['Todos'].get()
        for key in produtos_vars:
            if key != 'Todos':
                produtos_vars[key].set(todos_value)

    def abrir_buffer():
        script_path = os.path.join(os.path.dirname(__file__), 'processo_por_buffer.py')
        args = ['python', script_path]
        
        # Passar produtos selecionados como argumentos
        selecionados = []
        if produtos_vars['Todos'].get():
            args.append('--produtos=TODOS')
        else:
            for produto, var in produtos_vars.items():
                if var.get() and produto != 'Todos':
                    selecionados.append(produto)
            if selecionados:
                args.append(f'--produtos={",".join(selecionados)}')
        
        subprocess.Popen(args)
        win.destroy()

    win = tk.Toplevel()
    win.title("Selecionar Processo")
    win.geometry("400x450")
    
    # Botões de topo (Configurações e Ajuda)
    top_frame = tk.Frame(win)
    top_frame.pack(fill='x', padx=10, pady=5)
    
    tk.Button(top_frame, text="⚙️ Configurações", command=abrir_configuracoes, 
              width=15, bg="#007ACC", fg="white").pack(side='left', padx=2)
    tk.Button(top_frame, text="❓ Ajuda", command=mostrar_ajuda, 
              width=10, bg="#4CAF50", fg="white").pack(side='left', padx=2)
    
    tk.Label(win, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━").pack(pady=5)
    
    # Frame para produtos
    produtos_frame = tk.LabelFrame(win, text="Produtos a descarregar", padx=10, pady=10)
    produtos_frame.pack(padx=20, pady=10, fill='both')
    
    tk.Checkbutton(produtos_frame, text="☑ Todos os produtos", variable=produtos_vars['Todos'], 
                  command=toggle_todos, font=("Arial", 9, "bold")).pack(anchor='w', pady=2)
    
    tk.Label(produtos_frame, text="").pack()  # Espaçador
    
    tk.Checkbutton(produtos_frame, text="LAZ (Nuvem de pontos LiDAR)", 
                  variable=produtos_vars['LAZ']).pack(anchor='w', padx=20, pady=2)
    tk.Checkbutton(produtos_frame, text="MDS-2m (Modelo Digital Superfície 2m)", 
                  variable=produtos_vars['MDS-2m']).pack(anchor='w', padx=20, pady=2)
    tk.Checkbutton(produtos_frame, text="MDS-50cm (Modelo Digital Superfície 50cm)", 
                  variable=produtos_vars['MDS-50cm']).pack(anchor='w', padx=20, pady=2)
    tk.Checkbutton(produtos_frame, text="MDT-2m (Modelo Digital Terreno 2m)", 
                  variable=produtos_vars['MDT-2m']).pack(anchor='w', padx=20, pady=2)
    tk.Checkbutton(produtos_frame, text="MDT-50cm (Modelo Digital Terreno 50cm)", 
                  variable=produtos_vars['MDT-50cm']).pack(anchor='w', padx=20, pady=2)
    
    tk.Label(win, text="Escolha o tipo de projeto:", font=("Arial", 9, "bold")).pack(padx=20, pady=(10,5))
    
    # Botões de ação
    tk.Button(win, text="🗺️ Selecionar no Mapa e Iniciar Download", 
              command=lambda: open_map_picker(win, produtos_vars), 
              width=35, bg="#FFA500", fg="white", height=2).pack(pady=5)
    tk.Button(win, text="📍 Processo por Buffer (Avançado)", command=abrir_buffer, 
              width=35, bg="#28a745", fg="white").pack(pady=5)
    
    # Info no rodapé
    info_label = tk.Label(win, text="v2.1 | Seleção de produtos disponível", 
                          font=("Arial", 8), fg="gray")
    info_label.pack(side='bottom', pady=5)
    
    win.mainloop()

if __name__ == "__main__":
    selecionar_processo()
