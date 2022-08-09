import ssl
import time
import datetime
from turtle import update
import paho.mqtt.client as mqtt
from rigol import Rigol

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

def on_message(client, userdata, message):
    print("recieved message = ", str(message.payload))

def voltage_callback(client, userdata, message):
    print("new voltage: ", message.payload)
    # power.set_voltage(1)

def current_callback(client, userdata, message):
    print("new current: ", message.payload)

def on_publish(client,userdata,result):
    print("data published")

power = Rigol()
serials = []
instrs = []
for i in range(power.get_num()):
    serials.append(power.get_serial(i))
    instrs.append("PWSP"+str(i))

client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message
client.on_publish = on_publish
client.tls_set(None, None, None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.username_pw_set("picop", "MQTTR0cks8")
client.connect("mqtt.iot.wonderware.com", 8883, 60)
client.loop_start()

client.publish("paho/status", "connected")
for i in range(len(serials)):
    client.publish("paho/"+instrs[i]+"/status", "on")
    client.publish("paho/"+instrs[i]+"/serial", serials[i])

    
for i in instrs:
    client.subscribe("paho/"+i+"/#")
    client.message_callback_add("paho/"+i+"/voltage", voltage_callback)
    client.message_callback_add("paho/"+i+"/current", current_callback)

for i in range(30):
    for i in range(len(instrs)):
        client.publish("paho/"+instrs[i]+"/voltage", power.get_voltage(i))
        client.publish("paho/"+instrs[i]+"/current", power.get_current(i))
        client.publish("paho/"+instrs[i]+"/power", power.get_power(i))
        client.publish("paho/"+instrs[i]+"/time", str(datetime.datetime.now())[:-7])
    time.sleep(1)

client.publish("paho/status", "disconnected")
client.loop_stop()
