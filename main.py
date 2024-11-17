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

    if device_selected == "Door Sensor":
        door_simulation = DoorSensorSimulation(door_sensor, mqtt_manager)
        door_simulation.simulate()
    elif device_selected == "Indoor Sensor":
        indoor_sensor_simulation = IndoorSensorSimulation(indoor_sensor, mqtt_manager)
        indoor_sensor_simulation.simulate()
    elif device_selected == "Outdoor Sensor":
        outdoor_sensor_simulation = OutdoorSensorSimulation(
            outdoor_sensor, mqtt_manager
        )
        outdoor_sensor_simulation.simulate()
    elif device_selected == "Light Switch":
        light_switch_simulation = LightSwitchSimulation(light_switch, mqtt_manager)
        light_switch_simulation.simulate()
    elif device_selected == "Vacuum Cleaner":
        vacuum_cleaner_simulation = VacuumCleanerSimulation(
            vacuum_cleaner, mqtt_manager
        )
        vacuum_cleaner_simulation.simulate()

    mqtt_manager.stop()


if __name__ == "__main__":
    main()
