#if !defined(_HIL_H)
#define _HIL_H

#include "quanser_types.h"
#include "quanser_extern.h"
#include "quanser_errors.h"
#include "quanser_version.h"

#if defined(__APPLE__)

//! Project version number for hil framework.
EXTERN double hilVersionNumber;

//! Project version string for hil framework.
EXTERN const unsigned char hilVersionString[];

#endif

/*
    The name of a card type is not permitted to exceed this length.
    Card types exceeding this length will be truncated.
*/
#define MAX_CARD_TYPE_LENGTH    64

typedef struct tag_card *    t_card;
typedef struct tag_task *    t_task;
typedef struct tag_monitor * t_monitor;

typedef enum tag_clock
{
    SYSTEM_CLOCK_4    = -4,
    SYSTEM_CLOCK_3    = -3,
    SYSTEM_CLOCK_2    = -2,
    SYSTEM_CLOCK_1    = -1,

    HARDWARE_CLOCK_0  = 0,
    HARDWARE_CLOCK_1  = 1,
    HARDWARE_CLOCK_2  = 2,
    HARDWARE_CLOCK_3  = 3,
    HARDWARE_CLOCK_4  = 4,
    HARDWARE_CLOCK_5  = 5,
    HARDWARE_CLOCK_6  = 6,
    HARDWARE_CLOCK_7  = 7,
    HARDWARE_CLOCK_8  = 8,
    HARDWARE_CLOCK_9  = 9,
    HARDWARE_CLOCK_10 = 10,
    HARDWARE_CLOCK_11 = 11,
    HARDWARE_CLOCK_12 = 12,
    HARDWARE_CLOCK_13 = 13,
    HARDWARE_CLOCK_14 = 14,
    HARDWARE_CLOCK_15 = 15,
    HARDWARE_CLOCK_16 = 16,
    HARDWARE_CLOCK_17 = 17,
    HARDWARE_CLOCK_18 = 18,
    HARDWARE_CLOCK_19 = 19
} t_clock;

typedef enum tag_clock_mode
{
    CLOCK_TIMEBASE_MODE,    /* use clock as hardware timebase (default) */
    CLOCK_PWM_MODE,         /* use clock for PWM output */
    CLOCK_ENCODER_MODE,     /* use clock as an encoder input */

    NUMBER_OF_CLOCK_MODES
} t_clock_mode;

typedef enum tag_analog_input_configuration
{
    ANALOG_INPUT_RSE_CONFIGURATION,     /* return-referenced single-ended */
    ANALOG_INPUT_NRSE_CONFIGURATION,    /* non-return-referenced single-ended */
    ANALOG_INPUT_DIFF_CONFIGURATION,    /* differential */
    ANALOG_INPUT_PDIFF_CONFIGURATION,   /* pseudo-differential */

    NUMBER_OF_ANALOG_INPUT_CONFIGURATIONS
} t_analog_input_configuration;

typedef enum tag_pwm_mode
{
    PWM_DUTY_CYCLE_MODE,        /* PWM outputs vary in duty cycle by percentage*/
    PWM_FREQUENCY_MODE,         /* PWM outputs vary in frequency */
    PWM_PERIOD_MODE,            /* PWM outputs vary in period */
    PWM_ONE_SHOT_MODE,          /* PWM outputs vary in duty cycle, only a single pulse generated per write */
    PWM_TIME_MODE,              /* PWM outputs vary in duty cycle by specifying the active pulse time */
    PWM_ENCODER_EMULATION_MODE, /* PWM outputs vary in frequency by specifying counts/sec. Paired/complementary signals are 90 degrees out of phase. */
    PWM_RAW_MODE,               /* PWM outputs vary in duty cycle by raw board-specific values (used for DSHOT, for example, to allow throttle, telemetry and checksum to be encoded in a PWM output) */

    NUMBER_OF_PWM_MODES
} t_pwm_mode;

typedef enum tag_pwm_configuration
{
    PWM_UNIPOLAR_CONFIGURATION,
    PWM_BIPOLAR_CONFIGURATION,
    PWM_PAIRED_CONFIGURATION,
    PWM_COMPLEMENTARY_CONFIGURATION,

    NUMBER_OF_PWM_CONFIGURATIONS
} t_pwm_configuration;

typedef enum tag_pwm_alignment
{
    PWM_LEADING_EDGE_ALIGNED,
    PWM_TRAILING_EDGE_ALIGNED,
    PWM_CENTER_ALIGNED,

    NUMBER_OF_PWM_ALIGNMENTS
} t_pwm_alignment;

typedef enum tag_pwm_polarity
{
    PWM_ACTIVE_LOW_POLARITY,
    PWM_ACTIVE_HIGH_POLARITY,

    NUMBER_OF_PWM_POLARITIES
} t_pwm_polarity;

typedef enum tag_encoder_quadrature_mode
{
    ENCODER_QUADRATURE_NONE = 0,    /* No quadrature. Inputs are count and direction. */
    ENCODER_QUADRATURE_1X   = 1,    /* 1X. Inputs are A and B channels. */
    ENCODER_QUADRATURE_2X   = 2,    /* 2X. Inputs are A and B channels. */
    ENCODER_QUADRATURE_4X   = 4     /* 4X. Inputs are A and B channels. */
} t_encoder_quadrature_mode;

typedef enum tag_digital_configuration
{
    DIGITAL_OPEN_COLLECTOR_CONFIGURATION,   /* 0 = open collector */
    DIGITAL_TOTEM_POLE_CONFIGURATION,       /* 1 = totem-pole */

    NUMBER_OF_DIGITAL_CONFIGURATIONS
} t_digital_configuration;

typedef enum tag_digital_state
{
    DIGITAL_STATE_LOW,
    DIGITAL_STATE_HIGH,
    DIGITAL_STATE_TRISTATE,
    DIGITAL_STATE_NO_CHANGE,

    NUM_DIGITAL_STATES
} t_digital_state;

typedef enum tag_digital_mode
{
    DIGITAL_MODE_DIN,
    DIGITAL_MODE_DOUT,
    DIGITAL_MODE_PWM,
    DIGITAL_MODE_ENC,
    DIGITAL_MODE_SPI,
    DIGITAL_MODE_I2C,
    DIGITAL_MODE_UART,

    NUM_DIGITAL_MODES
} t_digital_mode;

typedef enum tag_hil_integer_property
{
    /* Product identification */
    PROPERTY_INTEGER_VENDOR_ID,
    PROPERTY_INTEGER_PRODUCT_ID,
    PROPERTY_INTEGER_SUBVENDOR_ID,
    PROPERTY_INTEGER_SUBPRODUCT_ID,

    /* Product version information */
    PROPERTY_INTEGER_MAJOR_VERSION,
    PROPERTY_INTEGER_MINOR_VERSION,
    PROPERTY_INTEGER_BUILD,
    PROPERTY_INTEGER_REVISION,
    PROPERTY_INTEGER_DATE,
    PROPERTY_INTEGER_TIME,

    /* Firmware version information */
    PROPERTY_INTEGER_FIRMWARE_MAJOR_VERSION,
    PROPERTY_INTEGER_FIRMWARE_MINOR_VERSION,
    PROPERTY_INTEGER_FIRMWARE_BUILD,
    PROPERTY_INTEGER_FIRMWARE_REVISION,
    PROPERTY_INTEGER_FIRMWARE_DATE,
    PROPERTY_INTEGER_FIRMWARE_TIME,

    /* Channel information */
    PROPERTY_INTEGER_NUMBER_OF_ANALOG_INPUTS,
    PROPERTY_INTEGER_NUMBER_OF_ENCODER_INPUTS,
    PROPERTY_INTEGER_NUMBER_OF_DIGITAL_INPUTS,
    PROPERTY_INTEGER_NUMBER_OF_OTHER_INPUTS,

    PROPERTY_INTEGER_NUMBER_OF_ANALOG_OUTPUTS,
    PROPERTY_INTEGER_NUMBER_OF_PWM_OUTPUTS,
    PROPERTY_INTEGER_NUMBER_OF_DIGITAL_OUTPUTS,
    PROPERTY_INTEGER_NUMBER_OF_OTHER_OUTPUTS,

    PROPERTY_INTEGER_NUMBER_OF_CLOCKS,
    PROPERTY_INTEGER_NUMBER_OF_INTERRUPTS,

    PROPERTY_INTEGER_PRODUCT_SPECIFIC = 128,

    /* HiQ specific integer properties */
    PROPERTY_INTEGER_HIQ_GYRO_RANGE = PROPERTY_INTEGER_PRODUCT_SPECIFIC,
    PROPERTY_INTEGER_HIQ_MAGNETOMETER_MODE,
    PROPERTY_INTEGER_HIQ_BLDC_MAX_PWM_TICKS,
    PROPERTY_INTEGER_HIQ_BLDC_RAMPUP_DELAY,
    PROPERTY_INTEGER_HIQ_BLDC_MAX_DUTY_CYCLE,
    PROPERTY_INTEGER_HIQ_BLDC_MIN_DUTY_CYCLE,
    PROPERTY_INTEGER_HIQ_BLDC_POLE_PAIRS,
    PROPERTY_INTEGER_HIQ_PWM_MODE,

    /* QBus specific integer properties */
    PROPERTY_INTEGER_QBUS_NUM_MODULES = PROPERTY_INTEGER_PRODUCT_SPECIFIC,

    /* Kobuki specific integer properties */
    PROPERTY_INTEGER_KOBUKI_UDID0 = PROPERTY_INTEGER_PRODUCT_SPECIFIC,
    PROPERTY_INTEGER_KOBUKI_UDID1,
    PROPERTY_INTEGER_KOBUKI_UDID2
} t_hil_integer_property;

typedef enum tag_hil_double_property
{
    PROPERTY_DOUBLE_PRODUCT_SPECIFIC = 128,

    /* HiQ specific double properties */
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_0 = PROPERTY_DOUBLE_PRODUCT_SPECIFIC,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_1,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_2,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_3,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_4,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_5,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_6,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_7,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_8,
    PROPERTY_DOUBLE_HIQ_SERVO_FINAL_VALUE_CH_9,

    /* Kobuki-specific double properties */
    PROPERTY_DOUBLE_KOBUKI_P_GAIN = PROPERTY_DOUBLE_PRODUCT_SPECIFIC,
    PROPERTY_DOUBLE_KOBUKI_I_GAIN,
    PROPERTY_DOUBLE_KOBUKI_D_GAIN

} t_hil_double_property;

