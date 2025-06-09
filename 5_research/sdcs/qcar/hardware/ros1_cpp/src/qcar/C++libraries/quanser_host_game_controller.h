#if !defined(_quanser_host_game_controller_h)
#define _quanser_host_game_controller_h

#include "quanser_host.h"
#include "quanser_packing.h"

#if defined(_WIN32) && (!defined(__MINGW32__) || defined(__QT__))
#pragma pack (push, 1)
#endif

#define INVALID_FORCE_FEEDBACK_EFFECT           (~0U)

#define FORCE_FEEDBACK_FLAG_DURATION_CHANGED        (1U << 0)   /* 0x00000001 */
#define FORCE_FEEDBACK_FLAG_DIRECTION_CHANGED       (1U << 1)   /* 0x00000002 */
#define FORCE_FEEDBACK_FLAG_DELAY_CHANGED           (1U << 2)   /* 0x00000004 */
#define FORCE_FEEDBACK_FLAG_ENVELOPE_CHANGED        (1U << 3)   /* 0x00000008 */
#define FORCE_FEEDBACK_FLAG_SPECIFIC_CHANGED        (1U << 4)   /* 0x00000010 */
#define FORCE_FEEDBACK_FLAG_PERIOD_CHANGED          (1U << 5)   /* 0x00000020 */
#define FORCE_FEEDBACK_FLAG_GAIN_CHANGED            (1U << 6)   /* 0x00000040 */
#define FORCE_FEEDBACK_FLAG_TRIGGER_BUTTON_CHANGED  (1U << 7)   /* 0x00000080 */
#define FORCE_FEEDBACK_FLAG_REPEAT_INTERVAL_CHANGED (1U << 8)   /* 0x00000100 */
#define FORCE_FEEDBACK_FLAG_DOWNLOAD                (1U << 24)  /* 0x01000000 */
#define FORCE_FEEDBACK_FLAG_RESTART                 (1U << 25)  /* 0x02000000 */
#define FORCE_FEEDBACK_FLAG_STOP                    (1U << 26)  /* 0x04000000 */
#define FORCE_FEEDBACK_FLAG_START                   (1U << 27)  /* 0x08000000 - Bits 28 through 31 are reserved */

typedef struct tag_force_feedback_envelope
{
    t_single attack_level;
    t_single attack_time;     /* in seconds */
    t_single fade_level;
    t_single fade_time;       /* in seconds */
} PACKED_ATTRIBUTE t_force_feedback_envelope;

typedef struct tag_force_feedback_parameters
{
    t_uint32 identifier;            /* unique identifier used to reference the effect (to change parameters on the fly) */
    t_uint32 flags;                 /* see FORCE_FEEDBACK_FLAG_XXX above */
    t_single duration;              /* in seconds (-1 = infinite) */
    t_single sample_period;         /* in seconds */
    t_single trigger_interval;      /* in seconds (also serves as number of iterations; -1 = not repetitive) */
    t_single start_delay;           /* in seconds */
    t_single gain;                  /* 0..1 */
    t_single direction[6];          /* direction and magnitude */
    t_force_feedback_envelope envelope;
    t_uint32 axes[6];               /* axes assignments */
    t_uint8  num_axes;              /* number of axes */
    t_int8   trigger_button;        /* 0..31 (-1 = no trigger) */
    t_uint8  reserved[2];           /* fill out to an even multiple of 4 bytes */
} PACKED_ATTRIBUTE t_force_feedback_parameters;

typedef struct tag_force_feedback_constant_force_parameters /* only Cartesian coordinates supported */
{
    t_force_feedback_parameters standard;
} PACKED_ATTRIBUTE t_force_feedback_constant_force_parameters;

/*
typedef struct tag_force_feedback_constant_force_command
{
    t_host_command_header header;
    t_force_feedback_constant_force_parameters parameters;
} PACKED_ATTRIBUTE t_force_feedback_constant_force_command;
*/

typedef struct tag_force_feedback_constant_force_configuration
{
    t_force_feedback_constant_force_parameters parameters;
    t_boolean manual;        
} PACKED_ATTRIBUTE t_force_feedback_constant_force_configuration;

typedef struct tag_force_feedback_set_constant_force
{
    t_force_feedback_constant_force_parameters parameters;
    t_uint32 modified_flags;
} PACKED_ATTRIBUTE t_force_feedback_set_constant_force;

