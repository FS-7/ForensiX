@echo off 

cd flask_asr

cd ..\flask_fr
start runner.bat

cd ..\flask_nlp
start runner.bat

cd ..\flask
start runner.bat

cd ..\react
start runner.bat

cd ..

@echo on