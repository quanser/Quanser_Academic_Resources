#if !defined(_quanser_thread_h)
#define _quanser_thread_h

/*
    This header file defines a set of functions for creating and manipulating real-time
    threads. It is modelled after the POSIX thread functions but is modified and restricted
    such that these functions work on every QUARC target.

    A thread is created using the qthread_create function. To ensure that the thread resources
    are freed, the qthread_join function must be called for the thread prior to program exit.
    To set the attributes of the thread upon thread creation, define a qthread_attr_t variable
    and initialize it using the qthread_attr_init function. This function initializes it with
    default values. To modify the defaults, use the appropriate qthread_attr_xxxx functions.
    After creating the thread, the qthread_attr_t variable should be destroyed using the
    qthread_attr_destroy function. The same qthread_attr_t variable may be used to create
    multiple threads.

    Cancellation points are supported, as in POSIX. Under Windows, a cancellation point is
    equivalent to an alertable function. The qthread_cancel function may be used to cause
    a thread to exit at a cancellation point. Hence, stopping a thread is often achieved by
    calling qthread_cancel followed by qthread_join.

    To ensure that any necessary cleanup is performed when a thread exits, even if it is
    cancelled, cleanup handlers are also supported. A cleanup handler is pushed on the
    "cleanup handler stack" by the qthread_cleanup_push function. This function will be
    called if the thread exits or is cancelled. The cleanup handler is removed from the
    cleanup handler stack by the qthread_cleanup_pop function. The qthread_cleanup_push
    and qthread_cleanup_pop functions must be scoped as if they were curly braces.

    A few other qthread functions exist for manipulating the CPU affinity and priority
    of threads, among others.
*/
#include "quanser_mutex.h"
#include "quanser_scheduler.h"

/* The minimum stack size allowed on any platform */
#define QTHREAD_STACK_MIN       8192

typedef void (*qthread_once_callback_t)(void);

/*
    Name:   qthread_cleanup_push

    Description:

    This function pushes a cleanup handler onto the cleanup handler stack.
    It must be matched by a corresponding call to qthread_cleanup_pop. These
    two functions must be paired in the same way as curly braces.

    When a thread exits or is cancelled, all the cleanup handlers currently
    on the cleanup handler stack are popped from the stack and executed.
    Cleanup handlers are a convenient way of ensuring that resources have been
    released when a thread exits, even if it is cancelled.

    To remove a cleanup handler from the stack, use the qthread_cleanup_pop
    function. The argument to the qthread_cleanup_pop function determines
    whether the cleanup handler is executed or not when it is popped from
    the stack.

    Note that cleanup handlers may not be used in C++ functions that contain
    objects that require stack unwinding (class objects defined on the stack
    that have a destructor). Use try/catch instead. Define a catch(...)
    condition to execute code when the thread is cancelled and rethrow the
    exception in the catch(...) handler so that the thread continues to be
    cancelled.

    Parameters:

    handler = the address of the cleanup handler routine. It must have the
              prototype:
                    void handler(void * context)
              It may be a static function so that it has file scope.
    context = the value that will be passed to the cleanup handler as its argument.

    Return value:

    This function does not return a value.
*/

/*
    Name:   qthread_cleanup_pop

    Description:

    This function pops a cleanup handler from the cleanup handler stack.
    If the execute argument is non-zero then it executes the cleanup handler
    after popping it from the stack. Otherwise, it removes the cleanup
    handler from the stack without executing it.

    Parameters:

    execute = a boolean flag indicating whether to execute the cleanup
              handler or not. Set it to true to execute the cleanup handler.
              If it is false then the cleanup handler is not executed.

    Return value:

    This function does not return a value.
*/

#if (defined(_WIN32) || defined(__INTIME__)) && (!defined(__MINGW32__) || defined(__QT__))

#include <windows.h>

typedef struct tag_qthread * qthread_t;
typedef t_uint qthread_id_t;
typedef t_uint qthread_return_t;
typedef INIT_ONCE qthread_once_t;
typedef DWORD qthread_key_t;

typedef struct tag_qthread_attr
{
    size_t stack_size;
    qsched_param_t scheduler_parameters;
    int scheduler_policy;
    int scheduler_inherit;
    qcpu_set_t cpu_affinity;
} qthread_attr_t;

