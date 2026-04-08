<p align="center">
  <img src="assets/icon.svg" alt="Study Organizer" width="140"/>
</p>

<h1 align="center">Study Organizer — Terminal Interface</h1>

<p align="center">
  A terminal-based study planner with spaced repetition, written in Python.
</p>

> **Branch note:** this is the `terminal_interface` branch. For the PyQt6 desktop GUI version, check out the `main` branch.

A lightweight CLI for planning, tracking, and reviewing university study sessions. It generates spaced-repetition calendars from a plain-text list of subjects and exam dates, shows you what to study each day, and tracks how long you spend on each topic — all from the terminal, with an interactive arrow-key interface powered by [questionary](https://github.com/tmbo/questionary).

## Features

- **Today's session** — interactive list of topics to review today, plus any sessions you skipped on previous days.
- **Spaced-repetition calendar generator** — reads a plain-text file of subjects and exam dates, and distributes each topic across a configurable number of review sessions before the exam.
- **Built-in study timer** — a stopwatch you start on any topic; time is saved to the topic's study history on `Ctrl+C`.
- **Mark as done** — close out a session without the timer when you've studied elsewhere.
- **Exam dates overview** — print upcoming exams and their countdown.
- **Statistics** — total minutes studied per subject and per topic.
- **Calendar view** — a full tabular view of the generated plan, printable to a `.txt` file.
- **Persistent storage** — all data is serialized to a single `binary_output.pkl`, so sessions resume exactly where you left off.

## Requirements

- Python **3.10+** (the core module uses PEP 604 union types like `datetime | None`)
- See `requirements.txt`:
  - `questionary` — interactive terminal prompts
  - `tabulate` — pretty tables

Works on Linux, macOS, and Windows (any terminal with ANSI-color support).

## Installation

```bash
git clone -b terminal_interface https://github.com/<your-username>/study-organizer.git
cd study-organizer

python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Launch the app:

```bash
python run.py
```

You'll get an interactive menu:

```
  Cosa vuoi fare?
  ❯   Sessione di oggi
      Crea nuovo calendario
      Date esami
      Statistiche
      Calendario
      Help
      ─────────────
      Esci
```

### Input file format

To create a new calendar, you need a plain-text file listing your subjects, exam dates, and topics. The format is:

```
#SubjectName YYYY MM DD        ← exam date
TopicName1 YYYY MM DD          ← topic start date
TopicName2 YYYY MM DD
...

#AnotherSubject YYYY MM DD
TopicA YYYY MM DD
TopicB YYYY MM DD
```

Example:

```
#Fisica 2026 6 15
Cinematica     2026 3 1
Dinamica       2026 3 5
Termodinamica  2026 3 10

#Analisi 2026 7 1
Limiti         2026 3 1
Derivate       2026 3 8
```

Lines starting with `#` declare a subject and its exam date; the lines that follow list the topics for that subject and the date you want to start reviewing each one. From this, the tool generates a spaced-repetition schedule aiming for a configurable number of review sessions per topic before the exam.

### Typical workflow

1. Write a `.txt` file as above.
2. Launch `run.py` and choose **Crea nuovo calendario** — pick the subjects to include and the target number of repetitions per topic.
3. Every day, open **Sessione di oggi** to see what to review. Pick a topic, start the timer or mark it as done.
4. Check **Statistiche** or **Date esami** whenever you want an overview.

The pickle file is portable — you can copy it between machines to sync your study plan.

## Project structure

```
.
├── run.py                # Terminal interface (questionary-based)
├── study_organizer.py    # Core data model, scheduler, persistence
├── requirements.txt
├── README.md
├── LICENSE
└── binary_output.pkl     # Created at runtime (your study data)
```

## Notes

- The UI labels and help text are in Italian — this reflects the original version of the tool. The core module's public API (`Materia`, `Argomento`, `sessione_di_oggi`, `ripetizione_spaziata`, …) is also Italian-named.
- Data is persisted via `pickle`, so do not load `.pkl` files from untrusted sources.
- The `binary_output.pkl` file produced by this branch is compatible with the PyQt6 GUI version on the `main` branch — you can switch between interfaces on the same data.

## License

Copyright (C) 2026 Angelo

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

See `LICENSE` for the full text.
