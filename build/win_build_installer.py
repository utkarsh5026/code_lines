import os
import sys
import subprocess
import shutil

from pathlib import Path


def install_dependencies():
    """Install required packages for building."""
    venv_dir = "build_env"
    subprocess.check_call([sys.executable, '-m', 'venv', venv_dir])

    if sys.platform == "win32":
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")

    subprocess.check_call([
        venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'
    ])
    subprocess.check_call([
        venv_python, '-m', 'pip', 'install', 'pyinstaller'
    ])
    subprocess.check_call([
        venv_python, '-m', 'pip', 'install', '-r',
        os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    ])

    return venv_python


def build_executable(venv_python):
    """Build the executable using PyInstaller."""
    pyinstaller_path = os.path.join(
        os.path.dirname(venv_python), "pyinstaller")
    subprocess.check_call([
        pyinstaller_path,
        '--name=line-counter',
        '--onefile',
        '--console',
        '--clean',
        os.path.join(os.path.dirname(__file__), '..', 'src', 'main.py')
    ])


def main():
    home_dir = Path.home()
    install_dir = home_dir / ".line_counter"
    exe_name = "line-counter.exe"

    print("🚀 Starting installation process...")

    print("📦 Installing dependencies...")
    venv_python = install_dependencies()

    print("🔨 Building executable...")
    build_executable(venv_python)

    print("📁 Creating installation directory...")
    install_dir.mkdir(exist_ok=True)

    print("📝 Copying executable...")
    source_exe = Path('dist') / exe_name
    dest_exe = install_dir / exe_name

    try:
        if not source_exe.exists():
            print(f"Error: Could not find executable at {source_exe}")
            return

        shutil.copy2(source_exe, dest_exe)

    finally:
        print("🧹 Cleaning up...")
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        shutil.rmtree('build_env', ignore_errors=True)
        if os.path.exists('line-counter.spec'):
            os.remove('line-counter.spec')

    print(f"""
✨ Installation Complete! ✨
The line-counter executable has been installed to: {install_dir}
Please restart your terminal to use the 'line-counter' command.
""")


if __name__ == '__main__':
    main()
