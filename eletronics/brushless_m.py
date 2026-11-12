import pigpio
import time

#This class represents brushless motor, it should be used in an loop and it control time by itself,
#to use it read the 'readme.md'. Made by Guilherme da Silva Correia. @https://github.com/guidshps

class BrushlessMotor:
    """
    Represents a brushless motor controlled by an eletronic speed controller and PWM signal.

    Args:
        hardware_pin (int) -> The hardware pin that the signal is generated. You should verify your board.
        frequency (int) -> The frequency that signal is generetad. 
        min_w (int) -> The minumim pulse width that ESC will receive in microseconds
        max_w (int)  -> Maximum pulse width that ESC will receive in microseconds
        incremental (int) -> Amount that pulse is increased or decreased in each period in microseconds
        period (float) -> Time between each increase or decrease of speed in seconds
    """

    def __init__(
            self, 
            hardware_pin: int, 
            frequency : int, 
            min_w : int, 
            max_w : int, 
            incremental : int, 
            period : float
        ): 
        """
        Initializer of the class, if the type of the parameters are not correct, the motor won't work.

        Args:
            hardware_pin (int) -> The hardware pin that the signal is generated. You should verify your board.
            frequency (int) -> The frequency that signal is generetad. 
            min_w (int) -> The minumim pulse width that ESC will receive in microseconds
            max_w (int)  -> Maximum pulse width that ESC will receive in microseconds
            incremental (int) -> Amount that pulse is increased or decreased in each period in microseconds
            period (float) -> Time between each increase or decrease of speed in seconds
        """
        if ( 
            not isinstance(hardware_pin, int) 
            or not isinstance(frequency, int)
            or not isinstance(min_w, int)
            or not isinstance(max_w, int)
            or not isinstance(incremental, int)
            or not isinstance(period, float)
        ):
            self.hardware_pin = None #Define 'None' how it does not exist
            self.frequency = None #Define 'None' how it does not exist
            self.current_pulse_w = None #Define 'None' how it does not exist
            self.goal_pulse_w = None #Define 'None' how it does not exist
            self.min_w = None #Define 'None' how it does not exist
            self.max_w = None #Define 'None' how it does not exist
            self.incremental = None #Define 'None' how it does not exist
            self.period = None #Define 'None' how it does not exist
            self.time_before = None #Define 'None' how it does not exist
            self.duty = None #Define 'None' how it does not exist
            return #Return if all of types are int

        self.hardware_pin = hardware_pin #The hardware pin from Raspberry Py 
        self.frequency = frequency #The frequency that Raspberry Pi runs the pulses
        self.current_pulse_w = min_w #The current pulse width in microseconds
        self.goal_pulse_w = min_w #The goal pulse width in microseconds to achieve (To soft accelerate)
        self.min_w = min_w #The minimum pulse width that brushless motor can have
        self.max_w = max_w  #The maximum pulse width that brushless motor can have
        self.incremental = incremental #Define how fast the brushless motor will acelerate
        self.period = period #Define how much time would take to increase to speed again
        self.time_before = 0 #It's the time before the speed have been increased, used to reference (In Seconds)
        self.duty = self.frequency * self.min_w #Stores the duty from the signal

    def set_speed(self, new_goal_pulse_w : int): 
        """
        Function that changes speed of the motor. This function do the brushless motor accelerate softly. If
        the new goal pulse are not an int type and the motor doesn't exist, it won't work
        
        Args:
            new_goal_pulse_w (int) -> The new goal pulse that would be achieve in microseconds
        """

        if self.hardware_pin is None: #Verify if the hardware pin is valid
            return #Return if hardware pin is not valid
        
        elif not isinstance(new_goal_pulse_w, int): #Verify if is new goal pulse width is not an int
            return #Return if is not an int
        
        elif new_goal_pulse_w < self.min_w or new_goal_pulse_w > self.max_w:
            return #Leave the function and not change his pulse width if it is not at the right period

        self.goal_pulse_w = new_goal_pulse_w #Change the goal pulse width

    def force_speed(self, new_goal_pulse_w : int): 
        """
        Function that changes speed of the motor. This function do the brushless motor accelerate abtruply. If
        the new goal pulse are not an int type or the motor doesn't exist, it won't work.
        
        Args:
            new_goal_pulse_w (int) -> The new goal pulse width is the width that would be achieve in microseconds
        """

        if self.hardware_pin is None: #Verify if the hardware pin is valid
            return #Return if hardware pin is not valid
    
        elif not isinstance(new_goal_pulse_w, int): #Verify if is new goal pulse width is not an int
            return #Return if is not an int
        
        elif new_goal_pulse_w < self.min_w or new_goal_pulse_w > self.max_w:
            return #Leave the function and not change his pulse width if it is not at the right period

        self.current_pulse_w = new_goal_pulse_w #Change the current pulse width 
        self.goal_pulse_w = new_goal_pulse_w #Change the goal pulse width
        #current pulse width is equal to goal pulse width, so the motor change his speed abruptly

    def calibrate_esc(self, pi : pigpio.pi): 
        """
        Function that calibrate the eletronic speed controller. If the pigpio.pi 
        is not valid or the motor doesn't exist, it won't work.

        Args:
            pi (pigpio.pi) -> 'pi' is one object from the class from 'pi' from the library pigpio
        """

        if self.hardware_pin is None: #Verify if the hardware pin is valid
            return #Return if hardware pin is not valid

        elif not isinstance(pi, pigpio.pi): #Verify if the pi is not valid 
            return #Return if pi is not of class of 'pihardware.pi'
        
        max_duty = int(self.frequency * self.max_w) #Calculates the maximum duty
        min_duty = int(self.frequency * self.min_w) #Calculates the minimum duty

        input("Are the battery desconected and the propeller removed? [PRESS ENTER]")
        pi.hardware_PWM(self.hardware_pin, self.frequency, max_duty) #Sets the hardware pin for the max value
        input("Connect the battery, when ESC release beeps. [PRESS ENTER]")
        pi.hardware_PWM(self.hardware_pin, self.frequency, min_duty) #Sets the hardware pin for the max value
        print("The calibrate were done suceffuly!") #Wars the user that the process were completed

    def change_incremental(self, new_incremental : int):
        """
        Function that changes incremental from brushless motor. If new incremental is not an int or the motor doesn't exist,
        it won't work.

        Args:
            new_incremental (int) -> New incremental that will be setted.
        """

        if self.hardware_pin is None: #Verify if the motor is not valid
            return #Return if the motor is not valid
        
        elif not isinstance(self, new_incremental): #Verify if new incremental is not an int
            return #If is not an int, leave the function

        self.incremental = new_incremental #Change to the new incremetal

    def change_period(self, new_period : float):
        """
        Function that changes the period from brushless motor. If the new period is not an int or the motor doesn't exist,
        it won't work.
        
        Args:
            new_period (int) -> The new period that will be setted. (seconds)
        """

        if self.hardware_pin is None: #Verify if the motor is not valid
            return #Return if the motor is not valid
        
        elif not isinstance(new_period, float): #Verify if new period is not an float
            return #If is not an float, leave the function

        self.period = new_period #Change to the new period

    def run(self, pi : pigpio.pi): 
        """
        Function that runs the brushless motor and accelerate it. If the Pi is not the right type and 
        the motor doesn't exist, it won't work

        Args:
            pi (pigpio.pi) -> 'pi' is one object from the class from 'pi' from the library pigpio
        """

        if self.hardware_pin is None: #Verify if the hardware pin is valid
            return #Return if hardware pin is not valid

        elif not isinstance(pi, pigpio.pi): #Verify if the pi is not valid 
            return #Return if pi is not of class of 'pihardware.pi'
        
        #Acceleration or desacceleration block for brushless motor
        if self.current_pulse_w != self.goal_pulse_w: #Verify if is necessary to change speed
            my_time = time.monotic() #The current time to compare with time before the last acceleration

            if my_time - self.time_before >= self.period: #Verify the period alrealdy have passed
                if self.current_pulse_w > self.goal_pulse_w: #If the current pulse width is bigger than the goal
                    self.current_pulse_w -= self.incremental #Decreases the speed of the motor
                    if self.current_pulse_w < self.goal_pulse_w: #If the current pulse width pass the goal
                        self.current_pulse_w = self.goal_pulse_w #The current pulse width will be set as goal pulse
                elif self.current_pulse_w < self.goal_pulse_w:
                    self.current_pulse_w += self.incremental #Increases the speed of the motor
                    if self.current_pulse_w > self.goal_pulse_w: #If the current pulse width pass the goal
                        self.current_pulse_w = self.goal_pulse_w #The current pulse width will be set as goal pulse

                self.duty = self.frequency * self.current_pulse_w #Calculates the duty of the signal
                self.time_before = my_time #Change the reference time before

        #Block that controls the PWM signal in hardware pin
        pi.hardware_PWM(self.hardware_pin, self.frequency, self.duty) #Turns on the hardware pin

    def stop(self, pi : pigpio.pi): #Function that stop the brushless motor
        """
        Function that stop the brushless motor softly. If the Pi is not the right type and the motor doesn't exist,
        it won't work
        
        Args:
            pi (pigpio.pi) -> 'pi' is one object from the class from 'pi' from the library pigpio
        """

        if self.hardware_pin is None: #Verify if hardware pin is None
            return #If it is None, leave the function
            
        elif not isinstance(pi, pigpio.pi): #Verify if the pi is not valid
            return #Return if pi is not of class of 'pihardware.pi'

        #Desacceleration block for brushless motor
        if self.current_pulse_w != self.min_w: #Verify if is necessary to change speed
            my_time = time.monotic() #The current time to compare with time before that have an acceleration

            if my_time - self.time_before >= self.period: #Verify if need to desaccelerate
                self.current_pulse_w -= self.incremental #Decrease the current pulse width

                if self.current_pulse_w < self.min_w: #If it passes the current pulse width pass the minimum
                    self.current_pulse_w = self.min_w #Return to minimum if it have passed

                self.time_before = my_time #Sets the new time before for nexts references
                self.duty = int(self.frequency * self.current_pulse_w) #Calculates the duty of the signal

        #Block that controls the PWM signal in hardware pin
        pi.hardware_PWM(self.hardware_pin, self.frequency, self.duty) #Turns on the hardware pin