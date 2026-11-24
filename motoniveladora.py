
import streamlit as st
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

# ==================================================
# TABLAS DEL MANUAL CATERPILLAR
# ==================================================

# Página 148 - Longitud de vertedera en metros

MODELOS = {
    "12M": 3.66,
    "14M": 4.27,
    "16M": 4.88,
    "24M": 7.32
}

# Página 146 - Velocidades en km/h

VELOCIDADES = {
    "Nivelación de acabado": (0, 4),
    "Trabajo pesado con la hoja": (0, 9),
    "Reparación de zanjas": (0, 5),
    "Desgarramiento": (0, 5),
    "Mantenimiento de carreteras": (5, 16),
    "Mantenimiento de caminos de acarreo": (5, 16),
    "Movimiento de nieve": (7, 21),
    "Limpieza de nieve": (15, 28)
}

# Página 148 - Longitud efectiva en metros

LONGITUD_EFECTIVA = {
    0:  [3.66, 4.27, 4.88, 7.32],
    5:  [3.64, 4.25, 4.86, 7.29],
    10: [3.60, 4.20, 4.80, 7.21],
    15: [3.53, 4.12, 4.71, 7.07],
    20: [3.44, 4.01, 4.58, 6.87],
    25: [3.32, 3.87, 4.42, 6.63],
    30: [3.17, 3.69, 4.22, 6.33],
    35: [3.00, 3.50, 4.00, 5.99],
    40: [2.80, 3.27, 3.74, 5.61],
    45: [2.59, 3.02, 3.45, 5.17]
}

# Página 1573 - Factor de tracción de NEUMÁTICOS

TRACCION = {
    "Hormigón": 0.90,
    "Marga arcillosa seca": 0.55,
    "Marga arcillosa mojada": 0.45,
    "Marga arcillosa con surcos": 0.40,
    "Arena seca": 0.20,
    "Arena mojada": 0.40,
    "Canteras": 0.65,
    "Camino de grava (suelta, no dura)": 0.36,
    "Nieve compacta": 0.20,
    "Hielo": 0.12,
    "Tierra firme": 0.55,
    "Tierra suelta": 0.45,
    "Carbón amontonado": 0.45
}


# ==================================================
# FUNCIONES AUXILIARES
# ==================================================

def decimal(valor):
    return Decimal(str(valor))


def redondear(valor):
    return decimal(valor).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def entero_superior(valor):
    return int(
        decimal(valor).to_integral_value(
            rounding=ROUND_CEILING
        )
    )


def numero(valor):
    return f"{valor:,.2f}"


def limpiar():
    for clave in list(st.session_state.keys()):
        if clave.startswith("mn_"):
            del st.session_state[clave]


def guardar_resultado(actividad, datos, resultado):

    st.session_state[f"mn_resultado_{actividad}"] = {
        "datos": datos,
        "resultado": resultado
    }


def recuperar_resultado(actividad, datos):

    clave = f"mn_resultado_{actividad}"

    registro = st.session_state.get(clave)

    if registro is None:
        return None

    if registro["datos"] != datos:
        st.session_state.pop(clave, None)
        return None

    return registro["resultado"]


# ==================================================
# MÓDULO PRINCIPAL DE MOTONIVELADORA
# ==================================================

