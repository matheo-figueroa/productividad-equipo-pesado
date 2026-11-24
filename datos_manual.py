
# ==================================================
# MANUAL DE RENDIMIENTO CATERPILLAR - EDICION 42
# ==================================================

# Modelos disponibles y tiempo de ciclo base (min)
# Pagina 998 del PDF
# Se utiliza el menor valor de cada intervalo.

TIEMPOS_CICLO = {
    "966H": 0.50,
    "972H": 0.50,
    "980H": 0.50,
    "988H": 0.55,
    "990H": 0.55,
    "992K": 0.60,
    "993K": 0.60,
    "994F": 0.60
}

MODELOS = list(TIEMPOS_CICLO.keys())


# ==================================================
# FACTORES DE CORRECCION DEL TIEMPO DE CICLO
# Pagina 998 del PDF
# ==================================================

FACTORES = {
    "Máquina": {
        "Manipulador de materiales": -0.05
    },

    "Materiales": {
        "Materiales mezclados": 0.02,
        "Hasta 3 mm": 0.02,
        "De 3 a 20 mm": -0.02,
        "De 20 a 150 mm": 0.00,
        "Más de 150 mm": 0.03,
        "Banco o fracturado": 0.04
    },

    "Pila": {
        "Apilado a más de 3 m": 0.00,
        "Apilado a menos de 3 m": 0.01,
        "Descargado por camión": 0.02
    },

    "Varios": {
        "Mismo propietario de camiones y cargadores": -0.04,
        "Propietario independiente de camiones": 0.04,
        "Operación constante": -0.04,
        "Operación intermitente": 0.04,
        "Punto de carga pequeño": 0.04,
        "Punto de carga frágil": 0.05
    }
}

# Factores cuyo valor puede variar según el ejercicio.

FACTORES_VARIABLES = [
    "Más de 150 mm",
    "Banco o fracturado",
    "Mismo propietario de camiones y cargadores",
    "Propietario independiente de camiones",
    "Operación constante",
    "Operación intermitente",
    "Punto de carga pequeño",
    "Punto de carga frágil"
]


# ==================================================
# CAPACIDADES COLMADAS DE LOS CUCHARONES (m3)
# Paginas 938 a 961 del PDF
# Se eliminan los valores repetidos por modelo.
# ==================================================

CAPACIDADES = {
    "966H": [3.5, 6.4],

    "972H": [
        1.8, 3.8, 4.0, 4.2, 4.3, 4.4,
        4.5, 4.6, 4.7, 4.8, 4.9, 5.1, 6.4
    ],

    "980H": [
        4.2, 4.3, 4.5, 4.6, 4.7, 4.9,
        5.0, 5.3, 5.4, 5.6, 5.7, 6.0,
        6.1, 8.2, 10.5
    ],

    "988H": [6.4, 6.9, 7.6, 7.7],

    "990H": [8.4, 8.6, 9.2],

    "992K": [10.7, 11.5, 12.3],

    "993K": [12.0, 12.8, 13.8, 14.5],

    "994F": [14.0, 15.0, 17.0, 19.0]
}


# Paginas de referencia de cada modelo.

PAGINAS_CAPACIDADES = {
    "966H": "938",
    "972H": "939-943",
    "980H": "944-948",
    "988H": "949-950",
    "990H": "951-952",
    "992K": "953-954",
    "993K": "955-960",
    "994F": "961"
}


# ==================================================
# PESO DE LOS MATERIALES Y FACTORES DE CARGA
# Pagina 1575 del PDF
#
# Orden de los datos:
# (Densidad suelta, Densidad en banco, Factor de carga)
#
# Densidades convertidas de kg/m3 a t/m3.
# ==================================================

MATERIALES = {
    "Basalto": (1.960, 2.970, 0.67),
    "Bauxita, caolín": (1.420, 1.900, 0.75),
    "Caliche": (1.250, 2.260, 0.55),
    "Carnotita": (1.630, 2.200, 0.74),
    "Ceniza": (0.560, 0.860, 0.66),

    "Arcilla en su lecho natural": (1.660, 2.020, 0.82),
    "Arcilla seca": (1.480, 1.840, 0.81),
    "Arcilla mojada": (1.660, 2.080, 0.80),

    "Arcilla y grava secas": (1.420, 1.660, 0.85),
    "Arcilla y grava mojadas": (1.540, 1.840, 0.85),

    "Carbón antracita en bruto": (1.190, 1.600, 0.74),
    "Carbón bituminoso en bruto": (0.950, 1.280, 0.74),

    "75% roca y 25% tierra": (1.960, 2.790, 0.70),
    "50% roca y 50% tierra": (1.720, 2.280, 0.75),
    "25% roca y 75% tierra": (1.570, 1.960, 0.80),

    "Tierra apisonada y seca": (1.510, 1.900, 0.80),
    "Tierra excavada y mojada": (1.600, 2.020, 0.79),
    "Tierra limo": (1.250, 1.540, 0.81),

    "Granito fragmentado": (1.660, 2.730, 0.61),

    "Grava de cantera": (1.930, 2.170, 0.89),
    "Grava seca": (1.510, 1.690, 0.89),
    "Grava seca de 6 a 50 mm": (1.690, 1.900, 0.89),
    "Grava mojada de 6 a 50 mm": (2.020, 2.260, 0.89),

    "Yeso fragmentado": (1.810, 3.170, 0.57),
    "Yeso triturado": (1.600, 2.790, 0.57),

    "Piedra caliza fragmentada": (1.540, 2.610, 0.59),
    "Magnetita": (2.790, 3.260, 0.85),
    "Pirita": (2.580, 3.030, 0.85),

    "Arena seca y suelta": (1.420, 1.600, 0.89),
    "Arena húmeda": (1.690, 1.900, 0.89),
    "Arena mojada": (1.840, 2.080, 0.89),

    "Arena y arcilla suelta": (1.600, 2.020, 0.79),
    "Arena y grava seca": (1.720, 1.930, 0.89),
    "Arena y grava mojada": (2.020, 2.230, 0.91),

    "Arenisca": (1.510, 2.520, 0.60),
    "Pizarra bituminosa": (1.250, 1.660, 0.75),
    "Escorias fragmentadas": (1.750, 2.940, 0.60),
    "Piedra triturada": (1.600, 2.670, 0.60),
    "Tierra vegetal": (0.950, 1.370, 0.70),
    "Roca fragmentada": (1.750, 2.610, 0.67)
}
