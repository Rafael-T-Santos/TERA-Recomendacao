import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder

df_ped = pd.read_csv(r'datasets/base_01012022_31032022.csv')
df_ped = df_ped[['CD_PEDIDO', 'CD_MATERIAL']]
df_ped = pd.crosstab(df_ped.CD_PEDIDO, df_ped.CD_MATERIAL)
df_ped[df_ped>1] = 1




qt_transact = 50
min_support = qt_transact / len(df_ped.index)

frequent_itemsets_fpgrowth_ped = fpgrowth(df_ped, min_support=min_support, use_colnames=True)

rules_fpgrowth_ped = association_rules(frequent_itemsets_fpgrowth_ped, metric = "lift", min_threshold = 1.01)
rules_fpgrowth_ped["antecedents_length"] = rules_fpgrowth_ped["antecedents"].apply(lambda x: len(x))
rules_fpgrowth_ped["consequents_length"] = rules_fpgrowth_ped["consequents"].apply(lambda x: len(x))
rules_fpgrowth_ped = rules_fpgrowth_ped[(rules_fpgrowth_ped["antecedents_length"] == 1)]

cols = ['antecedents','consequents']
rules_fpgrowth_ped[cols] = rules_fpgrowth_ped[cols].applymap(lambda x: str(x))

rules_fpgrowth_ped.to_csv(r'regras/rules_fpgrowth_ped.csv', index = False)

print('Tudo certo!') 