typedef enum tag_hil_string_property
{
    PROPERTY_STRING_MANUFACTURER,
    PROPERTY_STRING_PRODUCT_NAME,
    PROPERTY_STRING_MODEL_NAME,
    PROPERTY_STRING_SERIAL_NUMBER,
    PROPERTY_STRING_FIRMWARE_VERSION, /* may not match the integer properties as some firmware versions better expressed as a string */

    PROPERTY_STRING_PRODUCT_SPECIFIC = 128

} t_hil_string_property;

enum tag_other_channel_assignments
{
      OTHER_CHANNELS_LINEAR_POSITIONS      = 0      /* X, Y, Z linear position in metres (ie. 0=X1, 1=Y1, 2=Z1, 3=X2, 4=Y2, etc.) [altitude] */
    , OTHER_CHANNELS_ANGULAR_POSITIONS     = 1000   /* Rx, Ry, Rz angular position in radians */
    , OTHER_CHANNELS_LINEAR_VELOCITIES     = 2000   /* X, Y, Z linear velocity in m/s */
    , OTHER_CHANNELS_ANGULAR_VELOCITIES    = 3000   /* Rx, Ry, Rz angular velocity in rad/s [gyros] */
    , OTHER_CHANNELS_LINEAR_ACCELERATIONS  = 4000   /* X, Y, Z linear acceleration in m/s^2 [accelerometers] */
    , OTHER_CHANNELS_ANGULAR_ACCELERATIONS = 5000   /* Rx, Ry, Rz angular acceleration in rad/s^2 */
    , OTHER_CHANNELS_FORCES                = 6000   /* X, Y, Z force in N */
    , OTHER_CHANNELS_TORQUES               = 7000   /* Rx, Ry, Rz torque in N-m */
    , OTHER_CHANNELS_MAGNETIC_FIELDS       = 8000   /* X, Y, Z magnetic field in Teslas [magnetometer] */
    , OTHER_CHANNELS_PRESSURE              = 9000   /* Pressure in Pascals [airspeed and altimeter] */
    , OTHER_CHANNELS_TEMPERATURE           = 10000  /* Temperature in Celcius [temperature sensors] */
    , OTHER_CHANNELS_OPERATING_CAPACITY    = 11000  /* Operating capacity as a percentage (0.0 to 1.0 representing 0% to 100% for unipolar outputs or -1.0 to 1.0 representing -100% to 100% for bipolar outputs) */
    , OTHER_CHANNELS_TIME                  = 12000  /* Time in seconds (eg., time since bootup, time since last read, etc) */
    , OTHER_CHANNELS_COUNTS                = 13000  /* Counts [Geiger counter] */
    , OTHER_CHANNELS_COUNTS_PER_SECOND     = 14000  /* Counts per second [Geiger counter, encoder velocities]. Also used for frequency (Hz) */
    , OTHER_CHANNELS_COUNTS_PER_SECOND_2   = 15000  /* Counts per second squared [encoder accelerations] */
    , OTHER_CHANNELS_ENUMERATION           = 16000  /* Enumerated operations e.g. move left, right, forward, backward. */
	, OTHER_CHANNELS_RAW_DATA              = 17000  /* Raw data for sensor measurements or device commands */
	, OTHER_CHANNELS_CALIBRATION_DATA      = 18000  /* Calibration data */
    , OTHER_CHANNELS_RESISTANCE            = 19000  /* Resistance in Ohms */
};

enum tag_interrupt_source_assignments
{
      INTERRUPT_SOURCE_DIGITAL_INPUT            = 0         /* edge or level detected on digital input */
    , INTERRUPT_SOURCE_ENCODER_INDEX_PULSE      = 1000      /* encoder index pulse occurred */
    , INTERRUPT_SOURCE_ANALOG_THRESHOLD         = 2000      /* analog threshold exceeded */
    , INTERRUPT_SOURCE_TIMER                    = 3000      /* timer expired */
    , INTERRUPT_SOURCE_ERROR                    = 4000      /* error occurred. Specific errors enumerated below. */
    , INTERRUPT_SOURCE_ERROR_ESTOP              = 4000      /* emergency stop hit */
    , INTERRUPT_SOURCE_ERROR_MEMORY_FAILURE     = 4100      /* memory failure occurred */
    , INTERRUPT_SOURCE_ERROR_OSCILLATOR_FAILURE = 4101      /* oscillator failure occurred */
    , INTERRUPT_SOURCE_ERROR_STACK_OVERFLOW     = 4102      /* stack overflowed */
    , INTERRUPT_SOURCE_ERROR_PAGE_FAULT         = 4103      /* page fault occurred */
    , INTERRUPT_SOURCE_ERROR_DIVIDE_BY_ZERO     = 4104      /* division by zero occurred */
    , INTERRUPT_SOURCE_ERROR_NUMERIC_OVERFLOW   = 4105      /* numeric overflow occurred */
    , INTERRUPT_SOURCE_ERROR_LOW_VOLTAGE        = 4200      /* low voltage condition detected */
    , INTERRUPT_SOURCE_ERROR_OVER_VOLTAGE       = 4300      /* over-voltage condition detected */
    , INTERRUPT_SOURCE_ERROR_NOISE              = 4400      /* excessive noise detected */
    , INTERRUPT_SOURCE_USER                     = 30000     /* user-defined interrupt sources should be defined above this number */
};

typedef enum tag_buffer_overflow_mode
{
    BUFFER_MODE_ERROR_ON_OVERFLOW,      /* return an error on buffer overflow (default). */
    BUFFER_MODE_OVERWRITE_ON_OVERFLOW,  /* overwrite old samples on buffer overflow. */
    BUFFER_MODE_DISCARD_ON_OVERFLOW,    /* discard new samples on buffer overflow. */
    BUFFER_MODE_WAIT_ON_OVERFLOW,       /* waits on buffer overflow for space to become available (not supported by hardware cards, only for use by simulated cards) */
    BUFFER_MODE_SYNCHRONIZE,            /* provides complete buffer synchronization (not supported by hardware cards, only for use by simulated cards) */

    NUMBER_OF_BUFFER_OVERFLOW_MODES
} t_buffer_overflow_mode;

/*------------------------ Configuration operations ------------------------*/

/*
    Name:   hil_get_version

    Description:

    This function fills in the t_version structure passed as an argument with the
    current version of the HIL API. Before calling this function, initialize the
    size field of the t_version structure with the size of the t_version structure.
    For example,
    
        t_version version;
        t_error result;

        version.size = sizeof(version);
        result = hil_get_version(&version);

    The version structure is defined in quanser_version.h. It contains the major
    and minor release numbers as well as the release and build numbers.

    Parameters:

    version = the address of a t_version structure to be filled in by the call

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.
*/
EXTERN t_error
hil_get_version(t_version * version);

/*
    Name:   hil_open

    Description:

    Opens a particular instance of a hardware-in-the-loop or data acquisition card.
    The type of card to open is specified by the card_type parameter. For example,
    the string "q8" identifies Quanser's Q8 card. 
    
    The card_identifier field is used to differentiate between multiple instances 
    of a board. For example, if there is more than one Q8 in the system, then an 
    identifier of "0" would be used for the first board and an identifier of "1" 
    for the second board. In general, the card identifier is the string representation
    of a zero-based index. In other words, "0" represents the first board of the
    given type in the system, "1" represents the second board, etc. However, some
    drivers support other options for the card identifier. For example, the NI drivers
    for the QUARC Windows target allow the name of the board to be specified as it
    appears in the NI Measurement and Automation Explorer (MAX). For example, for the NI
    cards, "Dev1" may be used as a card identifier if that is the name given to a
    card in MAX. Read the QUARC documentation specific to your card for more information
    on the card identifier.

    The final argument is the address of a t_card handle in which the hil_open function
    stores the handle to the board. All but a couple of the HIL API functions require
    this handle in order to identify the board. The handle is an opaque data structure
    whose fields cannot (and should not) be accessed.

    If the card identifier is preceded by a '*' e.g. "*myboard" then the name following
    the '*' is located as a value under the registry key SOFTWARE/Quanser/QUARC/Cards/<card_type>/
    and the registry value associated with that name is used as the card identifier instead.
    This mechanism allows card identifiers to be configured externally so that
    "virtual card names" may be assigned.

    If the card identifier contains takes the form <card id>@<uri> then the card is
    accessed remotely via the URI. The URI must refer to a HIL Proxy Server which is
    interfacing with the actual HIL device on a remote machine.

    Parameters:

    card_type       = a string indicating the type of card e.g. "q8", "q3_controlpaq_fw"
    card_identifier = a string identifying the particular instance of that card type e.g. "0", "Dev1"
    card            = the address of a t_card variable in which to store the handle to the card

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.
*/
EXTERN t_error
hil_open(const char * card_type,  const char * card_identifier, t_card * card);

EXTERN t_error
hil_wopen(const wchar_t * card_type,  const wchar_t * card_identifier, t_card * card);

#if defined(_UNICODE)
#define hil_topen   hil_wopen
#else
#define hil_topen   hil_open
#endif

/*
    Name:   hil_is_valid

    Description:

    Returns true if the given card is valid i.e. opened. If the card has been closed, then
    this function returns false.

    Parameters:

    card  = a t_card variable containing the handle to the card. It must be obtained
            using the hil_open function.

    Return value:

    Returns true if the card is valid and open. Otherwise it returns false.
*/
EXTERN t_boolean
hil_is_valid(t_card card);

/*
    Name:   hil_close

    Description:

    Closes a card. Once a card has been closed, the t_card handle may no longer be used.

    Parameters:

    card  = a t_card variable containing the handle to the card. It must be obtained
            using the hil_open function.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.
*/
EXTERN t_error
hil_close(t_card card);

/*
    Name:   hil_close_all

    Description:

    Closes all open cards. The HIL API keeps track of all open cards to ensure that
    even if a card handle is lost, the card may still be closed. This function
    closes all open cards. After calling hil_close_all, every t_card handle is
    invalidated and may no longer be used.

    Parameters:

    none

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.
*/
EXTERN t_error
hil_close_all(void);

/** THESE TWO FUNCTIONS ARE STILL UNDER DEVELOPMENT. DO NOT USE. **/

EXTERN t_error
hil_acquire_exclusive_access(t_card card, void * card_specific);

