"""
Script para generar ejecutable .exe con PyInstaller.
"""

import subprocess
import sys
from pathlib import Path

def build_exe():
    """Construye el ejecutable .exe usando PyInstaller."""
    
    project_root = Path(__file__).parent
    main_file = project_root / "src" / "main.py"
    output_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # Comando PyInstaller
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin consola
        "--icon=src/resources/icon.ico",  # Ícono (opcional)
        f"--distpath={output_dir}",
        f"--buildpath={build_dir}",
        "--name=Transcriptor",  # Nombre del ejecutable
        str(main_file),
    ]
    
    print("🔨 Compilando ejecutable...")
    print(f"Comando: {' '.join(command)}\n")
    
    try:
        subprocess.run(command, check=True)
        print("\n✅ ¡Ejecutable generado exitosamente!")
        print(f"📁 Ubicación: {output_dir / 'Transcriptor.exe'}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al compilar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
