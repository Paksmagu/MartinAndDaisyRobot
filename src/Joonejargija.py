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
        self.color_sensor.mode = "COL-COLOR"
        self.color_sensor2.mode = "COL-COLOR"
        self.motor_left.duty_cycle_sp = 15
        self.motor_right.duty_cycle_sp = 15

    def drive(self):
        self.motor_left.run_forever(speed_sp=200)
        self.motor_right.run_forever(speed_sp=200)

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

    try:
        while (True):
            robot.drive()
            time.sleep(0.1)
            colors = robot.sense_color()
            print(robot.sense_color())
            #if 20 > robot.sense_reflection() > 11:
            #    continue
            #elif robot.sense_reflection() > 60:
            #    print("Poorab vasakule")
            #    robot.turn("Left")
            #else:
            #    print("Poorab paremale")
            #    robot.turn("Right")
            if (colors[0] != 1) and (colors[1] != 1):
                print("valge soidab otse")
                continue
            elif (colors[0] == 1) and (colors[1] == 1):
                print("molemad mustad, soidab otse")
                continue
            elif colors[0] == 1:
                print("Turning left")
                robot.turn("Left")
            elif colors[1] == 1:
                print("turning right")
                robot.turn("Right")

    except KeyboardInterrupt: # press CTRL C to quit
        robot.stop()


if __name__ == "__main__":
    main()