#define QTHREAD_DECL            __stdcall

#define QTHREAD_INHERIT_SCHED   0
#define QTHREAD_EXPLICIT_SCHED  1

#define QTHREAD_CANCELED        0xffffffffU

#define INVALID_QTHREAD         NULL
#define INVALID_QTHREAD_ID      (~0U)

#define QTHREAD_ONCE_INIT      INIT_ONCE_STATIC_INIT

#define QTHREAD_CANCEL_ENABLE   1
#define QTHREAD_CANCEL_DISABLE  0

struct _qthread_cleanup_context
{
    void (* _handler)(void * context);
    void * _context;
    volatile int _execute;
};

#if defined(__cplusplus)

#define qthread_cleanup_push(handler, context) \
    do { \
        struct _qthread_cleanup_context _qthread_cleanup_info = { handler, context, true }; \
        try {

#define qthread_cleanup_pop(execute)  \
            _qthread_cleanup_info._execute = execute;  \
            if (_qthread_cleanup_info._execute)        \
                _qthread_cleanup_info._handler(_qthread_cleanup_info._context); \
        } catch (...) {                 \
            if (_qthread_cleanup_info._execute)        \
                _qthread_cleanup_info._handler(_qthread_cleanup_info._context); \
            throw; \
        } \
    } while (0)

#else /* !__cplusplus */

#define qthread_cleanup_push(handler, context) \
    do { \
        struct _qthread_cleanup_context _qthread_cleanup_info = { handler, context, true }; \
        __try {

#define qthread_cleanup_pop(execute)  \
            _qthread_cleanup_info._execute = execute;  \
        } __finally {                 \
            if (_qthread_cleanup_info._execute)        \
                _qthread_cleanup_info._handler(_qthread_cleanup_info._context); \
        } \
    } while(0)

#endif /* __cplusplus */

#else

#include <pthread.h>

typedef pthread_t      qthread_t;
typedef pthread_t      qthread_id_t;
typedef void *         qthread_return_t;
typedef pthread_once_t qthread_once_t;
typedef pthread_key_t  qthread_key_t;

#if (defined(__linux) && !defined(_UCLIBC)) || defined(__vxworks) || defined(__APPLE__)
typedef pthread_attr_t qthread_attr_t;

#elif defined(__APPLE__ALT__)

#define QSCHED_REALTIME_FLAG_IS_REALTIME    (1 << 0)    /* real-time policy in force */
#define QSCHED_REALTIME_FLAG_PREEMPTIBLE    (1 << 1)    /* real-time thread is preemptible within the constraint */

typedef struct tag_qthread_realtime_attr
{
    int period;             /* period at which to repeatedly run real-time thread, in nanoseconds */
    int computation;        /* amount of computation time needed by the real-time thread each period, in nanoseconds */
    int constraint;         /* amount of time within the period over which computation time may be spread, in nanoseconds */
    unsigned char flags;    /* see QSCHED_REALTIME_FLAG_XXXX flags */
} t_qthread_realtime_attr;

typedef struct tag_qthread_attr
{
    pthread_attr_t standard_attributes; /* standard attributes, including policy and priority */
    
    /* Parameters for real-time scheduler policy, QSCHED_REALTIME */
    t_qthread_realtime_attr realtime;
} qthread_attr_t;        

#else
typedef struct tag_qthread_attr
{
    pthread_attr_t standard_attributes;
    qcpu_set_t     cpu_affinity;
} qthread_attr_t;

#endif

#define QTHREAD_DECL

#define QTHREAD_INHERIT_SCHED   PTHREAD_INHERIT_SCHED
#define QTHREAD_EXPLICIT_SCHED  PTHREAD_EXPLICIT_SCHED

#define QTHREAD_CANCELED        PTHREAD_CANCELED

#if defined(__APPLE__ALT__)
#define INVALID_QTHREAD         (NULL)
#define INVALID_QTHREAD_ID      ((qthread_id_t) (-1))
#elif defined(__MINGW32__) && !defined(__QT__)
extern pthread_t INVALID_QTHREAD;
#define INVALID_QTHREAD_ID      INVALID_QTHREAD
#else
#define INVALID_QTHREAD         ((qthread_t)(-1))
#define INVALID_QTHREAD_ID      ((qthread_id_t) (-1))
#endif