EXTERN t_error
hil_release_exclusive_access(t_card card, void * card_specific);

/*
    Name:   hil_set_analog_input_ranges

    Description:

    Sets the ranges of the analog inputs. Not all cards support programmable input ranges.
    Some cards only allow the ranges of all inputs to be set to the same value, rather than
    allowing each analog input to have a separate input range. Refer to the documentation
    for your card for details on the features supported by the card.

    The units for the minimum and maximum values are typically Volts, but may be Amps or
    a unit appropriate to the specific card.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    analog_channels = an array of unsigned integers (t_uint32) containing the analog input
                      channels whose ranges will be set. Channel numbers are zero-based. Thus,
                      channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the analog_channels array
    minimums        = an array of doubles (t_double) containing the minimum value of the input
                      range for the corresponding channel in the analog_channels array. This
                      array must be the same size as the analog_channels array.
    maximums        = an array of doubles (t_double) containing the maximum value of the input
                      range for the corresponding channel in the analog_channels array. This
                      array must be the same size as the analog_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = {  0,  3,  5 };
    t_double minimums[] = { -10, 0, -5 };
    t_double maximums[] = { +10, 5, +5 };
    t_error  result;

    // Set the range of analog input #0 to +/-10V, the range of analog input #3 to 0..5V
    // and the range of input #5 to +/-5V.
    result = hil_set_analog_input_ranges(card, channels, 3, minimums, maximums);
*/
EXTERN t_error
hil_set_analog_input_ranges(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, 
                            const t_double minimums[], const t_double maximums[]);

/*
    Name:   hil_set_analog_input_configuration

    Description:

    Sets the configurations of the analog inputs (single-ended/differential etc).
    Not all cards support programmable input configurations. Refer to the documentation
    for your card for details on the features supported by the card.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    analog_channels = an array of unsigned integers (t_uint32) containing the analog input
                      channels whose terminal configurations will be set. Channel numbers are
                      zero-based. Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the analog_channels array
    configurations  = an array of t_analog_input_configuration containing the configuration value of the
                      input for the corresponding channel in the analog_channels array. This
                      array must be the same size as the analog_channels array. Valid values are:
                          ANALOG_INPUT_RSE_CONFIGURATION - the input is referenced single-ended
                          ANALOG_INPUT_NRSE_CONFIGURATION - the input is non-referenced single-ended
                          ANALOG_INPUT_DIFF_CONFIGURATION - the input is differential
                          ANALOG_INPUT_PDIFF_CONFIGURATION - the input is pseudo-differential
                      Which input is of which type depends on the hardware card. Refer to the
                      documentation for your card for details on the supported configuration type.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]                   = { 0, 3, 5 };
    t_analog_input_configuration configs[] = { 0, 0, 2 };
    t_error  result;

    // Set the configuration of analog input #0 to be referenced single-ended,
    // the configuraiton of analog input #3 to be referenced single-ended,
    // and the configuration of analog input #5 to be differential.
    result = hil_set_analog_input_configuration(card, channels, 3, configs);
*/
EXTERN t_error
hil_set_analog_input_configuration(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, 
                                   const t_analog_input_configuration config[]);

/*
    Name:   hil_set_analog_output_ranges

    Description:

    Sets the ranges of the analog outputs. Not all cards support programmable output ranges.
    Some cards only allow the ranges of all outputs to be set to the same value, rather than
    allowing each analog output to have a separate output range. Refer to the documentation
    for your card for details on the features supported by the card.

    The units for the minimum and maximum values are typically Volts, but may be Amps or
    a unit appropriate to the specific card.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    analog_channels = an array of unsigned integers (t_uint32) containing the analog output
                      channels whose ranges will be set. Channel numbers are zero-based. Thus,
                      channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the analog_channels array
    minimums        = an array of doubles (t_double) containing the minimum value of the output
                      range for the corresponding channel in the analog_channels array. This
                      array must be the same size as the analog_channels array.
    maximums        = an array of doubles (t_double) containing the maximum value of the output
                      range for the corresponding channel in the analog_channels array. This
                      array must be the same size as the analog_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = {  0,  3,  5 };
    t_double minimums[] = { -10, 0, -5 };
    t_double maximums[] = { +10, 5, +5 };
    t_error  result;

    // Set the range of analog output #0 to +/-10V, the range of analog output #3 to 0..5V
    // and the range of output #5 to +/-5V.
    result = hil_set_analog_output_ranges(card, channels, 3, minimums, maximums);
*/
EXTERN t_error
hil_set_analog_output_ranges(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, 
                             const t_double minimums[], const t_double maximums[]);

/*
    Name:   hil_set_encoder_counts

    Description:

    Sets the current value of the counters for the encoder inputs on the card. Many cards
    do not support encoders. However, cards that do provide encoders typically support
    this function. Encoder values are specified as a 32-bit signed integer. Most cards
    do not support a full 32-bit counter for the encoders, although the Quanser Q8-series
    of cards do. If a card supports less then 32-bits, such as 24-bit or 16-bit counters,
    then the count values should be specified within the appropriate range.

    Parameters:

    card             = a t_card variable containing the handle to the card. It must be obtained
                       using the hil_open function.
    encoder_channels = an array of unsigned integers (t_uint32) containing the encoder input
                       channels whose counter values will be set. Channel numbers are zero-based. 
                       Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels     = the number of channels in the encoder_channels array
    buffer           = an array of signed integers (t_int32) containing the new counter 
                       values. There must be one element for each encoder channel specified in
                       the encoder_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = {  0,    1,     2 };
    t_int32  counts[]   = {  1000, 0, -1000 };
    t_error  result;

    // Set the count values of the first three encoder channels to
    // 1000, 0 and -1000 respectively.
    result = hil_set_encoder_counts(card, channels, 3, counts);
*/
EXTERN t_error
hil_set_encoder_counts(t_card card, const t_uint32 encoder_channels[], t_uint32 num_channels, const t_int32 buffer[]);

/*
    Name:   hil_set_encoder_quadrature_mode

    Description:

    Sets the quadrature mode of the encoder inputs on the card. Many cards do not
    support encoders. Cards which do provide encoders may not support different
    quadrature modes, or may not support different quadrature modes for each
    channel. Valid quadrature modes are:

        ENCODER_QUADRATURE_NONE = No quadrature. Inputs are count and direction.
        ENCODER_QUADRATURE_1X   = 1X. Inputs are A and B channels.
        ENCODER_QUADRATURE_2X   = 2X. Inputs are A and B channels.
        ENCODER_QUADRATURE_4X   = 4X. Inputs are A and B channels.

    The Quanser Q8-series support all the quadrature modes and each channel may
    be assigned a different mode. The 4X quadrature mode is typically the mode used
    for encoders because it provides the highest encoder resolution. The non-quadrature
    mode is used for frequency counting and other applications where count and direction
    inputs are required rather than standard A/B encoder inputs.

    Parameters:

    card             = a t_card variable containing the handle to the card. It must be obtained
                       using the hil_open function.
    encoder_channels = an array of unsigned integers (t_uint32) containing the encoder input
                       channels whose counter values will be set. Channel numbers are zero-based. 
                       Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels     = the number of channels in the encoder_channels array
    mode             = an array of t_encoder_quadrature constants containing the new encoder
                       quadrature mode for each channel. There must be one element for each 
                       encoder channel specified in the encoder_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = { 0, 1, 2 };
    t_int32  modes[]    = { ENCODER_QUADRATURE_4X, ENCODER_QUADRATURE_NONE, ENCODER_QUADRATURE_4X };
    t_error  result;

    // Set the quadrature mode of channels 0 and 2 to 4X quadrature and
    // set channel 1 to non-quadrature mode.
    result = hil_set_encoder_quadrature_mode(card, channels, 3, modes);
*/
EXTERN t_error
hil_set_encoder_quadrature_mode(t_card card, const t_uint32 encoder_channels[], t_uint32 num_channels, const t_encoder_quadrature_mode mode[]);

/*
    Name:   hil_set_encoder_filter_frequency

    Description:

    Some cards support filtering of their encoder inputs. This function sets the filter
    frequency of the encoder inputs on the card. Note that many cards do not
    support encoders. Cards which do provide encoders may not support filtering or different
    filter frequencies, or may not support different filter frequencies for each
    channel.

    The Quanser Q8-series support programmable filter frequencies and each channel may
    be assigned a different frequency. The fastest frequency is generally used so that
    the encoder inputs can handle the fastest possible A/B inputs. A slower filter
    frequency may be required in noisy environments. However, be aware that noisy
    encoder inputs is often an indication of a grounding problem or inadequate shielding,
    so be sure to check ground and shield connections carefully before resorting to
    more filtering of the encoder inputs. Filter frequencies will be rounded to the
    nearest filter frequency supported by the card.

    Parameters:

    card             = a t_card variable containing the handle to the card. It must be obtained
                       using the hil_open function.
    encoder_channels = an array of unsigned integers (t_uint32) containing the encoder input
                       channels whose counter values will be set. Channel numbers are zero-based. 
                       Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels     = the number of channels in the encoder_channels array
    frequency        = an array of doubles containing the new encoder filter frequencies in Hz
                       for each channel. There must be one element for each encoder channel 
                       specified in the encoder_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]  = { 0, 2, 4 };
    t_int32  frequency[] = { 1 /(120e-9 * 1), 1 /(120e-9 * 2), 1 /(120e-9 * 1) };
    t_error  result;

    // Set the filter frequencies of channels 0 and 4 to 8.33 MHz and
    // set channel 2 to 4.17 MHz.
    result = hil_set_encoder_filter_frequency(card, channels, 3, frequency);
*/
EXTERN t_error
hil_set_encoder_filter_frequency(t_card card, const t_uint32 encoder_channels[], t_uint32 num_channels, const t_double frequency[]);

