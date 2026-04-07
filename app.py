"""
Study Organizer — Desktop App
PyQt6 · Sidebar + stacked panels · Dark theme
"""
import sys
import os
import random
import json
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QScrollArea,
    QFrame, QDialog, QLineEdit, QDateEdit, QListWidget,
    QListWidgetItem, QProgressBar, QFileDialog, QMessageBox,
    QSizePolicy, QSlider, QDialogButtonBox, QCheckBox,
    QAbstractItemView, QSpacerItem,
)
from PyQt6.QtCore import Qt, QTimer, QDate, QSize
from PyQt6.QtGui import QFont, QColor

import study_organizer as so

# ── Palette ───────────────────────────────────────────────────────────────────
_BG      = "#111111"
_PANEL   = "#161616"
_CARD    = "#1D1D1D"
_INPUT   = "#242424"
_ACCENT  = "#00BCD4"
_ACCENTD = "#00838F"
_DANGER  = "#E57373"
_SUCCESS = "#81C784"
_WARN    = "#FFB74D"
_TXT1    = "#EFEFEF"
_TXT2    = "#777777"
_TXT3    = "#333333"
_BORDER  = "#242424"
_BORDER2 = "#2E2E2E"
_SW      = 220   # sidebar width


# ── Global stylesheet ─────────────────────────────────────────────────────────
STYLE = f"""
QMainWindow, QWidget {{
    background: {_BG};
    color: {_TXT1};
    font-size: 13px;
}}
QDialog {{
    background: #1A1A1A;
}}
/* Sidebar */
#sidebar {{
    background: {_BG};
    border-right: 1px solid {_BORDER};
}}
#appTitle {{
    color: {_ACCENT};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 28px 20px 4px 20px;
}}
#appSub {{
    color: {_TXT3};
    font-size: 10px;
    padding: 0 20px 24px 20px;
    letter-spacing: 0.5px;
}}
#navBtn {{
    background: transparent;
    border: none;
    border-left: 3px solid transparent;
    color: {_TXT2};
    text-align: left;
    padding: 12px 20px;
    font-size: 13px;
}}
#navBtn:hover {{
    background: rgba(255,255,255,0.04);
    color: {_TXT1};
}}
#navBtn[active="true"] {{
    border-left-color: {_ACCENT};
    color: {_ACCENT};
    background: rgba(0,188,212,0.07);
    font-weight: 600;
}}
/* Panel */
#panel {{ background: {_PANEL}; }}
#panelHeader {{
    background: {_PANEL};
    border-bottom: 1px solid {_BORDER};
}}
/* Cards */
#card {{
    background: {_CARD};
    border: 1px solid {_BORDER};
    border-radius: 8px;
}}
#dayCard {{
    background: {_CARD};
    border: 1px solid {_BORDER};
    border-radius: 8px;
}}
#dayCardToday {{
    background: rgba(0,188,212,0.06);
    border: 1px solid rgba(0,188,212,0.35);
    border-radius: 8px;
}}
/* Buttons */
#accentBtn {{
    background: {_ACCENT};
    color: #000;
    border: none;
    border-radius: 6px;
    padding: 9px 18px;
    font-weight: 700;
    font-size: 13px;
}}
#accentBtn:hover {{ background: {_ACCENTD}; }}
#accentBtn:disabled {{ background: {_TXT3}; color: {_TXT2}; }}
#ghostBtn {{
    background: transparent;
    color: {_TXT2};
    border: 1px solid {_BORDER2};
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 13px;
}}
#ghostBtn:hover {{ color: {_TXT1}; border-color: #555; }}
#dangerBtn {{
    background: transparent;
    color: {_DANGER};
    border: 1px solid rgba(229,115,115,0.25);
    border-radius: 6px;
    padding: 8px 14px;
}}
#dangerBtn:hover {{ background: rgba(229,115,115,0.1); }}
/* Inputs */
QLineEdit, QDateEdit, QSpinBox {{
    background: {_INPUT};
    border: 1px solid {_BORDER2};
    border-radius: 6px;
    color: {_TXT1};
    padding: 9px 11px;
    selection-background-color: {_ACCENT};
}}
QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {{
    border-color: {_ACCENT};
}}
QDateEdit::drop-down {{ border: none; width: 20px; }}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {_BORDER2}; width: 18px; border-radius: 3px;
}}
/* Scroll */
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ background: transparent; width: 5px; margin: 0; }}
QScrollBar::handle:vertical {{
    background: {_BORDER2}; border-radius: 3px; min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
/* List */
QListWidget {{
    background: {_CARD};
    border: 1px solid {_BORDER};
    border-radius: 8px;
    color: {_TXT1};
    outline: none;
    padding: 4px;
}}
QListWidget::item {{
    padding: 10px 12px;
    border-radius: 5px;
    margin: 1px 2px;
}}
QListWidget::item:selected {{
    background: rgba(0,188,212,0.12);
    color: {_ACCENT};
}}
QListWidget::item:hover:!selected {{ background: rgba(255,255,255,0.04); }}
/* Progress */
QProgressBar {{
    background: {_BORDER};
    border-radius: 3px;
    border: none;
    max-height: 5px;
}}
QProgressBar::chunk {{ background: {_ACCENT}; border-radius: 3px; }}
/* Slider */
QSlider::groove:horizontal {{
    background: {_BORDER2}; height: 4px; border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {_ACCENT}; width: 14px; height: 14px;
    margin: -5px 0; border-radius: 7px;
}}
QSlider::sub-page:horizontal {{ background: {_ACCENT}; border-radius: 2px; }}
/* Checkbox */
QCheckBox {{ spacing: 8px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1px solid {_BORDER2}; border-radius: 4px;
    background: {_INPUT};
}}
QCheckBox::indicator:checked {{
    background: {_ACCENT}; border-color: {_ACCENT};
}}
/* Label variants */
#h1 {{ font-size: 20px; font-weight: 700; }}
#h2 {{ font-size: 15px; font-weight: 600; }}
#h3 {{ font-size: 13px; font-weight: 600; }}
#muted {{ color: {_TXT2}; font-size: 12px; }}
#danger {{ color: {_DANGER}; }}
#success {{ color: {_SUCCESS}; }}
#accent {{ color: {_ACCENT}; }}
#sep {{ background: {_BORDER}; max-height: 1px; min-height: 1px; }}
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  DIALOGS
# ═══════════════════════════════════════════════════════════════════════════════

class TimerDialog(QDialog):
    """Stopwatch che conta in avanti. 'Ferma e salva' chiude e ritorna i minuti."""

    def __init__(self, mat_nome: str, arg_nome: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Timer")
        self.setFixedSize(320, 300)
        self.minuti = 0
        self._elapsed = 0

        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 32, 32, 28)
        lay.setSpacing(10)

        mat_lbl = QLabel(mat_nome.lstrip('#'))
        mat_lbl.setObjectName("muted")
        mat_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        arg_lbl = QLabel(arg_nome)
        arg_lbl.setObjectName("h2")
        arg_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._display = QLabel("00:00")
        self._display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._display.setStyleSheet(
            f"font-size: 52px; font-weight: 200; color: {_ACCENT}; letter-spacing: 3px;"
        )

        stop_btn = QPushButton("⏹   Ferma e salva")
        stop_btn.setObjectName("accentBtn")
        stop_btn.setFixedHeight(44)
        stop_btn.clicked.connect(self._ferma)

        cancel_btn = QPushButton("Annulla")
        cancel_btn.setObjectName("ghostBtn")
        cancel_btn.setFixedHeight(36)
        cancel_btn.clicked.connect(self.reject)

        lay.addWidget(mat_lbl)
        lay.addWidget(arg_lbl)
        lay.addStretch()
        lay.addWidget(self._display)
        lay.addStretch()
        lay.addWidget(stop_btn)
        lay.addSpacing(4)
        lay.addWidget(cancel_btn)

        self._qtimer = QTimer(self)
        self._qtimer.setInterval(1000)
        self._qtimer.timeout.connect(self._tick)
        self._qtimer.start()

    def _tick(self):
        self._elapsed += 1
        m, s = divmod(self._elapsed, 60)
        h, m = divmod(m, 60)
        self._display.setText(
            f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        )

    def _ferma(self):
        self._qtimer.stop()
        self.minuti = max(1, self._elapsed // 60)
        self.accept()

    def closeEvent(self, e):
        self._qtimer.stop()
        super().closeEvent(e)


class NuovaMateriaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuova materia")
        self.setFixedWidth(380)
        self.nome = ""
        self.data_esame = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 20)
        lay.setSpacing(14)

        lay.addWidget(_lbl("Nome materia", "h3"))
        self._nome = QLineEdit()
        self._nome.setPlaceholderText("Es: Fisica, Analisi Matematica …")
        lay.addWidget(self._nome)

        lay.addWidget(_lbl("Data esame", "h3"))
        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDate(QDate.currentDate().addMonths(3))
        self._date.setDisplayFormat("dd / MM / yyyy")
        lay.addWidget(self._date)

        lay.addSpacing(6)
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._ok)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _ok(self):
        nome = self._nome.text().strip()
        if not nome:
            return
        self.nome = nome if nome.startswith('#') else f'#{nome}'
        qd = self._date.date()
        self.data_esame = datetime(qd.year(), qd.month(), qd.day())
        self.accept()


class NuovoArgomentoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuovo argomento")
        self.setFixedWidth(380)
        self.nome = ""
        self.data_inizio = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 20)
        lay.setSpacing(14)

        lay.addWidget(_lbl("Nome argomento", "h3"))
        self._nome = QLineEdit()
        self._nome.setPlaceholderText("Es: Cinematica, Limiti …")
        lay.addWidget(self._nome)

        lay.addWidget(_lbl("Data inizio ripasso", "h3"))
        self._date = QDateEdit()
        self._date.setCalendarPopup(True)
        self._date.setDate(QDate.currentDate())
        self._date.setDisplayFormat("dd / MM / yyyy")
        lay.addWidget(self._date)

        lay.addSpacing(6)
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._ok)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _ok(self):
        nome = self._nome.text().strip()
        if not nome:
            return
        self.nome = nome
        qd = self._date.date()
        self.data_inizio = datetime(qd.year(), qd.month(), qd.day())
        self.accept()


class SelezionaMaterieDialog(QDialog):
    """Checkbox per scegliere quali materie importare da un .txt."""

    def __init__(self, disponibili: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleziona materie")
        self.setFixedWidth(340)
        self.selezionate: list[str] = []
        self._checks: list[tuple[str, QCheckBox]] = []

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 20)
        lay.setSpacing(10)

        lay.addWidget(_lbl("Materie trovate nel file:", "h3"))
        lay.addSpacing(4)

        for nome in disponibili:
            cb = QCheckBox(nome.lstrip('#'))
            cb.setChecked(True)
            lay.addWidget(cb)
            self._checks.append((nome, cb))

        lay.addSpacing(10)
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._ok)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _ok(self):
        self.selezionate = [nome for nome, cb in self._checks if cb.isChecked()]
        self.accept()


class GeneraCalendarioDialog(QDialog):
    """Chiede il numero di ripetizioni e genera il calendario."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Genera calendario")
        self.setFixedWidth(380)
        self.ripetizioni = 5

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 20)
        lay.setSpacing(14)

        lay.addWidget(_lbl("Ripetizioni per argomento", "h3"))

        self._val_lbl = QLabel("5")
        self._val_lbl.setStyleSheet(f"font-size: 28px; font-weight: 200; color: {_ACCENT};")
        self._val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(2, 10)
        self._slider.setValue(5)
        self._slider.valueChanged.connect(self._on_slider)

        hint = QLabel(
            "Con 5 ripetizioni i ripassi avvengono ai giorni: 0, 1, 3, 6, 10\n"
            "a partire dalla data di inizio di ogni argomento."
        )
        hint.setObjectName("muted")
        hint.setWordWrap(True)

        lay.addWidget(self._val_lbl)
        lay.addWidget(self._slider)
        lay.addWidget(hint)
        lay.addSpacing(8)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._ok)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _on_slider(self, v):
        self._val_lbl.setText(str(v))

    def _ok(self):
        self.ripetizioni = self._slider.value()
        self.accept()


