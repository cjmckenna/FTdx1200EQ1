import sys
from cx_Freeze import setup, Executable

build_exe_options = {}
setup(  name = "FTdx1200_EQ",
        version = "2.0.0",
        description = "Yaesu FTdx1200 and 3000 EQ Utility",
        options = {"build_exe":build_exe_options},
        executables = [Executable("ftdx1200_eq_app.py")])