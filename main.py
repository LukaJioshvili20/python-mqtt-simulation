import threading
import time

from broker import MQTTManager
from devices import (
    DoorSensor,
    IndoorSensor,
    LightSwitch,
    VacuumCleaner,
)
from menu import DeviceSelector
from simulation import (
    IndoorSensorSimulation,
    LightSwitchSimulation,
    OutdoorSensorSimulation,
    VacuumCleanerSimulation,
    DoorSensorSimulation,
)


def main():
    """
    Main function to initialize the MQTT manager, handle user input, and control simulations.
    """
    print("=== MQTT Broker Connection ===")

    # Step 1: Initialize the MQTT Manager (prompts user for broker details)
    mqtt_manager = MQTTManager()
    mqtt_manager.connect()
    mqtt_manager.start()

    time.sleep(2)

    # Home Doors
    door_sensor = DoorSensor("group1", "device1", mqtt_manager)

    # Temp x Humidity Sensors
    indoor_sensor = IndoorSensor("group2", "device3", mqtt_manager)
    outdoor_sensor = IndoorSensor("group2", "device4", mqtt_manager)

    # Light switched
    light_switch = LightSwitch("group3", "device5", mqtt_manager)

    # Vacuum Cleaner
    vacuum_cleaner = VacuumCleaner("group4", "device7", mqtt_manager)

    door_sensor.power_on()
    indoor_sensor.power_on()
    outdoor_sensor.power_on()
    light_switch.power_on()
    vacuum_cleaner.power_on()

    time.sleep(2)

    selection = DeviceSelector()
    device_selected = selection.get_selection()

    # Devices and their corresponding simulation classes
    device_simulations = {
        "Door Sensor": (door_sensor, DoorSensorSimulation),
        "Indoor Sensor": (indoor_sensor, IndoorSensorSimulation),
        "Outdoor Sensor": (outdoor_sensor, OutdoorSensorSimulation),
        "Light Switch": (light_switch, LightSwitchSimulation),
        "Vacuum Cleaner": (vacuum_cleaner, VacuumCleanerSimulation),
    }

    if device_selected == "All devices":
        print("Starting simulation for all devices... Press Ctrl+C to stop.")
        threads = []
        for device_name, (device, simulation_class) in device_simulations.items():
            # Create a thread for each device simulation
            thread = threading.Thread(
                target=start_simulation, args=(device, simulation_class, mqtt_manager)
            )
            thread.daemon = True  # Allows threads to exit when the main program exits
            threads.append(thread)
            thread.start()

        # Keep the main thread alive
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\nSimulation interrupted by user.")
    else:
        # Single device simulation
        device, simulation_class = device_simulations[device_selected]
        simulation = simulation_class(device, mqtt_manager)
        simulation.simulate()

    mqtt_manager.stop()


def start_simulation(device, simulation_class, mqtt_manager):
    """
    Start simulation for a single device in a thread.

    Args:
        device: The device instance.
        simulation_class: The simulation class to use.
        mqtt_manager: The MQTTManager instance.
    """
    simulation = simulation_class(device, mqtt_manager)
    simulation.simulate()


if __name__ == "__main__":
    main()
