cd extraction
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
CALL .venv\Scripts\deactivate.bat

cd ..\flask
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
CALL .venv\Scripts\deactivate.bat

cd ..\flask_asr
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
CALL .venv\Scripts\deactivate.bat

cd ..\flask_ir
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -r requirements_2.txt
CALL .venv\Scripts\deactivate.bat

cd ..\flask_nlp
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
CALL .venv\Scripts\deactivate.bat

cd ..\flask_rag
virtualenv .venv
CALL .venv\Scripts\activate.bat
pip install -r requirements.txt
CALL .venv\Scripts\deactivate.bat

cd ..\react
npm i
npx shadcn@latest init --
npx shadcn@latest add

cd ..
