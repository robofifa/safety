import robot_wheel_speeds_pb2
import paho.mqtt.client as mqtt  # import the client1
from time import sleep


def on_message(client, userdata, message):
    print("message received ", str(message.payload))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def main():
    broker_address = "127.0.0.1"
    print("creating new instance")
    client = mqtt.Client("test_safety")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address, port=1883)  # connect to broker
    client.loop_start()             # start the loop
    print("Subscribing to topic", "RoboFIFA/safety")
    client.subscribe("RoboFIFA/safety")

    robot_messages = robot_wheel_speeds_pb2.Robots()
    robot_message = robot_messages.robots.add()
    robot_message.id = 0
    robot_message.left = 0.0
    robot_message.right = .5
    client.publish("RoboFIFA/safety", robot_message.SerializeToString())
    print("closing robot server")
    print("stop listening for mqtt messages")
    sleep(1)
    client.loop_stop()  # stop the loop


if __name__ == '__main__':
    main()
