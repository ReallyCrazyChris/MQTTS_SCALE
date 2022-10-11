echo on
call ./env.bat

echo removing main.py hx711.py key.der cert.der
ampy rm /main.py
ampy rm /mqtt.py
ampy rm /hx711.py
ampy rm /cert.der
ampy rm /key.der


echo upload cert.der key.der hx711.py main.py
ampy put ./src/key.der /key.der
ampy put ./src/cert.der /cert.der
ampy put ./src/hx711.py /hx711.py
ampy put ./src/mqtt.py /mqtt.py
ampy put ./src/main.py /main.py

echo starting serial console
call ./console.bat




