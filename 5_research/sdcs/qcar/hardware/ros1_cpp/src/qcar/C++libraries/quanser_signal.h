#if !defined(_quanser_signal_h)
#define _quanser_signal_h

#include "quanser_errors.h"
#include "quanser_runtime.h"
#include <signal.h>

#if defined(_WIN32)

#define QSIG_BLOCK      0
#define QSIG_UNBLOCK    1
#define QSIG_SETMASK    2

typedef struct tag_qsigset
{
    t_uint32 signal_mask;
} qsigset_t;

typedef struct tag_qsigaction
{
    void (* sa_handler)(int signum);    /* may be SIG_DFL, SIG_IGN or address of a signal handler function */
    qsigset_t sa_mask;                  /* ignored */
    int sa_flags;                       /* ignored */
} qsigaction_t;

#else

#define SIGBREAK        SIGTERM

#define QSIG_BLOCK      SIG_BLOCK
#define QSIG_UNBLOCK    SIG_UNBLOCK
#define QSIG_SETMASK    SIG_SETMASK

typedef sigset_t qsigset_t;
typedef struct sigaction qsigaction_t;

#endif

EXTERN t_error
qsigemptyset(qsigset_t * set);

EXTERN t_error
qsigfillset(qsigset_t * set);

EXTERN t_int
qsigismember(const qsigset_t * set, int signal_number);

EXTERN t_error
qsigaddset(qsigset_t * set, int signal_number);

EXTERN t_error
qsigdelset(qsigset_t * set, int signal_number);

EXTERN t_error
qsigaction(int signum, const qsigaction_t * action, qsigaction_t * old_action);

EXTERN t_error
qthread_sigmask(int how, const qsigset_t * set, qsigset_t * old_set);

EXTERN t_error
qraise(int signal_number);

#endif