/*
    Name:   hil_set_digital_directions

    Description:

    Sets the direction of digital I/O lines. Many cards which support digital I/O allow
    the digital I/O lines to be programmed as inputs or outputs. Some cards organize the
    digital I/O into "ports" and only allow the direction of the port as a whole to be
    programmed. Others, like the Quanser Q8-series, allow each digital I/O line to be
    programmed individually. Pass this function a list of all those digital I/O lines
    which should be configured as inputs and a list of those to be programmed as outputs.
    Any digital I/O lines not present in either list will be left untouched. Cards
    which group digital I/O lines into "ports" and only allow the direction of the port 
    to be configured should return an error if some of the digital I/O lines in the port
    are programmed for opposing directions.

    Parameters:

    card                = a t_card variable containing the handle to the card. It must be obtained
                          using the hil_open function.
    digital_inputs      = an array of unsigned integers (t_uint32) containing the digital I/O
                          channels to be configured as inputs. Channel numbers are zero-based. 
                          Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_digital_inputs  = the number of channels in the digital_inputs array
    digital_outputs     = an array of unsigned integers (t_uint32) containing the digital I/O
                          channels to be configured as outputs. Channel numbers are zero-based. 
                          Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_digital_outputs = the number of channels in the digital_outputs array

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 input_channels[]  = { 0, 2, 4, 6 };
    t_uint32 output_channels[] = { 1, 3, 5, 7 };
    t_error  result;

    // Program the even channels as inputs and the odd channels as outputs
    // in an 8-bit digital I/O port.
    result = hil_set_digital_directions(card, input_channels, 4, output_channels, 4);
*/
EXTERN t_error
hil_set_digital_directions(t_card card, const t_uint32 digital_inputs[], t_uint32 num_digital_inputs, const t_uint32 digital_outputs[], t_uint32 num_digital_outputs);

/*
    Name:   hil_set_digital_output_configuration

    Description:

    Sets the configuration of digital output lines. Two output configurations are possible:
        DIGITAL_TOTEM_POLE_CONFIGURATION     = use a totem-pole output (active high and active low)
        DIGITAL_OPEN_COLLECTOR_CONFIGURATION = use an open-collector output (passive high, active low)
    Cards which have totem-pole outputs normally drive the output high or low actively. However,
    these outputs can simulate open-collector outputs by making the output tristate for a "high" output
    and active low for a "low" output. This function allows this emulation to be configured. Some
    cards allow the configuration to be programmed on a per-channel basis.

    Parameters:

    card                = a t_card variable containing the handle to the card. It must be obtained
                          using the hil_open function.
    channels            = an array of unsigned integers (t_uint32) containing the digital output
                          channels to be configured. Channel numbers are zero-based. 
                          Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels        = the number of channels in the channels array
    configurations      = an array of t_digital_configuration values indicating whether to use
                          totem-pole outputs (typically the default) or open-collector outputs.
                          There must be one element for each channel in the channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]  = { 0, 1, 2, 3 };
    t_digital_configuration configurations[] = { DIGITAL_TOTEM_POLE_CONFIGURATION, DIGITAL_OPEN_COLLECTOR_CONFIGURATION, DIGITAL_TOTEM_POLE_CONFIGURATION, DIGITAL_OPEN_COLLECTOR_CONFIGURATION };
    t_error result;

    // Program the even channels as totem-pole outputs and the odd channels as open-collector outputs.
    result = hil_set_digital_output_configuration(card, channels, 4, configurations);
*/
EXTERN t_error
hil_set_digital_output_configuration(t_card card, const t_uint32 channels[], t_uint32 num_channels, const t_digital_configuration configurations[]);

/*
    Name:   hil_set_clock_mode

    Description:

    Sets the mode of hardware timers on the card. Many cards support at least one
    timer. This timer may be multi-purpose, which different modes available. For
    example, the Quanser Q8-series has two 32-bit counters. Each counter may be
    configured as a clock (hardware timebase) or a PWM output. Other cards allow
    their counters to be used as a clock or an encoder counter. Not all cards
    support this flexibility and will return an error if the desired mode is
    unavailable. The modes currently available for this function are:

        CLOCK_TIMEBASE_MODE = use clock as hardware timebase (default)
        CLOCK_PWM_MODE      = use clock for PWM output
        CLOCK_ENCODER_MODE  = use clock as an encoder input

    Clocks are specified using one of the HARDWARE_CLOCK_<n> constants defined
    in this header file. The first clock is HARDWARE_CLOCK_0, the second clock
    is HARDWARE_CLOCK_1, etc. These constants are merely provided for greater
    readability. Hardware clocks may also be specified as a zero-based index,
    with 0 being the first clock, 1 being the second clock, etc. Thus, there
    may be more clocks on the card than there are HARDWARE_CLOCK_<n> constants.

    Note that this function may change the number of PWM channels available. Therefore,
    this function should be called prior to any of the PWM functions, in general.

    Parameters:

    card        = a t_card variable containing the handle to the card. It must be obtained
                  using the hil_open function.
    clocks      = an array of t_clock values containing the clocks whose modes will be set.
                  Clock numbers are zero-based. Thus, clock 0 is the first clock, clock 1 
                  the second clock, etc. Use the HARDWARE_CLOCK_<n> constants for greater
                  readability.
    num_clocks  = the number of channels in the clocks array
    modes       = an array of t_clock_mode values containing the new operational mode
                  for each clock. There must be one element for each clock specified
                  in the clocks array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 clocks[] = { HARDWARE_CLOCK_0,    HARDWARE_CLOCK_1 };
    t_int32  modes[]  = { CLOCK_TIMEBASE_MODE, CLOCK_PWM_MODE   };
    t_error  result;

    // Use clock 0 as a hardware timebase and use clock 1 as a PWM output
    result = hil_set_clock_mode(card, clocks, 2, modes);
*/
EXTERN t_error
hil_set_clock_mode(t_card card, const t_clock clocks[], t_uint32 num_clocks, const t_clock_mode modes[]);

/*
    Name:   hil_set_clock_frequency

    Description:

    Sets the frequency of the specified clocks. The clocks will be programmed to expire at the
    given frequencies. If a frequency of zero is indicated for a particular clock then that
    clock will be disabled (if possible).

    Parameters:

    card             = a t_card variable containing the handle to the card. It must be obtained
                       using the hil_open function.
    channels         = an array of t_clock values indicating the hardware clocks whose frequency
                       will be set. Channel numbers are zero-based. Thus, channel 0 is the first 
                       clock, channel 1 the second clock, etc.
    num_channels     = the number of channels in the channels array
    buffer           = an array of doubles containing the clock frequencies in Hertz.
                       There must be one element for each encoder channel specified in
                       the channels array. Use a frequency of zero to disable a clock.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]    = {  0,    1,     2    };
    t_int32  frequencies[] = {  1000, 50000, 3000 };
    t_error  result;

    // Set the frequencies of the first three clocks to 1 kHz, 50 kHz and 3 kHz respectively.
    result = hil_set_clock_frequency(card, channels, 3, frequencies);
*/
EXTERN t_error
hil_set_clock_frequency(t_card card, const t_clock channels[], t_uint32 num_channels, const t_double frequency[]);

/*
    Name:   hil_set_pwm_mode

    Description:

    Sets the mode used for the PWM channels. Most cards do not support different modes
    for their PWM channels but the Quanser Q8-series do. The duty cycle of PWM outputs
    is typically what is varied when driving these outputs, while maintaining a fixed
    PWM frequency. However, the Q8-series also allow the frequency or period of the PWM 
    outputs to be varied while maintaining a fixed duty cycle. Such frequency modulation
    is analogous to an FM radio signal, which also modulates frequency. Valid modes are:
    
        PWM_DUTY_CYCLE_MODE = PWM outputs vary in duty cycle
        PWM_FREQUENCY_MODE  = PWM outputs vary in frequency
        PWM_PERIOD_MODE     = PWM outputs vary in period

    Changing the PWM output mode affects how the values provided to functions such as 
    hil_write_pwm are interpreted. In duty cycle mode, which is the default, the input 
    to hil_write_pwm is treated as a duty cycle. Valid values range from -1 to 1, where
    a magnitude of 1 indicates a 100% duty cycle and 0 means a 0% duty cycle. The sign
    determines the direction. For cards with bipolar PWM outputs, the sign determines
    the polarity of the output. Otherwise the sign may change the value of another
    output pin or negative duty cycles will not be supported by the card.
    
    In frequency mode, the values passed to functions such as hil_write_pwm are interpreted 
    as new PWM frequencies in Hz. 
    
    Finally, in period mode, the values are treated as new PWM periods (1 / frequency) 
    in seconds.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    pwm_channels    = an array of unsigned integers (t_uint32) containing the PWM output
                      channels whose counter values will be set. Channel numbers are zero-based. 
                      Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the pwm_channels array
    mode            = an array of t_pwm_mode values containing the new PWM modes for
                      each channel. There must be one element for each PWM channel 
                      specified in the pwm_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = { 0, 1, 2 };
    t_int32  modes[]    = { PWM_DUTY_CYCLE_MODE, PWM_DUTY_CYCLE_MODE, PWM_FREQUENCY_MODE };
    t_error  result;

    // Set the modes of the first two PWM channels to duty cycle mode and
    // the mode of the third channel to frequency mode.
    result = hil_set_pwm_mode(card, channels, 3, modes);
*/
EXTERN t_error
hil_set_pwm_mode(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_pwm_mode mode[]);

