# 🗺️ DGT Rasters

**Sistema Automatizado de Download e Processamento de Dados Geoespaciais da Direção-Geral do Território (DGT)**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI--Assisted-GitHub%20Copilot-purple)](https://github.com/features/copilot)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Utilização](#-utilização)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Configuração](#-configuração)
- [Produtos Disponíveis](#-produtos-disponíveis)
- [Tecnologias](#-tecnologias)
- [Desenvolvimento com IA](#-desenvolvimento-com-ia)
- [Contribuir](#-contribuir)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 📖 Sobre o Projeto

O **DGT Rasters** é uma aplicação Python desenvolvida para automatizar o download e processamento de dados geoespaciais LiDAR disponibilizados pela Direção-Geral do Território de Portugal através do **Centro de Descargas de Dados (CDD)**.

### Objetivo

Facilitar o acesso a dados de alta qualidade para profissionais de GIS, investigadores e entidades que necessitam de:
- **Modelos Digitais de Terreno (MDT)** em resoluções de 2m e 50cm
- **Modelos Digitais de Superfície (MDS)** em resoluções de 2m e 50cm
- **Nuvens de pontos LiDAR (LAZ)** para análise detalhada

### Características

- ✅ **Interface Gráfica Intuitiva** - Seleção visual com mapa interativo
- ✅ **Download Automático** - Gestão de sessões e retry automático
- ✅ **Buffer Flexível** - De 100 metros a 15 km com deteção inteligente
- ✅ **Merge Opcional** - União automática de rasters numa única imagem
- ✅ **GeoPackage** - Formato moderno e portável para dados vetoriais
- ✅ **Configuração Centralizada** - Ficheiro JSON para credenciais e caminhos
- ✅ **Caminhos Relativos** - Projeto 100% portável

---

## 🚀 Funcionalidades

### 1. Seleção Interativa de Produtos
- Interface gráfica com checkboxes para escolher produtos
- 5 produtos LiDAR disponíveis (LAZ, MDS-2m, MDS-50cm, MDT-2m, MDT-50cm)
- Opção "Todos" para download completo

### 2. Mapa Interativo para Coordenadas
- Mapa base: **ESRI World Imagery** (imagens de satélite)
- Overlay com limite de Portugal (amarelo)
- Clique para selecionar coordenadas (WGS84)
- Navegação com drag & zoom

### 3. Buffer Inteligente
- **Intervalo**: 100 metros a 15 km
- **Deteção automática**: valores < 100 = km, ≥ 100 = metros
- Exemplo: `5` = 5 km, `500` = 500 metros

### 4. Merge de Rasters
- Diálogo opcional: "Pretende unir os rasters MDS e MDT?"
- Nomes simplificados: `MDS-50cm.tif`, `MDT-2m.tif`
- Proteção contra ficheiros bloqueados (timestamp automático)

### 5. Autenticação Robusta
- OAuth2 com sessão persistente
- Timeout automático (25 minutos)
- Retry inteligente em caso de falha

---

## 💻 Requisitos

### Sistema Operativo
- Windows 10/11 (testado)
- Linux / macOS (compatível, não testado)

### Python
- **Python 3.8 ou superior**
- Virtual environment (criado automaticamente)

### Credenciais DGT
- Conta no [Centro de Descargas de Dados](https://cdd.dgterritorio.gov.pt)
- Username e password válidos

### Espaço em Disco
- Mínimo: 1 GB (para instalação)
- Recomendado: 50+ GB (para dados descarregados)

---

## 📦 Instalação

### Método 1: Execução Automática (Recomendado)

1. **Clone o repositório**
   ```cmd
   git clone https://github.com/alexchainho/DGT_Rasters.git
   cd DGT_Rasters
   ```

2. **Configure as credenciais**
   - Copie `config\caminhos.json.template` para `config\caminhos.json`
   - Edite `config\caminhos.json` com suas credenciais DGT

3. **Execute o launcher**
   ```cmd
   Executar_DGT.bat
   ```

O script `Executar_DGT.bat` irá automaticamente:
- ✅ Criar o virtual environment (`dgt_venv`)
- ✅ Instalar todas as dependências
- ✅ Iniciar a aplicação

### Método 2: Instalação Manual

1. **Criar virtual environment**
   ```cmd
   python -m venv dgt_venv
   ```

2. **Ativar o ambiente**
   ```cmd
   dgt_venv\Scripts\activate
   ```

3. **Instalar dependências**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Configurar credenciais** (igual ao Método 1)

5. **Executar**
   ```cmd
   python src\seletor_projeto.py
   ```

---

## 🎮 Utilização

### Fluxo de Trabalho

```
┌─────────────────────────────────────────┐
│  1. Iniciar Aplicação                   │
│     Executar_DGT.bat                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Selecionar Produtos                 │
│     ☑ LAZ, MDS-2m, MDS-50cm, etc.       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Escolher Método                     │
│     • Processo por Buffer               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Definir Área                        │
│     • Mapa interativo                   │
│     • Clique para coordenadas           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Configurar Buffer                   │
│     • 100m a 15km                       │
│     • Merge opcional (Sim/Não)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  6. Selecionar Pasta de Destino        │
│     • Diálogo de seleção                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  7. Download Automático                 │
│     • Autenticação                      │
│     • Pesquisa de tiles                 │
│     • Download com progress             │
│     • Merge (se selecionado)            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  8. Conclusão                           │
│     • Ficheiros em pasta de destino     │
│     • Auto-terminar após 5s             │
└─────────────────────────────────────────┘
```

### Exemplo Prático

**Cenário**: Descarregar MDS-50cm e LAZ para zona de Lisboa com buffer de 2km e merge ativado

1. Execute `Executar_DGT.bat`
2. Selecione: ☑ MDS-50cm, ☑ LAZ
3. Clique em **"Processo por Buffer"**
4. No mapa, clique em Lisboa (aprox. 38.7°N, 9.1°W)
5. Digite buffer: `2` (= 2 km)
6. Diálogo merge: **Sim**
7. Selecione pasta de destino
8. Digite nome do projeto: `Lisboa_2km`
9. Aguarde o download (progresso em terminal)
10. ✅ Ficheiros criados:
    - `Lisboa_2km/MDS-50cm/MDS-50cm.tif` (merged)
    - `Lisboa_2km/LAZ/*.laz` (individuais)

---

## 📁 Estrutura do Projeto

```
DGT_Rasters/
├── 📄 README.md                    # Este ficheiro
├── 📄 requirements.txt             # Dependências Python
├── 🔧 Executar_DGT.bat            # Launcher automático
├── � .gitignore                  # Exclusões Git
│
├── 📂 config/                      # Configurações do projeto
│   ├── �🔐 caminhos.json           # Configurações (não versionado)
│   └── 📋 caminhos.json.template  # Template de configuração
│
├── 📂 src/                         # Código-fonte Python
│   ├── 🎨 seletor_projeto.py      # Interface gráfica principal
│   ├── 📥 processo_por_buffer.py  # Download por buffer
│   ├── 🔧 dgt_cdd_downloader.py   # Utilitários de download
│   └── ⚙️ config_loader.py        # Carregador de configurações
│
├── 📂 dados/                       # Dados base do projeto
│   └── 📦 dados_dgt.gpkg          # GeoPackage (grelha DGT + Portugal)
│
├── 📂 dgt_venv/                    # Virtual environment (auto-criado)
│   ├── Scripts/
│   ├── Lib/
│   └── ...
│
└── 📂 docs/                        # Documentação adicional
```

**Nota sobre Outputs**: Os ficheiros descarregados são guardados na pasta que escolher durante a execução da aplicação (selecionada via diálogo).

---

## ⚙️ Configuração

### Ficheiro `config/caminhos.json`

Estrutura do ficheiro de configuração (localizado em `config/caminhos.json`):

```json
{
  "_comment": "Caminhos relativos são resolvidos a partir do diretório do projeto",
  "venv_path": "dgt_venv",
  "credentials": {
    "username": "seu_email@exemplo.pt",
    "password": "sua_password"
  },
  "paths": {
    "geopackage": "dados/dados_dgt.gpkg"
  },
  "urls": {
    "stac_search": "https://cdd.dgterritorio.gov.pt/dgt-be/v1/search",
    "auth_base": "https://auth.cdd.dgterritorio.gov.pt/realms/dgterritorio/protocol/openid-connect",
    "redirect_uri": "https://cdd.dgterritorio.gov.pt/auth/callback",
    "main_site": "https://cdd.dgterritorio.gov.pt"
  },
  "settings": {
    "session_timeout": 1500,
    "download_delay": 5.0,
    "search_delay": 0.2,
    "max_retries": 3,
    "retry_delay": 10
  }
}
```

### Caminhos Relativos vs Absolutos

| Tipo | Exemplo | Uso |
|------|---------|-----|
| **Relativo** | `dados/dados_dgt.gpkg` | Ficheiros do projeto |
| **Absoluto** | `D:\Projetos\output` | Pastas externas |

**Vantagens dos Relativos**:
- ✅ Portabilidade total
- ✅ Funciona em qualquer máquina
- ✅ Ideal para Git/repositórios

### Interface de Configurações

A aplicação inclui editor gráfico (botão ⚙️):
- Editar credenciais
- Alterar caminhos (com diálogo de seleção)
- Ajustar timeouts e delays
- Guardar automaticamente em `config/caminhos.json`

---

## 📊 Produtos Disponíveis

### Produtos LiDAR (5 tipos)

| Produto | Descrição | Resolução | Formato | Tamanho Típico |
|---------|-----------|-----------|---------|----------------|
| **LAZ** | Nuvem de pontos LiDAR comprimida | Variável | .laz | 20-100 MB/tile |
| **MDS-2m** | Modelo Digital de Superfície | 2 metros | .tif | 5-10 MB/tile |
| **MDS-50cm** | Modelo Digital de Superfície | 50 cm | .tif | 50-100 MB/tile |
| **MDT-2m** | Modelo Digital de Terreno | 2 metros | .tif | 5-10 MB/tile |
| **MDT-50cm** | Modelo Digital de Terreno | 50 cm | .tif | 50-100 MB/tile |

### Diferença: MDS vs MDT

- **MDS (Modelo Digital de Superfície)**: Inclui vegetação, edifícios e estruturas
- **MDT (Modelo Digital de Terreno)**: Apenas terreno nu (solo)

### Sistemas de Coordenadas

- **Download/Seleção**: WGS84 (EPSG:4326)
- **Processamento**: PT-TM06/ETRS89 (EPSG:3763)
- **GeoPackage**: Mantém CRS original de cada layer

---

## 🛠️ Tecnologias

### Core

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.8+ | Linguagem principal |
| GeoPandas | 1.0+ | Manipulação de dados geoespaciais |
| Shapely | 2.0+ | Geometrias vetoriais |
| Rasterio | 1.4+ | Processamento de rasters |
| PyProj | 3.7+ | Transformação de coordenadas |

### Interface

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Tkinter | Built-in | GUI nativa Python |
| TkinterMapView | 1.29+ | Mapa interativo com tiles |
| CustomTkinter | 5.2+ | Widgets modernos |

### HTTP & API

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Requests | 2.32+ | Cliente HTTP |
| BeautifulSoup4 | 4.14+ | Parsing HTML (autenticação) |

### Formatos de Dados

| Formato | Uso | Vantagens |
|---------|-----|-----------|
| **GeoPackage** (.gpkg) | Dados vetoriais | Um ficheiro, UTF-8, índices espaciais |
| **GeoTIFF** (.tif) | Rasters MDS/MDT | Standard geoespacial, compressão |
| **LAZ** | Nuvens de pontos | Compressão LiDAR eficiente |
| **JSON** | Configuração | Legível, fácil de editar |

---

## 🤖 Desenvolvimento com IA

### Assistência de IA

Este projeto foi desenvolvido com apoio significativo de **GitHub Copilot**, a ferramenta de IA da Microsoft/OpenAI integrada no Visual Studio Code.

### Contribuições da IA

**GitHub Copilot ajudou em**:
- ✅ Geração de código boilerplate
- ✅ Implementação de padrões de autenticação OAuth2
- ✅ Lógica de retry e gestão de sessões
- ✅ Parsing de HTML para extração de formulários Keycloak
- ✅ Criação de interface gráfica Tkinter
- ✅ Integração com TkinterMapView
- ✅ Funções de merge de rasters com Rasterio
- ✅ Documentação e comentários
- ✅ Estruturação do projeto

### Desenvolvimento Humano

**Decisões e implementações humanas**:
- 🎯 Arquitetura geral do sistema
- 🎯 Escolha de tecnologias e bibliotecas
- 🎯 Design da interface do utilizador
- 🎯 Lógica de negócio específica para DGT
- 🎯 Testes e validação
- 🎯 Refactoring e otimizações
- 🎯 Migração para GeoPackage
- 🎯 Sistema de caminhos relativos

### Filosofia de Desenvolvimento

> **Humano + IA = Melhor Software**
>
> A IA acelerou o desenvolvimento, mas as decisões críticas, testes rigorosos e validação foram sempre humanas. O resultado é código robusto, bem documentado e pronto para produção.

---

## 🤝 Contribuir

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas alterações (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Áreas para Contribuição

- 🐛 Correção de bugs
- ✨ Novas funcionalidades
- 📝 Melhorias na documentação
- 🧪 Testes automatizados
- 🌐 Suporte para Linux/macOS
- 🎨 Melhorias na interface gráfica

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o ficheiro [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Alexandre Chainho**
- GitHub: [@alexchainho](https://github.com/alexchainho)
- Email: alexchainho@gmail.com


### Agradecimentos

- **Direção-Geral do Território (DGT)** - Pela disponibilização dos dados
- **GitHub Copilot** - Assistência AI no desenvolvimento
- **Comunidade Python GIS** - Bibliotecas de código aberto

---

## 📚 Documentação Adicional

Documentação em desenvolvimento. O README contém todas as informações necessárias para utilização do projeto.

---

## 🔗 Links Úteis

- [Centro de Descargas de Dados DGT](https://cdd.dgterritorio.gov.pt)
- [GeoPandas Documentation](https://geopandas.org)
- [Rasterio Documentation](https://rasterio.readthedocs.io)
- [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView)

---

## 📈 Estado do Projeto

- ✅ **Versão**: 1.0.0
- ✅ **Status**: Produção
- ✅ **Última atualização**: Outubro 2025
- ✅ **Python**: 3.8+
- ✅ **Plataforma**: Windows (testado), Linux/macOS (compatível)

---

<div align="center">

**Desenvolvido em Portugal 🇵🇹**

**Powered by GitHub Copilot 🤖**

</div>
