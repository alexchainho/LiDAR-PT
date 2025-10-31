# ============================================================================
# DGT Rasters - Setup Inicial
# Script para configuração inicial do projeto
# ============================================================================

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

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
    }
}
