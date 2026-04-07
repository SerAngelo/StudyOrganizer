from datetime import datetime, timedelta
import pickle
from tabulate import tabulate


PKL_FILE = "binary_output.pkl"

RED   = "\033[31m"
RESET = "\033[0m"


# ─────────────────────────────────────────────
#  Data classes
# ─────────────────────────────────────────────

class Argomento:
    def __init__(self, nome_arg: str):
        self.nome = nome_arg
        self.data_inizio: datetime | None = None
        self.date: list[str] = []
        self.sessioni_completate: set[str] = set()  # date esplicitamente segnate come fatte
        self.minuti_studiati: int = 0               # minuti totali accumulati dal timer
        self.sottoargomenti: list[str] = []         # elenco di sottoargomenti per il ripasso random

    def set_data(self, new_data: str) -> None:
        self.date.append(new_data)

    def set_data_inizio(self, data_inizio: datetime | None) -> None:
        self.data_inizio = data_inizio

    def segna_completato(self, data: str) -> None:
        self.sessioni_completate.add(data)

    def aggiungi_minuti(self, minuti: int) -> None:
        self.minuti_studiati += minuti

    def is_completato(self) -> bool:
        """True se almeno una sessione è stata esplicitamente completata."""
        return bool(self.sessioni_completate)

    def print_info(self) -> None:
        print(f"  Argomento: {self.nome}")


class Materia:
    def __init__(self, nome: str, argomenti: list):
        self.nome = nome
        self.argomenti = argomenti
        self.data_esame: datetime | None = None

    @property
    def N_argomenti(self) -> int:
        return len(self.argomenti)

    def set_data_esame(self, data_esame: datetime | None) -> None:
        self.data_esame = data_esame

    def print_info(self) -> None:
        print(f"Materia: {self.nome}")
        for argomento in self.argomenti:
            argomento.print_info()
        print()


# ─────────────────────────────────────────────
#  Compatibility helper
# ─────────────────────────────────────────────

def _compat(arg: Argomento) -> Argomento:
    if not hasattr(arg, 'sessioni_completate'):
        arg.sessioni_completate = set()
    if not hasattr(arg, 'minuti_studiati'):
        arg.minuti_studiati = 0
    if not hasattr(arg, 'sottoargomenti'):
        arg.sottoargomenti = []
    # vecchi .pkl avevano pomodori_completati
    if hasattr(arg, 'pomodori_completati'):
        if not arg.minuti_studiati:
            arg.minuti_studiati = arg.pomodori_completati * 25
        del arg.__dict__['pomodori_completati']
    return arg


# ─────────────────────────────────────────────
#  File parsing
# ─────────────────────────────────────────────

def leggi_materie_disponibili(nome_file: str) -> list[str]:
    materie = []
    try:
        with open(nome_file, 'r') as f:
            for line in f:
                token = line.strip().split()
                if token and token[0].startswith('#'):
                    materie.append(token[0])
    except FileNotFoundError:
        pass
    return materie


def leggi_file_e_crea_lista_materie(nome_file: str, materie_interessate: list[str]) -> list[Materia]:
    materie: list[Materia] = []
    materia_corrente: Materia | None = None

    with open(nome_file, 'r') as file:
        for line in file:
            token = line.strip().split()
            if not token:
                continue

            if token[0].startswith('#'):
                nome_tag = token[0]
                if nome_tag not in materie_interessate:
                    materia_corrente = None
                    continue

                argomenti: list[Argomento] = []
                materia_corrente = Materia(nome_tag, argomenti)

                try:
                    data_fine = datetime(int(token[1]), int(token[2]), int(token[3]))
                except (IndexError, ValueError):
                    data_fine = None

                materia_corrente.set_data_esame(data_fine)
                materie.append(materia_corrente)

            elif materia_corrente is not None and len(token) > 3:
                nome_arg = token[0]
                try:
                    data_inizio = datetime(int(token[1]), int(token[2]), int(token[3]))
                except (IndexError, ValueError):
                    data_inizio = None

                arg = Argomento(nome_arg)
                arg.set_data_inizio(data_inizio)
                materia_corrente.argomenti.append(arg)

    return materie


# ─────────────────────────────────────────────
#  PKL helpers
# ─────────────────────────────────────────────

def _carica(filePKL: str = PKL_FILE) -> list[Materia]:
    with open(filePKL, 'rb') as f:
        materie, _ = pickle.load(f)
    for materia in materie:
        for arg in materia.argomenti:
            _compat(arg)
    return materie


def _salva(materie: list[Materia], filePKL: str = PKL_FILE) -> None:
    with open(filePKL, 'wb') as f:
        pickle.dump([materie, datetime.now()], f)


# ─────────────────────────────────────────────
#  Core logic — calendario
# ─────────────────────────────────────────────

