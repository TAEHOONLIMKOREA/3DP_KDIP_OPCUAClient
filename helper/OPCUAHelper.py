import opcua
from helper import MongoHelper
from threading import Event
from datetime import datetime

nodes_BuildInfo = {}
nodes_BuildProcess = {}
nodes_Environment = {}
nodes_InertGas = {}
nodes_PowderBed = {}
nodes_ScanField = {}
nodes_test = {}

class BuildInfoSubEventHandler(object):

    def __init__(self, kdip):
        self.KDIP = kdip

    def datachange_notification(self, node, val, data):
        datetime_now = datetime.now()
        datetime_str = datetime_now.strftime("%Y%m%d_%H%M%S")
        if str(node) == "ns=2;s=Services.Scan System.Total Layers":
            self.KDIP.TotalLayer = val
            if val != 0:
                # 빌드 시작 신호
                if not self.KDIP.IsBuilding:
                    # 출력 중이지 않다면 시작 이벤트 발생
                    self.KDIP.BuildingEvent.set()
                self.KDIP.InfluxClient.CreateMeasurement(datetime_str)
                self.KDIP.MongoClient.CreateDB(datetime_str)
                doc = {"time": datetime_now, "TotalLayer": val}
                self.KDIP.MongoClient.InsertDocument("JobInfo", doc)
            else:
                # 빌드 종료 신호
                self.KDIP.BuildingEvent.clear()

        elif str(node) == "ns=2;s=Services.Scan System.Current Layer":
            self.KDIP.CurrentLayer = val
            if val == 0 and self.KDIP.TotalLayer == 0:
                self.KDIP.BuildingEvent.clear()
                return
            else:
                doc = {"time": datetime_now, "CurrentLayer": val}
                self.KDIP.MongoClient.InsertDocument("JobInfo", doc)
                # 이제 여기다가 사진 가져오는 코드 작성해야함










class EnvLogSubEventHandler(object):
    def __init__(self, kdip):
        self.KDIP = kdip

    def datachange_notification(self, node, val, data):
        print(str(node) + " : ", val)
        for paramName, _node in nodes_Environment.items():
            if _node == node:
                self.KDIP.InfluxClient.InsertPoint(paramName, val, self.KDIP.CurrentLayer, "Environment", datetime.now())
                return

        for paramName, _node in nodes_InertGas.items():
            if _node == node:
                self.KDIP.InfluxClient.InsertPoint(paramName, val, self.KDIP.CurrentLayer, "InertGas", datetime.now())
                return

        for paramName, _node in nodes_PowderBed.items():
            if _node == node:
                self.KDIP.InfluxClient.InsertPoint(paramName, val, self.KDIP.CurrentLayer, "PowderBed", datetime.now())
                return

        for paramName, _node in nodes_ScanField.items():
            if _node == node:
                self.KDIP.InfluxClient.InsertPoint(paramName, val, self.KDIP.CurrentLayer, "ScanField", datetime.now())
                return



# -------------------------------- Test Class (For Robot Server) --------------------------------
# class TestEventHandler(object):
#     def __init__(self, kdip):
#         self.KDIP = kdip
#     # event handler function
#     def datachange_notification(self, node, val, data):
#         if str(node) == "ns=2;s=Robot1_Axis1":
#             print(str(node) + " Received data: ", val)
#             if int(val) == -43:
#                 self.KDIP.TestEvent.set()
#                 self.KDIP.InfluxClient.CreateMeasurement(datetime.now().strftime("%Y%m%d_%H%M%S"))
#
#             elif int(val) == 43:
#                 self.KDIP.TestEvent.clear()
#
# class TestEventHandler2(object):
#     def __init__(self, kdip):
#         self.KDIP = kdip
#
#     def datachange_notification(self, node, val, data):
#         print(str(node) + " Received data: ", val)
#         paramName = None
#         for _name, _node in nodes_test.items():
#             if _node == node:
#                 paramName = _name
#                 break
#         self.KDIP.InfluxClient.InsertPoint(paramName, val, self.KDIP.CurrentLayer, "RobotServerTest", datetime.now())
# -----------------------------------------------------------------------------------------------

