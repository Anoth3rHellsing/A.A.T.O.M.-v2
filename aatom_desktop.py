+33
-0

"""Entry point for the A.A.T.O.M. desktop assistant.

This module launches the minimal system tray application defined in
``tray_app.py``. It exposes a ``main`` function so the app can be executed via
``python -m aatom_desktop`` and packaged with PyInstaller.
"""

import pystray

from tray_app import (
    create_image,
    on_open_chat,
    on_pause_ai,
    on_settings,
    on_exit,
)


def main() -> None:
    """Start the system tray icon."""
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("Open Chat", on_open_chat),
        pystray.MenuItem("Pause AI", on_pause_ai),
        pystray.MenuItem("Settings", on_settings),
        pystray.MenuItem("Exit", on_exit),
    )
    icon = pystray.Icon("aatom", image, "A.A.T.O.M.", menu)
    icon.run()


if __name__ == "__main__":  # pragma: no cover - manual launch
    main()
aatom_desktop.spec
