import pigpio
import time

#This class represents servo motor, it should be used in an loop and it control time by itself
#to use it read the 'readme.md'. Made by Guilherme da Silva Correia. @https://github.com/guidshps

class ServoMotor: 
    """
    Represents a servo motor controlled by an PWM signal.

    Args:
        hardware_pin (int) -> The hardware pin that the signal is generated. You should verify your board.
        frequency (int) -> The frequency that signal is generetad. 
        min_w (int) -> The minumim pulse width that ESC will receive in microseconds
        min_angle (int) -> The minimum angle that servo can achieve
        max_angle (int) -> The max angle that servo can achieve
        max_w (int)  -> Maximum pulse width that ESC will receive in microseconds
        period (float) -> Time between each increase or decrease of angles in seconds
    """

    def __init__(
            self, hardware_pin : int, 
            frequency : int, 
            min_w : int, 
            max_w : int, 
            min_angle: int, 
            max_angle: int,
            period : float
        ):
        """
        Initializer of the class, if the type of the parameters are not correct, the motor won't work.
        """

        if ( 
            not isinstance(hardware_pin, int) 
            or not isinstance(frequency, int)
            or not isinstance(min_w, int)
            or not isinstance(max_w, int)
            or not isinstance(min_angle, int)
            or not isinstance(max_angle, int)
            or not isinstance(period, float)
        ): #Verify if the types of are correct
            self.hardware_pin = None #Define 'None' how it does not exist
            self.frequency = None #Define 'None' how it does not exist
            self.current_pulse_w = None #Define 'None' how it does not exist
            self.current_angle = None #Define 'None' how it does not exist
            self.goal_angle = None #Define 'None' how it does not exist
            self.min_angle = None #Define 'None' how it does not exist
            self.max_angle = None #Define 'None' how it does not exist
            self.min_w = None #Define 'None' how it does not exist
            self.max_w = None #Define 'None' how it does not exist
            self.period = None #Define 'None' how it does not exist
            self.time_before = None #Define 'None' how it does not exist
            self.duty = None #Define 'None' how it does not exist
            return #Return if one or more of types are wrong
            

        self.hardware_pin = hardware_pin #The hardware pin from Raspberry Py
        self.frequency = frequency #The frequency that Raspberry Pi runs the pulses
        self.current_pulse_w = min_w #The current pulse width in microseconds
        self.current_angle = 0 #The angle that servo is currently
        self.goal_angle = 0 #The angle that servo is going to 
        self.min_angle = min_angle #The minimum angle that servo can achieve
        self.max_angle = max_angle #The maximum angle that servo can achieve
        self.min_w = min_w #The minimum pulse width that brushless motor can have
        self.max_w = max_w  #The maximum pulse width that brushless motor can have
        self.period = period #Define how much time would take to increase or decrease angle
        self.time_before = 0 #It's the time before the speed have been increased, used to reference, in seconds
        self.duty = self.frequency * self.min_w #Stores the duty of the signal

    def set_angle(self, new_goal_angle : int): #Function that defines an new angle for the servo
        """
        Function that set an new goal angle to the servo motor. It makes the servo have an soft aceleration.

        Args:
            new_goal_angle (int) -> The angle that the servo will achieve.
        """
        if self.hardware_pin is None: #Verify if the hardware pin exist
            return #Returns if the hardware pin is not valid

        elif not isinstance(new_goal_angle, int): #Verify if the new goal angles is an int type
            return #Returns if the new goal is not an int type
        
        self.goal_angle = new_goal_angle #Defines the new goal angle for the servo

    def force_angle(self, new_goal_angle : int):
        """
        Function that set an new goal angle to the servo motor. It makes the servo brusily.
        
        Args:
            new_goal_angle (int) -> The angle that the servo will achieve.
        """

        if self.hardware_pin is None: #Verify if the hardware pin exist
            return #Returns if the hardware pin is not valid
        
        elif not isinstance(new_goal_angle, int): #Verify if the new goal angles is an int type
            return #Returns if the new goal is not an int type

        self.current_pulse_w = new_goal_angle #Defines the new goal as the current angle
        self.goal_angle = new_goal_angle #Defines the new goal angle for the servo

    def change_period(self, new_period : float):
        """
        Function that set an new period to the servo motor.
                
        Args:
            new_period (period) -> The period that will be setted.
        """

        if self.hardware_pin is None: #Verify if the hardware pin exist
            return #Returns if the hardware pin is not valid
                
        elif not isinstance(new_period, float): #Verify if the new period is a float type
            return #Returns if the new goal is not a float type

        self.period = new_period #Sets the new period for the servo

    def run(self, pi : pigpio.pi): 
        """
        Function that runs the servo motor and change his angle. If the servo motor doesn't exist or the pi is the wrong type,
        this function will not work.

        Args:
            pi (pigpio.pi) -> 'pi' is one object from the class from 'pi' from the library pigpio
        """

        if self.hardware_pin is None: #Verify if the servo motor is not valid
            return #Returns if the servo is not valid

        elif not isinstance(pi, pigpio.pi): #Verify if the 'pi' is the correct type
            return #Returns if pi is the wrong type

        #Block that changes angle and calculates the current pulse width
        my_time = time.monotonic #Get the time reference from now

        if my_time - self.time_before >= self.period and self.current_angle != self.goal_angle: #Verify the conditions to change angle
            if self.current_angle > self.goal_angle: #If the current angle is bigger than the goal
                self.current_angle -= 1 #Decrease the current angle
                if self.current_angle < self.goal_angle: #If it has passed the goal angle
                    self.current_angle = self.goal_angle #It is defined as the goal angle
            elif self.current_angle < self.goal_angle: #If the current angle is smaller than the goal
                self.current_angle += 1 #Increase the current angle
                if self.current_angle > self.goal_angle: #If it has passed the goal angle
                    self.current_angle = self.goal_angle #It is defined as the goal angle

            self.time_before = my_time #Sets the new time reference 
            #Calculates the new pulse width
            self.current_pulse_w = ((self.current_angle - self.min_angle) * (self.max_w - self.min_w) / 
                                    (self.max_angle - self.self.min_angle) + self.self.min_w)
            self.duty = self.current_pulse_w * self.frequency #Calculates the new duty


        #Block that controls the hardware pin PWM signal
        pi.hardware_PWM(self.hardware_pin, self.frequency, self.duty)