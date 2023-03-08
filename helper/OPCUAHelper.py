import opcua
from threading import Event
from opcua import Client
from helper import InfluxDBHelper
from datetime import datetime

nodes_build_info = {}
nodes_ev_log = {}
nodes_test = {}
# test_event = Event()
BuildingEvent = Event()
global IsBuilding

class BuildInfoSubEventHandler(object):
    def datachange_notification(self, node, val, data):
        if str(node) == "ns=2;s=Services.Scan System.Current Layer":
            if val != 0:
                BuildingEvent.set()
            else:
                BuildingEvent.clear()

class EnvLogSubEventHandler(object):
    def datachange_notification(self, node, val, data):
        print(str(node) + " : ", val)


# -------------------------------- Test Class (For Robot Server) --------------------------------
# class TestEventHandler(object):
#     # event handler function
#     def datachange_notification(self, node, val, data):
#         if str(node) == "ns=2;s=Robot1_Axis1":
#             print(str(node) + " Received data: ", val)
#             if int(val) == -43:
#                 test_event.set()
#             elif int(val) == 43:
#                 test_event.clear()
#
# class TestEventHandler2(object):
#     def datachange_notification(self, node, val, data):
#         print(str(node) + " Received data: ", val)
# -----------------------------------------------------------------------------------------------



