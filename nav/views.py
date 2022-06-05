from django.shortcuts import render
from rest_framework.views import APIView
from time import sleep
from pymultiwii import MultiWii
from rest_framework.response import Response
from rest_framework import status
import threading


board = MultiWii("/dev/ttyUSB0") # init flight controller 

thr_reset = False # throttle reset flag
ch_val = 0 

def throttle():  # throttle control function
        while True:
            data = ch_val
            board.sendCMD(8,MultiWii.SET_RAW_RC,data)
            sleep(0.05)
            print(ch_val)
            if thr_reset:
                print("Throttle killed")
                break

def changeThrottle(val,pit,rol,ya): # throttle change function
    global ch_val
    ch_val = [rol,pit,ya,val]


class ThrottleView(APIView): # throttle API view
      

    def post(self,request,format=None): # http post function for throttle
        changeThrottle(int(request.data["thr"]),int(request.data["pitch"]),int(request.data["roll"]),int(request.data["yaw"]))

        return Response(status=status.HTTP_200_OK)


class ArmView(APIView): # arm/disarm API view
    def post(self,request,format=None): # POST function for arm command
        global thr_reset
        arm = request.data["arm"]

        if(arm==True): 
            thr_reset=False
            board.arm()
            print("Armed!")
            t1 = threading.Thread(target=throttle)
            t1.start()
        
        else:
            thr_reset=True
            board.disarm()
            print("Disarmed!")

        for thread in threading.enumerate(): 
            print(thread.name)

        return Response(status=status.HTTP_200_OK)