/*
    Name:   hil_set_pwm_configuration

    Description:

    Sets the configuration of the PWM output channels. Most cards do not support different
    configurations for their PWM channels but the Quanser QPID does. A PWM output configuration
    consists of a number of parameters:

        - whether each PWM channel is an independent unipolar output, a bipolar output,
          or whether the outputs are paired to make complementary outputs.
        - whether the PWM signals are edge-aligned or center-aligned
        - the polarity of the output (whether the duty cycle refers to the high pulse or low pulse width)

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    pwm_channels    = an array of unsigned integers (t_uint32) containing the PWM output
                      channels whose counter values will be set. Channel numbers are zero-based. 
                      Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the pwm_channels array
    configurations  = an array of t_pwm_configuration values containing the PWM configuration for
                      each channel. There must be one element for each PWM channel 
                      specified in the pwm_channels array. Valid values are:
                          PWM_UNIPOLAR_CONFIGURATION      - the output is a single unipolar output (default)
                          PWM_BIPOLAR_CONFIGURATION       - the output is a single bipolar output
                          PWM_PAIRED_CONFIGURATION        - the output is paired with another output of like polarity,
                                                            with programmable deadband
                          PWM_COMPLEMENTARY_CONFIGURATION - like paired but the secondary output is
                                                            inverted
                      Which outputs may be complementary pairs and which outputs may be bipolar is
                      determined by the card. The QPID, for example, implemented bipolar PWM outputs
                      through the corresponding analog outputs rather than using the normal PWM signal
                      lines.
    alignments      = the alignment of the pulse within the PWM period. Valid alignments are:
                          PWM_LEADING_EDGE_ALIGNED   - the pulse starts at the beginning of the PWM period, independent
                                                       of the pulse width (default)
                          PWM_TRAILING_EDGE_ALIGNED  - the pulse finishes at the end of the PWM period, independent
                                                       of the pulse width
                          PWM_CENTER_ALIGNED         - the pulse is centered within the PWM period
    polarities      = the polarity of the output. Valid values are:
                          PWM_ACTIVE_HIGH_POLARITY  - normal polarity. The duty cycle value determines the width of the high pulse (default).
                          PWM_ACTIVE_LOW_POLARITY - inverse polarity. The duty cycle value determines the width of the low pulse.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[] = { 0, 1, 2 };
    t_pwm_configuration configurations[] = { PWM_UNIPOLAR_CONFIGURATION, PWM_BIPOLAR_CONFIGURATION, PWM_COMPLEMENTARY_CONFIGURATION };
    t_pwm_alignment     alignments[]     = { PWM_CENTER_ALIGNED, PWM_EDGE_ALIGNED, PWM_CENTER_ALIGNED };
    t_pwm_polarity      polarities[]     = { PWM_ACTIVE_HIGH_POLARITY, PWM_ACTIVE_LOW_POLARITY, PWM_ACTIVE_HIGH_POLARITY };
    t_error  result;

    // Set the configuration of PWM channel 0 to be an independent output that is center-aligned with normal polarity.
    // Set the configuration of PWM channel 1 to be an independent bipolar output that is edge-aligned with inverse polarity.
    // Set the configuration of PWM channel 2 to be a complementary output that is center-aligned with normal polarity. For the QPID
    // this setting will also determine the configuration of PWM channel 3 since it is paired with channel 2 as a complementary output.
    result = hil_set_pwm_configuration(card, channels, 3, configurations, alignments, polarities);
*/
EXTERN t_error
hil_set_pwm_configuration(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_pwm_configuration configurations[],
                          const t_pwm_alignment alignments[], const t_pwm_polarity polarities[]);

/*
    Name:   hil_set_pwm_deadband

    Description:

    Sets the deadband of complementary PWM output channels. When two PWM outputs are configured as complementary
    by the hil_set_pwm_configuration function, the secondary channel outputs the inverse of the primary channel.
    Hence, when the primary channel is high, the secondary channel is low, and vice versa. However, a "deadband"
    may be introduced in the transition from high-to-low or low-to-high, such that the secondary output does not
    change immediately, as soon as the primary channel changes state. Such "deadband" is necessary when the PWM
    outputs are being used to drive an H-bridge or other transistor configurations to avoid two transistors in an
    H-bridge from being turned on at the same time, albeit briefly, and causing a current surge (since power would
    essentially be shorted to ground for a brief instant).

    This function allows the deadband to be specified. In fact, a different deadband may be specified for when
    the primary channel transitions from high-to-low or low-to-high, since transistor switching times may not be
    symmetric.

    The deadband may be set for any channels that are configured as bipolar, paired or complementary. Channels
    which are configured as unipolar are ignored (i.e., hil_set_pwm_deadband may be called for those channels
    but the deadband value is ignored and success is returned). Only the primary channel should have its deadband
    set. The secondary channel is ignored since its behaviour is governed entirely by the primary channel.

    Parameters:

    card                    = a t_card variable containing the handle to the card. It must be obtained
                              using the hil_open function.
    pwm_channels            = an array of unsigned integers (t_uint32) containing the PWM output
                              channels whose counter values will be set. Channel numbers are zero-based. 
                              Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels            = the number of channels in the pwm_channels array
    leading_edge_deadband   = an array of doubles indicating the deadband, in seconds, to use when
                              the primary channel switches from low to high.
    trailing_edge_deadband  = an array of doubles indicating the deadband, in seconds, to use when
                              the primary channel switches from high to low.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]      = { 0, 1, 2 };
    t_double leading_edge[]  = { 50e-9, 0, 100e-9 };
    t_double trailing_edge[] = { 100e-9, 0, 200e-9 };
    t_error  result;

    // Set PWM channel 0 to have a 100ns high-to-low deadband and a 50ns low-to-high deadband.
    // Set PWM channel 1 to have no deadband
    // Set PWM channel 2 to have a 200ns high-to-low deadband and a 100ns low-to-high deadband.
    result = hil_set_pwm_deadband(card, channels, 3, leading_edge, trailing_edge);
*/
EXTERN t_error
hil_set_pwm_deadband(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double leading_edge_deadband[], const t_double trailing_edge_deadband[]);

/*
    Name:   hil_set_pwm_frequency

    Description:

    Sets the frequency of the PWM channels. Many cards do not support PWM channels.
    Those that do may have a fixed PWM output frequency that cannot be varied. However,
    some cards, like the Quanser Q8-series, do allow the PWM output frequency to be
    configured. In fact, the frequency of each PWM output may be set individually.
    
    The range of valid PWM frequencies depends upon the card. See the card-specific
    documentation for details. PWM frequencies will be rounded to the nearest frequency
    supported by the card.

    This function should be used to configure the frequency of the PWM outputs when
    those channels are in duty cycle mode (see hil_set_pwm_mode). It is designed for
    configuring the PWM outputs, not updating their frequency every sampling instant.
    Use functions such as hil_write_pwm, hil_write_pwm_buffer or hil_task_write_pwm to 
    set the PWM output frequency for channels in frequency mode, where the frequency
    is varied continually.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    pwm_channels    = an array of unsigned integers (t_uint32) containing the PWM output
                      channels whose frequencies will be set. Channel numbers are zero-based. 
                      Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the pwm_channels array
    frequency       = an array of doubles containing the new PWM frequencies in Hz for
                      each channel. There must be one element for each PWM channel 
                      specified in the pwm_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]  = { 0, 1, 2 };
    t_int32  frequency[] = { 16276, 65104, 16276 };
    t_error  result;

    // Set the frequencies of PWM channels 0 and 2 to 16.276kHz (10-bit resolution)
    // the frequency of channel 1 to 65.104kHz (8-bit resolution).
    result = hil_set_pwm_frequency(card, channels, 3, frequency);
*/
EXTERN t_error
hil_set_pwm_frequency(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double frequency[]);

/*
    Name:   hil_set_pwm_duty_cycle

    Description:

    Sets the duty cycle of the PWM channels. This function should be used to configure
    the duty cycle of the PWM outputs when those channels are in frequency or period mode
    (see hil_set_pwm_mode), not duty cycle mode. It is designed for configuring the PWM 
    outputs, not updating  their duty cycle every sampling instant. Use functions such as 
    hil_write_pwm, hil_write_pwm_buffer or hil_task_write_pwm to set the PWM output duty 
    cycle for channels in duty cycle mode, where the duty cycle is varied continually.

    Since duty cycle mode is the default mode, and by far the most common, this function
    is generally never used. Most cards do not even support this function, although the
    Quanser Q8-series do. Instead, the hil_set_pwm_frequency function is used to
    configure the PWM output frequency during setup and then the hil_write_pwm,
    hil_write_pwm_buffer or hil_task_write_pwm function is used to change the PWM
    duty cycle during normal operation.

    Valid duty cycles range from 0 to 1, where 0 indicates a 0% duty cycle and 1 indicates
    a 100% duty cycle.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    pwm_channels    = an array of unsigned integers (t_uint32) containing the PWM output
                      channels whose duty cycles will be set. Channel numbers are zero-based. 
                      Thus, channel 0 is the first channel, channel 1 the second channel, etc.
    num_channels    = the number of channels in the pwm_channels array
    frequency       = an array of doubles containing the new PWM duty cycles for
                      each channel. There must be one element for each PWM channel 
                      specified in the pwm_channels array.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    t_uint32 channels[]   = { 0, 1, 2 };
    t_int32  duty_cycle[] = { 0.5, 0.75, 0.5};
    t_error  result;

    // Set the duty cycles of PWM channels 0 and 2 to 50% and the
    // the duty cycle of channel 1 to 75%.
    result = hil_set_pwm_duty_cycle(card, channels, 3, duty_cycle);
*/
EXTERN t_error
hil_set_pwm_duty_cycle(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double duty_cycle[]);

/*
    Name:   hil_set_card_specific_options

    Description:

    Sets options specific to a particular card. The options parameter is a string
    containing the card-specific options. The string typically takes the form:

        <name>=<value>,<name>=<value>,...

    where <name> is the name of an option and <value> is the option's value.
    In general, spaces should be avoided. Spaces may be contained in values
    if the value is enclosed in double quotes. For example, in the hypothetical
    options string below, the value of the vendor option contains a space so
    it is enclosed in quotes. 

        char options[] = "vendor=\"National Instruments\",terminal_board=e_series";

    Refer to the card's documentation for details on the options supported by
    the card. Many cards do not support any options since the standard HIL API
    functions cover most, if not all, of their functionality.

    Parameters:

    card            = a t_card variable containing the handle to the card. It must be obtained
                      using the hil_open function.
    options         = a string containing the options. See the standard format of this
                      argument in the discussion above. The string should be null terminated
                      although the options_size argument may be used to circumvent this
                      requirement by providing the actual length of the string.
    options_size    = the maximum number of characters that will be used from the
                      options string. If the options string is null-terminated then
                      this argument may be set to MAX_STRING_LENGTH.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    // Configure a National Instruments PCI-6259 card for use with a Quanser E-Series
    // terminal board.
    result = hil_set_card_specific_options(card, "terminal_board=e_series", MAX_STRING_LENGTH);
*/
EXTERN t_error
hil_set_card_specific_options(t_card card, const char * options, size_t options_size);

EXTERN t_error
hil_set_card_specific_woptions(t_card card, const wchar_t * options, size_t options_size);

#if defined(_UNICODE)
#define hil_set_card_specific_toptions  hil_set_card_specific_woptions
#else
#define hil_set_card_specific_toptions  hil_set_card_specific_options
#endif

/*-------------------------- Properties ------------------------------------*/

EXTERN t_error
hil_get_integer_property(t_card card, const t_hil_integer_property properties[], t_uint num_properties, t_int32 buffer[]);

EXTERN t_error
hil_get_double_property(t_card card, const t_hil_double_property properties[], t_uint num_properties, t_double buffer[]);

EXTERN t_error
hil_get_string_property(t_card card, t_hil_string_property property_code, char * buffer, size_t buffer_size);

