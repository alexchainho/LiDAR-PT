"""
Script de teste para verificar se todas as dependências estão funcionando
corretamente sem necessidade de definir PROJ_LIB manualmente.
"""

import sys

print("=" * 60)
print("TESTE DE DEPENDÊNCIAS - DGT Rasters")
print("=" * 60)

# Teste 1: Config Loader
print("\n[1/7] Testando config_loader...")
try:
    import config_loader
    config = config_loader.load_config()
    username, password = config_loader.get_credentials()
    print(f"  ✓ Config carregado")
    print(f"  ✓ Username: {username}")
    print(f"  ✓ Credenciais OK")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 2: PyProj
print("\n[2/7] Testando pyproj...")
try:
    import pyproj
    from pyproj import CRS, Transformer
    print(f"  ✓ PyProj version: {pyproj.__version__}")
    print(f"  ✓ PROJ data dir: {pyproj.datadir.get_data_dir()}")
    
    # Teste de transformação de coordenadas
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3763", always_xy=True)
    x, y = transformer.transform(-9.0, 39.0)
    print(f"  ✓ Transformação OK: (-9.0, 39.0) → ({x:.2f}, {y:.2f})")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 3: Geopandas
print("\n[3/7] Testando geopandas...")
try:
    import geopandas as gpd
    from shapely.geometry import Point
    
    # Criar um GeoDataFrame simples
    gdf = gpd.GeoDataFrame(
        {'name': ['teste']}, 
        geometry=[Point(-9.0, 39.0)],
        crs="EPSG:4326"
    )
    gdf_3763 = gdf.to_crs(epsg=3763)
    print(f"  ✓ Geopandas OK")
    print(f"  ✓ Conversão de CRS OK")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 4: Rasterio
print("\n[4/7] Testando rasterio...")
try:
    import rasterio
    print(f"  ✓ Rasterio version: {rasterio.__version__}")
    print(f"  ✓ GDAL version: {rasterio.__gdal_version__}")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 5: Requests
print("\n[5/7] Testando requests...")
try:
    import requests
    print(f"  ✓ Requests version: {requests.__version__}")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 6: Pandas
print("\n[6/7] Testando pandas...")
try:
    import pandas as pd
    print(f"  ✓ Pandas version: {pd.__version__}")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

# Teste 7: Laspy
print("\n[7/7] Testando laspy...")
try:
    import laspy
    print(f"  ✓ Laspy OK")
except Exception as e:
    print(f"  ✗ ERRO: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\nO ambiente está pronto para uso.")
print("Execute: python seletor_projeto.py")
print("=" * 60)
