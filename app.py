import streamlit as st
import data.datos as datos_demo
from data.procesar import DatosBundle, leer_archivo, sugerir_columna
from components.kpi import render_kpi
from components.heatmap import render_heatmap
from components.barras import render_barras
from components.mapa import render_mapa

st.set_page_config(
    page_title="ENRESE · Sistema de Reclamos",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS global - Estilo 4: Teal Profesional (fondo gris claro)
# Nota: los colores de texto secundario se oscurecieron a proposito (contraste
# ~8:1 sobre fondo claro) porque el dashboard se proyecta y los grises claros
# quedaban poco legibles en pantalla grande / con luz ambiente.
st.markdown("""<style>
.main { background-color: #EEF2F1; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }
div[data-testid="metric-container"] {
    background: #FAFCFB;
    border: 0.5px solid #DCE6E4;
    border-radius: 8px;
    padding: 0.75rem 1rem;
}
div[data-testid="metric-container"] label { color: #33504C !important; font-size: 14px !important; font-weight: 600; }
div[data-testid="metric-container"] div[data-testid="stMetricValue"] { color: #0B211E; font-size: 22px; }
div[data-testid="stMetricDelta"] { color: #33504C !important; }
h1, h2, h3 { color: #0B211E; }
.section-title {
    font-size: 14px; font-weight: 700; color: #33504C;
    text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.5rem;
}

/* Captions de Streamlit (st.caption): por defecto usan un gris claro que
   se lava bajo proyector, se oscurecen para que sean legibles */
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
    color: #33504C !important;
}

/* KPI: distinguir el total general (1 tarjeta, acentuada) del Top 3 de
   tipos de reclamo (grupo de 3 tarjetas), para que no se lean como 4
   indicadores equivalentes. */
.st-key-kpi_total {
    padding-right: 1.25rem;
    border-right: 1px solid #DCE6E4;
}
.st-key-kpi_total div[data-testid="metric-container"] {
    border-left: 3px solid #0D9488;
    background: #E6F5F3;
}
.st-key-kpi_top3 div[data-testid="metric-container"] {
    background: #FAFCFB;
}

/* Barra superior nativa de Streamlit (donde estan "Deploy" y el menu "...") */
header[data-testid="stHeader"] {
    background: #EEF2F1;
    border-bottom: 1px solid #DCE6E4;
}

/* Selector de año "incrustado" en esa barra fija: como Streamlit no permite
   insertar widgets dentro de su propio toolbar, el truco es renderizar el
   selectbox en un contenedor con key propio y reposicionarlo con
   position:fixed para que quede alineado con la franja del header nativo,
   a la izquierda de los botones Deploy / menu. */
.st-key-year_toolbar {
    position: fixed;
    top: 0;
    left: 1rem;
    height: 2.875rem;
    display: flex;
    align-items: center;
    z-index: 1000001;
}
.st-key-year_toolbar div[data-testid="stSelectbox"] { width: 190px; }
.st-key-year_toolbar div[data-testid="stSelectbox"] label { display: none; }
.st-key-year_toolbar div[data-baseweb="select"] {
    background: #FAFCFB;
    border-radius: 6px;
}
.st-key-year_toolbar div[data-baseweb="select"] * { color: #0B211E !important; }

/* Deja lugar en el contenido para que el titulo no quede pegado al header */
.block-container { padding-top: 1.2rem; }
</style>""", unsafe_allow_html=True)


def formatear_anio(a: str, es_demo: bool) -> str:
    # El año 2026 del dataset de ejemplo es parcial: siempre aclarar en el
    # selector. Para datos propios no se asume nada sobre si el ultimo año
    # esta completo o no.
    if es_demo and a == "2026":
        return f"{a} (parcial)"
    return a


# -- Header de contenido -------------------------------------------------------
st.markdown("## ENRESE `PROTOTIPO HITO 3`")

# -- Fuente de datos: dataset propio, justo debajo del nombre del proyecto -----
# El dashboard arranca vacio (sin datos de ejemplo precargados) para poder
# probar el flujo de carga real; los datos de ejemplo quedan como opcion
# explicita ("Ver con datos de ejemplo") en vez de ser lo que se ve por
# defecto.
with st.expander(
    "📂 Cargar dataset propio (reclamos.csv)",
    expanded="datos_bundle" not in st.session_state,
):
    st.caption(
        "Subí el archivo .zip de muestra_limpia tal cual (se busca reclamos.csv "
        "adentro) o el reclamos.csv suelto — separador ';', UTF-8 o latin-1, se "
        "detecta solo."
    )
    archivo = st.file_uploader("Archivo CSV o .zip", type=["csv", "zip"], key="uploader_reclamos")

    if archivo is not None:
        try:
            df_subido = leer_archivo(archivo)
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
            df_subido = None

        if df_subido is not None and df_subido.shape[1] >= 2:
            columnas = list(df_subido.columns)
            st.write(f"Se detectaron {len(df_subido):,} filas y {len(columnas)} columnas.".replace(",", "."))

            col1, col2 = st.columns(2)
            with col1:
                col_tipo = st.selectbox(
                    "Columna de tipo de reclamo", columnas,
                    index=columnas.index(sugerir_columna(columnas, ["cod_reclamo", "tipo", "cod_tipo", "reclamo"])),
                )
                col_fecha = st.selectbox(
                    "Columna de fecha", columnas,
                    index=columnas.index(sugerir_columna(columnas, ["fecha", "date", "alta"])),
                )
            with col2:
                col_localidad = st.selectbox(
                    "Columna de localidad", columnas,
                    index=columnas.index(sugerir_columna(columnas, ["localidad", "ciudad", "partido"])),
                )
                col_canal = st.selectbox(
                    "Columna de canal / empleado que recibe", columnas,
                    index=columnas.index(sugerir_columna(columnas, ["empl_recibe", "canal", "empleado"])),
                )

            if st.button("Generar gráficos con este archivo", type="primary"):
                try:
                    bundle = DatosBundle(df_subido, col_tipo, col_localidad, col_fecha, col_canal)
                    st.session_state["datos_bundle"] = bundle
                    st.session_state.pop("usar_demo", None)
                    total_ok = bundle.TOTALES["Todos los años"]
                    st.success(
                        f"Listo: {total_ok:,} expedientes procesados "
                        f"({bundle.filas_sin_fecha} filas sin fecha válida se excluyeron)."
                        .replace(",", ".")
                    )
                except Exception as e:
                    st.error(f"No se pudo procesar el archivo con esas columnas: {e}")
        elif df_subido is not None:
            st.error("El archivo no parece tener columnas separadas correctamente (revisá el separador).")

    col_demo, col_vaciar = st.columns(2)
    with col_demo:
        if "datos_bundle" not in st.session_state and not st.session_state.get("usar_demo"):
            if st.button("Ver con datos de ejemplo"):
                st.session_state["usar_demo"] = True
                st.rerun()
    with col_vaciar:
        if "datos_bundle" in st.session_state or st.session_state.get("usar_demo"):
            if st.button("↩ Vaciar dashboard"):
                st.session_state.pop("datos_bundle", None)
                st.session_state.pop("usar_demo", None)
                st.rerun()

usando_datos_propios = "datos_bundle" in st.session_state
usando_demo = st.session_state.get("usar_demo", False)

if usando_datos_propios:
    datos_activo = st.session_state["datos_bundle"]
elif usando_demo:
    datos_activo = datos_demo
else:
    datos_activo = None

if datos_activo is None:
    st.caption("Sistema de gestión de reclamos · sin datos cargados")
    st.divider()
    st.info(
        "El dashboard está vacío. Subí un dataset arriba (.zip o .csv) o "
        "usá el botón \"Ver con datos de ejemplo\" para ver los gráficos."
    )
else:
    # -- Selector de año, fijo en la barra superior (junto a Deploy / menu) -----
    with st.container(key="year_toolbar"):
        anio = st.selectbox(
            "Año", datos_activo.AÑOS, index=0,
            format_func=lambda a: formatear_anio(a, usando_demo),
            label_visibility="collapsed",
        )

    if usando_datos_propios:
        st.caption(
            f"Sistema de gestión de reclamos · dataset propio cargado "
            f"({datos_activo.TOTALES['Todos los años']:,} expedientes)".replace(",", ".")
        )
    else:
        st.caption("Sistema de gestión de reclamos · 2022–2026 (datos de ejemplo)")
    st.divider()

    # -- KPI Row ------------------------------------------------------------------
    render_kpi(anio, datos_activo)

    # -- Heatmap --------------------------------------------------------------------
    render_heatmap(anio, datos_activo)

    # -- Barras agrupadas apiladas ---------------------------------------------------
    render_barras(anio, datos_activo)

    # -- Mapa -------------------------------------------------------------------------
    render_mapa(anio, datos_activo)
