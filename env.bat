@echo off
echo use windows device manager to see which COM port your ESP is connected on

rem the com port to connect to the ESP on
set AMPY_PORT=COM13
rem the delay in seconds before serial communication is started with the ESP
set AMPY_DELAY=1
rem the communication baud/bit rate 
set AMPY_BAUD=115200

echo connecting to device on com port %AMPY_PORT% delay %AMPY_DELAY%s
