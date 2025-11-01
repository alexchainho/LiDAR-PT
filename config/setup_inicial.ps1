# ============================================================================
# DGT Rasters - Setup Inicial
# Script para configuração inicial do projeto
# ============================================================================

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Função para mostrar aviso de Python não encontrado
function Show-PythonNotFoundDialog {
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Python Nao Encontrado"
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
    $title.Text = "Python Nao Encontrado no Sistema"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkRed
    $form.Controls.Add($title)
    
    # Descrição
    $description = New-Object System.Windows.Forms.TextBox
    $description.Location = New-Object System.Drawing.Point(20, 90)
    $description.Size = New-Object System.Drawing.Size(660, 470)
    $description.Multiline = $true
    $description.ReadOnly = $true
    $description.ScrollBars = "Vertical"
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::LightYellow
    $description.Text = @"
===============================================================================
                    PYTHON NAO ENCONTRADO
===============================================================================

O DGT Rasters requer Python 3.8 ou superior para funcionar.

Python nao foi encontrado no PATH do sistema, o que significa que:
  * Python nao esta instalado, OU
  * Python esta instalado mas nao foi adicionado ao PATH durante instalacao

-------------------------------------------------------------------------------
O QUE E PYTHON?
-------------------------------------------------------------------------------
Python e uma linguagem de programacao necessaria para executar esta aplicacao.
E gratuito, open-source e amplamente utilizado em ciencia de dados e GIS.

-------------------------------------------------------------------------------
COMO INSTALAR PYTHON:
-------------------------------------------------------------------------------

PASSO 1: DOWNLOAD
  • Aceda a: https://www.python.org/downloads/
  • Clique em Download Python 3.12.x (ou versao mais recente)
  • Aguarde download do instalador (aproximadamente 25 MB)

PASSO 2: INSTALACAO
  • Execute o ficheiro descarregado (python-3.12.x.exe)
  
  ** IMPORTANTE **
  
  ┌────────────────────────────────────────────────────────────────┐
  │                                                                │
  │  ☑ MARQUE a opcao: "Add Python to PATH"                       │
  │                                                                │
  │  Esta opcao e OBRIGATORIA para que o Windows encontre Python! │
  │                                                                │
  └────────────────────────────────────────────────────────────────┘
  
  • Clique em "Install Now" (Instalacao Standard)
  • Aguarde conclusao (2-5 minutos)
  • Clique em "Close" ao finalizar

PASSO 3: VERIFICACAO
  • Feche TODAS as janelas de terminal abertas
  • Abra um NOVO terminal (CMD ou PowerShell)
  • Digite: python --version
  • Deve aparecer: Python 3.12.x (ou superior)

PASSO 4: EXECUTAR DGT RASTERS
  • Execute novamente Executar_DGT.bat
  • A instalacao continuara automaticamente

-------------------------------------------------------------------------------
REQUISITOS MINIMOS:
-------------------------------------------------------------------------------
  * Python 3.8 ou superior (recomendado: 3.12+)
  * Sistema Operativo: Windows 10/11
  * Espaco em disco: ~200 MB para Python + 1 GB para bibliotecas

-------------------------------------------------------------------------------
JA TENHO PYTHON INSTALADO?
-------------------------------------------------------------------------------
Se instalou Python mas nao marcou "Add to PATH":

  SOLUCAO 1 - Reinstalar (Recomendado):
    • Desinstale Python atual (Painel de Controlo > Programas)
    • Reinstale seguindo passos acima (marcar "Add to PATH")
  
  SOLUCAO 2 - Adicionar PATH manualmente (Avancado):
    • Painel de Controlo > Sistema > Configuracoes Avancadas
    • Variaveis de Ambiente > PATH > Editar
    • Adicionar: C:\Users\SeuUser\AppData\Local\Programs\Python\Python312
    • Adicionar: C:\Users\SeuUser\AppData\Local\Programs\Python\Python312\Scripts

===============================================================================

Clique em 'Abrir Site Python' para descarregar o instalador.
Apos instalar, execute novamente Executar_DGT.bat

"@
    $form.Controls.Add($description)
    
    # Botão para abrir site
    $btnDownload = New-Object System.Windows.Forms.Button
    $btnDownload.Location = New-Object System.Drawing.Point(340, 580)
    $btnDownload.Size = New-Object System.Drawing.Size(180, 40)
    $btnDownload.Text = "Abrir Site Python"
    $btnDownload.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $btnDownload.BackColor = [System.Drawing.Color]::LightBlue
    $btnDownload.FlatStyle = "Flat"
    $btnDownload.Add_Click({
        Start-Process "https://www.python.org/downloads/"
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
    $form.Text = "Versao Python Desatualizada"
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
    $title.Text = "Versao Python Desatualizada"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkOrange
    $form.Controls.Add($title)
    
    # Descrição
    $description = New-Object System.Windows.Forms.TextBox
    $description.Location = New-Object System.Drawing.Point(20, 90)
    $description.Size = New-Object System.Drawing.Size(660, 380)
    $description.Multiline = $true
    $description.ReadOnly = $true
    $description.ScrollBars = "Vertical"
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::LightYellow
    $description.Text = @"
===============================================================================
              VERSAO PYTHON DESATUALIZADA DETECTADA
===============================================================================

VERSAO ATUAL:    Python $CurrentVersion
VERSAO MINIMA:   Python 3.8
VERSAO RECOMENDADA: Python 3.12+

-------------------------------------------------------------------------------
PROBLEMA:
-------------------------------------------------------------------------------
A versao Python instalada no sistema ($CurrentVersion) e muito antiga e 
nao e compativel com as bibliotecas modernas necessarias para o DGT Rasters.

Bibliotecas como GeoPandas, Rasterio e NumPy requerem Python 3.8 ou superior.

-------------------------------------------------------------------------------
SOLUCAO: ATUALIZAR PYTHON
-------------------------------------------------------------------------------

OPCAO 1 - INSTALACAO LADO-A-LADO (Recomendado):
  
  1. Mantenha a versao atual (nao desinstalar)
  2. Instale nova versao Python 3.12+ em paralelo
  3. Durante instalacao, marque:
     ☑ Add Python to PATH
     ☑ Install for all users (opcional)
  
  4. A nova versao sera usada por padrao

OPCAO 2 - DESINSTALAR E REINSTALAR:
  
  1. Painel de Controlo > Programas > Desinstalar Python $CurrentVersion
  2. Aceda a: https://www.python.org/downloads/
  3. Descarregue Python 3.12.x ou superior
  4. Execute instalador com opcao "Add to PATH" marcada

-------------------------------------------------------------------------------
PASSOS PARA ATUALIZAR:
-------------------------------------------------------------------------------

1. DOWNLOAD:
   • Aceda: https://www.python.org/downloads/
   • Download Python 3.12.x (botao amarelo grande)

2. INSTALACAO:
   • Execute python-3.12.x.exe
   • ☑ MARQUE: "Add Python to PATH"
   • Clique: "Install Now"
   • Aguarde 2-5 minutos

3. VERIFICACAO:
   • Feche todos os terminais abertos
   • Abra NOVO terminal
   • Digite: python --version
   • Confirme: Python 3.12.x

4. EXECUTAR DGT RASTERS:
   • Execute novamente Executar_DGT.bat
   • Instalacao continuara automaticamente

===============================================================================

Clique em 'Abrir Site Python' para descarregar versao atualizada.

"@
    $form.Controls.Add($description)
    
    # Botão para abrir site
    $btnDownload = New-Object System.Windows.Forms.Button
    $btnDownload.Location = New-Object System.Drawing.Point(340, 490)
    $btnDownload.Size = New-Object System.Drawing.Size(180, 40)
    $btnDownload.Text = "Abrir Site Python"
    $btnDownload.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $btnDownload.BackColor = [System.Drawing.Color]::LightBlue
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
    $description = New-Object System.Windows.Forms.TextBox
    $description.Location = New-Object System.Drawing.Point(20, 70)
    $description.Size = New-Object System.Drawing.Size(610, 340)
    $description.Multiline = $true
    $description.ReadOnly = $true
    $description.ScrollBars = "Vertical"
    $description.Font = New-Object System.Drawing.Font("Consolas", 9)
    $description.BackColor = [System.Drawing.Color]::White
    $description.Text = @"
===============================================================================
                     PRIMEIRA EXECUCAO DETECTADA!
===============================================================================

Este assistente ira configurar o DGT Rasters no seu sistema.

PASSOS DA INSTALACAO:

-------------------------------------------------------------------------------
  1. CRIAR AMBIENTE VIRTUAL PYTHON (dgt_venv)
     * Isola as dependencias do projeto
     * Evita conflitos com outros projetos Python
     * Garante versoes especificas das bibliotecas

-------------------------------------------------------------------------------
  2. INSTALAR DEPENDENCIAS NECESSARIAS
     * GeoPandas, Rasterio, Tkinter e outras bibliotecas
     * Ferramentas para processamento geoespacial
     * Pode demorar 3-5 minutos (download + instalacao)

-------------------------------------------------------------------------------
  3. CONFIGURAR CREDENCIAIS DGT
     * Username e password para acesso aos dados
     * Necessario para download de ficheiros LiDAR
     * Sera solicitado numa janela apos instalacao

-------------------------------------------------------------------------------
  4. INICIAR APLICACAO
     * Interface grafica com mapa interativo
     * Selecao de produtos (LAZ, MDS, MDT)
     * Definicao de area de interesse

===============================================================================

REQUISITOS:
  [OK] Python 3.8+ instalado (obrigatorio)
  [OK] Conexao a Internet (obrigatoria)
  [OK] Espaco em disco: minimo 1GB para instalacao
  [..] Credenciais DGT (sera solicitado a seguir)

TEMPO ESTIMADO: 5-10 minutos

===============================================================================

Clique em 'Continuar' para iniciar a instalacao...

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
    $title.Text = "Configuracao de Credenciais de Acesso"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = [System.Drawing.Color]::DarkBlue
    $form.Controls.Add($title)
    
    # Informação
    $info = New-Object System.Windows.Forms.TextBox
    $info.Location = New-Object System.Drawing.Point(20, 70)
    $info.Size = New-Object System.Drawing.Size(620, 320)
    $info.Multiline = $true
    $info.ReadOnly = $true
    $info.ScrollBars = "Vertical"
    $info.Font = New-Object System.Drawing.Font("Consolas", 9)
    $info.BackColor = [System.Drawing.Color]::LightYellow
    $info.Text = @"
===============================================================================
         ACESSO AO CENTRO DE DESCARGAS DE DADOS DA DGT
===============================================================================

Para descarregar dados geograficos (LiDAR, MDS, MDT) da 
Direcao-Geral do Territorio, e necessario ter credenciais de acesso ao 
Centro de Descargas de Dados (CDD).

-------------------------------------------------------------------------------
INFORMACAO DO SERVICO:
-------------------------------------------------------------------------------
  * Entidade: Direcao-Geral do Territorio (DGT)
  * Servico: Centro de Descargas de Dados (CDD)
  * URL: https://cdd.dgterritorio.gov.pt
  * Dados: LiDAR, Modelos Digitais de Portugal

-------------------------------------------------------------------------------
NAO TEM CONTA? SIGA ESTES PASSOS:
-------------------------------------------------------------------------------

  1. Aceda ao site: https://cdd.dgterritorio.gov.pt/dgt-fe (link em baixo)
  
  2. Clique em Registar / Criar Conta Nova
  
  3. Preencha o formulario com os dados solicitados

  4. Pode ser necessario aguardar email de confirmacao para ativar a conta

  5. Apos ativacao, utilize as credenciais abaixo

-------------------------------------------------------------------------------
IMPORTANTE:
-------------------------------------------------------------------------------
  * As credenciais sao guardadas localmente em: config\caminhos.json
  * Nao sao partilhadas ou enviadas para outros servicos
  * Sao usadas apenas para autenticacao no servidor DGT

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
    $linkLabel.Text = "Nao tem conta? Clique aqui para criar registo no Centro de Descargas da DGT"
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
                "Por favor, preencha o username (email) e password.`n`nSem credenciais nao e possivel descarregar dados da DGT.",
                "Campos Obrigatorios",
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
