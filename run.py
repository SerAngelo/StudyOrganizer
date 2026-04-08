import os
import time
import questionary
from questionary import Style
import study_organizer as so

# ─────────────────────────────────────────────
#  Style
# ─────────────────────────────────────────────

STYLE = Style([
    ("qmark",        "fg:#00bcd4 bold"),
    ("question",     "bold"),
    ("answer",       "fg:#00bcd4 bold"),
    ("pointer",      "fg:#00bcd4 bold"),
    ("highlighted",  "fg:#00bcd4 bold"),
    ("selected",     "fg:#00bcd4"),
    ("separator",    "fg:#555555"),
    ("instruction",  "fg:#888888"),
])

BANNER = r"""
   _____ _             _          ____                        _              
  / ____| |           | |        / __ \                      (_)             
 | (___ | |_ _   _  __| |_   _  | |  | |_ __ __ _  __ _ _ __  _ _______ _ __ 
  \___ \| __| | | |/ _` | | | | | |  | | '__/ _` |/ _` | '_ \| |_  / _ \ '__|
  ____) | |_| |_| | (_| | |_| | | |__| | | | (_| | (_| | | | | |/ /  __/ |   
 |_____/ \__|\__,_|\__,_|\__, |  \____/|_|  \__, |\__,_|_| |_|_/___\___|_|   
                          __/ |              __/ |                           
                         |___/              |___/                            
"""

# Sentinel per "torna al menu" — evita ambiguità con None (Ctrl+C)
BACK = object()


# ─────────────────────────────────────────────
#  Helpers UI
# ─────────────────────────────────────────────

def clear() -> None:
    os.system("clear")


def header() -> None:
    clear()
    print("─" * 80)
    print(BANNER)
    print("         Your Ultimate Study Companion")
    print("─" * 80)
    print()


def back_menu() -> None:
    """Schermata con solo il pulsante 'Torna al menu'."""
    questionary.select(
        "",
        choices=[questionary.Choice("  ← Torna al menu", value=BACK)],
        style=STYLE,
    ).ask()


def ask_file(prompt: str, must_exist: bool = False) -> str:
    while True:
        path = questionary.text(prompt, style=STYLE).ask()
        if path is None:
            return ""
        path = path.strip()
        if must_exist and not os.path.isfile(path):
            print(f"  [!] File '{path}' non trovato. Riprova.")
            continue
        return path


# ─────────────────────────────────────────────
#  Timer
# ─────────────────────────────────────────────

