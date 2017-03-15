
# - valge ule 70
# - must alla 12

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
        self.motor_left.duty_cycle_sp = 20
        self.motor_right.run_forever()
        self.motor_right.duty_cycle_sp = 20

    def turn(self, direction, speed):
        if direction == "Left":
            if speed == 15:
                self.motor_left.duty_cycle_sp = 0
                self.motor_right.duty_cycle_sp = 15
            elif speed == 30:
                self.motor_left.duty_cycle_sp = 0
                self.motor_right.duty_cycle_sp = 30
            elif speed == 40:
                self.motor_left.duty_cycle_sp = 0
                self.motor_right.duty_cycle_sp = 40
        elif direction == "Right":
            if speed == 15:
                self.motor_left.duty_cycle_sp = 15
                self.motor_right.duty_cycle_sp = 0
            elif speed == 30:
                self.motor_left.duty_cycle_sp = 30
                self.motor_right.duty_cycle_sp = 0
            elif speed == 40:
                self.motor_left.duty_cycle_sp = 40
                self.motor_right.duty_cycle_sp = 0

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
            print("------------------------")
            robot.drive()

            # print(robot.sense_reflection())
            # lisab 5. ja 6. vaartuse kui juba liikund on ja kustutab esimesed 2
            reflection.extend(robot.sense_reflection())

            # hoiab 4 vaartust (2 iteratsiooni)
            reflection.pop(0) # 1.sensor
            reflection.pop(0) # 2.sensor
            print("1.1: " + str(reflection[0]) + ", 2.1: " + str(reflection[2]))
            print("1.2: " + str(reflection[1]) + ", 2.2: " + str(reflection[3]))

            # 1. sensor - vasak
            # 2. sensor - parem


            # JALGIB 1. (VASAKUT) SENSORIT

            # kui pole liiga tume ega hele
            if (10 < reflection[2] < 68):
                print ("* vahemikus")
                """
                if ((reflection[0] - reflection[2]) == 0):
                    print ("- otse")
                    robot.drive()
                """
                # liigub natuke heledamaks
                if (0 > (reflection[0] - reflection[2]) >= -10):
                    print ("- aeglaselt paremale")
                    robot.turn("Right", 15)
                # liigub natuke tumedamaks
                elif (10 >= (reflection[0] - reflection[2]) > 0):
                    print ("- aeglaselt vasakule")
                    robot.turn("Left", 15)
                # liigub palju heledamaks
                elif (- 10 > (reflection[0] - reflection[2])):
                    print ("- kiiresti paremale")
                    robot.turn("Right", 30)
                # liigub palju tumedamaks
                elif ((reflection[0] - reflection[2]) > 10):
                    print ("- kiiresti vasakule")
                    robot.turn("Left", 30)
            # kui on liiga hele
            elif (reflection[2] > 68):
                print ("* liiga hele")
                # veel kiiremini paremale
                robot.turn("Right", 30)
            # kui on liiga tuma
            elif (reflection[2] < 10):
                print ("* liiga tume")
                # veel kiiremini vasakule
                robot.turn("Left", 30)


            """
            tootab normilt, pekki laheb siis kui:
            - laheb vasaku sensoriga joonest paremale poole nii on on liiga hele, siis
              poorab paremale seni kuni tuleb must joon, ehk hakkab vastupidises suumas liikuma
              voi kui on joonest liiga kaugel, siis liigub selle jargi mis ette satub
            """



    except KeyboardInterrupt: # press CTRL C to quit
        robot.stop()


if __name__ == "__main__":
    main()
