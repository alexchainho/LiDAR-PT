# 🗺️ Configuração do Mapa - Seletor de Coordenadas

## Mapa Base Atual: ESRI World Imagery

O seletor de coordenadas está configurado para usar o mapa base **ESRI World Imagery** (imagens de satélite).

### URL do Tile Server
```
https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
```

## Outras Opções de Mapas Base

Se quiser alterar o mapa base, edite a função `open_map_picker()` em `seletor_projeto.py` e substitua a linha:

```python
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", max_zoom=22)
```

### Opções Disponíveis:

#### 1. **ESRI World Imagery** (Atual - Satélite)
```python
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", max_zoom=22)
```

#### 2. **ESRI World Street Map** (Mapa de ruas)
```python
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", max_zoom=22)
```

#### 3. **ESRI World Topo Map** (Topográfico)
```python
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}", max_zoom=22)
```

#### 4. **ESRI NatGeo World Map** (National Geographic)
```python
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}", max_zoom=22)
```

#### 5. **OpenStreetMap** (Padrão - gratuito)
```python
map_widget.set_tile_server("https://tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=19)
```

#### 6. **Google Satellite** (alternativa)
```python
map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}", max_zoom=22)
```

#### 7. **Google Hybrid** (Satélite + Labels)
```python
map_widget.set_tile_server("https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", max_zoom=22)
```

## Como Funciona

1. **Abrir**: Clique em "Selecionar Coordenadas no Mapa" na janela principal
2. **Navegar**: Use o mouse para arrastar e zoom com a roda do mouse
3. **Selecionar**: Clique no mapa para colocar/mover o marcador
4. **Confirmar**: Clique no botão "Confirmar" para copiar as coordenadas

## Formato das Coordenadas

As coordenadas são copiadas no formato:
```
39.123456,-8.654321
```
- Latitude, Longitude em graus decimais
- Sistema WGS84 (EPSG:4326)

## Notas Técnicas

- **Max Zoom**: O ESRI permite até zoom 22 (muito detalhado)
- **Performance**: Tiles são baixados em tempo real (requer internet)
- **Cache**: O tkintermapview faz cache local dos tiles
- **Portugal**: Mapa inicia centrado em (39.5°N, 8.0°W) zoom 7

## Resolução de Problemas

### Mapa aparece em branco
1. Verificar conexão à internet
2. Testar outro tile server (ex: OpenStreetMap)
3. Aguardar alguns segundos para carregamento inicial

### Coordenadas não copiam
- Certifique-se de clicar no mapa antes de confirmar
- O marcador "Selecionado" deve aparecer

### Tiles não carregam
- Alguns servidores podem ter rate limiting
- Use OpenStreetMap como fallback (sempre disponível)

---

**Configuração Atual**: ESRI World Imagery (Satélite)  
**Última atualização**: Outubro 2025
