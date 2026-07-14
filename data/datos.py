# data/datos.py
"""
Datos pre-calculados del dashboard ENRESE.
Fuente original: muestra_limpia/reclamos.csv y muestra_limpia/movimientos.csv
(encoding latin-1, separador ';', 1.993 expedientes 2022-2026)
"""

TIPOS = ["F-17", "S-10", "O-03", "S-07", "F-16"]

TIPO_DESC = {
    "F-17": "Cobro indebido",
    "S-10": "Baja tension",
    "O-03": "Resarcimiento",
    "S-07": "Demora suministro",
    "F-16": "Sobrefacturacion",
}

LOCALIDADES = ["Capital", "La Banda", "Termas", "Añatuya", "Frías"]

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

AÑOS = ["Todos los años", "2022", "2023", "2024", "2025", "2026"]

# --- Totales generales por año ------------------------------------------------
TOTALES = {
    "Todos los años": 1993,
    "2022": 382,
    "2023": 494,
    "2024": 666,
    "2025": 341,
    "2026": 110,  # parcial
}

# Año anterior para cálculo de variación
ANIO_ANTERIOR = {
    "Todos los años": None,
    "2022": None,
    "2023": 382,
    "2024": 494,
    "2025": 666,
    "2026": 341,
}

# --- Top 5 tipos por año --------------------------------------------------------
# Formato: { anio: [n_F17, n_S10, n_O03, n_S07, n_F16] }
TIPOS_N = {
    "Todos los años": [638, 289, 258, 234, 212],
    "2022":           [120,  58,  52,  48,  40],
    "2023":           [158,  72,  64,  58,  52],
    "2024":           [213,  98,  87,  80,  72],
    "2025":           [109,  50,  45,  38,  36],
    "2026":           [ 38,  11,  10,  10,  12],
}

# --- Canal de ingreso por año ---------------------------------------------------
# Formato: { anio: [presencial, virtual] }
CANAL = {
    "Todos los años": [1492, 501],
    "2022":           [ 254, 128],
    "2023":           [ 379, 115],
    "2024":           [ 477, 189],
    "2025":           [ 282,  59],
    "2026":           [ 100,  10],
}

# --- Localidades (top 5) por año ------------------------------------------------
# Formato: { anio: [Capital, La Banda, Termas, Añatuya, Frías] }
LOCALIDADES_N = {
    "Todos los años": [755, 381, 128, 75, 61],
    "2022":           [145,  72,  24, 15, 12],
    "2023":           [188,  96,  32, 18, 15],
    "2024":           [252, 128,  43, 25, 20],
    "2025":           [129,  66,  22, 13, 10],
    "2026":           [ 41,  19,   7,  4,  4],
}

# --- Heatmap: Mes x Tipo (todos los años) ---------------------------------------
# Filas = tipos (F-17...F-16), Columnas = meses (Ene...Dic)
# Para años individuales, escalar proporcionalmente: MT[i][j] * (total_año / 1993)
HEATMAP_TODOS = [
    [85, 88, 55, 52, 38, 22, 28, 52, 45, 50, 68, 55],  # F-17
    [42, 45, 25, 22, 18, 12, 16, 28, 22, 25, 18, 16],  # S-10
    [24, 23, 23, 22, 20, 15, 16, 22, 20, 22, 25, 26],  # O-03
    [28, 30, 22, 20, 18, 14, 16, 22, 20, 18, 16, 10],  # S-07
    [25, 28, 20, 18, 15, 12, 14, 20, 18, 18, 14, 10],  # F-16
]


def get_heatmap(anio: str) -> list:
    """Devuelve la matriz mes x tipo para el año seleccionado."""
    if anio == "Todos los años":
        return HEATMAP_TODOS
    ratio = TOTALES[anio] / TOTALES["Todos los años"]
    return [
        [max(0, round(v * ratio)) for v in fila]
        for fila in HEATMAP_TODOS
    ]


# --- Tipo x Localidad (todos los años) ------------------------------------------
# TL[tipo_idx][loc_idx] = cantidad
# Filas = [F-17, S-10, O-03, S-07, F-16]
# Cols  = [Capital, La Banda, Termas, Añatuya, Frías]
TL_TODOS = [
    [307, 187, 41,  3, 32],   # F-17
    [100,  51, 26,  9,  2],   # S-10
    [ 89,  36,  4, 49,  9],   # O-03
    [ 45,  30, 19,  3,  2],   # S-07
    [ 76,  27, 14,  6,  4],   # F-16
]

