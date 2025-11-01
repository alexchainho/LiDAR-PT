# ============================================================================
# DGT Rasters - Setup Inicial
# Script para configuração inicial do projeto
# ============================================================================

# Garantir encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Função para mostrar aviso de Python não encontrado
function Show-PythonNotFoundDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Python Não Encontrado"
    $form.Size = New-Object System.Drawing.Size(700, 680)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    
    # Ícone de aviso (símbolo ⚠)
    $iconLabel = New-Object System.Windows.Forms.Label
    $iconLabel.Location = New-Object System.Drawing.Point(20, 20)
    $iconLabel.Size = New-Object System.Drawing.Size(60, 60)
    $iconLabel.Text = "⚠"
    $iconLabel.Font = New-Object System.Drawing.Font("Segoe UI", 36, [System.Drawing.FontStyle]::Bold)
    $iconLabel.ForeColor = [System.Drawing.Color]::Orange
    $iconLabel.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
    $form.Controls.Add($iconLabel)
    
    # Título
    $title = New-Object System.Windows.Forms.Label
    $title.Location = New-Object System.Drawing.Point(90, 30)
    $title.Size = New-Object System.Drawing.Size(580, 40)
    $title.Text = "Python Não Encontrado no Sistema"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkRed
    $form.Controls.Add($title)
    
    # Descrição
    $description = New-Object System.Windows.Forms.RichTextBox
    $description.Location = New-Object System.Drawing.Point(20, 90)
    $description.Size = New-Object System.Drawing.Size(660, 470)
    $description.ReadOnly = $true
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::LightYellow
    $description.Text = @"
===============================================================================
                    PYTHON NÃO ENCONTRADO
===============================================================================

O DGT Rasters requer Python 3.8 ou superior para funcionar.

Python não foi encontrado no PATH do sistema, o que significa que:
  • Python não está instalado, OU
  • Python está instalado mas não foi adicionado ao PATH durante instalação

-------------------------------------------------------------------------------
O QUE É PYTHON?
-------------------------------------------------------------------------------
Python é uma linguagem de programação necessária para executar esta aplicação.
É gratuito, open-source e amplamente utilizado em ciência de dados e GIS.

-------------------------------------------------------------------------------
PORQUÊ PYTHON?
-------------------------------------------------------------------------------
O DGT Rasters utiliza Python para:
  • Processar dados geoespaciais (LiDAR, rasters)
  • Gerir downloads automáticos do servidor DGT
  • Manipular grandes volumes de dados geográficos
  • Criar interfaces gráficas interativas com mapas
  • Garantir compatibilidade com bibliotecas GIS standard (GDAL, GeoPandas)

Sem Python, a aplicação NÃO pode funcionar.

-------------------------------------------------------------------------------
COMO INSTALAR PYTHON 3.13:
-------------------------------------------------------------------------------

PASSO 1: DOWNLOAD
  • Clique no botão "Descarregar Python 3.13" abaixo
  • Será redirecionado para: https://www.python.org/downloads/release/python-3139/
  • percorra para baixo até encontrar "Windows installer (64-bit)"
  • Aguarde download do instalador (aproximadamente 25 MB)

PASSO 2: INSTALAÇÃO
  • Execute o ficheiro descarregado (python-3.13.x.exe)
  
  ** MUITO IMPORTANTE **
  
  ┌────────────────────────────────────────────────────────────────┐
  │                                                                │
  │  ☑ MARQUE a opção: "Add Python 3.13 to PATH"                  │
  │                                                                │
  │  Esta opção é OBRIGATÓRIA para que o Windows encontre Python!  │
  │                                                                │
  └────────────────────────────────────────────────────────────────┘
  
  • Clique em "Install Now" (Instalação Standard)
  • Aguarde conclusão (2-5 minutos)
  • Clique em "Close" ao finalizar

PASSO 3: VERIFICAÇÃO
  • Feche TODAS as janelas de terminal abertas
  • Abra um NOVO terminal (CMD ou PowerShell)
  • Digite: python --version
  • Deve aparecer: Python 3.13.x (ou superior)

PASSO 4: EXECUTAR DGT RASTERS
  • Execute novamente Executar_DGT.bat
  • A instalação continuará automaticamente

-------------------------------------------------------------------------------
REQUISITOS MÍNIMOS:
-------------------------------------------------------------------------------
  • Python 3.8 ou superior (recomendado: 3.13+)
  • Sistema Operativo: Windows 10/11
  • Espaço em disco: ~200 MB para Python + 1 GB para bibliotecas

