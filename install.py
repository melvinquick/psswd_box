import os
import shutil
import subprocess
import sys
from textwrap import dedent


def resolve_package_name():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    try:
        with open("/dev/tty", "r") as tty:
            sys.stdout.write("Enter the Python package name to install: ")
            sys.stdout.flush()
            name = tty.readline().strip()
            if not name:
                raise ValueError("Empty package name")
            return name
    except (OSError, ValueError) as exc:
        print(f"Error: no package name provided ({exc}).", file=sys.stderr)
        print("Usage: curl ... | python3 - <package_name>", file=sys.stderr)
        sys.exit(2)


PACKAGE_NAME = resolve_package_name()

# ---------------------------------------------------------------------------
# Derived names
# ---------------------------------------------------------------------------
EXECUTABLE_NAME = PACKAGE_NAME.replace("_", "-")
DISPLAY_NAME = " ".join(w.capitalize() for w in PACKAGE_NAME.split("_"))
VENV_NAME = f"{PACKAGE_NAME}_venv"
DESKTOP_FILENAME = f"{PACKAGE_NAME}.desktop"
ICON_RELATIVE_PATH = f"{PACKAGE_NAME}/resources/images/{PACKAGE_NAME}-128.png"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def print_green(skk):
    print(f"\033[92m {skk}\033[00m")


def print_red(skk):
    print(f"\033[91m {skk}\033[00m")


def get_venv_path():
    venv_dir = os.path.expanduser("~/.venvs")
    os.makedirs(venv_dir, exist_ok=True)
    return os.path.join(venv_dir, VENV_NAME)


def get_desktop_file_path():
    return os.path.expanduser(f"~/.local/share/applications/{DESKTOP_FILENAME}")


# ---------------------------------------------------------------------------
# Core install / uninstall
# ---------------------------------------------------------------------------
def create_venv(venv_path):
    print("Creating the virtual environment...", end=" ")
    sys.stdout.flush()
    subprocess.run(
        [sys.executable, "-m", "venv", venv_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")

    print("Ensuring pip is up to date...", end=" ")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--upgrade", "pip"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")


def install_app(venv_path):
    print(f"Installing {DISPLAY_NAME} into the virtual environment...", end=" ")
    sys.stdout.flush()
    pip_path = os.path.join(venv_path, "bin", "pip")
    subprocess.run(
        [pip_path, "install", "--no-cache-dir", PACKAGE_NAME],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print_green("[OK]")


def get_installed_metadata(venv_path):
    python_path = os.path.join(venv_path, "bin", "python3")
    result = subprocess.run(
        [
            python_path,
            "-c",
            (
                "from importlib.metadata import metadata; "
                f"m = metadata('{PACKAGE_NAME}'); "
                "print(m['Version']); "
                "print(m.get('Summary', ''))"
            ),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    version = lines[0] if lines else "unknown"
    description = lines[1] if len(lines) > 1 else ""
    return version, description


def get_icon(venv_path):
    site_packages = os.path.join(venv_path, "lib")
    for folder in os.listdir(site_packages):
        if folder.startswith("python"):
            site_packages = os.path.join(site_packages, folder, "site-packages")
            break
    return os.path.join(site_packages, ICON_RELATIVE_PATH)


def get_python_path(venv_path):
    return os.path.join(venv_path, "bin", "python3")


def get_app_path(venv_path):
    return os.path.join(venv_path, "bin", EXECUTABLE_NAME)


def create_desktop_file(icon, version, description, python, app):
    print("Creating the .desktop entry...", end=" ")
    sys.stdout.flush()
    desktop_content = dedent(f"""\
        [Desktop Entry]
        Version={version}
        Type=Application
        Name={DISPLAY_NAME}
        Comment={description}
        Exec={python} {app}
        Icon={icon}
        Terminal=false
        Categories=Utility;
    """)
    desktop_path = get_desktop_file_path()
    os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
    with open(desktop_path, "w") as f:
        f.write(desktop_content)
    print_green("[OK]")


def do_uninstall():
    venv_path = get_venv_path()
    desktop_file_path = get_desktop_file_path()
    removed = False

    if os.path.exists(venv_path):
        print("Removing the virtual environment...", end=" ")
        sys.stdout.flush()
        shutil.rmtree(venv_path)
        print_green("[OK]")
        removed = True

    if os.path.exists(desktop_file_path):
        print("Removing the .desktop entry...", end=" ")
        sys.stdout.flush()
        os.remove(desktop_file_path)
        print_green("[OK]")
        removed = True

    return removed


def do_install():
    venv_path = get_venv_path()
    create_venv(venv_path)
    install_app(venv_path)

    version, description = get_installed_metadata(venv_path)

    create_desktop_file(
        get_icon(venv_path),
        version,
        description,
        get_python_path(venv_path),
        get_app_path(venv_path),
    )

    print()
    print_green(f"{DISPLAY_NAME} v{version} has been successfully installed.")


def handle_update():
    print(f"\nUpdating {DISPLAY_NAME}...\n")
    existed = do_uninstall()
    if not existed:
        print("No existing installation found. Performing fresh install.\n")
    else:
        print()
    do_install()


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
def show_menu():
    try:
        with open("/dev/tty", "r") as tty:
            while True:
                print(f"\n=== {DISPLAY_NAME} Installer ===")
                print("1) Install")
                print("2) Update")
                print("3) Uninstall")
                print("0) Exit")

                sys.stdout.write("\nSelect an option [0-3]: ")
                sys.stdout.flush()
                choice = tty.readline().strip()

                if choice == "1":
                    if os.path.exists(get_venv_path()):
                        print_red(
                            "\nExisting installation detected. "
                            "Please use 'Update' instead."
                        )
                        continue
                    print()
                    do_install()
                    break
                elif choice == "2":
                    handle_update()
                    break
                elif choice == "3":
                    print()
                    if do_uninstall():
                        print()
                        print_green(f"{DISPLAY_NAME} has been uninstalled.")
                    else:
                        print(f"\n{DISPLAY_NAME} does not appear to be installed.")
                    break
                elif choice == "0":
                    print("\nGoodbye.")
                    break
                else:
                    print_red("\nInvalid selection. Please try again.")
    except OSError:
        print_red("Error: No interactive terminal available.")
        print_red("Please run this script from a terminal session.")
        sys.exit(1)


def main():
    show_menu()


if __name__ == "__main__":
    main()
