from opcua import Client
from helper import InfluxDBHelper
from threading import Event
from datetime import datetime
import time

event = Event()
# url = "opc.tcp://localhost:26543"
# client = Client(url)


class UaClient(object):

    def __init__(self, url):
        self.client = Client(url)


    def _reset(self):
        self.client = None

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



    def StartBuildInfoDataStream(self):
        # Start OPCUA Data Channel
        print("Start OPCUA Stream")

        # Optional if you already knew node's id
        root = self.client.get_root_node()

        # Read node
        node_CurrentLayer = self.client.get_node("ns=2;s=Services.Scan System.Current Layer")
        node_TotalLayer = self.client.get_node("ns=2;s=Services.Scan System.Total Layers")
        node_JobFile = self.client.get_node("ns=2;s=Services.Scan System.JobFile")
        node_JobID = self.client.get_node("ns=2;s=Services.Scan System.JobID")


        while event.is_set():
            # print(f'Root node is {root}')

            timestamp = datetime.now()

            value_CurrentLayer = node_CurrentLayer.get_value()
            value_TotalLayer = node_TotalLayer.get_value()
            value_JobFile = node_JobFile.get_value()
            value_JobID = node_JobID.get_value()


            InfluxDBHelper.InsertPoint("Robot1_Axis1", value_CurrentLayer, 1, "INERTGAS", timestamp)
            InfluxDBHelper.InsertPoint("Robot1_Axis2", value_TotalLayer, 1, "ENVIRONMENT", timestamp)
            # InfluxDBHelper.InsertPoint("Robot1_Axis3", value_JobFile, 1, "POWDERED", timestamp)
            # InfluxDBHelper.InsertPoint("Robot1_Axis4", value_JobID, 1, "SCANFIELD", timestamp)

            time.sleep(1)

        print("Finished OPCUA Stream")



    # InfluxDB에 넣어야함.
    def StartEnvDataStream(self):

        # __Environment Parameter__
        node_OxygenLowChamber = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Oxygen Chamber Low.AI4""")
        node_PressureChamber = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Chamber.AI5""")
        node_PressurePostFilter = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Post Filter.AI7""")
        node_PressurePreFilter = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Pressure Pre Filter.AI7""")
        node_TemperatureBuildplate = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Buildplate.AI1""")
        node_TemperatureChamber = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Chamber.AI0""")
        node_TemperatureHopper = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Temperature Hopper.AI2""")
        node_BuildplateHeaterControl = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Buildplate Heater Control.AO2""")
        node_HopperHeaterControl = self.client.get_node("ns=2;s=Targets.Target_0.Analog Input.""Hopper Heater Control.AO3""")


        # __Inert_Gas__
        node_GasControlThresholdA = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdA""")
        node_GasControlThresholdB = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.ThresholdB""")
        node_GasControlHysterisis = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Hysterisis""")
        node_GasControlVirtualOxygenValue = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.VirtualOxygenValue""")
        node_GasControlEMCYStatus = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.EMCYStatus""")
        node_GasControlCommand = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Command""")
        node_GasControlFeedback = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Feedback""")
        node_GasControlManual = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Manual""")
        node_GasControlStatus = self.client.get_node("ns=2;s=User Channels.GasControl.""GasControl.Status""")
        node_ValveCirculation = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Circulation.DO1""")
        node_ValveFume = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Fume.DO3""")
        node_ValveInlet = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Inlet.DO0""")
        node_ValveOutlet = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Outlet.DO4""")
        node_ValveVentilation = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Valve Ventilation.DO2""")
        node_PumpSwitch = self.client.get_node("ns=2;s=TargetsTarget_0.Digital Output.""Pump Switch.D11""")


        # __Powder_Bed__
        node_BuildplateMotionPositionFeedback = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Feedback")
        node_BuildplateMotionPositionRequest = self.client.get_node("ns=2;s=Components.Buildplate Motion.Position Request")
        node_BuildplateMotionSpeedFeedback = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Feedback")
        node_BuildplateMotionSpeedRequest = self.client.get_node("ns=2;s=Components.Buildplate Motion.Speed Request")
        node_BuildplateMotionStatus = self.client.get_node("ns=2;s=Components.Buildplate Motion.Status")
        node_MaterialMotionCommand = self.client.get_node("ns=2;s=Components.Material Motion.Command")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")
        node_ = self.client.get_node("")

        while event.is_set():
            # print(f'Root node is {root}')

            timestamp = datetime.now()

            # value_CurrentLayer = node_CurrentLayer.get_value()
            # value_TotalLayer = node_TotalLayer.get_value()
            # value_JobFile = node_JobFile.get_value()
            # value_JobID = node_JobID.get_value()
            #
            # InfluxDBHelper.InsertPoint("Robot1_Axis1", value_CurrentLayer, 1, "INERTGAS", timestamp)
            # InfluxDBHelper.InsertPoint("Robot1_Axis2", value_TotalLayer, 1, "ENVIRONMENT", timestamp)
            # InfluxDBHelper.InsertPoint("Robot1_Axis3", value_JobFile, 1, "POWDERED", timestamp)
            # InfluxDBHelper.InsertPoint("Robot1_Axis4", value_JobID, 1, "SCANFIELD", timestamp)

            time.sleep(1)

        print("Finished OPCUA Stream")
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