# Berkay Sit, 2018
# Issue 1...

import threading
import DobotDllType as dType
import time

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Set Up Variables:
gripperOn = 0 #1 On, 0 Off

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 100, 100, 100, 100, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    #dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    print("Device Name:" , dType.GetDeviceName(api))

    print("Hareket-01: Kablo.1 konumuna git")
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, 150, 80, 0, isQueued = 1)
    print("Hareket-02: Kablo.1 konumunda alçal")
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, 150, 20, 0, isQueued = 1)
    ## Gripper Close
    dType.SetEndEffectorGripper(api, gripperOn, 1, 1)
    ###dType.SetWAITCmd(api, 1, 1)
    print("Hareket-03: Kablo.1 konumunda yüksel")
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, 150, 80, 0, isQueued = 1)

    print("Hareket-04: Kablo.2 konumunda git")
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, -150, 80, 0, isQueued = 1)
    print("Hareket-05: Kablo.2 konumunda alçal")
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, -150, 20, 0, isQueued = 1)
    ## Gripper Release
    dType.SetEndEffectorGripper(api, gripperOn, 0, 1)
    ###dType.SetWAITCmd(api, 2, 1)
    ## Gripper Off
    dType.SetEndEffectorGripper(api, 0, 0, 1)
    

    print("Hareket-06: Kablo.2 konumunda yüksel")
    #print("lastIndex basi")
    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 260, -150, 80, 0, isQueued = 1)[0]

    #Start to Execute Command Queued
    print("SetQueuedCmdStartExec")
    dType.SetQueuedCmdStartExec(api)

    print("Last Index: ", lastIndex)
    num = 0
    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)
        
        if num != dType.GetQueuedCmdCurrentIndex(api)[0]:
            print("Current Index: ", dType.GetQueuedCmdCurrentIndex(api)[0])
            num = dType.GetQueuedCmdCurrentIndex(api)[0]
        #print("lastIndex: ", lastIndex, "- dType.GetQueuedCmdCurrentIndex(api)[0]: ", dType.GetQueuedCmdCurrentIndex(api)[0])

    #Stop to Execute Command Queued
    print("SetQueuedCmdStopExec")
    dType.SetQueuedCmdStopExec(api)
    

#Disconnect Dobot
print("DisconnectDobot")
dType.DisconnectDobot(api)
print("...Goodbye...")
