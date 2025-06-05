import pandas as pd
import numpy as np
import joblib
from datetime import datetime
'''
O modelo precisa das seguintes informações pra rodar:
- data_pas: Data e hora da previsão (formato datetime, ex: '2024-01-02 04:08:00')
- numero_dias_sem_chuva: Número de dias sem chuva (opcional, 1 modelo pra cada situação) (inteiro)
- latitude: Latitude do local (float)
- longitude: Longitude do local (float)
- estado: Estado do local (string, por exemplo: 'PERNAMBUCO', 'RIO DE JANEIRO', etc.)

tipos de retorno:
-0: risco baixo
-1: risco alto
'''


# Funções auxiliares para pré-processamento
def faixa_dias_sem_chuva(dias):
    if dias <= 10:
        return '0-10'
    elif dias <= 20:
        return '11-20'
    elif dias <= 30:
        return '21-30'
    else:
        return '30+'

def periodo_do_dia(hora):
    if 5 <= hora < 12:
        return 'manha'
    elif 12 <= hora < 17:
        return 'tarde'
    elif 17 <= hora < 21:
        return 'noite'
    else:
        return 'madrugada'

def preprocessar_com_dias_sem_chuva(df: pd.DataFrame) -> pd.DataFrame:
    df_preditivo = df.copy()
    df_preditivo['mes'] = df_preditivo['data_pas'].dt.month
    df_preditivo['dia'] = df_preditivo['data_pas'].dt.day
    df_preditivo['hora'] = df_preditivo['data_pas'].dt.hour
    df_preditivo['dia_semana'] = df_preditivo['data_pas'].dt.dayofweek
    df_preditivo = df_preditivo.drop(columns=['data_pas'])
    df_preditivo['faixa_dias_sem_chuva'] = df_preditivo['numero_dias_sem_chuva'].apply(faixa_dias_sem_chuva)
    df_preditivo['periodo_dia'] = df_preditivo['hora'].apply(periodo_do_dia)
    return df_preditivo

def preprocessar_sem_dias_sem_chuva(df: pd.DataFrame) -> pd.DataFrame:
    df_preditivo = df.copy()
    df_preditivo['mes'] = df_preditivo['data_pas'].dt.month
    df_preditivo['dia'] = df_preditivo['data_pas'].dt.day
    df_preditivo['hora'] = df_preditivo['data_pas'].dt.hour
    df_preditivo['dia_semana'] = df_preditivo['data_pas'].dt.dayofweek
    df_preditivo = df_preditivo.drop(columns=['data_pas'])
    if 'numero_dias_sem_chuva' in df_preditivo.columns:
        df_preditivo = df_preditivo.drop(columns=['numero_dias_sem_chuva'])
    df_preditivo['periodo_dia'] = df_preditivo['hora'].apply(periodo_do_dia)
    return df_preditivo


# Função para carregar e executar o modelo modelo_com_dias_sem_chuva.pkl
def predizer_com_dias_sem_chuva(dados: pd.DataFrame):
    modelo = joblib.load('./sentinela/ia/modelo_com_dias_sem_chuva.pkl')
    dados_proc = preprocessar_com_dias_sem_chuva(dados)
    pred = modelo.predict(dados_proc)
    return pred

# Função para carregar e executar o modelo modelo_sem_dias_sem_chuva.pkl
def predizer_sem_dias_sem_chuva(dados: pd.DataFrame):
    modelo = joblib.load('./sentinela/ia/modelo_sem_dias_sem_chuva.pkl')
    dados_proc = preprocessar_sem_dias_sem_chuva(dados)
    pred = modelo.predict(dados_proc)
    return pred

# Exemplo de uso:
# df_exemplo = pd.DataFrame({...})
# resultado = predizer_com_dias_sem_chuva(df_exemplo)
# resultado2 = predizer_sem_dias_sem_chuva(df_exemplo)

df_exemplo = pd.DataFrame({
    'data_pas': [pd.Timestamp(datetime(2025, 11, 28, 14))],
    'numero_dias_sem_chuva': [25],
    'latitude': [-11.5],
    'longitude': [-56.2],
    'estado': ['PERNAMBUCO'],
})