#define QTHREAD_ONCE_INIT       PTHREAD_ONCE_INIT

#define QTHREAD_CANCEL_ENABLE   PTHREAD_CANCEL_ENABLE
#define QTHREAD_CANCEL_DISABLE  PTHREAD_CANCEL_DISABLE

#define qthread_cleanup_push(handler, context)  pthread_cleanup_push(handler, context)
#define qthread_cleanup_pop(execute)            pthread_cleanup_pop(execute)

#endif

typedef void (QTHREAD_DECL * qthread_key_destructor_t)(void*);

/*
    Name:   qthread_attr_init

    Description:

    This function must be called to initialize a qthread_attr_t structure.
    It initializes all the fields to appropriate default values. To modify
    any of the fields of the qthread_attr_t structure, use the qthread_attr_xxxx
    functions. Do not modify the structure directly since its contents differ
    on every QUARC target.

    When the qthread_attr_t structure is no longer needed, free up its
    resources by calling qthread_attr_destroy.

    Parameters:

    attributes  = the address of the qthread_attr_t variable to initialize.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_init(qthread_attr_t * attributes);

/*
    Name:   qthread_attr_getstacksize

    Description:

    This function returns the stack size configured in a qthread_attr_t structure.
    The stack size is returned in the stack_size argument, not the return
    value.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    stack_size  = the address of a size_t variable that will be set to the stack 
                  size.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_getstacksize(const qthread_attr_t * attributes, size_t * stack_size);

/*
    Name:   qthread_attr_setstacksize

    Description:

    This function sets the stack size configured in a qthread_attr_t structure.
    The stack size is specified in bytes. It must be at least QTHREAD_STACK_MIN
    bytes or an error will be returned.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    stack_size  = the new stack size.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_setstacksize(qthread_attr_t * attributes, size_t stack_size);

/*
    Name:   qthread_attr_getinheritsched

    Description:

    This function returns whether the scheduler parameters are configured as inherited
    or explicitly defined in a qthread_attr_t structure. The inherited setting
    is returned in the inherit_sched argument, not the return value. The value
    of the inherit_sched argument will be one of two values upon return from
    this function:
        
        QTHREAD_INHERIT_SCHED   = the scheduler parameters are inherited
        QTHREAD_EXPLICIT_SCHED  = the scheduler parameters are explicitly specified

    It the scheduler parameters are inherited then the scheduler parameters
    stored in the qthread_attr_t structure are ignored, even if the
    qthread_attr_setschedparam function has been called.

    Parameters:

    attributes      = the address of the qthread_attr_t variable.
    inherit_sched   = the address of an int variable that will be set to the
                      scheduler inheritance setting.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_getinheritsched(const qthread_attr_t * attributes, int * inherit_sched);

/*
    Name:   qthread_attr_setinheritsched

    Description:

    This function sets whether the scheduler parameters are inherited
    or explicitly defined in a qthread_attr_t structure. It may be set to
    one of two values:
        
        QTHREAD_INHERIT_SCHED   = the scheduler parameters are inherited
        QTHREAD_EXPLICIT_SCHED  = the scheduler parameters are explicitly specified

    It the scheduler parameters are inherited then the scheduler parameters
    stored in the qthread_attr_t structure are ignored, even if the
    qthread_attr_setschedparam function has been called.

    Thus, to change the thread priority (a scheduler parameter), call the
    following sequence of functions:

        qsched_param_t param;
        param.priority = 0;

        qthread_attr_setinheritsched(&attr, QTHREAD_EXPLICIT_SCHED);
        qthread_attr_setschedparam(&attr, &param);

    Parameters:

    attributes      = the address of the qthread_attr_t variable.
    inherit_sched   = either QTHREAD_INHERIT_SCHED or QTHREAD_EXPLICIT_SCHED.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_setinheritsched(qthread_attr_t * attributes, int inherit_sched);

/*
    Name:   qthread_attr_getschedpolicy

    Description:

    This function returns the scheduler policy configured in a qthread_attr_t 
    structure. Scheduler policies are defined in quanser_scheduler.h. The
    default policy is QSCHED_FIFO. Not all scheduler policies are valid on
    all QUARC targets.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    policy      = the address of an int variable that will be set to the
                  scheduler policy defined in the qthread_attr_t structure.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_getschedpolicy(const qthread_attr_t* attributes, int * policy);

/*
    Name:   qthread_attr_setschedpolicy

    Description:

    This function configures the scheduler policy in a qthread_attr_t 
    structure. Scheduler policies are defined in quanser_scheduler.h. The
    default policy is QSCHED_FIFO. Not all scheduler policies are valid on
    all QUARC targets.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    policy      = one of the QSCHED_XXXX constants defining the scheduler
                  policy.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_setschedpolicy(qthread_attr_t* attributes, int policy);

/*
    Name:   qthread_attr_getschedparam

    Description:

    This function returns the scheduler parameters configured in a qthread_attr_t 
    structure. The scheduler parameters are defined in quanser_scheduler.h. The
    only scheduler parameter currently used is the sched_priority, which defines
    the priority that will be used for the thread. The scheduler parameters are
    returned in a qsched_param_t structure. The priority will be in 
    the range of priorities returned by the scheduler functions
    qsched_get_priority_min and qsched_get_priority_max, which get the minimum
    and maximum priorities for a given scheduler policy.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    param       = the address of a qsched_param_t structure that will be filled
                  with the scheduler parameters defined in the qthread_attr_t 
                  structure.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_getschedparam(const qthread_attr_t * attributes, qsched_param_t * param);
                    
/*
    Name:   qthread_attr_setschedparam

    Description:

    This function sets the scheduler parameters in a qthread_attr_t structure. 
    The scheduler parameters are defined in quanser_scheduler.h. The
    only scheduler parameter currently used is the sched_priority, which defines
    the priority that will be used for the thread. The priority must be in 
    the range of priorities returned by the scheduler functions
    qsched_get_priority_min and qsched_get_priority_max, which get the minimum
    and maximum priorities for a given scheduler policy.

    Parameters:

    attributes  = the address of the qthread_attr_t variable.
    param       = the address of a qsched_param_t structure that must be filled
                  with the desired scheduler parameters.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_setschedparam(qthread_attr_t * attributes, const qsched_param_t * param);

/*
    Name:   qthread_attr_getaffinity

    Description:

    This function returns the CPU affinity configured in a qthread_attr_t 
    structure. The qcpu_set_t structure is defined in quanser_scheduler.h. It
    identifies a set of CPUs upon which the thread will be allowed to run. This
    structure is defined differently on each QUARC target and its fields should never
    be accessed directly. Instead, use the QCPU_XXXX macros to get information
    about the CPUs in the set of CPUs defined by a qcpu_set_t structure.

    Parameters:

    attributes      = the address of the qthread_attr_t variable.
    cpu_set_size    = the size of the CPU set. Pass sizeof(qcpu_set_t).
    set             = the address of a qcpu_set_t structure that will be filled
                      with the CPU affinity mask defined in the qthread_attr_t 
                      structure.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN int
qthread_attr_getaffinity(const qthread_attr_t * attributes, size_t cpu_set_size, qcpu_set_t * set);

/*
    Name:   qthread_attr_setaffinity

    Description:

    This function sets the CPU affinity in a qthread_attr_t  structure. The 
    qcpu_set_t structure is defined in quanser_scheduler.h. It identifies a set of
    CPUs upon which the thread will be allowed to run. This structure is defined 
    differently on each QUARC target and its fields should never be accessed directly. 
    Instead, use the QCPU_XXXX macros to set the information about the CPUs in the 
    set of CPUs defined by a qcpu_set_t structure. For example:

        qcpu_set_t affinity;
        QCPU_ZERO(&affinity);
        QCPU_SET(0, &affinity);     // allow thread to run on CPU 0
        QCPU_SET(2, &affinity);     // allow thread to run on CPU 2

        qthread_attr_setaffinity(&attr, sizeof(affinity), &affinity);

    Parameters:

    attributes      = the address of the qthread_attr_t variable.
    cpu_set_size    = the size of the CPU set. Pass sizeof(qcpu_set_t).
    set             = the address of a qcpu_set_t structure containing
                      the CPU affinity.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN int
qthread_attr_setaffinity(qthread_attr_t * attributes, size_t cpu_set_size, const qcpu_set_t * set);

/*
    Name:   qthread_attr_destroy

    Description:

    This function releases any resources allocated in the qthread_attr_t
    structure. It must be called when the qthread_attr_t structure is no
    longer needed. Note that the qthread_attr_t structure may be destroyed
    as soon as the thread is created. It does NOT need to be maintained
    until thread exit.

    Parameters:

    attributes = the address of the qthread_attr_t variable.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_attr_destroy(qthread_attr_t * attributes);

/*
    Name:   qthread_create

    Description:

    This function creates a thread. The handle to the thread is returned in the
    qthread_t variable whose address is passed in the thread parameter. Likewise,
    the identifier of the thread is returned in the qthread_id_t variables whose
    address is passed in the thread_id parameter. The thread_id parameter may be
    NULL if the thread identifier is not required. The thread identifier is the
    only way to compare threads for equality, however. This function differs from
    the POSIX pthread_create function in this regard because some QUARC targets
    differentiate between a thread handle and a thread identifier.

    The characteristics of the thread are defined by the qthread_attr_t structure
    whose address is passed in the attributes parameter. This parameter may be NULL
    to use the default thread attributes.

    The start_routine parameter is the address of a function that will be called
    as the main entry point of the new thread. The thread continues execution
    until the start_routine returns or calls the qthread_exit function. The start
    routine should be declared as:

        qthread_return_t QTHREAD_DECL mythreadroutine(void * context) { ... }

    The name of the routine is arbitrary. The routine may also be static so that
    it has file scope. Do not forget the QTHREAD_DECL and do not define a return
    type other than qthread_return_t. These quantities ensure that the code will
    work properly on all QUARC targets.

    The context argument of the start_routine will be the value passed in the
    argument parameter of qthread_create. If the address of a structure is passed
    to the thread then be sure that the structure remains valid and does not go
    out of scope (if defined on the stack) until the thread has copied it or
    otherwise used its contents. This requirement is typically satisfied by
    waiting on a semaphore in the thread that called qthread_create and signalling
    that semaphore in the start_routine of the new thread when the structure is
    no longer needed.

    To kill a thread in a graceful manner, cancel the thread using the qthread_cancel
    function. The qthread_cancel function causes the thread to exit when it reaches
    a "cancellation point", which is typically a blocking system call or the 
    qthread_testcancel function. On the QUARC Windows target, only functions that
    perform an alertable wait are cancellation points.

    To wait for a thread to exit, use the qthread_join function. The name comes
    from the POSIX pthread API and refers to the synchronization that occurs between
    the current thread and the thread being waited upon when this function is called.
    The qthread_join function returns the exit code of the thread.

    The qthread_join function MUST be called to release the resources for the thread.
    Use the qthread_cancel function if necessary to ensure that the thread will exit
    before calling qthread_join, although it is better to code the thread in such a
    way that it is guaranteed to exit when desired. 

    If the thread cannot be created then a negative error code is returned and the
    thread handle is set to INVALID_QTHREAD. Use the error code rather than INVALID_QTHREAD
    however to test for failure to create the thread.
    
    Parameters:

    thread          = the address of a qthread_t variable to receive the thread handle
                      of the new thread. It must NOT be NULL.
    thread_id       = the address of a qthread_id_t variable to receive the thread
                      identifier of the new thread. It may be NULL.
    attributes      = the address of a qthread_attr_t structure defining the desired
                      attributes of the new thread.
    start_routine   = the function to call in the new thread (the main entry point
                      of the new thread).
    argument        = a value that is passed to the start_routine.

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_create(qthread_t * thread, qthread_id_t * thread_id, const qthread_attr_t * attributes,
               qthread_return_t (QTHREAD_DECL * start_routine) (void *), void * argument);

/*
    Name:   qthread_self

    Description:

    This function returns the handle of the current thread. This handle may NOT be
    used to compare threads since it may only be a placemarker to identify the
    current thread. It should not be passed to other threads to refer to the
    current thread (for example, so another thread may call qthread_cancel). Only
    the thread handle returned by qthread_create may be passed to other threads
    for such a purpose. The handle returned by this function may ONLY be used
    by the current thread.

    To compare threads, use the qthread_id and qthread_equal functions instead,
    since thread identifiers uniquely identify each thread.

    The semantics of this function differ from the POSIX pthread_self() function.
    The full semantics of pthread_self are split between two functions in QUARC:
    qthread_self and qthread_id.

    Parameters:

    This function has no parameters.

    Return value:

    A handle which refers to the current thread. This handle may only be used
    by the current thread.
*/
EXTERN qthread_t
qthread_self(void);

