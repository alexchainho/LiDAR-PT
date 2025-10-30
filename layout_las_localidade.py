import os
import laspy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Configurações ---
# Pasta onde estão os ficheiros LAS (ajustar se necessário)
PASTA_LAS = r"D:\CSTE\DGT_Rasters\localidades"
# Nome da localidade (pode ser passado como argumento ou detetado automaticamente)
NOME_LOCALIDADE = None  # Se None, deteta automaticamente a primeira subpasta

# --- Função para encontrar as pastas de LAS ---
def encontrar_pasta_las(base_path):
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            las_dir = os.path.join(root, d, "LAZ")
            if os.path.exists(las_dir):
                return las_dir, d
    return None, None

# --- Carregar todos os LAS da pasta ---
def carregar_las(pasta):
    pontos = []
    classes = []
    for fname in os.listdir(pasta):
        if fname.lower().endswith('.las'):
            las_path = os.path.join(pasta, fname)
            with laspy.open(las_path) as f:
                las = f.read()
                xyz = np.vstack((las.x, las.y, las.z)).T
                pontos.append(xyz)
                classes.append(las.classification)
    if pontos:
        return np.vstack(pontos), np.hstack(classes)
    else:
        return None, None

# --- Paleta de cores para classes LAS padrão ---
CORES_CLASSES = {
    1: 'gray',    # Unclassified
    2: 'green',   # Ground
    3: 'brown',   # Low Vegetation
    4: 'yellow',  # Medium Vegetation
    5: 'darkgreen', # High Vegetation
    6: 'red',     # Building
    7: 'purple',  # Low Point (noise)
    9: 'blue',    # Water
    17: 'orange', # Bridge deck
    18: 'pink',   # High noise
}
def cor_por_classe(cls):
    return CORES_CLASSES.get(cls, 'black')

# --- Main ---
def main():
    global NOME_LOCALIDADE
    if NOME_LOCALIDADE is None:
        las_dir, nome = encontrar_pasta_las(PASTA_LAS)
        if not las_dir:
            print("Nenhuma pasta LAZ/LAS encontrada!")
            return
        NOME_LOCALIDADE = nome
    else:
        las_dir = os.path.join(PASTA_LAS, NOME_LOCALIDADE, "LAZ")
    print(f"A carregar LAS de: {las_dir}")
    pontos, classes = carregar_las(las_dir)
    if pontos is None:
        print("Nenhum ficheiro LAS encontrado!")
        return
    # --- Plot 3D ---
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    # Plotar por classe
    for cls in np.unique(classes):
        mask = classes == cls
        ax.scatter(pontos[mask,0], pontos[mask,1], pontos[mask,2],
                   s=0.5, c=cor_por_classe(cls), label=f'Classe {cls}', alpha=0.7)
    ax.view_init(elev=30, azim=45)  # Inclinação 45º
    ax.set_title(f"LAS - {NOME_LOCALIDADE}")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(markerscale=6, loc='upper right', fontsize='small')
    plt.tight_layout()
    out_path = os.path.join(las_dir, f"layout_las_{NOME_LOCALIDADE}.png")
    plt.savefig(out_path, dpi=300)
    print(f"Layout salvo em: {out_path}")
    plt.show()

if __name__ == "__main__":
    main()
