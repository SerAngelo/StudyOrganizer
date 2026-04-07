# Study Organizer

A desktop application for planning, tracking, and reviewing university study sessions, built with **PyQt6**. It combines a spaced-repetition scheduler, a study timer, exam-date tracking, statistics, a random subtopic reviewer, and an audio note recorder — all in a single dark-themed sidebar interface.

The project consists of two layers:

- **`study_organizer.py`** — a pure-Python core module defining the data model (`Materia`, `Argomento`) and the persistence layer (pickle-based), independent of any GUI.
- **`app.py`** — a PyQt6 desktop frontend built on top of the core module, with a sidebar navigation and stacked panels.

## Features

- **Today panel** — shows the topics scheduled for the current day, with one-click session completion and an integrated study timer.
- **Calendar generator** — automatically distributes topics across the days leading up to each exam, supporting both even spacing and spaced-repetition style scheduling.
- **Calendar editor** — drag, edit, and reorganize the generated study plan by hand.
- **Exam dates manager** — keep track of upcoming exams and their countdown.
- **Statistics panel** — total minutes studied per subject, completion rates, and progress bars.
- **Random subtopic review** — pick a random subtopic from any subject to test recall, with a dedicated dialog for managing the subtopic lists.
- **Audio recordings panel** — record, play back, and organize voice notes per subject (uses `PyQt6.QtMultimedia`).
- **Persistent storage** — all data is serialized to a single `binary_output.pkl` file, so sessions resume exactly where you left off.
- **Dark theme** — a custom Qt stylesheet with a consistent palette across every panel and dialog.

## Requirements

- Python **3.10+** (the core module uses PEP 604 union types like `datetime | None`)
- See `requirements.txt`:
  - `PyQt6` (including the `QtMultimedia` module for the recordings panel)
  - `tabulate`

On most Linux distributions PyQt6 ships with multimedia support out of the box. If recording does not work, make sure the GStreamer plugins are installed (e.g. on Arch: `gst-plugins-base`, `gst-plugins-good`, `gst-plugins-bad`).

## Installation

```bash
git clone https://github.com/<your-username>/study-organizer.git
cd study-organizer

python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Launch the desktop app:

```bash
python app.py
```

On first launch the app creates an empty `binary_output.pkl` in the working directory. From there you can:

1. Add one or more **subjects** (`Materie`) and assign each an exam date.
2. Add **topics** (`Argomenti`) under each subject, optionally with subtopics.
3. Open **Generate Calendar** to distribute the topics across the days before the exam.
4. Use the **Today** panel each day to mark sessions as done and run the timer.
5. Review your progress in **Statistics**, or do quick recall checks via **Random Review**.

The pickle file is portable — you can copy it between machines to sync your study plan.

## Project structure

```
.
├── app.py                # PyQt6 desktop frontend
├── study_organizer.py    # Core data model and persistence
├── requirements.txt
├── README.md
└── binary_output.pkl     # Created at runtime (your study data)
```

## Notes

- The core module (`study_organizer.py`) was originally written as a CLI tool and is still usable independently of the GUI; it can be imported into scripts or notebooks for batch operations on the data.
- Comments and some method names in the core module are in Italian (`Materia`, `Argomento`, `data_esame`, …) — this is intentional and reflects the original CLI version. The GUI labels are also in Italian.
- Data is persisted via `pickle`, so do not load `.pkl` files from untrusted sources.

## License


Copyright (C) 2026 Angelo Serrecchia

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

See `LICENSE` for the full text.
