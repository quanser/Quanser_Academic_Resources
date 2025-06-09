#if !defined(_quanser_time_h)
#define _quanser_time_h

#include "quanser_extern.h"
#include "quanser_errors.h"

#define MAX_TIMEOUT     (9223372036854775807.999999999)

typedef struct tag_timeout
{
    t_long    seconds;
    t_int     nanoseconds;
    t_boolean is_absolute;
} t_timeout;

/*
    Description:

    This function converts a time in seconds (and possible
    fractional seconds) into a t_timeout structure. If the
    time exceeds the maximum representable time in a t_timeout
    structure (eg. time_value = infinity) then NULL is returned
    and the t_timeout structure is set to the maximum representable
    value. Otherwise a pointer to the t_timeout structure is
    returned. If the time is negative, then the t_timeout is
    set to zeroes.

    NOTE: This function cannot be used in an RTDLL because it
          uses floating-point!!

    Parameters:

    timeout     = a pointer to the t_timeout structure in which
                  to store the result.
    time_value  = the time in seconds (with possible fractional
                  seconds) to be converted.

    Return values:

    Returns the value of the timeout parameter on success. If
    the time value is too large to be represented in a t_timeout
    structure then NULL is returned.
*/
EXTERN t_timeout *
timeout_get_timeout(t_timeout * timeout, double time_value);

/*
    Description:

    This function returns true (1) if the timeout is negative.
    Absolute timeouts are always viewed as positive. Only relative
    timeouts may be negative.

    Parameters:

    timeout     = the timeout to check for a negative value

    Return values:

    Returns true (1) if the timeout is negative. Otherwise it returns
    false (0);
*/
EXTERN t_boolean
timeout_is_negative(const t_timeout * timeout);

/*
    Description:

    This function returns true (1) if the timeout is zero.

    Parameters:

    timeout     = the timeout to check for been zero

    Return values:

    Returns true (1) if the timeout is zero. Otherwise it returns
    false (0);
*/
EXTERN t_boolean
timeout_is_zero(const t_timeout * timeout);

/*
    Description:

    This function returns true (1) if the absolute timeout has
    expired. It uses timeout_get_current_time internally to
    get the current time. Use timeout_compare instead of this
    function if multiple comparisons will be made in order to
    minimize the number of calls to timeout_get_current_time.
    If the timeout is relative then it returns true (1) if the
    relative timeout is negative or zero and false (0) otherwise.

    Parameters:

    timeout = the timeout to check for expiration

    Return values:

    Returns true (1) if the timeout is expired. Otherwise it returns
    false (0);
*/
EXTERN t_boolean
timeout_is_expired(const t_timeout * timeout);

/*
    Description:

    This function converts a timeout to an absolute timeout. If
    the timeout is relative, then it adds the current time as retrieved
    by timeout_get_current_time to the relative timeout. Otherwise
    it simply copies the t_timeout structure.

    Parameters:

    result      = the t_timeout structure in which to store the result
    timeout     = the relative or absolute timeout convert to absolute time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_absolute(t_timeout * result, const t_timeout * timeout);

/*
    Description:

    This function converts a timeout to a relative timeout. If
    the timeout is absolute, then it subtracts the current time as retrieved
    by timeout_get_current_time from the absolute timeout. Otherwise
    it simply copies the t_timeout structure.

    Parameters:

    result      = the t_timeout structure in which to store the result
    timeout     = the relative or absolute timeout convert to relative time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_relative(t_timeout * result, const t_timeout * timeout);

/*
    Description:

    This function compares two timeout values. Both timeouts should
    be either relative or absolute. If one timeout is relative and
    the other timeout is absolute than the relative timeout is converted
    to an absolute timeout prior to doing the comparison.

    Parameters:

    left     = the timeout from which to subtract
    right    = the timeout to subtract from the left argument

    Return values:

    Returns -1 if left < right, 0 if left == right and +1 if left > right.
*/
EXTERN t_int
timeout_compare(const t_timeout * left, const t_timeout * right);

/*
    Description:

    This function subtracts two timeout values such that:
        result = left - right
    If both timeout values are relative, then the result is relative.
    If both timeout values are absolute, then the result is relative.
    If the left-hand side is absolute and the right-hand side is relative,
    then the result is absolute. If the left-hand side is relative in the
    right hand side is absolute then an error is returned.

    Parameters:

    result   = the t_timeout structure in which to store the result
    left     = the timeout from which to subtract
    right    = the timeout to subtract from the left argument

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_subtract(t_timeout * result, const t_timeout * left, const t_timeout * right);

/*
    Description:

    This function adds two timeout values such that:
        result = left + right
    If both timeout values are relative, then the result is relative.
    If both timeout values are absolute, then an error is returned.
    If one time is relative and the other absolute than the result
    is absolute.

    Parameters:

    result   = the t_timeout structure in which to store the result
    left     = the timeout to which to add
    right    = the timeout to add to the left argument

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_add(t_timeout * result, const t_timeout * left, const t_timeout * right);

/*
    Description:

    This function retrieves the current time. This function is
    is used to convert between absolute and relative time.
    The meaning of this time value may have no correlation to the
    current date and time of the system. The resolution of this time
    is system-dependent.

    Parameters:

    timeout  = the t_timeout structure in which to store the current time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_current_time(t_timeout * time);

/*
    Description:

    This function retrieves the current high-resolution time. This
    function may be used to time very short intervals because it
    is typically based on a 64-bit free running counter with
    sub-microsecond resolution.

    The meaning of this time value may have no correlation to the
    current date and time of the system. The resolution of this time
    is system-dependent.

    Parameters:

    timeout  = the t_timeout structure in which to store the high-resolution time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_high_resolution_time(t_timeout * time);

/*
    Description:

    This function retrieves the CPU time consumed by the current thread.

    Parameters:

    timeout = the t_timeout structure in which to store the CPU time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_thread_cpu_time(t_timeout * time);

/*
    Description:

    This function retrieves the CPU time consumed by the process.

    Parameters:

    timeout = the t_timeout structure in which to store the CPU time

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_process_cpu_time(t_timeout * time);

/*
    Description:

    This function converts the given timeout into a relative time in
    milliseconds from the current high-resolution time. If the timeout
    parameter is NULL then the number of milliseconds is set to -1.
    Many systems interpret this value as infinite which is the intended
    meaning of a NULL timeout parameter. If the given timeout precedes
    the current time than the number of milliseconds is set to 0.
    If the timeout exceeds the value of a 32-bit integer milliseconds then
    an error is returned.

    Parameters:

    timeout      = the t_timeout to convert to a relative time in milliseconds
    milliseconds = a pointer to as t_int32 variable in which to store the
                   number of milliseconds

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
timeout_get_milliseconds(t_int32 * milliseconds, const t_timeout * timeout);

#endif
