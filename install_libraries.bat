@echo off
SET LOGFILE=install_log.txt
ECHO Installation started at %date% %time% > %LOGFILE%

REM Function to install a Python package
:install
ECHO Installing %1...
pip install %1 >> %LOGFILE% 2>&1
IF ERRORLEVEL 1 (
    ECHO Failed to install %1
    ECHO Failed to install %1 >> %LOGFILE%
) ELSE (
    ECHO Successfully installed %1
    ECHO Successfully installed %1 >> %LOGFILE%
)
GOTO :eof

REM List of Python libraries to install
CALL :install opencv-python
CALL :install pillow
CALL :install numpy
CALL :install pyttsx3
CALL :install xlwt
CALL :install xlrd
CALL :install xlutils
CALL :install flask
CALL :install pandas

ECHO Installation completed at %date% %time% >> %LOGFILE%
ECHO Installation process is complete. Check %LOGFILE% for details.
PAUSE
