import os
import json
from flask import Flask, request, jsonify, render_template, send_from_directory

# 1. Configuração do Flask e Definição de Caminhos
# Garante que o Flask saiba onde estão os diretórios estáticos e de templates
app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')

# Define o caminho raiz do projeto para localizar o JSON
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# Caminho completo para o arquivo JSON (deve ser 'data/base.json')
JSON_FILE_PATH = os.path.join(SITE_ROOT, 'data', 'base.json')

# Variável global para armazenar os dados carregados
SEARCH_DATA = []

# Função para carregar o JSON (chamada na inicialização do app)
def load_json_data():
    """Carrega o conteúdo do base.json para a memória."""
    global SEARCH_DATA
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            SEARCH_DATA = json.load(f)
        print(f"Dados de busca carregados com sucesso: {len(SEARCH_DATA)} itens.")
    except FileNotFoundError:
        print(f"ERRO: Arquivo JSON não encontrado em: {JSON_FILE_PATH}. Crie a pasta 'data' e o arquivo 'base.json'.")
    except json.JSONDecodeError:
        print("ERRO: O arquivo JSON está mal formatado. Verifique a sintaxe.")

# Carrega os dados assim que o script for executado
load_json_data()

# 2. Rota Principal para Servir o Frontend HTML
@app.route('/')
def index():
    """Serve a página principal ('templates/index.html')."""
    # Note: O index.html é onde seu código frontend (HTML, CSS, JS) deve estar.
    return render_template('index.html')

# 3. Endpoint de API para a Busca (GET)
@app.route('/api/search', methods=['GET'])
def search():
    """
    Endpoint para buscar no JSON baseado no parâmetro 'query'.
    Retorna os dados, incluindo o 'content_path'.
    """
    query = request.args.get('query', '').lower().strip()
    
    if not query:
        return jsonify([])

    results = []
    
    # Busca de correspondência por sub-string
    for item in SEARCH_DATA:
        # Cria uma string grande com todos os textos para facilitar a busca
        search_text = f"{item.get('title', '')} {item.get('description', '')} {' '.join(item.get('keywords', []))}".lower()
        
        if query in search_text:
            # Retorna todos os campos necessários para o frontend
            results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'description': item.get('description'),
                # Este é o campo crucial para o frontend saber qual arquivo buscar
                'content_path': item.get('content_path') 
            })
    
    return jsonify(results)

# 4. Inicializa o servidor
if __name__ == '__main__':
    # O debug=True permite que o servidor reinicie automaticamente após salvar o código
    # e mostra mensagens de erro detalhadas.
    app.run(debug=True)
