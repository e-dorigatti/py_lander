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

from simulation import Simulation

def gradient_descent(function, initial_position, max_iter, step_size):
    """
    Minimizes a function: R -> R * R starting from initial_position
    trying at most max_iter times. The function should return a tuple
    with the current value along with the derivative or None if
    no such derivative is available. In this case it will be estimated
    using the difference quotient.
    """

    i, position, epsilon = 0, initial_position, 0.001
    value, derivative = 0, 100
    while i < max_iter and abs(derivative) > 0.000001:
        value, derivative = function(position)
        if derivative is None:
            v1, d1 = function(position - epsilon)
            v2, d2 = function(position + epsilon)
            derivative = (v2 - v1) / (2 * epsilon)

        i += 1
        position += derivative * step_size
        # print 'i = %d  value = %f  derivative = %f  position = %f' %\
        #    (i, value, derivative, position)

    return position

def find_holding_thrust():
    """
    Find the thrust needed to keep the lander's speed constant.
    """
    def minimize(thrust):
        """
        This is the function to minimize. We don't really care about the
        speed at the moment
        """
        prev_speed = sim.speed
        sim.step_simulate(thrust)

        return sim.speed, (sim.speed - prev_speed) / sim.delta_t

    sim = Simulation(None)
    thrust = gradient_descent(minimize, 0.5, 1000, 0.05)
    return thrust

def find_distance(start_speed, end_speed):
    """
    Find the distance needed to slow down from start_speed to
    end_speed using maximum engine output.
    """
    sim = Simulation(None)
    sim.position = 0.0
    sim.speed = start_speed

    while sim.speed > end_speed:
        sim.step_simulate(1.0)
        # print 'position = %f  speed = %f' % (sim.position, sim.speed)

    return abs(sim.position)

def make_controller(b, h2, falling_speed):
    def controller(sim):
        if sim.position > h2:
            if sim.speed < falling_speed:
                return 0.0
            else:
                return b
        else:
            return 1.0

    return controller

if __name__ == '__main__':
    sim = Simulation(None)
    falling_speed = 0.95 * sim.max_speed
    landing_speed = 0.8 * sim.max_landing_speed


    print 'Finding b...'
    b = find_holding_thrust()

    print 'b = %f\n\nFinding h2...' % b
    h2 = find_distance(falling_speed, landing_speed)

    print 'h2 = %f\n\nPress enter to start simulation...' % h2
    junk = raw_input()
    sim.controller = make_controller(b, h2, falling_speed)
    print sim.simulate(debug = True)
