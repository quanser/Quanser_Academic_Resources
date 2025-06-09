#if !defined(_qtimer_h)
#define _qtimer_h

#include "quanser_extern.h"
#include "quanser_types.h"
#include "quanser_errors.h"
#include "quanser_time.h"
#include "quanser_thread.h"

#if defined(UNDER_RTSS) || defined(__INTIME__)
#define TIMER_DECL              __stdcall
#define DELAYTIMER_MAX          1
#define TIMER_FLAG_FAST_TIMER   0   /* this option does not exist under INtime or RTX */
#elif defined(_WIN32)
#define TIMER_DECL
#define DELAYTIMER_MAX          1
#define TIMER_FLAG_FAST_TIMER   1   /* allow QUARC Timing Services to be used */
#else
#define TIMER_DECL
#define TIMER_FLAG_FAST_TIMER   0   /* this option only exists under Windows */
#endif

typedef struct tag_period
{
    t_long seconds;
    t_int  nanoseconds;
} t_period;

typedef enum tag_timer_notify_type
{
    TIMER_NOTIFY_EVENT,
    TIMER_NOTIFY_HANDLER,
    TIMER_NOTIFY_SEMAPHORE
} t_timer_notify_type;

typedef struct tag_timer_event * t_timer_event;
typedef struct tag_timer_semaphore * t_timer_semaphore;
typedef void (TIMER_DECL * t_timer_proc)(void * argument);

typedef struct tag_timer_notify
{
    t_timer_notify_type notify_type;
    union tag_value
    {
        t_timer_event event;
        t_timer_semaphore semaphore;
        struct tag_timer_thread
        {
            t_timer_proc handler;
            void * argument;
            qthread_attr_t attributes;
        } thread;
    } notify_value;
    t_uint flags;       /* set to 0 for all targets except Windows (in which case TIMER_FLAG_FAST_TIMER flag may be set) */
} t_timer_notify;

typedef struct tag_timer * t_timer;