def avvia_timer(materia_nome: str, argomento_nome: str) -> int:
    """
    Stopwatch: conta il tempo di studio.
    Ctrl+C per fermare. Ritorna i minuti trascorsi.
    """
    clear()
    print("─" * 80)
    print(f"\n  Materia:   {materia_nome}")
    print(f"  Argomento: {argomento_nome}")
    print("\n  Timer avviato. Premi Ctrl+C quando hai finito.\n")
    print("─" * 80)

    start = time.time()
    try:
        while True:
            elapsed = int(time.time() - start)
            h, rem = divmod(elapsed, 3600)
            m, s = divmod(rem, 60)
            display = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            print(f"\r  ⏱  {display}", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        elapsed = int(time.time() - start)
        minuti = max(1, elapsed // 60)
        print(f"\n\n  Timer fermato. Tempo registrato: {minuti} min")
        return minuti


# ─────────────────────────────────────────────
#  Sessione di oggi
# ─────────────────────────────────────────────

def _mostra_lista_sessione(saltati: list, oggi: list) -> None:
    if saltati:
        print(f"  \033[31mArgomenti saltati da ripetere ({len(saltati)}):\033[0m")
        per_mat: dict = {}
        for mat, arg in saltati:
            per_mat.setdefault(mat.nome, []).append(arg.nome)
        for nome_mat, args in per_mat.items():
            print(f"    {nome_mat}")
            for a in args:
                print(f"      • {a}")
        print()

    if oggi:
        print(f"  Argomenti da ripetere oggi ({len(oggi)}):")
        per_mat = {}
        for mat, arg in oggi:
            per_mat.setdefault(mat.nome, []).append(arg.nome)
        for nome_mat, args in per_mat.items():
            print(f"    {nome_mat}")
            for a in args:
                print(f"      • {a}")
        print()


def _build_scelte(saltati: list, oggi: list) -> list:
    """
    Costruisce la lista di Choice per questionary.
    Un argomento può comparire due volte se è sia saltato che da ripetere oggi.
    Il valore è (materia_nome, arg_nome, scope) con scope='past' o 'today'.
    """
    scelte = []

    if saltati:
        scelte.append(questionary.Separator("  ── Saltati ──"))
        for mat, arg in saltati:
            label = f"  {mat.nome}  →  {arg.nome}"
            scelte.append(questionary.Choice(label, value=(mat.nome, arg.nome, "past")))

    if oggi:
        scelte.append(questionary.Separator("  ── Oggi ──"))
        for mat, arg in oggi:
            label = f"  {mat.nome}  →  {arg.nome}"
            scelte.append(questionary.Choice(label, value=(mat.nome, arg.nome, "today")))

    scelte.append(questionary.Separator())
    scelte.append(questionary.Choice("  ← Torna al menu", value=BACK))
    return scelte


def _ridisegna_sessione() -> tuple[list, list] | None:
    """Ricarica, ridisegna header + lista. Ritorna (saltati, oggi) o None se file mancante."""
    header()
    print("  ── Sessione di oggi ──\n")
    try:
        saltati, oggi = so.sessione_di_oggi(so.PKL_FILE)
    except FileNotFoundError:
        print("  [!] Nessun calendario trovato. Creane uno prima.")
        return None
    _mostra_lista_sessione(saltati, oggi)
    return saltati, oggi


def sessione_di_oggi() -> None:
    result = _ridisegna_sessione()
    if result is None:
        back_menu()
        return

    saltati, oggi = result
    if not saltati and not oggi:
        print("  ✓ Nessun argomento da ripetere. Ottimo lavoro!")
        back_menu()
        return

    while True:
        if not saltati and not oggi:
            print("\n  ✓ Sessione completata!")
            back_menu()
            return

        scelte_arg = _build_scelte(saltati, oggi)

        scelta = questionary.select(
            "  Seleziona l'argomento:",
            choices=scelte_arg,
            style=STYLE,
        ).ask()

        if scelta is None or scelta is BACK:
            break

        materia_nome, arg_nome, scope = scelta  # sempre 3 elementi

        # ── Azione sull'argomento ──
        scope_label = "arretrati" if scope == "past" else "sessione di oggi"
        azione = questionary.select(
            f"  '{arg_nome}'  [{scope_label}]:",
            choices=[
                questionary.Choice("  Avvia timer", value="timer"),
                questionary.Choice("  Segna come fatto", value="fatto"),
                questionary.Choice("  ← Indietro", value=BACK),
            ],
            style=STYLE,
        ).ask()

        if azione is None or azione is BACK:
            # Torna indietro: ridisegna per pulire lo schermo
            result = _ridisegna_sessione()
            if result is None:
                return
            saltati, oggi = result
            continue

        if azione == "timer":
            minuti = avvia_timer(materia_nome, arg_nome)
            so.aggiungi_minuti_studio(so.PKL_FILE, materia_nome, arg_nome, minuti)
            time.sleep(1)

        elif azione == "fatto":
            so.segna_completato(so.PKL_FILE, materia_nome, arg_nome, scope)
            print(f"\n  ✓ '{arg_nome}' segnato come completato ({scope_label}).")
            time.sleep(0.8)

        # Ridisegna sempre dopo un'azione
        result = _ridisegna_sessione()
        if result is None:
            return
        saltati, oggi = result


# ─────────────────────────────────────────────
#  Azioni menu
# ─────────────────────────────────────────────

def crea_nuovo_calendario() -> None:
    header()
    print("  ── Nuovo calendario ──\n")

    nome_file = ask_file("  File .txt con le materie:", must_exist=True)
    if not nome_file:
        back_menu()
        return

    disponibili = so.leggi_materie_disponibili(nome_file)
    if not disponibili:
        print("  [!] Nessuna materia trovata nel file.")
        back_menu()
        return

    materie_scelte = questionary.checkbox(
        "  Seleziona le materie da includere:",
        choices=disponibili,
        instruction="",
        style=STYLE,
    ).ask()

    if not materie_scelte:
        print("  [!] Nessuna materia selezionata.")
        back_menu()
        return

    rip_str = questionary.text(
        "  Numero di ripetizioni ideale per argomento:",
        validate=lambda v: v.isdigit() and int(v) > 0 or "Inserisci un intero > 0",
        style=STYLE,
    ).ask()
    if rip_str is None:
        back_menu()
        return
    ripetizioni = int(rip_str)

    nome_output = questionary.text(
        "  Nome file .txt per il calendario:",
        default="calendario.txt",
        style=STYLE,
    ).ask()
    if not nome_output:
        back_menu()
        return

    print()
    so.ripetizione_spaziata(nome_file, materie_scelte, ripetizioni, save=True)
    so.stampa_tabella_materie(so.PKL_FILE, nome_output)
    back_menu()


def mostra_date() -> None:
    header()
    print("  ── Date esami ──\n")
    try:
        so.date_esame(so.PKL_FILE)
    except FileNotFoundError:
        print("  [!] Nessun calendario trovato. Creane uno prima.")
    back_menu()


def mostra_statistiche() -> None:
    header()
    print("  ── Statistiche di studio ──\n")
    try:
        so.statistiche(so.PKL_FILE)
    except FileNotFoundError:
        print("  [!] Nessun calendario trovato. Creane uno prima.")
    back_menu()


def mostra_calendario() -> None:
    header()
    print("  ── Calendario ──\n")
    try:
        so.mostra_calendario_terminale(so.PKL_FILE)
    except FileNotFoundError:
        print("  [!] Nessun calendario trovato. Creane uno prima.")
    back_menu()


def mostra_help() -> None:
    header()
    print("  ── Formato file di input ──\n")
    print("""  Il file .txt deve essere strutturato così:

    #NomeMateria YYYY MM GG     ← data esame
    NomeArgomento1 YYYY MM GG   ← data inizio ripasso
    NomeArgomento2 YYYY MM GG
    ...

    Esempio:
    ┌──────────────────────────────────────────┐
    │ #Fisica 2025 6 15                        │
    │ Cinematica     2025 3 1                  │
    │ Dinamica       2025 3 5                  │
    │ Termodinamica  2025 3 10                 │
    │                                          │
    │ #Analisi 2025 7 1                        │
    │ Limiti         2025 3 1                  │
    │ Derivate       2025 3 8                  │
    └──────────────────────────────────────────┘
  """)
    back_menu()


# ─────────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────────

MENU_CHOICES = [
    questionary.Choice("  Sessione di oggi",       value="oggi"),
    questionary.Choice("  Crea nuovo calendario",  value="new"),
    questionary.Choice("  Date esami",             value="dates"),
    questionary.Choice("  Statistiche",            value="stats"),
    questionary.Choice("  Calendario",             value="show"),
    questionary.Choice("  Help",                   value="help"),
    questionary.Separator(),
    questionary.Choice("  Esci",                   value="exit"),
]


def main() -> None:
    while True:
        header()
        action = questionary.select(
            "  Cosa vuoi fare?",
            choices=MENU_CHOICES,
            style=STYLE,
        ).ask()

        if action is None or action == "exit":
            clear()
            print("  Arrivederci!\n")
            break
        elif action == "oggi":
            sessione_di_oggi()
        elif action == "new":
            crea_nuovo_calendario()
        elif action == "dates":
            mostra_date()
        elif action == "stats":
            mostra_statistiche()
        elif action == "show":
            mostra_calendario()
        elif action == "help":
            mostra_help()


if __name__ == "__main__":
    main()