# ═══════════════════════════════════════════════════════════════════════════════
#  PANEL WIDGETS (riusabili)
# ═══════════════════════════════════════════════════════════════════════════════

def _lbl(text: str, obj_name: str = "") -> QLabel:
    l = QLabel(text)
    if obj_name:
        l.setObjectName(obj_name)
    return l


def _sep() -> QFrame:
    f = QFrame()
    f.setObjectName("sep")
    f.setFrameShape(QFrame.Shape.HLine)
    return f


def _scroll_area() -> tuple[QScrollArea, QWidget, QVBoxLayout]:
    """Returns (scroll, container_widget, container_layout)."""
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    container = QWidget()
    container.setObjectName("panel")
    lay = QVBoxLayout(container)
    lay.setContentsMargins(28, 24, 28, 32)
    lay.setSpacing(8)
    scroll.setWidget(container)
    return scroll, container, lay


def _empty_state(icon: str, title: str, subtitle: str = "") -> QWidget:
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lay.setSpacing(8)
    icon_lbl = QLabel(icon)
    icon_lbl.setStyleSheet("font-size: 40px;")
    icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    t = QLabel(title)
    t.setObjectName("h2")
    t.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lay.addWidget(icon_lbl)
    lay.addWidget(t)
    if subtitle:
        s = QLabel(subtitle)
        s.setObjectName("muted")
        s.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(s)
    return w


class ArgCard(QFrame):
    """Card per un singolo argomento nella sessione di oggi."""

    def __init__(self, mat, arg, scope: str, on_timer, on_done, on_ripassa, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        has_sub = bool(arg.sottoargomenti)
        self.setFixedHeight(76)

        is_past = scope == "past"
        bar_color = _DANGER if is_past else _ACCENT

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 16, 0)
        outer.setSpacing(0)

        # Colored left bar
        bar = QFrame()
        bar.setFixedWidth(4)
        bar.setStyleSheet(
            f"background: {bar_color}; border-radius: 0px; "
            f"border-top-left-radius: 8px; border-bottom-left-radius: 8px;"
        )
        outer.addWidget(bar)
        outer.addSpacing(16)

        # Text
        text_lay = QVBoxLayout()
        text_lay.setSpacing(3)
        text_lay.setContentsMargins(0, 0, 0, 0)
        mat_lbl = QLabel(mat.nome.lstrip('#'))
        mat_lbl.setObjectName("muted")
        arg_lbl = QLabel(arg.nome)
        arg_lbl.setObjectName("h3")
        sub_lbl = QLabel(f"{len(arg.sottoargomenti)} sottoargomenti" if has_sub else "")
        sub_lbl.setStyleSheet(f"color: {_ACCENT}; font-size: 10px;")
        text_lay.addStretch()
        text_lay.addWidget(mat_lbl)
        text_lay.addWidget(arg_lbl)
        if has_sub:
            text_lay.addWidget(sub_lbl)
        text_lay.addStretch()
        outer.addLayout(text_lay)
        outer.addStretch()

        # Buttons
        if has_sub:
            ripassa_btn = QPushButton("🎲  Ripassa")
            ripassa_btn.setObjectName("ghostBtn")
            ripassa_btn.setFixedSize(100, 32)
            ripassa_btn.clicked.connect(lambda: on_ripassa(arg))
            outer.addWidget(ripassa_btn)
            outer.addSpacing(8)

        timer_btn = QPushButton("⏱  Timer")
        timer_btn.setObjectName("ghostBtn")
        timer_btn.setFixedSize(90, 32)
        timer_btn.clicked.connect(lambda: on_timer(mat.nome, arg.nome))

        done_btn = QPushButton("✓  Fatto")
        done_btn.setObjectName("accentBtn")
        done_btn.setFixedSize(90, 32)
        done_btn.clicked.connect(lambda: on_done(mat.nome, arg.nome, scope))

        outer.addWidget(timer_btn)
        outer.addSpacing(8)
        outer.addWidget(done_btn)


# ═══════════════════════════════════════════════════════════════════════════════
#  PANELS
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
#  RANDOM REVIEW DIALOG
# ═══════════════════════════════════════════════════════════════════════════════

class SottoargomentiDialog(QDialog):
    """Gestisce la lista di sottoargomenti di un argomento."""

    def __init__(self, arg, parent=None):
        super().__init__(parent)
        self._arg = arg
        self.setWindowTitle(f"Sottoargomenti — {arg.nome}")
        self.setFixedWidth(420)
        self.setMinimumHeight(320)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 20)
        lay.setSpacing(12)

        lay.addWidget(_lbl(f"Sottoargomenti di «{arg.nome}»", "h2"))
        hint = _lbl("Saranno mostrati in ordine casuale durante il ripasso.", "muted")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        self._list = QListWidget()
        self._list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        for s in arg.sottoargomenti:
            self._list.addItem(s)
        lay.addWidget(self._list)

        # Add row
        add_row = QHBoxLayout()
        self._input = QLineEdit()
        self._input.setPlaceholderText("Nuovo sottoargomento…")
        self._input.returnPressed.connect(self._aggiungi)
        add_btn = QPushButton("Aggiungi")
        add_btn.setObjectName("accentBtn")
        add_btn.setFixedHeight(36)
        add_btn.clicked.connect(self._aggiungi)
        add_row.addWidget(self._input)
        add_row.addWidget(add_btn)
        lay.addLayout(add_row)

        del_btn = QPushButton("Elimina selezionato")
        del_btn.setObjectName("dangerBtn")
        del_btn.setFixedHeight(32)
        del_btn.clicked.connect(self._elimina)
        lay.addWidget(del_btn)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(self._salva)
        lay.addWidget(btns)

    def _aggiungi(self):
        testo = self._input.text().strip()
        if testo:
            self._list.addItem(testo)
            self._input.clear()

    def _elimina(self):
        row = self._list.currentRow()
        if row >= 0:
            self._list.takeItem(row)

    def _salva(self):
        self._arg.sottoargomenti = [
            self._list.item(i).text()
            for i in range(self._list.count())
        ]
        self.accept()


