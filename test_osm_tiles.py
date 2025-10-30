"""
Testa mapa com OpenStreetMap (tiles simples) para verificar se tkintermapview funciona
"""
import tkinter as tk
from tkintermapview import TkinterMapView

def main():
    print("=" * 60)
    print("TESTE COM OPENSTREETMAP (tiles simples)")
    print("=" * 60)
    
    root = tk.Tk()
    root.title("Teste OSM - tkintermapview")
    root.geometry("900x700")
    
    print("Criando widget de mapa...")
    map_widget = TkinterMapView(root, width=880, height=650, corner_radius=0)
    map_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    print("Usando OpenStreetMap (default)...")
    # OSM é o default - não precisa configurar tile server
    
    root.update_idletasks()
    
    print("Posicionando em Lisboa...")
    map_widget.set_position(38.7223, -9.1393)
    map_widget.set_zoom(12)
    
    marker = map_widget.set_marker(38.7223, -9.1393, text="Lisboa")
    print(f"Marcador criado: {marker}")
    
    print("=" * 60)
    print("SE APARECER O MAPA:")
    print("  → tkintermapview funciona!")
    print("  → Problema é específico dos tiles ESRI")
    print("\nSE NÃO APARECER:")
    print("  → Problema no tkintermapview ou na instalação")
    print("=" * 60)
    
    root.mainloop()

if __name__ == "__main__":
    main()
