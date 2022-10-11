import utime
import machine
from ubinascii import hexlify
from mqtt import MQTTClient

import json
import hx711

# ssid and password of your wifi router
wifi_ssid="SummerTime"
wifi_password="Calmhat436"

# host,port,username and password of the mqtt broker
mqtt_hostname='cbb90cade46d4ff38fdf18a5dc12c4be.s2.eu.hivemq.cloud'
mqtt_port=8883 
mqtt_user="test1"
mqtt_password="TestPass"
mqtt_client_id = hexlify(machine.unique_id())



def connect_to_wifi(ssid=None, password=''):
    ''' connect to the wifi router'''
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to wifi network...')
        sta_if.active(True)
        # Please use your own Wifi Routers Credentials !!
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    
    print('successfull connection to ',ssid)
    print('network config:', sta_if.ifconfig())


def puback_cb(msg_id):
  print('PUBACK ID = %r' % msg_id)

def suback_cb(msg_id, qos):
  print('SUBACK ID = %r, Accepted QOS = %r' % (msg_id, qos))
  
def con_cb(connected):
  if connected:
    client.subscribe('subscribe/topic')

def msg_cb(topic, pay):
  print('Received %s: %s' % (topic.decode("utf-8"), pay.decode("utf-8")))


connect_to_wifi(wifi_ssid, wifi_password)  

# load the private key for TLS aka mqtts
with open('key.der') as f:
    key = f.read()
# load the certificate for TLS aka mqtts
with open('cert.der') as f:
    cert = f.read()

ssl_params={
    "key": key, 
    "cert": cert, 
    "server_hostname":mqtt_hostname
}    
  
client = MQTTClient(mqtt_hostname, port=mqtt_port, ssl=True, ssl_params=ssl_params )

client.set_connected_callback(con_cb)
client.set_puback_callback(puback_cb)
client.set_suback_callback(suback_cb)
client.set_message_callback(msg_cb)

client.connect(mqtt_client_id, user=mqtt_user, password=mqtt_password, clean_session=True)



weight = 0
while True:
  if client.isconnected():
    try:
      measurement = hx711.weight()
      if measurement != None and weight != measurement:
            weight = measurement        
            print("publish scale/value " + str(weight))
            pub_id = client.publish('scale/value', str(weight), False)

    except Exception as e:
      print(e)
  else:
    utime.sleep(2)
   

