# components/barras.py
import streamlit as st
import plotly.graph_objects as go
from data.datos import COLORES_TIPO, CARD_BG, TEXT_MAIN, TEXT_MUTED, BORDER


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def render_barras(anio: str, datos):
    """Renderiza barras agrupadas apiladas: localidad x tipo x canal de ingreso.

    `datos` expone TIPOS, TIPO_DESC, LOCALIDADES, CANAL y get_TL(anio)
    (data.datos para el dataset de ejemplo, o un data.procesar.DatosBundle
    para datos subidos). Los 5 colores de COLORES_TIPO se aplican por
    posicion, no por codigo, asi funcionan igual con tipos reales distintos.
    """
    tipos = datos.TIPOS
    tipo_desc = datos.TIPO_DESC
    localidades = datos.LOCALIDADES

    canal = datos.CANAL[anio]
    total_canal = canal[0] + canal[1]
    p_ratio = canal[0] / total_canal if total_canal else 0  # fraccion presencial
    TL = datos.get_TL(anio)

    fig = go.Figure()
    colores = list(COLORES_TIPO.values())

    for i, tipo in enumerate(tipos):
        n_loc = len(localidades)
        datos_pres = [round(TL[i][j] * p_ratio) for j in range(n_loc)]
        datos_virt = [TL[i][j] - datos_pres[j] for j in range(n_loc)]
        color = colores[i % len(colores)]

        # Barra presencial (color solido)
        fig.add_trace(go.Bar(
            name=f"{tipo} - {tipo_desc.get(tipo, tipo)}",
            x=localidades,
            y=datos_pres,
            offsetgroup="presencial",
            legendgroup=tipo,
            marker_color=color,
            hovertemplate=f"<b>{tipo} Presencial</b><br>%{{x}}: %{{y}} exp.<extra></extra>",
        ))

        # Barra virtual (mismo color, mas transparente + borde para que se
        # distinga bien sobre el fondo claro)
        fig.add_trace(go.Bar(
            name=f"{tipo} - {tipo_desc.get(tipo, tipo)}",
            x=localidades,
            y=datos_virt,
            offsetgroup="virtual",
            legendgroup=tipo,
            marker=dict(
                color=hex_to_rgba(color, 0.5),
                line=dict(color=color, width=1),
            ),
            showlegend=False,
            hovertemplate=f"<b>{tipo} Virtual</b><br>%{{x}}: %{{y}} exp.<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        title=dict(
            text="LOCALIDAD × TIPO DE RECLAMO × CANAL DE INGRESO",
            font=dict(size=12, color=TEXT_MUTED),
            x=0,
        ),
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        font=dict(color=TEXT_MAIN),
        height=320,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            font=dict(size=11),
        ),
        yaxis=dict(
            title="Expedientes",
            gridcolor="rgba(11,33,30,0.10)",
        ),
        xaxis=dict(
            gridcolor="rgba(11,33,30,0.10)",
        ),
        margin=dict(l=60, r=20, t=80, b=40),
        annotations=[dict(
            text="Barra izquierda = <b>Presencial</b> (color solido)  ·  Barra derecha = <b>Virtual</b> (mismo color, mas claro)",
            x=0, y=1.13, xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=10, color=TEXT_MUTED),
            bgcolor=CARD_BG,
            bordercolor=BORDER,
            borderwidth=1,
        )],
    )

    st.plotly_chart(fig, width='stretch')
