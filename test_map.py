"""
Script de teste para verificar se o mapa ESRI World Imagery carrega no tkintermapview
"""
import tkinter as tk
from tkintermapview import TkinterMapView

def test_map():
    root = tk.Tk()
    root.title("Teste ESRI World Imagery - Portugal")
    root.geometry("900x700")
    
    print("Criando widget de mapa...")
    map_widget = TkinterMapView(root, width=880, height=650, corner_radius=0)
    map_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    print("Configurando tile server ESRI World Imagery...")
    map_widget.set_tile_server(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        max_zoom=20
    )
    
    print("Posicionando em Portugal (39.5°N, 8.0°W)...")
    map_widget.set_position(39.5, -8.0)
    
    print("Ajustando zoom para 7...")
    map_widget.set_zoom(7)
    
    print("\n" + "="*60)
    print("Mapa carregado!")
    print("="*60)
    print("\nInstruções:")
    print("- Use o mouse para arrastar o mapa")
    print("- Use a roda do mouse para zoom")
    print("- Clique para adicionar um marcador")
    print("- Feche a janela quando terminar")
    print("="*60 + "\n")
    
    # Adicionar marcador de teste em Lisboa
    marker = map_widget.set_marker(38.7223, -9.1393, text="Lisboa")
    print(f"Marcador adicionado em Lisboa: {marker}")
    
    # Callback para cliques
    def on_click(coords):
        lat, lon = coords
        print(f"Clique detectado: Lat={lat:.6f}, Lon={lon:.6f}")
        map_widget.set_marker(lat, lon, text=f"{lat:.4f}, {lon:.4f}")
    
    map_widget.add_left_click_map_command(on_click)
    
    # Testar diferentes tiles após 5 segundos
    def test_osm():
        print("\nTestando OSM (se ESRI não funcionar)...")
        map_widget.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=19)
    
    # Descomentar para testar OSM após 5s
    # root.after(5000, test_osm)
    
    root.mainloop()

if __name__ == "__main__":
    print("Iniciando teste do mapa...")
    test_map()
