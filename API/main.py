#uvicorn main:api

import pandas as pd
import sys
import math
from fastapi import FastAPI

import consultas_questor as c 

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

rules_fpgrowth = pd.read_csv(r'regras/rules_fpgrowth_ped.csv')
rules_fpgrowth['antecedents'] = rules_fpgrowth['antecedents'].str.replace("""frozenset""", "", regex=True).str.replace("(", "", regex=True).str.replace("{", "", regex=True).str.replace("}", "", regex=True).str.replace(")", "")
rules_fpgrowth['consequents'] = rules_fpgrowth['consequents'].str.replace("""frozenset""", "", regex=True).str.replace("(", "", regex=True).str.replace("{", "", regex=True).str.replace("}", "", regex=True).str.replace(")", "")
rules_ncm = pd.read_csv(r'regras/rules_ncm.csv')

api = FastAPI()

@api.get("/")
def root_get():
    return "Hello World"

@api.get('/favicon.ico', include_in_schema=False)

@api.post("/{item}")
def post_item(item: int):
    ds_item_base = ''
    est_item_base = 0
    status_ncm = 0
    item_rec = ''
    ds_item_rec = ''
    est_item_rec = ''
    
    if item == int:
        pass
    else:
        resultado = rules_fpgrowth[rules_fpgrowth['antecedents'] == item]
        if resultado.empty == True:
            item_estoque = c.consulta_estoque(item)
            if item_estoque.empty == True:
                ds_item_base = 'Item não encontrado na base de dados. Digite novamente.'
            else:
                ds_item_base = (str(item_estoque.iloc[0]['DS_MATERIAL']))
                est_item_base = (str(item_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))
                cd_ncm = rules_ncm['CD_NCM'][rules_ncm['CD_MATERIAL'] == int(item)]

                if cd_ncm.empty == True:
                    status_ncm = 'Não existem vendas suficientes para recomendacao.'
                else:
                    pass

                grupo_materiais = list(rules_ncm['CD_MATERIAL'][rules_ncm['CD_NCM'] == int(cd_ncm)])
            
                if len(grupo_materiais) > 1:
                    lista_support = []
                    for i in range(len(grupo_materiais)):
                        resultado = rules_fpgrowth[rules_fpgrowth['antecedents'] == str(grupo_materiais[i])]
                        lista_support.append(resultado['confidence'].max())
                    
                    for i in range(len(lista_support)):
                        if math.isnan(lista_support[i]):
                            lista_support[i] = 0
                        else:
                            pass
                    
                    maior = max(lista_support)
                    if maior == 0:
                        ds_item_rec = 'Não existem vendas suficientes para recomendacao.'
                    else:
                        index = lista_support.index(maior)
                        resultado_antecedent = grupo_materiais[index]
                        resultado = rules_fpgrowth[rules_fpgrowth['antecedents'] == str(resultado_antecedent)]
                        df_estoque = c.consulta_estoque(resultado.iloc[0]['consequents'])

                        item_rec = (str(df_estoque.iloc[0]['CD_MATERIAL']))
                        ds_item_rec = (str(df_estoque.iloc[0]['DS_MATERIAL']))
                        est_item_rec = (str(df_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))
                else:
                    resultado = rules_fpgrowth[rules_fpgrowth['antecedents'] == str(grupo_materiais)]
                    df_estoque = c.consulta_estoque(resultado.iloc[0]['consequents'])

                    item_rec = (str(df_estoque.iloc[0]['CD_MATERIAL']))
                    ds_item_rec = (str(df_estoque.iloc[0]['DS_MATERIAL']))
                    est_item_rec = (str(df_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))
        else:            
            if len(resultado) > 1:
                item_estoque = c.consulta_estoque(item)
                ds_item_base = (str(item_estoque.iloc[0]['DS_MATERIAL']))
                est_item_base = (str(item_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))

                confidence = resultado['confidence'].max()
                resultado = resultado[(resultado['confidence'] == confidence)]
                df_estoque = c.consulta_estoque(resultado.iloc[0]['consequents'])
                item_rec = (str(df_estoque.iloc[0]['CD_MATERIAL']))
                ds_item_rec = (str(df_estoque.iloc[0]['DS_MATERIAL']))
                est_item_rec = (str(df_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))
            else:
                item_estoque = c.consulta_estoque(item)
                ds_item_base = (str(item_estoque.iloc[0]['DS_MATERIAL']))
                est_item_base (str(item_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))

                df_estoque = c.consulta_estoque(resultado.iloc[0]['consequents'])
                item_rec = (str(df_estoque.iloc[0]['CD_MATERIAL']))
                ds_item_rec = (str(df_estoque.iloc[0]['DS_MATERIAL']))
                est_item_rec = (str(df_estoque.iloc[0]['NR_ESTOQUE_DISPONIVEL']))


    return {
            "algoritmo": "fpgrowth",
            "min_support": "50/len(df.index) =  0.0004625774817281895",
            "metrica": "lift >= 1",
            "message": f"Item selecionado {item}",
            "ds_item_base": ds_item_base,
            "est_item_base": est_item_base,
            "status_ncm": status_ncm,
            "item_rec": item_rec,
            "ds_item_rec": ds_item_rec,
            "est_item_rec": est_item_rec
            }
