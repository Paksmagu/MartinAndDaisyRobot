"""
- käib joone paremat äärt mööda
- kui leiab musta, pöörab paremale
- kui leiab valge, pöörab vasakule
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
        self.motor_left.duty_cycle_sp = 15
        self.motor_right.run_forever()
        self.motor_right.duty_cycle_sp = 15

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

    def sense_color(self):
        return self.color_sensor.value(), self.color_sensor2.value()


def main():
    robot = Robot()

    print(robot.sense_color())

    reflection = []
    for x in range(0, 2):
        reflection.extend(robot.sense_reflection())

    print(reflection)

    try:
        while (True):
            # robot.drive()
            time.sleep(2)
            print(robot.sense_reflection())
            # lisab 5. ja 6. vaartuse kui juba liikund on ja kustutab esimesed 2
            reflection.extend(robot.sense_reflection())
            print("loobi sees 6 liiget ")
            print(reflection)

            # hoiab 4 vaartust (2 iteratsiooni)
            reflection.pop(0) # 1.sensor
            reflection.pop(0) # 2.sensor
            print("peale pop'i 4 liiget")
            print(reflection)

            # 1. sensor - vasak
            # 2. sensor - parem

            robot.stop()

            # 1. sensori vaartus kasvab 2. vaheneb - liigub vasakule
            if ((reflection[0] - reflection[2] > 0
                and reflection[1] - reflection[3] < 0)
                  or (reflection[0] - reflection[2] >= 0
                and reflection[1] - reflection[3] < 0)
                  or (reflection[0] - reflection[2] > 0
                and reflection[1] - reflection[3] <= 0)):
                print("right")
                time.sleep(2)
                # robot.turn("Right")
            #1. sensori vaartus kahaneb 2. suureneb - liigub paremale
            elif ((reflection[0] - reflection[2] < 0
                and reflection[1] - reflection[3] > 0)
                  or (reflection[0] - reflection[2] <= 0
                and reflection[1] - reflection[3] > 0)
                  or (reflection[0] - reflection[2] < 0
                and reflection[1] - reflection[3] >= 0)):
                print("left")
                time.sleep(2)
                # robot.turn("Left")


    except KeyboardInterrupt: # press CTRL C to quit
        robot.stop()


if __name__ == "__main__":
    main()
