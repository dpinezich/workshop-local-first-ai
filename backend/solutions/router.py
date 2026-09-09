"""LOESUNG Block 6 – naiver, aber ehrlicher Router."""

PRIVATE_KEYWORDS = [
    "kunde", "kundin", "mitarbeiter", "lohn", "gehalt", "vertraulich",
    "intern", "diagnose", "iban", "ahv", "patient", "bewerbung", "kantonsspital",
]

COMPLEX_HINTS = ["analysiere", "begruende", "begründe", "vergleiche ausfuehrlich",
                 "schreibe einen aufsatz", "refactor", "architektur"]


def is_private(text: str) -> bool:
    t = text.lower()
    return any(kw in t for kw in PRIVATE_KEYWORDS)


def is_complex(text: str) -> bool:
    t = text.lower()
    return len(t) > 2000 or any(h in t for h in COMPLEX_HINTS)


def choose_backend(messages: list[dict]) -> str:
    user_text = " ".join(m.get("content", "") for m in messages
                         if m.get("role") == "user" and isinstance(m.get("content"), str))
    if is_private(user_text):
        return "local"          # Compliance schlaegt alles
    if is_complex(user_text):
        return "cloud"
    return "local"              # Default: lokal ist gratis

# Diskussionsfragen fuer den Workshop:
# 1. Keywords sind schwach (Umlaute, Synonyme, Englisch) – was waere besser?
#    -> Ein kleiner LOKALER Klassifikator entscheidet, was lokal bleiben muss.
#       (Die Entscheidung selbst darf nie in die Cloud – sonst ist das Kind im Brunnen.)
# 2. Wer pflegt die Liste? IT? Legal? -> Governance-Frage, nicht Technik.
# 3. False Positives kosten Qualitaet, False Negatives kosten Compliance.
#    In regulierten Branchen: im Zweifel IMMER lokal.
