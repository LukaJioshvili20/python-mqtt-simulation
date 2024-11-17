import time

import json

class DoorSensorSimulation:
    def __init__(self, door_sensor, mqtt_manager):
        self.door_sensor = door_sensor
        self.mqtt_manager = mqtt_manager

    def simulate(self):
        """Simulate the door sensor and publish its state."""
        while True:
            self.simulate_step()
            time.sleep(20)

    def simulate_step(self):
        """Simulate one step for the door sensor."""

        state = self.door_sensor.generate_state()
        if state['state'] == 'open':
            self.door_sensor.close_door()
        else:
            self.door_sensor.open_door()

        state = self.door_sensor.generate_state()

        topic = f"home/{self.door_sensor.group_id}/{self.door_sensor.device_type}/{self.door_sensor.device_id}/state/update"
        self.mqtt_manager.publish(topic, json.dumps(state))

