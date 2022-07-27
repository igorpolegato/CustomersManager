import pandas as pd

def data(coluna=None, name="nome"):
    planilha = pd.read_excel(f"excel/{name}.xlsx")
    
    if coluna:
        sol = list(planilha[coluna])
    else:
        sol = planilha

    return sol