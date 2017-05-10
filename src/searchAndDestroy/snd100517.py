from ev3dev import ev3
from time import *


class Robot:
    def __init__(self):
        self.speed = 50
        self.btn = ev3.Button()
        self.sound = ev3.Sound()
        self.gyro = ev3.GyroSensor('in1')
        self.gyro.mode = 'GYRO-ANG'
        self.sonar = ev3.UltrasonicSensor('in4')
        self.sonar.mode = 'US-DIST-CM'
        self.motor_left = ev3.LargeMotor('outB')
        self.motor_right = ev3.LargeMotor('outC')
        self.color_sensor = ev3.ColorSensor('in2')
        self.color_sensor.mode = "COL-REFLECT"  # 0-100

    def drive(self):
        self.motor_left.run_forever(speed_sp=self.speed)
        self.motor_right.run_forever(speed_sp=self.speed)

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

    def gyro_value(self):
        return self.gyro.value() % 360

    def sonar_value(self):
        return self.sonar.value() / 10


def main():
    robot = Robot()
    shortest = 10000
    shortest_gyro = 0
    print("Sonar: " + str(robot.sonar_value()) + " Gyro: " + str(robot.gyro_value()))
    robot.turn_fast("right")
    try:
        while not robot.btn.any():
            if robot.gyro.value() < 360:
                sleep(0.5)
                robot.stop()
                print("Sonar: " + str(robot.sonar_value()) + " Gyro: " + str(robot.gyro_value()))
                if robot.sonar.value() < shortest:
                    shortest = robot.sonar.value()
                    shortest_gyro = robot.gyro_value()
                sleep(0.5)
                robot.turn_fast("right")
            else:
                if robot.gyro_value() == shortest_gyro:
                    print("FOUND THIS PEICE OF SHIT")
                    robot.stop()
                else:
                    robot.turn_fast("right")
                    print("Sonar: " + str(robot.sonar_value()) + " Gyro: " + str(robot.gyro_value()))
        robot.stop()
    except KeyboardInterrupt:
        print("gyro true value: " + str(robot.gyro.value()))
        robot.stop()


if __name__ == "__main__":
    main()