-------------------------------------------------------------------------------
JÁ TENHO PYTHON INSTALADO?
-------------------------------------------------------------------------------
Se instalou Python mas não marcou "Add to PATH":

  SOLUÇÃO 1 - Reinstalar (Recomendado):
    • Desinstale Python atual (Painel de Controlo > Programas)
    • Reinstale seguindo passos acima (marcar "Add to PATH")
  
  SOLUÇÃO 2 - Adicionar PATH manualmente (Avançado):
    • Painel de Controlo > Sistema > Configurações Avançadas
    • Variáveis de Ambiente > PATH > Editar
    • Adicionar: C:\Users\SeuUser\AppData\Local\Programs\Python\Python313
    • Adicionar: C:\Users\SeuUser\AppData\Local\Programs\Python\Python313\Scripts

===============================================================================

Clique em 'Descarregar Python 3.13' para abrir a página de download.
Após instalar, execute novamente Executar_DGT.bat

"@
    $form.Controls.Add($description)
    
    # Botão para abrir site e fechar programa
    $btnDownload = New-Object System.Windows.Forms.Button
    $btnDownload.Location = New-Object System.Drawing.Point(300, 580)
    $btnDownload.Size = New-Object System.Drawing.Size(220, 40)
    $btnDownload.Text = "Descarregar Python 3.13"
    $btnDownload.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $btnDownload.BackColor = [System.Drawing.Color]::LightGreen
    $btnDownload.FlatStyle = "Flat"
    $btnDownload.Add_Click({
        Start-Process "https://www.python.org/downloads/"
        $form.DialogResult = [System.Windows.Forms.DialogResult]::Abort
        $form.Close()
    })
    $form.Controls.Add($btnDownload)
    
    # Botão Fechar
    $btnClose = New-Object System.Windows.Forms.Button
    $btnClose.Location = New-Object System.Drawing.Point(540, 580)
    $btnClose.Size = New-Object System.Drawing.Size(140, 40)
    $btnClose.Text = "Fechar"
    $btnClose.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $btnClose.FlatStyle = "Flat"
    $btnClose.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.Controls.Add($btnClose)
    
    $form.CancelButton = $btnClose
    
    $result = $form.ShowDialog()
    return $result
}

