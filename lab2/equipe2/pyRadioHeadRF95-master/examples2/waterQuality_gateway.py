#!/usr/bin/python

import sys, os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Add path to pyRadioHeadiRF95 module
sys.path.append(os.path.dirname(__file__) + "/../")

import pyRadioHeadRF95 as radio
import time

rf95 = radio.RF95()

rf95.init()

rf95.setTxPower(20, False)
rf95.setFrequency(915)

rf95.setSignalBandwidth(rf95.Bandwidth500KHZ)
rf95.setSpreadingFactor(rf95.SpreadingFactor12)
rf95.setCodingRate4(rf95.CodingRate4_5)

print ("StartUp Done!")
print ("Receiving...")

'''
	Configuracoes do MQTT
'''

broker = "10.208.7.67"
port = 1883
keepAlive = 60
topic = 'SENSOR_DATA/PH_VALUE'
firstTime = True

def on_connect(client, userdata, flags, rc):
	println("[MQTT STATUS] Conectado ao broker. "+str(rc))

def on_message(client, userdata, msg):
	message = str(msg.payload)
	print("[MQTT STATUS] Topico: "+msg.topic+" / Mensagem: "+message)

def on_publish(client, userdata, result):
	print("Data published on "+topic)
	pass

print ("[MQTT STATUS] Inicializando MQTT...")

#client = mqtt.Client()
#client.on_connect=on_connect
#client.connect(broker, port)

while True:
	if rf95.available():
		(sensorRead, l) = rf95.recv()
		#@TODO
		#	testar isso ai embaixo
		#msg = sensorRead[:10] 
		msg = sensorRead
		if (len(msg) < 5):
			print(int(msg[3]))
			if(int(msg[3]) == 5):
				rf95.setCodingRate4(rf95.CodingRate4_5)
				print("Coding Rate = 4/5")
			if(int(msg[3]) == 6):
				rf95.setCodingRate4(rf95.CodingRate4_6)
				print("Coding Rate = 4/6")
			if(int(msg[3]) == 7):
				rf95.setCodingRate4(rf95.CodingRate4_7)
				print("Coding Rate = 4/7")
			if(int(msg[3]) == 8):
				rf95.setCodingRate4(rf95.CodingRate4_8)
				print("Coding Rate = 4/8")
		else:
			print(msg)			
                sys.stdout.flush()
#print ("Mensagem: " + msg)
#ans = client.publish(topic, temp)
#print ans
#time.sleep(2)
#else:
#time.sleep(0.05)
