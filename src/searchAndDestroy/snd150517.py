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
        return self.sonar.value() / 10 # in cm?


def main():
    # irl: 140cm x 140cm; matrix: 16x16; ehk 10x10cm 0-kuubid
    # 0 - default val 
    # 1 - walls
    # 2 - bottle, kui leiab pudeli, siis 0 -> 2

    robot = Robot()
    
    print("Sonar: " + str(robot.sonar_value()) + " Gyro: " + str(robot.gyro_value()))

    # initalizeb matrixi
    matrix = [[0 for x in range(16)] for y in range(16)]
    for i in range(0, 16):
        for j in range(0, 16):
            if i == 0 or i == 15:
                matrix[i][j] = 1
            else if j == 0 or j == 15:
                matrix[i][j] = 1
            else: 
                continue


    # platsil ainult 3 silindrit, robot stardib platsi keskelt
    # teeb täistiiru ja jätab 3 kõige lähemat sonari valuet ja 
    # samadel kohtadel olevat gyro valued meelde,
    # teisel tiirul käib kõik silindrid läbi, minnes alati tagasi keskele

    closest_sonar_values = [3000, 3000, 3000]
    closest_gyro_values = [0, 0, 0]
    cnt = 0

    try:
        while not robot.btn.any() and robot.gyro_value() < 360:
            robot.turn_fast("right")

            # leiab lähimad 3 ja paneb nad closest_sonar_values listi
            sonar_val = robot.sonar_value()
            if sonar_val < 3000:
                robot.sleep(5)
                for value in closest_sonar_values:
                    if sonar_val < value:
                        closest_sonar_values[cnt] = sonar_val
                        closest_gyro_values[cnt] = robot.gyro_value()
                        cnt += 1

        # läheb silindrite juurde ja tagasi keskele
        cnt = 0
        gyro_value = 0

        while not robot.btn.any():
            for value in closest_gyro_values:
                while robot.gyro_value() + gyro_value == value + (45 / 2):
                    gyro_value += robot.gyro_value()
                    robot.turn_fast()
                while robot.sonar_value() > 1: # tagasi ümberpööramiseks ka natuke ruumi siis
                    robot.drive()
                while robot.
                # TODO:
                # 1. pöörata tagasi ümber
                # 2. sõita tagasi keskele
                # 3. pöörata veelkord tagasi ümber, et oleks sellises suunas
                #    kust alustas just käidud silindri juurde sõitmist, et keskmist 
                #    spinni tegeva gyro muutuja value oleks õigesti pagas
                # 1. tagurdab tagasi sama palju kui sõitis edasi




    except KeyboardInterrupt:
        print("gyro true value: " + str(robot.gyro.value()))
        robot.stop()


if __name__ == "__main__":
    main()