/*
    Name:   qthread_id

    Description:

    This function returns the identifier of the current thread. The thread identifier
    uniquely identifies the thread. Thus, it may be used to compare threads via the
    qthread_equal function. However, the thread identifier may NOT be used in place
    of a thread handle. For example, it is not possible to pass the thread identifier
    to the qthread_cancel function. Code which does so is not guaranteed to work on
    all QUARC targets (and, in fact, is guaranteed to fail miserably on some
    QUARC targets).

    Only the thread handle returned by the qthread_create function may be passed
    to functions which require a thread handle, such as qthread_cancel and qthread_join.

    Parameters:

    This function has no parameters.

    Return value:

    A handle which refers to the current thread. This handle may only be used
    by the current thread.
*/
EXTERN qthread_id_t
qthread_id(void);

/*
    Name:   qthread_equal

    Description:

    This function compares two thread identifiers to determine whether they
    refer to the same thread. The thread identifer of a thread is returned by
    the qthread_create function (as the second argument!) or the qthread_id
    function.

    This function returns true if the threads are equal and false otherwise.

    Parameters:

    t1 = the identifer of the first thread
    t2 = the identifer of the second thread to compare to the first

    Return value:

    Returns true if the threads are the same and false otherwise.
*/
EXTERN t_boolean
qthread_equal(qthread_id_t t1, qthread_id_t t2);