typedef struct tag_force_feedback_add_constant_force_command
{
    t_host_command_header header;
    t_force_feedback_constant_force_configuration configuration;
} PACKED_ATTRIBUTE t_force_feedback_add_constant_force_command;

typedef struct tag_force_feedback_set_constant_force_command
{
    t_host_command_header header;
    t_force_feedback_set_constant_force updates;
} PACKED_ATTRIBUTE t_force_feedback_set_constant_force_command;

typedef struct tag_force_feedback_ramp_force_parameters /* only Cartesian coordinates supported */
{
    t_force_feedback_parameters standard;
    t_single start_magnitude;
    t_single end_magnitude;
} PACKED_ATTRIBUTE t_force_feedback_ramp_force_parameters;

/*
typedef struct tag_force_feedback_ramp_force_command
{
    t_host_command_header header;
    t_force_feedback_ramp_force_parameters parameters;
} PACKED_ATTRIBUTE t_force_feedback_ramp_force_command;
*/

typedef struct tag_force_feedback_ramp_force_configuration
{
    t_force_feedback_ramp_force_parameters parameters;
    t_boolean manual;        
} PACKED_ATTRIBUTE t_force_feedback_ramp_force_configuration;

typedef struct tag_force_feedback_set_ramp_force
{
    t_force_feedback_ramp_force_parameters parameters;
    t_uint32 modified_flags;
} PACKED_ATTRIBUTE t_force_feedback_set_ramp_force;

typedef struct tag_force_feedback_add_ramp_force_command
{
    t_host_command_header header;
    t_force_feedback_ramp_force_configuration configuration;
} PACKED_ATTRIBUTE t_force_feedback_add_ramp_force_command;

typedef struct tag_force_feedback_set_ramp_force_command
{
    t_host_command_header header;
    t_force_feedback_set_ramp_force updates;
} PACKED_ATTRIBUTE t_force_feedback_set_ramp_force_command;

typedef enum tag_force_feedback_periodic_waveform
{
    FORCE_FEEDBACK_PERIODIC_SQUARE,
    FORCE_FEEDBACK_PERIODIC_SINE,
    FORCE_FEEDBACK_PERIODIC_TRIANGLE,
    FORCE_FEEDBACK_PERIODIC_SAWTOOTH_UP,
    FORCE_FEEDBACK_PERIODIC_SAWTOOTH_DOWN,

    NUMBER_OF_FORCE_FEEDBACK_PERIODIC_WAVEFORMS
} t_force_feedback_periodic_waveform;

typedef struct tag_force_feedback_periodic_parameters /* only Cartesian coordinates supported */
{
    t_force_feedback_parameters standard;
    t_single offset;
    t_single phase;
    t_single period;
} PACKED_ATTRIBUTE t_force_feedback_periodic_parameters;

/*
typedef struct tag_force_feedback_periodic_command
{
    t_host_command_header header;
    t_force_feedback_periodic_parameters parameters;
} PACKED_ATTRIBUTE t_force_feedback_periodic_command;
*/

typedef struct tag_force_feedback_periodic_configuration
{
    t_force_feedback_periodic_parameters parameters;
    t_force_feedback_periodic_waveform periodic_type;
    t_boolean manual;        
} PACKED_ATTRIBUTE t_force_feedback_periodic_configuration;

typedef struct tag_force_feedback_set_periodic
{
    t_force_feedback_periodic_parameters parameters;
    t_uint32 modified_flags;
} PACKED_ATTRIBUTE t_force_feedback_set_periodic;

typedef struct tag_force_feedback_add_periodic_command
{
    t_host_command_header header;
    t_force_feedback_periodic_configuration configuration;
} PACKED_ATTRIBUTE t_force_feedback_add_periodic_command;

typedef struct tag_force_feedback_set_periodic_command
{
    t_host_command_header header;
    t_force_feedback_set_periodic updates;
} PACKED_ATTRIBUTE t_force_feedback_set_periodic_command;

typedef enum tag_force_feedback_condition_type
{
    FORCE_FEEDBACK_CONDITION_SPRING,
    FORCE_FEEDBACK_CONDITION_DAMPER,
    FORCE_FEEDBACK_CONDITION_INERTIA,
    FORCE_FEEDBACK_CONDITION_FRICTION,

    NUMBER_OF_FORCE_FEEDBACK_CONDITION_TYPES
} t_force_feedback_condition_type;