/*
    Description:

    This function creates a timer event. Timer events are much like
    semaphores or Windows events except they are restricted to
    timers and do not maintain a count. A qtimer may be configured
    to post a timer event at each timer expiration. Wait on this
    event using the qtimer_event_wait function. The timer event may
    be signalled manually using the qtimer_event_post function.

    If timer events are shared between timers then the timer
    overrun count may report unexpected results. In general,
    timer events should not be shared between timers.

    The timer event must be deleted using qtimer_event_delete
    when it is no longer in use in order to free up system
    resources.

    Under QNX, this function is a cancellation point. It is not
    a cancellation point under Windows or RTX.

    Parameters:

    event   = a pointer to a t_timer_event variable in which to store
              the handle to the event

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_event_create(t_timer_event * event);

/*
    Description:

    This function posts a timer event. The qtimer_event_wait
    function will return just as if a qtimer had posted the
    event. If this function is called multiple times before
    the first qtimer_event_wait call then qtimer_event_wait
    will only recognize one event. This behaviour is similar
    to Windows events or UNIX non-queued signals.

    Parameters:

    event = a handle to the timer event

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_event_post(t_timer_event event);

/*
    Description:

    This function waits for a timer event. The qtimer_event_wait
    function will block until the timer event is posted, either
    by a qtimer or calling qtimer_event_post. If a timer event
    is posted multiple times before the first qtimer_event_wait
    call then qtimer_event_wait will only recognize one event. 
    This behaviour is similar to Windows events or UNIX non-queued
    signals.

    In QNX, this function can be interrupted by a signal, in which
    case it returns -QERR_INTERRUPTED.

    Parameters:

    event = a handle to the timer event

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_event_wait(t_timer_event event);

/*
    Description:

    This function deletes a timer event. It must be called
    to clean up the resources allocated for the event. The event
    cannot be used after it has been deleted.

    Parameters:

    event = a handle to the timer event

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_event_delete(t_timer_event event);

/*
    Description:

    This function creates a timer semaphore. Timer semaphores are much like
    regular semaphores or Windows semaphores except they are restricted to
    timers. A qtimer may be configured to post a timer semaphore at each timer 
    expiration. Wait on this semaphore using the qtimer_semaphore_wait function. 
    The timer semaphore may be signalled manually using the qtimer_semaphore_post function.

    If timer semaphores are shared between timers then the timer
    overrun count may report unexpected results. In general,
    timer semaphores should not be shared between timers.

    The timer semaphore must be deleted using qtimer_semaphore_delete
    when it is no longer in use in order to free up system
    resources.

    Under QNX, this function is a cancellation point. It is not
    a cancellation point under Windows or RTX.

    Parameters:

    semaphore = a pointer to a t_timer_semaphore variable in which to store
                the handle to the semaphore

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_semaphore_create(t_timer_semaphore* semaphore);

/*
    Description:

    This function posts a timer semaphore. The qtimer_semaphore_wait
    function will return just as if a qtimer had posted the
    semaphore. If this function is called multiple times before
    the first qtimer_semaphore_wait call then qtimer_semaphore_wait
    will return immediately for the same number of times. This behaviour 
    is similar to a Windows or UNIX semaphores.

    Parameters:

    semaphore = a handle to the timer semaphore

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_semaphore_post(t_timer_semaphore semaphore);

/*
    Description:

    This function waits for a timer semaphore. The qtimer_semaphore_wait
    function will block until the timer semaphore is posted, either
    by a qtimer or calling qtimer_semaphore_post. If a timer semaphore
    is posted multiple times before the first qtimer_semaphore_wait
    call then qtimer_semaphore_wait will return immediately for the
    same number of times the semaphore was posted. This behaviour is 
    similar to Windows or UNIX semaphores.

    In QNX, this function can be interrupted by a signal, in which
    case it returns -QERR_INTERRUPTED.

    Parameters:

    semaphore = a handle to the timer semaphore

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_semaphore_wait(t_timer_semaphore semaphore);

/*
    Description:

    This function deletes a timer semaphore. It must be called
    to clean up the resources allocated for the semaphore. The semaphore
    cannot be used after it has been deleted.

    Parameters:

    semaphore = a handle to the timer semaphore

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_semaphore_delete(t_timer_semaphore semaphore);

/*
    Description:

    This function creates a timer. The t_timer_notify structure
    indicates the type of notification to perform when the timer
    expires. Quanser timers support two notifications mechanisms:
        - a timer event
        - a timer handler
    
    Timer events are like Windows events or UNIX signals and allow
    code to wait on the event using the qtimer_event_wait function.
    Timer events are created using the qtimer_event_create function.
    To use a timer event for notification, set the notify_type field
    to TIMER_NOTIFY_EVENT and set the notify_value.event field to
    the t_timer_event handle created via qtimer_event_create.

    Timer handlers are callback functions that are invoked when the
    timer expires. Unlike signal handlers, timer handlers are executed
    in a separate thread and thus the functions called within a timer
    handler must be multithread-safe but not asynchronous-signal safe.

    This function is not a cancellation point.

    Parameters:

    notify  = a pointer to a t_timer_notify structure indicating the
              type of notification mechanism to use for the timer
    timer   = a pointer to a t_timer variable in which to store
              the handle to the timer

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_create(const t_timer_notify * notify, t_timer * timer);

/*
    Description:

    This function sets the resolution of the timer. Every call to
    qtimer_begin_timer_resolution must ALWAYS be matched by a call
    to qtimer_end_resolution once the timer is no longer in use,
    unless qtimer_begin_resolution returns an error.
    
    In general, the resolution may be set to the same period as the
    desired timer period. This function must be called to achieve
    sampling rates faster than 1KHz on QNX. This function is also
    useful to ensure that a given sampling rate is achievable
    prior to actually setting the timer.

    If the specified resolution is not supported because it is
    too small then -QERR_OUT_OF_RANGE is returned. If the new
    resolution is too large, then the resolution is left
    unchanged and 0 is returned.

    Under QNX, this function may be a cancellation point.

    Parameters:

    timer      = the handle to the timer
    resolution = a pointer to a t_period structure containing
                 the new resolution. It may not be NULL.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_begin_resolution(t_timer timer, const t_period * resolution);

/*
    Description:

    This function takes a desired period and returns the actual period
    that can be delivered by the given timer. Timers are always based
    upon counter driven by an oscillator of a given fixed frequency.
    Hence, the period that can be delivered by a timer is always an
    integer multiple of the oscillator period. The actual_period returned
    by this function will be an integer multiple of the oscillator period.

    This function is not a cancellation point.

    Parameters:

    timer           = the handle to the timer
    desired_period  = a pointer to a t_period structure containing the
                      desired period.
    actual_period   = a pointer to a t_period structure in which the
                      actual period will be returned.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_get_actual_period(t_timer timer, const t_period * desired_period, t_period * actual_period);

/*
    Description:

    This function sets the timer. The timer may be periodic
    or one-shot. Set the is_periodic argument to true to get
    a periodic timer. Otherwise the timer only expires once.

    This function is not a cancellation point.

    Parameters:

    timer       = the handle to the timer
    period      = a pointer to a t_period structure containing the
                  expiration interval.
    is_periodic = set to true to make the timer periodic. Set
                  to false to make a one-shot timer.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_set_time(t_timer timer, const t_period * period, t_boolean is_periodic);

/*
    Description:

    This function returns the number of timer overruns. Only a single
    timer event is queued for any given timer event at any point in
    time. When a timer event is pending from the last timer
    expiration and the timer expires again then a timer overrun
    occurs and the overrun count is incremented. If the timer event
    is processed before the next timer expiration then an overrun
    does not occur.

    The overrun count returned is the number of extra timer expirations
    that occurred between the time the expiration event was signaled
    and when it was delivered or accepted, up to DELAYTIMER_MAX. If
    the number of overruns is greater than or equal to DELAYTIMER_MAX,
    the overrun count is set to DELAYTIMER_MAX.

    The value returned by qtimer_getoverrun applies only to the most
    recent expiration of the timer. If no expiration signal has been
    signaled then the overrun count is zero.

    This function will always return 0 for TIMER_NOTIFY_HANDLER
    timer notifications under RTX.

    Parameters:

    timer = the handle to the timer

    Return values:

    Returns the number of overruns on success. Otherwise it returns a
    negative error code.
*/
EXTERN t_int
qtimer_get_overrun(t_timer timer);

/*
    Description:

    This function cancels the timer without deleting it. The timer
    can be set again using qtimer_set_time after it is cancelled.

    Parameters:

    timer = the handle to the timer

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_cancel(t_timer timer);

/*
    Description:

    This function resets the resolution of the timer. Every call to
    qtimer_begin_timer_resolution must ALWAYS be matched by a call
    to qtimer_end_resolution once the timer is no longer in use,
    unless qtimer_begin_resolution returns an error. Do not call
    qtimer_end_resolution if qtimer_begin_resolution returned an
    error.
    
    Parameters:

    timer = the handle to the timer

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_end_resolution(t_timer timer);

/*
    Description:

    This function deletes the timer.

    Parameters:

    timer = the handle to the timer

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_delete(t_timer timer);

/*
    Description:

    This function sleeps for the given timeout period.

    Parameters:

    timeout = the timeout interval

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qtimer_sleep(const t_timeout * timeout);

#endif