class UaClient(object):

    def __init__(self, kdip):
        self.KDIP = kdip
        self.Handles_BuildInfo = []
        self.Handles_EnvLog = []
        self.handles_test1 = []
        self.handles_test2 = []

    def ConnectServer(self, url):
        try:
            self.url = url
            self.client = opcua.Client(url)
            # Connect to Server
            self.client.connect()
            print("Client Connected")
        except:
            print("Except Occurred!")


    def DisconnectServer(self):
            # Disconnect when finish
            self.client.disconnect()

    # -------------------------------- Test Func (Robot Server) --------------------------------

    # def CreateSubscribe(self):
    #     handler = TestEventHandler(self.KDIP)
    #     self.TestSub = self.client.create_subscription(500, handler)
    #
    #     handler = TestEventHandler2(self.KDIP)
    #     self.TestSub2 = self.client.create_subscription(500, handler)
    #
    # def StartTestBuildInfoStream(self):
    #     handle = self.TestSub.subscribe_data_change(nodes_test['Robot1_Axis1'])
    #     self.handles_test1.append(handle)
    #
    # def StartRobotServerStream(self):
    #     for node in nodes_test.values():
    #         self.handles_test2.append(self.TestSub2.subscribe_data_change(node))
    #     self.KDIP.IsBuilding = True
    #
    # def FinishTestBuildInfoStream(self):
    #     for h in self.handles_test1:
    #         self.TestSub.unsubscribe(h)
    #     self.handles_test1.clear()
    #
    # def FinishRobotServerStream(self):
    #     for h in self.handles_test2:
    #         self.TestSub2.unsubscribe(h)
    #     self.handles_test2.clear()
    #     self.KDIP.IsBuilding = False

    # -----------------------------------------------------------------------------
    def CreateSubscribe(self):
        handler = BuildInfoSubEventHandler(self.KDIP)
        self.BuildInfoSub = self.client.create_subscription(1000, handler)

        handler = EnvLogSubEventHandler(self.KDIP)
        self.EnvLogSub = self.client.create_subscription(1000, handler)

    def StartEnvLogStream(self):
        print("Start Log Data Stream")
        for node in nodes_Environment.values():
            self.Handles_EnvLog.append(self.EnvLogSub.subscribe_data_change(node))

        for node in nodes_InertGas.values():
            self.Handles_EnvLog.append(self.EnvLogSub.subscribe_data_change(node))

        for node in nodes_PowderBed.values():
            self.Handles_EnvLog.append(self.EnvLogSub.subscribe_data_change(node))

        for node in nodes_ScanField.values():
            self.Handles_EnvLog.append(self.EnvLogSub.subscribe_data_change(node))

        self.KDIP.IsBuilding = True

    def StartBuildInfoStream(self):
        print("Start BuildInfo Data Stream")
        for node in nodes_BuildProcess.values():
            self.Handles_BuildInfo.append(self.EnvLogSub.subscribe_data_change(node))

    def FinishEnvLogStream(self):
        for h in self.Handles_EnvLog:
            self.EnvLogSub.unsubscribe(h)
        # handle array 초기화 ★중요★
        self.Handles_EnvLog.clear()
        self.KDIP.IsBuilding = False

    def FinishBuildInfoStream(self):
        for h in self.Handles_BuildInfo:
            self.BuildInfoSub.unsubscribe(h)
            # handle array 초기화 ★중요★
        self.Handles_BuildInfo.clear()


    def SetUaNodes(self):
        # _COMMON__ 5개
        nodes_BuildInfo['ServerStatus'] = self.client.get_node("i=2256")
        nodes_BuildInfo['CurrentLayer'] = self.client.get_node("ns=2;s=Services.Scan System.Current Layer")
        nodes_BuildInfo['TotalLayers'] = self.client.get_node("ns=2;s=Services.Scan System.Total Layers")
        nodes_BuildInfo['JobFile'] = self.client.get_node("ns=2;s=Services.Scan System.JobFile")
        nodes_BuildInfo['JobId'] = self.client.get_node("ns=2;s=Services.Scan System.JobID")

        # __Build Process__ 15개
        nodes_BuildProcess['Command'] = self.client.get_node("ns=2;s=Services.Scan System.Command")
        nodes_BuildProcess['CurrentHeight'] = self.client.get_node("ns=2;s=Services.Scan System.CurrentHeight")
        nodes_BuildProcess['SystemStatus'] = self.client.get_node("ns=2;s=Services.Scan System.Status")
        nodes_BuildProcess['RecoatPlatformPosition'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.PlatformPosition""")
        nodes_BuildProcess['RecoatRecoaterPosition'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.RecoaterPosition""")
        nodes_BuildProcess['StartBuildTime'] = self.client.get_node("ns=2;s=User Channels.MCP Interface.""MCP Interface.StartBuildTime""")
        nodes_BuildProcess['ElapsedBuildTime'] = self.client.get_node("ns=2;s=User Channels.MCP Interface.""MCP Interface.ElapsedBuildTime""")
        nodes_BuildProcess['MachineState'] = self.client.get_node("ns=2;s=User Channels.Supervisor.""Supervisor.Machine State""")
        nodes_BuildProcess['RemainingScanTime'] = self.client.get_node("ns=2;s=Services.Scan System.""Scan System.Remaining Scan Time""")
        nodes_BuildProcess['ChamberLock'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Chamber Lock.DO23""")
        nodes_BuildProcess['DoorInterlock'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Door Interlock.DI1""")
        nodes_BuildProcess['EmergencyStop'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""EmergencyStop.DI0""")
        nodes_BuildProcess['HopperPowder'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Hopper Powder.DI4""")
        nodes_BuildProcess['RecyclePowderB'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Recycle Powder B.DI6""")
        nodes_BuildProcess['RecyclePowderF'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""RecyclePowderF.DI5""")

        # __Environment Parameter__ 10개
        nodes_Environment['OxygenHighChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Oxygen Chamber High.AI3""")
        nodes_Environment['OxygenLowChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Oxygen Chamber Low.AI4""")
        nodes_Environment['PressureChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Chamber.AI5""")
        nodes_Environment['PressurePostFilter'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Post Filter.AI7""")
        nodes_Environment['PressurePreFilter'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Pre Filter.AI7""")
        nodes_Environment['TemperatureBuildplate'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Buildplate.AI1""")
        nodes_Environment['TemperatureChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Chamber.AI0""")
        nodes_Environment['TemperatureHopper'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Hopper.AI2""")
        nodes_Environment['BuildplateHeaterControl'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Buildplate Heater Control.AO2""")
        nodes_Environment['HopperHeaterControl'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Hopper Heater Control.AO3""")

        # __Inert_Gas__15개
        nodes_InertGas['GasControlThresholdA'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdA""")
        nodes_InertGas['GasControlThresholdB'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdB""")
        nodes_InertGas['GasControlHysterisis'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Hysterisis""")
        nodes_InertGas['GasControlVirtualOxygenValue'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.VirtualOxygenValue""")
        nodes_InertGas['GasControlEMCYStatus'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.EMCYStatus""")
        nodes_InertGas['GasControlCommand'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Command""")
        nodes_InertGas['GasControlFeedback'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Feedback""")
        nodes_InertGas['GasControlManual'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Manual""")
        nodes_InertGas['GasControlStatus'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Status""")
        nodes_InertGas['ValveCirculation'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Circulation.DO1""")
        nodes_InertGas['ValveFume'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Fume.DO3""")
        nodes_InertGas['ValveInlet'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Inlet.DO0""")
        nodes_InertGas['ValveOutlet'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Outlet.DO4""")
        nodes_InertGas['ValveVentilation'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Ventilation.DO2""")
        nodes_InertGas['PumpSwitch'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Pump Switch.D11""")

        # __Powder_Bed__34개
        nodes_PowderBed['BuildplateMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Feedback")
        nodes_PowderBed['BuildplateMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Request")
        nodes_PowderBed['BuildplateMotionSpeedFeedback'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Feedback")
        nodes_PowderBed['BuildplateMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Request")
        nodes_PowderBed['BuildplateMotionStatus'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Status")
        nodes_PowderBed['MaterialMotionCommand'] = self.client.get_node("ns=2;s=Components.Material Motion.Command")
        nodes_PowderBed['MaterialMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Material Motion.Position Feedback")
        nodes_PowderBed['MaterialMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Material Motion.Position Request")
        nodes_PowderBed['MaterialMotionSpeedFeedback'] = self.client.get_node("ns=2;s=Components.Material Motion.Speed Feedback")
        nodes_PowderBed['MaterialMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Material Motion.Speed Request")
        nodes_PowderBed['MaterialMotionStatus'] = self.client.get_node("ns=2;s=Components.Material Motion.Status")
        nodes_PowderBed['RecoaterMotionCommand'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Command")
        nodes_PowderBed['RecoaterMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Position Feedback")
        nodes_PowderBed['RecoaterMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Position Request")
        nodes_PowderBed['RecoaterMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Speed Request")
        nodes_PowderBed['RecoaterMotionStatus'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Status")
        nodes_PowderBed['RecoatAmount'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Amount""")
        nodes_PowderBed['RecoatCommandMonitored'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Command""")
        nodes_PowderBed['RecoatFirstLayerAmount'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerAmount""")
        nodes_PowderBed['RecoatFirstLayerSpeed'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerSpeed""")
        nodes_PowderBed['RecoatFirstLayerThickness'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerThickness""")
        nodes_PowderBed['RecoatLayerStartTime'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.LayerStartTime""")
        nodes_PowderBed['RecoatLayerThickness'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.LayerThickness""")
        nodes_PowderBed['RecoatMode'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Mode""")
        nodes_PowderBed['RecoatRecoatingSpeed'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.RecoatingSpeed""")
        nodes_PowderBed['RecoatStatus'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Status""")
        nodes_PowderBed['BuildSettingsFeederDosage'] = self.client.get_node("ns=2;s=User Channels.BuildSettings.""BuildSettings.FeederDosage""")
        nodes_PowderBed['HopperPositionPreset'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Hopper Position Preset.DO16""")
        nodes_PowderBed['LEDDisplay0'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 0.DO17""")
        nodes_PowderBed['LEDDisplay1'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 1.DO18""")
        nodes_PowderBed['LEDDisplay2'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 2.DO19""")
        nodes_PowderBed['LEDDisplay3'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 3.DO20""")
        nodes_PowderBed['LEDDisplay4'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 4.DO21""")
        nodes_PowderBed['LEDDisplay5'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 5.DO22""")



        # __ScanFiled__ 18개
        nodes_ScanField['LaserPowerRequest'] = self.client.get_node("ns=2;s=Components.Analog Laser.Power Request")
        nodes_ScanField['LaserPowerFeedback'] = self.client.get_node("ns=2;s=Components.Analog Laser.Power Feedback")
        nodes_ScanField['LaserGateRequest'] = self.client.get_node("ns=2;s=Components.Analog Laser.Gate Request")
        nodes_ScanField['LaserGateFeedback'] = self.client.get_node("ns=2;s=Components.Analog Laser.Gate Feedback")
        nodes_ScanField['ScanFieldCommand'] = self.client.get_node("ns=2;s=Components.Scan Field.Command")
        nodes_ScanField['ScanFieldSpotSizeFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Spot Size Feedback")
        nodes_ScanField['ScanFieldStatus'] = self.client.get_node("ns=2;s=Components.Scan Field.Status")
        nodes_ScanField['ScanFieldXFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.X Feedback")
        nodes_ScanField['ScanFieldXRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.X Request")
        nodes_ScanField['ScanFieldYFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Y Feedback")
        nodes_ScanField['ScanFieldYRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.Y Request")
        nodes_ScanField['ScanFieldZFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Z Feedback")
        nodes_ScanField['ScanFieldZRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.Z Request")
        nodes_ScanField['LightSwitch'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Light Switch.DO10""")
        nodes_ScanField['LaserRemoteSwitch'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Remote Switch.DO6""")
        nodes_ScanField['LaserRemoteStart'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Remote Start.DO7""")
        nodes_ScanField['LaserEmission'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Emission.DO8""")
        nodes_ScanField['LaserGuideBeam'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Guide Beam.DO9""")


        nodes_test['Robot1_Axis1'] = self.client.get_node("ns=2;s=Robot1_Axis1")
        nodes_test['Robot1_Axis2'] = self.client.get_node("ns=2;s=Robot1_Axis2")
        nodes_test['Robot1_Axis3'] = self.client.get_node("ns=2;s=Robot1_Axis3")
        nodes_test['Robot1_Axis4'] = self.client.get_node("ns=2;s=Robot1_Axis4")

        # while event.is_set():
        #     # print(f'Root node is {root}')
        #
        #     timestamp = datetime.now()
        #
        #     # value_CurrentLayer = node_CurrentLayer.get_value()
        #     # value_TotalLayer = node_TotalLayer.get_value()
        #     # value_JobFile = node_JobFile.get_value()
        #     # value_JobID = node_JobID.get_value()
        #     #
        #     # InfluxDBHelper.InsertPoint("Robot1_Axis1", value_CurrentLayer, 1, "INERTGAS", timestamp)
        #     # InfluxDBHelper.InsertPoint("Robot1_Axis2", value_TotalLayer, 1, "ENVIRONMENT", timestamp)
        #     # InfluxDBHelper.InsertPoint("Robot1_Axis3", value_JobFile, 1, "POWDERED", timestamp)
        #     # InfluxDBHelper.InsertPoint("Robot1_Axis4", value_JobID, 1, "SCANFIELD", timestamp)
        #
        #     time.sleep(1)
        #
        # print("Finished OPCUA EVLog Stream")

# # Read node
# Robot1_Axis1 = client.get_node("ns=2;s=Robot1_Axis1")
# Robot1_Axis2 = client.get_node("ns=2;s=Robot1_Axis2")
# Robot1_Axis3 = client.get_node("ns=2;s=Robot1_Axis3")
# Robot1_Axis4 = client.get_node("ns=2;s=Robot1_Axis4")
#
# value1 = Robot1_Axis1.get_value()
# value2 = Robot1_Axis2.get_value()
# value3 = Robot1_Axis3.get_value()
# value4 = Robot1_Axis4.get_value()
#
# # Print Value
# # print(f'Value of Robot1_Axis1 :{value1}')  # Get and print only value of the node
# # print(f'Value of Robot1_Axis2 :{value2}')  # Get and print only value of the node
# # print(f'Value of Robot1_Axis3 :{value3}')  # Get and print only value of the node
# # print(f'Value of Robot1_Axis4 :{value4}')  # Get and print only value of the node
#
# InfluxDBHelper.InsertPoint("Robot1_Axis1", value1, 1, "INERTGAS")
# InfluxDBHelper.InsertPoint("Robot1_Axis2", value2, 1, "ENVIRONMENT")
# InfluxDBHelper.InsertPoint("Robot1_Axis3", value3, 1, "POWDERED")
# InfluxDBHelper.InsertPoint("Robot1_Axis4", value4, 1, "SCANFIELD")

# # Optional if you already knew node's id
# root = client.get_root_node()
# print(f'Root node is {root}')
#
# # Read node
# var = client.get_node("ns=2;i=2")
#
# # Print Value
# print(f'Value of node :{var.get_value()}')  # Get and print only value of the node
# print(f'Full value of node : {var.get_data_value()}')  # Get and print full value of the node
#
# # Write Value
# var.set_value(1.3)  # Set value into 1.3
# print(f'New value is : {var.get_value()}')  # Get and print full value of the node