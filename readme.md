# MQTTS-Scale using ESP32, HX711 and Secure HiveMQ Cloud


## Description
The mqtts-scale sends weight messages in kilograms to a cloud based mqtt broker. The communication is secured with SSl/TLS using a private key and a certificate.

This code is sucessully working with:
- ESP32
- Micropython V1.19
- [Secure HiveMQ Cloud](https://www.hivemq.com/mqtt-cloud-broker/)
- HX711 weigh bridge amplifier


Dependancies
======

## Install Python

If you don't already have python installed

[www.python.org/downloads/](https://www.python.org/downloads/)



## Install Esptool
Esptool is used to erase and write the Micropython firmware to the ESP flash memory

As with most of the commands in this document, please open a Terminal ( cmd.exe )

and run the following

``pip install esptool``

test the installation by a running 

``esptool``

## Install Ampy
Ampy is a program that uploads files to the micropython file store on the ESP

``pip install adafruit-ampy``

test the installation by  running 

``ampy``

## Install Openssl

Please follow this excellent [article](https://medium.com/swlh/installing-openssl-on-windows-10-and-updating-path-80992e26f6a1)

## Install PuTTY

PuTTY is an awesome remote terminal tool. PuTTY supports serial communication
which we will need to interact with the ESP REPL

Please go to [www.putty.org](https://www.putty.org/)

Download and Install Putty



## MQTTS Broker

You can use any MQTTS broker, but this software is confimed to work with HiveMQ Cloud.

So head on over to [https://www.hivemq.com/mqtt-cloud-broker/](https://www.hivemq.com/mqtt-cloud-broker/)

An try out their ``Free to connect IoT devices`` option

Click ``create a new cluster`` 

Then create credentials by following ``manage cluster`` -> `access management` 

``tip:`` the Password shoud have at least 8 characters, numbers, upper- and lowercase letters.

document the Cluster URL and Port (TLS) settings, you need it later

Setup
======

## Configure env.bat

In order to program your ESP you need to set the communications port
use windows device manager to see which COM port your ESP is connected on

open the file env.bat and set the com port to connect to the ESP on
```
AMPY_PORT=<ESP COM PORT> # insert your ESP's COM port
```

if you have problems in uploading to the device change delay time
set the delay in seconds before serial communication is started with the ESP

```
AMPY_DELAY=1
```

the communication baud/bit rate sould remain the same

````
AMPY_BAUD=115200
````

Flashing the Micropython Firmware
======
## Install Micropython onto the ESP

change to the firmware directory

``cd firmware``

erase the current flash

``erase.bat``

flash the micropython firmware binary to the ESP

``flash.bat``

return to the parent folder

``cd ..``


## Verify the Micropython Installation

Test that the Micropython is working on the ESP, by connecting to the
ESP and doing a hardware reset

``console.bat`` will start a Terminal console session using *PuTTY*. 

When the terminal connects, press the reset button on the ESP 
and you should see details about the installed firmware

```
ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x17 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:5656
load:0x40078000,len:12696
load:0x40080400,len:4292
entry 0x400806b0
```

Secure Encryption
======
## Generate Private Key and Certificate
The micropython mqtt client can conenct to a secure broker server, by using a ``public key`` and a ``certificate``

The certificates and keys are generated in the PEM format, a base64 encoded file

PEM format files are also converted / provided in the ``DER`` format. This is a Binary HEXADECIMAL format wich is used by the Micropython MQTTS client.

## Create a Certificate Signing Request

change to the ssl directory

``cd ssl``

open the request.txt file in your text editor or ide. update the section ``[req_distinguished_name]`` with the ESP's information

````
[req]
default_bits           = 2048
prompt                 = no
default_md             = sha384
distinguished_name     = req_distinguished_name

[req_distinguished_name]
countryName            = < Two Charater County Code e.g. DE>
stateOrProvinceName    = < State e.g. Bayern>
organizationName       = < Company e.g. Work
organizationalUnitName = < Innovation >
commonName             = < A Unique Device ID/Name >
emailAddress           = < support@myworkplace.com >
````

save the requests.txt file

## Generate the keys and certificate files

from within the ssl directory run 

``generate_key_and_cert.bat`` 

in a terminal. This will create and copy the key and certificate files to the src directory

### Or you can do it manually

create a private_key and a certificate signing request

````
openssl.exe req -newkey rsa:2048 -keyout key.pem -nodes -out request.csr -config request.txt
````

sign the certificate signing request, and produce a certificate

````
openssl.exe x509 -req -sha256 -days 365 -in request.csr -signkey key.pem -out cert.pem
````

convert the certifivate from pem format to der format

````
openssl x509 -in cert.pem -out cert.der -outform DER
````

convert the private key from pem format to der format

````
openssl.exe rsa -in key.pem -out key.der -outform DER
````


Once the following files have been created 

````
request.csr
key.pem
key.der
cert.pem
cert.der
````

copy ``key.der`` and ``cert.der`` to the ``src`` folder

````
copy *.der ..\src /Y
````

return to the parent folder

``cd ..``


Provide the Wifi Router SSID and Password
====

In your ide or text editor open the file ``main.py``. Around line 31

````
    # ssid and password of your wifi router
    wifi_ssid="<Insert your router SSID>"
    wifi_password="<Insert your router Password>"

````

so that it looks something like ...

````
    # ssid and password of your wifi router
    wifi_ssid="Autobahn"
    wifi_password="NoSpeedLimits"

````

Provide the MQTT broker servers Hostname, Username and Password
====

In the file ``main.py``. Around line 38

````
    # set the mqtt broker hostname 
    server_hostname='<Insert broker server ip or url>'

    # set the username and password to authenticate with the broker
    user="<Insert Username>"
    password="<Insert Password>" 

````
so that it looks something like ...

````
    # set the mqtt broker hostname 
    server_hostname='6bc6d75f09de69d3b8d0c4424bb33880.s2.eu.hivemq.cloud'

    # set the username and password to authenticate with the broker
    user="IamScale01"
    password="Wannabe75kg!" 

````

``tip:`` use a password that has 8 characters or more, including Upper and lowercase characters with numbers and special characters. 



Uploading the source code to the ESP
======

Open a terminal window and run

``upload.bat``
