"""
- soidab mustast joonest paremal
- valge > 70
- must < 11
"""
import time
from ev3dev import ev3


class Robot:
    def __init__(self):
        self.speed = 25
        self.btn = ev3.Button()
        self.gyro = ev3.GyroSensor('in1')
        self.gyro.mode = 'GYRO-ANG'
        self.sonar = ev3.UltrasonicSensor('in4')
        self.sonar.mode = 'US-DIST-CM'
        self.motor_left = ev3.LargeMotor('outB')
        self.motor_right = ev3.LargeMotor('outC')
        self.color_sensor = ev3.ColorSensor('in2')
        self.color_sensor.mode = "COL-REFLECT"  # 0-100

    def drive(self):
        self.motor_left.run_forever(speed_sp=-self.speed)
        self.motor_right.run_forever(speed_sp=-self.speed)

    def turn(self, direction):
        if direction == "right":
            self.motor_right.stop()
            self.motor_left.run_forever(speed_sp=self.speed * 3)
        elif direction == "left":
            self.motor_left.stop()
            self.motor_right.run_forever(speed_sp=self.speed * 3)

    def turn_fast(self, direction):
        if direction == "right":
            self.motor_right.run_forever(speed_sp=-self.speed)
            self.motor_left.run_forever(speed_sp=self.speed)
        elif direction == "left":
            self.motor_left.run_forever(speed_sp=-self.speed)
            self.motor_right.run_forever(speed_sp=self.speed)

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def sense_reflection(self):
        return self.color_sensor.value()


def main():
    robot = Robot()
    try:
        while not robot.btn.any():
            print("SONAR: " + str(robot.sonar.value() / 10))
            print("GYRO: " + str(robot.gyro.value() % 360))
            robot.turn_fast("right")
        robot.stop()
    except KeyboardInterrupt:
        robot.stop()


if __name__ == "__main__":
    main()