EXTERN t_error
hil_get_wstring_property(t_card card, t_hil_string_property property_code, wchar_t * buffer, size_t buffer_size);

EXTERN t_error
hil_set_integer_property(t_card card, const t_hil_integer_property properties[], t_uint num_properties, const t_int32 buffer[]);

EXTERN t_error
hil_set_double_property(t_card card, const t_hil_double_property properties[], t_uint num_properties, const t_double buffer[]);

EXTERN t_error
hil_set_string_property(t_card card, t_hil_string_property property_code, const char * buffer, size_t buffer_size);

EXTERN t_error
hil_set_wstring_property(t_card card, t_hil_string_property property_code, const wchar_t * buffer, size_t buffer_size);

#if defined(_UNICODE)
#define hil_get_tstring_property    hil_get_wstring_property
#define hil_set_tstring_property    hil_set_wstring_property
#else
#define hil_get_tstring_property    hil_get_string_property
#define hil_set_tstring_property    hil_set_string_property
#endif

/*-------------------------- Immediate operations --------------------------*/

EXTERN t_error
hil_read_analog(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, t_double  buffer[]);

EXTERN t_error
hil_read_encoder(t_card card, const t_uint32 encoder_channels[], t_uint32 num_channels, t_int32   buffer[]);

EXTERN t_error
hil_read_digital(t_card card, const t_uint32 digital_lines[], t_uint32 num_lines,    t_boolean buffer[]);

EXTERN t_error
hil_read_other(t_card card, const t_uint32 other_channels[], t_uint32 num_channels, t_double  buffer[]);

EXTERN t_error
hil_read_analog_codes(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, t_int32 buffer[]);

EXTERN t_error
hil_read(t_card card, 
         const t_uint32 analog_channels[],  t_uint32 num_analog_channels, 
         const t_uint32 encoder_channels[], t_uint32 num_encoder_channels, 
         const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
         const t_uint32 other_channels[],   t_uint32 num_other_channels, 
         t_double  analog_buffer[],
         t_int32   encoder_buffer[],
         t_boolean digital_buffer[],
         t_double  other_buffer[]);

EXTERN t_error
hil_write_analog(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, const t_double  buffer[]);

EXTERN t_error
hil_write_pwm(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double  buffer[]);

EXTERN t_error
hil_write_digital(t_card card, const t_uint32 digital_lines[], t_uint32 num_lines, const t_boolean buffer[]);

EXTERN t_error
hil_write_other(t_card card, const t_uint32 other_channels[], t_uint32 num_channels, const t_double  buffer[]);

EXTERN t_error
hil_write_analog_codes(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, const t_int32 buffer[]);

EXTERN t_error
hil_write(t_card card, 
          const t_uint32 analog_channels[],  t_uint32 num_analog_channels, 
          const t_uint32 pwm_channels[],     t_uint32 num_pwm_channels, 
          const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
          const t_uint32 other_channels[],   t_uint32 num_other_channels, 
          const t_double  analog_buffer[],
          const t_double  pwm_buffer[],
          const t_boolean digital_buffer[],
          const t_double  other_buffer[]);

EXTERN t_error
hil_read_analog_write_analog(t_card card, 
                             const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
                             const t_uint32 analog_output_channels[], t_uint32 num_analog_output_channels, 
                             t_double       analog_input_buffer[],
                             const t_double analog_output_buffer[]);

EXTERN t_error
hil_read_encoder_write_pwm(t_card card, 
                           const t_uint32 encoder_input_channels[],  t_uint32 num_encoder_input_channels, 
                           const t_uint32 pwm_output_channels[], t_uint32 num_pwm_output_channels, 
                           t_int32        encoder_input_buffer[],
                           const t_double pwm_output_buffer[]);

EXTERN t_error
hil_read_digital_write_digital(t_card card, 
                               const t_uint32  digital_input_lines[],    t_uint32 num_digital_input_lines, 
                               const t_uint32  digital_output_lines[],   t_uint32 num_digital_output_lines, 
                               t_boolean       digital_input_buffer[],
                               const t_boolean digital_output_buffer[]);

EXTERN t_error
hil_read_other_write_other(t_card card, 
                           const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 
                           const t_uint32 other_output_channels[],  t_uint32 num_other_output_channels, 
                           t_double       other_input_buffer[],
                           const t_double other_output_buffer[]);

EXTERN t_error
hil_read_write(t_card card,
               const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
               const t_uint32 encoder_input_channels[], t_uint32 num_encoder_input_channels, 
               const t_uint32 digital_input_lines[],    t_uint32 num_digital_input_lines, 
               const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 

               const t_uint32 analog_output_channels[],  t_uint32 num_analog_output_channels, 
               const t_uint32 pwm_output_channels[],     t_uint32 num_pwm_output_channels, 
               const t_uint32 digital_output_lines[],    t_uint32 num_digital_output_lines, 
               const t_uint32 other_output_channels[],   t_uint32 num_other_output_channels, 

               t_double  analog_input_buffer[],
               t_int32   encoder_input_buffer[],
               t_boolean digital_input_buffer[],
               t_double  other_input_buffer[],

               const t_double  analog_output_buffer[],
               const t_double  pwm_output_buffer[],
               const t_boolean digital_output_buffer[],
               const t_double  other_output_buffer[]);

/*-------------------------- Buffered operations ---------------------------*/

EXTERN t_error
hil_read_analog_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                       const t_uint32 analog_channels[], t_uint32 num_channels, t_double buffer[]);

EXTERN t_error
hil_read_encoder_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                        const t_uint32 encoder_channels[], t_uint32 num_channels, t_int32 buffer[]);

EXTERN t_error
hil_read_digital_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                        const t_uint32 digital_lines[], t_uint32 num_lines, t_boolean buffer[]);

EXTERN t_error
hil_read_other_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                      const t_uint32 other_channels[], t_uint32 num_channels, t_double buffer[]);

EXTERN t_error
hil_read_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                const t_uint32 analog_channels[],  t_uint32 num_analog_channels, 
                const t_uint32 encoder_channels[], t_uint32 num_encoder_channels, 
                const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
                const t_uint32 other_channels[],   t_uint32 num_other_channels, 
                t_double  analog_buffer[],
                t_int32   encoder_buffer[],
                t_boolean digital_buffer[],
                t_double  other_buffer[]);

EXTERN t_error
hil_write_analog_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                        const t_uint32 analog_channels[], t_uint32 num_channels, const t_double  buffer[]);

EXTERN t_error
hil_write_pwm_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                     const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double buffer[]);

EXTERN t_error
hil_write_digital_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                         const t_uint32 digital_lines[], t_uint32 num_lines, const t_boolean buffer[]);

EXTERN t_error
hil_write_other_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                       const t_uint32 other_channels[], t_uint32 num_channels, const t_double buffer[]);

EXTERN t_error
hil_write_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                 const t_uint32 analog_channels[],  t_uint32 num_analog_channels, 
                 const t_uint32 pwm_channels[],     t_uint32 num_pwm_channels, 
                 const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
                 const t_uint32 other_channels[],   t_uint32 num_other_channels, 
                 const t_double  analog_buffer[],
                 const t_double  pwm_buffer[],
                 const t_boolean digital_buffer[],
                 const t_double  other_buffer[]);

EXTERN t_error
hil_read_analog_write_analog_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                                    const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
                                    const t_uint32 analog_output_channels[], t_uint32 num_analog_output_channels, 
                                    t_double       analog_input_buffer[],
                                    const t_double analog_output_buffer[]);

EXTERN t_error
hil_read_encoder_write_pwm_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                                  const t_uint32 encoder_input_channels[],  t_uint32 num_encoder_input_channels, 
                                  const t_uint32 pwm_output_channels[],     t_uint32 num_pwm_output_channels, 
                                  t_int32        encoder_input_buffer[],
                                  const t_double pwm_output_buffer[]);

EXTERN t_error
hil_read_digital_write_digital_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                                      const t_uint32  digital_input_lines[],    t_uint32 num_digital_input_lines, 
                                      const t_uint32  digital_output_lines[],   t_uint32 num_digital_output_lines, 
                                      t_boolean       digital_input_buffer[],
                                      const t_boolean digital_output_buffer[]);

EXTERN t_error
hil_read_other_write_other_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                                  const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 
                                  const t_uint32 other_output_channels[],  t_uint32 num_other_output_channels, 
                                  t_double       other_input_buffer[],
                                  const t_double other_output_buffer[]);

EXTERN t_error
hil_read_write_buffer(t_card card, t_clock clock, t_double frequency, t_uint32 num_samples,
                      const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
                      const t_uint32 encoder_input_channels[], t_uint32 num_encoder_input_channels, 
                      const t_uint32 digital_input_lines[],    t_uint32 num_digital_input_lines, 
                      const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 

                      const t_uint32 analog_output_channels[],  t_uint32 num_analog_output_channels, 
                      const t_uint32 pwm_output_channels[],     t_uint32 num_pwm_output_channels, 
                      const t_uint32 digital_output_lines[],    t_uint32 num_digital_output_lines, 
                      const t_uint32 other_output_channels[],   t_uint32 num_other_output_channels, 

                      t_double  analog_input_buffer[],
                      t_int32   encoder_input_buffer[],
                      t_boolean digital_input_buffer[],
                      t_double  other_input_buffer[],

                      const t_double  analog_output_buffer[],
                      const t_double  pwm_output_buffer[],
                      const t_boolean digital_output_buffer[],
                      const t_double  other_output_buffer[]);

/*-------------------------- Asynchronous operations -----------------------*/

EXTERN t_error
hil_task_create_analog_reader(t_card card, t_uint32 samples_in_buffer, 
                              const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                              t_task *task);

EXTERN t_error
hil_task_create_encoder_reader(t_card card, t_uint32 samples_in_buffer,
                               const t_uint32 encoder_channels[], t_uint32 num_encoder_channels,
                               t_task *task);

EXTERN t_error
hil_task_create_digital_reader(t_card card, t_uint32 samples_in_buffer,
                               const t_uint32 digital_lines[],    t_uint32 num_digital_lines,
                               t_task *task);

EXTERN t_error
hil_task_create_other_reader(t_card card, t_uint32 samples_in_buffer, 
                             const t_uint32 other_channels[],  t_uint32 num_other_channels,
                             t_task *task);

