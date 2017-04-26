# TODO: Võta alguse ja lõpu gyro väärtused ja siis selle keskmine
# TODO: Maatrix solution?
# TODO:


from ev3dev import ev3


class Robot:
    def __init__(self):
        self.speed = 25
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

    def gyro_value(self):
        return self.gyro.value() % 360

    def sonar_value(self):
        return self.sonar.value() / 10


def main():
    robot = Robot()
    sonar_values = []
    working = True
    min_dist = 3000
    min_deg = 361
    first_turn = True
    for x in range(2):
        sonar_values.append(robot.sonar.value())
    try:
        while not robot.btn.any() and working:
            if first_turn:
                robot.turn_fast("right")
                new_sonar_value = robot.sonar.value()
                sonar_values.append(new_sonar_value)
                sonar_values.pop(0)
                print("Dist: " + str(min_dist) + " Deg: " + str(min_deg))
                # print("Gyro: " + str(robot.gyro_value()) + " Sonar: " + str(robot.sonar_value()))
                if min_dist > new_sonar_value:
                    min_dist = sonar_values[1]
                    min_deg = robot.gyro_value()
                    print("Gyro: " + str(robot.gyro_value()) + " Sonar: " + str(robot.sonar_value()))
                if robot.gyro_value() == 180:
                    first_turn = False
            else:
                if robot.gyro_value() != min_deg:
                    robot.turn_fast("left")
                if robot.gyro_value() == min_deg:
                    robot.stop()
        robot.stop()
    except KeyboardInterrupt:
        robot.stop()


if __name__ == "__main__":
    main()
