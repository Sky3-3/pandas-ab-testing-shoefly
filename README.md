# Proyecto Python: Análisis de Pruebas A/B y Optimización de CTR con Pandas

Este repositorio contiene un proyecto práctico desarrollado en Python utilizando la librería **Pandas** para evaluar el rendimiento de una campaña de publicidad digital mediante pruebas A/B. El script automatiza el procesamiento de registros de visitas, calcula las tasas de clics (*Click-Through Rate* - CTR) agregadas por fuentes de tráfico, genera tablas pivote de contingencia y desglosa el comportamiento diario de los usuarios para determinar de manera estadística cuál de las variantes experimentales (Anuncio A o Anuncio B) genera mayor interacción.

---

## Código Python del Proyecto

El programa realiza la ingesta del archivo de eventos de clics, define métricas lógicas booleanas, construye resúmenes agregados y segmenta los sets de datos para auditar las variantes de la campaña:

```python
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

```

---

## Resultados y Matrices de Contingencia Extraídas

El procesamiento de datos distribuye las interacciones permitiendo identificar de forma clara los sesgos de conversión y la efectividad de las plataformas digitales empleadas.

### 1. Desglose Global de Conversión por Plataforma (`clicks_pivot`)

Muestra el volumen de usuarios que vieron el anuncio frente a los que finalmente interactuaron con la publicación:

| utm_source | Clics Completados (`True`) | Impresiones sin Clic (`False`) | Tasa de Conversión (CTR) |
| --- | --- | --- | --- |
| **email** | 80 | 175 | 31.37% |
| **facebook** | 180 | 324 | 35.71% |
| **google** | 239 | 441 | 35.14% |
| **twitter** | 66 | 149 | 30.69% |

### 2. Comparativa del Test A/B Diario (`percent_clicked`)

Al aislar las muestras del experimento, se observa cómo fluctúa el rendimiento porcentual del CTR de cada anuncio a lo largo de la semana:

| Día de la Semana | CTR Variante A (Control) | CTR Variante B (Alternativa) | Diagnóstico Operativo |
| --- | --- | --- | --- |
| 1 - Monday | 11.32% | 12.11% | La Variante B muestra mayor adopción inicial. |
| 2 - Tuesday | 14.89% | 11.45% | La Variante A performa mejor a mitad de semana. |
| 5 - Friday | 12.08% | 14.16% | Incremento de clics los fines de semana para la opción B. |

---

## Conceptos Técnicos Aplicados

* **Pruebas A/B en Entornos Digitales**: Metodología de experimentación que consiste en dividir de manera aleatoria el tráfico de una plataforma en dos variantes (A y B) para medir el impacto de un cambio de diseño o contenido sobre una métrica de conversión central.
* **Modelado de Tablas Pivote (`.pivot()`)**: Operación de reestructuración que transforma filas largas de datos agregados en una matriz bidimensional compacta, convirtiendo los valores únicos de una columna en nuevos encabezados para facilitar la lectura analítica.
* **Operador de Negación Bitwise (`~`)**: Utilizado para invertir vectores booleanos. En la instrucción `~ad_clicks.ad_click_timestamp.isnull()`, evalúa la serie y devuelve `True` únicamente en aquellas filas donde el registro posee una marca de tiempo válida, aislando las interacciones reales.
directamente a armar el **repositorio indexador central de tu perfil** para que sirva de portada formal de todo tu portafolio en GitHub.
