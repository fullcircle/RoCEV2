import simpy
import random


# Define RoCEv2 packet types
class RoCEv2Packet:

  def __init__(self, packet_type, payload):
    self.packet_type = packet_type
    self.payload = payload


def rocev2_sender(env, receiver):
  while True:
    # Simulate sending RoCEv2 packets
    packet_type = random.choice(["Data", "Ack", "Error"])
    payload = f"Data Payload" if packet_type == "Data" else None
    packet = RoCEv2Packet(packet_type, payload)
    print(f"Sending {packet.packet_type} packet")
    receiver.put(packet)  # Send packet to the receiver
    yield env.timeout(1)  # Adjust the time interval for traffic generation


def rocev2_receiver(env):
  while True:
    # Receive and process RoCEv2 packets
    packet = yield receiver.get()
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

# Create RoCEv2 sender and receiver processes
env.process(rocev2_sender(env, receiver))
env.process(rocev2_receiver(env))

# Run the simulation for a specified duration
env.run(until=20)  # Adjust the simulation duration as needed
"""In this extended simulation:

    We've introduced a RoCEv2Packet class to represent RoCEv2 packets with different types (Data, Ack, Error).

    The rocev2_sender process now randomly selects packet types, including "Error" packets, and sends them to the receiver. When an "Error" packet is sent, it simulates an error condition.

    The rocev2_receiver process detects "Error" packets and initiates error recovery, which takes 5 time units in this example. During this time, no normal packet processing occurs.

You can further refine error handling by implementing specific error recovery mechanisms for RoCEv2, such as retransmissions or error correction codes, depending on your simulation objectives. This example provides a foundation for introducing error scenarios and observing how RoCEv2 handles them within your simulation."""
