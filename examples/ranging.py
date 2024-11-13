# ANT+ - Stride Based Speed and Distance Sensor Example
#
# SDM demo working with OpenAnt Library (https://github.com/Tigge/openant)
# using feature of:
# - acting as Transmitting Device (TX-Broadcast)
# - gracefully close ANT-Channels
#
# For further details on Speed & Distance Sensor, check out the thisisant.com webpage

import logging
import time

from openant.easy.node import Node
from openant.easy.channel import Channel
from openant.base.commons import format_list

# Definition of Variables
NETWORK_KEY = [0xE8, 0xE4, 0x33, 0xA9, 0xDD, 0x56, 0xC1, 0x43]
Device_Type = 16  # 124 = Stride & Distance Sensor
Device_Number = 12345  # Change if you need.
Channel_Period = 8192
Channel_Frequency = 66

##########################################################################


class AntSendDemo:
    def __init__(self):

        self.ANTMessageCount = 0
        self.ANTMessagePayload = [0, 0, 0, 0, 0, 0, 0, 0]

    def Create_Next_DataPage(self):
        # Define Variables
        self.ANTMessageCount += 1
        
        self.ANTMessagePayload = [0x31, self.ANTMessageCount, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            # ANTMessageCount reset
        if self.ANTMessageCount >=255:
            self.ANTMessageCount = 0

        return self.ANTMessagePayload

    # TX Event
    def on_data(self, data):
        print("callback")
        # ANTMessagePayload = self.Create_Next_DataPage()
        # page = data[0]

        # if page == 80: # manufacturer
        #     print("Manifacturer data ")
        # elif page == 81:
        #     print("Acknowledgement ")
        # elif (page & 0x0F) <= 7:
        #     distance = data[6]
        #     print(f"distance : {distance} cm")

        # print(f"on_data: {data}")
        # #self.ActualTime = time.time() - self.TimeProgramStart

        # # ANTMessagePayload = array.array('B', [1, 255, 133, 128, 8, 0, 128, 0])    # just for Debuggung pourpose
        # print(self.ANTMessagePayload)
        # if self.ANTMessageCount%20 == 0:
        #     self.channel.send_acknowledged_data(self.ANTMessagePayload) 
        #  # Final call for broadcasting data
        # print(
        #     self.ActualTime,
        #     "TX:",
        #     Device_Number,
        #     ",",
        #     Device_Type,
        #     ":",
        #     format_list(ANTMessagePayload),
        # )

    # Open Channel
    def OpenChannel(self):

        self.node = Node()  # initialize the ANT+ device as node

        # CHANNEL CONFIGURATION
        self.node.set_network_key(0x00, NETWORK_KEY)  # set network key
        self.channel = self.node.new_channel(Channel.Type.BIDIRECTIONAL_RECEIVE) 
        # self.channel.set_id(
        #     Device_Number, Device_Type, 5
        # )  # set channel id as <Device Number, Device Type, Transmission Type>
        self.channel.set_period(Channel_Period)  # set Channel Period
        self.channel.set_rf_freq(Channel_Frequency)  # set Channel Frequency
        self.channel.set_search_timeout(12)
        self.channel.set_id(0, 16, 0)
        print("Starting a node")
        # Callback function for each TX event
        # self.channel.on_broadcast_data = self.on_data
        # self.channel.on_burst_data = self.on_data

        self.channel.open()  # Open the ANT-Channel with given configuration
        self.start_frame = 0
        data = self.node.start(self.start_frame, True)
        print(data)
        self.start_frame = data[5]
        time.sleep(4)
        try:
            while True:
                self.Create_Next_DataPage()
                print(f"frame: {self.ANTMessagePayload}")
                self.channel.send_acknowledged_data(self.ANTMessagePayload)
                data = self.node.start(self.start_frame)
                self.start_frame = data[5]
                dist = ( data[7] <<8 | data[6])
                print(f"data: {data}")
                print(f"distance: {dist}")
                print("\n")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Closing ANT+ Channel...")
            self.channel.close()
            self.node.stop()
        finally:
            print("Final checking...")
            # not sure if there is anything else we should check?! :)


###########################################################################################################################
def main():
    print("ANT+ Ranging Demo")
    logging.basicConfig(
        filename="example.log", level=logging.DEBUG
    )  # just for Debugging purpose, outcomment this in live version

    ant_senddemo = AntSendDemo()

    try:
        ant_senddemo.OpenChannel()  # start
    except KeyboardInterrupt:
        print("Closing ANT+ Channel!")
    finally:
        print("Finally...")
        logging.shutdown()  # Shutdown Logger

    print("Close demo...")


if __name__ == "__main__":
    main()