# Função para mostrar aviso de versão Python antiga
function Show-PythonVersionDialog {
    param(
        [string]$CurrentVersion
    )
    
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Versão Python Desatualizada"
    $form.Size = New-Object System.Drawing.Size(700, 580)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    
    # Ícone de aviso
    $iconLabel = New-Object System.Windows.Forms.Label
    $iconLabel.Location = New-Object System.Drawing.Point(20, 20)
    $iconLabel.Size = New-Object System.Drawing.Size(60, 60)
    $iconLabel.Text = "⚠"
    $iconLabel.Font = New-Object System.Drawing.Font("Segoe UI", 36, [System.Drawing.FontStyle]::Bold)
    $iconLabel.ForeColor = [System.Drawing.Color]::Orange
    $iconLabel.TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
    $form.Controls.Add($iconLabel)
    
    # Título
    $title = New-Object System.Windows.Forms.Label
    $title.Location = New-Object System.Drawing.Point(90, 30)
    $title.Size = New-Object System.Drawing.Size(580, 40)
    $title.Text = "Versão Python Desatualizada"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkOrange
    $form.Controls.Add($title)
    
    # Descrição
    $description = New-Object System.Windows.Forms.RichTextBox
    $description.Location = New-Object System.Drawing.Point(20, 90)
    $description.Size = New-Object System.Drawing.Size(660, 380)
    $description.ReadOnly = $true
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::LightYellow
    $description.Text = @"
===============================================================================
              VERSÃO PYTHON DESATUALIZADA DETETADA
===============================================================================

VERSÃO ATUAL:        Python $CurrentVersion
VERSÃO MÍNIMA:       Python 3.8
VERSÃO RECOMENDADA:  Python 3.13+

-------------------------------------------------------------------------------
PROBLEMA:
-------------------------------------------------------------------------------
A versão Python instalada no sistema ($CurrentVersion) é muito antiga e 
não é compatível com as bibliotecas modernas necessárias para o DGT Rasters.

Bibliotecas como GeoPandas, Rasterio e NumPy requerem Python 3.8 ou superior.

-------------------------------------------------------------------------------
SOLUÇÃO: ATUALIZAR PYTHON
-------------------------------------------------------------------------------

OPÇÃO 1 - INSTALAÇÃO LADO-A-LADO (Recomendado):
  
  1. Mantenha a versão atual (não desinstalar)
  2. Instale nova versão Python 3.13+ em paralelo
  3. Durante instalação, marque:
     ☑ Add Python 3.13 to PATH
     ☑ Install for all users (opcional)
  
  4. A nova versão será usada por padrão

OPÇÃO 2 - DESINSTALAR E REINSTALAR:
  
  1. Painel de Controlo > Programas > Desinstalar Python $CurrentVersion
  2. Aceda a: https://www.python.org/downloads/
  3. Descarregue Python 3.13.x ou superior
  4. Execute instalador com opção "Add to PATH" marcada

-------------------------------------------------------------------------------
PASSOS PARA ATUALIZAR:
-------------------------------------------------------------------------------

1. DOWNLOAD:
   • Clique no botão "Descarregar Python 3.13" abaixo
   • Será redirecionado para: https://www.python.org/downloads/
   • Download Python 3.13.x (botão amarelo grande)

2. INSTALAÇÃO:
   • Execute python-3.13.x.exe
   • ☑ MARQUE: "Add Python 3.13 to PATH"
   • Clique: "Install Now"
   • Aguarde 2-5 minutos

3. VERIFICAÇÃO:
   • Feche todos os terminais abertos
   • Abra NOVO terminal
   • Digite: python --version
   • Confirme: Python 3.13.x

4. EXECUTAR DGT RASTERS:
   • Execute novamente Executar_DGT.bat
   • Instalação continuará automaticamente

===============================================================================

Clique em 'Descarregar Python 3.13' para obter a versão atualizada.

"@
    $form.Controls.Add($description)
    
    # Botão para abrir site
    $btnDownload = New-Object System.Windows.Forms.Button
    $btnDownload.Location = New-Object System.Drawing.Point(300, 490)
    $btnDownload.Size = New-Object System.Drawing.Size(220, 40)
    $btnDownload.Text = "Descarregar Python 3.13"
    $btnDownload.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $btnDownload.BackColor = [System.Drawing.Color]::LightGreen
    $btnDownload.FlatStyle = "Flat"
    $btnDownload.Add_Click({
        Start-Process "https://www.python.org/downloads/"
    })
    $form.Controls.Add($btnDownload)
    
    # Botão Fechar
    $btnClose = New-Object System.Windows.Forms.Button
    $btnClose.Location = New-Object System.Drawing.Point(540, 490)
    $btnClose.Size = New-Object System.Drawing.Size(140, 40)
    $btnClose.Text = "Fechar"
    $btnClose.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $btnClose.FlatStyle = "Flat"
    $btnClose.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.Controls.Add($btnClose)
    
    $form.CancelButton = $btnClose
    
    $result = $form.ShowDialog()
    return $result
}

# Função para mostrar janela de boas-vindas
function Show-WelcomeDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "DGT Rasters - Bem-vindo"
    $form.Size = New-Object System.Drawing.Size(650, 500)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    
    # Título
    $title = New-Object System.Windows.Forms.Label
    $title.Location = New-Object System.Drawing.Point(20, 20)
    $title.Size = New-Object System.Drawing.Size(610, 40)
    $title.Text = "DGT Rasters - Sistema de Download de Dados Geoespaciais"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkBlue
    $form.Controls.Add($title)
    
    # Descrição
    $description = New-Object System.Windows.Forms.RichTextBox
    $description.Location = New-Object System.Drawing.Point(20, 70)
    $description.Size = New-Object System.Drawing.Size(610, 340)
    $description.ReadOnly = $true
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::White
    $description.Text = @"
===============================================================================
                     PRIMEIRA EXECUÇÃO DETETADA!
===============================================================================

Este assistente irá configurar o DGT Rasters no seu sistema.

PASSOS DA INSTALAÇÃO:

-------------------------------------------------------------------------------
  1. CRIAR AMBIENTE VIRTUAL PYTHON (dgt_venv)
     • Isola as dependências do projeto
     • Evita conflitos com outros projetos Python
     • Garante versões específicas das bibliotecas

-------------------------------------------------------------------------------
  2. INSTALAR DEPENDÊNCIAS NECESSÁRIAS
     • GeoPandas, Rasterio, Tkinter e outras bibliotecas
     • Ferramentas para processamento geoespacial
     • Pode demorar 3-5 minutos (download + instalação)

-------------------------------------------------------------------------------
  3. CONFIGURAR CREDENCIAIS DGT
     • Username e password para acesso aos dados
     • Necessário para download de ficheiros LiDAR
     • Será solicitado numa janela após instalação

-------------------------------------------------------------------------------
  4. INICIAR APLICAÇÃO
     • Interface gráfica com mapa interativo
     • Seleção de produtos (LAZ, MDS, MDT)
     • Definição de área de interesse

