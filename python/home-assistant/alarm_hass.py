import time
import RPi.GPIO as io
io.setmode(io.BCM)
import homeassistant.remote as remote
from homeassistant.const import STATE_ON

api = remote.API('127.0.0.1', '')

if __name__ == "__main__":     
    door_pin = 14

    io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp
    status = 0

    while True:
        if io.input(door_pin) and status == 0:
            remote.set_state(api, 'sensor.Switch_Frontdoor', new_state='Open')
            print("DOOR ALARM!")
            status = 1
        elif not io.input(door_pin) and status == 1:
            remote.set_state(api, 'sensor.Switch_Frontdoor', new_state='Closed')
            status = 0

        time.sleep(0.5)