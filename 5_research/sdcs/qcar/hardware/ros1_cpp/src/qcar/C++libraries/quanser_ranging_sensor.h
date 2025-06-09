#if !defined(_quanser_ranging_sensor_h)
#define _quanser_ranging_sensor_h

#include "quanser_errors.h"
#include "quanser_extern.h"

typedef struct tag_ranging_sensor * t_ranging_sensor;

typedef enum tag_ranging_sensor_type
{
    RANGING_SENSOR_TYPE_INVALID,        /* Invalid sensor type */
    RANGING_SENSOR_TYPE_VL53L1,         /* ST Microelectronics VL31L1 time-of-flight sensor */
    RANGING_SENSOR_TYPE_RPLIDAR,        /* Slamtec RPLidar 2D LIDAR sensor */

    NUMBER_OF_RANGING_SENSOR_TYPES = RANGING_SENSOR_TYPE_RPLIDAR
} t_ranging_sensor_type;

typedef enum tag_ranging_distance
{
    RANGING_DISTANCE_SHORT,
    RANGING_DISTANCE_MEDIUM,
    RANGING_DISTANCE_LONG,

    NUMBER_OF_RANGING_DISTANCES
} t_ranging_distance;

typedef enum tag_ranging_measurement_mode
{
    RANGING_MEASUREMENT_MODE_NORMAL,        /* return actual measurement data. Number of measurements will vary and angles will not be consistent between scans. Angles will start close to zero. */
    RANGING_MEASUREMENT_MODE_INTERPOLATED,  /* returns the number of measurements, N, requested. Angles will start at zero and be 360/N apart. Raw measurements will be interpolated to estimate distance at each angle */
    
    NUMBER_OF_RANGING_MEASUREMENT_MODES
} t_ranging_measurement_mode;

typedef struct tag_ranging_measurement
{
    t_double distance;          /* the distance in metres */
    t_double distance_sigma;    /* an estimate of the standard deviation in the current distance measurement */
    t_double heading;           /* the heading in radians (will be zero for 1D ranging sensors) */
    t_uint8 quality;            /* an indication of the quality of the measurement (0 to 100%) */
} t_ranging_measurement;

/* VL53L1X Time of Flight Ranging Sensor */

/*
** Description:
**      Opens the ranging sensor.
**
** Arguments:
**      uri                = a URI used for communicating with the device. The VL53L1X is an I2C-based sensor supporting a 400 kHz I2C interface.
**                           Hence, the URI should reference an I2C interface if using a real device.
**      range              = the distance mode to use.
**      timing_budget      = the time in seconds allowed for the sensor to perform a reading
**      measurement_period = the interval at which the device reads the sensor. It must be at least 4ms longer than the timing_budget parameter.
**      sensor             = the address of a t_ranging_sensor variable which will receive the handle to the sensor.
*/
EXTERN t_error
vl53l1x_open(const char * uri, t_ranging_distance range, t_double timing_budget, t_double measurement_period, t_ranging_sensor * sensor);

EXTERN t_int
vl53l1x_read(t_ranging_sensor sensor, t_ranging_measurement * measurement);

EXTERN t_error
vl53l1x_close(t_ranging_sensor sensor);

/* RPLIDAR 2D LIDAR Sensors */

EXTERN t_error
rplidar_open(const char * uri, t_ranging_distance range, t_ranging_sensor * sensor);

/*
** Description:
**      Reads LIDAR data from the ranging sensor.
**
**      When the measurement mode is RANGING_MEASUREMENT_MODE_NORMAL, the "raw" sensor readings from the LIDAR are returned 
**      (but the values are scaled to the SI units expected). In this case, the number of measurements may vary and the angles
**      may not be consistent between scans. Furthermore, while the angles will be in ascending order, the first angle may not
**      be zero. It will, however, be close to zero. If the size of the measurements buffer provided is not large enough then
**      -QERR_BUFFER_TOO_SMALL will be returned. In this case, the function may be called again with a larger buffer.
**
**      When the measurement mode is RANGING_MEASUREMENT_MODE_INTERPOLATED, the raw sensor readings from the LIDAR are not
**      returned. Instead, the number of "measurements" requested will be returned, in which the angles are 360/N degrees
**      apart (in radians), where N is the number of measurements requested and the first angle is zero. The distances will be
**      interpolated from the raw data, as will the standard deviation and quality. Interpolation is only performed between two
**      consecutive valid readings. The advantage of this mode is that the angles are always consistent, as are the number of
**      measurements, so the data is easier to process in Simulink.
**
**      If no new scan data is available then -QERR_WOULD_BLOCK is returned.
**
**      If the quality is zero then it indicates an invalid measurement (no reflected laser pulse).
**
** Arguments:
**      sensor                          = the t_ranging_sensor variable which contains the handle to the sensor (handle returned by rplidar_open).
**      mode                            = the measurement mode, which determines how the scan data is returned.
**      maximum_interpolated_distance   = in interpolation mode, this is the maximum difference between the distance measurement of contiguous samples
**                                        for which interpolation will be used. Beyond this difference, the distance of the sample with the closest
**                                        angle to the desired heading will be used.
**      measurements                    = a buffer in which the actual measurement data is stored.
**      num_measurements                = the size of the measurements buffer in elements.
**
** Return value:
**      Returns the number of measurements actually copied to the measurements buffer on success. Otherwise it returns a negative
**      error code. It returns -QERR_BUFFER_TOO_SMALL if the supplied measurements buffer is not large enough to hold the scan data.
**      If no new data is available then it returns -QERR_WOULD_BLOCK.
*/
EXTERN t_int
rplidar_read(t_ranging_sensor sensor, t_ranging_measurement_mode mode, t_double maximum_interpolated_distance, t_ranging_measurement * measurements, t_uint num_measurements);

EXTERN t_error
rplidar_close(t_ranging_sensor sensor);


#endif
