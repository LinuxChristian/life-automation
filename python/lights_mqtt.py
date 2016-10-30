#!/usr/bin/env python                                                                                                                             $
# -*- coding: utf-8 -*-

import time
from subprocess import call

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

def operate_lights_leklint(client, userdata, msg):
    if msg.payload.decode('utf-8') == 'ON':
        call(['python3.4','/home/osmc/pyrtl433/send_signal.py', '/home/osmc/pyrtl433/quigg_2_on.npy'])
        print("Le Klint ON")
    else:
        call(['python3.4','/home/osmc/pyrtl433/send_signal.py', '/home/osmc/pyrtl433/quigg_2_off.npy'])
        print("Le Klint OFF")

def operate_lights_louise(client, userdata, msg):
    if msg.payload.decode('utf-8') == 'ON':
        call(['python3.4','/home/osmc/pyrtl433/send_signal.py', '/home/osmc/pyrtl433/quigg_1_on.npy'])
        print("Louise ON")
    else:
        call(['python3.4','/home/osmc/pyrtl433/send_signal.py', '/home/osmc/pyrtl433/quigg_1_off.npy'])
        print("Louise OFF")

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect('192.168.1.100')
    client.subscribe('lights/livingroom/#')
    client.message_callback_add('lights/livingroom/leklint', operate_lights_leklint)
    client.message_callback_add('lights/livingroom/louise', operate_lights_louise)

    client.loop_forever()