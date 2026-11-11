import pigpio
import time

#This class represents brushless motor, it should be used in an loop and it control time by itself
#to use it read the 'readme.md'. Made by Guilherme da Silva Correia. @https://github.com/guidshps

class ServoMotor: #Class that represents the servo motor
    def __init__(self, hardware_pin : int): #Initializer of the class
        self.hardware_pin = hardware_pin #The hardware pin that controls the servo motor
        self.current_angle = 0 #The angle that is servo is currently
        self.goal_angle = 0 #The angle that servo are going to move

    def set_goal_angle(self, new_goal_angle : int): #Function that defines an new angle for the servo
        self.goal_angle = new_goal_angle #Defines the new goal angle for the servo

    def run(self): #Function that runs an the servo motor
        pass
