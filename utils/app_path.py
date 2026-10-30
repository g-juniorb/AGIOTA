from pathlib import Path
import platform


if platform.system() == "Windows":

    APP_DIR = (
        Path.home()
        / "AppData"
        / "Local"
        / "GIGI"
    )

elif platform.system() == "Darwin":

    APP_DIR = (
        Path.home()
        / "Library"
        / "Application Support"
        / "GIGI"
    )

else:

    APP_DIR = (
        Path.home()
        / ".GIGI"
    )


APP_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CONFIG_DIR = APP_DIR
PROFILE_DIR = APP_DIR / "profile"
REPORTS_DIR = APP_DIR / "reports"
LOGS_DIR = APP_DIR / "logs"

PROFILE_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)