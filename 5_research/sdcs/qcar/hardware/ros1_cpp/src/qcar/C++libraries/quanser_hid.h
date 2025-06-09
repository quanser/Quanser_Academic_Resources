#if !defined(_quanser_hid_h)
#define _quanser_hid_h

#include "quanser_errors.h"
#include "quanser_host_game_controller.h"

/*------------------------- Game Controller Support ------------------------*/

typedef struct tag_game_controller * t_game_controller;

/* If max_force_feedback_effects == 0 then not f/f. */
EXTERN t_error
game_controller_open(t_uint8 controller_number, t_uint16 buffer_size, t_double deadzone[6], t_double saturation[6], t_boolean auto_center,
                     t_uint16 max_force_feedback_effects, t_double force_feedback_gain, t_game_controller * game_controller);

EXTERN t_error
game_controller_poll(t_game_controller controller, t_game_controller_states * state, t_boolean * is_new);

EXTERN t_error
game_controller_close(t_game_controller controller); 

#endif
