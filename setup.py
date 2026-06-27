import sys
import os
from cx_Freeze import setup, Executable

python_dir = os.path.dirname(sys.executable)

include_files = [
    (os.path.join(python_dir, "vcruntime140.dll"), "vcruntime140.dll"),
    (os.path.join(python_dir, "vcruntime140_1.dll"), "vcruntime140_1.dll")
]

build_exe_options = {
    "packages": ["pygame"],
    "include_files": include_files
}

executables = [
    Executable(
        "main.py", 
        base="Win32GUI", 
        target_name="Alice_vs_Rainha.exe"
    )
]

setup(
    name="Alice vs Rainha de Copas",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=executables
)