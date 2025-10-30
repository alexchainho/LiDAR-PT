import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import subprocess
import os
import json
import config_loader
import webbrowser

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
        'censos_shapefile': 'Shapefile Censos:',
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
        
        def browse_path(var=path_var, is_file='csv' in key or 'shapefile' in key):
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
def open_map_picker(parent=None):
    """Abre uma janela com um mapa onde o utilizador pode clicar para obter coordenadas.
    Usa `tkintermapview` se disponível; caso contrário informa para instalar.
    Ao confirmar, copia as coordenadas para o clipboard.
    """
    try:
        from tkintermapview import TkinterMapView
    except Exception:
        # Se tkintermapview não estiver disponível, oferecer uma alternativa no browser
        answer = messagebox.askyesno(
            "Dependência ausente",
            "A biblioteca 'tkintermapview' não está instalada no venv.\n"
            "Deseja abrir um mapa no navegador para selecionar coordenadas manualmente?\n\n"
            "(Se preferir instalar a dependência, ative o venv e execute: pip install tkintermapview)")
        if answer:
            webbrowser.open("https://www.latlong.net/convert-address-to-lat-long.html")
        return None

    win = tk.Toplevel(parent if parent else None)
    win.title("Selecionar Coordenadas no Mapa - ESRI World Imagery")
    win.geometry("900x700")

    # Frame para o mapa
    map_frame = tk.Frame(win)
    map_frame.pack(fill="both", expand=True, padx=5, pady=5)

    map_widget = TkinterMapView(map_frame, width=890, height=620, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    
    # Configurar mapa base ESRI World Imagery (Satélite)
    # Importante: set_tile_server ANTES de set_position
    map_widget.set_tile_server(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
        max_zoom=20
    )
    
    # Forçar atualização do canvas
    win.update_idletasks()
    
    # Carregar e adicionar limite de Portugal
    try:
        import geopandas as gpd
        portugal_shp = config_loader.get_path("portugal_shapefile")
        gdf_portugal = gpd.read_file(portugal_shp)
        
        # Reprojetar para WGS84 (EPSG:4326) se necessário
        if gdf_portugal.crs and gdf_portugal.crs.to_epsg() != 4326:
            gdf_portugal = gdf_portugal.to_crs(epsg=4326)
        
        # Adicionar polígonos de Portugal ao mapa
        for idx, row in gdf_portugal.iterrows():
            geom = row.geometry
            if geom.geom_type == 'Polygon':
                coords = [(lat, lon) for lon, lat in geom.exterior.coords]
                map_widget.set_polygon(coords, outline_color="yellow", border_width=3, fill_color=None, name=f"Portugal_{idx}")
            elif geom.geom_type == 'MultiPolygon':
                for poly in geom.geoms:
                    coords = [(lat, lon) for lon, lat in poly.exterior.coords]
                    map_widget.set_polygon(coords, outline_color="yellow", border_width=3, fill_color=None, name=f"Portugal_{idx}")
        
        print(f"✅ Limite de Portugal carregado: {len(gdf_portugal)} geometrias")
    except Exception as e:
        print(f"⚠️ Erro ao carregar limite de Portugal: {e}")
    
    # Centrar em Portugal com zoom apropriado
    map_widget.set_position(39.5, -8.0)  # Centro de Portugal
    map_widget.set_zoom(7)  # Zoom inicial para ver Portugal inteiro

    selected = {"marker": None, "coords": None}

    def on_map_click(coords):
        """Callback quando o utilizador clica no mapa.
        coords é uma tupla (latitude, longitude)
        """
        lat, lon = coords
        print(f"Clique no mapa: {lat}, {lon}")  # Debug
        
        if selected["marker"]:
            selected["marker"].delete()  # Remover marcador anterior
        
        selected["marker"] = map_widget.set_marker(lat, lon, text="Selecionado")
        selected["coords"] = (lat, lon)

    # Adicionar callback de clique no mapa
    map_widget.add_left_click_map_command(on_map_click)

    btn_frame = tk.Frame(win)
    btn_frame.pack(fill='x')

    def confirmar():
        if not selected["coords"]:
            messagebox.showwarning("Aviso", "Nenhuma coordenada selecionada no mapa.")
            return
        lat, lon = selected["coords"]
        # copiar para clipboard da aplicação principal
        try:
            win.clipboard_clear()
            win.clipboard_append(f"{lat:.6f},{lon:.6f}")
        except Exception:
            pass
        messagebox.showinfo("Coordenadas", f"Coordenadas copiadas para o clipboard:\n{lat:.6f}, {lon:.6f}")
        win.destroy()

    def cancelar():
        win.destroy()

    tk.Button(btn_frame, text="Confirmar", command=confirmar, bg="#007ACC", fg="white").pack(side='left', padx=10, pady=6)
    tk.Button(btn_frame, text="Cancelar", command=cancelar).pack(side='left', padx=10, pady=6)

    return None

# Função para abrir a janela de seleção de projeto

def selecionar_processo():
    root = tk.Tk()
    root.withdraw()
    
    # Variáveis para checkboxes
    mds_var = tk.BooleanVar(value=True)
    laz_var = tk.BooleanVar(value=False)

    def abrir_buffer():
        script_path = os.path.join(os.path.dirname(__file__), 'processo_por_buffer.py')
        args = ['python', script_path]
        if mds_var.get() and not laz_var.get():
            args.append('--tipo=MDS')
        elif laz_var.get() and not mds_var.get():
            args.append('--tipo=LAZ')
        # ambos ou nenhum: default (ambos)
        subprocess.Popen(args)
        root.destroy()

    win = tk.Toplevel()
    win.title("Selecionar Processo")
    win.geometry("350x250")
    
    # Botões de topo (Configurações e Ajuda)
    top_frame = tk.Frame(win)
    top_frame.pack(fill='x', padx=10, pady=5)
    
    tk.Button(top_frame, text="⚙️ Configurações", command=abrir_configuracoes, 
              width=15, bg="#007ACC", fg="white").pack(side='left', padx=2)
    tk.Button(top_frame, text="❓ Ajuda", command=mostrar_ajuda, 
              width=10, bg="#4CAF50", fg="white").pack(side='left', padx=2)
    
    tk.Label(win, text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━").pack(pady=5)
    
    tk.Label(win, text="Escolha o tipo de dados a descarregar:").pack(padx=20, pady=(10,0))
    tk.Checkbutton(win, text="MDS-50cm", variable=mds_var).pack(anchor='w', padx=30)
    tk.Checkbutton(win, text="LAZ", variable=laz_var).pack(anchor='w', padx=30)
    tk.Label(win, text="Escolha o tipo de projeto:").pack(padx=20, pady=(10,0))
    # Botão para selecionar coordenadas num mapa (útil antes de abrir os processos)
    tk.Button(win, text="Selecionar Coordenadas no Mapa", command=lambda: open_map_picker(win), width=30).pack(pady=5)
    tk.Button(win, text="Processo por Buffer", command=abrir_buffer, width=25).pack(pady=5)
    
    # Info no rodapé
    info_label = tk.Label(win, text="v2.0 | Configurável via interface", 
                          font=("Arial", 8), fg="gray")
    info_label.pack(side='bottom', pady=5)
    
    win.mainloop()

if __name__ == "__main__":
    selecionar_processo()
