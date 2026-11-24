
import streamlit as st


def aplicar_estilos():

    st.markdown("""
    <style>

    /* FONDO GENERAL */

    .stApp {
        background-color: #F4F6F8;
        color: #182433;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
    }

    /* ENCABEZADO PRINCIPAL */

    .encabezado {
        background: linear-gradient(
            120deg, #182433, #30465C
        );
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 28px;
        border-bottom: 5px solid #E9B62E;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
    }

    .encabezado h1 {
        color: #FFFFFF !important;
        font-size: 32px;
        margin: 0;
        padding: 0;
    }

    .encabezado p {
        color: #CBD5E1 !important;
        font-size: 16px;
        margin-top: 10px;
        margin-bottom: 0;
    }

    .etiqueta-superior {
        color: #E9B62E;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    /* TITULOS */

    h1, h2, h3 {
        color: #182433 !important;
        font-weight: 700 !important;
    }

    /* TARJETAS DE MAQUINARIA */

    .tarjeta-equipo {
        background-color: #FFFFFF;
        border: 1px solid #DDE3EA;
        border-radius: 14px;
        padding: 24px;
        min-height: 160px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }

    .tarjeta-activa {
        border: 2px solid #E9B62E;
        background-color: #FFFCF2;
    }

    .tarjeta-equipo h3 {
        margin: 8px 0;
        font-size: 22px;
    }

    .tarjeta-equipo p {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .icono-equipo {
        font-size: 32px;
    }

    .numero-modulo {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 1.5px;
    }

    /* BOTONES */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 44px;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background-color: #E9B62E !important;
        color: #182433 !important;
        border: 1px solid #E9B62E !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #D6A31C !important;
        border-color: #D6A31C !important;
        color: #182433 !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #182433 !important;
        border: 1px solid #CBD5E1 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #E9B62E !important;
        background-color: #FFFCF2 !important;
    }

    /* CAMPOS DE ENTRADA */

    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"] input {
        color: #182433 !important;
    }

    div[data-testid="stWidgetLabel"] p {
        font-weight: 600;
        color: #334155;
    }

    /* TARJETAS DE RESULTADOS */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DDE3EA;
        border-left: 5px solid #E9B62E;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricValue"] {
        color: #182433;
        font-weight: 700;
        font-size: 27px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
    }

    /* DESARROLLO MATEMATICO */

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    /* TABLAS */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* SEPARADORES */

    hr {
        border-color: #DDE3EA !important;
        margin-top: 30px !important;
        margin-bottom: 25px !important;
    }

    /* PIE DE PAGINA */

    .pie-pagina {
        text-align: center;
        color: #8491A3;
        font-size: 12px;
        padding: 20px 0;
        line-height: 1.8;
    }

    /* ADAPTACION A CELULARES */

    @media (max-width: 640px) {

        .encabezado {
            padding: 22px;
        }

        .encabezado h1 {
            font-size: 25px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 23px;
        }

    }

    /* CORRECCION DE CONTRASTE */

    /* Etiquetas de los formularios */

    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        color: #182433 !important;
        font-weight: 600 !important;
    }

    /* Menus desplegables */

    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #182433 !important;
        border-color: #CBD5E1 !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="select"] svg {
        color: #182433 !important;
    }

    /* Encabezados desplegables */

    [data-testid="stExpander"] summary {
        background-color: #E8EDF2 !important;
        color: #182433 !important;
        border-radius: 8px;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary svg {
        color: #182433 !important;
        font-weight: 600 !important;
    }

    /* Etiquetas de casillas y opciones */

    [data-testid="stCheckbox"] p,
    [data-testid="stRadio"] p {
        color: #182433 !important;
    }

    /* FONDO SUAVE Y CONFORT VISUAL */

    /* FONDO SUAVE Y CONFORT VISUAL */

    .stApp {
        background-color: #B8C4CF !important;
    }

    .tarjeta-equipo,
    div[data-testid="stMetric"],
    div[data-testid="stExpander"] {
        background-color: #D1DAE2 !important;
    }

    .tarjeta-activa {
        background-color: #DCD5BF !important;
        border-color: #D9AC38 !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
        background-color: #D1DAE2 !important;
        border-color: #94A4B4 !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #A7B6C4 !important;
        color: #182433 !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: #D1DAE2 !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #D9AC38 !important;
        border-color: #D9AC38 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #C69A2E !important;
        border-color: #C69A2E !important;
    }

    .pie-pagina {
        color: #475569 !important;
    }

    hr {
        border-color: #94A4B4 !important;
    }

    /* ALINEACION DE TARJETAS */

    .tarjeta-equipo {
        box-sizing: border-box;
        height: 240px;
        display: flex;
        flex-direction: column;
    }

    @media (max-width: 640px) {
        .tarjeta-equipo {
            height: auto;
            min-height: 220px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
