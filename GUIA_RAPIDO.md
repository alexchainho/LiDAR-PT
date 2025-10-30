# 🚀 Guia Rápido - DGT Rasters

## Como Iniciar

### 1️⃣ Ativar o Ambiente Virtual
```cmd
cd D:\CSTE\DGT_Rasters
dgt_venv\Scripts\activate
```

### 2️⃣ Iniciar a Aplicação
```cmd
python seletor_projeto.py
```

## 🎛️ Interface Principal

A janela principal oferece:

```
┌─────────────────────────────────────┐
│     ⚙️ Configurações                │  ← Clique aqui para editar
├─────────────────────────────────────┤
│                                     │
│  Escolha o tipo de dados:           │
│  ☑ MDS-50cm                         │
│  ☐ LAZ                              │
│                                     │
│  Escolha o tipo de projeto:         │
│  [Processo por Buffer]              │
│  [Processo por Localidade]          │
│                                     │
└─────────────────────────────────────┘
```

## ⚙️ Configurações

Ao clicar no botão **⚙️ Configurações**, abre uma janela com:

### 📧 CREDENCIAIS
- **Username**: Email de login DGT
- **Password**: Password (campo oculto com ***)

### 📁 CAMINHOS
Cada caminho tem um botão **[...]** para seleção:
- **Pasta Base TOs**: Onde são criados os projetos
- **CSV Ocorrências**: Ficheiro com dados ANEPC
- **Shapefile Censos**: Lugares 2021
- **Pasta Localidades**: Base para localidades

### ⏱️ CONFIGURAÇÕES
- **Download Delay**: Tempo entre downloads (segundos)
- **Session Timeout**: Duração da sessão (segundos)

### 💾 Guardar
- **[Guardar]** → Aplica alterações ao `caminhos.json`
- **[Cancelar]** → Descarta alterações

## 🔄 Fluxos de Trabalho

### A) Processo por Buffer
1. Inicia `seletor_projeto.py`
2. Seleciona tipo de dados (MDS/LAZ)
3. Clica "Processo por Buffer"
4. Escolhe método: SADO ou Coordenadas
5. Sistema cria buffer automático
6. Download inicia

### B) Processo por Localidade
1. Inicia `seletor_projeto.py`
2. Seleciona tipo de dados (MDS/LAZ)
3. Clica "Processo por Localidade"
4. Insere coordenadas
5. Sistema identifica localidade
6. Download inicia

## 💡 Dicas

### Primeira Utilização
1. ⚙️ Abra **Configurações**
2. ✏️ Verifique/edite **credenciais**
3. 📂 Confirme todos os **caminhos**
4. 💾 **Guarde** as alterações

### Alterar Credenciais
- Não precisa editar código
- Use a interface de configurações
- Password é guardada em `caminhos.json`

### Alterar Pastas de Output
- Durante execução, janela pergunta pasta
- Ou configure pasta padrão em Configurações

### Segurança
- `caminhos.json` contém credenciais
- Ficheiro está em `.gitignore`
- Não partilhar este ficheiro

## 🆘 Resolução de Problemas

### Erro: "Module not found"
```cmd
dgt_venv\Scripts\activate
pip install -r requirements.txt
```

### Erro: "Config file not found"
- Verifique se `caminhos.json` existe
- Use `caminhos.json.template` como base

### Erro de Autenticação
- Abra Configurações (⚙️)
- Verifique username/password
- Guarde e tente novamente

### Caminhos Inválidos
- Abra Configurações (⚙️)
- Use botões [...] para selecionar
- Confirme que pastas/ficheiros existem

## 📞 Estrutura de Ficheiros

```
DGT_Rasters/
├── dgt_venv/                    # Ambiente virtual
├── config_loader.py             # Carregador de configurações
├── caminhos.json               # Configurações (PRIVADO)
├── caminhos.json.template      # Template para configuração
├── seletor_projeto.py          # Interface principal ⭐
├── processo_por_buffer.py      # Processo buffer
├── processo_por_localidade.py  # Processo localidade
├── dgt_cdd_downloader.py       # Core do downloader
├── layout_las_localidade.py    # Visualização LAS
├── dados/                      # Shapefiles base
├── localidades/                # Output localidades
└── requirements.txt            # Dependências Python
```

## ✅ Checklist de Instalação

- [ ] Virtual environment criado (`dgt_venv`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] `caminhos.json` configurado
- [ ] Credenciais DGT inseridas
- [ ] Caminhos verificados
- [ ] Teste com `python seletor_projeto.py`
- [ ] Botão Configurações funciona
- [ ] Consegue guardar alterações

---

**Versão**: 2.0  
**Última atualização**: Outubro 2025  
**Funcionalidades**: Interface de configuração integrada
