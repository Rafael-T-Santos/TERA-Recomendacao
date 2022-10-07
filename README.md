# Algoritmo de Recomendação para a Venda de Materiais de Construção

Projeto final do curso de Data Science e Machine Learning ofertado pela TERA

[Artigo do Projeto](https://carolruckert.medium.com/algoritmo-de-recomenda%C3%A7%C3%A3o-para-a-venda-de-materiais-de-constru%C3%A7%C3%A3o-94b5737728ca)

# Resumo

O projeto conta com um algoritmo de recomendação de vendas, nesse caso optamos pelo FPGROWTH, o mesmo cria um conjunto de dados de itens frequentes e partir disso um conjunto de regras de associação, fazendo com que tenhamos uma recomendação um para um.

# API

Dentro da pasta API temos o arquivo consultas_questor.py o mesmo é responsavel pela conexão ao banco de dados da empresa e pela consulta dos dados que iremos utilizar, fazendo com que os mesmos sejam exportados em arquivos csv, arquivos esses constantes na pasta datasets.

Ainda dentro da pasta API temos o arquivo controller.py esse arquivo é o responsável por efetivamente rodar o algoritmo de recomendação com base em todos os suportes e metricas que definimos lá no inicio em nosso notebook Projeto_principal.ipynb. Mesmo que o algoritmo utilizado seja muito melhor comparado ao anterior(Apriori) ainda tivemos um tempo de de execução de cerca de 40 segundos, com isso decidimos criar o conjunto de regras previamente a sua utilização.

Nossa API em si está presente no arquivo main.py, ela lê o conjunto de regras criado anteriormente e prepara a recomendação de venda com base na solicitação do usuário, o usuário informa o item o qual necessita de uma recomendação e a API retorna o algoritmo utilizado, suporte, metrica, e dados dos itens tanto o antecedente como consequente, nossa API ainda tem um segundo nível, caso não exista regra que satisfaça as metricas utilizadas criamos uma condição em que nosso sistema de recomendação verifica o NCM do item, e procura recomendações com base nesse NCM, visto que esse código categoriza os itens.

# Interface

Na pasta interface podemos verificar o arquivo interface.py, foi criada uma interface windows utilizando a biblioteca PySide6 onde foi tomado o cuidado de selecionar uma área que não afete o uso do ERP e também botoes e cores iguais ao mesmo, com isso conseguimos criar uma interface que se assemelha a um modulo do proprio ERP, fazendo com que não seja causado estranhamento pelo usuário, nossa interface é responsável pelo request na API.
