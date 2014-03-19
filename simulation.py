from time import sleep

class Simulation:
    def __init__(self, controller):
        self.starting_position = 150.0
        self.max_speed = 30.0
        self.max_landing_speed = 5.0
        self.max_engine_thrust = 175.0
        
        self.gravity = 9.8
        self.mass = 7.5
        self.delta_t = 0.01
        self.max_steps = 10000

        self.controller = controller
        self.position = self.starting_position
        self.speed = 0.0
        self.time = 0.0

    def step_simulate(self, engine_input):
        """
        Updates the lander state according to the controller's input
        """
        force = engine_input * self.max_engine_thrust
        acceleration = self.gravity - force / self.mass
        self.speed += acceleration * self.delta_t
        self.position -= self.speed * self.delta_t

    def simulate(self, debug = False):
        """
        Performs the simulation using the given controller and
        returns whether the lander landed successfully on the
        moon or crashed / flown away and the time it took
        """
        steps = 0
        while (self.position > 0 and
            steps < self.max_steps and
            self.speed < self.max_speed):

            control = self.controller(self)
            self.step_simulate(control)
            steps += 1
            self.time = steps * self.delta_t

            if debug:
                print ('time %f position %f speed %f thrust %f' %
                    (self.time, self.position, self.speed, control))
                sleep(self.delta_t)

        return (self.position <= 0 and self.speed < self.max_landing_speed,
            steps * self.delta_t)


def simple_controller(sim):
    """
    Quite simple yet pretty good
    """

    if sim.position > 52:
        target_speed = sim.max_speed * 0.9
        if sim.speed > target_speed:
            return 1.0
        else:
            return 0.0
    else:
        return 1.0

# such encapsulation
def cheating_controller(sim):
    sim.position = -0.1
    sim.speed = sim.max_landing_speed * 0.5
    return 0

if __name__ == '__main__':
    a = Simulation(simple_controller)
    print a.simulate(debug = True)
