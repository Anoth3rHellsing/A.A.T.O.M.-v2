# A.A.T.O.M.-v2

A.A.T.O.M.-v2 is an experimental desktop assistant that combines a floating chat
interface, a plugin system, memory embeddings, and proactive background tasks.
It is built with Python and designed to be extensible so you can script new
behaviours with simple Python modules.

## Features

- **Chat overlay** powered by [PySide6](https://www.qt.io/qt-for-python) for a
  compact on-screen conversation window.
- **OpenAI chat engine** with automatic rate‑limit retries and pluggable model
  support.
- **Memory manager** built on [FAISS](https://github.com/facebookresearch/faiss)
  and OpenAI embeddings for semantic search.
- **Plugin loader** that discovers and executes Python plugins placed in the
  `plugins/` directory.
- **Screen capture + OCR** using Pillow and Tesseract via `pytesseract`.
- **Cross‑platform notifications** (Windows, macOS, Linux).
- **System tray application** for quick actions and status control.
- **Proactive loop** for periodic background callbacks such as hydration
  reminders.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-user>/A.A.T.O.M.-v2.git
   cd A.A.T.O.M.-v2
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   Install the libraries used across the modules:

   ```bash
   pip install openai faiss-cpu numpy pillow pytesseract PySide6 pystray
   ```

   - On Windows, install `win10toast` for notifications:

     ```bash
     pip install win10toast
     ```

   - For OCR support install [Tesseract OCR](https://tesseract-ocr.github.io/)
     and ensure the `tesseract` binary is available in your `PATH`.

4. **Set environment variables**

   - `OPENAI_API_KEY` – required for chat and embedding features.
   - `TESSDATA_PREFIX` – optional; points to the Tesseract language data
     directory if not using the default installation path.

## Usage

Each module can be run independently during development, or you can integrate
them into a larger desktop application.

### Chat overlay

```bash
python chat_overlay.py
```

Type a message and press *Send* to see it echo in the floating window. In a full
application you would connect `ChatOverlay.message_sent` to your chat backend.

### OpenAI chat engine

```python
from openai_chat_engine import OpenAIChatEngine

engine = OpenAIChatEngine(api_key="YOUR_API_KEY")
response = await engine.chat([{"role": "user", "content": "Hello"}])
```

The engine automatically retries rate‑limited requests up to three times.

### Memory manager

```python
from memory import MemoryManager

mem = MemoryManager("./memory_store")
mem.add("Remember the milk", {"source": "note"})
print(mem.search("milk"))
```

Entries are embedded with OpenAI and stored in a local FAISS index for fast
semantic search.

### Plugins

Drop Python files in the `plugins/` directory and implement the following
attributes:

```python
NAME = "My Plugin"
DESCRIPTION = "Does something useful"

async def execute(**kwargs):
    ...
```

Plugins are automatically discovered and can be invoked with
`PluginLoader.run("My Plugin")`.

### Screen capture and OCR

```bash
python capture_ocr.py
```

Captures the screen (or region) and prints recognized Spanish/English text using
Tesseract.

### Notifications

Use `notification.send_notification("Title", "Body")` for cross‑platform toast
messages. On unsupported systems the message is printed to stdout.

### Proactive loop

```python
from proactive_loop import start_proactive_loop, hydration_reminder

loop = start_proactive_loop([hydration_reminder])
# loop.pause() and loop.resume() control execution
```

### System tray app

```bash
python tray_app.py
```

Creates a minimal tray icon with menu actions such as "Open Chat" and "Exit".

### Windows convenience scripts

- **run_aatom.bat** – sets up a virtual environment (if missing), installs
  dependencies from `requirements.txt`, and runs `python -m aatom_desktop`.
- **update_aatom.bat** – pulls the latest changes from `main` and invokes
  `run_aatom.bat`.

## Building a binary

A `PyInstaller` spec file is included for packaging the project:

```bash
pyinstaller aatom_desktop.spec
```

## Contributing

Feel free to fork the repository and submit pull requests. Issues and feature
requests are welcome!

## License

Distributed under the MIT License. See `LICENSE` for more information.

