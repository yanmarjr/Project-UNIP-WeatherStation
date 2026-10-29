
import pandas as pd

# Functions:
def porcentagem(variavel, dado):
    average = len(variavel) / len(dado) * 100
    return average

dados = pd.read_csv("dados.csv", sep=";") # Lendo os dados do csv usando DataFrame.read_csv()

# Filtering the Data by Column
data = dados["Data"]
temperatura = dados["Temperatura"]
umidade = dados["Umidade"]
pressao = dados["Pressão"]
luminosidade = dados["Luminosidade"]
chuva = dados["Chuva"]

# Calculando a porcentagem de (dias) que choveu:
dias_de_chuva = dados.loc[chuva == 1, ["Chuva"]]
porcentagem_de_chuva = porcentagem(dias_de_chuva, dados)
print(f"Porcentagem de chuva: {porcentagem_de_chuva:.2f} % dos (dias) tiveram chuva")

# Calculando a porcentagem de luminosidade:
dias_de_luz = dados.loc[luminosidade == 1, ["Luminosidade"]]
porcentagem_de_luz = porcentagem(dias_de_luz, dados)
print(f"Porcentagem de (dias) com luz: {porcentagem_de_luz:.2f} % dos (dias) tiveram luminosidade")

# Calculando (the average) numero de pressão:
pressao_somente_valor = (pressao.str.split(" ").str[0].astype(float))
pressao_average = pressao_somente_valor.mean()
print(f"Average pressao é: {pressao_average:.2f} hPa")