EXTERN t_error
hil_task_create_reader(t_card card, t_uint32 samples_in_buffer, 
                       const t_uint32 analog_channels[],  t_uint32 num_analog_channels,
                       const t_uint32 encoder_channels[], t_uint32 num_encoder_channels,
                       const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
                       const t_uint32 other_channels[],   t_uint32 num_other_channels,
                       t_task *task);

EXTERN t_error
hil_task_create_analog_writer(t_card card, t_uint32 samples_in_buffer, 
                              const t_uint32 analog_channels[], t_uint32 num_analog_channels,
                              t_task *task);

EXTERN t_error
hil_task_create_pwm_writer(t_card card, t_uint32 samples_in_buffer, 
                           const t_uint32 pwm_channels[], t_uint32 num_pwm_channels, 
                           t_task *task);

EXTERN t_error
hil_task_create_digital_writer(t_card card, t_uint32 samples_in_buffer, 
                               const t_uint32 digital_lines[], t_uint32 num_digital_lines, 
                               t_task *task);

EXTERN t_error
hil_task_create_other_writer(t_card card, t_uint32 samples_in_buffer, 
                             const t_uint32 other_channels[], t_uint32 num_other_channels,
                             t_task *task);

EXTERN t_error
hil_task_create_writer(t_card card, t_uint32 samples_in_buffer, 
                       const t_uint32 analog_channels[],  t_uint32 num_analog_channels,
                       const t_uint32 pwm_channels[],     t_uint32 num_pwm_channels,
                       const t_uint32 digital_lines[],    t_uint32 num_digital_lines, 
                       const t_uint32 other_channels[],   t_uint32 num_other_channels,
                       t_task *task);

EXTERN t_error
hil_task_create_analog_reader_analog_writer(t_card card, t_uint32 samples_in_buffer,
                       const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
                       const t_uint32 analog_output_channels[], t_uint32 num_analog_output_channels, 
                       t_task *task);

EXTERN t_error
hil_task_create_encoder_reader_pwm_writer(t_card card, t_uint32 samples_in_buffer,
                       const t_uint32 encoder_input_channels[],  t_uint32 num_encoder_input_channels, 
                       const t_uint32 pwm_output_channels[], t_uint32 num_pwm_output_channels, 
                       t_task *task);

EXTERN t_error
hil_task_create_digital_reader_digital_writer(t_card card, t_uint32 samples_in_buffer,
                       const t_uint32 digital_input_lines[],    t_uint32 num_digital_input_lines, 
                       const t_uint32 digital_output_lines[],   t_uint32 num_digital_output_lines, 
                       t_task *task);

EXTERN t_error
hil_task_create_other_reader_other_writer(t_card card, t_uint32 samples_in_buffer,
                       const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 
                       const t_uint32 other_output_channels[],  t_uint32 num_other_output_channels, 
                       t_task *task);

EXTERN t_error
hil_task_create_reader_writer(t_card card, t_uint32 samples_in_buffer,
                       const t_uint32 analog_input_channels[],  t_uint32 num_analog_input_channels, 
                       const t_uint32 encoder_input_channels[], t_uint32 num_encoder_input_channels, 
                       const t_uint32 digital_input_lines[],    t_uint32 num_digital_input_lines, 
                       const t_uint32 other_input_channels[],   t_uint32 num_other_input_channels, 

                       const t_uint32 analog_output_channels[],  t_uint32 num_analog_output_channels, 
                       const t_uint32 pwm_output_channels[],     t_uint32 num_pwm_output_channels, 
                       const t_uint32 digital_output_lines[],    t_uint32 num_digital_output_lines, 
                       const t_uint32 other_output_channels[],   t_uint32 num_other_output_channels, 
                       t_task *task);

/*
    Name:   hil_task_set_buffer_overflow_mode

    Description:

    Determines how buffer overflows are handled for a task. The task buffer overflows when samples
    are not being read fast enough by task_read_xxx to keep up with the data being read by the card
    at its inputs, or when samples are not being written fast enough by task_write_xxx to stay ahead
    of the data being written by the card to its outputs. Buffering is used to handle cases where
    the application is momentarily interrupted and the size of the buffer determines how long an
    interruption is permitted. If increasing the buffer size does not prevent buffer overflow then
    the application is simply not capable of keeping up with real time.
    
    By default, an error will be returned by the next hil_task_read_xxx or hil_task_write_xxx call
    when a buffer overflow occurs and the task will need to be stopped. The reason this is the default
    behaviour is that the HIL API is intended for real-time applications where missing samples is
    regarded as a fatal error.

    However, for those applications where samples may be missed then the buffer overflow handling
    can be altered using the hil_task_set_buffer_overflow_mode function (if the card supports it).
    There are three possible modes:

    BUFFER_MODE_ERROR_ON_OVERFLOW:

    This is the default mode in which buffer overflows cause a QERR_BUFFER_OVERFLOW error to be
    returned by the next hil_tas_read_xxx or hil_task_write_xxx. The task should be stopped at
    that point.

    BUFFER_MODE_OVERWRITE_ON_OVERFLOW:

    In this mode, old samples in the buffer are discarded to make room for new samples if the
    buffer overflows. For writer tasks, this means that there may be unexpected discontinuities in
    the output waveforms. For reader tasks, it means that samples may be lost and only the more
    recent samples will be read.

    BUFFER_MODE_DISCARD_ON_OVERFLOW:

    In this mode, new samples are discarded if there is no room in the buffer. For writer tasks,
    this means that there may be unexpected discontinuities in the output waveforms. For reader
    tasks, it means that samples may be lost and only the oldest samples will be read.

    BUFFER_MODE_WAIT_ON_OVERFLOW
    
    In this mode, the task waits on buffer overflow for space to become available. This mode is
    not supported by hardware cards but is only for use by simulated cards.

    BUFFER_MODE_SYNCHRONIZE
    
    In this mode, the task provides complete buffer synchronization. This mode is not supported
    by hardware cards but is only for use by simulated cards.

    Parameters:

    task     = a t_task variable containing the handle to the task. It must be obtained
               using one of the hil_task_create_xxx functions.
    mode     = the new buffer overflow mode.

    Return value:

    Returns 0 on success. If an error occurs then a negative error code is returned.

    Examples:

    result = hil_task_set_buffer_overflow_mode(task, BUFFER_MODE_OVERWRITE_ON_OVERFLOW);
*/
EXTERN t_error
hil_task_set_buffer_overflow_mode(t_task task, t_buffer_overflow_mode mode);

/*
    Name:   hil_task_get_buffer_overflows

    Description:

    Returns the number of buffer overflows that have occurred since the task was started. This
    function is only relevant when the buffer overflow mode has been changed from the default mode
    i.e., when the overflow mode is not BUFFER_MODE_ERROR_ON_OVERFLOW.
    
    Parameters:

    task     = a t_task variable containing the handle to the task. It must be obtained
               using one of the hil_task_create_xxx functions.

    Return value:

    Returns the number of buffer overflows. If an error occurs then a negative error code is returned.

    Examples:

    num_overflows = hil_task_get_buffer_overflows(task);
*/
EXTERN t_int
hil_task_get_buffer_overflows(t_task task);

EXTERN t_error
hil_task_get_card(t_task task, t_card *card);

EXTERN t_error
hil_task_get_num_channels(t_task task,
                          t_uint32 *num_analog_input_channels,
                          t_uint32 *num_encoder_input_channels,
                          t_uint32 *num_digital_input_lines,
                          t_uint32 *num_other_input_channels,
                          
                          t_uint32 *num_analog_output_channels,
                          t_uint32 *num_pwm_output_channels,
                          t_uint32 *num_digital_output_lines,
                          t_uint32 *num_other_output_channels);

EXTERN t_error
hil_task_start(t_task task, t_clock clock, t_double frequency, t_uint32 num_samples);

EXTERN t_error
hil_task_read_analog(t_task task, t_uint32 num_samples, t_double analog_buffer[]);

EXTERN t_error
hil_task_read_encoder(t_task task, t_uint32 num_samples, t_int32 encoder_buffer[]);

EXTERN t_error
hil_task_read_digital(t_task task, t_uint32 num_samples, t_boolean digital_buffer[]);

EXTERN t_error
hil_task_read_other(t_task task, t_uint32 num_samples, t_double  other_buffer[]);

EXTERN t_error
hil_task_read(t_task task, t_uint32 num_samples,
              t_double  analog_buffer[],
              t_int32   encoder_buffer[],
              t_boolean digital_buffer[],
              t_double  other_buffer[]);

EXTERN t_error
hil_task_write_analog(t_task task, t_uint32 num_samples, const t_double analog_buffer[]);

EXTERN t_error
hil_task_write_pwm(t_task task, t_uint32 num_samples, const t_double pwm_buffer[]);

EXTERN t_error
hil_task_write_digital(t_task task, t_uint32 num_samples, const t_boolean digital_buffer[]);

EXTERN t_error
hil_task_write_other(t_task task, t_uint32 num_samples, const t_double other_buffer[]);

EXTERN t_error
hil_task_write(t_task task, t_uint32 num_samples,
               const t_double  analog_buffer[],
               const t_double  pwm_buffer[],
               const t_boolean digital_buffer[],
               const t_double  other_buffer[]);

EXTERN t_error
hil_task_read_analog_write_analog(t_task task, t_uint32 num_samples,
                                  t_double  analog_input_buffer[],
                                  const t_double  analog_output_buffer[]);

EXTERN t_error
hil_task_read_encoder_write_pwm(t_task task, t_uint32 num_samples,
                                t_int32  encoder_input_buffer[],
                                const t_double pwm_output_buffer[]);

EXTERN t_error
hil_task_read_digital_write_digital(t_task task, t_uint32 num_samples,
                                t_boolean digital_input_buffer[],
                                const t_boolean digital_output_buffer[]);

EXTERN t_error
hil_task_read_other_write_other(t_task task, t_uint32 num_samples,
                                t_double  other_input_buffer[],
                                const t_double  other_output_buffer[]);

EXTERN t_error
hil_task_read_write(t_task task, t_uint32 num_samples,
                    t_double  analog_input_buffer[],
                    t_int32   encoder_input_buffer[],
                    t_boolean digital_input_buffer[],
                    t_double  other_input_buffer[],

                    const t_double  analog_output_buffer[],
                    const t_double  pwm_output_buffer[],
                    const t_boolean digital_output_buffer[],
                    const t_double  other_output_buffer[]);

