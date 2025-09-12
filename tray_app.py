from PIL import Image, ImageDraw
import pystray


def create_image() -> Image.Image:
    """Generate a dummy 64x64 PNG image."""
    image = Image.new("RGB", (64, 64), color="navy")
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill="white")
    return image


def on_open_chat(icon, item):
    print("CHAT WINDOW!")


def on_pause_ai(icon, item):
    print("PAUSE AI")


def on_settings(icon, item):
    print("SETTINGS")


def on_exit(icon, item):
    icon.stop()


if __name__ == "__main__":
    image = create_image()
    menu = pystray.Menu(
        pystray.MenuItem("Open Chat", on_open_chat),
        pystray.MenuItem("Pause AI", on_pause_ai),
        pystray.MenuItem("Settings", on_settings),
        pystray.MenuItem("Exit", on_exit),
    )
    icon = pystray.Icon("aatom", image, "A.A.T.O.M.", menu)
    icon.run()
