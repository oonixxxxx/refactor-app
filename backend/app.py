from flask import Flask, request, jsonify, send_from_directory
import ast
import astor
import os

app = Flask(__name__, static_folder='../front')

def refactor_code(code):
    try:
        # Парсим код в AST (Abstract Syntax Tree)
        tree = ast.parse(code)
        
        # Пример простого рефакторинга: удаление неиспользуемых импортов
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                node.names = [alias for alias in node.names if not alias.name.startswith('unused_')]
        
        # Преобразуем AST обратно в код
        refactored_code = astor.to_source(tree)
        return refactored_code
    except Exception as e:
        return str(e)

@app.route('/refactor', methods=['POST'])
def refactor():
    data = request.json
    code = data.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    refactored_code = refactor_code(code)
    return jsonify({'refactored_code': refactored_code})

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)