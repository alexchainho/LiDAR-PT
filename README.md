# DGT Rasters - Automação de Download e Processamento

## Estrutura de Pastas

```
DGT_Rasters/
├── requirements.txt           # Dependências Python do projeto
├── caminhos.json              # Caminho do venv utilizado
├── seletor_projeto.py         # Interface Tkinter para seleção do processo
├── processo_por_localidade.py # Script principal para download/processamento por localidade
├── processo_por_buffer.py     #
├── dgt_cdd_downloader.py      # Funções utilitárias de download DGT
├── dados/
│   └── Lugares_2021.shp      # Camada de localidades (shapefile)
├── localidades/
│   └── <nome_localidade>/    # Pasta criada para cada localidade processada
│       ├── <nome>.shp                # Polígono da localidade
│       ├── <nome>_grelha5km.shp      # Grelha regular 5km x 5km
│       ├── MDS-50cm/                 # Rasters MDS-50cm descarregados e unidos
│       └── LAZ/                      # Nuvens de pontos LAZ/LAS
└── ... outros scripts e outputs
```

## Fluxo de Execução

1. **Executar Executar_DGT.bat**
   - Cria/ativa o ambiente virtual Python (venv) e instala dependências.
   - Lê/escreve o caminho do venv em `caminhos.json`.
   - Inicia a interface gráfica (`seletor_projeto.py`).

2. **Selecionar o tipo de processo**
   - Processo por Localidade: pede coordenadas, identifica localidade, cria pasta e grelha 5km x 5km.
   - Faz download dos dados DGT (MDS-50cm, LAZ) para a pasta da localidade.
   - Une rasters MDS-50cm e salva na pasta.

3. **Outputs**
   - Todos os dados e resultados ficam organizados em subpastas de `localidades/<nome_localidade>/`.

## Requisitos
- Python 3.13
- Windows
- Pacotes: ver `requirements.txt`

## Observações
- O recorte dos dados é feito pela extensão (bbox) da localidade.
- A grelha criada é regular, 5km x 5km, cobrindo toda a extensão da localidade.
- O batch é robusto: reutiliza o venv se já existir, instala dependências automaticamente.
