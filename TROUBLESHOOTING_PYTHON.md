# Resolução de Problemas - Python não Detetado

## Problema Comum

Se tem Python 3.12.8 (ou outra versão compatível) instalado mas o `Executar_DGT.bat` diz que não encontra o Python, siga estes passos:

## ✅ Versões Compatíveis

O DGT Rasters aceita **qualquer versão Python 3.8 ou superior**, incluindo:
- Python 3.8.x
- Python 3.9.x
- Python 3.10.x
- Python 3.11.x
- **Python 3.12.x** ✓ (incluindo 3.12.8)
- Python 3.13.x

## 🔍 Diagnóstico

### Passo 1: Verificar se Python está instalado

Execute o ficheiro `testar_python.bat` incluído neste projeto. Este script irá:
1. Testar se Python é detetado
2. Mostrar a versão instalada
3. Verificar se Python está no PATH
4. Identificar o problema

### Passo 2: Soluções Comuns

#### ⚠️ SOLUÇÃO 1: Abrir Novo Terminal (Mais Comum)

Se **acabou de instalar Python**, o problema mais comum é que o terminal atual não tem as variáveis de ambiente atualizadas.

**SOLUÇÃO:**
1. **FECHE COMPLETAMENTE** todos os terminais/PowerShell abertos
2. **Abra um NOVO terminal**
3. Execute novamente `Executar_DGT.bat`
4. Python deverá ser detetado agora

#### 🔧 SOLUÇÃO 2: Python não está no PATH

Se Python está instalado mas não foi adicionado ao PATH:

**Opção A - Reinstalar (Recomendado):**
1. Painel de Controlo → Programas → Desinstalar Python
2. Descarregar novamente de https://www.python.org/downloads/
3. Durante instalação, **marcar obrigatoriamente**: ☑ `Add Python to PATH`
4. Concluir instalação
5. Reiniciar terminal

**Opção B - Adicionar PATH Manualmente (Avançado):**
1. Painel de Controlo → Sistema → Configurações avançadas do sistema
2. Variáveis de Ambiente
3. Em "Variáveis do sistema", selecionar `Path` → Editar
4. Adicionar **dois** novos caminhos:
   - `C:\Users\<SeuUsuário>\AppData\Local\Programs\Python\Python312`
   - `C:\Users\<SeuUsuário>\AppData\Local\Programs\Python\Python312\Scripts`
   
   ⚠️ **Nota:** Ajuste "Python312" conforme sua versão instalada
5. Clicar OK em todas as janelas
6. **REINICIAR** todos os terminais

#### 🔄 SOLUÇÃO 3: Python instalado via Microsoft Store

Se instalou Python via Microsoft Store, pode haver conflitos.

**SOLUÇÃO:**
1. Desinstalar Python da Microsoft Store
2. Instalar versão oficial de https://www.python.org/downloads/
3. Marcar `Add Python to PATH` durante instalação

## 📋 Verificação Manual

Abra um **novo** terminal e execute:

```cmd
python --version
```

Deverá mostrar algo como:
```
Python 3.12.8
```

Se mostrar erro, Python não está no PATH.

## 🆘 Ainda não funciona?

Se após todas estas soluções ainda não funcionar:

1. Execute `testar_python.bat` e copie a saída completa
2. Verifique se tem permissões de administrador
3. Verifique se antivírus não está a bloquear Python
4. Tente executar `Executar_DGT.bat` como Administrador

## 💡 Resumo Rápido

**Problema:** Python 3.12.8 instalado mas não detetado
**Causa mais comum:** Terminal antigo (antes da instalação)
**Solução:** Fechar terminal e abrir um novo

---

**Versões Aceites:** Python 3.8+ (incluindo 3.12.8)  
**Versões Recomendadas:** Python 3.12 ou 3.13 (mais recentes)
