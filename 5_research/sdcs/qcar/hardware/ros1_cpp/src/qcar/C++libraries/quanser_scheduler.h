#if !defined(_quanser_scheduler_h)
#define _quanser_scheduler_h

#include "quanser_runtime.h"
#include "quanser_inline.h"
#include "quanser_types.h"
#include "quanser_process.h"

/* 
    Scheduler Policies

    QUARC defines up to three different scheduler policies:

        QSCHED_FIFO     = threads of equal priority are executed on a first-come first-serve basis
        QSCHED_RR       = threads of equal priority are executed in a round-robin ordering
        QSCHED_OTHER    = an operating system specific policy is to be used
        QSCHED_REALTIME = specific to Mac OS X. Allows actual computation time to be requested. 

    Not all scheduler policies are supported on all platforms.
*/

/*
    Name:   QCPU_ZERO

    Description:

    Initializes a qcpu_set_t structure. This macro must be called
    to initialize a qcpu_set_t structure before any of the other QCPU
    macros are called. It initializes the set of CPUs to be empty.
    
    The qcpu_set_t structure defines a set of CPUs. It is used to
    set the CPU affinity of a process or thread so that the thread, or
    threads of the process, will only run on the specified CPUs.
    
    Parameters:

    set = the set of CPUs to initialize.

    Return values:

    This function has no return value.
*/

/*
    Name:   QCPU_SET

    Description:

    Adds a CPU to the set of CPUs defined by a qcpu_set_t structure.
    CPUs are numbered starting at zero.
    
    The qcpu_set_t structure defines a set of CPUs. It is used to
    set the CPU affinity of a process or thread so that the thread, or
    threads of the process, will only run on the specified CPUs.
    
    Parameters:

    cpu = the number of the CPU to add to the set
    set = the set of CPUs to modify.

    Return values:

    This function has no return value.
*/

/*
    Name:   QCPU_CLR

    Description:

    Removes a CPU from the set of CPUs defined by a qcpu_set_t structure.
    CPUs are numbered starting at zero.
    
    The qcpu_set_t structure defines a set of CPUs. It is used to
    set the CPU affinity of a process or thread so that the thread, or
    threads of the process, will only run on the specified CPUs.
    
    Parameters:

    cpu = the number of the CPU to remove from the set
    set = the set of CPUs to modify.

    Return values:

    This function has no return value.
*/

/*
    Name:   QCPU_ISSET

    Description:

    Indicates whether a CPU belongs to the set of CPUs defined by a 
    qcpu_set_t structure. CPUs are numbered starting at zero.
    
    The qcpu_set_t structure defines a set of CPUs. It is used to
    set the CPU affinity of a process or thread so that the thread, or
    threads of the process, will only run on the specified CPUs.
    
    Parameters:

    cpu = the number of the CPU to check
    set = the set of CPUs to check

    Return values:

    Returns a non-zero value if the CPU is in the set. Otherwise
    it returns zero.
*/

#if defined(UNDER_RTSS)

#define QSCHED_FIFO     0
#define QSCHED_RR       1
#define QSCHED_OTHER    QSCHED_RR

#elif defined(_WIN32)

#define QSCHED_FIFO     0
#define QSCHED_OTHER    QSCHED_FIFO

#else

#include <sched.h>

#define QSCHED_FIFO     SCHED_FIFO
#define QSCHED_RR       SCHED_RR
#define QSCHED_OTHER    SCHED_OTHER

#if defined(__APPLE__ALT__)
#define QSCHED_REALTIME (__SCHED_PARAM_SIZE__ + 1)
#endif

#endif

typedef struct qsched_param
{
    int sched_priority;
    
#if defined(__APPLE__ALT__)
    int period;             /* period at which to repeatedly run real-time thread, in nanoseconds */
    int computation;        /* amount of computation time needed by the real-time thread each period, in nanoseconds */
    int constraint;         /* amount of time within the period over which computation time may be spread, in nanoseconds */
    char preemptible;       /* whether the real-time thread may be preempted during its computation (but still maintaining constraint) */
#endif
} qsched_param_t;

#if defined(__linux)

typedef cpu_set_t  qcpu_set_t;
#define QCPU_ZERO  CPU_ZERO
#define QCPU_SET   CPU_SET
#define QCPU_CLR   CPU_CLR
#define QCPU_ISSET CPU_ISSET

#else

/* 
    For now, assume there are no more than 32 processors.
    However, use the form of sched and pthread affinity
    functions that support many more processors (more than
    1024 processors) to make future expansion easier and
    use a structure for the same reason. On Linux, we
    can use the actual cpu_set_t structure and put conditional
    code in the various macros and functions that we
    have defined in quanser_runtime that use this structure.
*/
typedef struct tag_qcpu_set
{
    t_uint mask;
} qcpu_set_t;

INLINE void
QCPU_ZERO(qcpu_set_t * set)
{
    set->mask = 0;
}

INLINE void
QCPU_SET(int cpu, qcpu_set_t * set)
{
    set->mask |= (1 << cpu);
}

INLINE void
QCPU_CLR(int cpu, qcpu_set_t * set)
{
    set->mask &= ~(1 << cpu);
}

