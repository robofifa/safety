import robot_wheel_speeds_pb2
import paho.mqtt.client as mqtt  # import the client1

received_messages = robot_wheel_speeds_pb2.Robots()
send_messages = robot_wheel_speeds_pb2.Robots()


def on_message(client, userdata, message):
    print("message received ", str(message.payload))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    if message.topic == "RoboFIFA/safety":
        print("parsing packaging message...")
        received_messages.ParseFromString(message.payload)


def main():
    broker_address = "127.0.0.1"
    print("creating new instance")
    client = mqtt.Client("safety")  # create new instance
    client.on_message = on_message  # attach function to callback
    print("connecting to broker")
    client.connect(broker_address, port=1883)  # connect to broker
    client.loop_start()             # start the loop
    print("Subscribing to topic", "RoboFIFA/safety")
    client.subscribe("RoboFIFA/safety")
    try:
        while True:
            while received_messages.robots:
                robot_message = received_messages.robots.pop()
                robot_message.left = robot_message.left if robot_message.left < -1.0 else -1.0
                robot_message.right = robot_message.right if robot_message.right < -1.0 else -1.0
                robot_message.left = robot_message.left if robot_message.left > 1.0 else 1.0
                robot_message.right = robot_message.right if robot_message.right > 1.0 else 1.0
                send_messages.robots.add().CopyFrom(robot_message)
            client.publish("RoboFIFA/packaging", send_messages.SerializeToString())
            send_messages.Clear()
    except KeyboardInterrupt:
        pass
    print("closing robot server")
    print("stop listening for mqtt messages")
    client.loop_stop()  # stop the loop


if __name__ == '__main__':
    main()
