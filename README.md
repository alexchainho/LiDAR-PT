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
  - [Assistente de Configuração Automática](#-primeira-execução---assistente-de-configuração-automática)
  - [FAQ - Perguntas Frequentes](#-perguntas-frequentes-faq---assistente-de-configuração)
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
- ✅ **Assistente de Configuração** - Setup automático na primeira execução com popups gráficos
- ✅ **Download Automático** - Gestão de sessões e retry automático
- ✅ **Buffer Flexível** - De 100 metros a 15 km com deteção inteligente
- ✅ **Merge Opcional** - União automática de rasters numa única imagem
- ✅ **GeoPackage** - Formato moderno e portável para dados vetoriais
- ✅ **Configuração Centralizada** - Ficheiro JSON para credenciais e caminhos
- ✅ **Caminhos Relativos** - Projeto 100% portável
- ✅ **Zero Configuração Manual** - Credenciais solicitadas automaticamente via popup

---

## 🚀 Funcionalidades

### 0. Assistente de Configuração Automática (Primeira Execução)
- **Janela popup de boas-vindas** com explicação dos passos de instalação
- **Criação automática** do ambiente virtual Python (`dgt_venv`)
- **Instalação automática** de todas as dependências necessárias
- **Janela popup de credenciais** com:
  - Campos para username (email) e password
  - Informações detalhadas sobre o Centro de Descargas da DGT
  - Link direto e clicável para criar conta: [cdd.dgterritorio.gov.pt/dgt-fe](https://cdd.dgterritorio.gov.pt/dgt-fe)
  - Validação de campos obrigatórios
- **Criação automática** do ficheiro `config\caminhos.json` com credenciais
- **Zero configuração manual** necessária

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
- **Python 3.8 ou superior** (qualquer versão: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13)
- Virtual environment (criado automaticamente)

> **⚠️ Python 3.12.8 ou outra versão não detetado?**  
> Veja a secção [Resolução de Problemas - Python](#-resolução-de-problemas---python) abaixo.

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

2. **Execute o launcher**
   ```cmd
   Executar_DGT.bat
   ```

#### 🎯 Primeira Execução - Assistente de Configuração Automática

Na **primeira execução**, o sistema detecta automaticamente a ausência do ambiente virtual e do ficheiro de configuração, apresentando um **assistente gráfico interativo** com janelas popup:

##### 🪟 Passo 1: Janela de Boas-Vindas
Uma janela gráfica (650x500px) é apresentada com:
- **Explicação detalhada** dos 4 passos da instalação
- **Requisitos do sistema** (Python 3.8+, Internet, Espaço em disco)
- **Tempo estimado** de configuração: 5-10 minutos
- **Botões de ação:** [Continuar] para prosseguir ou [Cancelar] para sair

##### 🐍 Passo 2: Criação do Ambiente Virtual
Após clicar em "Continuar", o sistema automaticamente:
- Cria o virtual environment `dgt_venv`
- Isola todas as dependências do projeto
- Evita conflitos com outros projetos Python

##### 📚 Passo 3: Instalação de Dependências
Instalação automática de todas as bibliotecas necessárias:
- **Geoespacial:** GeoPandas, Rasterio, Fiona, Shapely
- **Interface:** Tkinter, Pillow
- **HTTP:** Requests, urllib3
- **Processamento:** NumPy, GDAL, laspy
- Processo pode demorar 3-5 minutos (dependendo da conexão)

##### 🔐 Passo 4: Configuração de Credenciais DGT
Uma segunda janela popup (650x620px) é apresentada solicitando:
- **Username (Email):** Campo de texto para o email de registo
- **Password:** Campo mascarado (asteriscos) para a password
- **Informações detalhadas:**
  - Explicação sobre o Centro de Descargas de Dados da DGT
  - Instruções passo-a-passo para criar conta nova
  - Link clicável para registo: [https://cdd.dgterritorio.gov.pt/dgt-fe](https://cdd.dgterritorio.gov.pt/dgt-fe)
- **Validação:** Campos obrigatórios (aviso se deixados vazios)
- **Segurança:** Credenciais guardadas localmente em `config\caminhos.json`
- **Botões:** [Guardar] para confirmar ou [Cancelar] para sair

##### 🚀 Passo 5: Inicialização da Aplicação
Após guardar as credenciais:
- Ficheiro `config\caminhos.json` é criado e populado
- Aplicação inicia automaticamente
- Interface gráfica com mapa interativo é apresentada

---

> **📌 Importante:** 
> - Nas **execuções seguintes**, o launcher apenas verifica dependências e inicia a aplicação diretamente
> - **Não são mostrados popups** após a primeira configuração
> - Para reconfigurar credenciais, edite manualmente `config\caminhos.json`

> **⚠️ Nota de Segurança:**
> - As credenciais são guardadas **localmente** no seu computador
> - **Não são partilhadas** ou enviadas para outros serviços
> - São usadas **apenas** para autenticação no servidor da DGT


---

#### ✨ Funcionalidades do `Executar_DGT.bat`

O launcher automatizado realiza as seguintes tarefas:

**Detecção Inteligente:**
- ✅ Detecta automaticamente se é primeira execução
- ✅ Verifica existência do virtual environment (`dgt_venv`)
- ✅ Verifica existência do ficheiro de configuração (`config\caminhos.json`)

**Primeira Execução:**
- ✅ Mostra **popup de boas-vindas** com instruções detalhadas
- ✅ Cria automaticamente o virtual environment Python
- ✅ Ativa o ambiente virtual
- ✅ Atualiza pip para versão mais recente
- ✅ Instala todas as dependências do `requirements.txt`
- ✅ Mostra **popup de credenciais DGT** com link para registo
- ✅ Cria e popula `config\caminhos.json` com credenciais fornecidas
- ✅ Inicia a aplicação automaticamente

**Execuções Seguintes:**
- ✅ Ativa o virtual environment
- ✅ Verifica e atualiza dependências (se necessário)
- ✅ Valida existência de `config\caminhos.json`
- ✅ Inicia a aplicação diretamente (sem popups)

**Tratamento de Erros:**
- ⚠️ Mensagens claras em caso de falha
- ⚠️ Instruções de resolução de problemas
- ⚠️ Opção de cancelamento seguro em qualquer etapa

---

#### 📸 Capturas de Ecrã do Assistente

<details>
<summary>🖼️ Clique para ver as janelas do assistente de configuração</summary>

**Janela 1: Boas-Vindas**
```
┌────────────────────────────────────────────────────────────┐
│ DGT Rasters - Sistema de Download de Dados Geoespaciais   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ ═══════════════════════════════════════════════════════   │
│      PRIMEIRA EXECUCAO DETECTADA!                          │
│ ═══════════════════════════════════════════════════════   │
│                                                            │
│ PASSOS DA INSTALACAO:                                      │
│                                                            │
│  1. CRIAR AMBIENTE VIRTUAL PYTHON (dgt_venv)              │
│     * Isola as dependencias do projeto                    │
│     * Evita conflitos com outros projetos Python          │
│                                                            │
│  2. INSTALAR DEPENDENCIAS NECESSARIAS                     │
│     * GeoPandas, Rasterio, Tkinter e outras bibliotecas   │
│     * Pode demorar 3-5 minutos                            │
│                                                            │
│  3. CONFIGURAR CREDENCIAIS DGT                            │
│     * Username e password para acesso aos dados           │
│                                                            │
│  4. INICIAR APLICACAO                                     │
│     * Interface grafica com mapa interativo               │
│                                                            │
│ TEMPO ESTIMADO: 5-10 minutos                              │
│                                                            │
│                            [Continuar]  [Cancelar]        │
└────────────────────────────────────────────────────────────┘
```

**Janela 2: Credenciais DGT**
```
┌────────────────────────────────────────────────────────────┐
│ Configuracao de Credenciais de Acesso                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ ACESSO AO CENTRO DE DESCARGAS DE DADOS DA DGT             │
│                                                            │
│ Para descarregar dados geograficos da DGT, e necessario   │
│ ter credenciais de acesso ao Centro de Descargas.         │
│                                                            │
│ NAO TEM CONTA? SIGA ESTES PASSOS:                         │
│   1. Aceda: https://cdd.dgterritorio.gov.pt/dgt-fe        │
│   2. Clique em "Registar" ou "Criar Conta Nova"           │
│   3. Preencha o formulario de registo                     │
│   4. Aguarde email de confirmacao                         │
│   5. Apos ativacao, utilize credenciais abaixo            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Username (Email):  [________________________________]      │
│                                                            │
│ Password:          [********************************]      │
│                                                            │
│ Nao tem conta? Clique aqui para criar registo no CDD      │
│                                                            │
│                            [Guardar]  [Cancelar]          │
└────────────────────────────────────────────────────────────┘
```

</details>

---

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

## ❓ Perguntas Frequentes (FAQ) - Assistente de Configuração

<details>
<summary><b>📌 Como funciona a detecção de primeira execução?</b></summary>

O sistema verifica automaticamente se a pasta `dgt_venv` existe. Se não existir, considera-se primeira execução e o assistente gráfico é ativado.

</details>

<details>
<summary><b>🔄 Posso executar o assistente novamente?</b></summary>

Sim! Para reconfigurar tudo:
1. Elimine a pasta `dgt_venv`
2. Elimine o ficheiro `config\caminhos.json`
3. Execute `Executar_DGT.bat` novamente

O assistente será ativado automaticamente.

</details>

<details>
<summary><b>🔐 Onde são guardadas as minhas credenciais?</b></summary>

As credenciais são guardadas localmente no ficheiro `config\caminhos.json` no seu computador. 

**Importante:**
- ✅ Guardadas **apenas localmente**
- ✅ **Não são enviadas** para outros serviços
- ✅ Usadas **apenas** para autenticação no servidor da DGT
- ⚠️ Adicione `config\caminhos.json` ao `.gitignore` (já configurado)

</details>

<details>
<summary><b>✏️ Como alterar as credenciais depois da primeira execução?</b></summary>

Tem 3 opções:

**Opção 1 - Edição Manual (Rápido):**
```cmd
notepad config\caminhos.json
```
Altere os campos `username` e `password` e guarde.

**Opção 2 - Reconfigurar Tudo:**
```cmd
rmdir /s /q dgt_venv
del config\caminhos.json
Executar_DGT.bat
```

**Opção 3 - Apenas Credenciais:**
```cmd
del config\caminhos.json
Executar_DGT.bat
```
(O venv existente será reutilizado, apenas credenciais são solicitadas)

</details>

<details>
<summary><b>❌ O que fazer se cancelar o assistente?</b></summary>

Se cancelar em qualquer janela popup:
- O processo é interrompido de forma segura
- Nenhum ficheiro é criado ou modificado
- Pode executar `Executar_DGT.bat` novamente quando quiser
- O assistente começará do início

</details>

<details>
<summary><b>🌐 Não tenho conta DGT. Como criar?</b></summary>

**Passo a passo:**
1. Aceda a: [https://cdd.dgterritorio.gov.pt/dgt-fe](https://cdd.dgterritorio.gov.pt/dgt-fe)
2. Clique em **"Registar"** ou **"Criar Conta Nova"**
3. Preencha o formulário com:
   - Nome completo
   - Email válido (será o username)
   - Password segura
   - Dados de contacto
4. Aguarde email de confirmação
5. Clique no link de ativação recebido por email
6. Use o email e password no assistente de configuração

**Nota:** O link para registo também está disponível na janela de credenciais (clicável).

</details>

<details>
<summary><b>⚠️ Erro: "Python não encontrado"</b></summary>

**Causa:** Python 3.8+ não está instalado ou não está no PATH do sistema.

**Solução:**
1. Instale Python 3.8 ou superior: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Durante a instalação, marque **"Add Python to PATH"**
3. Reinicie o terminal/computador
4. Execute `Executar_DGT.bat` novamente

**Ver mais detalhes:** [Resolução de Problemas - Python](#-resolução-de-problemas---python)

</details>

<details>
<summary><b>⚠️ Erro durante instalação de dependências</b></summary>

**Possíveis causas:**
- Conexão à Internet instável
- Firewall/Antivírus bloqueando downloads
- Falta de permissões administrativas

**Soluções:**
1. Verifique conexão à Internet
2. Desative temporariamente antivírus
3. Execute como Administrador (botão direito → "Executar como administrador")
4. Tente instalação manual:
   ```cmd
   dgt_venv\Scripts\activate
   pip install -r requirements.txt -v
   ```

</details>

<details>
<summary><b>🔧 O popup não aparece no Windows</b></summary>

**Causa:** Restrições de PowerShell ExecutionPolicy.

**Solução:**
Execute uma vez como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois execute normalmente `Executar_DGT.bat`.

</details>

<details>
<summary><b>📊 Quanto tempo demora a primeira execução?</b></summary>

**Tempo estimado: 5-10 minutos**

Dividido em:
- Criação venv: ~30 segundos
- Instalação dependências: 3-5 minutos (varia com conexão)
- Configuração credenciais: ~1 minuto (interação do utilizador)
- Inicialização app: ~10 segundos

**Nota:** Execuções seguintes são instantâneas (2-5 segundos).

</details>

---

## 🔧 Resolução de Problemas - Python

### ⚠️ "Python não encontrado" mas tenho Python 3.12.8 (ou outra versão) instalado

Este é um problema **muito comum** que ocorre quando Python está instalado mas não é detetado pelo sistema.

#### 🎯 Ferramenta de Diagnóstico

Execute o script de teste incluído no projeto:

```cmd
testar_python.bat
```

Este script irá:
- ✅ Verificar se Python é detetado
- ✅ Mostrar a versão instalada
- ✅ Verificar se Python está no PATH do sistema
- ✅ Identificar automaticamente o problema

#### 🔍 Causas Comuns e Soluções

<details>
<summary><b>1️⃣ Terminal Antigo (MAIS COMUM - 80% dos casos)</b></summary>

**Problema:**  
Instalou Python mas está a usar o **mesmo terminal** que estava aberto antes da instalação.

**Por que acontece:**  
O Windows carrega as variáveis de ambiente (incluindo PATH) apenas quando o terminal é aberto. Se instalar Python num terminal já aberto, esse terminal não "vê" o novo Python.

**✅ SOLUÇÃO (Simples):**
1. **FECHE COMPLETAMENTE** todos os terminais/PowerShell/CMD abertos
2. **Abra um NOVO terminal** (tecla Windows → `cmd` → Enter)
3. Execute novamente `Executar_DGT.bat`
4. Python deverá ser detetado agora

**Resultado esperado:**
```
[VERIFICACAO] A verificar instalacao do Python...
[OK] Python 3.12.8 detectado
```

</details>

<details>
<summary><b>2️⃣ Python não está no PATH</b></summary>

**Problema:**  
Durante a instalação de Python, **não marcou** a opção `Add Python to PATH`.

**Verificação:**
```cmd
where python
```
Se mostrar erro "não foi possível encontrar", Python não está no PATH.

**✅ SOLUÇÃO A - Reinstalar (Recomendado):**
1. Painel de Controlo → Programas → Desinstalar Python
2. Descarregar novamente de [python.org/downloads](https://www.python.org/downloads/)
3. Durante instalação, **MARCAR OBRIGATORIAMENTE**: ☑ `Add Python to PATH`
4. Concluir instalação
5. **Fechar todos os terminais**
6. Abrir novo terminal e executar `Executar_DGT.bat`

**✅ SOLUÇÃO B - Adicionar PATH Manualmente (Avançado):**
1. Localizar pasta de instalação Python (normalmente):
   - `C:\Users\<Usuario>\AppData\Local\Programs\Python\Python312`
   - `C:\Python312`
2. Painel de Controlo → Sistema → Configurações avançadas do sistema
3. Botão "Variáveis de Ambiente"
4. Em "Variáveis do sistema", selecionar `Path` → Editar
5. Adicionar **dois** novos caminhos:
   - Pasta Python: `C:\Python312` (ajustar conforme sua versão)
   - Pasta Scripts: `C:\Python312\Scripts`
6. Clicar OK em todas as janelas
7. **REINICIAR todos os terminais**
8. Testar: `python --version`

</details>

<details>
<summary><b>3️⃣ Python instalado via Microsoft Store</b></summary>

**Problema:**  
Python da Microsoft Store pode ter conflitos ou não ser detetado corretamente.

**✅ SOLUÇÃO:**
1. Desinstalar Python da Microsoft Store:
   - Configurações → Aplicações → Python → Desinstalar
2. Instalar versão oficial:
   - [python.org/downloads](https://www.python.org/downloads/)
   - **Marcar**: ☑ `Add Python to PATH`
3. Reiniciar terminal
4. Executar `Executar_DGT.bat`

</details>

<details>
<summary><b>4️⃣ Múltiplas versões Python instaladas</b></summary>

**Problema:**  
Tem várias versões Python e o sistema usa a versão errada.

**Verificação:**
```cmd
where python
```
Se mostrar múltiplos caminhos, há várias versões.

**✅ SOLUÇÃO:**
1. Decidir qual versão manter (recomendado: mais recente ≥ 3.8)
2. Desinstalar versões antigas não necessárias
3. Ou ajustar PATH para priorizar versão desejada (avançado)
4. Testar: `python --version`

</details>

<details>
<summary><b>5️⃣ Permissões ou Antivírus</b></summary>

**Problema:**  
Antivírus ou falta de permissões bloqueia execução de Python.

**✅ SOLUÇÃO:**
1. Executar `Executar_DGT.bat` como **Administrador**:
   - Botão direito → "Executar como administrador"
2. Se ainda falhar, desativar temporariamente antivírus
3. Adicionar pasta do projeto às exceções do antivírus

</details>

#### 📋 Checklist de Verificação

Execute este checklist para garantir que Python está corretamente configurado:

```cmd
REM 1. Testar comando python
python --version

REM 2. Verificar localização
where python

REM 3. Testar execução de código
python -c "print('Python OK')"

REM 4. Verificar pip
pip --version
```

**Todos os comandos devem funcionar sem erros.**

#### 📚 Documentação Completa

Para mais detalhes, consulte o ficheiro:
- **[TROUBLESHOOTING_PYTHON.md](TROUBLESHOOTING_PYTHON.md)** - Guia completo de resolução de problemas

#### ✅ Versões Compatíveis

O DGT Rasters aceita **qualquer versão Python 3.8 ou superior**:

| Versão | Status |
|--------|--------|
| Python 3.7 ou inferior | ❌ Não suportado |
| Python 3.8.x | ✅ Compatível |
| Python 3.9.x | ✅ Compatível |
| Python 3.10.x | ✅ Compatível |
| Python 3.11.x | ✅ Compatível |
| **Python 3.12.x** | ✅ **Compatível** (incluindo 3.12.8) |
| Python 3.13.x | ✅ Compatível (recomendado) |

**Nota:** As mensagens do instalador mencionam Python 3.13 como **recomendado**, mas **não é obrigatório**. Qualquer versão ≥ 3.8 funciona perfeitamente.

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
│  3. Definir Área                        │
│     OPÇÃO A: Mapa interativo (direto)   │
│     • Clique para coordenadas           │
│     • Navegação com drag & zoom         │
│                                         │
│     OPÇÃO B: Processo por Buffer        │
│     • Clicar no botão "Processo Buffer" │
│     • Inserir coordenadas manualmente   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Configurar Buffer                   │
│     • 100m a 15km                       │
│     • Merge opcional (Sim/Não)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Selecionar Pasta de Destino         │
│     • Diálogo de seleção                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  6. Nome do Projeto                     │
│     • Digite o nome identificador       │
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

**Via Mapa Interativo (Recomendado):**
1. Execute `Executar_DGT.bat`
2. Selecione: ☑ MDS-50cm, ☑ LAZ
3. Clique em **"Selecionar Coordenadas no Mapa"**
4. No mapa, clique em Lisboa (aprox. 38.7°N, 9.1°W)
5. Digite buffer: `2` (= 2 km)
6. Diálogo merge: **Sim**
7. Selecione pasta de destino
8. Digite nome do projeto: `Lisboa_2km`
9. Aguarde o download (progresso em terminal)
10. ✅ Ficheiros criados:
    - `Lisboa_2km/MDS-50cm/MDS-50cm.tif` (merged)
    - `Lisboa_2km/LAZ/*.laz` (individuais)

**Alternativa - Via Botão "Processo por Buffer":**
- Útil se preferir inserir coordenadas manualmente
- Mesmo fluxo, mas sem interação com o mapa

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
└── 📂 dgt_venv/                    # Virtual environment (auto-criado)
    ├── Scripts/
    ├── Lib/
    └── ...
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