def ripetizione_spaziata(
    nome_file: str,
    materie_da_ripassare: list[str],
    ripetizioni: int,
    save: bool = False,
) -> list[Materia]:

    materie = leggi_file_e_crea_lista_materie(nome_file, materie_da_ripassare)

    for materia in materie:
        if materia.data_esame is None:
            print(f"  [!] Materia '{materia.nome}' senza data esame — saltata.")
            continue

        for arg in materia.argomenti:
            if arg.data_inizio is None:
                continue

            dataI = arg.data_inizio
            dataF = materia.data_esame
            total_days = (dataF - dataI).days

            if total_days <= 0:
                continue

            giorni = [
                (dataI + timedelta(days=g)).strftime('%Y-%m-%d')
                for g in range(total_days)
            ]

            correct_days = {
                int(n * (n + 1) / 2)
                for n in range(ripetizioni)
            }

            for idy, day in enumerate(giorni):
                if idy in correct_days:
                    arg.set_data(day)

    if save:
        with open(PKL_FILE, 'wb') as f:
            pickle.dump([materie, datetime.now()], f)
        print(f"\n  ✓ Calendario salvato in '{PKL_FILE}'")

    return materie


# ─────────────────────────────────────────────
#  Sessione di oggi
# ─────────────────────────────────────────────

def sessione_di_oggi(
    filePKL: str = PKL_FILE,
) -> tuple[list[tuple], list[tuple]]:
    """
    Ritorna (saltati, oggi):
    - saltati: (materia, arg) con sessioni scadute non completate (deduplicati per arg)
    - oggi:    (materia, arg) pianificati per oggi e non ancora completati
    """
    today = datetime.now().strftime('%Y-%m-%d')
    materie = _carica(filePKL)

    saltati: list[tuple] = []
    oggi: list[tuple] = []
    seen_saltati: set[str] = set()

    for materia in materie:
        for arg in materia.argomenti:
            # Sessioni passate non completate (arg non ancora fatto in quei giorni)
            ha_arretrati = any(
                d < today and d not in arg.sessioni_completate
                for d in arg.date
            )
            if ha_arretrati and arg.nome not in seen_saltati:
                saltati.append((materia, arg))
                seen_saltati.add(arg.nome)

            # Sessione di oggi non completata
            if today in arg.date and today not in arg.sessioni_completate:
                oggi.append((materia, arg))

    return saltati, oggi


def segna_completato(
    filePKL: str,
    materia_nome: str,
    argomento_nome: str,
    scope: str = "today",   # "today" | "past"
) -> None:
    """
    scope='today' : marca solo la data odierna (sessione pianificata per oggi)
    scope='past'  : marca tutte le date passate non ancora completate (arretrati)
    """
    today = datetime.now().strftime('%Y-%m-%d')
    materie = _carica(filePKL)
    for materia in materie:
        if materia.nome == materia_nome:
            for arg in materia.argomenti:
                if arg.nome == argomento_nome:
                    if scope == "today":
                        if today in arg.date and today not in arg.sessioni_completate:
                            arg.segna_completato(today)
                    elif scope == "past":
                        for d in arg.date:
                            if d < today and d not in arg.sessioni_completate:
                                arg.segna_completato(d)
    _salva(materie, filePKL)


def aggiungi_minuti_studio(
    filePKL: str,
    materia_nome: str,
    argomento_nome: str,
    minuti: int,
) -> None:
    materie = _carica(filePKL)
    for materia in materie:
        if materia.nome == materia_nome:
            for arg in materia.argomenti:
                if arg.nome == argomento_nome:
                    arg.aggiungi_minuti(minuti)
    _salva(materie, filePKL)


# ─────────────────────────────────────────────
#  Statistiche
# ─────────────────────────────────────────────

def statistiche(filePKL: str = PKL_FILE) -> None:
    today_str = datetime.now().strftime('%Y-%m-%d')
    materie = _carica(filePKL)

    print()
    rows = []
    totale_minuti = 0

    for materia in materie:
        sessioni_totali  = sum(len(a.date) for a in materia.argomenti)
        sessioni_fatte   = sum(len(a.sessioni_completate) for a in materia.argomenti)
        sessioni_saltate = sum(
            len([d for d in a.date if d < today_str and d not in a.sessioni_completate])
            for a in materia.argomenti
        )
        minuti = sum(a.minuti_studiati for a in materia.argomenti)
        totale_minuti += minuti
        ore = minuti / 60
        perc = f"{int(sessioni_fatte / sessioni_totali * 100)}%" if sessioni_totali else "N/A"

        rows.append([
            materia.nome,
            f"{sessioni_fatte}/{sessioni_totali}",
            perc,
            sessioni_saltate,
            f"{ore:.1f}h",
        ])

    print(tabulate(
        rows,
        headers=["Materia", "Sessioni", "Completamento", "Saltate", "Ore di studio"],
        tablefmt="rounded_outline",
    ))

    print(f"\n  Ore di studio totali: {totale_minuti / 60:.1f}h  ({totale_minuti} min)\n")


# ─────────────────────────────────────────────
#  Output / display
# ─────────────────────────────────────────────