/*
    Name:   qthread_cancel

    Description:

    This function cancels the given thread. The thread will exit the next
    time it reaches a cancellation point. On POSIX systems, only certain system
    calls are defined as cancellation points. Refer to the documentation for
    the target operating system for details on which functions are cancellation
    points. On Windows, QUARC defines alertable functions as cancellation
    points. 
    
    Note that the QUARC communications functions qcomm_send, qcomm_receive and 
    qcomm_poll are generally cancellation points on all QUARC targets. Writers
    of protocol drivers should ensure that their driver also conforms to this
    requirement, if possible, because doing so ensures that QUARC can interrupt
    blocking I/O when the model is stopped.

    The qthread_mutex_xxx functions are not cancellation points. Hence, the
    thread being cancelled generally has the opportunity to exit a critical
    section before being cancelled.

    To ensure that a thread has an opportunity to release resources when it
    is cancelled, use the qthread_cleanup_push and qthread_cleanup_pop macros
    to push or pop cleanup handlers from the cleanup handler stack. The
    cleanup handler functions currently on the cleanup handler stack are
    invoked by a thread when the thread is cancelled. Refer to the documentation
    for qthread_cleanup_push/pop near the top of this file for more information.

    Parameters:

    thread    = the handle of the thread to cancel
    thread_id = the identifier of the thread to cancel (required by some O/Ses)

    Return value:

    Returns 0 if the thread has been marked as cancelled and a negative error
    code otherwise.
*/
EXTERN t_error
qthread_cancel(qthread_t thread, qthread_id_t thread_id);

