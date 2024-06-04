from experta import *
from sys import exit

class WrongInput(Exception):
    def __init__(self):
        self.message = "Wrong input given, please try again"
        super().__init__(self.message)

class LED:
    class Power(Fact):
        pass

    class WiFi(Fact):
        pass

    class ErrorLED(Fact):
        pass

    class ReadyLED(Fact):
        pass

class TimeInterval:
    class ErrorLEDInterval(Fact):
        pass

    class ReadyLEDInterval(Fact):
        pass

class NumberOfBlinks:
    class ErrorLEDBlinks(Fact):
        pass

    class ReadyLEDBlinks(Fact):
        pass

class ProblemSolver(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action = 'solve')

    @Rule(Fact(action = 'solve'), salience=6)
    def ask_for_ErrorLED_state(self):
        state = input_diode_state(input('ErrorLED state:\n0 - off\n1 - on\n2 - blinking\n'))
        print(f"ErrorLED state: {state}\n")
        self.declare(LED.ErrorLED(state=state))

    @Rule(Fact(action = 'solve'), salience=5)
    def ask_for_ErrorLED_time(self):
        time = input_diode_time(input('ErrorLED blinking time:\n0 - doesn\'t apply\n1 - 0.5s\n2 - 1s\n3 - 1.5s\n4 - other\n'))
        print(f"ErrorLED blinking time: {time}\n")
        self.declare(TimeInterval.ErrorLEDInterval(time=time))

    @Rule(Fact(action = 'solve'), salience=4)
    def ask_for_ErrorLED_blinks(self):
        number = input_diode_blinks(input('ErrorLED number of blinks:\n0 - doesn\'t apply\n1 - 1\n2 - 2\n3 - 3\n4 - 4\n5 - other\n'))
        print(f"ErrorLED number of blinks: {number}\n")
        self.declare(NumberOfBlinks.ErrorLEDBlinks(number=number))

    @Rule(Fact(action = 'solve'), salience=3)
    def ask_for_ReadyLED_state(self):
        state = input_diode_state(input('ReadyLED state:\n0 - off\n1 - on\n2 - blinking\n3 - dimmed\n'))
        print(f"ReadyLED state: {state}\n")
        self.declare(LED.ReadyLED(state=state))

    @Rule(Fact(action = 'solve'), salience=2)
    def ask_for_ReadyLED_time(self):
        time = input_diode_time(input('ReadyLED blinking time:\n0 - doesn\'t apply\n1 - 0.5s\n2 - 1s\n3 - 1.5s\n4 - 4\n5 - other\n'))
        print(f"ReadyLED blinking time: {time}\n")
        self.declare(TimeInterval.ReadyLEDInterval(time=time))

    @Rule(Fact(action = 'solve'), salience=1)
    def ask_for_ReadyLED_blinks(self):
        number = input_diode_blinks(input('ReadyLED number of blinks:\n0 - doesn\'t apply\n1 - 1\n2 - 2\n3 - 3\n4 - other\n'))
        print(f"ReadyLED number of blinks: {number}\n")
        self.declare(NumberOfBlinks.ReadyLEDBlinks(number=number))

    @Rule(NOT(Fact(state='off') | Fact(state='on') | Fact(state='blinking') | Fact(state='dimmed')), 
        NOT(Fact(time='doesn\'t apply') | Fact(time='0.5s') | Fact(time='1s') | Fact(time='1.5s') | Fact(time='other')),
        NOT(Fact(number='doesn\'t apply') | Fact(number='1') | Fact(number='2') | Fact(number='3') | Fact(number='4') | Fact(number='other')),
        salience=-1)
    def default_message(self):
        print("Unknown problem occurred. Please, try again")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state='off'),  LED.ReadyLED(state='dimmed')), salience=10)
    def set_sleep(self):
        print('SLEEP\nThe printer is asleep. Let it sleep for a while <3')
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="off"), LED.ReadyLED(state="on")), salience=10)
    def set_ready(self):
        print("READY\nThe printer is ready. Let's go!")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="off"), LED.ReadyLED(state="blinking"), TimeInterval.ReadyLEDInterval(time="1s")), salience=10)
    def set_wait(self):
        print("WAIT\nThe printer is cooling down. Please wait!")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="off"), LED.ReadyLED(state="blinking"), TimeInterval.ReadyLEDInterval(time="0.5s")), salience=10)
    def set_printing(self):
        print("PRINTING\nThe printer prints as fast as it can!")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="on"), TimeInterval.ErrorLEDInterval(time="other"), TimeInterval.ReadyLEDInterval(time="other")), salience=10)
    def set_toner_low(self):
        print("TONER LOW\nThe printer will soon run out of toner. Keep that in mind!")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="off"), TimeInterval.ErrorLEDInterval(time="1.5s")), salience=10)
    def set_toner_ended(self):
        print("NO TONER\nThe printer run out of toner! You were supposed to replace it a long time ago!")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="off"), NumberOfBlinks.ErrorLEDBlinks(number="4")), salience=10)
    def set_cartridge(self):
        print("CARTRIDGE ERROR\nThe drum unit and toner cartridge assembly is not installed correctly")
        exit()
    
    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="on"), NumberOfBlinks.ErrorLEDBlinks(number="3")), salience=10)
    def set_drum_low(self):
        print("REPLACE DRUM\nReplace the drum with a new one")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="off"), NumberOfBlinks.ErrorLEDBlinks(number="3")), salience=10)
    def set_drum(self):
        print("CORONA CABLE(?)\nThe corona wire needs to be cleaned(?)")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="off"), TimeInterval.ErrorLEDInterval(time="1s"), NumberOfBlinks.ErrorLEDBlinks(number="2")), salience=10)
    def set_jam_tray(self):
        print("PAPER PROBLEM\nProblems with paper. Check it's size, clear the jam or put more paper")
        exit()

    #ok
    @Rule(AND(LED.ErrorLED(state="blinking"), LED.ReadyLED(state="off"), TimeInterval.ErrorLEDInterval(time="1s"),
    NumberOfBlinks.ErrorLEDBlinks(number="4")), salience=10)
    def set_cover(self):
        print("COVER IS OPEN\nClose the top cover!")
        exit()
        
    #ok
    @Rule(AND(LED.ErrorLED(state="on"), LED.ReadyLED(state="on")), salience=10)
    def set_cancel_printing(self):
        print("CANCEL PRINTING\nThe printer is canceling the job")
        exit()

def input_diode_state(state):
    if state == '0':
        return 'off'
    elif state == '1':
        return 'on'
    elif state == '2':
        return 'blinking'
    elif state == '3':
        return 'dimmed'
    else:
        raise WrongInput()
    
def input_diode_time(time):
    if time == '0':
        return 'doesn\'t apply'
    elif time == '1':
        return '0.5s'
    elif time == '2':
        return '1s'
    elif time == '3':
        return '1.5s'
    elif time == '4':
        return 'other'
    else:
        raise WrongInput()
    
def input_diode_blinks(number):
    if number == '0':
        return 'doesn\'t apply'
    elif number == '1':
        return '1'
    elif number == '2':
        return '2'
    elif number == '3':
        return '3'
    elif number =='4':
        return "4"
    elif number == '5':
        return 'other'
    else:
        raise WrongInput()

if __name__ == '__main__':
    solver = ProblemSolver()
    solver.reset()
    solver.run()