===============================================================================

REQUISITOS:
  [OK] Python 3.8+ instalado (obrigatório)
  [OK] Conexão à Internet (obrigatória)
  [OK] Espaço em disco: mínimo 1GB para instalação
  [..] Credenciais DGT (será solicitado a seguir)

TEMPO ESTIMADO: 5-10 minutos

===============================================================================

Clique em 'Continuar' para iniciar a instalação...

"@
    $form.Controls.Add($description)
    
    # Botão Continuar
    $btnOK = New-Object System.Windows.Forms.Button
    $btnOK.Location = New-Object System.Drawing.Point(430, 420)
    $btnOK.Size = New-Object System.Drawing.Size(100, 35)
    $btnOK.Text = "Continuar"
    $btnOK.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $btnOK.BackColor = [System.Drawing.Color]::LightGreen
    $btnOK.FlatStyle = "Flat"
    $btnOK.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $form.Controls.Add($btnOK)
    
    # Botão Cancelar
    $btnCancel = New-Object System.Windows.Forms.Button
    $btnCancel.Location = New-Object System.Drawing.Point(310, 420)
    $btnCancel.Size = New-Object System.Drawing.Size(100, 35)
    $btnCancel.Text = "Cancelar"
    $btnCancel.Font = New-Object System.Drawing.Font("Segoe UI", 10)
    $btnCancel.FlatStyle = "Flat"
    $btnCancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.Controls.Add($btnCancel)
    
    $form.AcceptButton = $btnOK
    $form.CancelButton = $btnCancel
    
    $result = $form.ShowDialog()
    return $result -eq [System.Windows.Forms.DialogResult]::OK
}


# Função para solicitar credenciais DGT
function Show-CredentialsDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Credenciais DGT - Centro de Descargas"
    $form.Size = New-Object System.Drawing.Size(650, 620)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false
    $form.MinimizeBox = $false
    
    # Título
    $title = New-Object System.Windows.Forms.Label
    $title.Location = New-Object System.Drawing.Point(20, 20)
    $title.Size = New-Object System.Drawing.Size(610, 40)
    $title.Text = "Configuração de Credenciais de Acesso"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkBlue
    $form.Controls.Add($title)
    
    # Informação
    $info = New-Object System.Windows.Forms.RichTextBox
    $info.Location = New-Object System.Drawing.Point(20, 70)
    $info.Size = New-Object System.Drawing.Size(620, 320)
    $info.ReadOnly = $true
    $info.Font = New-Object System.Drawing.Font("Consolas", 9)
    $info.BackColor = [System.Drawing.Color]::LightYellow
    $info.Text = @"
===============================================================================
         ACESSO AO CENTRO DE DESCARGAS DE DADOS DA DGT
===============================================================================

Para descarregar dados geográficos (LiDAR, MDS, MDT) da 
Direção-Geral do Território, é necessário ter credenciais de acesso ao 
Centro de Descargas de Dados (CDD).

-------------------------------------------------------------------------------
INFORMAÇÃO DO SERVIÇO:
-------------------------------------------------------------------------------
  • Entidade: Direção-Geral do Território (DGT)
  • Serviço: Centro de Descargas de Dados (CDD)
  • URL: https://cdd.dgterritorio.gov.pt
  • Dados: LiDAR, Modelos Digitais de Portugal

-------------------------------------------------------------------------------
NÃO TEM CONTA? SIGA ESTES PASSOS:
-------------------------------------------------------------------------------

  1. Aceda ao site: https://cdd.dgterritorio.gov.pt/dgt-fe (link em baixo)
  
  2. Clique em Registar / Criar Conta Nova
  
  3. Preencha o formulário com os dados solicitados

  4. Pode ser necessário aguardar email de confirmação para ativar a conta

  5. Após ativação, utilize as credenciais abaixo

-------------------------------------------------------------------------------
IMPORTANTE:
-------------------------------------------------------------------------------
  • As credenciais são guardadas localmente em: config\caminhos.json
  • Não são partilhadas ou enviadas para outros serviços
  • São usadas apenas para autenticação no servidor DGT

===============================================================================