/*
    Name:   qthread_testcancel

    Description:

    This function defines a cancellation point. It tests whether the current thread
    is being cancelled and exits the thread if the thread is being cancelled.
    This function is convenient for defining points at which the thread may
    exit, particularly for worker threads which may not call a system function
    that is a cancellation point. Refer to qthread_cancel for more details.

    This function does NOT block waiting for the thread to be cancelled.
    Instead, it simply polls the state of the thread cancellation.

    Parameters:

    This function has no parameters.

    Return value:

    This function does not return a value since it never returns if the
    thread is cancelled.
*/
EXTERN void
qthread_testcancel(void);

/*
    Name:   qthread_join

    Description:

    This function waits for a thread to exit. It also release any resources
    required for the thread and returns the thread's exit code. The exit code
    of the thread is the value returned by the thread routine or passed to
    qthread_exit. 
    
    This function MUST be called to release the resources for the thread. Use
    the qthread_cancel function if necessary to ensure that the thread will
    exit before calling qthread_join, although it is better to code the thread
    such that it is guaranteed to exit when desired.

    If the thread is cancelled, then the exit code will be QTHREAD_CANCELED.

    Parameters:

    thread      = the handle of the thread for which to wait
    exit_code   = the address of a qthread_return_t variable which will be set
                  to the exit code of the thread. Pass NULL if the exit code
                  is not needed.

    Return value:

    Returns 0 on success and a negative error code on failure.
*/
EXTERN t_error
qthread_join(qthread_t thread, qthread_return_t * exit_code);

