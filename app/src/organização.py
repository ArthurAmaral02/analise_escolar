# notação das variaveis

from pathlib import Path
VARIAVEIS_NUMERICAS = (
    "age",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
)

VARIAVEIS_ORDINAIS = (
    "Medu",
    "Fedu",
    "traveltime",
    "studytime",
    "famrel",
    "freetime",
    "goout",
    "Dalc",
    "Walc",
    "health"
)

VARIAVEIS_BINARIAS = (
    "school",
    "sex",
    "address",
    "famsize",
    "Pstatus",
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic"
)

VARIAVEIS_NOMINAIS = (
    "Mjob",
    "Fjob",
    "reason",
    "guardian"
)

# ===================================================================================
NOTA_MINIMA_APROVACAO = 10
# ===================================================================================
# Faixas de faltas: (descrição, mínimo, máximo)
FAIXAS_FALTAS = (
    ("0 faltas", 0, 0),
    ("1 a 5 faltas", 1, 5),
    ("6 a 10 faltas", 6, 10),
    ("mais de 10 faltas", 11, None),
)

LIMITES_VARIAVEIS = {
    "age": (15, 22),
    "Medu": (0, 4),
    "Fedu": (0, 4),
    "traveltime": (1, 4),
    "studytime": (1, 4),
    "failures": (0, 3),
    "famrel": (1, 5),
    "freetime": (1, 5),
    "goout": (1, 5),
    "Dalc": (1, 5),
    "Walc": (1, 5),
    "health": (1, 5),
    "G1": (0, 20),
    "G2": (0, 20),
    "G3": (0, 20)
}

COLUNAS_BINARIAS = (
    "school", "sex", "address", "famsize", "Pstatus",
    "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic",
    "Mjob_teacher", "Mjob_health", "Mjob_services",
    "Mjob_at_home", "Mjob_other",
    "Fjob_teacher", "Fjob_health", "Fjob_services",
    "Fjob_at_home", "Fjob_other",
    "reason_home", "reason_reputation",
    "reason_course", "reason_other",
    "guardian_mother", "guardian_father", "guardian_other"
)

GRUPOS_ONE_HOT = {
    "Mjob": (
        "Mjob_teacher", "Mjob_health", "Mjob_services",
        "Mjob_at_home", "Mjob_other"
    ),
    "Fjob": (
        "Fjob_teacher", "Fjob_health", "Fjob_services",
        "Fjob_at_home", "Fjob_other"
    ),
    "reason": (
        "reason_home", "reason_reputation",
        "reason_course", "reason_other"
    ),
    "guardian": (
        "guardian_mother", "guardian_father",
        "guardian_other"
    )
}


DELIMITADOR = ";"
CAMINHO_CSV = Path(__file__).resolve().parent.parent / "dados" / "student-mat.csv"

COLUNAS_INTEIRAS = (
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3"
)

CODIFICACAO_BINARIA = {
    "school": {"GP": 0, "MS": 1},
    "sex": {"F": 0, "M": 1},
    "address": {"U": 0, "R": 1},
    "famsize": {"LE3": 0, "GT3": 1},
    "Pstatus": {"T": 0, "A": 1},
    "schoolsup": {"no": 0, "yes": 1},
    "famsup": {"no": 0, "yes": 1},
    "paid": {"no": 0, "yes": 1},
    "activities": {"no": 0, "yes": 1},
    "nursery": {"no": 0, "yes": 1},
    "higher": {"no": 0, "yes": 1},
    "internet": {"no": 0, "yes": 1},
    "romantic": {"no": 0, "yes": 1}
}

CATEGORIAS_NOMINAIS = {
    "Mjob": ("teacher", "health", "services", "at_home", "other"),
    "Fjob": ("teacher", "health", "services", "at_home", "other"),
    "reason": ("home", "reputation", "course", "other"),
    "guardian": ("mother", "father", "other")
}


TODAS_VARIAVEIS = (
    VARIAVEIS_NUMERICAS
    + VARIAVEIS_ORDINAIS
    + VARIAVEIS_BINARIAS
    + VARIAVEIS_NOMINAIS
)

VARIAVEIS_ORIGINAIS = (
    "school", "sex", "age", "address", "famsize",
    "Pstatus", "Medu", "Fedu", "traveltime",
    "studytime", "failures", "schoolsup", "famsup",
    "paid", "activities", "nursery", "higher",
    "internet", "romantic", "famrel", "freetime",
    "goout", "Dalc", "Walc", "health", "absences",
    "G1", "G2", "G3", "Mjob", "Fjob",
    "reason", "guardian"
)
