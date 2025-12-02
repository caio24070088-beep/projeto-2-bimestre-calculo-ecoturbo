# PROJETO 2º BIMESTRE: ecoTURBO.com

Alunos: Caio Nicolas Neves Rodrigues, Arthur Aviz Lima, CC4MA
Matéria: Resolução Diferencial de Problemas

## Descrição
Esse é um sistema fullstack em Python que tem o objetivo de analisar os carros avaliados pelo INMETRO em 2025 e filtrar os melhores carros nos quesitos economia e energia limpa de acordo com a preferência do usuário. O sistema é interativo e pode ser acessado via web.

## Requisitos
- Python 3.8 ou superior
- Flask
- Flask-CORS
- pandas
- Navegador web moderno (Chrome, Firefox, Edge, etc.)

## Tutorial de Instalação e Execução
1. **Clone o repositório ou copie os arquivos para seu computador.**
2. **Instale as dependências:**
	Abra o terminal na pasta do projeto e execute:
	```bash
	pip install flask flask-cors pandas
	```
3. **Execute o servidor Flask:**
	```bash
	python app.py
	```
4. **Acesse o sistema:**
	Abra o navegador e acesse [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Exemplos de Uso
- Filtrar carros por marca, modelo, combustível, propulsão e velocidade.
- Visualizar o catálogo completo de veículos.
- Comparar dois ou mais carros lado a lado.

## Estrutura do Projeto
```
projeto-2-bimestre-calculo/
│
├── app.py                        # Backend Flask (API e servidor)
├── calculos.py                   # Funções de cálculo e manipulação de dados
├── index.html                    # Interface web (frontend)
├── tabela_inmetro_carros_2025.csv # Base de dados dos carros (CSV)
├── README.md                     # Este arquivo
└── ...
```

## Estrutura do Banco/Arquivos
- **tabela_inmetro_carros_2025.csv**: Arquivo CSV contendo os dados dos veículos (marca, modelo, consumo, combustível, propulsão, etc.).
- **calculos.py**: Funções para cálculos matemáticos e manipulação do DataFrame.
- **app.py**: API Flask que serve os dados e a interface web.
- **index.html**: Página web interativa para o usuário.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

