@echo off
pip install -r requirements.txt
"D:/FontForgeBuilds/bin/ffpython.exe" ./fontforge_script.py --chdoc
pause
python fonttools_script.py
pause