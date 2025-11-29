@echo off
echo Creating virtual environment...

IF NOT EXIST venv (
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Starting server...
python app.py

pause