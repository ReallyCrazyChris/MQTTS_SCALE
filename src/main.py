import utime
import json
import hx711
from umqtt.robust import MQTTClient

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

if __name__ == "__main__":
    
    # load the private key
    with open('key.der') as f:
        key = f.read()
    # load the certificate
    with open('cert.der') as f:
        cert = f.read()

    # ssid and password of your wifi router
    wifi_ssid="SummerTime"
    wifi_password="Calmhat436"

    connect_to_wifi(wifi_ssid, wifi_password)

    # set the mqtt broker hostname 
    server_hostname='de69d3b8d0c4424bb338806bc6d75f09.s2.eu.hivemq.cloud'
    # set the TLSV1.2 secure port of the broker
    port=8883
    
    # set the username and password to authenticate with the broker
    user="ESP32"
    password="WishUsLuck1!" #use a password 8 characers, with Upper&Lower Case, and a number and a speial character

    # use a unique client id ;-)
    client_id = "ESP32"

    # last will topic and message ... (✖╭╮✖)
    topic = 'scale/state'
    msg = json.dumps({"active":0})

    print("connecting to mqtts broker ",server_hostname, port)

    # define the parameters for 
    ssl_params={
        "key": key, 
        "cert": cert, 
        #"server_side":False,
        "server_hostname":server_hostname
        #"cert_reqs":"",
        #"cadata":"",
        #"do_handshake":False
        }
    
    # create a client object
    client = MQTTClient(
        client_id,
        server_hostname, 
        port, 
        user, 
        password, 
        keepalive=120, 
        ssl=True, 
        ssl_params=ssl_params) 

    # create the will ... (✖╭╮✖)
    client.set_last_will(topic, msg, retain = False, qos = 1)
    
    # connect to the broker server ( clean_session = non persistent session )
    # http://www.steves-internet-guide.com/mqtt-clean-sessions-example/
    client.connect(clean_session = True)
    #client.ping()
    #client.reconnect()

    # Uncomment to send scale values
    '''while True:
        weight = hx711.sample()
        message = {"weight":weight}
        message = json.dumps( message )
        print("Sending message " + message)
        client.publish(topic='scale/value', msg=message)
        utime.sleep(0.2)'''

    # Send Mock Data
    for i in range(0, 101):
        weight = i
        #message = {"weight":weight}
        #message = json.dumps( message )
        print("Sending message " + str(weight))
        client.publish(topic='scale/value', msg=str(weight))
        utime.sleep(0.2)

       

    client.disconnect()
  

