
import streamlit as st

from cargador import mostrar_cargador
from motoniveladora import mostrar_motoniveladora
from estilos import aplicar_estilos


# ==================================================
# CONFIGURACION DE LA PAGINA
# ==================================================

st.set_page_config(
    page_title="Productividad de equipo pesado",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

aplicar_estilos()


# ==================================================
# ENCABEZADO
# ==================================================

st.html("""
<div class="encabezado">
    
    <h1>Productividad de equipo pesado</h1>
    <p>
        Herramienta de cálculo, selección y análisis
        del rendimiento de maquinaria pesada.
    </p>
</div>
""")


# ==================================================
# SELECCION DEL EQUIPO
# ==================================================

if "equipo_seleccionado" not in st.session_state:
    st.session_state.equipo_seleccionado = None


def seleccionar_equipo(equipo):
    st.session_state.equipo_seleccionado = equipo


st.subheader("Seleccione el equipo")

st.caption(
    "Seleccione la maquinaria que desea evaluar."
)

col1, col2 = st.columns(2)


# ==================================================
# TARJETA DEL CARGADOR FRONTAL
# ==================================================

with col1:

    clase = "tarjeta-equipo"

    if st.session_state.equipo_seleccionado == "Cargador frontal":
        clase += " tarjeta-activa"

    st.html(f"""
    <div class="{clase}">
        <div class="numero-modulo">
            MÓDULO 01
        </div>
        <div class="icono-equipo">
            🚜
        </div>
        <h3>Cargador frontal</h3>
        <p>
            Cálculo de productividad, capacidad
            de cucharón y selección de equipos.
        </p>
    </div>
    """)

    st.button(
        "Seleccionar cargador frontal",
        key="seleccionar_cargador",
        type="primary",
        use_container_width=True,
        on_click=seleccionar_equipo,
        args=("Cargador frontal",)
    )


# ==================================================
# TARJETA DE LA MOTONIVELADORA
# ==================================================

with col2:

    clase = "tarjeta-equipo"

    if st.session_state.equipo_seleccionado == "Motoniveladora":
        clase += " tarjeta-activa"

    st.html(f"""
    <div class="{clase}">
        <div class="numero-modulo">
            MÓDULO 02
        </div>
        <div class="icono-equipo">
            ⚙️
        </div>
        <h3>Motoniveladora</h3>
        <p>
            Cálculo de productividad, tiempo de trabajo,
            fuerza de tracción y fuerza descendente.
        </p>
    </div>
    """)

    st.button(
        "Seleccionar motoniveladora",
        key="seleccionar_motoniveladora",
        type="primary",
        use_container_width=True,
        on_click=seleccionar_equipo,
        args=("Motoniveladora",)
    )


# ==================================================
# MODULOS DE CALCULO
# ==================================================

st.divider()

equipo = st.session_state.equipo_seleccionado

if equipo == "Cargador frontal":

    st.caption("MÓDULO 01 / CARGADOR FRONTAL")

    mostrar_cargador()

elif equipo == "Motoniveladora":

    st.caption("MÓDULO 02 / MOTONIVELADORA")

    mostrar_motoniveladora()

else:

    st.info(
        "Seleccione uno de los equipos para comenzar "
        "con los cálculos."
    )


# ==================================================
# PIE DE PAGINA
# ==================================================

st.divider()

st.html("""
<div class="pie-pagina">
    Software de productividad de equipo pesado
    <br>
    Basado en el Manual de Rendimiento Caterpillar
    - Edición 42
    <br>
    Proyecto académico | TECSUP
    <br>
    Gestión y Mantenimiento de Maquinaria Pesada
</div>
""")
