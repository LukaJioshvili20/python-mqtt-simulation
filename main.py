from broker.mqtt_manager import MQTTManager
from menu import DeviceSelector
from simulation.simulation_controller import SimulationController

from devices import DeviceType


def main():
    """
    Main function to initialize the MQTT manager, handle user input, and control simulations.
    """
    print("=== MQTT Broker Connection ===")

    # Step 1: Initialize the MQTT Manager (prompts user for broker details)
    mqtt_manager = MQTTManager()
    mqtt_manager.connect()
    mqtt_manager.start()

    try:
        # Step 2: Display device selection menu
        selector = DeviceSelector()
        selected_device = selector.get_selection()
        print(f"You selected: {selected_device}")

        # Step 3: Initialize the Simulation Controller
        controller = SimulationController(mqtt_manager)

        # Step 4: Power on all devices or the selected device
        if selected_device == "All devices":
            power_on_all_devices(controller, mqtt_manager)
        else:
            power_on_device(controller, selected_device, mqtt_manager)

        # Step 5: Subscribe to appropriate topics
        if selected_device == "All devices":
            # Subscribe to the root topic to listen to all messages
            mqtt_manager.subscribe(
                "home/#", lambda client, userdata, message: print_message(message)
            )
        else:
            # Subscribe to topics for the selected device
            base_topic = f"home/{selected_device.replace(' ', '_').lower()}/#"
            mqtt_manager.subscribe(
                base_topic, lambda client, userdata, message: print_message(message)
            )

        # Step 6: Start the simulation
        if selected_device == "All devices":
            controller.simulate_all_devices()
        else:
            controller.simulate_device(selected_device)
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        # Ensure the MQTT manager is stopped gracefully on exit
        mqtt_manager.stop()


def print_message(message):
    """
    Helper function to print received MQTT messages.

    Args:
        message: The MQTT message object containing topic and payload.
    """
    print(f"Message received on topic '{message.topic}': {message.payload.decode()}")


def power_on_all_devices(controller, mqtt_manager):
    """
    Power on all devices managed by the simulation controller.

    Args:
        controller: The SimulationController instance.
        mqtt_manager: The MQTTManager instance.
    """
    for device_type in DeviceType.list():
        print(f"Powering on {device_type}...")
        device = controller.device_classes[device_type]("home", device_type.lower(), mqtt_manager)
        device.power_on()


def power_on_device(controller, selected_device, mqtt_manager):
    """
    Power on a single selected device.

    Args:
        controller: The SimulationController instance.
        selected_device: The name of the selected device.
        mqtt_manager: The MQTTManager instance.
    """
    print(f"Powering on {selected_device}...")
    device = controller.device_classes[selected_device]("home", selected_device.lower(), mqtt_manager)
    device.power_on()


if __name__ == "__main__":
    main()
