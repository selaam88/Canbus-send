#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

"""
Example for sending CAN frames via ASCII protocol (slcan).
"""

import sys
import time

import can
import serial

CAN_DEV = '/dev/ttyUSB0@3000000'

SLEEP_TIME_SECOND = 10
DATABASE = {
    "kmTeller": [
        [0x1A0, [1, 0, 0, 0, 0, 0, 0, 0], 0.4, 0, "km cmd 1"],
        [0x5A0, [0, 0, 50, 0, 0, 0, 0, 0], 0.8, 0, "km cmd 1"]
    ],
    "knipperlichtL": [
        [0x531, [0, 0, 17], 0.4, 0, "Knipperlicht L aan"],
        [0x531, [0, 0, 16], 0.8, SLEEP_TIME_SECOND, "Knipperlicht L uit"]
    ],
    "knipperlichtR": [
        [0x531, [0, 0, 18], 0.4, 0, "Knipperlicht R aan"],
        [0x531, [0, 0, 20], 0.8, SLEEP_TIME_SECOND, "Knipperlicht R uit"]
    ],
    "knipperlichten": [
        [0x531, [0, 0, 23], 0.4, 0, "Knipperlichten aan"],
        [0x531, [0, 0, 24], 0.8, SLEEP_TIME_SECOND, "Knipperlichten uit"]
    ]
}

DATABASE_DBC = {
    "toerenTeller": [['Motor_1', 'Motordrehzahl', 2000, 0.01, "speed meter on"]]
}


def decodebremse_1():
    import cantools
    db = cantools.db.load_file('/home/selaam/Downloads/vw_golf_mk4 (copy).dbc')

    msg = db.get_message_by_name('Bremse_1')
    msg_data = msg.encode(
        {'snelheid_vervangingswaarde': 1, 'ESP_Systemstatus_4_1': 0, 'ESP_Passiv_getastet': 1, 'ASR_controller_t': 1,
         'Zaehler_Bremse_1': 14, 'MSR_Eingriffsmoment': 48, 'ASR_Eingriffsmoment_schnell': 40,
         'ASR_Eingriffsmoment_langsam': 32, 'Geschwindigkeit_neu__Bremse_1_': 0.01, 'Aktiver_Bremskraftverstaerker': 1,
         'ABS_in_Diagnose': 1, 'Fehlerstatus_Schlechtwegausblen': 1, 'Schlechtwegausblendung': 1,
         'Fahrer_bremst__Bremse_1___4_1_': 1, 'Bremskontroll_Lampe': 1, 'Lampe_ASR___ESP': 1, 'Lampe_ABS': 1,
         'EBV_Eingriff': 1, 'ASR_Schaltbeeinflussung': 1, 'ESP_Eingriff': 1, 'EDS_Eingriff': 0, 'ABS_Bremsung__4_1_': 0,
         'MSR_Anforderung': 0, 'ASR_Anforderung': 0})

    print(msg_data)
    sendMessage(msg.frame_id, msg_data)

    # decode('Motor_1', 'Motordrehzahl', 3000, 0.01)


def decode(id, message, number, period):
    import cantools
    db = cantools.db.load_file('/home/selaam/Downloads/vw_golf_mk4 (copy).dbc')

    msg = db.get_message_by_name(id)
    msg_data = msg.encode({'Motordrehzahl': 3000})

    print(message, number)
    print(msg_data)

    sendMessage(msg.frame_id, msg_data, period, 10)


def toerenteller():
    decode('Motor_1', 'Motordrehzahl', 2000, 0.01)
    print("speed meter on")
    time.sleep(100)


def kmteller():
    sendMessage(0x1A0, [1, 0, 0, 0, 0, 0, 0, 0], 0.4)
    sendMessage(0x5A0, [0, 0, 50, 0, 0, 0, 0, 0], 0.8)
    print("speed meter on")
    time.sleep(100)


def fill():
    a = input("choose your function")
    a = int(a)
    if a == 1:
        knipperlichtL()
        print("you have turned on knipperichtL")
        a = input("choose your function")
        a = int(a)
    elif a == 2:
        knipperlichtR()
        print("you have turned on knipperichtR")
    elif a == 3:
        knipperlichten()
        print("you have turned on knipperichten")


def knipperlichtL():
    sendMessage(0x531, [0, 0, 17], 0.4)
    sendMessage(0x531, [0, 0, 16], 0.8)
    print("knipperlichtL on")
    time.sleep(10)


def knipperlichtR():
    sendMessage(0x531, [0, 0, 18], 0.4)
    sendMessage(0x531, [0, 0, 20], 0.8)
    time.sleep(10)


def knipperlichten():
    sendMessage(0x531, [0, 0, 23], 0.4)
    sendMessage(0x531, [0, 0, 24], 0.8)
    time.sleep(10)


def sendToIdWithDataRange():
    for j in range(1,8):
        for i in range(0, 255):
            sendMessage(0x1A0, [i, i, i, i, i, i, i, i], 0.02, 0)
            print(i)

def repeat(array, id):
    for i in range(0, 255):
        sendMessage(0x1A0, [i, i, i, i, i, i, i, i], 0.02, 0)
        print(i)


def sendMessage(hexId, data, period, sleepTime):
    try:
        bus = getBus()
    except serial.serialutil.SerialException as err:
        print(err)
        sys.exit(1)

    message = can.Message(arbitration_id=hexId, is_extended_id=False, data=data)
    bus.send_periodic(message, period)
    time.sleep(sleepTime)

def sendSequential():
    sendMessage(0x320, generate(), 0.01, 1)
def getBus():
    bus = can.interface.Bus(bustype='slcan',
                            channel=CAN_DEV,
                            rtscts=True,
                            bitrate=500000)
    return bus

def generate():
    start = 0
    end =255
    for indexA in range(start, end):
        for indexB in range(start, end):
            for indexC in range(start, end):
                for indexD in range(start, end):
                    for indexE in range(start, end):
                        for indexF in range(start, end):
                            for indexG in range(start, end):
                                for indexH in range(start, end):
                                    print(indexH, indexG, indexF, indexE, indexD, indexC, indexB, indexA)

generate()


def main():
    """main routine."""
    try:
        bus = getBus()
    except serial.serialutil.SerialException as err:

        print(err)
        sys.exit(1)

    # send standard frame

    msg = can.Message(arbitration_id=0x1A0,
                      is_extended_id=False,
                      data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    bus.send_periodic(msg, 1)
    time.sleep(1)

    bus.shutdown()


if __name__ == '__main__':
    # main()
    # knipperlichtL()
    # knipperlichtR()
    # knipperlichten()
    # fill()
    # decode()
    # runCommand()
    # sendToIdWithDataRange()
     generate()

# kmteller()
# toerenteller()
