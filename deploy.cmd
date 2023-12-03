for /f %%D in ('wmic volume get DriveLetter^, Label ^| find "CIRCUITPY"') do set myDrive=%%D
echo %myDrive%

REM delete any existing python files so we know it's only going to run our new ones
del %myDrive%\*.py
REM copy over our python files
xcopy *.py %myDrive%\ /Y
REM rename the main file to code.py
ren %myDrive%\code_1.py code.py
REM copy over our lib files
xcopy lib %myDrive%\lib /Y