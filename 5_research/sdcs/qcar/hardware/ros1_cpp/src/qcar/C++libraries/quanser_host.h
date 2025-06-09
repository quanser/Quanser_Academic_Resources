#if !defined(_quanser_host_h)
#define _quanser_host_h

#include "quanser_extern.h"
#include "quanser_errors.h"
#include "quanser_thread.h"

typedef enum tag_host_command
{
    HOST_COMMAND_INVALID,       /* avoid zero as a command for additional error checking */
    HOST_COMMAND_LOAD,
    HOST_COMMAND_SET_PROPERTY
} t_host_command;

typedef struct tag_host_command_header
{
    t_uint32 peripheral_id;
    t_uint32 command;
} t_host_command_header;

typedef struct tag_host_data_header
{
    t_uint32 peripheral_id;
    t_uint32 data_length;       /* should not exceed 2^31-1 (i.e. INT_MAX) */
} t_host_data_header;

typedef enum tag_host_state
{
    HOST_STATE_NOT_LISTENING,
    HOST_STATE_NOT_CONNECTED,
    HOST_STATE_CONNECTED
} t_host_state;

typedef struct tag_host_status
{
    t_error error_status;
    t_host_state connection_status; /* TODO: make enumerated type */
} t_host_status;

typedef struct tag_host_remote_interface * t_host_remote_interface;
typedef t_error (* t_host_remote_interface_connect_function)(t_host_remote_interface host, void * context);
typedef t_error (* t_host_remote_interface_receive_function)(t_host_remote_interface host, void * context, t_uint32 peripheral_id, const void * data, t_uint32 data_length);
typedef t_error (* t_host_remote_interface_disconnect_function)(t_host_remote_interface host, void * context);

EXTERN t_error
host_remote_interface_open(const char * uri, t_host_remote_interface_connect_function connect_function, t_host_remote_interface_receive_function receive_function,
                           t_host_remote_interface_disconnect_function disconnect_function, t_int send_buffer_size, t_int receive_buffer_size,
                           const qthread_attr_t * attributes, void * context, t_host_remote_interface * host);

EXTERN t_error
host_remote_interface_get_status(t_host_remote_interface host, t_host_status * status);

EXTERN t_error
host_remote_interface_send(t_host_remote_interface host, const void * buffer, t_uint32 buffer_length);

EXTERN t_error
host_remote_interface_close(t_host_remote_interface host);

#endif
