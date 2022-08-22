from os import close
import pyodbc
import pandas as pd
import openpyxl
import unidecode
import csv
import warnings

#ignore by message
warnings.filterwarnings("ignore", category=UserWarning)

with open(r'_config\config.csv', 'r') as arquivo_csv:
    leitor = csv.DictReader(arquivo_csv, delimiter=';')
    for coluna in leitor:
        server = coluna['server']
        database = coluna['database']
        username = coluna['username']
        password = coluna['password']

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()
df = pd.DataFrame()

def consulta_questor():
    consulta = """
    SELECT
    T1.CD_PEDIDO,
    T2.CD_CLIENTE,
    T4.DS_CIDADE,
    T4.DS_UF,
    T1.CD_ITEM, 
    T1.CD_MATERIAL, 
    T1.DS_MATERIAL, 
    (CASE WHEN T5.DT_CADASTRO IS NULL THEN T2.DT_CADASTRO ELSE T5.DT_CADASTRO END) AS DT_CADASTRO,
    T2.DT_ATUALIZACAO, 
    T1.DS_UNIDADE, 
    T1.NR_QUANTIDADE, 
    T1.VL_UNITARIO, 
    T1.VL_TOTAL, 
    T1.CD_VENDEDOR
        FROM TBL_PEDIDOS_ITENS T1
            INNER JOIN TBL_PEDIDOS T2
            ON T1.CD_PEDIDO = T2.CD_PEDIDO
                INNER JOIN TBL_ENTIDADES T3
                ON T2.CD_CLIENTE = T3.CD_ENTIDADE
					INNER JOIN TBL_ENDERECO_CIDADES T4
					ON T3.CD_CIDADE = T4.CD_CIDADE
						LEFT JOIN TBL_ORCAMENTOS T5
						ON T5.CD_ORCAMENTO = T2.CD_ORCAMENTO
									WHERE T2.CD_FILIAL = 3
										AND T2.CD_STATUS = 4
											AND T2.DT_CADASTRO BETWEEN CONVERT(datetime, '2022-01-01T00:00:00.000') 
											AND CONVERT(datetime, '2022-03-31T00:00:00.000');
											
    """

    df = pd.read_sql_query(consulta, cnxn)
    #print(df.to_string(index=False))
    df.to_csv(r'datasets\base_01012022_31032022.csv', index = False)

def consulta_estoque(cd_material):
    consulta = f"""
    SELECT
    T1.CD_MATERIAL, 
    T1.DS_MATERIAL, 
    T2.NR_ESTOQUE_DISPONIVEL 
        FROM TBL_MATERIAIS T1
            INNER JOIN TBL_MATERIAIS_ESTOQUE T2
            ON T1.CD_MATERIAL = T2.CD_MATERIAL
            WHERE T2.CD_FILIAL = 3
                AND T1.CD_MATERIAL = {cd_material};
    """

    df_estoque = pd.read_sql_query(consulta, cnxn)
    return df_estoque

def consulta_ncm():
    consulta = """
    SELECT CD_MATERIAL, 
    CD_NCM 
        FROM TBL_MATERIAIS
            ORDER BY CD_MATERIAL;"""

    df = pd.read_sql_query(consulta, cnxn)
    df.to_csv(r'datasets\base_ncm.csv', index = False)


#consulta_questor()
#consulta_ncm()

