import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Função para abrir a janela de seleção de projeto

def selecionar_processo():
    root = tk.Tk()
    root.withdraw()
    
    # Variáveis para checkboxes
    mds_var = tk.BooleanVar(value=True)
    laz_var = tk.BooleanVar(value=False)

    def abrir_buffer():
        script_path = os.path.join(os.path.dirname(__file__), 'processo_por_buffer.py')
        args = ['python', script_path]
        if mds_var.get() and not laz_var.get():
            args.append('--tipo=MDS')
        elif laz_var.get() and not mds_var.get():
            args.append('--tipo=LAZ')
        # ambos ou nenhum: default (ambos)
        subprocess.Popen(args)
        root.destroy()

    def abrir_localidade():
        script_path = os.path.join(os.path.dirname(__file__), 'processo_por_localidade.py')
        args = ['python', script_path]
        if mds_var.get() and not laz_var.get():
            args.append('--tipo=MDS')
        elif laz_var.get() and not mds_var.get():
            args.append('--tipo=LAZ')
        # ambos ou nenhum: default (ambos)
        subprocess.Popen(args)
        root.destroy()

    win = tk.Toplevel()
    win.title("Selecionar Processo")
    tk.Label(win, text="Escolha o tipo de dados a descarregar:").pack(padx=20, pady=(10,0))
    tk.Checkbutton(win, text="MDS-50cm", variable=mds_var).pack(anchor='w', padx=30)
    tk.Checkbutton(win, text="LAZ", variable=laz_var).pack(anchor='w', padx=30)
    tk.Label(win, text="Escolha o tipo de projeto:").pack(padx=20, pady=(10,0))
    tk.Button(win, text="Processo por Buffer", command=abrir_buffer, width=25).pack(pady=5)
    tk.Button(win, text="Processo por Localidade", command=abrir_localidade, width=25).pack(pady=5)
    win.mainloop()

if __name__ == "__main__":
    selecionar_processo()
