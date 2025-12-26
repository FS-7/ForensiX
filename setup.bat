cd extraction
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
.venv\Scripts\deactivate.bat

cd ..\flask
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
.venv\Scripts\deactivate.bat

cd ..\flask_asr
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
.venv\Scripts\deactivate.bat

cd ..\flask_fr
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -r requirements_2.txt
.venv\Scripts\deactivate.bat

cd ..\flask_nlp
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
.venv\Scripts\deactivate.bat

cd ..\flask_rag
virtualenv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
.venv\Scripts\deactivate.bat

cd ..\react
npm i
npx shadcn@latest init --
npx shadcn@latest add

cd ..
