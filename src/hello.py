from ev3dev import ev3
import time

class Robot:
    def __init__(self):
        self.motor_left = ev3.LargeMotor("outB")
        self.motor_right = ev3.LargeMotor("outC")
        self.motor_left.reset()
        self.motor_right.reset()
        self.color_sensor = ev3.ColorSensor("in1")
        self.color_sensor.mode = "COL-COLOR"

    def set_robot_speed(self, speed):
        self.set_speed(self.motor_left, speed)
        self.set_speed(self.motor_right, speed)
        self.robot_speed = speed 

    def set_speed(self, motor, speed):
        motor.duty_cycle_sp = speed

    def drive(self):
        print("Sending command")
        self.motor_left.run_forever()
        self.motor_right.run_forever()

    def sleep(self, duration):
        for _ in range(duration):
            print("Sleeping 1sec")
            time.sleep(1)
        
    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def timed_drive(self, duration):
        self.drive()
        self.sleep(duration)
        self.stop()

    def turn(self, direction, duration):
        if direction == "Right":
            self.set_speed(self.motor_right, 0)
            self.timed_drive(duration)
            self.set_speed(self.motor_right, self.robot_speed)
        if direction == "Left":
            self.set_speed(self.motor_left, 0)
            self.timed_drive(duration)
            self.set_speed(self.motor_left, self.robot_speed)

    def sense_color(self):
            return self.color_sensor.value()

        
def main():
    robot = Robot()
    
    """
    robot.set_robot_speed(10)
    robot.timed_drive(5)
    robot.turn("Right", 2)
    robot.timed_drive(5)
    robot.turn("Left", 2)
    """
    """
    g = ev3.GyroSensor("in2")
    g.mode = "GYRO-ANG"
    while True:
        print(g.value())
    """

    u = ev3.UltrasonicSensor("in3")
    u.mode = "US-DIST-CM"

    robot.set_robot_speed(15)

    for _ in range(7):
        print(u.value())
        robot.drive()
        
        while robot.sense_color() != 1:   
            pass

        robot.turn("Left", 5)
        
    robot.stop()

    
if __name__ == "__main__":
    main()

