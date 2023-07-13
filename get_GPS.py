from matplotlib.image import imread
import torch
import cv2
import os
import numpy as np

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
# from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.move import extended_move_by, extended_move_to
from olympe.video.pdraw import Pdraw, PdrawState
# from olympe.video.renderer import PdrawRenderer
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, PositionChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged, HomeChanged
from olympe.messages import gimbal
import time
import csv

# parrot設定
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
DRONE_IP = os.environ.get("DRONE_IP", "192.168.42.1")

# 離陸
def takeoff(drone):
    print("------------------------------takeoff------------------------------")
    assert drone(TakeOff()).wait().success()
    time.sleep(5)

# 毎秒0.7mでFm前進
def go(drone, F):
    print("------------------------------go------------------------------")
    assert drone(
        extended_move_by(F, 0, 0, 0, 0.7, 0.7, 0.7)
    ).wait().success()
    time.sleep(3)

# 毎秒0.7mでRm右進
def go_LR(drone, R):
    print("------------------------------go------------------------------")
    assert drone(
        extended_move_by(0, R, 0, 0, 0.7, 0.7, 0.7)
    ).wait().success()
    time.sleep(3)

# 毎秒0.7mでHm上昇
def up(drone, H):
    print("------------------------------gain_altitude------------------------------")
    drone(
        extended_move_by(0, 0, -H, 0, 0.7, 0.7, 0.7)
    ).wait().success()
    time.sleep(3)

# 着陸
def landing(drone):
    print("------------------------------landing------------------------------")
    drone(Landing()).wait().success()
    drone.disconnect()

def get_now_gps(drone, drone_info):
    # Wait for GPS fix
    drone(GPSFixStateChanged(_policy='wait'))

    #ドローン離陸前のGPS
    # gps = drone.get_state(HomeChanged)
    gps = drone.get_state(PositionChanged)
    print(gps)
    print(type(gps))
    drone_info.append([gps['latitude'], gps['longitude'], gps['altitude']])
    print(drone_info)
    print(type(drone_info))
    
    # time.sleep(1)
       
    return drone_info
    
def set_gimbal(drone, deg):
    drone(gimbal.set_target(
        gimbal_id=0,
        control_mode="position",
        yaw_frame_of_reference="none",
        yaw=0.0,
        pitch_frame_of_reference="absolute",
        pitch=deg,
        roll_frame_of_reference="none",
        roll=0.0,
    )).wait()
    time.sleep(12)


if __name__ == '__main__':
    # ドローン接続
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    
    # ジンバルの角度設定
    set_gimbal(drone, -90.0)    # -90で真下
    print("ジンバルの調節完了")
    drone_info = []


    
    takeoff(drone)
    time.sleep(2)
    drone_info = get_now_gps(drone, drone_info)
    
    up(drone, 1)
    time.sleep(1)
    drone_info = get_now_gps(drone, drone_info)
    
    go(drone, 1)
    time.sleep(1)
    drone_info = get_now_gps(drone)

    
    go(drone, 1)
    time.sleep(1)
    drone_info = get_now_gps(drone)
    
    go(drone, 1)
    time.sleep(1)
    drone_info = get_now_gps(drone)

    
    go_LR(drone, 1)
    time.sleep(1)
    drone_info = get_now_gps(drone)
    
    go_LR(drone, 1)
    time.sleep(1)
    gdrone_info = get_now_gps(drone) 

    landing(drone)
    drone_info = get_now_gps(drone,drone_info)
    print(drone_info)
    

    with open('keiro.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(drone_info)