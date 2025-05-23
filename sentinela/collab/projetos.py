# -*- coding: utf-8 -*-
"""projetos.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ictS_C5Ak1l5yXrypdQy4ezYuIXLE7y1
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv('dados_filtrados_caatinga.csv')
df.head()

"""# Limpeza dos dados"""

df['numero_dias_sem_chuva'] = df['numero_dias_sem_chuva'].astype('uint8')
df['precipitacao'] = df['precipitacao'].astype('float32')
df['risco_fogo'] = df['risco_fogo'].astype('float32')
df['frp'] = df['frp'].astype('float32')
df.info()

colunas_categoricas = ['estado', 'municipio', 'satelite']

for col in colunas_categoricas:
    df[col] = df[col].astype('category')

df['data_pas'] = pd.to_datetime(df['data_pas'], errors='coerce')

df.info(memory_usage='deep')

df.head(5)

"""# Gráficos iniciais"""

colunas_numericas = ['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']

fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for i, col in enumerate(colunas_numericas):
    sns.histplot(data=df, x=col, bins=50, kde=True, color='skyblue', ax=axes[i])
    axes[i].set_title(f'{col}', fontsize=13)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 4, figsize=(15, 3))
for i, col in enumerate(colunas_numericas):
    sns.boxplot(data=df, x=col, ax=axes[i], color='lightblue')
    axes[i].set_title(f'{col}', fontsize=13)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('')

plt.tight_layout()
plt.show()

prec_por_estado = df.groupby('estado', observed=True)['precipitacao'].mean().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(x=prec_por_estado.values, y=prec_por_estado.index)
plt.title('Média de precipitação por estado', fontsize=14)
plt.xlabel('Precipitação média (mm)')
plt.ylabel('Estado')
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 5))
sns.heatmap(df.corr(numeric_only=True).round(3), annot=True, cmap='coolwarm')

df['ano_mes'] = df['data_pas'].dt.to_period('M')

prec_por_tempo = df.groupby('ano_mes')['risco_fogo'].mean()

