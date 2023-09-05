import simpy
import random

# Define RoCEv2 packet types
class RoCEv2Packet:
    def __init__(self, packet_type, payload):
        self.packet_type = packet_type
        self.payload = payload

# Define a simple WRED class
class WRED:
    def __init__(self, min_threshold, max_threshold, max_probability):
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.max_probability = max_probability

    def drop_packet(self, queue_size):
        if queue_size <= self.min_threshold:
            return False
        elif queue_size >= self.max_threshold:
            return True
        else:
            probability = (queue_size - self.min_threshold) / (self.max_threshold - self.min_threshold)
            return random.random() < probability * self.max_probability

def rocev2_sender(env, receiver):
    while True:
        # Simulate sending RoCEv2 packets
        packet_type = random.choice(["Data", "Ack", "Error"])
        payload = f"Data Payload" if packet_type == "Data" else None
        packet = RoCEv2Packet(packet_type, payload)
        print(f"Sending {packet.packet_type} packet")
        receiver.put(packet)  # Send packet to the receiver
        yield env.timeout(1)  # Adjust the time interval for traffic generation

def rocev2_receiver(env, switch, wred):
    while True:
        # Receive and process RoCEv2 packets
        packet = yield switch.get()
        print(f"Received {packet.packet_type} packet")

        if packet.packet_type == "Error":
            # Simulate error handling
            print("Error detected. Initiating error recovery...")
            yield env.timeout(5)  # Simulate error recovery time
            print("Error recovery complete.")
        else:
            # Process normal packets
            yield env.timeout(1)  # Adjust processing time

# Create a SimPy environment
env = simpy.Environment()

# Create a shared event for sender and receiver
receiver = simpy.Store(env)

# Create RoCEv2 sender process
env.process(rocev2_sender(env, receiver))

# Create RoCEv2 receiver process
env.process(rocev2_receiver(env, receiver, None))  # Note: WRED not used in receiver

# Run the simulation for a specified duration
env.run(until=20)  # Adjust the simulation duration as needed
