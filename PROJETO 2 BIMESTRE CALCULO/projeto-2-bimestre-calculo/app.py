from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import pandas as pd
from pathlib import Path
from calculos import funcao_quadratica, derivada_funcao_quadratica

app = Flask(__name__)
CORS(app)

def load_data():
    csv_path = Path(__file__).parent / 'tabela_inmetro_carros_2025.csv'
    df = pd.read_csv(csv_path, sep=';', encoding='Latin-1', decimal=',')
    
    df['id'] = range(len(df))
    return df

df = load_data()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/catalogo', methods=['GET'])
def catalogo():
    try:
        catalogo_data = {}
        
        
        for marca in df['Marca'].dropna().unique():
            catalogo_data[marca] = []
            marca_df = df[df['Marca'] == marca]
            
            
            for modelo in marca_df['Modelo'].dropna().unique():
                modelo_df = marca_df[marca_df['Modelo'] == modelo]
                
                
                modelo_info = {
                    'modelo': modelo,
                    'versoes': len(modelo_df),
                    'combustiveis': modelo_df['Combustível'].unique().tolist(),
                }
                catalogo_data[marca].append(modelo_info)
        
        return jsonify({'sucesso': True, 'catalogo': catalogo_data}), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/filtros', methods=['GET'])
def opcoes_filtros():
    """Retorna opções disponíveis para filtros"""
    try:
        filtros = {
            'marcas': sorted(df['Marca'].dropna().unique().tolist()),
            'combustiveis': sorted(df['Combustível'].dropna().unique().tolist()),
            'propulsoes': sorted(df['Propulsão'].dropna().unique().tolist()),
            'categorias': sorted(df['Categoria'].dropna().unique().tolist()),
        }
        return jsonify({'sucesso': True, 'filtros': filtros}), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/carros', methods=['POST'])
def buscar_carros():
    try:
        filtros = request.get_json() or {}
        resultado = df.copy()
        
        if 'marca' in filtros and filtros['marca']:
            resultado = resultado[resultado['Marca'] == filtros['marca']]
        
        if 'modelo' in filtros and filtros['modelo']:
            resultado = resultado[resultado['Modelo'] == filtros['modelo']]
        
        if 'combustivel' in filtros and filtros['combustivel']:
            resultado = resultado[resultado['Combustível'] == filtros['combustivel']]
        
        if 'propulsao' in filtros and filtros['propulsao']:
            resultado = resultado[resultado['Propulsão'] == filtros['propulsao']]
        
        if 'categoria' in filtros and filtros['categoria']:
            resultado = resultado[resultado['Categoria'] == filtros['categoria']]
        
        velocidade = filtros.get('velocidade', 50)  
        if velocidade:
            resultado['consumo_calculado'] = resultado.apply(
                lambda row: funcao_quadratica(velocidade), axis=1
            )
            resultado['derivada_consumo'] = resultado.apply(
                lambda row: derivada_funcao_quadratica(velocidade), axis=1
            )
        
        carros = resultado.to_dict('records')
        
        return jsonify({
            'sucesso': True,
            'total': len(carros),
            'carros': carros
        }), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/carros/recomendacao', methods=['POST'])
def recomendacao():
    try:
        dados = request.get_json() or {}
        prioridade = dados.get('prioridade', 'economia')
        velocidade = dados.get('velocidade', 50)
        filtros = dados.get('filtros', {})
          
        resultado = df.copy()
        if 'marca' in filtros:
            resultado = resultado[resultado['Marca'] == filtros['marca']]
        if 'combustivel' in filtros:
            resultado = resultado[resultado['Combustível'] == filtros['combustivel']]
        
        resultado['consumo_calculado'] = resultado.apply(
            lambda row: funcao_quadratica(velocidade), axis=1
        )
        
        
        if prioridade == 'economia':
            
            resultado = resultado.sort_values('consumo_calculado')
        elif prioridade == 'emissoes':
            
            resultado = resultado.sort_values('Emissões Gasolina/Diesel (CO2 g/km)', na_position='last')
        
        top_5 = resultado.head(5).to_dict('records')
        
        return jsonify({
            'sucesso': True,
            'prioridade': prioridade,
            'recomendacoes': top_5
        }), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/funcao_quadratica', methods=['POST'])
def api_funcao_quadratica():

    try:
        dados = request.get_json() or {}
        velocidade = dados.get('velocidade', 50)
        a = dados.get('a', 0.45)
        b = dados.get('b', 6.39)
        c = dados.get('c', 20.54)
        
        consumo = funcao_quadratica(velocidade, a, b, c)
        derivada = derivada_funcao_quadratica(velocidade, a, b)
        
        return jsonify({
            'sucesso': True,
            'velocidade': velocidade,
            'consumo': consumo,
            'derivada': derivada,
            'parametros': {'a': a, 'b': b, 'c': c}
        }), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/carros/comparacao', methods=['POST'])
def comparacao_carros():
    try:
        dados = request.get_json() or {}
        ids = dados.get('ids', [])
        velocidade = dados.get('velocidade', 50)
        
        if not ids or len(ids) == 0:
            return jsonify({'sucesso': False, 'erro': 'Nenhum carro selecionado'}), 400
        
        if len(ids) > 4:
            return jsonify({'sucesso': False, 'erro': 'Máximo 4 carros para comparação'}), 400
        
        carros_comparacao = []
        for car_id in ids:
            carro = df[df['id'] == car_id]
            if not carro.empty:
                carro_dict = carro.iloc[0].to_dict()
            
                carro_dict['consumo_calculado'] = funcao_quadratica(velocidade)
                carro_dict['derivada_consumo'] = derivada_funcao_quadratica(velocidade)
                carros_comparacao.append(carro_dict)
        
        if not carros_comparacao:
            return jsonify({'sucesso': False, 'erro': 'Carros não encontrados'}), 404
        
        return jsonify({
            'sucesso': True,
            'total_carros': len(carros_comparacao),
            'velocidade': velocidade,
            'carros': carros_comparacao
        }), 200
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500



@app.errorhandler(404)
def not_found(error):
    return jsonify({'sucesso': False, 'erro': 'Rota não encontrada'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'sucesso': False, 'erro': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