plt.figure(figsize=(14, 5))
prec_por_tempo.plot(kind='line', marker='o')
plt.title('risco_fogo médio ao longo do tempo')
plt.xlabel('Ano e mês')
plt.ylabel('Precipitação média (mm)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

import folium
from folium.plugins import HeatMap

df_filtrado_mapa = df[df['risco_fogo'] == 1.0][['latitude', 'longitude', 'risco_fogo']].dropna()

# Amostragem para evitar sobrecarga
df_sample_mapa = df_filtrado_mapa.sample(n=8000, random_state=42)

# Criar o mapa centralizado na Caatinga
mapa = folium.Map(location=[-9.5, -40.5], zoom_start=5)

# Adicionar HeatMap
heat_data = [[row['latitude'], row['longitude'], row['risco_fogo']] for index, row in df_sample_mapa.iterrows()]
HeatMap(heat_data, radius=10).add_to(mapa)

mapa

"""# Análise Multivariada
## Dias sem chuva X Risco fogo
"""

plt.figure(figsize=(8,6))
plt.hexbin(df['numero_dias_sem_chuva'], df['risco_fogo'], gridsize=50, cmap='Blues', bins='log')
plt.colorbar(label='log(Número de pontos)')
plt.title('Densidade: Número de Dias sem Chuva vs Risco de Fogo')
plt.xlabel('Número de Dias sem Chuva')
plt.ylabel('Risco de Fogo')
plt.grid(True)
plt.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Assuming 'colunas_numericas' from your previous code contains the numerical features
variaveis_numericas = df[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']]

# Padronizar os dados (importante para K-Means)
scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(variaveis_numericas)

# Encontrar o número ideal de clusters usando o método do cotovelo
inertia = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(dados_padronizados)
    inertia.append(kmeans.inertia_)

# Plotar a curva do método do cotovelo
plt.figure(figsize=(8,6))
plt.plot(k_range, inertia, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo para Definição de k')
plt.grid()
plt.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

# 1. Selecionar as variáveis numéricas
variaveis_numericas = df[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']]

# 2. Padronizar os dados
scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(variaveis_numericas)

# 3. Definir o número de clusters (por exemplo, 5 com base no método do cotovelo)
kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
kmeans.fit(dados_padronizados)

# 4. Adicionar os rótulos de cluster ao DataFrame original
df['cluster'] = kmeans.labels_

# 5. Analisar a média das variáveis dentro de cada cluster
analise_clusters = df.groupby('cluster')[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']].mean()

print("Médias das variáveis em cada cluster:")
print(analise_clusters)

# 6. (Opcional) Visualizar a distribuição dos clusters
plt.figure(figsize=(8,6))
plt.scatter(df['numero_dias_sem_chuva'], df['risco_fogo'], c=df['cluster'], cmap='viridis')
plt.xlabel('Número de dias sem chuva')
plt.ylabel('Risco de Fogo')
plt.title('Distribuição dos Clusters')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# prompt: gere um código que pega os clusters gerados na celula anterior e faz uma analise de cada regiao presente nos clusters, plote um grafico

import matplotlib.pyplot as plt
import seaborn as sns

# Análise das regiões em cada cluster
plt.figure(figsize=(10, 6))
sns.countplot(x='cluster', hue='estado', data=df)
plt.title('Distribuição de Estados por Cluster')
plt.xlabel('Cluster')
plt.ylabel('Contagem de Estados')
plt.show()

# Estatísticas descritivas para cada cluster e região
for cluster in df['cluster'].unique():
  print(f"\nCluster {cluster}:")
  cluster_data = df[df['cluster'] == cluster]
  for estado in cluster_data['estado'].unique():
    estado_data = cluster_data[cluster_data['estado'] == estado]
    print(f"  Estado: {estado}")
    print(estado_data[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']].describe())

# Plotar um gráfico de barras para cada variável numérica em cada cluster
for column in ['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='cluster', y=column, data=df)
    plt.title(f'Média de {column} por Cluster')
    plt.xlabel('Cluster')
    plt.ylabel(column)
    plt.show()

# prompt: em relação ao grafico anterior e a analise de clusters, foi notavel que o 2 representa o menor numeor de casos, assim prejudicando a analise, por favor rescreva a analise desconsiderando o cluster 2

# Analisar a média das variáveis dentro de cada cluster, desconsiderando o cluster 2
analise_clusters = df[df['cluster'] != 2].groupby('cluster')[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']].mean()

print("Médias das variáveis em cada cluster (excluindo o cluster 2):")
print(analise_clusters)

# (Opcional) Visualizar a distribuição dos clusters, desconsiderando o cluster 2
plt.figure(figsize=(8,6))
plt.scatter(df[df['cluster'] != 2]['numero_dias_sem_chuva'], df[df['cluster'] != 2]['risco_fogo'], c=df[df['cluster'] != 2]['cluster'], cmap='viridis')
plt.xlabel('Número de dias sem chuva')
plt.ylabel('Risco de Fogo')
plt.title('Distribuição dos Clusters (excluindo o cluster 2)')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# Análise das regiões em cada cluster (excluindo o cluster 2)
plt.figure(figsize=(10, 6))
sns.countplot(x='cluster', hue='estado', data=df[df['cluster'] != 2])
plt.title('Distribuição de Estados por Cluster (excluindo o cluster 2)')
plt.xlabel('Cluster')
plt.ylabel('Contagem de Estados')
plt.show()

# Estatísticas descritivas para cada cluster e região (excluindo o cluster 2)
for cluster in df[df['cluster'] != 2]['cluster'].unique():
  print(f"\nCluster {cluster}:")
  cluster_data = df[(df['cluster'] == cluster)]
  for estado in cluster_data['estado'].unique():
    estado_data = cluster_data[cluster_data['estado'] == estado]
    print(f"  Estado: {estado}")
    print(estado_data[['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']].describe())

# Plotar um gráfico de barras para cada variável numérica em cada cluster (excluindo o cluster 2)
for column in ['numero_dias_sem_chuva', 'precipitacao', 'risco_fogo', 'frp']:
    plt.figure(figsize=(10, 6))
    sns.barplot(x='cluster', y=column, data=df[df['cluster'] != 2])
    plt.title(f'Média de {column} por Cluster (excluindo o cluster 2)')
    plt.xlabel('Cluster')
    plt.ylabel(column)
    plt.show()

"""# Modelo preditivo

### Tratando os dados pro modelo
"""

df_preditivo = df.copy()
df_preditivo = df_preditivo.drop(columns=['municipio', 'cluster'])

df_preditivo.info()

df_preditivo['mes'] = df_preditivo['data_pas'].dt.month
df_preditivo['dia'] = df_preditivo['data_pas'].dt.day
df_preditivo['hora'] = df_preditivo['data_pas'].dt.hour
df_preditivo['dia_semana'] = df_preditivo['data_pas'].dt.dayofweek

df_preditivo = df_preditivo.drop(columns=['data_pas', 'ano_mes'])

df_preditivo.head()

df_preditivo = pd.get_dummies(df_preditivo, columns=['satelite', 'estado'], drop_first=True)
df_preditivo.columns

"""### divisao de treino/teste"""

from sklearn.model_selection import train_test_split

X = df_preditivo.drop(columns=['risco_fogo'])

# Variável alvo: risco_fogo
y = df_preditivo['risco_fogo']

# Dividindo os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

"""### Começando e avaliando o modelo"""

from sklearn.ensemble import RandomForestRegressor

# Instanciando o modelo com os melhores parâmetros
model_rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

# Treinando o modelo
model_rf.fit(X_train, y_train)

# Fazendo previsões
y_pred = model_rf.predict(X_test)

from sklearn.metrics import mean_squared_error, r2_score
print('Teste:')
print(f"MSE: {mean_squared_error(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"R²: {r2_score(y_test, y_pred):.4f}")
print('-'*30)
print('Treinamento:')
print(f"MSE: {mean_squared_error(y_train, model_rf.predict(X_train)):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_train, model_rf.predict(X_train))):.4f}")
print(f"R²: {r2_score(y_train, model_rf.predict(X_train)):.4f}")

import pandas as pd
import matplotlib.pyplot as plt

# Obtendo a importância das features
importances = model_rf.feature_importances_

# Criando um DataFrame para visualizar a importância
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importances
})

# Ordenando as features pela importância
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Imprimindo as colunas mais importantes
# (Opcional) Visualizar a importância das features
plt.figure(figsize=(10, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
plt.title('Importância das Features no Modelo RandomForestRegressor')
plt.xlabel('Importância')
plt.ylabel('Feature')
plt.tight_layout()
plt.show()

"""# Exportando modelo"""

import joblib

# Salva o modelo treinado em um arquivo
joblib.dump(model_rf, 'modelo_preditivo.pkl')

"""# Avaliação Paiva

Escolher uma das e modelagens abaixo:

1. 01(um) problema de Classificação
2. 01(um) problema de Regressão Não Paramétrica
3. 01(um) problema de Série Temporal

Requisitos para modelo escolhido:

1. Realizar a EDA para escolher o objetivo da modelagem(Ex.: Qual/Quais variáveis independentes X explicam a variável dependente Y)
2. Desenho Experimental:
    3.1. Teste comparativo: 30 simulações com amostras representativas, sendo 70% da base para treino e 30% para validação. Para série temporal, 02(dois) ciclos para prever 01(um)ciclo
    3.2. Validação: aplicar o devido teste de hipótese para os resultados das métricas de performance para cada modelo comparado

## Escolhendo modelagem
"""

df_modelagem = df.copy()
df_modelagem = df_modelagem.drop(columns=['municipio', 'cluster'])

plt.figure(figsize=(8, 6))
sns.heatmap(df_modelagem.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Correlação entre variáveis")
plt.show()

sns.pairplot(df_modelagem[['numero_dias_sem_chuva', 'precipitacao', 'frp', 'risco_fogo']])
plt.suptitle("Dispersão entre variáveis", y=1.02)
plt.show()

plt.figure(figsize=(6, 4))
sns.histplot(df['risco_fogo'], bins=30, kde=True, color='red')
plt.title("Distribuição de risco_fogo")
plt.grid(True)
plt.show()

"""Categorizando classes pro modelo"""

# Ver quantos valores intermediários entre 0 e 1 existem
intermed = df[(df['risco_fogo'] > 0) & (df['risco_fogo'] < 1)]
print(f"Total de valores intermediários: {len(intermed)}")
intermed['risco_fogo'].value_counts().sort_index()

def categoriza_risco(valor):
    if valor == 0.0:
        return 'baixo'
    elif valor == 1.0:
        return 'alto'
    else:
        return 'medio'

df['risco_cat'] = df['risco_fogo'].apply(categoriza_risco)
print(df['risco_cat'].value_counts())