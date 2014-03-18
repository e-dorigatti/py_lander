#   
#          * thrust
#          . speed
#     
#      ^
#      |
# 100% -                                       * * * * * *
#      |
#      |
#      |
#    b -      * * * * * * * * * * * * * * * * *
#      |
#    a -     . . . . . . . . . . . . . . . . . .
#      |    .                                    .
#      |   .                                       .    Landing
#      |  .                                          .   |
#      | .                                             . |
#      |                                                 v
#      +-*-*-^---------------------------------^------------> time 
#      0     t1                                t2    
# 
# The controller starts by free-falling to get as close as possible
# to the maximum speed a, from 0 to t1, which is then maintained using
# a constant thrust b, from t1 to t2. After t2 the engine output is set
# to its maximum and the lander slows down until a safe landing.
#
# A genetic algorithm is used to determine the best values for t2 and b.

from simulation import Simulation
from random import randrange

def evaluate_controller(controller):
    """
    Gives a score to the controller based on its landing
    performance, determined by the simulation outcome and
    the time elapsed.
    """
    sim = Simulation(controller)
    success, time = sim.simulate()
    if success:
        return time
    else:
        return -(time + 100)

def create_controller(t2, b):
    """
    Creates a parametrized controller behaving as described
    above (free fall --> constant speed --> max thrust).

    a is 90% of max_speed
    t1 is determined according to a
    """
    def controller(sim):
        if sim.time < t2:
            if sim.speed >= sim.max_speed * 0.9:
                return b * 0.01
            else:
                return 0
        else:
            return 1.0

    return controller

def controller_fitness(args):
    t2 = max(0, args[0])
    b = max(0, args[1])
    b = min(b, 100)

    controller = create_controller(t2, b)
    return evaluate_controller(controller)