EXTERN t_error
hil_task_flush(t_task task);

EXTERN t_error
hil_task_stop(t_task task);

EXTERN t_error
hil_task_delete(t_task task);

EXTERN t_error
hil_task_stop_all(t_card card);

EXTERN t_error
hil_task_delete_all(t_card card);

EXTERN t_boolean
hil_task_is_valid(t_task task);

/*-------------------------- Watchdog operations ---------------------------*/

/*
    Description:

    This function sets the state that the analog outputs will be set to
    if the watchdog expires. Most cards do not allow this state to be
    configured. The Q8-series cards may be configured to reset the analog
    outputs to 0V. In this case, the digital outputs must also be
    configured to go tristate. If no expiration states are configured for
    the Q8-series, then the analog and digital outputs will not be reconfigured
    when the watchdog expires.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the analog channels for which the expiration state should be set
    num_channels = the number of analog channels in the channels and voltages vectors
    voltages     = the analog voltages to which to set the analog outputs upon expiration

    Return values:

    Returns 0 upon success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_set_analog_expiration_state(t_card card, const t_uint channels[], t_uint num_channels, const t_double voltages[]);

/*
    Description:

    This function sets the state that the PWM outputs will be set to
    if the watchdog expires. Currently there are no cards which allow
    this state to be configured.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the PWM channels for which the expiration state should be set
    num_channels = the number of PWM channels in the channels and voltages vectors
    duty_cycles  = the PWM duty cycles to which to set the PWM outputs upon expiration (affected by the PWM mode)

    Return values:

    Returns 0 upon success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_set_pwm_expiration_state(t_card card, const t_uint channels[], t_uint num_channels, const t_double duty_cycles[]);

/*
    Description:

    This function sets the state that the digital outputs will be set to
    if the watchdog expires. Most cards do not allow this state to be
    configured. The Q8-series cards may be configured to reset the digital
    outputs to tri-state. In this case, the analog outputs must also be
    configured to go 0V. If no expiration states are configured for
    the Q8-series, then the analog and digital outputs will not be reconfigured
    when the watchdog expires.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the digital channels for which the expiration state should be set
    num_channels = the number of digital channels in the channels and states vectors
    states       = the digital states to which to configure the digital outputs upon expiration

    Return values:

    Returns 0 upon success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_set_digital_expiration_state(t_card card, const t_uint channels[], t_uint num_channels, const t_digital_state states[]);

/*
    Description:

    This function sets the state that the other outputs will be set to
    if the watchdog expires. Currently there are no cards which allow
    this state to be configured.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the other channels for which the expiration state should be set
    num_channels = the number of other channels in the channels and voltages vectors
    values       = the values to which to set the other outputs upon expiration

    Return values:

    Returns 0 upon success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_set_other_expiration_state(t_card card, const t_uint channels[], t_uint num_channels, const t_double values[]);

/*
    Description:

    This function starts the watchdog timer with the given timeout interval.
    It should only be called after the expiration states have been configured
    using the hil_watchdog_set_xxxx_expiration_state functions. Once the watchdog
    timer has been started, it must be reloaded each time before it expires using 
    the hil_watchdog_reload function.

    Parameters:

    card    = a card opened using the hil_open function
    timeout = the expiration timeout interval in seconds

    Return values:

    Returns 0 upon success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_start(t_card card, t_double timeout);

/*
    Description:

    This function reloads the watchdog timer. It is typically called to reload
    the watchdog timer before it expires at the top of the control loop.

    Parameters:

    card = a card opened using the hil_open function

    Return values:

    Returns 1 if the watchdog timer was reloaded prior to expiration. Returns 0 if
    the watchdog timer had expired before being reloaded. Otherwise it returns a negative 
    error code.
*/
EXTERN t_error
hil_watchdog_reload(t_card card);

/*
    Description:

    Indicates whether the watchdog has expired.

    Parameters:

    card = a card opened using the hil_open function

    Return values:

    Returns true (1) if the watchdog has expired. Otherwise it returns false (0). If an error
    occurs then a negative error code is returned.
*/
EXTERN t_error
hil_watchdog_is_expired(t_card card);

/*
    Description:

    When the watchdog timer expires, it prevents further access to the hardware after
    setting the outputs to the configured expiration states. In order to clear this
    "protected" state and allow access to the hardware again, the hil_watchdog_clear
    function must be called. This function restores the hardware to its state prior
    to the watchdog timer expiring, if possible. For example, for the Q8-series cards
    it reprograms the digital directions and analog modes to their original values since
    these are reset by the watchdog expiration (if the analog and digital output
    expiration states have been configured).

    Parameters:

    card = a card opened using the hil_open function

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_clear(t_card card);

/*
    Description:

    This function stops the watchdog timer. The watchdog timer will no longer expire
    so the hil_watchdog_reload function need no longer be called.  Stopping the watchdog
    timer does not clear the watchdog state if the watchdog has already expired. Use the
    hil_watchdog_clear function for this purpose.

    Parameters:

    card = a card opened using the hil_open function

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_watchdog_stop(t_card card);

/*-------------------------- Interrupt handling ----------------------------*/

/*
    Description:

    This function polls the interrupt sources of the card and returns their current state.
    Each element of the state vector is one of two values:
        false = no interrupt has occurred for that channel
        true  = an interrupt did occur for that channel

    Note that the channel numbers for interrupt sources are assigned according to a standardized
    list, much like the "other" channels. Also, this function does not block.

    If an interrupt is detected, that interrupt is acknowledged so that the hil_poll_interrupt
    function only sets the state to true once for each interrupt that occurs. The next invocation
    of hil_poll_interrupt will have the state set to false unless another interrupt has occurred
    between the two calls to hil_poll_interrupt.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the interrupt sources to poll
    num_channels = the number of interrupt sources in the channels and states vectors
    states       = the status of each interrupt source. This array must be at least num_channels
                   elements in length.

    Return values:

    Returns the number of interrupt sources which occurred on success. Otherwise it returns a 
    negative error code.
*/
EXTERN t_int
hil_poll_interrupt(t_card card, const t_uint channels[], t_uint num_channels, t_boolean states[]);

/*
    Description:

    This function creates a "monitor" to watch the status of interrupt sources. Monitors are like
    tasks except they are not periodic. After creating a monitor, start the monitor using the
    hil_monitor_start function. Then wait for an interrupt to occur using the hil_monitor_read_interrupt
    function, which does not return until one of the interrupt events occurs or the hil_monitor_stop
    function is called. Delete the monitor using the hil_monitor_delete function.

    Note that the channel numbers for interrupt sources are assigned according to a standardized
    list, much like the "other" channels.

    Parameters:

    card         = a card opened using the hil_open function
    channels     = the interrupt sources to acknowledge
    num_channels = the number of interrupt sources in the channels vector
    monitor      = a pointer to a t_monitor variable which will be assigned a monitor handle
                   that may be used with the other hil_monitor functions.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_monitor_create_interrupt_reader(t_card card, const t_uint channels[], t_uint num_channels, t_monitor * monitor);

/*
    Description:

    This function starts the monitor watching for events. A monitor must be started before polling
    for events. The monitor can be stopped by calling hil_monitor_stop. Calling hil_monitor_stop
    will interrupt any blocking calls to hil_monitor_poll_interrupt.

    Parameters:

    monitor = a monitor created using one of the hil_monitor_create_interrupt_reader function.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_monitor_start(t_monitor monitor);

/*
    Description:

    This function waits for one of the monitored events to occur. In this instance, it waits for
    an interrupt to occur. This function does not return until one of the monitored interrupts
    occurs or the hil_monitor_stop function is called from another thread. The status of all the
    monitored interrupt sources is returned in the states vector. More than one element will be
    set to true if more than one interrupt occurred at the same time. The states vector must be
    at least as large as the number of interrupt sources specified in the 
    hil_monitor_create_interrupt_reader function that created the monitor.

    Be sure to call hil_monitor_start to start the monitor initially before attempting to invoke 
    this function. Otherwise it may block indefinitely.

    Any interrupts that do occur are acknowledged so that the hil_monitor_read_interrupt function
    will only return once for each interrupt that occurs on a particular interrupt line. A second
    call to hil_monitor_read_interrupt will block until another interrupt occurs.

    Parameters:

    monitor      = a monitor created using one of the hil_monitor_create_interrupt_reader function.
    states       = the status of all the interrupt sources being watched by this monitor. The states
                   occur in the same order as the interrupt sources were specified in the
                   hil_monitor_create_interrupt_reader function.

    Return values:

    Returns the number of interrupt sources which occurred on success. If it returns zero then the
    blocking operation was interrupted by a call to hil_monitor_stop. Otherwise it returns a negative 
    error code.
*/
EXTERN t_int
hil_monitor_read_interrupt(t_monitor monitor, t_boolean states[]);

/*
    Description:

    This function stops the monitor from watching for events. Calling hil_monitor_stop will
    interrupt any blocking calls to hil_monitor_poll_interrupt.

    Note that the channel numbers for interrupt sources are assigned according to a standardized
    list, much like the "other" channels.

    Parameters:

    monitor = a monitor created using one of the hil_monitor_create_interrupt_reader function.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_monitor_stop(t_monitor monitor);

/*
    Description:

    This function deletes the monitor. A monitor may not be used after it has been deleted.

    Parameters:

    monitor = a monitor created using one of the hil_monitor_create_interrupt_reader function.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
hil_monitor_delete(t_monitor monitor);

EXTERN t_error
hil_monitor_stop_all(t_card card);

EXTERN t_error
hil_monitor_delete_all(t_card card);

EXTERN t_boolean
hil_monitor_is_valid(t_monitor monitor);

/*-------------------------- Termination handling --------------------------*/

EXTERN t_error
hil_set_analog_termination_state(t_card card, const t_uint32 analog_channels[], t_uint32 num_channels, const t_double buffer[]);

EXTERN t_error
hil_set_pwm_termination_state(t_card card, const t_uint32 pwm_channels[], t_uint32 num_channels, const t_double buffer[]);

EXTERN t_error
hil_set_digital_termination_state(t_card card, const t_uint32 digital_lines[], t_uint32 num_lines, const t_boolean buffer[]);

EXTERN t_error
hil_set_other_termination_state(t_card card, const t_uint32 other_channels[], t_uint32 num_channels, const t_double buffer[]);

EXTERN t_error
hil_write_termination_states(t_card card);

#endif
