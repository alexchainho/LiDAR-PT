# Alterações Implementadas no Projeto DGT_Rasters

## Resumo das Alterações

Este documento descreve as alterações implementadas no projeto DGT_Rasters conforme solicitado.

## 1. Virtual Environment (venv)

✅ **Criado**: `dgt_venv`
- Localização: `d:\CSTE\DGT_Rasters\dgt_venv`
- Todos os pacotes necessários foram instalados a partir do `requirements.txt`
- Para ativar o ambiente virtual:
  ```cmd
  dgt_venv\Scripts\activate
  ```

## 2. Ficheiro de Configuração (caminhos.json)

✅ **Atualizado**: `caminhos.json`

O ficheiro agora contém:

### Credenciais de Login
```json
"credentials": {
  "username": "chainho.ac@gnr.pt",
  "password": "G_nr2050086"
}
```

### Caminhos do Sistema
```json
"paths": {
  "base_path_tos": "Pasta base para projetos TOs",
  "csv_ocorrencias": "CSV com dados ANEPC",
  "censos_shapefile": "Shapefile de lugares 2021",
  "grelha_dgt": "Grelha DGT",
  "localidades_base": "Pasta base para localidades"
}
```

**Nota**: O caminho `proj_lib` foi removido. O `pyproj` instalado no venv gerencia automaticamente os dados PROJ.

### URLs
```json
"urls": {
  "stac_search": "URL da API STAC",
  "auth_base": "URL base de autenticação",
  "redirect_uri": "URI de redirecionamento",
  "main_site": "Site principal DGT"
}
```

### Configurações
```json
"settings": {
  "session_timeout": 1500,
  "download_delay": 5.0,
  "search_delay": 0.2,
  "max_retries": 3,
  "retry_delay": 10
}
```

## 3. Módulo de Configuração (config_loader.py)

✅ **Criado**: `config_loader.py`

Módulo utilitário para carregar configurações do ficheiro JSON:

### Funções Disponíveis:
- `load_config()` - Carrega todo o ficheiro de configuração
- `get_credentials()` - Retorna username e password
- `get_path(path_key)` - Retorna um caminho específico
- `get_url(url_key)` - Retorna uma URL específica
- `get_setting(setting_key)` - Retorna uma configuração específica
- `get_all_paths()` - Retorna todos os caminhos
- `get_all_urls()` - Retorna todas as URLs
- `get_all_settings()` - Retorna todas as configurações

## 4. Seleção de Pasta de Output via Tkinter

✅ **Implementado** em:
- `processo_por_buffer.py`
- `processo_por_localidade.py`
- `dgt_cdd_downloader.py`

### Alterações:
- A função `create_folder()` agora abre uma janela de diálogo Tkinter
- O utilizador pode selecionar a pasta base para o projeto
- Se não selecionar, usa a pasta padrão do `caminhos.json`
- Melhora a flexibilidade do sistema

## 5. Ficheiros Atualizados

### Todos os scripts Python foram atualizados para:
1. Importar o módulo `config_loader`
2. Carregar credenciais do JSON em vez de hardcoded
3. Usar caminhos do JSON em vez de hardcoded
4. Usar URLs do JSON
5. Usar configurações do JSON

### Ficheiros Modificados:
- ✅ `processo_por_buffer.py`
- ✅ `processo_por_localidade.py`
- ✅ `dgt_cdd_downloader.py`
- ✅ `layout_las_localidade.py`
- ✅ `seletor_projeto.py` - **NOVA**: Interface para configurações
- ✅ `caminhos.json`

## Interface de Configuração (NOVO!)

### Janela Principal do Seletor
O ficheiro `seletor_projeto.py` agora inclui um botão **⚙️ Configurações** que permite:

#### 1. Editar Credenciais
- Username
- Password (campo oculto)

#### 2. Configurar Caminhos
- Pasta Base TOs
- CSV Ocorrências
- Shapefile Censos
- Pasta Localidades
- Cada caminho tem um botão "..." para seleção via diálogo

#### 3. Ajustar Configurações
- Download Delay (segundos)
- Session Timeout (segundos)

#### 4. Guardar Alterações
- Botão "Guardar" atualiza o ficheiro `caminhos.json`
- Validação e confirmação de sucesso
- Botão "Cancelar" para descartar alterações

### Como Usar a Interface de Configuração
1. Execute `python seletor_projeto.py`
2. Clique no botão **⚙️ Configurações**
3. Edite os campos desejados
4. Use os botões "..." para selecionar pastas/ficheiros
5. Clique em "Guardar" para aplicar as alterações

## Como Usar

### 1. Ativar o Virtual Environment
```cmd
cd d:\CSTE\DGT_Rasters
dgt_venv\Scripts\activate
```

### 2. Executar os Scripts
```cmd
python processo_por_buffer.py
python processo_por_localidade.py
```

### 3. Atualizar Configurações
Edite o ficheiro `caminhos.json` para alterar:
- Credenciais
- Caminhos
- URLs
- Configurações de timeout/delay

## Vantagens das Alterações

1. **Segurança**: Credenciais centralizadas num único ficheiro
2. **Manutenibilidade**: Fácil alterar caminhos sem modificar código
3. **Flexibilidade**: Seleção de pastas via interface gráfica
4. **Isolamento**: Virtual environment evita conflitos de dependências
5. **Reutilização**: Módulo config_loader pode ser usado em novos scripts
6. **Portabilidade**: PyProj gerenciado pelo venv (sem configuração manual)

## Notas Importantes

⚠️ **Segurança**: Considere adicionar `caminhos.json` ao `.gitignore` se usar controlo de versões, para proteger as credenciais.

⚠️ **Caminhos**: Verifique se todos os caminhos no `caminhos.json` estão corretos para o seu sistema.

⚠️ **Dependencies**: O virtual environment já tem todos os pacotes instalados. Use sempre o venv ao executar os scripts.

✅ **PROJ_LIB**: Não é mais necessário configurar manualmente. O pyproj no venv gerencia automaticamente os dados PROJ.
