from opcua import Client
import time




def ConnectServer():
    url = "opc.tcp://localhost:26543"
    client = Client(url)
    try:
        # Initiate

        # Connect to Server
        client.connect()
        print("Client Connected")

        while True:
            # Optional if you already knew node's id
            root = client.get_root_node()
            print(f'Root node is {root}')

            # Read node
            Robot1_Axis1 = client.get_node("ns=2;s=Robot1_Axis1")
            Robot1_Axis2 = client.get_node("ns=2;s=Robot1_Axis2")
            Robot1_Axis3 = client.get_node("ns=2;s=Robot1_Axis3")
            Robot1_Axis4 = client.get_node("ns=2;s=Robot1_Axis4")

            # Print Value
            print(f'Value of Robot1_Axis1 :{Robot1_Axis1.get_value()}')  # Get and print only value of the node
            print(f'Value of Robot1_Axis2 :{Robot1_Axis2.get_value()}')  # Get and print only value of the node
            print(f'Value of Robot1_Axis3 :{Robot1_Axis3.get_value()}')  # Get and print only value of the node
            print(f'Value of Robot1_Axis4 :{Robot1_Axis4.get_value()}')  # Get and print only value of the node

            time.sleep(1)
    finally:
        # Disconnect when finish
        client.disconnect()


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