/*
    Name:   qthread_timedjoin

    Description:

    This function waits for a thread to exit until the specified timeout.
    If it does not time out, then it also release any resources required for the
    thread and returns the thread's exit code. The exit code of the thread is the
    value returned by the thread routine or passed to qthread_exit.

    This function, or qthread_join, MUST be called to release the resources for the thread. Use
    the qthread_cancel function if necessary to ensure that the thread will
    exit before calling qthread_join, although it is better to code the thread
    such that it is guaranteed to exit when desired.

    If the thread is cancelled, then the exit code will be QTHREAD_CANCELED.
    
    If the wait times out before the thread completes then -QERR_TIMED_OUT is returned.

    Parameters:

    thread      = the handle of the thread for which to wait
    exit_code   = the address of a qthread_return_t variable which will be set
                  to the exit code of the thread. Pass NULL if the exit code
                  is not needed.

    Return value:

    Returns 0 on success and a negative error code on failure.
*/
EXTERN t_error
qthread_timedjoin(qthread_t thread, qthread_return_t* exit_code, const t_timeout * timeout);

/*
    Name:   qthread_exit

    Description:

    This function causes the current thread to exit normally. It
    does not return. The exit code passed as an argument will be
    the exit code of the thread. This exit code will be returned
    by the qthread_join function in its exit_code argument.

    Parameters:

    exit_code   = the exit code for the thread

    Return value:

    This function never returns.
*/
EXTERN void
qthread_exit(qthread_return_t exit_code);

