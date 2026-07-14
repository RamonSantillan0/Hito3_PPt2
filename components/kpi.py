# components/kpi.py
import streamlit as st


def render_kpi(anio: str, datos):
    """Renderiza la fila de KPI: total general (separado) + top 3 tipos de reclamo.

    `datos` es cualquier objeto con la interfaz de data.datos: TOTALES,
    ANIO_ANTERIOR, TIPOS, TIPO_DESC, TIPOS_N (el modulo data.datos para el
    dataset de ejemplo, o un data.procesar.DatosBundle para datos subidos).
    """
    total = datos.TOTALES[anio]
    prev = datos.ANIO_ANTERIOR[anio]
    tipos_n = datos.TIPOS_N[anio]
    tipos = datos.TIPOS
    tipo_desc = datos.TIPO_DESC

    delta_str = None
    if prev:
        pct = round((total - prev) / prev * 100)
        delta_str = f"{pct:+d}% vs año anterior"

    # Dos grupos claramente separados: el total general (1 columna, con acento)
    # y el Top 3 de tipos de reclamo (3 columnas agrupadas bajo su propia etiqueta).
    col_total, col_top3 = st.columns([1, 3], gap="medium")

    with col_total:
        with st.container(key="kpi_total"):
            st.markdown('<div class="section-title">General</div>', unsafe_allow_html=True)
            st.metric(
                label="Total expedientes",
                value=f"{total:,}".replace(",", "."),
                delta=delta_str,
            )

    with col_top3:
        with st.container(key="kpi_top3"):
            st.markdown('<div class="section-title">Top 3 tipos de reclamo</div>', unsafe_allow_html=True)
            cols = st.columns(min(3, len(tipos)))
            for i, col in enumerate(cols):
                n = tipos_n[i]
                pct = round(n / total * 100) if total else 0
                with col:
                    st.metric(
                        label=tipo_desc.get(tipos[i], tipos[i]),
                        value=f"{tipos[i]}  —  {n:,}".replace(",", "."),
                        delta=f"{pct}% del total",
                        delta_color="off",
                    )

    st.markdown("")  # separador visual