def date_esame(filePKL: str = PKL_FILE) -> None:
    materie = _carica(filePKL)
    rows = []
    for mat in materie:
        if mat.data_esame is None:
            rows.append([mat.nome, "N/A", "N/A"])
        else:
            giorni_rimanenti = (mat.data_esame - datetime.now()).days
            rows.append([
                mat.nome,
                mat.data_esame.strftime('%Y-%m-%d'),
                f"{giorni_rimanenti} gg",
            ])
    print()
    print(tabulate(rows, headers=["Materia", "Data esame", "Giorni rimanenti"], tablefmt="rounded_outline"))
    print()


def _cella_colorata(testo: str, rosso: bool) -> str:
    if not testo:
        return ""
    return f"{RED}{testo}{RESET}" if rosso else testo


def mostra_calendario_terminale(filePKL: str = PKL_FILE) -> None:
    """
    Stampa il calendario nel terminale colorando in rosso le celle
    che contengono argomenti con sessioni scadute e non completate.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    materie = _carica(filePKL)

    # Costruisco mappa data → materia → lista argomenti
    argomenti_per_data: dict = {}
    for materia in materie:
        for arg in materia.argomenti:
            for data in arg.date:
                argomenti_per_data.setdefault(data, {})
                argomenti_per_data[data].setdefault(materia.nome, [])
                argomenti_per_data[data][materia.nome].append(arg)

    date_ordinate = sorted(argomenti_per_data.keys())

    table_rows = []
    for data in date_ordinate:
        row = [data]
        for materia in materie:
            if materia.nome in argomenti_per_data[data]:
                args = argomenti_per_data[data][materia.nome]
                parti = []
                for a in args:
                    # Rosso se: data passata E quella data non è in sessioni_completate
                    scaduto = data < today and data not in a.sessioni_completate
                    parti.append(_cella_colorata(a.nome, scaduto))
                row.append(", ".join(parti))
            else:
                row.append("")
        table_rows.append(row)

    headers = ["Data"] + [m.nome for m in materie]
    print(tabulate(table_rows, headers, tablefmt="grid"))


def stampa_tabella_materie(filePKL: str = PKL_FILE, nome_file_output: str = "calendario.txt") -> None:
    """Salva il calendario su file .txt (senza colori ANSI)."""
    materie = _carica(filePKL)
    argomenti_per_data: dict = {}

    for materia in materie:
        for argomento in materia.argomenti:
            for data in argomento.date:
                argomenti_per_data.setdefault(data, {})
                argomenti_per_data[data].setdefault(materia.nome, [])
                argomenti_per_data[data][materia.nome].append(argomento)

    date_ordinate = sorted(argomenti_per_data.keys())
    table_rows = []
    for data in date_ordinate:
        row = [data]
        for materia in materie:
            if materia.nome in argomenti_per_data[data]:
                args = argomenti_per_data[data][materia.nome]
                row.append(", ".join(a.nome for a in args))
            else:
                row.append("")
        table_rows.append(row)

    headers = ["Data"] + [m.nome for m in materie]
    table = tabulate(table_rows, headers, tablefmt="grid")

    with open(nome_file_output, 'w') as f:
        f.write(table)

    print(f"\n  ✓ Tabella salvata in '{nome_file_output}'")


# ─────────────────────────────────────────────
#  Creazione calendario da dati strutturati (UI)
# ─────────────────────────────────────────────

def crea_calendario_da_dizionari(
    dati: list[dict],
    ripetizioni: int,
) -> None:
    """
    Crea e salva un calendario da dati strutturati provenienti dalla GUI.

    dati = [
        {
            'nome': '#Fisica',
            'data_esame': datetime(2025, 6, 15),
            'argomenti': [
                {'nome': 'Cinematica', 'data_inizio': datetime(2025, 3, 1)},
                ...
            ]
        },
        ...
    ]
    """
    materie: list[Materia] = []

    for d in dati:
        args: list[Argomento] = []
        m = Materia(d['nome'], args)
        m.set_data_esame(d.get('data_esame'))
        for a_dict in d.get('argomenti', []):
            arg = Argomento(a_dict['nome'])
            arg.set_data_inizio(a_dict.get('data_inizio'))
            arg.sottoargomenti = list(a_dict.get('sottoargomenti', []))
            args.append(arg)
        materie.append(m)

    correct_days = {int(n * (n + 1) / 2) for n in range(ripetizioni)}

    for materia in materie:
        if materia.data_esame is None:
            continue
        for arg in materia.argomenti:
            if arg.data_inizio is None:
                continue
            dataI = arg.data_inizio
            dataF = materia.data_esame
            total = (dataF - dataI).days
            if total <= 0:
                continue
            for g in range(total):
                if g in correct_days:
                    day = (dataI + timedelta(days=g)).strftime('%Y-%m-%d')
                    arg.set_data(day)

    _salva(materie)
    print(f"  ✓ Calendario salvato in '{PKL_FILE}'")
