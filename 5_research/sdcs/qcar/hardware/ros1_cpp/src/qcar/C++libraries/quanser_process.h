#if !defined(_quanser_process_h)
#define _quanser_process_h

#include "quanser_runtime.h"
#include "quanser_time.h"

#if defined(_WIN32)

typedef struct tag_qpid * qpid_t;

#else

#if defined(__QNX__)
#include <process.h>
#elif defined(__linux) || defined(__APPLE__) || defined(__vxworks)
#include <sys/types.h>
#endif

#if !defined(__vxworks)
#include <sys/time.h>
#endif

#include <sys/resource.h> 

typedef pid_t qpid_t;

#endif

typedef struct tag_resource_usage
{
    t_timeout user_time;
    t_timeout system_time;
} t_resource_usage;

/*
    Description:

    Returns a process identifier corresponding to the current process.
    Note that in some operating systems, the qpid_t type actually
    corresponds to a process "handle". Hence, the getqpid() function
    must be used to get the process identifier for the current process
    because a value of 0 for a qpid_t does not necessarily correspond to
    the current process.

    Parameters:

    none

    Return values:

    Returns the process identifier. It always succeeds.
*/
EXTERN qpid_t
getqpid(void);

#define process_get_id()  getqpid()

/*
    Description:

    Returns a structure containing information about the CPU usage
    of the process. It is similar to the POSIX getrusage() function
    except that it returns less information in order to remain
    portable across different operating systems.

    Parameters:

    usage - pointer to a structure it fills in with CPU usage information

    Return values:

    Returns zero on success and a negative error code on failure.
*/
EXTERN t_error
process_getrusage(t_resource_usage * usage);

#endif
