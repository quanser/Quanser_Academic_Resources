from .q_misc import Calculus, Utilities

saturate = Utilities.saturate

def speed_control(desired_speed, measured_speed, arm, dt, k_ff=0.1, k_p=0.1, k_i=0.1):
    ''' This function implements a feedforward + feedback speed controller for the QCar. You can provide gains optionally\n
    INPUTS:
    desired_speed - desired speed (m/s)
    measured_speed - longitudonal linear velocity of the car (m/s)
    arm - high (1) for enabled controller, low (0) will provide default 0 output
    dt - sample time of your loop

    OUTPUTS:
    pwm_duty_cycle - throttle (%)'''   

    # integrator object for feedback control
    integrator_1 = Calculus().integrator_variable(dt)
    next(integrator_1)
    
    # control equation with saturation and modulation w/ arm
    difference = arm*(desired_speed - measured_speed) 
    cmd =  k_ff * desired_speed  +  ( k_p * difference + integrator_1.send( (k_i * difference , dt ) ) )
    #      ----------------  +  ------------------------------------------------------------
    #      feedforward term  +                      feedback term
    
    # saturate output and return
    return arm*cmd