def mostrar_motoniveladora():

    st.header("Motoniveladora")

    st.write(
        "Cálculo de productividad, tiempo de trabajo, "
        "fuerza de tracción y fuerza descendente de la hoja."
    )

    st.caption(
        "Cada actividad cuenta con su propio botón "
        "de resolución independiente."
    )

    st.button(
        "Limpiar todos los datos",
        key="mn_limpiar",
        on_click=limpiar
    )

    resumen = []

    # ==============================================
    # ACTIVIDAD 1 - PRODUCTIVIDAD
    # ==============================================

    st.divider()

    st.subheader("Actividad 1 — Productividad")

    modelo = st.selectbox(
        "Modelo de motoniveladora",
        list(MODELOS.keys()),
        key="mn_modelo"
    )

    origen_ih = st.radio(
        "Obtención de Ih",
        [
            "Automático — Manual, pág. 148",
            "Ingreso manual"
        ],
        key="mn_origen_ih"
    )

    if origen_ih == "Ingreso manual":

        ih = st.number_input(
            "Longitud de vertedera — Ih (m)",
            min_value=0.0,
            value=None,
            format="%.3f",
            key="mn_ih"
        )

    else:

        ih = MODELOS[modelo]

        st.info(
            f"Longitud de vertedera Ih = {ih:.2f} m"
        )

    trabajo = st.selectbox(
        "Tipo de trabajo — Manual, pág. 146",
        list(VELOCIDADES.keys()),
        key="mn_trabajo"
    )

    velocidad_min, velocidad_max = VELOCIDADES[trabajo]

    S = decimal(velocidad_max)

    st.caption(
        f"Intervalo: {velocidad_min}–{velocidad_max} km/h. "
        f"Velocidad seleccionada: {S} km/h."
    )

    angulo = st.selectbox(
        "Ángulo de vertedera — Manual, pág. 148",
        list(LONGITUD_EFECTIVA.keys()),
        format_func=lambda x: f"{x}°",
        key="mn_angulo"
    )

    longitudes = list(MODELOS.values())

    if ih is None:

        le = None

    elif ih in longitudes:

        posicion = longitudes.index(ih)

        le = LONGITUD_EFECTIVA[angulo][posicion]

        st.info(
            f"Longitud efectiva Le = {le:.2f} m"
        )

    else:

        st.warning(
            "La longitud ingresada no aparece en la tabla. "
            "Ingrese Le manualmente."
        )

        le = st.number_input(
            "Longitud efectiva — Le (m)",
            min_value=0.0,
            value=None,
            format="%.3f",
            key="mn_le"
        )

    col1, col2 = st.columns(2)

    with col1:

        lo = st.number_input(
            "Ancho recomendado — Lo (m)",
            min_value=0.0,
            value=None,
            format="%.3f",
            key="mn_lo"
        )

    with col2:

        eficiencia = st.number_input(
            "Eficiencia — E (%)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            key="mn_eficiencia"
        )

        if eficiencia is not None:

            st.caption(
                f"Factor E = {eficiencia / 100:g}"
            )

    material = st.selectbox(
        "Material — Manual, pág. 1573",
        ["Sin especificar"]
        + list(TRACCION.keys())
        + ["Otro material"],
        key="mn_material"
    )

    if material == "Otro material":

        nombre_material = st.text_input(
            "Nombre del material",
            key="mn_nombre_material"
        )

        T = st.number_input(
            "Factor de tracción de neumáticos",
            min_value=0.0,
            value=None,
            format="%.3f",
            key="mn_factor_manual"
        )

    elif material == "Sin especificar":

        nombre_material = ""
        T = None

    else:

        nombre_material = material
        T = TRACCION[material]

        st.caption(
            f"Factor de tracción de neumáticos: {T:.2f}"
        )

    st.caption(
        "El material es opcional para la actividad 1. "
        "Solamente es necesario para la actividad 3."
    )

    datos1 = (
        modelo,
        ih,
        trabajo,
        angulo,
        le,
        lo,
        eficiencia
    )

    resultado1 = recuperar_resultado(1, datos1)

    # BOTÓN INDEPENDIENTE DE ACTIVIDAD 1

    if st.button(
        "Resolver actividad 1",
        type="primary",
        use_container_width=True,
        key="mn_resolver_1"
    ):

        errores = []

        if ih is None or ih <= 0:
            errores.append("Ingrese una longitud Ih válida.")

        if le is None or le <= 0:
            errores.append("Ingrese una longitud Le válida.")

        if ih is not None and le is not None:
            if le > ih:
                errores.append("Le no puede ser mayor que Ih.")

        if lo is None:
            errores.append("Ingrese el ancho recomendado Lo.")

        elif le is not None and lo >= le:
            errores.append("Lo debe ser menor que Le.")

        if eficiencia is None or eficiencia <= 0:
            errores.append("Ingrese una eficiencia válida.")

        if errores:

            for error in errores:
                st.error(error)

        else:

            E = decimal(eficiencia) / 100

            ancho_efectivo = redondear(
                decimal(le) - decimal(lo)
            )

            A = redondear(
                S * ancho_efectivo * 1000 * E
            )

            if A <= 0:

                st.error(
                    "La productividad debe ser mayor que cero."
                )

            else:

                resultado1 = {
                    "A": A,
                    "E": E,
                    "ancho_efectivo": ancho_efectivo
                }

                guardar_resultado(
                    1, datos1, resultado1
                )

    A = None

    # RESULTADOS DE ACTIVIDAD 1

    if resultado1 is not None:

        A = resultado1["A"]
        E = resultado1["E"]
        ancho_efectivo = resultado1["ancho_efectivo"]

        st.metric(
            "Productividad de la motoniveladora",
            f"{numero(A)} m²/h"
        )

        with st.expander(
            "Desarrollo matemático — Actividad 1",
            expanded=True
        ):

            st.markdown("**1. Velocidad de operación**")

            st.write(
                f"Tipo de trabajo: {trabajo}."
            )

            st.write(
                f"Intervalo: {velocidad_min}–"
                f"{velocidad_max} km/h."
            )

            st.latex(rf"S={S}\;km/h")

            st.markdown(
                "**2. Longitud efectiva de vertedera**"
            )

            st.write(
                f"Ih = {ih:g} m. Ángulo = {angulo}°."
            )

            st.latex(rf"Le={le:g}\;m")

            st.markdown("**3. Factor de eficiencia**")

            st.latex(
                rf"E=\frac{{{eficiencia:g}}}{{100}}={E}"
            )

            st.markdown("**4. Productividad**")

            st.latex(
                r"A=S\times(Le-Lo)\times1000\times E"
            )

            st.latex(
                rf"A={S}\times({le:g}-{lo:g})"
                rf"\times1000\times{E}"
            )

            st.latex(
                rf"A={S}\times{ancho_efectivo}"
                rf"\times1000\times{E}"
            )

            st.latex(
                rf"A={numero(A)}\;m^2/h"
            )

        st.success(
            f"Respuesta: La productividad de la "
            f"motoniveladora es de {numero(A)} m²/h."
        )

        resumen.append({
            "Actividad": 1,
            "Variable": "A",
            "Descripción": "Productividad",
            "Resultado": numero(A),
            "Unidad": "m²/h"
        })

    # ==============================================
    # ACTIVIDAD 2 - TIEMPO DE TRABAJO
    # ==============================================

    st.divider()

    st.subheader("Actividad 2 — Tiempo de trabajo")

    if A is not None:

        st.info(
            f"Productividad recuperada de la actividad 1: "
            f"A = {numero(A)} m²/h"
        )

    else:

        st.info(
            "Resuelva primero la actividad 1 "
            "para obtener la productividad A."
        )

    at = st.number_input(
        "Ancho del terreno — aT (m)",
        min_value=0.0,
        value=None,
        key="mn_ancho"
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        distancia = st.number_input(
            "Distancia a nivelar — LT",
            min_value=0.0,
            value=None,
            format="%.3f",
            key="mn_distancia"
        )

    with col2:

        unidad = st.selectbox(
            "Unidad de distancia",
            ["m", "km"],
            key="mn_unidad"
        )

    LT = None

    if distancia is not None:

        LT = decimal(distancia)

        if unidad == "km":
            LT = LT * 1000

        st.caption(
            f"Distancia para el cálculo: {numero(LT)} m"
        )

    col1, col2 = st.columns(2)

    with col1:

        htd = st.number_input(
            "Turno de trabajo — HTD (h/día)",
            min_value=0.0,
            max_value=24.0,
            value=None,
            key="mn_turno"
        )

    with col2:

        np = st.number_input(
            "Número de pasadas — NP",
            min_value=1,
            value=None,
            step=1,
            key="mn_pasadas"
        )

    datos2 = (
        datos1,
        A,
        at,
        LT,
        unidad,
        htd,
        np
    )

    resultado2 = recuperar_resultado(2, datos2)

    # BOTÓN INDEPENDIENTE DE ACTIVIDAD 2

    if st.button(
        "Resolver actividad 2",
        type="primary",
        use_container_width=True,
        key="mn_resolver_2"
    ):

        errores = []

        if A is None:
            errores.append("Primero resuelva la actividad 1.")

        if at is None or at <= 0:
            errores.append("Ingrese el ancho del terreno.")

        if LT is None or LT <= 0:
            errores.append("Ingrese la distancia a nivelar.")

        if htd is None or htd <= 0:
            errores.append("Ingrese el turno de trabajo.")

        if np is None or np <= 0:
            errores.append("Ingrese el número de pasadas.")

        if errores:

            for error in errores:
                st.error(error)

        else:

            AT = redondear(
                decimal(at) * LT * decimal(np)
            )

            NH = redondear(AT / A)

            DT_decimal = NH / decimal(htd)

            DT = entero_superior(DT_decimal)

            resultado2 = {
                "AT": AT,
                "NH": NH,
                "DT_decimal": DT_decimal,
                "DT": DT
            }

            guardar_resultado(
                2, datos2, resultado2
            )

    # RESULTADOS DE ACTIVIDAD 2

    if resultado2 is not None:

        AT = resultado2["AT"]
        NH = resultado2["NH"]
        DT_decimal = resultado2["DT_decimal"]
        DT = resultado2["DT"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Área total",
            f"{numero(AT)} m²"
        )

        col2.metric(
            "Número de horas",
            f"{numero(NH)} h"
        )

        col3.metric(
            "Días totales",
            f"{DT} días"
        )

        with st.expander(
            "Desarrollo matemático — Actividad 2",
            expanded=True
        ):

            if unidad == "km":

                st.markdown(
                    "**Conversión de distancia**"
                )

                st.latex(
                    rf"LT={distancia:g}\times1000"
                    rf"={numero(LT)}\;m"
                )

            st.markdown(
                "**1. Área total de trabajo**"
            )

            st.latex(
                r"AT=(aT\times LT)\times NP"
            )

            st.latex(
                rf"AT=({at:g}\times{LT})\times{np}"
            )

            st.latex(
                rf"AT={numero(AT)}\;m^2"
            )

            st.markdown("**2. Número de horas**")

            st.latex(r"NH=\frac{AT}{A}")

            st.latex(
                rf"NH=\frac{{{numero(AT)}}}"
                rf"{{{numero(A)}}}"
            )

            st.latex(
                rf"NH={numero(NH)}\;h"
            )

            st.markdown("**3. Días totales**")

            st.latex(r"DT=\frac{NH}{HTD}")

            st.latex(
                rf"DT=\frac{{{numero(NH)}}}{{{htd:g}}}"
            )

            st.latex(
                rf"DT\approx"
                rf"{numero(redondear(DT_decimal))}"
                rf"\;\text{{dias}}"
            )

            st.latex(
                rf"DT={DT}\;\text{{dias}}"
            )

            st.caption(
                "El resultado se aproxima al entero superior."
            )

        st.success(
            f"Respuesta: Se requieren {DT} días de "
            "trabajo para completar la nivelación."
        )

        resumen.extend([
            {
                "Actividad": 2,
                "Variable": "AT",
                "Descripción": "Área total de trabajo",
                "Resultado": numero(AT),
                "Unidad": "m²"
            },
            {
                "Actividad": 2,
                "Variable": "NH",
                "Descripción": "Número de horas",
                "Resultado": numero(NH),
                "Unidad": "h"
            },
            {
                "Actividad": 2,
                "Variable": "DT",
                "Descripción": "Días totales",
                "Resultado": str(DT),
                "Unidad": "días"
            }
        ])

    # ==============================================
    # ACTIVIDAD 3 - FUERZA DE TRACCIÓN
    # ==============================================

    st.divider()

    st.subheader("Actividad 3 — Fuerza de tracción")

    st.info(
        f"Modelo seleccionado: {modelo}"
    )

    if T is not None and nombre_material.strip():

        col1, col2 = st.columns(2)

        col1.write(
            f"**Material:** {nombre_material}"
        )

        col2.write(
            f"**Factor de tracción T:** {T:g}"
        )

        st.caption(
            "Datos recuperados de la actividad 1. "
            "Factor de tracción de neumáticos."
        )

    else:

        st.info(
            "Seleccione el material en la actividad 1."
        )

    wr = st.number_input(
        "Masa sobre el eje trasero — Wr (kg)",
        min_value=0.0,
        value=None,
        key="mn_wr"
    )

    st.caption(
        "Ingrese el dato obtenido de la ficha "
        "técnica de la motoniveladora."
    )

    datos3 = (
        modelo,
        nombre_material,
        T,
        wr
    )

    resultado3 = recuperar_resultado(3, datos3)

    # BOTÓN INDEPENDIENTE DE ACTIVIDAD 3

    if st.button(
        "Resolver actividad 3",
        type="primary",
        use_container_width=True,
        key="mn_resolver_3"
    ):

        errores = []

        if not nombre_material.strip():
            errores.append("Seleccione o ingrese el material.")

        if T is None or T <= 0:
            errores.append(
                "Ingrese un factor de tracción válido."
            )

        if wr is None or wr <= 0:
            errores.append(
                "Ingrese la masa sobre el eje trasero."
            )

        if errores:

            for error in errores:
                st.error(error)

        else:

            TH = redondear(
                decimal(wr) * decimal(T)
            )

            resultado3 = {
                "TH": TH
            }

            guardar_resultado(
                3, datos3, resultado3
            )

    # RESULTADOS DE ACTIVIDAD 3

    if resultado3 is not None:

        TH = resultado3["TH"]

        st.metric(
            "Fuerza de tracción",
            f"{numero(TH)} kgf"
        )

        with st.expander(
            "Desarrollo matemático — Actividad 3",
            expanded=True
        ):

            st.write(
                f"Material: {nombre_material}"
            )

            st.write(
                f"Factor de tracción de neumáticos: {T:g}"
            )

            st.markdown("**1. Fórmula**")

            st.latex(r"TH=Wr\times T")

            st.markdown("**2. Sustitución**")

            st.latex(
                rf"TH={wr:g}\times{T:g}"
            )

            st.markdown("**3. Resultado**")

            st.latex(
                rf"TH={numero(TH)}\;kgf"
            )

        st.success(
            f"Respuesta: La fuerza de tracción "
            f"disponible es de {numero(TH)} kgf."
        )

        resumen.append({
            "Actividad": 3,
            "Variable": "TH",
            "Descripción": "Fuerza de tracción",
            "Resultado": numero(TH),
            "Unidad": "kgf"
        })

    # ==============================================
    # ACTIVIDAD 4 - FUERZA DESCENDENTE
    # ==============================================

    st.divider()

    st.subheader(
        "Actividad 4 — Fuerza descendente de la hoja"
    )

    st.info(
        f"Modelo seleccionado: {modelo}"
    )

    wb = st.number_input(
        "Distancia entre ejes — WB (m)",
        min_value=0.0,
        value=None,
        format="%.3f",
        key="mn_wb"
    )

    ba = st.number_input(
        "Distancia de la hoja al eje delantero — BA (m)",
        min_value=0.0,
        value=None,
        format="%.3f",
        key="mn_ba"
    )

    fw = st.number_input(
        "Peso sobre las ruedas delanteras — FW (kg)",
        min_value=0.0,
        value=None,
        key="mn_fw"
    )

    st.caption(
        "Ingrese los datos de la ficha técnica. "
        "Las distancias deben estar en metros."
    )

    datos4 = (
        modelo,
        wb,
        ba,
        fw
    )

    resultado4 = recuperar_resultado(4, datos4)

    # BOTÓN INDEPENDIENTE DE ACTIVIDAD 4

    if st.button(
        "Resolver actividad 4",
        type="primary",
        use_container_width=True,
        key="mn_resolver_4"
    ):

        errores = []

        if wb is None or wb <= 0:
            errores.append("Ingrese una distancia WB válida.")

        if ba is None:
            errores.append("Ingrese la distancia BA.")

        elif wb is not None and ba >= wb:
            errores.append("WB debe ser mayor que BA.")

        if fw is None or fw <= 0:
            errores.append(
                "Ingrese el peso sobre las ruedas delanteras."
            )

        if errores:

            for error in errores:
                st.error(error)

        else:

            diferencia = decimal(wb) - decimal(ba)

            BD = redondear(
                decimal(wb) / diferencia * decimal(fw)
            )

            resultado4 = {
                "BD": BD,
                "diferencia": diferencia
            }

            guardar_resultado(
                4, datos4, resultado4
            )

    # RESULTADOS DE ACTIVIDAD 4

    if resultado4 is not None:

        BD = resultado4["BD"]

        diferencia = resultado4["diferencia"]

        st.metric(
            "Fuerza descendente de la hoja",
            f"{numero(BD)} kgf"
        )

        with st.expander(
            "Desarrollo matemático — Actividad 4",
            expanded=True
        ):

            st.markdown("**1. Fórmula**")

            st.latex(
                r"BD=\frac{WB}{WB-BA}\times FW"
            )

            st.markdown("**2. Sustitución**")

            st.latex(
                rf"BD=\frac{{{wb:g}}}"
                rf"{{{wb:g}-{ba:g}}}\times{fw:g}"
            )

            st.markdown("**3. Resolución**")

            st.latex(
                rf"BD=\frac{{{wb:g}}}"
                rf"{{{diferencia}}}\times{fw:g}"
            )

            st.markdown("**4. Resultado**")

            st.latex(
                rf"BD={numero(BD)}\;kgf"
            )

        st.success(
            f"Respuesta: La fuerza descendente de "
            f"la hoja es de {numero(BD)} kgf."
        )

        resumen.append({
            "Actividad": 4,
            "Variable": "BD",
            "Descripción": "Fuerza descendente de la hoja",
            "Resultado": numero(BD),
            "Unidad": "kgf"
        })

    # ==============================================
    # RESUMEN GENERAL
    # ==============================================

    if resumen:

        st.divider()

        st.header("Resumen general de resultados")

        st.write(
            f"Modelo de motoniveladora: {modelo}"
        )

        st.dataframe(
            resumen,
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            "Se muestran únicamente las actividades "
            "resueltas correctamente."
        )

    st.divider()

    st.caption(
        "Referencia: Manual de Rendimiento Caterpillar, "
        "edición 42, páginas 146, 148 y 1573."
    )
