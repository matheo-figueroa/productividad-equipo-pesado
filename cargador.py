
import streamlit as st
import pandas as pd

from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING

from datos_manual import (
    MODELOS,
    TIEMPOS_CICLO,
    FACTORES,
    FACTORES_VARIABLES,
    CAPACIDADES,
    PAGINAS_CAPACIDADES,
    MATERIALES
)


# ==================================================
# FUNCIONES MATEMATICAS
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


def leer_numero(texto):
    return decimal(texto.strip().replace(",", "."))


# ==================================================
# FORMULARIO DEL CARGADOR FRONTAL
# ==================================================

def mostrar_cargador():

    st.header("Cálculo de productividad del cargador frontal")

    st.write(
        "Ingrese los datos del ejercicio en las siguientes "
        "secciones y presione Resolver ejercicio."
    )

    def limpiar():
        for clave in list(st.session_state.keys()):
            if clave.startswith("cf_"):
                del st.session_state[clave]

    st.button(
        "Limpiar formulario",
        on_click=limpiar
    )

    # ----------------------------------------------
    # 1. DATOS GENERALES
    # ----------------------------------------------

    st.subheader("1. Datos generales")

    col1, col2 = st.columns(2)

    with col1:
        prd = st.number_input(
            "Producción diaria requerida - Prd (t/día)",
            min_value=0.0,
            value=None,
            placeholder="Ej. 102000",
            key="cf_prd"
        )

    with col2:
        hd = st.number_input(
            "Horas diarias de trabajo - Hd (h/día)",
            min_value=0.0,
            max_value=24.0,
            value=None,
            placeholder="Ingrese las horas",
            key="cf_hd"
        )

    # ----------------------------------------------
    # 2. CARGADORES DISPONIBLES
    # ----------------------------------------------

    st.subheader("2. Cargadores disponibles")

    st.caption(
        "Seleccione el rango de modelos indicado "
        "en el enunciado del ejercicio."
    )

    col1, col2 = st.columns(2)

    with col1:
        modelo_inicial = st.selectbox(
            "Desde el modelo",
            MODELOS,
            key="cf_inicio"
        )

    with col2:
        modelo_final = st.selectbox(
            "Hasta el modelo",
            MODELOS,
            index=len(MODELOS) - 1,
            key="cf_final"
        )

    inicio = MODELOS.index(modelo_inicial)
    final = MODELOS.index(modelo_final)

    modelos_evaluados = MODELOS[inicio:final + 1]

    if modelos_evaluados:
        st.write(
            "Modelos que serán evaluados: "
            + ", ".join(modelos_evaluados)
        )

    # ----------------------------------------------
    # 3. FACTORES DE CORRECCION
    # ----------------------------------------------

    st.subheader("3. Factores de corrección")

    st.caption(
        "Manual Caterpillar, edición 42, página 998 del PDF."
    )

    st.write(
        "Seleccione únicamente las condiciones "
        "mencionadas en el ejercicio."
    )

    factores_seleccionados = []

    for categoria, opciones in FACTORES.items():

        with st.expander(categoria, expanded=True):

            for nombre, valor in opciones.items():

                seleccionado = st.checkbox(
                    f"{nombre} ({valor:+.2f} min)",
                    key=f"cf_factor_{nombre}"
                )

                if seleccionado:

                    if nombre in FACTORES_VARIABLES:

                        valor = st.number_input(
                            f"Valor de corrección: {nombre}",
                            value=float(valor),
                            step=0.01,
                            format="%.2f",
                            key=f"cf_valor_{nombre}"
                        )

                    factores_seleccionados.append(
                        (nombre, decimal(valor))
                    )

    fact = redondear(
        sum(
            (v for _, v in factores_seleccionados),
            Decimal("0")
        )
    )

    st.metric(
        "Suma de factores - Fact",
        f"{fact:+.2f} min"
    )

    # ----------------------------------------------
    # 4. TIEMPO PERDIDO
    # ----------------------------------------------

    st.subheader("4. Tiempo perdido")

    st.write(
        "Ingrese el tiempo perdido en minutos por hora. "
        "Si existen varios valores, sepárelos con punto "
        "y coma (;)."
    )

    texto_tp = st.text_input(
        "Tiempo perdido - Tp (min/h)",
        value="0",
        placeholder="Ej. 5; 0.04; 0.02",
        key="cf_tp"
    )

    error_tp = False

    try:

        tiempos = [
            leer_numero(x)
            for x in texto_tp.split(";")
            if x.strip()
        ]

        if not tiempos or any(
            not x.is_finite() or x < 0
            for x in tiempos
        ):
            raise ValueError()

        tp = redondear(sum(tiempos))

        st.metric(
            "Tiempo perdido total",
            f"{tp:.2f} min/h"
        )

    except Exception:

        error_tp = True
        st.error("Ingrese tiempos perdidos válidos.")

    # ----------------------------------------------
    # 5. CARACTERISTICAS DEL MATERIAL
    # ----------------------------------------------

    st.subheader("5. Características del material")

    modo = st.radio(
        "Origen de los datos",
        [
            "Ingresar datos manualmente",
            "Consultar tabla del manual Caterpillar"
        ],
        key="cf_modo"
    )

    if modo == "Consultar tabla del manual Caterpillar":

        st.caption(
            "Manual Caterpillar, edición 42, "
            "página 1575 del PDF."
        )

        material = st.selectbox(
            "Seleccione el material",
            list(MATERIALES.keys()),
            key="cf_material"
        )

        d_suelta, d_banco, fc = MATERIALES[material]

        estado = st.radio(
            "Estado del material",
            ["Suelto", "En banco"],
            key="cf_estado"
        )

        if estado == "Suelto":
            d = d_suelta
        else:
            d = d_banco

        col1, col2 = st.columns(2)

        col1.metric(
            "Densidad - D",
            f"{d:.3f} t/m³"
        )

        col2.metric(
            "Factor de carga - Fc",
            f"{fc:.2f}"
        )

    else:

        col1, col2 = st.columns(2)

        with col1:
            d = st.number_input(
                "Densidad - D (t/m³)",
                min_value=0.0,
                value=None,
                format="%.3f",
                placeholder="Ej. 1.570",
                key="cf_d"
            )

        with col2:
            fc = st.number_input(
                "Factor de carga - Fc",
                min_value=0.0,
                value=None,
                format="%.3f",
                placeholder="Ej. 0.80",
                key="cf_fc"
            )

        st.caption(
            "Si el factor de carga es 80%, ingrese 0.80."
        )

    st.divider()

    resolver = st.button(
        "Resolver ejercicio",
        type="primary",
        use_container_width=True
    )

    if not resolver:
        return

    # ----------------------------------------------
    # VALIDACION DE LOS DATOS
    # ----------------------------------------------

    if prd is None or prd <= 0:
        st.error("Ingrese una producción diaria mayor a cero.")
        return

    if hd is None or hd <= 0:
        st.error("Ingrese las horas diarias de trabajo.")
        return

    if inicio > final:
        st.error("El rango de cargadores no es válido.")
        return

    if error_tp:
        return

    if tp >= 60:
        st.error("El tiempo perdido debe ser menor a 60 min/h.")
        return

    if d is None or d <= 0:
        st.error("Ingrese una densidad mayor a cero.")
        return

    if fc is None or fc <= 0:
        st.error("Ingrese un factor de carga mayor a cero.")
        return

    prd = decimal(prd)
    hd = decimal(hd)
    d = decimal(d)
    fc = decimal(fc)

    # ==================================================
    # CALCULOS DE PRODUCTIVIDAD
    # ==================================================

    # Paso 1: Produccion requerida por hora.

    prh = redondear(prd / hd)

    # Eficiencia de trabajo.

    ef = redondear((60 - tp) / 60)

    if ef <= 0:
        st.error("La eficiencia redondeada es cero.")
        return

    resultados = []

    for modelo in modelos_evaluados:

        # Paso 2: Tiempo de ciclo.

        tcb = decimal(TIEMPOS_CICLO[modelo])

        tc = redondear(tcb + fact)

        if tc <= 0:
            st.error(
                f"Tiempo de ciclo inválido para {modelo}."
            )
            return

        # Paso 3: Ciclos reales de trabajo.

        ctr = entero_superior((60 - tp) / tc)

        # Paso 4: Carga util por ciclo.

        cuc = redondear(prh / ctr)

        # Paso 5: Seleccion del cucharon.

        scu = redondear((cuc / d) / fc)

        # Paso 6: Produccion real.

        for capacidad in CAPACIDADES[modelo]:

            cchr = decimal(capacidad)

            # Valor inconsistente en el manual.
            # Se excluye hasta verificarlo.

            if modelo == "972H" and cchr == decimal(1.8):
                continue

            prd_real = redondear(
                cchr * ctr * ef * fc * hd * d
            )

            if prd_real <= 0:
                continue

            # Cantidad minima de camiones necesaria.

            camiones = entero_superior(
                prd / prd_real
            )

            produccion_total = redondear(
                prd_real * camiones
            )

            exceso = redondear(
                produccion_total - prd
            )

            resultados.append({
                "Modelo": modelo,
                "Tcb": tcb,
                "Fact": fact,
                "TC": tc,
                "Ctr": ctr,
                "CUC": cuc,
                "SCU": scu,
                "Ef": ef,
                "Cchr": cchr,
                "Prd real": prd_real,
                "Camiones": camiones,
                "Producción total": produccion_total,
                "Exceso": exceso
            })

    if not resultados:
        st.error("No se encontraron alternativas válidas.")
        return

    # Seleccionar la produccion superior mas cercana.

    validos = [
        r for r in resultados
        if r["Producción total"] >= prd
    ]

    if not validos:
        st.error("Ninguna alternativa cumple la producción.")
        return

    mejor = min(
        validos,
        key=lambda r: r["Exceso"]
    )

    # ==================================================
    # PRESENTACION DE RESULTADOS
    # ==================================================

    st.divider()

    st.header("Resultados del ejercicio")

    st.success(
        f"Equipo seleccionado: Caterpillar {mejor['Modelo']}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Modelo seleccionado",
        mejor["Modelo"]
    )

    col2.metric(
        "Capacidad colmada",
        f"{mejor['Cchr']:.2f} m³"
    )

    col3.metric(
        "Cantidad de camiones",
        mejor["Camiones"]
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Producción diaria requerida",
        f"{numero(prd)} t/día"
    )

    col2.metric(
        "Producción total obtenida",
        f"{numero(mejor['Producción total'])} t/día"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Producción real unitaria",
        f"{numero(mejor['Prd real'])} t/día"
    )

    col2.metric(
        "Exceso de producción",
        f"{numero(mejor['Exceso'])} t/día"
    )

    st.write(
        "La alternativa seleccionada cumple con la "
        "producción requerida y presenta el menor "
        "exceso entre las alternativas evaluadas."
    )

    # ----------------------------------------------
    # RESUMEN DE DATOS CALCULADOS
    # ----------------------------------------------

    st.subheader("Resumen de datos importantes")

    resumen = [
        ["Prd", "Producción diaria requerida", numero(prd), "t/día"],
        ["Hd", "Horas diarias", numero(hd), "h/día"],
        ["Prh", "Producción requerida por hora", numero(prh), "t/h"],
        ["Tcb", "Tiempo de ciclo base", numero(mejor["Tcb"]), "min"],
        ["Fact", "Factores de corrección", numero(fact), "min"],
        ["TC", "Tiempo de ciclo", numero(mejor["TC"]), "min"],
        ["Tp", "Tiempo perdido", numero(tp), "min/h"],
        ["Ctr", "Ciclos reales", str(mejor["Ctr"]), "ciclos/h"],
        ["CUC", "Carga útil por ciclo", numero(mejor["CUC"]), "t/ciclo"],
        ["D", "Densidad", str(d), "t/m³"],
        ["Fc", "Factor de carga", str(fc), "-"],
        ["SCU", "Capacidad calculada", numero(mejor["SCU"]), "m³"],
        ["Ef", "Eficiencia", numero(ef), "-"],
        ["Cchr", "Capacidad colmada real", numero(mejor["Cchr"]), "m³"],
        ["Prd real", "Producción real", numero(mejor["Prd real"]), "t/día"]
    ]

    st.table(
        pd.DataFrame(
            resumen,
            columns=[
                "Variable",
                "Descripción",
                "Valor",
                "Unidad"
            ]
        )
    )

    # ----------------------------------------------
    # DESARROLLO MATEMATICO
    # ----------------------------------------------

    st.header("Desarrollo matemático")

    st.caption(
        "Procedimiento correspondiente al modelo seleccionado. "
        "Los resultados se redondean a dos decimales, "
        "excepto los ciclos reales y la cantidad de camiones."
    )

    st.subheader("Paso 1. Producción requerida por hora")

    st.latex(r"Prh=\frac{Prd}{Hd}")

    st.latex(
        rf"Prh=\frac{{{prd}}}{{{hd}}}"
        rf"={prh}\;\text{{t/h}}"
    )

    st.subheader("Paso 2. Tiempo de ciclo")

    st.caption(
        "Tiempo de ciclo base: página 998 del manual."
    )

    st.write(
        f"Modelo: {mejor['Modelo']}"
    )

    st.write(
        f"Tiempo de ciclo base: {mejor['Tcb']} min"
    )

    if factores_seleccionados:

        for nombre, valor in factores_seleccionados:
            st.write(f"{nombre}: {valor:+.2f} min")

        suma_factores = " + ".join(
            f"({v})"
            for _, v in factores_seleccionados
        )

        st.latex(
            rf"Fact={suma_factores}={fact}"
        )

    else:
        st.write("No se seleccionaron factores de corrección.")

    st.latex(r"TC=Tcb+Fact")

    st.latex(
        rf"TC={mejor['Tcb']}+({fact})"
        rf"={mejor['TC']}\;\text{{min}}"
    )

    st.subheader("Paso 3. Ciclos reales de trabajo por hora")

    suma_tiempos = " + ".join(
        str(x) for x in tiempos
    )

    st.latex(
        rf"Tp={suma_tiempos}={tp}"
    )

    st.latex(r"Ctr=\frac{60-Tp}{TC}")

    ctr_original = (60 - tp) / mejor["TC"]

    st.latex(
        rf"Ctr=\frac{{60-{tp}}}{{{mejor['TC']}}}"
        rf"\approx {ctr_original:.6f}"
    )

    st.write("Se aproxima al entero superior.")

    st.latex(
        rf"\boxed{{Ctr={mejor['Ctr']}"
        rf"\;\text{{ciclos/h}}}}"
    )

    st.subheader("Paso 4. Carga útil por ciclo")

    st.latex(r"CUC=\frac{Prh}{Ctr}")

    st.latex(
        rf"CUC=\frac{{{prh}}}{{{mejor['Ctr']}}}"
        rf"\approx {mejor['CUC']}\;\text{{t/ciclo}}"
    )

    st.subheader("Paso 5. Selección del cucharón")

    st.latex(r"SCU=\frac{CUC/D}{Fc}")

    st.latex(
        rf"SCU=\frac{{{mejor['CUC']}/{d}}}{{{fc}}}"
        rf"\approx {mejor['SCU']}\;\text{{m}}^3"
    )

    st.write(
        "Capacidades colmadas disponibles para "
        f"el modelo {mejor['Modelo']}:"
    )

    st.write(
        ", ".join(
            str(c)
            for c in CAPACIDADES[mejor["Modelo"]]
            if not (
                mejor["Modelo"] == "972H" and c == 1.8
            )
        ) + " m³"
    )

    st.caption(
        "Referencia: páginas "
        + PAGINAS_CAPACIDADES[mejor["Modelo"]]
        + " del PDF."
    )

    st.subheader("Paso 6. Producción real")

    st.latex(r"Ef=\frac{60-Tp}{60}")

    st.latex(
        rf"Ef=\frac{{60-{tp}}}{{60}}"
        rf"\approx {ef}"
    )

    st.latex(
        r"Prd_{real}=Cchr\times Ctr\times Ef"
        r"\times Fc\times Hd\times D"
    )

    st.latex(
        rf"Prd_{{real}}={mejor['Cchr']}"
        rf"\times {mejor['Ctr']}"
        rf"\times {ef}"
        rf"\times {fc}"
        rf"\times {hd}"
        rf"\times {d}"
    )

    st.latex(
        rf"\boxed{{Prd_{{real}}={mejor['Prd real']}"
        rf"\;\text{{t/día}}}}"
    )

    # ----------------------------------------------
    # CANTIDAD DE CAMIONES
    # ----------------------------------------------

    st.subheader("Determinación de la cantidad de camiones")

    st.latex(
        r"N=\left\lceil"
        r"\frac{Prd}{Prd_{real}}"
        r"\right\rceil"
    )

    st.latex(
        rf"N=\left\lceil"
        rf"\frac{{{prd}}}{{{mejor['Prd real']}}}"
        rf"\right\rceil={mejor['Camiones']}"
    )

    # Mostrar el ultimo valor inferior al requerido.

    if mejor["Camiones"] > 1:

        anterior = mejor["Camiones"] - 1

        produccion_anterior = redondear(
            mejor["Prd real"] * anterior
        )

        st.write(
            f"{anterior} camiones: "
            f"{numero(produccion_anterior)} t/día. "
            "No cumple la producción requerida."
        )

    st.write(
        f"{mejor['Camiones']} camiones: "
        f"{numero(mejor['Producción total'])} t/día. "
        "Cumple la producción requerida."
    )

    st.latex(r"Prd_{total}=Prd_{real}\times N")

    st.latex(
        rf"Prd_{{total}}={mejor['Prd real']}"
        rf"\times {mejor['Camiones']}"
        rf"={mejor['Producción total']}"
    )

    st.latex(
        rf"Exceso={mejor['Producción total']}-{prd}"
        rf"={mejor['Exceso']}"
    )

    # ----------------------------------------------
    # COMPARACION DE TODAS LAS ALTERNATIVAS
    # ----------------------------------------------

    st.header("Comparación de alternativas")

    st.write(
        "Se evalúan las capacidades colmadas de los "
        "modelos disponibles y se determina la cantidad "
        "mínima de camiones para cada alternativa."
    )

    tabla = []

    ordenados = sorted(
        validos,
        key=lambda r: r["Exceso"]
    )

    for posicion, r in enumerate(ordenados):

        tabla.append({
            "Modelo": r["Modelo"],
            "Cchr (m³)": float(r["Cchr"]),
            "TC (min)": float(r["TC"]),
            "Ctr (ciclos/h)": r["Ctr"],
            "SCU (m³)": float(r["SCU"]),
            "Prd real (t/día)": float(r["Prd real"]),
            "Camiones": r["Camiones"],
            "Producción total (t/día)": float(r["Producción total"]),
            "Exceso (t/día)": float(r["Exceso"]),
            "Selección": "ÓPTIMO" if posicion == 0 else "-"
        })

    df = pd.DataFrame(tabla)

    st.dataframe(
        df.style.format(
            {
                "Cchr (m³)": "{:.2f}",
                "TC (min)": "{:.2f}",
                "SCU (m³)": "{:.2f}",
                "Prd real (t/día)": "{:.2f}",
                "Producción total (t/día)": "{:.2f}",
                "Exceso (t/día)": "{:.2f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Total de alternativas evaluadas: {len(resultados)}"
    )

    if "972H" in modelos_evaluados:
        st.warning(
            "Se excluyó la capacidad de 1.8 m³ del 972H "
            "por una inconsistencia de unidades en la "
            "página 939 del manual, pendiente de verificar."
        )

    st.divider()

    st.subheader("Referencias")

    st.markdown(
        "- Manual de Rendimiento Caterpillar, edición 42.\n"
        "- Páginas 938-961: capacidades colmadas.\n"
        "- Página 998: tiempos de ciclo y correcciones.\n"
        "- Página 1575: densidad y factores de carga.\n"
        "- Procedimiento de laboratorio de productividad "
        "de equipo pesado."
    )
