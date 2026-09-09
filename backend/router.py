"""
BLOCK 6 · UEBUNG: Der intelligente Router
=========================================
Die Kernidee des ganzen Workshops als Code:

    Private Daten oder simple Aufgabe  -> lokales Modell
    Komplexes Reasoning, langer Kontext -> Cloud

Implementiere choose_backend(). Starte naiv (Keywords + Laenge),
wir diskutieren danach, was in Produktion besser waere.

Haengst du fest?  ->  backend/solutions/router.py
"""

# Woerter, die auf private/interne Daten hindeuten.
# TODO 1: Ergaenze die Liste – was waere in DEINER Firma "privat"?
PRIVATE_KEYWORDS = [
    "kunde", "kundin", "mitarbeiter", "lohn", "gehalt",
    "vertraulich", "intern", "diagnose", "iban",
]


def is_private(text: str) -> bool:
    """True, wenn der Text private/interne Daten enthalten koennte."""
    # TODO 2: Pruefe, ob eines der PRIVATE_KEYWORDS im Text vorkommt
    #         (Tipp: text.lower())
    raise NotImplementedError("TODO 2: is_private implementieren")


def is_complex(text: str) -> bool:
    """True, wenn die Aufgabe vermutlich Cloud-Niveau braucht."""
    # TODO 3: Einfache Heuristik, z.B.:
    #   - Text laenger als 2000 Zeichen  -> komplex
    #   - Woerter wie "analysiere", "begruende", "schreibe einen Aufsatz"
    raise NotImplementedError("TODO 3: is_complex implementieren")


def choose_backend(messages: list[dict]) -> str:
    """
    Entscheidet 'local' oder 'cloud' fuer eine Konversation.
    REGEL: Privat schlaegt IMMER alles andere. Compliance first.
    """
    # TODO 4: Alle User-Nachrichten zu einem Text zusammenfassen,
    #         dann: privat -> "local", komplex -> "cloud", sonst -> "local"
    raise NotImplementedError("TODO 4: choose_backend implementieren")
