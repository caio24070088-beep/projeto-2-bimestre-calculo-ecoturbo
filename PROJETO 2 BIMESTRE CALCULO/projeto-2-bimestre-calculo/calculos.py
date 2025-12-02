import pandas as pd
import numpy as np
from nbformat import read
from pathlib import Path

def load_variable_from_notebook(notebook_path, var_name='df', run_all=False):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = read(f, as_version=4)

    kernel = {}
    for cell in nb.cells:
        if cell.cell_type == 'code':
            try:
                exec(cell.source, kernel)
            except Exception as e:
                print(f"Aviso: erro ao executar célula: {e}")

    return kernel.get(var_name, None)


def funcao_quadratica(v, a=0.45, b=6.39, c=20.54):
    return a * v**2 - b * v + c


def derivada_funcao_quadratica(v, a=0.45, b=6.39):
    """Retorna a derivada da função quadrática: C'(v) = 2av - b"""
    return 2 * a * v - b


if __name__ == '__main__':
    df = pd.read_csv('tabela_inmetro_carros_2025.csv', sep=';', encoding='Latin-1', decimal=',')
    
    if df is not None:
        print(f"DataFrame carregado com sucesso: {df.shape}")
        print(df.head())
    else:
        print("Erro: DataFrame não foi encontrado")
    
    print("\n--- Aplicação da Função Quadrática ---")
    velocidades = [30, 50, 70, 90, 100]
    
    for v in velocidades:
        consumo = funcao_quadratica(v)
        derivada = derivada_funcao_quadratica(v)
        print(f"Velocidade: {v} km/h → Consumo: {consumo:.4f} L/km | Derivada: {derivada:.4f}")