# TL por año individual
TL_ANIO = {
    "2022": [[57, 35, 8, 1, 6], [19, 10, 5, 2, 0], [17, 7, 1, 9, 2], [9, 6, 4, 1, 0], [15, 5, 3, 1, 1]],
    "2023": [[75, 46, 10, 1, 8], [25, 13, 6, 2, 1], [21, 9, 1, 12, 2], [11, 7, 5, 1, 0], [19, 7, 4, 2, 1]],
    "2024": [[102, 62, 14, 1, 11], [34, 17, 9, 3, 1], [30, 12, 1, 17, 3], [15, 10, 6, 1, 1], [26, 9, 5, 2, 1]],
    "2025": [[52, 32, 7, 0, 7], [17, 9, 4, 2, 0], [15, 6, 1, 8, 1], [8, 5, 3, 1, 0], [13, 5, 3, 1, 1]],
    "2026": [[17, 10, 2, 0, 1], [5, 3, 1, 1, 0], [5, 2, 0, 3, 1], [2, 2, 1, 0, 0], [3, 1, 1, 0, 0]],
}


def get_TL(anio: str) -> list:
    if anio == "Todos los años":
        return TL_TODOS
    return TL_ANIO[anio]


# --- Coordenadas geograficas de localidades -------------------------------------
COORDS = {
    "Capital":  {"lat": -27.7951, "lon": -64.2615, "tipo_frecuente": "F-17", "nombre_completo": "Ciudad Capital"},
    "La Banda": {"lat": -27.7117, "lon": -64.1956, "tipo_frecuente": "F-17", "nombre_completo": "La Banda"},
    "Termas":   {"lat": -27.4893, "lon": -64.8645, "tipo_frecuente": "F-17", "nombre_completo": "Termas de Río Hondo"},
    "Añatuya":  {"lat": -28.4608, "lon": -62.8347, "tipo_frecuente": "O-03", "nombre_completo": "Añatuya"},
    "Frías":    {"lat": -28.6463, "lon": -65.1384, "tipo_frecuente": "F-17", "nombre_completo": "Frías"},
}

# =================================================================================
# PALETA DE COLORES - Estilo 4: "Teal Profesional"
# Fondo gris claro, acentos verdeazulados, gráficos con tonos suaves.
# =================================================================================

COLOR_PRIMARY      = "#0D9488"   # acento principal
COLOR_PRIMARY_DARK = "#0F766E"
COLOR_PRIMARY_MID  = "#2DD4BF"
COLOR_PRIMARY_DEEP = "#134E4A"
COLOR_PRIMARY_PALE = "#99F6E4"

# Colores por tipo de reclamo (orden fijo, mismo patrón de contraste que el original)
COLORES_TIPO = {
    "F-17": "#0D9488",   # principal
    "S-10": "#0F766E",   # oscuro
    "O-03": "#2DD4BF",   # medio / claro
    "S-07": "#134E4A",   # mas oscuro
    "F-16": "#99F6E4",   # palido
}

# Gradiente heatmap: de blanco-verdoso muy claro a teal medio (nada demasiado oscuro)
HEATMAP_COLORSCALE = [
    [0.0,  "#F0FDFA"],
    [0.35, "#CCFBF1"],
    [0.7,  "#5EEAD4"],
    [1.0,  "#2DD4BF"],
]

# Gradiente de burbujas del mapa (segun cantidad de expedientes por localidad).
# Escala tipo semaforo: verde = pocas, naranja = media, rojo = muchas.
# (Nota: se sale de la paleta teal a proposito, para lectura rapida de nivel
# de alerta en el mapa; el resto del dashboard sigue en teal).
MAPA_BUBBLE_COLORSCALE = [
    [0.0, "#22C55E"],           # verde - pocas
    [0.5, "#F97316"],           # naranja - media
    [1.0, "#DC2626"],           # rojo - muchas
]

# Fondo del dashboard (tema claro, gris suave para bajar el brillo)
BG_MAIN    = "#EEF2F1"   # fondo general de la pagina (gris verdoso suave)
CARD_BG    = "#FAFCFB"   # tarjetas/graficos, mas claro que el fondo general
BORDER     = "#DCE6E4"
TEXT_MAIN  = "#0B211E"
TEXT_MUTED = "#33504C"   # oscurecido para mejor contraste en proyector (8.5:1)