class UaClient(object):

    def __init__(self, url):
        self.url = url
        self.client = opcua.Client(url)
        self.current_layer = 0
        self.total_layer = 0
        self.handles_build_info = []
        self.handles_env_log = []
        # self.handles_test1 = []
        # self.handles_test2 = []

    def ConnectServer(self):
        try:
            # Connect to Server
            self.client.connect()
            print("Client Connected")
        except:
            print("Except Occurred!")


    def DisconnectServer(self):
            # Disconnect when finish
            self.client.disconnect()

    # -------------------------------- Test Func (Robot Server) --------------------------------

    # def CreateTestBuildInfoSubscribe(self):
    #     handler = TestEventHandler()
    #     self.sub = self.client.create_subscription(500, handler)
    #
    # def CreateRobotServerSubscribe(self):
    #     handler = TestEventHandler2()
    #     self.sub2 = self.client.create_subscription(500, handler)
    #
    # def StartTestBuildInfoStream(self):
    #     handle = self.sub.subscribe_data_change(nodes_test['Robot1_Axis1'])
    #     self.handles_test1.append(handle)
    #
    # def StartRobotServerStream(self):
    #     self.handles_test2.clear()
    #
    #     for node in nodes_test.values():
    #         self.handles_test2.append(self.sub2.subscribe_data_change(node))
    #     global IsBuilding
    #     IsBuilding = True
    #
    #     # InfluxDBHelper.InsertPoint("Robot1_Axis1", value1, 1, "INERTGAS")
    #     # InfluxDBHelper.InsertPoint("Robot1_Axis2", value2, 1, "ENVIRONMENT")
    #     # InfluxDBHelper.InsertPoint("Robot1_Axis3", value3, 1, "POWDERED")
    #     # InfluxDBHelper.InsertPoint("Robot1_Axis4", value4, 1, "SCANFIELD")
    #
    # def FinishTestBuildInfoStream(self):
    #     for h in self.handles_test1:
    #         self.sub.unsubscribe(h)
    #
    # def FinishRobotServerStream(self):
    #     global IsBuilding
    #     for h in self.handles_test2:
    #         self.sub2.unsubscribe(h)
    #     IsBuilding = False

    # -----------------------------------------------------------------------------
    def CreateEnvLogSubscribe(self):
        handler = EnvLogSubEventHandler()
        self.EnvLogSub = self.client.create_subscription(1000, handler)

    def CreateBuildInfoSubscribe(self):
        handler = BuildInfoSubEventHandler()
        self.BuildInfoSub = self.client.create_subscription(1000, handler)

    def StartEnvLogStream(self):
        print("Start OPC-UA EnvLog Data Stream")
        for node in nodes_ev_log.values():
            self.handles_env_log.append(self.EnvLogSub.subscribe_data_change(node))

    def StartBuildInfoStream(self):
        print("Start OPC-UA BuildInfo Data Stream")
        for node in nodes_build_info.values():
            self.handles_build_info.append(self.EnvLogSub.subscribe_data_change(node))

    def FinishEnvLogStream(self):
        global IsBuilding
        for h in self.handles_env_log:
            self.EnvLogSub.unsubscribe(h)
        # handle array 초기화 ★중요★
        self.handles_env_log.clear()
        IsBuilding = False

    def FinishBuildInfoStream(self):
        for h in self.handles_build_info:
            self.BuildInfoSub.unsubscribe(h)
            # handle array 초기화 ★중요★
        self.handles_build_info.clear()


    def SetUaNodes(self):
        # _COMMON__ 3개
        nodes_build_info['ServerStatus'] = self.client.get_node("i=2256")
        nodes_build_info['CurrentLayer'] = self.client.get_node("ns=2;s=Services.Scan System.Current Layer")
        nodes_build_info['TotalLayers'] = self.client.get_node("ns=2;s=Services.Scan System.Total Layers")

        # __Build Process__ 17개
        nodes_build_info['JobFile'] = self.client.get_node("ns=2;s=Services.Scan System.JobFile")
        nodes_build_info['JobId'] = self.client.get_node("ns=2;s=Services.Scan System.JobID")
        nodes_build_info['Command'] = self.client.get_node("ns=2;s=Services.Scan System.Command")
        nodes_build_info['CurrentHeight'] = self.client.get_node("ns=2;s=Services.Scan System.CurrentHeight")
        nodes_build_info['SystemStatus'] = self.client.get_node("ns=2;s=Services.Scan System.Status")
        nodes_build_info['RecoatPlatformPosition'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.PlatformPosition""")
        nodes_build_info['RecoatRecoaterPosition'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.RecoaterPosition""")
        nodes_build_info['StartBuildTime'] = self.client.get_node("ns=2;s=User Channels.MCP Interface.""MCP Interface.StartBuildTime""")
        nodes_build_info['ElapsedBuildTime'] = self.client.get_node("ns=2;s=User Channels.MCP Interface.""MCP Interface.ElapsedBuildTime""")
        nodes_build_info['MachineState'] = self.client.get_node("ns=2;s=User Channels.Supervisor.""Supervisor.Machine State""")
        nodes_build_info['RemainingScanTime'] = self.client.get_node("ns=2;s=Services.Scan System.""Scan System.Remaining Scan Time""")
        nodes_build_info['ChamberLock'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Chamber Lock.DO23""")
        nodes_build_info['DoorInterlock'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Door Interlock.DI1""")
        nodes_build_info['EmergencyStop'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""EmergencyStop.DI0""")
        nodes_build_info['HopperPowder'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Hopper Powder.DI4""")
        nodes_build_info['RecyclePowderB'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""Recycle Powder B.DI6""")
        nodes_build_info['RecyclePowderF'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Input.""RecyclePowderF.DI5""")

        # __Environment Parameter__ 10개
        nodes_ev_log['OxygenHighChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Oxygen Chamber High.AI3""")
        nodes_ev_log['OxygenLowChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Oxygen Chamber Low.AI4""")
        nodes_ev_log['PressureChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Chamber.AI5""")
        nodes_ev_log['PressurePostFilter'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Post Filter.AI7""")
        nodes_ev_log['PressurePreFilter'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Pre Filter.AI7""")
        nodes_ev_log['TemperatureBuildplate'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Buildplate.AI1""")
        nodes_ev_log['TemperatureChamber'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Chamber.AI0""")
        nodes_ev_log['TemperatureHopper'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Hopper.AI2""")
        nodes_ev_log['BuildplateHeaterControl'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Buildplate Heater Control.AO2""")
        nodes_ev_log['HopperHeaterControl'] = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Hopper Heater Control.AO3""")

        # __Inert_Gas__15개
        nodes_ev_log['GasControlThresholdA'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdA""")
        nodes_ev_log['GasControlThresholdB'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdB""")
        nodes_ev_log['GasControlHysterisis'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Hysterisis""")
        nodes_ev_log['GasControlVirtualOxygenValue'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.VirtualOxygenValue""")
        nodes_ev_log['GasControlEMCYStatus'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.EMCYStatus""")
        nodes_ev_log['GasControlCommand'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Command""")
        nodes_ev_log['GasControlFeedback'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Feedback""")
        nodes_ev_log['GasControlManual'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Manual""")
        nodes_ev_log['GasControlStatus'] = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Status""")
        nodes_ev_log['ValveCirculation'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Circulation.DO1""")
        nodes_ev_log['ValveFume'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Fume.DO3""")
        nodes_ev_log['ValveInlet'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Inlet.DO0""")
        nodes_ev_log['ValveOutlet'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Outlet.DO4""")
        nodes_ev_log['ValveVentilation'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Ventilation.DO2""")
        nodes_ev_log['PumpSwitch'] = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Pump Switch.D11""")

        # __Powder_Bed__34개
        nodes_ev_log['BuildplateMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Feedback")
        nodes_ev_log['BuildplateMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Request")
        nodes_ev_log['BuildplateMotionSpeedFeedback'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Feedback")
        nodes_ev_log['BuildplateMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Request")
        nodes_ev_log['BuildplateMotionStatus'] = self.client.get_node("ns=2;s=Components.Buildplate Motion.Status")
        nodes_ev_log['MaterialMotionCommand'] = self.client.get_node("ns=2;s=Components.Material Motion.Command")
        nodes_ev_log['MaterialMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Material Motion.Position Feedback")
        nodes_ev_log['MaterialMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Material Motion.Position Request")
        nodes_ev_log['MaterialMotionSpeedFeedback'] = self.client.get_node("ns=2;s=Components.Material Motion.Speed Feedback")
        nodes_ev_log['MaterialMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Material Motion.Speed Request")
        nodes_ev_log['MaterialMotionStatus'] = self.client.get_node("ns=2;s=Components.Material Motion.Status")
        nodes_ev_log['RecoaterMotionCommand'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Command")
        nodes_ev_log['RecoaterMotionPositionFeedback'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Position Feedback")
        nodes_ev_log['RecoaterMotionPositionRequest'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Position Request")
        nodes_ev_log['RecoaterMotionSpeedRequest'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Speed Request")
        nodes_ev_log['RecoaterMotionStatus'] = self.client.get_node("ns=2;s=Components.Recoater Motion.Status")
        nodes_ev_log['RecoatAmount'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Amount""")
        nodes_ev_log['RecoatCommandMonitored'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Command""")
        nodes_ev_log['RecoatFirstLayerAmount'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerAmount""")
        nodes_ev_log['RecoatFirstLayerSpeed'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerSpeed""")
        nodes_ev_log['RecoatFirstLayerThickness'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.FirstLayerThickness""")
        nodes_ev_log['RecoatLayerStartTime'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.LayerStartTime""")
        nodes_ev_log['RecoatLayerThickness'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.LayerThickness""")
        nodes_ev_log['RecoatMode'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Mode""")
        nodes_ev_log['RecoatRecoatingSpeed'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.RecoatingSpeed""")
        nodes_ev_log['RecoatStatus'] = self.client.get_node("ns=2;s=User Channels.Recoat.""Recoat.Status""")
        nodes_ev_log['BuildSettingsFeederDosage'] = self.client.get_node("ns=2;s=User Channels.BuildSettings.""BuildSettings.FeederDosage""")
        nodes_ev_log['HopperPositionPreset'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Hopper Position Preset.DO16""")
        nodes_ev_log['LEDDisplay0'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 0.DO17""")
        nodes_ev_log['LEDDisplay1'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 1.DO18""")
        nodes_ev_log['LEDDisplay2'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 2.DO19""")
        nodes_ev_log['LEDDisplay3'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 3.DO20""")
        nodes_ev_log['LEDDisplay4'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 4.DO21""")
        nodes_ev_log['LEDDisplay5'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""LED Display 5.DO22""")



        # __ScanFiled__ 18개
        nodes_ev_log['LaserPowerRequest'] = self.client.get_node("ns=2;s=Components.Analog Laser.Power Request")
        nodes_ev_log['LaserPowerFeedback'] = self.client.get_node("ns=2;s=Components.Analog Laser.Power Feedback")
        nodes_ev_log['LaserGateRequest'] = self.client.get_node("ns=2;s=Components.Analog Laser.Gate Request")
        nodes_ev_log['LaserGateFeedback'] = self.client.get_node("ns=2;s=Components.Analog Laser.Gate Feedback")
        nodes_ev_log['ScanFieldCommand'] = self.client.get_node("ns=2;s=Components.Scan Field.Command")
        nodes_ev_log['ScanFieldSpotSizeFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Spot Size Feedback")
        nodes_ev_log['ScanFieldStatus'] = self.client.get_node("ns=2;s=Components.Scan Field.Status")
        nodes_ev_log['ScanFieldXFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.X Feedback")
        nodes_ev_log['ScanFieldXRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.X Request")
        nodes_ev_log['ScanFieldYFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Y Feedback")
        nodes_ev_log['ScanFieldYRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.Y Request")
        nodes_ev_log['ScanFieldZFeedback'] = self.client.get_node("ns=2;s=Components.Scan Field.Z Feedback")
        nodes_ev_log['ScanFieldZRequest'] = self.client.get_node("ns=2;s=Components.Scan Field.Z Request")
        nodes_ev_log['LightSwitch'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Light Switch.DO10""")
        nodes_ev_log['LaserRemoteSwitch'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Remote Switch.DO6""")
        nodes_ev_log['LaserRemoteStart'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Remote Start.DO7""")
        nodes_ev_log['LaserEmission'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Emission.DO8""")
        nodes_ev_log['LaserGuideBeam'] = self.client.get_node("ns=2;s=Targets.Target_0.Digital Output.""Laser Guide Beam.DO9""")


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