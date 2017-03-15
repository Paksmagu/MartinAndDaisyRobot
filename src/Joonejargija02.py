"""
- sensorid reageerivad juba väiksemale tumedusele
- kui läheb juba alla 20 siis pöörab vastavalt
- mõlemad sensorid on valge peal aga üksteise vastas
- valge üle 70
- must alla 12
"""

from ev3dev import ev3
import time


class Robot:

    def __init__(self):
        #self.state = ev3.backspace.process()
        self.motor_left = ev3.LargeMotor("outB")
        self.motor_right = ev3.LargeMotor("outC")
        self.motor_left.reset()
        self.motor_right.reset()
        self.color_sensor = ev3.ColorSensor("in1")
        self.color_sensor2 = ev3.ColorSensor("in4")
        self.color_sensor.mode = "COL-REFLECT"
        self.color_sensor2.mode = "COL-REFLECT"
        self.motor_left.duty_cycle_sp = 15
        self.motor_right.duty_cycle_sp = 15

    def drive(self):
        self.motor_left.run_forever()
        self.motor_right.run_forever()

    def turn(self, direction):
        if direction == "Right":
            self.motor_right.duty_cycle_sp = 0
            self.motor_left.duty_cycle_sp = 15
        elif direction == "Left":
            self.motor_left.duty_cycle_sp = 0
            self.motor_right.duty_cycle_sp = 15

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def sense_reflection(self):
        return self.color_sensor.value(), self.color_sensor2.value()


def main():
    robot = Robot()

    print(robot.sense_reflection())

    try:
        while (True):
            robot.drive()
            time.sleep(0.1)
            reflection = robot.sense_reflection()
            print(robot.sense_reflection())

            if (90 > reflection[0] > 65) and (90 > reflection[1] > 65):
                continue
            elif (reflection[0] <= 20) and (reflection[1] <= 20):
                # kui peab risti olevast mustast üle sõitma
                continue
            elif (12 <= reflection[0] <= 65):
                robot.turn("Left")
            elif (12 <= reflection[1] <= 65):
                robot.turn("Right")

    except KeyboardInterrupt: # press CTRL C to quit
        robot.stop()


if __name__ == "__main__":
    main()
