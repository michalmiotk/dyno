# requirements 
python 3.10.2

# building 
```
pip install pyinstaller
cd building
pyinstaller --onefile --windowed --hidden-import=matplotlib --hidden-import=tkinter ../main.py
```