/*
    Name:   qthread_getschedparam

    Description:

    This function returns the scheduler parameters of the given thread, unlike
    the qthread_attr_getschedparam function, which returns the scheduler parameter
    defined in a qthread_attr_t structure.

    The scheduler parameters are defined in quanser_scheduler.h. The only
    scheduler parameter currently used is the sched_priority, which defines
    the priority of the thread. The scheduler parameters are returned in a 
    qsched_param_t structure. The priority will be in  the range of priorities 
    returned by the scheduler functions qsched_get_priority_min and 
    qsched_get_priority_max, which get the minimum and maximum priorities 
    for a given scheduler policy.

    Parameters:

    thread  = the handle of the thread whose scheduler parameters are to be obtained
    param   = the address of a qsched_param_t structure that will be filled
              with the scheduler parameters of the given thread

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_getschedparam(qthread_t thread, int * policy, qsched_param_t * param);

/*
    Name:   qthread_setschedparam

    Description:

    This function sets the scheduler parameters of the given thread, unlike
    the qthread_attr_setschedparam function, which configures the scheduler 
    parameters in a qthread_attr_t structure. The qthread_setschedparam
    function may be used to change the priority or scheduler policy of
    an existing thread.

    Scheduler policies are defined in quanser_scheduler.h. The
    default policy is QSCHED_FIFO. Not all scheduler policies are valid on
    all QUARC targets.

    The scheduler parameters are also defined in quanser_scheduler.h. The only
    scheduler parameter currently used is the sched_priority, which defines
    the priority of the thread. The scheduler parameters are passed in a 
    qsched_param_t structure. The priority must be in  the range of priorities 
    returned by the scheduler functions qsched_get_priority_min and 
    qsched_get_priority_max, which get the minimum and maximum priorities 
    for a given scheduler policy.

    Parameters:

    thread  = the handle of the thread whose scheduler parameters will be set
    policy  = the scheduler policy to use for the thread
    param   = the address of a qsched_param_t structure that must be filled
              in with the desired scheduler parameters

    Return value:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_setschedparam(qthread_t thread, int policy, const qsched_param_t * param);

/*
    Description:

    Sets the affinity mask for the given thread. The only
    thread currently supported is the current thread, as returned
    by qthread_self(). 
    
    This function restricts the set of CPUs upon which the thread
    may run. The affinity mask of the thread must be a subset of 
    the affinity mask for the process to which the thread belongs.

    Parameters:

    thread       = the thread handle of the thread whose affinity mask 
                   is being set. Currently only the current thread is supported.
    cpu_set_size = the size of the pass qcpu_set_t structure in bytes. Always
                   pass sizeof(qcpu_set_t).
    set          = the set of CPUs upon which the thread may run. Use the
                   QCPU_XXXX macros to define the CPUs in the set.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN int
qthread_setaffinity(qthread_t thread, size_t cpu_set_size, const qcpu_set_t * set);

/*
    Description:

    Gets the resource usage of the current thread. Presently only the
    CPU times spent in user-mode and kernel-mode are returned.

    To get the total resource usage for the process, see process_getrusage
    in quanser_process.h.

    Parameters:

    usage = pointer to a t_resource_usage structure in which the usage
            information will be stored. See quanser_process.h for details.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_getrusage(t_resource_usage * usage);

/*
    Description:

    The first thread to call qthread_once with a given once_control will
    call init_routine. Subsequent calls to qthread_once with the same once_control
    will not call the init_routine. On return from qthread_once it is
    guaranteed that init_routine has been called.

    The once_control argument must be initialized with QTHREAD_ONCE_INIT
    prior to calling this function.

    Parameters:

    once_control = pointer to a qthread_once_t structure that has been initialized
                   to QTHREAD_ONCE_INIT.
    init_routine = function pointer of the callback to invoke once.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_once(qthread_once_t * once_control, qthread_once_callback_t init_routine);

/*
    Description:

    Creates a key for accessing a thread-local storage slot. The key is used
    with the qthread_setspecific and qthread_getspecific to access storage
    local to each thread.

    If a destructor is provided (non-NULL) then it is invoked when the thread
    exits to clean up any resources stored referenced by the thread local storage
    slot, such as dynamically allocated memory.

    Parameters:

    key        = pointer to a qthread_key_t variable that will be initialized with
                 the key for the thread-local storage slot.
    destructor = function pointer of the destructor to invoke when the thread exits.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_key_create(qthread_key_t * key, qthread_key_destructor_t destructor);

/*
    Description:

    Deletes a key for accessing a thread-local storage slot. The destructor
    for key will not be called if the value stored in the slot is NULL. Otherwise
    it *may* be called. Hence, the caller should ensure that all threads are no
    longer using the slot before calling qthread_key_delete and that the value is
    NULL.

    Parameters:

    key = the qthread_key_t variable containing the
          key for the thread-local storage slot.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_key_delete(qthread_key_t key);

/*
    Description:

    Sets the value associated with a thread-local storage key
    for the current thread.

    Parameters:

    key   = the qthread_key_t variable containing the
            key for the thread-local storage slot.
    value = the value to store in thread-local storage.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN t_error
qthread_setspecific(qthread_key_t key, const void * value);

/*
    Description:

    Gets the value associated with a thread-local storage key
    for the current thread.

    Parameters:

    key   = the qthread_key_t variable containing the
            key for the thread-local storage slot.

    Return values:

    Returns the value retrieved from thread-local storage or NULL
    if no data is stored in the slot for the current thread.
*/
EXTERN void *
qthread_getspecific(qthread_key_t key);

/*
    Description:

    Sets the cancelability state of the calling thread. If the
    state is set to QTHREAD_CANCEL_ENABLE then the thread is
    cancelable, which is the default state. If the state is
    set to QTHREAD_CANCEL_DISABLE then the thread is not
    cancelable. If a cancellation request is received it is
    blocked until cancelability is enabled.

    Parameters:

    state     = the new cancelability state
    old_state = a pointer to a variable to receive the old
                cancelability state. This argument may be NULL.

    Return values:

    Returns 0 on success and a negative error code on failure.
*/
EXTERN t_error
qthread_setcancelstate(int state, int * old_state);

#endif
