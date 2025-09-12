from __future__ import annotations

import platform
import subprocess


def send_notification(title: str, body: str) -> None:
    """Send a desktop notification.

    The implementation is platform specific:
    - Windows uses :mod:`win10toast`.
    - macOS uses ``osascript``.
    - Linux tries the ``notify-send`` command.

    If sending the notification fails for any reason the title and body are
    printed to stdout as a fallback.
    """
    system = platform.system()

    try:
        if system == "Windows":
            from win10toast import ToastNotifier  # type: ignore

            notifier = ToastNotifier()
            notifier.show_toast(title, body, threaded=True)
        elif system == "Darwin":
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'display notification "{body}" with title "{title}"',
                ],
                check=True,
            )
        elif system == "Linux":
            subprocess.run(["notify-send", title, body], check=True)
        else:
            raise OSError("Unsupported platform")
    except Exception:
        print(f"{title}: {body}")


if __name__ == "__main__":
    send_notification("AATOM", "Hydrate yourself!")
