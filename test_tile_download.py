"""
Testa se os tiles do ESRI World Imagery são acessíveis
"""
import requests

def test_esri_tile():
    # Tile do centro de Portugal (z=7, x=62, y=49)
    url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/7/49/62"
    
    print("Testando acesso aos tiles ESRI World Imagery...")
    print(f"URL: {url}")
    print("-" * 60)
    
    try:
        # Desabilitar verificação SSL (problema com certificado PostgreSQL)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.get(url, timeout=10, verify=False)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Tiles ESRI são acessíveis!")
            print("   → O tile foi baixado com sucesso")
            print("   → O problema pode ser no rendering do tkintermapview")
        else:
            print(f"\n❌ ERRO! Status {response.status_code}")
            print("   → Tiles não estão acessíveis")
            
    except Exception as e:
        print(f"\n❌ ERRO ao conectar:")
        print(f"   {e}")
        print("   → Verifique conexão de rede ou firewall")

if __name__ == "__main__":
    test_esri_tile()