typedef struct tag_force_feedback_condition_coefficients
{
    t_single offset;
    t_single positive_coefficient;
    t_single negative_coefficient;
    t_single positive_saturation;
    t_single negative_saturation;
    t_single deadband;
} PACKED_ATTRIBUTE t_force_feedback_condition_coefficients;

typedef struct tag_force_feedback_condition_parameters /* only Cartesian coordinates supported */
{
    t_force_feedback_parameters standard;
    t_force_feedback_condition_coefficients conditions[6];
    t_uint num_conditions;
} PACKED_ATTRIBUTE t_force_feedback_condition_parameters;

typedef struct tag_force_feedback_condition_configuration
{
    t_force_feedback_condition_parameters parameters;
    t_force_feedback_condition_type condition_type;
    t_boolean manual;        
} PACKED_ATTRIBUTE t_force_feedback_condition_configuration;

typedef struct tag_force_feedback_set_condition
{
    t_force_feedback_condition_parameters parameters;
    t_uint32 modified_flags;
} PACKED_ATTRIBUTE t_force_feedback_set_condition;

typedef struct tag_force_feedback_add_condition_command
{
    t_host_command_header header;
    t_force_feedback_condition_configuration configuration;
} PACKED_ATTRIBUTE t_force_feedback_add_condition_command;

typedef struct tag_force_feedback_set_condition_command
{
    t_host_command_header header;
    t_force_feedback_set_condition updates;
} PACKED_ATTRIBUTE t_force_feedback_set_condition_command;

typedef struct tag_game_controller_states
{
    t_single x;                 /* x-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single y;                 /* y-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single z;                 /* z-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single rx;                /* rx-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single ry;                /* ry-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single rz;                /* rz-coordinate as a percentage of the range. Spans -1.0 to 1.0 */
    t_single sliders[2];        /* sliders as a percentage of the range. Spans 0.0 to 1.0 */
    t_single point_of_views[4]; /* point-of-view positions (in positive radians or -1 = centred). */
    t_uint32 buttons;           /* state of each of 32 buttons. If the bit corresponding to the button is 0 the button is released. If it is 1 then the button is pressed */
} PACKED_ATTRIBUTE t_game_controller_states;

typedef struct tag_host_game_controller_data
{
    t_host_data_header header;
    t_game_controller_states state;
} PACKED_ATTRIBUTE t_host_game_controller_data;

typedef struct tag_host_game_controller_configuration
{
    t_uint16 max_effects;           /* maximum number of force feedback effects supported. Enter 0 for a game controller without force feedback */
    t_uint16 buffer_size;           /* default should be 12 */
    t_uint16 deadzone[6];           /* per axis, 0..10000 = 0 to 100%. Use 0xffff to indicate unset. Default to empty matrix. */
    t_uint16 saturation[6];         /* per axis, 0..10000 = 0 to 100%. Use 0xffff to indicate unset. Default to empty matrix. */
    t_uint16 force_feedback_gain;   /* per device, 0..10000 = 0 to 100%. Default should be 10000. */
    t_uint8 controller_number;      /* 1..16 */
    t_boolean auto_center;          /* default to false for no auto-centering. Non-zero to enable auto-centering */
    t_boolean debug_mode;           /* enable/disable debug mode */
} PACKED_ATTRIBUTE t_host_game_controller_configuration;

typedef enum tag_game_controller_properties
{
    GAME_CONTROLLER_PROPERTY_ADD_CONDITION = HOST_COMMAND_SET_PROPERTY,
    GAME_CONTROLLER_PROPERTY_SET_CONDITION,
    GAME_CONTROLLER_PROPERTY_ADD_CONSTANT,
    GAME_CONTROLLER_PROPERTY_SET_CONSTANT,
    GAME_CONTROLLER_PROPERTY_ADD_PERIODIC,
    GAME_CONTROLLER_PROPERTY_SET_PERIODIC,
    GAME_CONTROLLER_PROPERTY_ADD_RAMP,
    GAME_CONTROLLER_PROPERTY_SET_RAMP,

    NUMBER_OF_GAME_CONTROLLER_PROPERTIES
} t_game_controller_properties;

#if defined(_WIN32) && (!defined(__MINGW32__) || defined(__QT__))
#pragma pack (pop)
#endif

#endif