"@
    $form.Controls.Add($info)
    
    # Username
    $lblUsername = New-Object System.Windows.Forms.Label
    $lblUsername.Location = New-Object System.Drawing.Point(20, 405)
    $lblUsername.Size = New-Object System.Drawing.Size(180, 25)
    $lblUsername.Text = "Username (Email):"
    $lblUsername.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $form.Controls.Add($lblUsername)
    
    $txtUsername = New-Object System.Windows.Forms.TextBox
    $txtUsername.Location = New-Object System.Drawing.Point(200, 405)
    $txtUsername.Size = New-Object System.Drawing.Size(430, 28)
    $txtUsername.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $txtUsername.TabIndex = 0
    $form.Controls.Add($txtUsername)
    
    # Password
    $lblPassword = New-Object System.Windows.Forms.Label
    $lblPassword.Location = New-Object System.Drawing.Point(20, 445)
    $lblPassword.Size = New-Object System.Drawing.Size(180, 25)
    $lblPassword.Text = "Password:"
    $lblPassword.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $form.Controls.Add($lblPassword)
    
    $txtPassword = New-Object System.Windows.Forms.TextBox
    $txtPassword.Location = New-Object System.Drawing.Point(200, 445)
    $txtPassword.Size = New-Object System.Drawing.Size(430, 28)
    $txtPassword.PasswordChar = '*'
    $txtPassword.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $txtPassword.TabIndex = 1
    $form.Controls.Add($txtPassword)
    
    # Link para registo
    $linkLabel = New-Object System.Windows.Forms.LinkLabel
    $linkLabel.Location = New-Object System.Drawing.Point(20, 485)
    $linkLabel.Size = New-Object System.Drawing.Size(610, 25)
    $linkLabel.Text = "Não tem conta? Clique aqui para criar registo no Centro de Descargas da DGT"
    $linkLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Italic)
    $linkLabel.LinkColor = [System.Drawing.Color]::Blue
    $linkLabel.ActiveLinkColor = [System.Drawing.Color]::Red
    $linkLabel.Add_LinkClicked({
        Start-Process "https://cdd.dgterritorio.gov.pt/dgt-fe"
    })
    $form.Controls.Add($linkLabel)
    
    # Botões
    $btnOK = New-Object System.Windows.Forms.Button
    $btnOK.Location = New-Object System.Drawing.Point(530, 545)
    $btnOK.Size = New-Object System.Drawing.Size(100, 35)
    $btnOK.Text = "Guardar"
    $btnOK.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $btnOK.BackColor = [System.Drawing.Color]::LightGreen
    $btnOK.FlatStyle = "Flat"
    $btnOK.TabIndex = 2
    $btnOK.Add_Click({
        if ([string]::IsNullOrWhiteSpace($txtUsername.Text) -or [string]::IsNullOrWhiteSpace($txtPassword.Text)) {
            [System.Windows.Forms.MessageBox]::Show(
                "Por favor, preencha o username (email) e password.`n`nSem credenciais não é possível descarregar dados da DGT.",
                "Campos Obrigatórios",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Warning
            )
        } else {
            $form.Tag = @{
                Username = $txtUsername.Text.Trim()
                Password = $txtPassword.Text
            }
            $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        }
    })
    $form.Controls.Add($btnOK)
    
    $btnCancel = New-Object System.Windows.Forms.Button
    $btnCancel.Location = New-Object System.Drawing.Point(410, 545)
    $btnCancel.Size = New-Object System.Drawing.Size(100, 35)
    $btnCancel.Text = "Cancelar"
    $btnCancel.Font = New-Object System.Drawing.Font("Segoe UI", 11)
    $btnCancel.FlatStyle = "Flat"
    $btnCancel.TabIndex = 3
    $btnCancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.Controls.Add($btnCancel)
    
    $form.AcceptButton = $btnOK
    $form.CancelButton = $btnCancel
    
    # Focar no campo username ao abrir
    $form.Add_Shown({
        $form.Activate()
        $txtUsername.Focus()
    })
    
    $result = $form.ShowDialog()
    
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        return $form.Tag
    }
    return $null
}

# Se executado diretamente (não como módulo)
if ($MyInvocation.InvocationName -ne '.') {
    # Executar a função especificada via parâmetro -Command
    if ($args.Count -gt 0) {
        $functionName = $args[0]
        if ($functionName -eq 'Show-WelcomeDialog') {
            $result = Show-WelcomeDialog
            if ($result) {
                exit 0
            } else {
                exit 1
            }
        }
        elseif ($functionName -eq 'Show-CredentialsDialog') {
            $result = Show-CredentialsDialog
            if ($result) {
                exit 0
            } else {
                exit 1
            }
        }
        elseif ($functionName -eq 'Show-PythonNotFoundDialog') {
            $result = Show-PythonNotFoundDialog
            exit 0
        }
        elseif ($functionName -eq 'Show-PythonVersionDialog') {
            if ($args.Count -gt 1) {
                $version = $args[1]
                $result = Show-PythonVersionDialog -CurrentVersion $version
            }
            exit 0
        }
    }
}
