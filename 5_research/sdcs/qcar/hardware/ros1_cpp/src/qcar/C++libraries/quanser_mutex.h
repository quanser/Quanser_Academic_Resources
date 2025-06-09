#if !defined(_quanser_mutex_h)
#define _quanser_mutex_h

#include "quanser_extern.h"
#include "quanser_errors.h"
#include "quanser_types.h"

#if defined(_WIN32)

typedef struct tag_qthread_mutexattr
{
    int flags;
} qthread_mutexattr_t;

typedef struct tag_qthread_mutex * qthread_mutex_t;

#else

#include <pthread.h>

typedef pthread_mutexattr_t  qthread_mutexattr_t;
typedef pthread_mutex_t      qthread_mutex_t;

#endif

/* 
** Initializes an unnamed mutex. The mutex should be free using qthread_mutex_destroy.
*/
EXTERN t_error
qthread_mutex_init(qthread_mutex_t * mutex, const qthread_mutexattr_t * attributes);

/*
** Description:
**
** Creates or opens a named mutex. The named mutex may be shared across processes.
** If the exclusive flag is set then a -QERR_MUTEX_ALREADY_EXISTS error will be returned
** if the mutex already exists. Otherwise the mutex will be opened. The name should always
** begin with a forward slash and should not be more than 255 characters long.
**
** The mutex should be closed using qthread_mutex_close when it
** is no longer in use.
**
** Parameters:
**
** mutex     = a pointer to the qthread_mutex_t * variable in which a pointer to the mutex
**             will be stored.
** name      = the name of the mutex. It must begin with a '/' character.
** exclusive = whether to create the mutex if it already exists
**
** Return value:
**
** Returns 0 on success. If an error occurs then a negative error code is returned.
*/
EXTERN t_error
qthread_mutex_create(qthread_mutex_t ** mutex, const char * name, t_boolean exclusive);

/*
** Locks the mutex. It returns 0 on success and a negative error code otherwise.
** The one exception is for a named mutex that was locked by a thread that terminated.
** In that case, the return value is -QERR_MUTEX_ABANDONED and the mutex will be 
** owned by the caller. However, the caller should check for consistency of the shared
** resource protected by the mutex.
*/
EXTERN t_error
qthread_mutex_lock(qthread_mutex_t * mutex);

/* Unlocks the mutex */
EXTERN t_error
qthread_mutex_unlock(qthread_mutex_t * mutex);

/* Destroys a mutex. Do not use this function with named mutexes */
EXTERN t_error
qthread_mutex_destroy(qthread_mutex_t * mutex);

/* Closes a named mutex */
EXTERN t_error
qthread_mutex_close(qthread_mutex_t * mutex);

#endif
