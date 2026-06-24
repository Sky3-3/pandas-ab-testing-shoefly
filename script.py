import pandas as pd

# --- 1. Ingesta y Exploración de Datos ---
ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head())

# Conteo de visitas totales agrupadas por plataforma de origen
as_clicks_visit = ad_clicks.groupby("utm_source").user_id.count().reset_index()

# --- 2. Análisis de Rendimiento de Clics (CTR) Global ---
# Creación de una columna booleana que detecta si el usuario hizo clic (marca de tiempo no nula)
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

# Agrupación y conteo por fuente de tráfico y estado del clic
click_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

# Construcción de una tabla pivote para reestructurar la matriz de contingencia
clicks_pivot = click_by_source.pivot(
    columns='is_click',
    index='utm_source',
    values='user_id'
).reset_index()

# Cálculo porcentual del CTR por plataforma
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])
print(clicks_pivot)

# --- 3. Segmentación del Experimento (Pruebas A/B) ---
# Verificación del tamaño muestral asignado a cada grupo del test
print(ad_clicks.groupby("experimental_group").user_id.count().reset_index())

# División del DataFrame principal en sub-datasets independientes por variante
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# --- 4. Auditoría Cronológica Diaria ---
# Análisis del comportamiento de conversión para el Anuncio A
a_clicks_by_day = a_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()
a_clicks_pivot = a_clicks_by_day.pivot(index='day', columns='is_click', values='user_id').reset_index()
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])

# Análisis del comportamiento de conversión para el Anuncio B
b_clicks_by_day = b_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()
b_clicks_pivot = b_clicks_by_day.pivot(index='day', columns='is_click', values='user_id').reset_index()
b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])

# Impresión formal de las matrices de conversión diarias
print("Métricas Diarias - Variante A:")
print(a_clicks_pivot)
print("\nMétricas Diarias - Variante B:")
print(b_clicks_pivot)
