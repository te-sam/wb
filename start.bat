cd /d %~dp0
pip install -r requirements.txt
call venv\Scripts\activate
python main.py