class RandomReviewDialog(QDialog):
    """Mostra i sottoargomenti uno alla volta in ordine casuale."""

    def __init__(self, arg, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Ripasso — {arg.nome}")
        self.setFixedSize(480, 360)

        self._items = arg.sottoargomenti[:]
        random.shuffle(self._items)
        self._idx = 0
        self._revealed = False

        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 32, 32, 28)
        lay.setSpacing(0)

        # Progress bar + counter
        top_row = QHBoxLayout()
        self._counter = QLabel()
        self._counter.setObjectName("muted")
        top_row.addStretch()
        top_row.addWidget(self._counter)
        lay.addLayout(top_row)
        lay.addSpacing(6)

        self._progress = QProgressBar()
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(4)
        lay.addWidget(self._progress)
        lay.addSpacing(32)

        # Card area
        self._card = QFrame()
        self._card.setObjectName("card")
        self._card.setMinimumHeight(140)
        card_lay = QVBoxLayout(self._card)
        card_lay.setContentsMargins(24, 24, 24, 24)
        card_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._arg_lbl = QLabel(arg.nome)
        self._arg_lbl.setObjectName("muted")
        self._arg_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._main_lbl = QLabel()
        self._main_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._main_lbl.setWordWrap(True)
        self._main_lbl.setStyleSheet(
            f"font-size: 20px; font-weight: 600; color: {_TXT1}; line-height: 1.4;"
        )

        card_lay.addWidget(self._arg_lbl)
        card_lay.addSpacing(10)
        card_lay.addWidget(self._main_lbl)
        lay.addWidget(self._card)
        lay.addSpacing(28)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._shuffle_btn = QPushButton("🔀  Rimescola")
        self._shuffle_btn.setObjectName("ghostBtn")
        self._shuffle_btn.setFixedHeight(40)
        self._shuffle_btn.clicked.connect(self._rimescola)

        self._next_btn = QPushButton("Successivo  →")
        self._next_btn.setObjectName("accentBtn")
        self._next_btn.setFixedHeight(40)
        self._next_btn.clicked.connect(self._prossimo)

        close_btn = QPushButton("Chiudi")
        close_btn.setObjectName("ghostBtn")
        close_btn.setFixedHeight(40)
        close_btn.clicked.connect(self.accept)

        btn_row.addWidget(self._shuffle_btn)
        btn_row.addStretch()
        btn_row.addWidget(close_btn)
        btn_row.addWidget(self._next_btn)
        lay.addLayout(btn_row)

        self._aggiorna()

    def _aggiorna(self):
        total = len(self._items)
        if total == 0:
            self._main_lbl.setText("Nessun sottoargomento.")
            self._next_btn.setEnabled(False)
            return

        current = self._items[self._idx]
        self._main_lbl.setText(current)
        self._counter.setText(f"{self._idx + 1} / {total}")
        self._progress.setMaximum(total)
        self._progress.setValue(self._idx + 1)

        is_last = self._idx >= total - 1
        self._next_btn.setText("Ricomincia  ↺" if is_last else "Successivo  →")
        self._next_btn.setStyleSheet(
            f"background: {_TXT3}; color: {_TXT2};" if is_last else ""
        )

    def _prossimo(self):
        total = len(self._items)
        if self._idx >= total - 1:
            # Restart with new shuffle
            self._rimescola()
        else:
            self._idx += 1
            self._aggiorna()

    def _rimescola(self):
        random.shuffle(self._items)
        self._idx = 0
        self._aggiorna()


class OggiPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Sessione di oggi", "h1"))
        hlay.addStretch()
        self._date_lbl = _lbl("", "muted")
        hlay.addWidget(self._date_lbl)
        lay.addWidget(hdr)

        self._scroll, self._container, self._clay = _scroll_area()
        self._clay.addStretch()
        lay.addWidget(self._scroll)

    def refresh(self):
        self._date_lbl.setText(datetime.now().strftime("%d %B %Y"))
        # Clear all widgets except the trailing stretch
        while self._clay.count() > 1:
            item = self._clay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            saltati, oggi = so.sessione_di_oggi(so.PKL_FILE)
        except FileNotFoundError:
            self._clay.insertWidget(0, _empty_state(
                "📂", "Nessun calendario trovato",
                "Crea un calendario dalla sezione Materie"
            ))
            return

        if not saltati and not oggi:
            self._clay.insertWidget(0, _empty_state("✅", "Tutto fatto!", "Nessun argomento da ripetere oggi"))
            return

        pos = 0
        if saltati:
            sec = _lbl(f"  SALTATI  ({len(saltati)})", "muted")
            sec.setStyleSheet(f"color: {_DANGER}; font-size: 11px; letter-spacing: 1px; font-weight: 600;")
            self._clay.insertWidget(pos, sec); pos += 1
            for mat, arg in saltati:
                self._clay.insertWidget(pos, ArgCard(
                    mat, arg, "past", self._on_timer, self._on_done, self._on_ripassa
                )); pos += 1

        if oggi:
            if saltati:
                spacer = QWidget(); spacer.setFixedHeight(8)
                self._clay.insertWidget(pos, spacer); pos += 1
            sec = _lbl(f"  OGGI  ({len(oggi)})", "muted")
            sec.setStyleSheet(f"color: {_ACCENT}; font-size: 11px; letter-spacing: 1px; font-weight: 600;")
            self._clay.insertWidget(pos, sec); pos += 1
            for mat, arg in oggi:
                self._clay.insertWidget(pos, ArgCard(
                    mat, arg, "today", self._on_timer, self._on_done, self._on_ripassa
                )); pos += 1

    def _on_timer(self, mat_nome, arg_nome):
        dlg = TimerDialog(mat_nome, arg_nome, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            so.aggiungi_minuti_studio(so.PKL_FILE, mat_nome, arg_nome, dlg.minuti)
        self.refresh()

    def _on_done(self, mat_nome, arg_nome, scope):
        so.segna_completato(so.PKL_FILE, mat_nome, arg_nome, scope)
        self.refresh()

    def _on_ripassa(self, arg):
        dlg = RandomReviewDialog(arg, self)
        dlg.exec()




class _EnterDateEdit(QDateEdit):
    """QDateEdit che emette confirmed() solo alla pressione di Invio/Return."""
    from PyQt6.QtCore import pyqtSignal as _sig
    confirmed = _sig()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.confirmed.emit()

class CalendarioEditPanel(QWidget):
    """
    Pannello unificato Crea / Modifica calendario.

    Sezione superiore (collassabile):
      • Importa da .txt  → sceglie file, seleziona materie, chiede ripetizioni,
                           AGGIUNGE al pkl esistente (o lo crea)
      • Crea da zero     → stessa cosa ma via dialog interattivi

    Sezione inferiore (sempre visibile):
      Tre colonne Materie | Argomenti | Sottoargomenti sul pkl.
      Ogni modifica è salvata immediatamente.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self._materie = []
        self._setup_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ─────────────────────────────────────────────────────────
        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Calendario", "h1"))
        hlay.addStretch()

        imp_btn = QPushButton("↑  Importa .txt")
        imp_btn.setObjectName("ghostBtn")
        imp_btn.clicked.connect(self._importa)

        hlay.addWidget(imp_btn)
        root.addWidget(hdr)

        # ── Three-column edit area ──────────────────────────────────────────
        body = QWidget()
        body.setObjectName("panel")
        clay = QHBoxLayout(body)
        clay.setContentsMargins(28, 24, 28, 24)
        clay.setSpacing(20)

        # Col 1 — Materie
        c1 = QWidget()
        l1 = QVBoxLayout(c1)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.setSpacing(8)
        l1.addWidget(_lbl("Materie", "h3"))

        self._mat_list = QListWidget()
        self._mat_list.currentRowChanged.connect(self._on_mat)
        self._mat_list.itemDoubleClicked.connect(self._rinomina_materia)
        l1.addWidget(self._mat_list)

        add_m_btn = QPushButton("＋  Aggiungi materia")
        add_m_btn.setObjectName("ghostBtn")
        add_m_btn.setFixedHeight(34)
        add_m_btn.clicked.connect(self._aggiungi_materia)
        l1.addWidget(add_m_btn)

        del_m = QPushButton("Elimina materia")
        del_m.setObjectName("dangerBtn")
        del_m.setFixedHeight(32)
        del_m.clicked.connect(self._elimina_materia)
        l1.addWidget(del_m)

        # Col 2 — Argomenti
        c2 = QWidget()
        l2 = QVBoxLayout(c2)
        l2.setContentsMargins(0, 0, 0, 0)
        l2.setSpacing(8)

        l2.addWidget(_lbl("Argomenti", "h3"))

        self._arg_list = QListWidget()
        self._arg_list.currentRowChanged.connect(self._on_arg)
        self._arg_list.itemDoubleClicked.connect(self._rinomina_argomento)
        l2.addWidget(self._arg_list)

        self._add_arg_btn = QPushButton("＋  Aggiungi argomento")
        self._add_arg_btn.setObjectName("ghostBtn")
        self._add_arg_btn.setFixedHeight(34)
        self._add_arg_btn.setEnabled(False)
        self._add_arg_btn.clicked.connect(self._aggiungi_argomento)
        l2.addWidget(self._add_arg_btn)



        del_a = QPushButton("Elimina argomento")
        del_a.setObjectName("dangerBtn")
        del_a.setFixedHeight(32)
        del_a.clicked.connect(self._elimina_argomento)
        l2.addWidget(del_a)

        # Col 3 — Sottoargomenti
        c3 = QWidget()
        l3 = QVBoxLayout(c3)
        l3.setContentsMargins(0, 0, 0, 0)
        l3.setSpacing(8)

        sh = QHBoxLayout()
        sh.addWidget(_lbl("Sottoargomenti", "h3"))
        sh.addStretch()
        self._sub_count_lbl = _lbl("", "muted")
        sh.addWidget(self._sub_count_lbl)
        l3.addLayout(sh)

        self._sub_list = QListWidget()
        self._sub_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._sub_list.setEnabled(False)
        self._sub_list.model().rowsMoved.connect(self._on_sub_reorder)
        self._sub_list.itemDoubleClicked.connect(self._rinomina_sub)
        l3.addWidget(self._sub_list)

        sub_add_row = QHBoxLayout()
        self._sub_input = QLineEdit()
        self._sub_input.setPlaceholderText("Nuovo sottoargomento…")
        self._sub_input.setEnabled(False)
        self._sub_input.returnPressed.connect(self._aggiungi_sub)
        self._sub_add_btn = QPushButton("Aggiungi")
        self._sub_add_btn.setObjectName("accentBtn")
        self._sub_add_btn.setFixedHeight(36)
        self._sub_add_btn.setEnabled(False)
        self._sub_add_btn.clicked.connect(self._aggiungi_sub)
        sub_add_row.addWidget(self._sub_input)
        sub_add_row.addWidget(self._sub_add_btn)
        l3.addLayout(sub_add_row)

        self._sub_del_btn = QPushButton("Elimina selezionato")
        self._sub_del_btn.setObjectName("dangerBtn")
        self._sub_del_btn.setFixedHeight(32)
        self._sub_del_btn.setEnabled(False)
        self._sub_del_btn.clicked.connect(self._elimina_sub)
        l3.addWidget(self._sub_del_btn)

        clay.addWidget(c1, 1)
        clay.addWidget(c2, 1)
        clay.addWidget(c3, 1)
        root.addWidget(body)

    # ── Refresh ───────────────────────────────────────────────────────────────

    def refresh(self):
        self._materie = []
        self._mat_list.clear()
        self._arg_list.clear()
        self._sub_list.clear()
        self._add_arg_btn.setEnabled(False)
        self._sub_list.setEnabled(False)
        self._sub_input.setEnabled(False)
        self._sub_add_btn.setEnabled(False)
        self._sub_del_btn.setEnabled(False)
        self._sub_count_lbl.setText("")

        try:
            self._materie = so._carica(so.PKL_FILE)
        except FileNotFoundError:
            self._mat_list.addItem("Nessun calendario — usa «Importa .txt» o «Nuova materia»")
            return

        for m in self._materie:
            esame = m.data_esame.strftime('%d/%m/%Y') if m.data_esame else "—"
            self._mat_list.addItem(f"{m.nome.lstrip('#')}   ·   {esame}")

    # ── Column 1: Materie ─────────────────────────────────────────────────────

    def _on_mat(self, row: int):
        self._arg_list.clear()
        self._sub_list.clear()
        self._sub_list.setEnabled(False)
        self._sub_input.setEnabled(False)
        self._sub_add_btn.setEnabled(False)
        self._sub_del_btn.setEnabled(False)
        self._sub_count_lbl.setText("")

        ok = 0 <= row < len(self._materie)
        self._add_arg_btn.setEnabled(ok)
        if not ok:
            return

        mat = self._materie[row]
        for a in mat.argomenti:
            n = len(a.sottoargomenti)
            s = f"  ·  {n} sub" if n else ""
            d = a.data_inizio.strftime('%d/%m/%Y') if a.data_inizio else "—"
            self._arg_list.addItem(f"{a.nome}   ·   da {d}{s}")

    def _aggiungi_materia(self):
        dlg = NuovaMateriaDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        m = so.Materia(dlg.nome, [])
        m.set_data_esame(dlg.data_esame)
        self._materie.append(m)
        esame = m.data_esame.strftime('%d/%m/%Y') if m.data_esame else "—"
        self._mat_list.addItem(f"{m.nome.lstrip('#')}   ·   {esame}")
        self._salva()

    def _elimina_materia(self):
        row = self._mat_list.currentRow()
        if row < 0 or row >= len(self._materie):
            return
        nome = self._materie[row].nome.lstrip('#')
        r = QMessageBox.question(
            self, "Conferma",
            f"Eliminare la materia «{nome}» e tutti i suoi argomenti?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.StandardButton.Yes:
            return
        self._materie.pop(row)
        self._mat_list.takeItem(row)
        self._arg_list.clear()
        self._sub_list.clear()
        self._add_arg_btn.setEnabled(False)
        self._salva()

    # ── Column 2: Argomenti ───────────────────────────────────────────────────

    def _on_arg(self, row: int):
        self._sub_list.clear()
        self._sub_list.setEnabled(False)
        self._sub_input.setEnabled(False)
        self._sub_add_btn.setEnabled(False)
        self._sub_del_btn.setEnabled(False)
        self._sub_count_lbl.setText("")

        mr = self._mat_list.currentRow()
        ok = (0 <= mr < len(self._materie)) and (0 <= row < len(self._materie[mr].argomenti))
        if not ok:
            return

        arg = self._materie[mr].argomenti[row]
        for s in arg.sottoargomenti:
            self._sub_list.addItem(s)
        self._sub_list.setEnabled(True)
        self._sub_input.setEnabled(True)
        self._sub_add_btn.setEnabled(True)
        self._sub_del_btn.setEnabled(True)
        self._sub_count_lbl.setText(f"{len(arg.sottoargomenti)} elementi")

    def _aggiungi_argomento(self):
        mr = self._mat_list.currentRow()
        if mr < 0 or mr >= len(self._materie):
            return
        dlg = NuovoArgomentoDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        rdlg = GeneraCalendarioDialog(self)
        rdlg.setWindowTitle("Ripetizioni per questo argomento")
        if rdlg.exec() != QDialog.DialogCode.Accepted:
            return
        mat = self._materie[mr]
        arg = so.Argomento(dlg.nome)
        arg.set_data_inizio(dlg.data_inizio)
        if mat.data_esame and dlg.data_inizio:
            from datetime import timedelta
            correct_days = {int(n*(n+1)//2) for n in range(rdlg.ripetizioni)}
            total = (mat.data_esame - dlg.data_inizio).days
            for g in range(max(total, 0)):
                if g in correct_days:
                    arg.set_data((dlg.data_inizio + timedelta(days=g)).strftime('%Y-%m-%d'))
        mat.argomenti.append(arg)
        d = dlg.data_inizio.strftime('%d/%m/%Y') if dlg.data_inizio else "—"
        self._arg_list.addItem(f"{arg.nome}   ·   da {d}")
        self._salva()

    def _elimina_argomento(self):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        if mr < 0 or ar < 0:
            return
        args = self._materie[mr].argomenti
        if ar >= len(args):
            return
        r = QMessageBox.question(
            self, "Conferma", f"Eliminare l'argomento «{args[ar].nome}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if r != QMessageBox.StandardButton.Yes:
            return
        args.pop(ar)
        self._arg_list.takeItem(ar)
        self._sub_list.clear()
        self._salva()

    # ── Column 3: Sottoargomenti ──────────────────────────────────────────────

    def _current_arg(self):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        if mr < 0 or ar < 0 or mr >= len(self._materie):
            return None
        args = self._materie[mr].argomenti
        return args[ar] if ar < len(args) else None

    def _aggiungi_sub(self):
        testo = self._sub_input.text().strip()
        if not testo:
            return
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti.append(testo)
        self._sub_list.addItem(testo)
        self._sub_input.clear()
        self._sub_count_lbl.setText(f"{len(arg.sottoargomenti)} elementi")
        self._aggiorna_arg_label()
        self._salva()

    def _elimina_sub(self):
        row = self._sub_list.currentRow()
        if row < 0:
            return
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti.pop(row)
        self._sub_list.takeItem(row)
        self._sub_count_lbl.setText(f"{len(arg.sottoargomenti)} elementi")
        self._aggiorna_arg_label()
        self._salva()

    def _on_sub_reorder(self):
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti = [
            self._sub_list.item(i).text()
            for i in range(self._sub_list.count())
        ]
        self._salva()

    def _aggiorna_arg_label(self):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        if mr < 0 or ar < 0 or mr >= len(self._materie):
            return
        a = self._materie[mr].argomenti[ar]
        n = len(a.sottoargomenti)
        s = f"  ·  {n} sub" if n else ""
        d = a.data_inizio.strftime('%d/%m/%Y') if a.data_inizio else "—"
        self._arg_list.item(ar).setText(f"{a.nome}   ·   da {d}{s}")

    # ── Import from .txt ──────────────────────────────────────────────────────

    def _importa(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona file", os.path.expanduser("~"), "File testo (*.txt)"
        )
        if not path:
            return
        disponibili = so.leggi_materie_disponibili(path)
        if not disponibili:
            QMessageBox.warning(self, "Errore", "Nessuna materia trovata nel file.")
            return
        dlg = SelezionaMaterieDialog(disponibili, self)
        if dlg.exec() != QDialog.DialogCode.Accepted or not dlg.selezionate:
            return
        rdlg = GeneraCalendarioDialog(self)
        if rdlg.exec() != QDialog.DialogCode.Accepted:
            return

        nuove = so.leggi_file_e_crea_lista_materie(path, dlg.selezionate)
        # calcola date
        correct_days = {int(n*(n+1)/2) for n in range(rdlg.ripetizioni)}
        from datetime import timedelta
        for mat in nuove:
            if not mat.data_esame:
                continue
            for arg in mat.argomenti:
                if not arg.data_inizio:
                    continue
                total = (mat.data_esame - arg.data_inizio).days
                for g in range(max(total, 0)):
                    if g in correct_days:
                        arg.set_data((arg.data_inizio + timedelta(days=g)).strftime('%Y-%m-%d'))

        self._materie.extend(nuove)
        self._salva()
        self.refresh()
        QMessageBox.information(self, "Importato", f"{len(nuove)} materie aggiunte al calendario.")


    # ── Dialog modifica unificato ─────────────────────────────────────────────

    def _rinomina_materia(self, item):
        row = self._mat_list.row(item)
        if row < 0 or row >= len(self._materie):
            return
        mat = self._materie[row]

        dlg = QDialog(self)
        dlg.setWindowTitle("Modifica materia")
        dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)

        lay.addWidget(_lbl("Nome", "h3"))
        nome_edit = QLineEdit(mat.nome.lstrip('#'))
        nome_edit.selectAll()
        lay.addWidget(nome_edit)

        lay.addWidget(_lbl("Data esame", "h3"))
        data_edit = QDateEdit()
        data_edit.setCalendarPopup(True)
        data_edit.setDisplayFormat("dd / MM / yyyy")
        if mat.data_esame:
            data_edit.setDate(QDate(mat.data_esame.year, mat.data_esame.month, mat.data_esame.day))
        else:
            data_edit.setDate(QDate.currentDate().addMonths(3))
        lay.addWidget(data_edit)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        nome_edit.returnPressed.connect(dlg.accept)
        lay.addWidget(btns)

        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        nuovo_nome = nome_edit.text().strip()
        if not nuovo_nome:
            return
        mat.nome = f'#{nuovo_nome}' if not nuovo_nome.startswith('#') else nuovo_nome
        qd = data_edit.date()
        mat.data_esame = datetime(qd.year(), qd.month(), qd.day())


        esame = mat.data_esame.strftime('%d/%m/%Y')
        item.setText(f"{mat.nome.lstrip('#')}   ·   {esame}")
        self._salva()

    def _rinomina_argomento(self, item):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.row(item)
        if mr < 0 or ar < 0 or mr >= len(self._materie):
            return
        args = self._materie[mr].argomenti
        if ar >= len(args):
            return
        arg = args[ar]

        dlg = QDialog(self)
        dlg.setWindowTitle("Modifica argomento")
        dlg.setFixedWidth(380)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)

        lay.addWidget(_lbl("Nome", "h3"))
        nome_edit = QLineEdit(arg.nome)
        nome_edit.selectAll()
        lay.addWidget(nome_edit)

        lay.addWidget(_lbl("Data inizio ripasso", "h3"))
        data_edit = QDateEdit()
        data_edit.setCalendarPopup(True)
        data_edit.setDisplayFormat("dd / MM / yyyy")
        if arg.data_inizio:
            data_edit.setDate(QDate(arg.data_inizio.year, arg.data_inizio.month, arg.data_inizio.day))
        else:
            data_edit.setDate(QDate.currentDate())
        lay.addWidget(data_edit)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        nome_edit.returnPressed.connect(dlg.accept)
        lay.addWidget(btns)

        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        nuovo_nome = nome_edit.text().strip()
        if not nuovo_nome:
            return

        nome_cambiato = nuovo_nome != arg.nome
        data_cambiata = (arg.data_inizio is None or
            data_edit.date() != QDate(arg.data_inizio.year, arg.data_inizio.month, arg.data_inizio.day))

        arg.nome = nuovo_nome

        if data_cambiata:
            # Se la data è cambiata chiedi ripetizioni e ricalcola
            rdlg = GeneraCalendarioDialog(self)
            rdlg.setWindowTitle("Ricalcola ripetizioni")
            rdlg._slider.setValue(max(2, min(10, len(arg.date))))
            if rdlg.exec() == QDialog.DialogCode.Accepted:
                from datetime import timedelta
                qd = data_edit.date()
                arg.data_inizio = datetime(qd.year(), qd.month(), qd.day())
                arg.date.clear()
                arg.sessioni_completate.clear()
                mat = self._materie[mr]
                if mat.data_esame and arg.data_inizio:
                    correct_days = {int(n*(n+1)//2) for n in range(rdlg.ripetizioni)}
                    total = (mat.data_esame - arg.data_inizio).days
                    for g in range(max(total, 0)):
                        if g in correct_days:
                            arg.date.append((arg.data_inizio + timedelta(days=g)).strftime('%Y-%m-%d'))

        n = len(arg.sottoargomenti)
        s = f"  ·  {n} sub" if n else ""
        d = arg.data_inizio.strftime('%d/%m/%Y') if arg.data_inizio else "—"
        item.setText(f"{arg.nome}   ·   da {d}{s}")
        self._salva()

    def _rinomina_sub(self, item):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        sr = self._sub_list.row(item)
        if mr < 0 or ar < 0 or sr < 0 or mr >= len(self._materie):
            return
        args = self._materie[mr].argomenti
        if ar >= len(args) or sr >= len(args[ar].sottoargomenti):
            return

        dlg = QDialog(self)
        dlg.setWindowTitle("Modifica sottoargomento")
        dlg.setFixedWidth(360)
        lay = QVBoxLayout(dlg)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)
        lay.addWidget(_lbl("Nome", "h3"))
        edit = QLineEdit(args[ar].sottoargomenti[sr])
        edit.selectAll()
        lay.addWidget(edit)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        edit.returnPressed.connect(dlg.accept)
        lay.addWidget(btns)

        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        nuovo = edit.text().strip()
        if not nuovo:
            return
        args[ar].sottoargomenti[sr] = nuovo
        item.setText(nuovo)
        self._salva()

    def _salva(self):
        so._salva(self._materie)



class CalendarioPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Calendario", "h1"))
        lay.addWidget(hdr)

        self._scroll, self._container, self._clay = _scroll_area()
        self._clay.addStretch()
        lay.addWidget(self._scroll)

    def refresh(self):
        while self._clay.count() > 1:
            item = self._clay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            calendario = self._build_calendario()
        except FileNotFoundError:
            self._clay.insertWidget(0, _empty_state("📅", "Nessun calendario trovato"))
            return

        if not calendario:
            self._clay.insertWidget(0, _empty_state("📅", "Calendario vuoto"))
            return

        today = datetime.now().strftime('%Y-%m-%d')
        for i, data in enumerate(sorted(calendario.keys())):
            card = self._make_day_card(data, calendario[data], today)
            self._clay.insertWidget(i, card)

    def _build_calendario(self) -> dict:
        materie = so._carica(so.PKL_FILE)
        cal: dict = {}
        for mat in materie:
            for arg in mat.argomenti:
                for d in arg.date:
                    cal.setdefault(d, []).append((mat, arg))
        return cal

    def _make_day_card(self, data: str, pairs: list, today: str) -> QFrame:
        is_today = data == today
        is_past = data < today
        card = QFrame()
        card.setObjectName("dayCardToday" if is_today else "dayCard")

        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(6)

        date_row = QHBoxLayout()
        date_lbl = QLabel(data)
        date_lbl.setStyleSheet(
            f"font-weight: 600; color: {_ACCENT if is_today else (_TXT2 if is_past else _TXT1)};"
        )
        date_row.addWidget(date_lbl)
        if is_today:
            badge = QLabel("  oggi  ")
            badge.setStyleSheet(
                f"background: {_ACCENT}; color: #000; border-radius: 4px; "
                f"font-size: 10px; font-weight: 700; padding: 1px 6px;"
            )
            date_row.addWidget(badge)
        date_row.addStretch()
        lay.addLayout(date_row)

        for mat, arg in pairs:
            scaduto = is_past and data not in arg.sessioni_completate
            completato = data in arg.sessioni_completate
            entry = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(
                f"color: {_DANGER if scaduto else (_SUCCESS if completato else _TXT2)}; font-size: 8px;"
            )
            dot.setFixedWidth(14)
            text = QLabel(f"{mat.nome.lstrip('#')}  ·  {arg.nome}")
            text.setStyleSheet(
                f"color: {_DANGER if scaduto else (_TXT2 if completato else _TXT1)}; font-size: 12px;"
            )
            status = QLabel("✓" if completato else ("⚠" if scaduto else ""))
            status.setStyleSheet(f"color: {_SUCCESS if completato else _DANGER};")
            entry.addWidget(dot)
            entry.addWidget(text)
            entry.addStretch()
            entry.addWidget(status)
            lay.addLayout(entry)

        return card


class DateEsamePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Date esami", "h1"))
        lay.addWidget(hdr)

        self._scroll, self._container, self._clay = _scroll_area()
        self._clay.addStretch()
        lay.addWidget(self._scroll)

    def refresh(self):
        while self._clay.count() > 1:
            item = self._clay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            materie = so._carica(so.PKL_FILE)
        except FileNotFoundError:
            self._clay.insertWidget(0, _empty_state("🎓", "Nessun calendario trovato"))
            return

        materie_con_esame = [m for m in materie if m.data_esame]
        materie_con_esame.sort(key=lambda m: m.data_esame)

        for i, mat in enumerate(materie_con_esame):
            giorni = (mat.data_esame - datetime.now()).days
            urgente = 0 <= giorni < 14
            passato = giorni < 0

            card = QFrame()
            card.setObjectName("card")
            card.setFixedHeight(72)
            clay = QHBoxLayout(card)
            clay.setContentsMargins(20, 0, 20, 0)

            name_lbl = QLabel(mat.nome.lstrip('#'))
            name_lbl.setObjectName("h2")
            date_lbl = QLabel(mat.data_esame.strftime('%d %B %Y'))
            date_lbl.setObjectName("muted")
            text_col = QVBoxLayout()
            text_col.setSpacing(3)
            text_col.addStretch()
            text_col.addWidget(name_lbl)
            text_col.addWidget(date_lbl)
            text_col.addStretch()

            if passato:
                count_lbl = QLabel("passato")
                count_lbl.setObjectName("muted")
            else:
                count_lbl = QLabel(str(giorni))
                count_lbl.setStyleSheet(
                    f"font-size: 28px; font-weight: 200; "
                    f"color: {_DANGER if urgente else _ACCENT};"
                )
            days_lbl = QLabel("giorni")
            days_lbl.setObjectName("muted")
            count_col = QVBoxLayout()
            count_col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            count_col.addWidget(count_lbl)
            if not passato:
                count_col.addWidget(days_lbl)

            clay.addLayout(text_col)
            clay.addStretch()
            clay.addLayout(count_col)
            self._clay.insertWidget(i, card)


class StatistichePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Statistiche", "h1"))
        lay.addWidget(hdr)

        self._scroll, self._container, self._clay = _scroll_area()
        self._clay.addStretch()
        lay.addWidget(self._scroll)

    def refresh(self):
        while self._clay.count() > 1:
            item = self._clay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            materie = so._carica(so.PKL_FILE)
        except FileNotFoundError:
            self._clay.insertWidget(0, _empty_state("📊", "Nessun calendario trovato"))
            return

        today = datetime.now().strftime('%Y-%m-%d')
        tot_minuti = sum(a.minuti_studiati for m in materie for a in m.argomenti)

        summary = QFrame()
        summary.setObjectName("card")
        summary.setFixedHeight(80)
        sl = QHBoxLayout(summary)
        sl.setContentsMargins(24, 0, 24, 0)

        for val, lbl in [
            (f"{tot_minuti // 60}h {tot_minuti % 60}m", "Ore di studio"),
            (str(len(materie)), "Materie"),
            (str(sum(len(m.argomenti) for m in materie)), "Argomenti"),
        ]:
            col = QVBoxLayout()
            col.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v = QLabel(val)
            v.setStyleSheet(f"font-size: 22px; font-weight: 600; color: {_ACCENT};")
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l = QLabel(lbl)
            l.setObjectName("muted")
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            col.addWidget(v)
            col.addWidget(l)
            sl.addLayout(col)
            if lbl != "Argomenti":
                divider = QFrame()
                divider.setFrameShape(QFrame.Shape.VLine)
                divider.setStyleSheet(f"color: {_BORDER2};")
                sl.addWidget(divider)

        self._clay.insertWidget(0, summary)

        for i, mat in enumerate(materie):
            tot = sum(len(a.date) for a in mat.argomenti)
            done = sum(len(a.sessioni_completate) for a in mat.argomenti)
            saltate = sum(
                len([d for d in a.date if d < today and d not in a.sessioni_completate])
                for a in mat.argomenti
            )
            minuti = sum(a.minuti_studiati for a in mat.argomenti)
            perc = done / tot if tot else 0
            ore = minuti / 60

            card = QFrame()
            card.setObjectName("card")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 14, 20, 14)
            cl.setSpacing(8)

            name_row = QHBoxLayout()
            name_row.addWidget(_lbl(mat.nome.lstrip('#'), "h3"))
            name_row.addStretch()
            perc_lbl = QLabel(f"{int(perc * 100)}%")
            perc_lbl.setStyleSheet(f"color: {_ACCENT}; font-size: 13px; font-weight: 600;")
            name_row.addWidget(perc_lbl)
            cl.addLayout(name_row)

            pb = QProgressBar()
            pb.setRange(0, 100)
            pb.setValue(int(perc * 100))
            pb.setTextVisible(False)
            pb.setFixedHeight(5)
            if perc > 0.7:
                pb.setStyleSheet("QProgressBar::chunk { background: #81C784; border-radius: 3px; }")
            elif perc < 0.3 and saltate > 0:
                pb.setStyleSheet("QProgressBar::chunk { background: #E57373; border-radius: 3px; }")
            cl.addWidget(pb)

            stats_row = QHBoxLayout()
            for val, lbl in [
                (f"{done}/{tot}", "sessioni"),
                (str(saltate), "saltate"),
                (f"{ore:.1f}h", "studio"),
            ]:
                mini = QVBoxLayout()
                mini.setSpacing(1)
                v = QLabel(val)
                v.setStyleSheet(
                    f"font-size: 13px; font-weight: 600; "
                    f"color: {_DANGER if lbl == 'saltate' and saltate > 0 else _TXT1};"
                )
                l = QLabel(lbl)
                l.setObjectName("muted")
                mini.addWidget(v)
                mini.addWidget(l)
                stats_row.addLayout(mini)
                if lbl != "studio":
                    stats_row.addStretch()
            cl.addLayout(stats_row)
            self._clay.insertWidget(i + 1, card)

class SottoargomentiPklPanel(QWidget):
    """
    Gestisce i sottoargomenti direttamente sul .pkl esistente.
    Funziona indipendentemente dalla bozza in MateriePanel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self._materie = []
        self._setup_ui()

    def _setup_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Sottoargomenti", "h1"))
        hlay.addStretch()
        hint = _lbl("Le modifiche vengono salvate immediatamente.", "muted")
        hlay.addWidget(hint)
        lay.addWidget(hdr)

        # Two-column layout: materie+argomenti | sottoargomenti
        content = QWidget()
        content.setObjectName("panel")
        clay = QHBoxLayout(content)
        clay.setContentsMargins(28, 24, 28, 24)
        clay.setSpacing(20)

        # ── Left: materie ──
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(10)
        ll.addWidget(_lbl("Materia", "h3"))
        self._mat_list = QListWidget()
        self._mat_list.currentRowChanged.connect(self._on_mat)
        ll.addWidget(self._mat_list)

        # ── Center: argomenti ──
        center = QWidget()
        cl = QVBoxLayout(center)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(10)
        cl.addWidget(_lbl("Argomento", "h3"))
        self._arg_list = QListWidget()
        self._arg_list.currentRowChanged.connect(self._on_arg)
        cl.addWidget(self._arg_list)

        # ── Right: sottoargomenti (editable) ──
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(10)

        sub_hdr = QHBoxLayout()
        sub_hdr.addWidget(_lbl("Sottoargomenti", "h3"))
        sub_hdr.addStretch()
        self._sub_count = _lbl("", "muted")
        sub_hdr.addWidget(self._sub_count)
        rl.addLayout(sub_hdr)

        self._sub_list = QListWidget()
        self._sub_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._sub_list.setEnabled(False)
        self._sub_list.model().rowsMoved.connect(self._on_reorder)
        rl.addWidget(self._sub_list)

        # Add row
        add_row = QHBoxLayout()
        self._sub_input = QLineEdit()
        self._sub_input.setPlaceholderText("Nuovo sottoargomento…")
        self._sub_input.setEnabled(False)
        self._sub_input.returnPressed.connect(self._aggiungi_sub)
        self._add_sub_btn = QPushButton("Aggiungi")
        self._add_sub_btn.setObjectName("accentBtn")
        self._add_sub_btn.setFixedHeight(36)
        self._add_sub_btn.setEnabled(False)
        self._add_sub_btn.clicked.connect(self._aggiungi_sub)
        add_row.addWidget(self._sub_input)
        add_row.addWidget(self._add_sub_btn)
        rl.addLayout(add_row)

        self._del_sub_btn = QPushButton("Elimina selezionato")
        self._del_sub_btn.setObjectName("dangerBtn")
        self._del_sub_btn.setFixedHeight(32)
        self._del_sub_btn.setEnabled(False)
        self._del_sub_btn.clicked.connect(self._elimina_sub)
        rl.addWidget(self._del_sub_btn)

        clay.addWidget(left, 1)
        clay.addWidget(center, 1)
        clay.addWidget(right, 1)
        lay.addWidget(content)

    # ── Refresh ──────────────────────────────────────────────────────────────

    def refresh(self):
        try:
            self._materie = so._carica(so.PKL_FILE)
        except FileNotFoundError:
            self._materie = []

        self._mat_list.clear()
        self._arg_list.clear()
        self._sub_list.clear()
        self._sub_list.setEnabled(False)
        self._sub_input.setEnabled(False)
        self._add_sub_btn.setEnabled(False)
        self._del_sub_btn.setEnabled(False)
        self._sub_count.setText("")

        if not self._materie:
            self._mat_list.addItem("Nessun calendario trovato")
            return

        for m in self._materie:
            self._mat_list.addItem(m.nome.lstrip("#"))

    # ── Selection handlers ────────────────────────────────────────────────────

    def _on_mat(self, row: int):
        self._arg_list.clear()
        self._sub_list.clear()
        self._sub_list.setEnabled(False)
        self._sub_input.setEnabled(False)
        self._add_sub_btn.setEnabled(False)
        self._del_sub_btn.setEnabled(False)
        self._sub_count.setText("")
        if row < 0 or row >= len(self._materie):
            return
        for a in self._materie[row].argomenti:
            n = len(a.sottoargomenti)
            suffix = f"  ·  {n} sub" if n else ""
            self._arg_list.addItem(f"{a.nome}{suffix}")

    def _on_arg(self, row: int):
        mat_row = self._mat_list.currentRow()
        self._sub_list.clear()
        if mat_row < 0 or row < 0 or mat_row >= len(self._materie):
            return
        args = self._materie[mat_row].argomenti
        if row >= len(args):
            return
        arg = args[row]
        for s in arg.sottoargomenti:
            self._sub_list.addItem(s)
        enabled = True
        self._sub_list.setEnabled(enabled)
        self._sub_input.setEnabled(enabled)
        self._add_sub_btn.setEnabled(enabled)
        self._del_sub_btn.setEnabled(enabled)
        self._sub_count.setText(f"{len(arg.sottoargomenti)} elementi")

    # ── Edit actions ──────────────────────────────────────────────────────────

    def _current_arg(self):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        if mr < 0 or ar < 0 or mr >= len(self._materie):
            return None
        args = self._materie[mr].argomenti
        return args[ar] if ar < len(args) else None

    def _aggiungi_sub(self):
        testo = self._sub_input.text().strip()
        if not testo:
            return
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti.append(testo)
        self._sub_list.addItem(testo)
        self._sub_input.clear()
        self._sub_count.setText(f"{len(arg.sottoargomenti)} elementi")
        self._salva()
        # Aggiorna la label nell'arg_list
        self._aggiorna_arg_label()

    def _elimina_sub(self):
        row = self._sub_list.currentRow()
        if row < 0:
            return
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti.pop(row)
        self._sub_list.takeItem(row)
        self._sub_count.setText(f"{len(arg.sottoargomenti)} elementi")
        self._salva()
        self._aggiorna_arg_label()

    def _on_reorder(self):
        """Sincronizza l'ordine della QListWidget con il modello dopo drag-and-drop."""
        arg = self._current_arg()
        if arg is None:
            return
        arg.sottoargomenti = [
            self._sub_list.item(i).text()
            for i in range(self._sub_list.count())
        ]
        self._salva()

    def _aggiorna_arg_label(self):
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        if mr < 0 or ar < 0 or mr >= len(self._materie):
            return
        arg = self._materie[mr].argomenti[ar]
        n = len(arg.sottoargomenti)
        suffix = f"  ·  {n} sub" if n else ""
        self._arg_list.item(ar).setText(f"{arg.nome}{suffix}")

    def _salva(self):
        so._salva(self._materie)


RECORDINGS_DIR = Path(__file__).parent / "recordings"


def _sanitize(s: str) -> str:
    """Rende una stringa sicura per un nome file."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in s).strip("_")[:40]


class RegistrazioniPanel(QWidget):
    """
    Registra la voce mentre ripeti un sottoargomento.
    Struttura: Materia → Argomento → Sottoargomento → lista registrazioni.
    File salvati in recordings/<mat>/<arg>/<sub>/<timestamp>.wav
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self._materie = []
        self._recording = False
        self._playing = False
        self._current_file: Path | None = None

        # ── QtMultimedia ──────────────────────────────────────────────────
        try:
            from PyQt6.QtMultimedia import (
                QMediaRecorder, QMediaCaptureSession,
                QAudioInput, QMediaPlayer, QAudioOutput,
            )
            self._session  = QMediaCaptureSession()
            self._ai       = QAudioInput()
            self._session.setAudioInput(self._ai)
            self._recorder = QMediaRecorder()
            self._session.setRecorder(self._recorder)
            self._recorder.recorderStateChanged.connect(self._on_recorder_state)

            self._player  = QMediaPlayer()
            self._aout    = QAudioOutput()
            self._player.setAudioOutput(self._aout)
            self._aout.setVolume(1.0)
            self._player.playbackStateChanged.connect(self._on_player_state)
            self._multimedia_ok = True
        except Exception as e:
            self._multimedia_ok = False
            self._mm_error = str(e)

        self._setup_ui()

    # ── UI ────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(70)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(28, 0, 28, 0)
        hlay.addWidget(_lbl("Registrazioni", "h1"))
        hlay.addStretch()
        hlay.addWidget(_lbl("Registra mentre ripeti un sottoargomento.", "muted"))
        root.addWidget(hdr)

        if not self._multimedia_ok:
            root.addWidget(_empty_state(
                "⚠️", "QtMultimedia non disponibile",
                f"Installa PyQt6 con supporto multimedia.\n{getattr(self, '_mm_error', '')}"
            ))
            return

        # Body: 4 columns
        body = QWidget()
        body.setObjectName("panel")
        clay = QHBoxLayout(body)
        clay.setContentsMargins(28, 24, 28, 24)
        clay.setSpacing(16)

        # Col 1 — Materie
        c1 = QWidget()
        l1 = QVBoxLayout(c1)
        l1.setContentsMargins(0, 0, 0, 0)
        l1.setSpacing(6)
        l1.addWidget(_lbl("Materia", "h3"))
        self._mat_list = QListWidget()
        self._mat_list.currentRowChanged.connect(self._on_mat)
        l1.addWidget(self._mat_list)

        # Col 2 — Argomenti
        c2 = QWidget()
        l2 = QVBoxLayout(c2)
        l2.setContentsMargins(0, 0, 0, 0)
        l2.setSpacing(6)
        l2.addWidget(_lbl("Argomento", "h3"))
        self._arg_list = QListWidget()
        self._arg_list.currentRowChanged.connect(self._on_arg)
        l2.addWidget(self._arg_list)

        # Col 3 — Sottoargomenti
        c3 = QWidget()
        l3 = QVBoxLayout(c3)
        l3.setContentsMargins(0, 0, 0, 0)
        l3.setSpacing(6)
        l3.addWidget(_lbl("Sottoargomento", "h3"))
        self._sub_list = QListWidget()
        self._sub_list.currentRowChanged.connect(self._on_sub)
        l3.addWidget(self._sub_list)

        # Col 4 — Registrazioni + controlli
        c4 = QWidget()
        l4 = QVBoxLayout(c4)
        l4.setContentsMargins(0, 0, 0, 0)
        l4.setSpacing(8)

        rec_hdr = QHBoxLayout()
        rec_hdr.addWidget(_lbl("Registrazioni", "h3"))
        rec_hdr.addStretch()
        self._rec_count = _lbl("", "muted")
        rec_hdr.addWidget(self._rec_count)
        l4.addLayout(rec_hdr)

        self._rec_list = QListWidget()
        self._rec_list.currentRowChanged.connect(self._on_rec_sel)
        l4.addWidget(self._rec_list)

        # Record button (big, toggles)
        self._rec_btn = QPushButton("⏺   Registra")
        self._rec_btn.setObjectName("accentBtn")
        self._rec_btn.setFixedHeight(44)
        self._rec_btn.setEnabled(False)
        self._rec_btn.clicked.connect(self._toggle_rec)
        l4.addWidget(self._rec_btn)

        # Timer label during recording
        self._rec_timer_lbl = QLabel("")
        self._rec_timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._rec_timer_lbl.setStyleSheet(f"color: {_DANGER}; font-size: 13px;")
        l4.addWidget(self._rec_timer_lbl)

        # Playback controls
        pb_row = QHBoxLayout()
        self._play_btn = QPushButton("▶  Ascolta")
        self._play_btn.setObjectName("ghostBtn")
        self._play_btn.setFixedHeight(36)
        self._play_btn.setEnabled(False)
        self._play_btn.clicked.connect(self._toggle_play)

        self._del_btn = QPushButton("🗑")
        self._del_btn.setObjectName("dangerBtn")
        self._del_btn.setFixedHeight(36)
        self._del_btn.setFixedWidth(44)
        self._del_btn.setEnabled(False)
        self._del_btn.clicked.connect(self._elimina_rec)

        pb_row.addWidget(self._play_btn)
        pb_row.addWidget(self._del_btn)
        l4.addLayout(pb_row)

        clay.addWidget(c1, 1)
        clay.addWidget(c2, 1)
        clay.addWidget(c3, 1)
        clay.addWidget(c4, 1)
        root.addWidget(body)

        # Internal timer for recording elapsed time
        self._elapsed_timer = QTimer(self)
        self._elapsed_timer.setInterval(1000)
        self._elapsed_timer.timeout.connect(self._tick_rec)
        self._rec_elapsed = 0

    # ── Refresh ───────────────────────────────────────────────────────────

    def refresh(self):
        self._mat_list.clear()
        self._arg_list.clear()
        self._sub_list.clear()
        self._rec_list.clear()
        self._rec_btn.setEnabled(False)
        self._play_btn.setEnabled(False)
        self._del_btn.setEnabled(False)
        self._rec_count.setText("")

        try:
            self._materie = so._carica(so.PKL_FILE)
        except FileNotFoundError:
            self._materie = []
            self._mat_list.addItem("Nessun calendario trovato")
            return

        for m in self._materie:
            self._mat_list.addItem(m.nome.lstrip("#"))

    # ── Selection cascade ─────────────────────────────────────────────────

    def _on_mat(self, row: int):
        self._arg_list.clear()
        self._sub_list.clear()
        self._rec_list.clear()
        self._rec_btn.setEnabled(False)
        self._play_btn.setEnabled(False)
        self._del_btn.setEnabled(False)
        self._rec_count.setText("")
        if row < 0 or row >= len(self._materie):
            return
        for a in self._materie[row].argomenti:
            self._arg_list.addItem(a.nome)

    def _on_arg(self, row: int):
        self._sub_list.clear()
        self._rec_list.clear()
        self._rec_btn.setEnabled(False)
        self._play_btn.setEnabled(False)
        self._del_btn.setEnabled(False)
        self._rec_count.setText("")
        mr = self._mat_list.currentRow()
        if mr < 0 or row < 0 or mr >= len(self._materie):
            return
        args = self._materie[mr].argomenti
        if row >= len(args):
            return
        for s in args[row].sottoargomenti:
            self._sub_list.addItem(s)

    def _on_sub(self, row: int):
        self._rec_list.clear()
        self._play_btn.setEnabled(False)
        self._del_btn.setEnabled(False)
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        ok = (0 <= mr < len(self._materie)
              and 0 <= ar < len(self._materie[mr].argomenti)
              and row >= 0)
        self._rec_btn.setEnabled(ok)
        self._rec_count.setText("")
        if not ok:
            return
        self._carica_registrazioni()

    # ── Recording path helpers ────────────────────────────────────────────

    def _rec_dir(self) -> Path | None:
        mr = self._mat_list.currentRow()
        ar = self._arg_list.currentRow()
        sr = self._sub_list.currentRow()
        if mr < 0 or ar < 0 or sr < 0:
            return None
        mat = self._materie[mr]
        arg = mat.argomenti[ar]
        sub = arg.sottoargomenti[sr]
        path = RECORDINGS_DIR / _sanitize(mat.nome) / _sanitize(arg.nome) / _sanitize(sub)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _carica_registrazioni(self):
        d = self._rec_dir()
        if d is None:
            return
        files = sorted([f for f in d.iterdir() if f.suffix in (".m4a", ".wav")], reverse=True)
        self._rec_list.clear()
        for f in files:
            # Filename: YYYYMMDD_HHMMSS.wav → label leggibile
            try:
                ts = datetime.strptime(f.stem, "%Y%m%d_%H%M%S")
                label = ts.strftime("%d %b %Y  %H:%M:%S")
            except ValueError:
                label = f.stem
            self._rec_list.addItem(label)
        self._rec_count.setText(f"{len(files)} registrazioni")
        self._play_btn.setEnabled(False)
        self._del_btn.setEnabled(False)

    def _rec_files(self) -> list[Path]:
        d = self._rec_dir()
        if d is None:
            return []
        return sorted([f for f in d.iterdir() if f.suffix in (".wav", ".m4a")], reverse=True)

    # ── Record ────────────────────────────────────────────────────────────

    def _toggle_rec(self):
        if not self._recording:
            self._start_rec()
        else:
            self._stop_rec()

    def _start_rec(self):
        from PyQt6.QtCore import QUrl
        from PyQt6.QtMultimedia import QMediaFormat

        d = self._rec_dir()
        if d is None:
            return

        # FFmpeg su Linux usa Mpeg4Audio/AAC — lo impostiamo esplicitamente
        fmt = QMediaFormat()
        fmt.setFileFormat(QMediaFormat.FileFormat.Mpeg4Audio)
        fmt.setAudioCodec(QMediaFormat.AudioCodec.AAC)
        self._recorder.setMediaFormat(fmt)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._current_file = d / f"{ts}.m4a"

        self._recorder.setOutputLocation(QUrl.fromLocalFile(str(self._current_file)))
        self._recorder.record()

    def _stop_rec(self):
        self._recorder.stop()

    def _on_recorder_state(self, state):
        from PyQt6.QtMultimedia import QMediaRecorder
        if state == QMediaRecorder.RecorderState.RecordingState:
            self._recording = True
            self._rec_elapsed = 0
            self._elapsed_timer.start()
            self._rec_btn.setText("⏹   Ferma")
            self._rec_btn.setStyleSheet(f"background: {_DANGER}; color: #fff; border: none; border-radius: 6px; padding: 9px 18px; font-weight: 700;")
        else:
            self._recording = False
            self._elapsed_timer.stop()
            self._rec_timer_lbl.setText("  ✓ Salvataggio in corso…")
            self._rec_btn.setText("⏺   Registra")
            self._rec_btn.setStyleSheet("")
            # FFmpeg finalizza il file in modo asincrono — aspettiamo 900ms
            QTimer.singleShot(900, self._dopo_stop)

    def _dopo_stop(self):
        self._rec_timer_lbl.setText("")
        self._carica_registrazioni()
        if self._rec_list.count() > 0:
            self._rec_list.setCurrentRow(0)

    def _tick_rec(self):
        self._rec_elapsed += 1
        m, s = divmod(self._rec_elapsed, 60)
        self._rec_timer_lbl.setText(f"⏺  {m:02d}:{s:02d}  in registrazione…")

    # ── Playback ──────────────────────────────────────────────────────────

    def _on_rec_sel(self, row: int):
        self._player.stop()
        self._play_btn.setEnabled(row >= 0)
        self._del_btn.setEnabled(row >= 0)
        self._play_btn.setText("▶  Ascolta")

    def _toggle_play(self):
        if self._playing:
            self._player.stop()
        else:
            files = self._rec_files()
            row = self._rec_list.currentRow()
            if row < 0 or row >= len(files):
                return
            from PyQt6.QtCore import QUrl
            self._player.setSource(QUrl.fromLocalFile(str(files[row])))
            self._player.play()

    def _on_player_state(self, state):
        from PyQt6.QtMultimedia import QMediaPlayer
        self._playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        self._play_btn.setText("⏹  Ferma" if self._playing else "▶  Ascolta")

    # ── Delete ────────────────────────────────────────────────────────────

    def _elimina_rec(self):
        row = self._rec_list.currentRow()
        files = self._rec_files()
        if row < 0 or row >= len(files):
            return
        f = files[row]
        r = QMessageBox.question(
            self, "Elimina registrazione",
            f"Eliminare la registrazione del {self._rec_list.item(row).text()}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if r != QMessageBox.StandardButton.Yes:
            return
        self._player.stop()
        f.unlink(missing_ok=True)
        self._carica_registrazioni()

class Sidebar(QWidget):
    page_changed = __import__('PyQt6.QtCore', fromlist=['pyqtSignal']).pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(_SW)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        title = QLabel("STUDY\nORGANIZER")
        title.setObjectName("appTitle")
        sub = QLabel("study companion")
        sub.setObjectName("appSub")
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addWidget(_sep())

        self._btns: list[QPushButton] = []
        items = [
            ("📅  Sessione di oggi", 0),
            ("📚  Crea / Modifica",  1),
            ("🗓  Calendario",       2),
            ("🎓  Date esami",       3),
            ("📊  Statistiche",      4),
            ("🎙  Registrazioni",    5),
        ]
        for label, idx in items:
            btn = QPushButton(label)
            btn.setObjectName("navBtn")
            btn.setFixedHeight(44)
            btn.clicked.connect(lambda _, i=idx: self._select(i))
            lay.addWidget(btn)
            self._btns.append(btn)

        lay.addStretch()
        self._select(0)

    def _select(self, idx: int):
        for i, btn in enumerate(self._btns):
            btn.setProperty("active", i == idx)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self.page_changed.emit(idx)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ═══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Organizer")
        self.setMinimumSize(960, 620)
        self.resize(1100, 680)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._sidebar = Sidebar()
        root.addWidget(self._sidebar)

        self._stack = QStackedWidget()
        self._stack.setObjectName("panel")
        root.addWidget(self._stack)

        self._panels = [
            OggiPanel(),
            CalendarioEditPanel(),
            CalendarioPanel(),
            DateEsamePanel(),
            StatistichePanel(),
            RegistrazioniPanel(),
        ]
        for p in self._panels:
            self._stack.addWidget(p)

        self._sidebar.page_changed.connect(self._switch)
        self._switch(0)

    def _switch(self, idx: int):
        self._stack.setCurrentIndex(idx)
        self._panels[idx].refresh()


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    app.setFont(QFont("Helvetica Neue", 13))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
