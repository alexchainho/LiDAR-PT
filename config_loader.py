"""
Módulo para carregar configurações do ficheiro caminhos.json
"""
import json
import os

def load_config():
    """Carrega as configurações do ficheiro caminhos.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'caminhos.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_credentials():
    """Retorna as credenciais de login"""
    config = load_config()
    return config['credentials']['username'], config['credentials']['password']

def get_path(path_key):
    """Retorna um caminho específico do ficheiro de configuração"""
    config = load_config()
    return config['paths'].get(path_key)

def get_url(url_key):
    """Retorna uma URL específica do ficheiro de configuração"""
    config = load_config()
    return config['urls'].get(url_key)

def get_setting(setting_key):
    """Retorna uma configuração específica"""
    config = load_config()
    return config['settings'].get(setting_key)

def get_all_paths():
    """Retorna todos os caminhos"""
    config = load_config()
    return config['paths']

def get_all_urls():
    """Retorna todas as URLs"""
    config = load_config()
    return config['urls']

def get_all_settings():
    """Retorna todas as configurações"""
    config = load_config()
    return config['settings']
