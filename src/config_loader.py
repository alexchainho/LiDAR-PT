"""
Módulo para carregar configurações do ficheiro caminhos.json
"""
import json
import os

# Diretório base do projeto (um nível acima de src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """Carrega as configurações do ficheiro caminhos.json"""
    config_path = os.path.join(BASE_DIR, 'config', 'caminhos.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def _resolve_path(path):
    """Resolve caminho relativo para absoluto"""
    if path is None:
        return None
    # Se já for absoluto, retorna como está
    if os.path.isabs(path):
        return path
    # Se for relativo, resolve a partir do diretório base do projeto
    return os.path.abspath(os.path.join(BASE_DIR, path))

def get_credentials():
    """Retorna as credenciais de login"""
    config = load_config()
    return config['credentials']['username'], config['credentials']['password']

def get_path(path_key):
    """Retorna um caminho específico do ficheiro de configuração (resolve relativos)"""
    config = load_config()
    path = config['paths'].get(path_key)
    return _resolve_path(path)

def get_url(url_key):
    """Retorna uma URL específica do ficheiro de configuração"""
    config = load_config()
    return config['urls'].get(url_key)

def get_setting(setting_key):
    """Retorna uma configuração específica"""
    config = load_config()
    return config['settings'].get(setting_key)

def get_all_paths():
    """Retorna todos os caminhos (resolve relativos)"""
    config = load_config()
    paths = config['paths'].copy()
    # Resolver todos os caminhos relativos
    for key, path in paths.items():
        paths[key] = _resolve_path(path)
    return paths

def get_all_urls():
    """Retorna todas as URLs"""
    config = load_config()
    return config['urls']

def get_all_settings():
    """Retorna todas as configurações"""
    config = load_config()
    return config['settings']