INLINE int
QCPU_ISSET(int cpu, const qcpu_set_t * set)
{
    return ((set->mask & (1 << cpu)) != 0);
}

#endif

typedef enum tag_sleep_mode
{
    SLEEP_MODE_ENABLED,     /* default mode - sleeping is enabled */
    SLEEP_MODE_DISABLED     /* sleeping is disabled */
} t_sleep_mode;

/*
    Name:   qsched_setaffinity

    Description:

    Sets the process affinity mask for the given process. The only
    process currently supported is the current process, as returned
    by getqpid(). 
    
    This function restricts the set of CPUs upon which threads created
    by this process may run. The affinity mask of the current
    thread is also set. This function should be called from the main 
    thread of the process before any other threads are created because
    it is not guaranteed to set the affinity masks of threads created
    by the process prior to calling this function.

    Parameters:

    pid          = the process identifier of the process whose affinity mask 
                   is being set. Currently only the current process is supported.
    cpu_set_size = the size of the pass qcpu_set_t structure in bytes. Always
                   pass sizeof(qcpu_set_t).
    set          = the set of CPUs upon which the process may run. Use the
                   QCPU_XXXX macros to define the CPUs in the set.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN int
qsched_setaffinity(qpid_t pid, size_t cpu_set_size, const qcpu_set_t * set);

/*
    Name:   qsched_getaffinity

    Description:

    Gets the process affinity mask for the given process. The only
    process currently supported is the current process, as returned
    by getqpid(). 
    
    The process affinity mask restricts the set of CPUs upon which threads 
    created by this process may run.

    Parameters:

    pid          = the process identifier of the process whose affinity mask 
                   is being obtained. Currently only the current process is supported.
    cpu_set_size = the size of the pass qcpu_set_t structure in bytes. Always
                   pass sizeof(qcpu_set_t).
    set          = the address of a qcpu_set_t structure to receive set of CPUs 
                   upon which the process may run. Use the QCPU_ISSET macro to 
                   determine which CPUs are in the set.

    Return values:

    Returns 0 on success. Otherwise it returns a negative error code.
*/
EXTERN int
qsched_getaffinity(qpid_t pid, size_t cpu_set_size, qcpu_set_t * set);

/*
    Name:   qsched_get_priority_min

    Description:

    Returns the minimum priority defined for a particular scheduler policy.
    The default scheduler policy is SCHED_FIFO. Note that the range of
    priorities is typically different for each scheduler policy so do not
    assume otherwise. 
    
    On QUARC targets, the minimum priority is often zero, but do not depend 
    on this behaviour. It is always true that the minimum priority is always
    less than or equal to the maximum priority and higher priority numbers
    indicate higher priority.

    Use the qsched_get_priority_max function to get the maximum priority.
    
    Parameters:

    policy = the scheduler policy. Typically QSCHED_FIFO.

    Return values:

    Returns the minimum priority on success. Otherwise it returns a negative error code.
*/
EXTERN int
qsched_get_priority_min(int policy);

/*
    Name:   qsched_get_priority_max

    Description:

    Returns the maximum priority defined for a particular scheduler policy.
    The default scheduler policy is SCHED_FIFO. Note that the range of
    priorities is typically different for each scheduler policy so do not
    assume otherwise. 
    
    On QUARC targets, the maximum priority varies widely. Hard real-time targets
    often have 128 priority levels or more. The soft real-time Windows target
    only has 16 priority levels.

    The minimum priority is always less than or equal to the maximum priority 
    and higher priority numbers indicate higher priority.

    Use the qsched_get_priority_min function to get the minimum priority.
    
    Parameters:

    policy = the scheduler policy. Typically QSCHED_FIFO.

    Return values:

    Returns the maximum priority on success. Otherwise it returns a negative error code.
*/
EXTERN int
qsched_get_priority_max(int policy);

/*
    Name:   qsched_get_num_cpus

    Description:

    Returns the number of CPUs. QUARC fully supports systems with multiple CPUs.
    This function may be used to determine the number of CPUs available to QUARC.
    Note that this number may be less than the actual number of CPUs (or more
    technically, the number of CPU cores or CPU threads) in systems where a
    hard real-time kernel such as INTime or RTX is running on the same platform
    as another operating system such as Windows and the two are configured to run
    exclusively on different CPUs.
    
    Parameters:

    This function has no parameters.

    Return values:

    Returns the number of CPUs on success. Otherwise it returns a negative error code.
*/
EXTERN int
qsched_get_num_cpus(void);

/*
    Name:   qsched_set_sleep_mode

    Description:

    Sets the sleep mode of the current thread, which can prevent the computer from
    going into a true sleep state while the thread is running.
    
    Parameters:

    The sleep mode to set. If sleeping is disabled it should be re-enabled before
    exiting the thread.

    Return values:

    Returns zero on success and a negative error code on failure.
*/
EXTERN t_error
qsched_set_sleep_mode(t_sleep_mode mode);

/*
    Name:   qsched_yield

    Description:

    Causes the calling thread to relinquish the CPU. The thread is moved to the end
    of the scheduler queue for its static priority and a new thread gets to run.
    
    Parameters:

    None.

    Return values:

    Returns zero on success and a negative error code on failure.
*/
EXTERN t_error
qsched_yield(void);

#endif
