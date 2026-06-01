import os
import subprocess
import sys
import venv
from pathlib import Path


def check_virtualenv():
    """Проверяет, запущен ли скрипт в виртуальном окружении"""
    if not hasattr(sys, 'real_prefix') and (os.environ.get('VIRTUAL_ENV') is None):
        raise RuntimeError("Please activate your virtualenv first.")


def install_requirements():
    requirements = ["beautifulsoup4", "pytest"]
    with open("temp_requirements.txt", "w") as f:
        f.write("\n".join(requirements))

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "temp_requirements.txt"])
    finally:
        if os.path.exists("temp_requirements.txt"):
            os.remove("temp_requirements.txt")


def save_requirements():
    result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True)
    installed_packages = result.stdout

    with open("requirements.txt", "w") as f:
        f.write(installed_packages)

    print("Installed packages:")
    print(installed_packages)


def create_env_archive():
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        print("Virtual environment path not found. Skipping archiving.")
        return

    env_name = os.path.basename(venv_path)
    archive_name = f"{env_name}_env"

    try:
        if os.name == 'nt': #windows
            import shutil
            shutil.make_archive(archive_name, 'zip', venv_path)
            print(f"Created archive: {archive_name}.zip")
        else:
            import tarfile
            with tarfile.open(f"{archive_name}.tar.gz", "w:gz") as tar:
                tar.add(venv_path, arcname=env_name)
            print(f"Created archive: {archive_name}.tar.gz")
    except Exception as e:
        print(f"Failed to create archive: {e}")


def main():
    try:
        check_virtualenv()
        install_requirements()
        save_requirements()
        create_env_archive()
        print("Program is ended")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()