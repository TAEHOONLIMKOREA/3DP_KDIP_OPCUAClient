from opcua import Client
from helper import InfluxDBHelper
from threading import Event
import time

event = Event()
url = "opc.tcp://localhost:26543"
client = Client(url)

def ConnectOPCUAServer():
    try:
        # Connect to Server
        client.connect()
        print("Client Connected")
    except:
        print("Except Occurred!")


def DisconnectOPCUAServer():
        # Disconnect when finish
        client.disconnect()



def StartOPCUAStream():
    # Start OPCUA Data Channel
    print("Start OPCUA Stream")
    while event.is_set():
        # Optional if you already knew node's id
        root = client.get_root_node()
        # print(f'Root node is {root}')

        # Read node
        Robot1_Axis1 = client.get_node("ns=2;s=Robot1_Axis1")
        Robot1_Axis2 = client.get_node("ns=2;s=Robot1_Axis2")
        Robot1_Axis3 = client.get_node("ns=2;s=Robot1_Axis3")
        Robot1_Axis4 = client.get_node("ns=2;s=Robot1_Axis4")

        value1 = Robot1_Axis1.get_value()
        value2 = Robot1_Axis2.get_value()
        value3 = Robot1_Axis3.get_value()
        value4 = Robot1_Axis4.get_value()

        # Print Value
        # print(f'Value of Robot1_Axis1 :{value1}')  # Get and print only value of the node
        # print(f'Value of Robot1_Axis2 :{value2}')  # Get and print only value of the node
        # print(f'Value of Robot1_Axis3 :{value3}')  # Get and print only value of the node
        # print(f'Value of Robot1_Axis4 :{value4}')  # Get and print only value of the node

        InfluxDBHelper.InsertPoint("Robot1_Axis1", value1, 1, "INERTGAS")
        InfluxDBHelper.InsertPoint("Robot1_Axis2", value2, 1, "ENVIRONMENT")
        InfluxDBHelper.InsertPoint("Robot1_Axis3", value3, 1, "POWDERED")
        InfluxDBHelper.InsertPoint("Robot1_Axis4", value4, 1, "SCANFIELD")

        time.sleep(1)

    print("Finished OPCUA Stream")



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