#if !defined(_quanser_errors_h)
#define _quanser_errors_h

#include "quanser_types.h"

/*
    Error messages must ALWAYS be added to the end of the list.  NEVER add an error message
    to the middle of the list. Doing so could cause code that is already built using QUARC
    to fail when the user upgrades QUARC, or it could cause the wrong error message to be
    displayed when an error occurs. Either situation would be very confusing to the user
    who upgrades QUARC. Even if error messages would more naturally be grouped together,
    add the new error messages to the end of the list anyways. Do NOT insert an error
    message into the middle of the list.

    To create separate error messages for QUARC and QRCP, create a second comment on the
    same line for QRCP. When the error messages are generated for QRCP, this second comment
    will be used instead. See the QERR_DAQMX_CANNOT_CLEAR_TASK error message for an
    example.
*/
enum tag_error
{
    QERR_NO_ERROR,
    QERR_OUT_OF_MEMORY,                                                 /* Not enough memory to perform the operation. */
    QERR_OUT_OF_RESOURCES,                                              /* Not enough system resources are available to perform the operation. */
    QERR_OUT_OF_RANGE,                                                  /* A value is outside the valid range. */
    QERR_INVALID_ARGUMENT,                                              /* One of the arguments is invalid. */
    QERR_PAGE_FAULT,                                                    /* A page fault occurred accessing one of the arguments. */
    QERR_NOT_SUPPORTED,                                                 /* The specified option or operation is not supported. It may be supported on other platforms. Please check the documentation. */
    QERR_DEADLOCK,                                                      /* A deadlock situation would have occurred. */
    QERR_BUSY,                                                          /* An operation is already in progress. */
    QERR_OBJECT_NOT_FOUND,                                              /* The object could not be found. */
    QERR_FILE_NOT_FOUND,                                                /* The file could not be found. */
    QERR_NO_PERMISSION,                                                 /* The process lacks the appropriate privileges to perform the operation. If you are downloading a model then the model may be loaded on the target. Stop the model and download the code again. If you are uploading a MAT file then the host and target are likely the same machine and the operation would overwrite the MAT file with itself. */
    QERR_TOO_MANY_PROCESSES,                                            /* Too many processes are accessing an RTDLL. */
    QERR_UNRECOGNIZED_ERROR,                                            /* An operating system function returned an unrecognized error. */
    QERR_TIMED_OUT,                                                     /* The operation timed out. */
    QERR_LIBRARY_NOT_FOUND,                                             /* Unable to locate the dynamic link library or shared object. */
    QERR_LIBRARY_NOT_CLOSED,                                            /* Failed to close dynamic link library or shared object. */
    QERR_STRING_TOO_SMALL,                                              /* The string buffer is too small to hold the result. */
    QERR_STRING_NOT_TERMINATED,                                         /* The string is not null-terminated within the given size. */
    QERR_INVALID_URI,                                                   /* The absolute URI is not valid. */
    QERR_URI_OPTION_TOO_LONG,                                           /* The option name for a URI is too long. Option names must not be longer than URI_MAX_OPTION_LENGTH. */
    QERR_MISSING_URI_OPTION_VALUE,                                      /* The option for a URI is present but there is no associated value, as expected. */
    QERR_INVALID_URI_OPTION_VALUE,                                      /* The option for a URI is present but the value is invalid. */
    QERR_INVALID_URI_PORT_VALUE,                                        /* The port for a URI is present but the value is invalid. */
    QERR_MISSING_FUNCTION,                                              /* A required function is missing from a driver. */
    QERR_INVALID_CONNECTION,                                            /* The connection is not valid. A connection cannot be used after it has been closed. */
    QERR_NON_BLOCKING_NOT_SUPPORTED,                                    /* Non-blocking mode is not supported for the given protocol. */
    QERR_CANNOT_INITIALIZE_SOCKETS,                                     /* It was not possible to initialize the socket library. */
    QERR_NAGLE_NOT_SUPPORTED,                                           /* The Nagle algorithm is not supported for the given communication subsystem. */
    QERR_INVALID_BUFFER_SIZE,                                           /* The specified buffer size is not valid. It may be out of an acceptable range. */
    QERR_SOCKET_NOT_REUSABLE,                                           /* The socket address could not be made reusable. */
    QERR_CANNOT_BIND_SOCKET,                                            /* It was not possible to bind the socket to the given port. Check that the port number is valid and not in use. */
    QERR_CANNOT_LISTEN,                                                 /* It was not possible to listen on the specified connection. */
    QERR_CANNOT_CONNECT,                                                /* It was not possible to connect to the specified URI. */
    QERR_WOULD_BLOCK,                                                   /* A non-blocking operation would have blocked. */
    QERR_INTERRUPTED,                                                   /* A blocking operation was interrupted by a signal. */
    QERR_HOST_NOT_FOUND,                                                /* The specified host could not be found. */
    QERR_INVALID_SOCKET,                                                /* Socket is not valid. It may have been closed already or never created successfully. */
    QERR_CANNOT_LINGER,                                                 /* Unable to set the linker options for a connection. */
    QERR_CANNOT_ACCEPT_CONNECTION,                                      /* The listening socket was unable to accept a client connection. */
    QERR_CANNOT_SEND,                                                   /* Unable to send data over a connection. */
    QERR_CANNOT_RECEIVE,                                                /* Unable to receive data over a connection. */
    QERR_CANNOT_POLL,                                                   /* Unable to poll a connection. */
    QERR_CANNOT_SHUTDOWN,                                               /* Unable to shut down send and/or receives on the connection. */
    QERR_CONNECTION_SHUTDOWN,                                           /* The connection has been shut down. */
    QERR_CANNOT_CLOSE,                                                  /* Unable to close the connection. */
    QERR_CANNOT_GET_TIME,                                               /* Unable to get the current high-resolution time. */
    QERR_CANNOT_SUBTRACT_TIMEOUTS,                                      /* The timeouts cannot be subtracted because the left-hand side is relative in the right hand side is absolute. */
    QERR_CANNOT_ADD_TIMEOUTS,                                           /* The timeouts cannot be added because both sides are absolute timeouts. */
    QERR_CANNOT_OBTAIN_LOCK,                                            /* Cannot obtain a lock to gain exclusive access to a critical section of code. */
    QERR_INVALID_RECONFIGURATION,                                       /* Reconfiguration instance is not valid. It may have been closed already or never opened successfully. */
    QERR_BEGIN_CONTROL_NOT_CALLED,                                      /* The reconfiguration_begin_control function has not been called. */
    QERR_CANNOT_SWITCH,                                                 /* An attempt to switch models failed due to a communication failure. */
    QERR_INVALID_BASE,                                                  /* The given base is invalid and cannot be used to convert the integer to a string. */
    QERR_INVALID_TIMER_EVENT,                                           /* The timer event passed as an argument is invalid. */
    QERR_INVALID_TIMER_NOTIFICATION,                                    /* The timer notification structure is invalid. */
    QERR_INVALID_TIMER_RESOLUTION,                                      /* The specified timer resolution is invalid. */
    QERR_INVALID_TIMER_PERIOD,                                          /* The specified timer period is invalid. */
    QERR_INVALID_TIMER,                                                 /* The timer passed as an argument is invalid. */
    QERR_CANNOT_GET_RESOLUTION,                                         /* The timer resolution could not be retrieved. Stack or memory corruption is likely. */
    QERR_CANNOT_SET_RESOLUTION,                                         /* The timer resolution could not be set. The user does not have permission. */
    QERR_BEGIN_RESOLUTION_NOT_CALLED,                                   /* The qtimer_begin_resolution function has not been called successfully. */
    QERR_STATE_INCOMPATIBLE,                                            /* The state information is not compatible. Reconfiguration states must have the same data type and size. */
    QERR_INVALID_STATE,                                                 /* The state is invalid. It may have already been unregistered. */
    QERR_INVALID_STREAM,                                                /* The stream is not valid. A stream cannot be used after it has been closed. */
    QERR_STREAM_BUFFER_TOO_SMALL,                                       /* The stream buffer is too small to send or receive units of the given size. */
    QERR_INVALID_DPC,                                                   /* The DPC object is not valid. A DPC object cannot be used after it has been closed. */
    QERR_INVALID_METHOD,                                                /* The method code received is not valid. The DPC object should be closed. */
    QERR_INVALID_INTERFACE,                                             /* The interface code received is not valid. The DPC object should be closed. */
    QERR_DPC_DISCONNECTED,                                              /* The DPC connection has been closed at the peer. */
    QERR_INVALID_LOG,                                                   /* The log object is not valid. A log object cannot be used after it has been closed. */
    QERR_INVALID_SEMAPHORE,                                             /* The semaphore is not valid. A semaphore cannot be used after it has been destroyed. */
    QERR_INVALID_MUTEX,                                                 /* The mutex is not valid. A mutex cannot be used after it has been destroyed. */
    QERR_ARGUMENT_LIST_TOO_BIG,                                         /* The argument list for the model is too big. */
    QERR_FILE_NOT_EXECUTABLE,                                           /* The model specified is not executable. */
    QERR_TOO_MANY_LINKS,                                                /* Too many symbolic links or prefixes. */
    QERR_NAME_TOO_LONG,                                                 /* The length of a path or pathname component exceeds the limit. */
    QERR_NOT_DIRECTORY,                                                 /* A component of the path isn't a directory. */
    QERR_NAME_CONFLICT,                                                 /* A different kind of object with the same name appears in the global namespace. */
    QERR_INVALID_ESCAPE_SEQUENCE,                                       /* An escape sequence in a quoted string is invalid. */
    QERR_INVALID_STOP_BITS,                                             /* Stop bits option has an invalid value. It must be "1", "1.5" or "2". */
    QERR_INVALID_FLOW_CONTROL,                                          /* Invalid flow control option. Supported values are "none", "hw", "sw". */
    QERR_INVALID_PARITY,                                                /* Invalid parity option. Supported values are "none", "even", "odd", "mark", "space". */
    QERR_NOT_SOCK_STREAM,                                               /* The operation is not supported because the socket is not a SOCK_STREAM socket. */
    QERR_CANNOT_FIND_SOCKET_DRIVER,                                     /* The operation failed because the socket manager/driver could not be found. */
    QERR_NETWORK_FAILED,                                                /* The network subsystem has failed. */
    QERR_SOCKETS_NOT_INITIALIZED,                                       /* The socket library has not been initialized. */
    QERR_OPERATION_IN_PROGRESS,                                         /* A blocking socket operation is currently in progress. */
    QERR_INVALID_CARD_HANDLE,                                           /* The given t_card handle is not a valid card. In some Simulink versions, this error can arise when a HIL Initialize block is not in the same subsystem as a HIL Timebase block, due to Simulink incorrectly determining the execution order. In this case, try putting the two HIL blocks in the same subsystem. */ /* The given t_card handle is not a valid card.*/
    QERR_VERSION_ARGUMENT_IS_NULL,                                      /* The version object passed as a parameter is NULL. */
    QERR_INVALID_VERSION_ARGUMENT,                                      /* The version structure does not have the right length. */
    QERR_DRIVER_MISSING_OPEN_OR_CLOSE,                                  /* A hardware driver is missing the open and/or close function. */
    QERR_CARD_ARGUMENT_IS_NULL,                                         /* The card argument to hil_open is NULL. */
    QERR_CARD_TYPE_ARGUMENT_IS_NULL,                                    /* The card type argument to hil_open is NULL. */
    QERR_FUNCTION_NOT_SUPPORTED,                                        /* The function is not supported. */
    QERR_MISSING_ANALOG_INPUTS,                                         /* No analog input channels were specified even though the number of analog inputs is nonzero. */
    QERR_MISSING_ANALOG_OUTPUTS,                                        /* No analog output channels were specified even though the number of analog outputs is nonzero. */
    QERR_MISSING_ENCODER_INPUTS,                                        /* No encoder input channels were specified even though the number of encoder inputs is nonzero. */
    QERR_MISSING_PWM_OUTPUTS,                                           /* No PWM output channels were specified even though the number of PWM outputs is nonzero. */
    QERR_MISSING_DIGITAL_INPUTS,                                        /* No digital input channels were specified even though the number of digital inputs is nonzero. */
    QERR_MISSING_DIGITAL_OUTPUTS,                                       /* No digital outputs were specified even though the number of digital outputs is nonzero. */
    QERR_MISSING_OTHER_INPUTS,                                          /* No other input channels were specified even though the number of other inputs is nonzero. */
    QERR_MISSING_OTHER_OUTPUTS,                                         /* No other output channels were specified even though the number of other outputs is nonzero. */
    QERR_MISSING_CLOCK_INPUTS,                                          /* No clocks were specified even though the number of clocks is nonzero. */
    QERR_TASK_ARGUMENT_IS_NULL,                                         /* The task argument to a HIL function is NULL. */
    QERR_INVALID_TASK_HANDLE,                                           /* An invalid task handle was passed as an argument to a HIL function. */
    QERR_BOARD_ARGUMENT_IS_NULL,                                        /* The board argument passed to the board-specific HIL driver is NULL. This situation should never occur unless the user is calling the board-specific driver directly or memory has been corrupted. */
    QERR_UNABLE_TO_OPEN_DRIVER,                                         /* An operating system specific kernel-level driver for the card was found but could not be loaded. There may be a device conflict, hardware problem, or the driver may not be correctly installed. */
    QERR_BOARD_NOT_FOUND,                                               /* An operating system specific kernel-level driver for the specified card could not be found. The card or driver may not be installed. The kernel-level driver is the driver that gets installed when the operating system detects the hardware. Check Device Manager to see if the card is present or recognized by the operating system. Also verify that you have selected the correct card in the HIL Initialize block or hil_open function. */
    QERR_BOARD_IN_USE,                                                  /* The board is in use by another process and the board-specific driver does not support multi-process access to the card. */
    QERR_UNABLE_TO_LOCK_DEVICE,                                         /* It was not possible to get exclusive access to the device. The operation has been aborted. */
    QERR_BUFFER_OVERFLOW,                                               /* For a read operation, the buffer has overflowed. For a write operation, there is no more data left in the buffer. The sampling frequency is too fast for the rate at which data is being read from or written to the buffer. For HIL Timebase blocks or HIL tasks, oversampling has occurred. For Stream blocks, the hardware FIFO overflowed. */
    QERR_UNABLE_TO_CLOSE_DRIVER,                                        /* It was not possible to close the operating system specific kernel-level driver. The driver handle may be invalid. For example, the device may have already been closed or memory may have been corrupted. */
    QERR_INVALID_BOARD_HANDLE,                                          /* An invalid board handle was passed as an argument to the board-specific HIL driver. Once a card has been closed using hil_close the board handle is invalid. */
    QERR_OUT_OF_REQUIRED_SYSTEM_RESOURCES,                              /* There are not enough system resources to perform the requested operation. Try rebooting, requesting fewer samples, or adding more memory to your machine. */
    QERR_DRIVER_INCOMPATIBLE_WITH_BOARD_DLL,                            /* The board-specific HIL driver passed an invalid parameter to the operating system specific kernel-level driver for the board. The board-specific HIL driver is likely not compatible with the operating system specific kernel-level driver for the board. Make sure both are up-to-date and compatible versions. */
    QERR_INTERNAL_BUFFER_TOO_SMALL,                                     /* The board-specific HIL driver used an internal buffer that was too small for the operating system specific kernel-level driver for the board. The board-specific HIL driver is likely not compatible with the operating system specific kernel-level driver for the board. Make sure both are up-to-date and compatible versions. */
    QERR_ANALOG_RESOURCE_IN_USE,                                        /* The analog-to-digital converter on the HIL board is currently in use by another operation. */
    QERR_INVALID_BUFFER_HANDLE,                                         /* An invalid buffer handle was passed to a board-specific HIL driver function. */
    QERR_ANALOG_INPUT_CHANNELS_NOT_SUPPORTED,                           /* Analog input channels are not supported by this board. */
    QERR_TOO_MANY_ANALOG_INPUT_CHANNELS,                                /* Too many analog input channels were specified. */
    QERR_INVALID_ANALOG_INPUT_CHANNEL,                                  /* One of the analog input channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_ENCODER_INPUT_CHANNELS_NOT_SUPPORTED,                          /* Counter input channels are not supported by this board. */
    QERR_TOO_MANY_ENCODER_INPUT_CHANNELS,                               /* Too many encoder input channels were specified. */
    QERR_INVALID_ENCODER_INPUT_CHANNEL,                                 /* One of the encoder input channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_DIGITAL_INPUT_CHANNELS_NOT_SUPPORTED,                          /* Digital input channels are not supported by this board. */
    QERR_TOO_MANY_DIGITAL_INPUT_CHANNELS,                               /* Too many digital input channels were specified. */
    QERR_INVALID_DIGITAL_INPUT_CHANNEL,                                 /* One of the digital input channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_OTHER_INPUT_CHANNELS_NOT_SUPPORTED,                            /* Other input channels are not supported by this board. */
    QERR_TOO_MANY_OTHER_INPUT_CHANNELS,                                 /* Too many other input channels were specified. */
    QERR_INVALID_OTHER_INPUT_CHANNEL,                                   /* One of the other input channels that was specified is not a valid channel number. Channel numbers are typically divided into ranges according to functionality. Refer to the documentation for your card. */
    QERR_ANALOG_OUTPUT_CHANNELS_NOT_SUPPORTED,                          /* Analog output channels are not supported by this board. */
    QERR_TOO_MANY_ANALOG_OUTPUT_CHANNELS,                               /* Too many analog output channels were specified. */
    QERR_INVALID_ANALOG_OUTPUT_CHANNEL,                                 /* One of the analog output channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_PWM_OUTPUT_CHANNELS_NOT_SUPPORTED,                             /* PWM output channels are not supported by this board. */
    QERR_TOO_MANY_PWM_OUTPUT_CHANNELS,                                  /* Too many PWM output channels were specified. */
    QERR_INVALID_PWM_OUTPUT_CHANNEL,                                    /* One of the PWM output channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_DIGITAL_OUTPUT_CHANNELS_NOT_SUPPORTED,                         /* Digital output channels are not supported by this board. */
    QERR_TOO_MANY_DIGITAL_OUTPUT_CHANNELS,                              /* Too many digital output channels were specified. */
    QERR_INVALID_DIGITAL_OUTPUT_CHANNEL,                                /* One of the digital output channels that was specified is not a valid channel number. Channel numbers typically range from 0 to one less than the number of channels. */
    QERR_OTHER_OUTPUT_CHANNELS_NOT_SUPPORTED,                           /* Other output channels are not supported by this board. */
    QERR_TOO_MANY_OTHER_OUTPUT_CHANNELS,                                /* Too many other output channels were specified. */
    QERR_INVALID_OTHER_OUTPUT_CHANNEL,                                  /* One of the other output channels that was specified is not a valid channel number. Channel numbers are typically divided into ranges according to functionality. Refer to the documentation for your card. */
    QERR_CONFLICTING_DIGITAL_DIRECTIONS,                                /* A digital channel was specified as both an input and an output. Digital channels cannot be programmed as an input and an output at the same time. */
    QERR_CLOCK_NOT_SUPPORTED,                                           /* The specified clock is not supported by the board-specific HIL driver for this board. */
    QERR_HARDWARE_CLOCK_IN_USE,                                         /* The specified hardware clock is already in use for another operation and the board-specific HIL driver for this board does not permit sharing of the hardware clock. */
    QERR_TOO_MANY_CLOCKS,                                               /* Too many clocks were specified. */
    QERR_CLOCK_MODE_NOT_SUPPORTED,                                      /* The specified clock mode is not supported by this board. */
    QERR_PWM_MODE_NOT_SUPPORTED,                                        /* The specified PWM mode is not supported by this board. */
    QERR_CLOCK_FREQUENCY_NOT_POSITIVE,                                  /* The clock frequency specified is negative or zero. The clock frequency must be positive. */
    QERR_CLOCK_FREQUENCY_TOO_HIGH,                                      /* The clock frequency is too high for the specified clock. Try using a different clock. Hardware clocks are generally faster than the system clocks. */
    QERR_CLOCK_FREQUENCY_TOO_LOW,                                       /* The clock frequency is too low for the specified clock. Try using a different clock. System clocks are preferable for low frequencies so that hardware clocks remain available for higher frequency operations. */
    QERR_CLOCK_FREQUENCY_INVALID,                                       /* The clock frequency is invalid for the specified clock, or the clock may be unavailable. Try using a different clock frequency (usually slower) or a different clock. */
    QERR_DUTY_CYCLE_NOT_POSITIVE,                                       /* The specified duty cycle is negative and negative duty cycles are not supported by this board. */
    QERR_DUTY_CYCLE_TOO_HIGH,                                           /* The specified duty cycle is more than 100% (i.e. greater than 1.0). */
    QERR_WRONG_CLOCK_MODE,                                              /* The specified clock is multipurpose and is in the wrong mode for this operation. */
    QERR_INVALID_OPERATION_HANDLE,                                      /* An invalid operation handle was passed as an argument to the board-specific HIL driver. Once a task has been deleted using hil_task_delete the operation handle is invalid. */
    QERR_OPERATION_ARGUMENT_IS_NULL,                                    /* The operation argument to a board-specific HIL driver is NULL. This situation should never occur unless the user is calling the board-specific driver directly or memory has been corrupted. */
    QERR_INTERRUPT_VECTOR_IN_USE,                                       /* The interrupt vector required by the board is in use by another device and the board-specific HIL driver does not support sharing of the interrupt vector. */
    QERR_TOO_MANY_SAMPLES_FOR_BUFFER,                                   /* The number of samples requested in the read or write operation is more than the number of samples being buffered by the task. Increase the buffer size for the task or read or write fewer samples. */
    QERR_MISSING_ANALOG_INPUT_BUFFER,                                   /* Analog input channels have been specified but not enough buffer space has been provided for the read operation. */
    QERR_MISSING_ENCODER_INPUT_BUFFER,                                  /* Encoder input channels have been specified but not enough buffer space has been provided for the read operation. */
    QERR_MISSING_DIGITAL_INPUT_BUFFER,                                  /* Digital input channels have been specified but not enough buffer space has been provided for the read operation. */
    QERR_MISSING_OTHER_INPUT_BUFFER,                                    /* Other input channels have been specified but not enough buffer space has been provided for the read operation. */
    QERR_MISSING_ANALOG_OUTPUT_BUFFER,                                  /* Analog output channels have been specified but not enough values have been provided for the write operation. */
    QERR_MISSING_PWM_OUTPUT_BUFFER,                                     /* PWM output channels have been specified but not enough values have been provided for the write operation. */
    QERR_MISSING_DIGITAL_OUTPUT_BUFFER,                                 /* Digital output channels have been specified but not enough values have has been provided for the write operation. */
    QERR_MISSING_OTHER_OUTPUT_BUFFER,                                   /* Other output channels have been specified but not enough values have been provided for the write operation. */
    QERR_READING_FROM_WRITE_ONLY_TASK,                                  /* An attempt was made to read from a write-only task. */
    QERR_WRITING_TO_READ_ONLY_TASK,                                     /* An attempt was made to write to a read-only task. */
    QERR_PROCESS_NOT_FOUND,                                             /* The specified model process could not be found. */
    QERR_PROCESS_CANNOT_BE_STOPPED,                                     /* The specified model process could not be stopped. */
    QERR_ERROR_MESSAGE_NOT_FOUND,                                       /* An error message corresponding to the given error code could not be found. */
    QERR_PORT_IN_USE,                                                   /* Unable to listen on the specified port. The port is already in use. */
    QERR_HOST_BUSY,                                                     /* The host is too busy to accept a connection at this point in time. Try again later. */
    QERR_HOST_SHUTDOWN,                                                 /* The host was shut down during the operation. */
    QERR_CONNECTION_RESET,                                              /* The connection was reset. The remote peer may have exited without closing the connection. */
    QERR_CHANNEL_NOT_LISTENING,                                         /* The channel is not a listening channel so it cannot be used to accept connections. */
    QERR_CHANNEL_IS_LISTENING,                                          /* The channel is a listening channel so it cannot be used to send and receive data. */
    QERR_UNRECOGNIZED_BOARD_TYPE,                                       /* The specified board type is not recognized. Please install the board-specific HIL driver for this board type. */
    QERR_INVALID_PREFERENCES_ROOT,                                      /* The root node specified for preferences was invalid. */
    QERR_PREFERENCES_NODE_NOT_FOUND,                                    /* The specified preference node could not be found. */
    QERR_CANNOT_ENUMERATE_VALUES,                                       /* The values of a preferences node could not be enumerated. */
    QERR_PREFERENCES_NODE_TOO_LONG,                                     /* The path for the preferences node is too long. */
    QERR_URI_NOT_FOUND,                                                 /* The specified URI could not be found. */
    QERR_CANNOT_SET_PREFERENCES_VALUE,                                  /* The preferences value could not be set. You may not have sufficient privileges. */
    QERR_CANNOT_DELETE_PREFERENCES_VALUE,                               /* The preferences value could not be deleted. It may not exist, or you may not have sufficient privileges. */
    QERR_REMOVING_LAST_URI,                                             /* An attempt has been made to remove the last URI upon which the target is serving. To avoid leaving no means to connect to the target, the last URI may not be removed. The target must serve on at least one URI. */
    QERR_REMOVING_URI_IN_USE,                                           /* It is not possible to remove the URI associated with the current connection to the target. */
    QERR_OPERATION_PENDING,                                             /* The operation is not complete. It is still pending. This error should never be returned by any function to the user. */
    QERR_OVERSAMPLING_DETECTED,                                         /* Oversampling has been detected. The sampling rate is too fast and cannot be maintained. */
    QERR_TIMEBASE_ALREADY_REGISTERED,                                   /* A Timebase block has already been registered. Only one Timebase block may be present in the model. */
    QERR_TIMEBASE_NOT_REGISTERED,                                       /* A Timebase block has not been registered. */
    QERR_CANNOT_GET_PREFERENCES_VALUE,                                  /* The preferences value could not be retrieved. You may not have sufficient privileges. */
    QERR_INVALID_LICENSE,                                               /* The Quanser product does not have a valid license for the requested operation. For example, you may be trying to run more than one model at a time when you are only licensed for one, or your license may have expired. Run qc_get_loaded_models to see the models currently loaded and qc_stop_model to stop a model. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. Contact Quanser if you think your license may have expired or it does not suit your current needs. */
    QERR_MISSING_LICENSE_FILE,                                          /* The license file is missing. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_ETHERCAT_MASTER_NOT_FOUND,                                     /* The corresponding EtherCAT Master could not be found. Make sure that an EtherCAT Master block is present in the model. */
    QERR_CANNOT_OPEN_ETHERCAT,                                          /* Unable to open the EtherCAT device specified. Make sure the XML configuration and IP address specified are correct */
    QERR_ETHERCAT_DEVICE_IS_NULL,                                       /* A null pointer was specified instead of a valid EtherCAT device. */
    QERR_ETHERCAT_SYNC_CLIENT_IS_NULL,                                  /* The EtherCAT device does not have a synchronization client. */
    QERR_INVALID_XML_COMMENT,                                           /* An invalid comment was specified in the XML file. */
    QERR_INVALID_XML,                                                   /* Malformed XML in the XML file. */
    QERR_INVALID_XML_DOCUMENT_TYPE,                                     /* Missing document type declaration <!DOCTYPE ...> in the XML file. */
    QERR_SPACE_PRECEDES_XML_DECLARATION,                                /* Whitespace may not precede the <?xml ...> declaration in the XML file. */
    QERR_MULTIPLE_XML_ROOTS,                                            /* The XML file has more than one root element. */
    QERR_UNTERMINATED_XML_COMMENT,                                      /* A comment in the XML file was not terminated. */
    QERR_MISSING_XML_VERSION,                                           /* The version information in the <?xml ...> XML declaration is missing. */
    QERR_INVALID_XML_VERSION,                                           /* The specified XML version is not supported by this XML parser. */
    QERR_INVALID_XML_ENCODING,                                          /* The encoding information in the <?xml ...> XML declaration is not specified properly. */
    QERR_INVALID_XML_STANDALONE,                                        /* The standalone option in the <?xml ...> XML declaration is not specified properly. */
    QERR_INVALID_XML_DECLARATION,                                       /* The <?xml ...?> XML declaration is not formed correctly. */
    QERR_INVALID_XML_DECLARATION_END,                                   /* The <?xml ...?> XML declaration is not terminated correctly. */
    QERR_UNSUPPORTED_XML_MARKUP,                                        /* Markup that is currently unsupported was found in the XML file. */
    QERR_MISSING_URI_PATH,                                              /* The path component of the URI is missing. */
    QERR_INVALID_FILE_MODE,                                             /* The mode option specified for a file URI is invalid. */
    QERR_INVALID_FILE_SHARE_MODE,                                       /* The share mode option specified for a file URI is invalid. */
    QERR_NO_FILE_SIZE,                                                  /* The end of the file could not be determined. */
    QERR_CHANGE_NOTIFICATIONS_NOT_SUPPORTED,                            /* Change notifications are not supported on the specified file system. */
    QERR_WRITING_TO_READ_ONLY_STREAM,                                   /* An attempt was made to write to a read-only stream. */
    QERR_READING_FROM_WRITE_ONLY_STREAM,                                /* An attempt was made to read from a write-only stream. */
    QERR_INVALID_STREAM_FORMAT,                                         /* The character format specified for the stream is out of range. */
    QERR_ILLEGAL_UTF8_CHARACTER,                                        /* An illegal UTF-8 character was encountered in the stream. */
    QERR_ILLEGAL_UTF16_CHARACTER,                                       /* An illegal UTF-16 character was encountered in the stream. */
    QERR_ILLEGAL_UTF32_CHARACTER,                                       /* An illegal UTF-32 character was encountered in the stream. */
    QERR_XML_DECLARATION_NOT_FIRST,                                     /* An <?xml ...> declaration appears but it is not the first tag in the XML stream. */
    QERR_XML_DOCTYPE_ALREADY_PARSED,                                    /* The <!DOCTYPE ...> declaration has already appeared in the XML stream. */
    QERR_INVALID_PI_TARGET_NAME,                                        /* The name of the XML processing instruction target is invalid. */
    QERR_INVALID_XML_PROCESSING_INSTRUCTION,                            /* The XML processing instruction was invalid. */
    QERR_INVALID_XML_EXTERNAL_ID,                                       /* The external identifier in the document type declaration is invalid. */
    QERR_INVALID_DOCTYPE_NAME,                                          /* The name of the document type is invalid. */
    QERR_INVALID_XML_SYSTEM_LITERAL,                                    /* The system literal associated with the external identifier in the document type declaration is invalid. */
    QERR_INVALID_DOCTYPE_NOT_TERMINATED,                                /* The document type definition is not terminated properly. */
    QERR_INVALID_XML_ELEMENT_NAME,                                      /* The name of the XML element is invalid. Names must begin with a letter, underscore or colon. */
    QERR_INVALID_XML_ELEMENT,                                           /* An XML element is invalid. An attribute name may be invalid or it is not terminated correctly. */
    QERR_MISSING_XML_ATTRIBUTE_VALUE,                                   /* An attribute appears in an XML element tag but there is no associated value. */
    QERR_TAG_IN_XML_ATTRIBUTE_VALUES,                                   /* Tags are not allowed within attribute values. Use &lt; to put a '<' in an attribute value. */
    QERR_INVALID_XML_ENTITY_REFERENCE,                                  /* Invalid XML entity reference. Escape ampersands using &amp; to put ampersands in values. */
    QERR_INVALID_XML_CHAR_REFERENCE,                                    /* The value of the character reference is not a valid character for XML. */
    QERR_UNTERMINATED_XML_ATTRIBUTE_VALUE,                              /* An XML attribute value string is not terminated. */
    QERR_CDATA_TERMINATOR_IN_CHAR_DATA,                                 /* The CDATA termination sequence ']]>' is not allowed within XML content. */
    QERR_INVALID_XML_TAG,                                               /* An XML tag is invalid. */
    QERR_INVALID_XML_CDATA_TAG,                                         /* The XML <![CDATA[ ...]]> tag was invalid. */
    QERR_INVALID_XML_CDATA,                                             /* The contents of a CDATA section were invalid. An invalid character was detected. */
    QERR_UNTERMINATED_XML_ELEMENT,                                      /* An XML element was not terminated properly. */
    QERR_INVALID_DOM_NODE,                                              /* The DOM node is NULL or otherwise invalid. */
    QERR_INVALID_DOM_NODE_LIST,                                         /* The DOM node list is null or otherwise invalid. */
    QERR_ITEM_NOT_IN_LIST,                                              /* An attempt was made to access a node in a list to which it did not belong, or the node does not belong to a list. */
    QERR_STRING_IS_NULL,                                                /* The string buffer passed as an argument is NULL. */
    QERR_MISMATCHED_XML_ELEMENT_TAG,                                    /* An XML end tag does not match the corresponding start tag. */
    QERR_INVALID_DOM_NAMED_NODE_MAP,                                    /* The DOM named node map is null or otherwise invalid. */
    QERR_ITEM_NOT_IN_MAP,                                               /* An attempt was made to access a node in a map to which it did not belong, or the node does not belong to a map. */
    QERR_DUPLICATE_XML_ATTRIBUTE,                                       /* An XML element has more than one attribute with the same name. */
    QERR_ILLEGAL_UTF8_LEAD_CHAR,                                        /* The UTF-8 code unit is not a valid lead byte. It is a code unit that is only valid in the middle of a UTF-8 character. */
    QERR_TRUNCATED_UTF8_CHAR,                                           /* The UTF-8 character may be valid but the given length is too small to contain it. */
    QERR_ILLEGAL_UTF16_LEAD_CHAR,                                       /* The UTF-16 code unit is not a valid lead byte. It is a code unit that is only valid as a surrogate code unit. */
    QERR_TRUNCATED_UTF16_CHAR,                                          /* The UTF-16 character may be valid but the given length is too small to contain it. */
    QERR_CANNOT_START_LICENSE_MANAGER,                                  /* The Quanser license manager could not be started. */
    QERR_CANNOT_STOP_LICENSE_MANAGER,                                   /* The Quanser license manager could not be stopped. */
    QERR_TRUNCATED_UTF32_CHAR,                                          /* The UTF-32 character may be valid but the given length is too small to contain it. */
    QERR_INVALID_THREAD_AFFINITY,                                       /* The thread was assigned an affinity that does not correspond to an existing CPU or a CPU in the process affinity. */
    QERR_INVALID_PROCESS_AFFINITY,                                      /* The process was assigned an affinity that does not correspond to an existing CPU. */
    QERR_CANNOT_GET_PROCESS_AFFINITY,                                   /* The process affinity could not be determined. */
    QERR_THREAD_AFFINITY_UNAVAILABLE,                                   /* Setting the thread CPU affinity is not currently available on this platform. */
    QERR_INCOMPLETE_WRITE,                                              /* This error should never be returned. It is used internally by the Quanser Stream API. */
    QERR_PRINT_NUM_WRITTEN_IS_NULL,                                     /* The "number written" argument to a stream_print function is NULL. It must point to an appropriately-sized integer. */
    QERR_STREAM_FORMAT_NOT_DEDUCED,                                     /* The character format of the stream can only be deduced from the first bytes in the stream. */
    QERR_MISMATCHED_STREAM_FORMAT,                                      /* The character format set for the stream does not match the format indicated by the byte order mark (BOM) in the stream itself. */
    QERR_DIRECTX_NOT_INSTALLED,                                         /* Unable to use DirectX. Make sure DirectX 10.0 or above is installed. */
    QERR_NO_GAME_CONTROLLERS_ATTACHED,                                  /* There are no game controllers currently attached to the system. */
    QERR_CANNOT_ACCESS_GAME_CONTROLLER,                                 /* Unable to access game controller. */
    QERR_CANNOT_SET_GAME_CONTROLLER_FORMAT,                             /* Unable to set data format of game controller. */
    QERR_CANNOT_POLL_GAME_CONTROLLER,                                   /* Unable to poll the game controller. */
    QERR_CANNOT_GET_GAME_CONTROLLER_STATE,                              /* Unable to get the state of the game controller. */
    QERR_CANNOT_GET_MOUSE_STATE,                                        /* Unable to get the state of the mouse. */
    QERR_ETHERCAT_INVALID_BYTE_SIZE,                                    /* Invalid ByteSize field specified for EtherCAT process image. */
    QERR_INVALID_ETHERCAT_SOURCE,                                       /* Invalid Source Mac address field for the EtherCAT device. */
    QERR_INVALID_ETHERCAT_INITIALIZATION_DATA,                          /* Invalid Data field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_DATA_LENGTH,                                  /* Invalid DataLength field in an initialization or cyclic command for an EtherCAT device. */
    QERR_CANNOT_GET_BUFFER_SIZE,                                        /* It was not possible to get the buffer size. */
    QERR_CANNOT_GET_PACKET_SIZE,                                        /* It was not possible to get the maximum packet size. */
    QERR_DATAGRAM_TOO_LARGE,                                            /* The datagram received was too large for the buffer provided in the receive operation. */
    QERR_NO_DESIGNATED_PEER,                                            /* An attempt was made to send data when no connection has been established with a particular peer. For connectionless protocols like UDP the server-side must receive data from a peer before sending any data in order to establish a "connection". */
    QERR_CANNOT_INDICATE_CLOSURE,                                       /* It was not possible to indicate closure of the connection to the remote peer. */
    QERR_INVALID_PEER_OPTION,                                           /* Invalid "peer" option was specified. Valid values for the "peer" option are "one", "any", "broadcast" or "manual". */
    QERR_CANNOT_BROADCAST,                                              /* The communication protocol, such as UDP, could not be configured for broadcasting. */
    QERR_ETHERCAT_VALIDATE_DATA_WRONG_LENGTH,                           /* The Validate/Data field in an initialization command for an EtherCAT device contains data of a different size than the Data or DataLength field. */
    QERR_INVALID_ETHERCAT_VALIDATION_DATA,                              /* Invalid Validate/Data field in an initialization command for an EtherCAT device. */
    QERR_ETHERCAT_VALIDATE_MASK_WRONG_LENGTH,                           /* The Validate/DataMask field in an initialization command for an EtherCAT device contains data of a different size than the Data or DataLength field. */
    QERR_INVALID_ETHERCAT_VALIDATION_MASK,                              /* Invalid Validate/DataMask field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_TIMEOUT,                                      /* Invalid Validate/Timeout field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_BEFORE_SLAVE,                                 /* Invalid BeforeSlave field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_TRANSITION,                                   /* Invalid Transition field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_REQUIRES_FIELD,                               /* Invalid Requires field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_COMMAND,                                      /* Invalid Cmd field in an initialization or cyclic command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_LOGICAL_ADDRESS,                              /* Invalid Addr field (logical address) in an initialization or cyclic command for EtherCAT device. */
    QERR_INVALID_ETHERCAT_ADDRESS_PAGE,                                 /* Invalid Adp field (physical address page) in an initialization or cyclic command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_ADDRESS_OFFSET,                               /* Invalid Ado field (physical address offset) in an initialization or cyclic command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_COUNT,                                        /* Invalid Cnt field (working counter value) in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_RETRIES,                                      /* Invalid Retries field in an initialization command for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_START_ADDRESS,                                /* Invalid StartAddr field in the mailbox states description for an EtherCAT master. */
    QERR_INVALID_ETHERCAT_MAILBOX_SIZE,                                 /* Invalid Count field in the mailbox states description for EtherCAT master. */
    QERR_INVALID_ETHERCAT_SLAVE_ADDRESS,                                /* Invalid PhysAddr field (physical address) in the information section (Info) for an EtherCAT slave. */
    QERR_INVALID_ETHERCAT_STATE,                                        /* Invalid State field (slave state) in the cyclic commands for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_INPUT_OFFSET,                                 /* Invalid InputOffs field (offset at which a cyclic command reads from the process image) in the cyclic commands for an EtherCAT device. */
    QERR_INVALID_ETHERCAT_OUTPUT_OFFSET,                                /* Invalid OutputOffs field (offset at which a cyclic command writes to the process image) in the cyclic commands for an EtherCAT device. */
    QERR_OUT_OF_BAND_DATA_NOT_SUPPORTED,                                /* The socket does not support receiving out-of-band data in the normal stream. */
    QERR_NO_CORRESPONDING_INTERNET_ADDRESS,                             /* There is no corresponding Internet address for the given MAC address. */
    QERR_CANNOT_SET_DESCRIPTOR_FLAGS,                                   /* Unable to set the flags of a file descriptor or socket. */
    QERR_NO_ACCESS_TO_SHARED_MEMORY,                                    /* The process does not have permission to create global shared memory. On Vista and later operating systems, creation of global shared memory requires SeCreateGlobalPrivilege. This privilege is only enabled by default for administrators, services and the local system account. Try adding the local=yes option to the URI e.g. "shmem://mymem:1?local=yes". */
    QERR_SEMAPHORE_NOT_FOUND,                                           /* The named semaphore could not be found. */
    QERR_SEMAPHORE_ALREADY_EXISTS,                                      /* The named semaphore already exists. */
    QERR_NO_CORRESPONDING_NETWORK_CARD,                                 /* There is no corresponding network card for the given MAC address. */
    QERR_PATH_IN_URI,                                                   /* The given protocol does not support paths in the URI. Separate options from the hostname and port using a '?' rather than a '/', much like an HTTP query. */
    QERR_UNSUPPORTED_BAUD_RATE,                                         /* The given serial baud rate is not supported. */
    QERR_ETHERCAT_MASTER_ALREADY_RUNNING,                               /* An EtherCAT master is already running on the given MAC address. Stop the existing EtherCAT master first. */
    QERR_MISSING_CLOCK_MODES,                                           /* Clocks have been specified but not enough clock modes have been provided. */
    QERR_MISSING_ENCODER_COUNTS,                                        /* Encoder input channels have been specified but not enough encoder counts have been provided. */
    QERR_MISSING_PWM_MODES,                                             /* PWM output channels have been specified but not enough PWM modes have been provided. */
    QERR_MISSING_PWM_FREQUENCIES,                                       /* PWM output channels have been specified but not enough PWM frequencies have been provided. */
    QERR_MISSING_PWM_DUTY_CYCLES,                                       /* PWM output channels have been specified but not enough PWM duty cycles have been provided. */
    QERR_INVALID_NUMBER_OF_SAMPLES_IN_BUFFER,                           /* The number of samples in the task buffer must be greater than zero. */
    QERR_INVALID_NUMBER_OF_SAMPLES,                                     /* The number of samples requested in the read or write operation must be greater than zero. */
    QERR_ETHERCAT_DATAGRAM_TOO_LARGE,                                   /* The EtherCAT datagram to be sent is too large. Check the XML description. */
    QERR_NO_MORE_ETHERCAT_PACKETS,                                      /* The EtherCAT master puts a limit on the number of packets which may be queued for transmission. This limit has been exceeded so no more packets are available. */
    QERR_INVALID_ETHERCAT_CYCLIC_COMMAND,                               /* The EtherCAT process image either could not be created or is not large enough for one of the cyclic command specified in the XML. */
    QERR_AUTOPILOT_ARGUMENT_IS_NULL,                                    /* The autopilot argument to val_open is NULL. */
    QERR_AUTOPILOT_TYPE_ARGUMENT_IS_NULL,                               /* The autopilot type argument to val_open is NULL. */
    QERR_INVALID_AUTOPILOT_HANDLE,                                      /* The given t_autopilot handle is not a valid autopilot. */
    QERR_URI_HOSTNAME_TOO_LONG,                                         /* The hostname specified in the URI is too long. */
    QERR_URI_SCHEME_TOO_LONG,                                           /* The scheme specified in the URI is too long. */
    QERR_INVALID_CHANNEL,                                               /* The given t_channel handle is not valid. */
    QERR_ARCNET_NODE_ID_OUT_OF_BOUNDS,                                  /* The given ARCNET node ID is out of bounds (0-255). */
    QERR_ARCNET_CANNOT_OPEN,                                            /* Cannot open and initialize the ARCNET board. */
    QERR_ARCNET_TARGET_NODE_DNE,                                        /* The ARCNET message cannot be sent because there is no node on the network with the given target node ID. */
    QERR_ARCNET_EXCESSIVE_NAKS,                                         /* The ARCNET transmission failed due to excessive NAKs. */
    QERR_ETHERCAT_PACKET_LOST,                                          /* An EtherCAT packet that was sent was lost and never returned. The slave device was not ready. */
    QERR_ETHERCAT_TELEGRAM_LOST,                                        /* An EtherCAT telegram that was sent within a packet was not present in the packet when the packet returned. Data corruption has occurred! */
    QERR_INVALID_ETHERCAT_FRAME_LENGTH,                                 /* The telegrams within an EtherCAT packet do not fit within the EtherCAT frame. Packet is corrupted! */
    QERR_ETHERCAT_COMMAND_TIMED_OUT,                                    /* An EtherCAT slave did not respond as expected within the timeout interval. */
    QERR_INVALID_ETHERCAT_TELEGRAM_LENGTH,                              /* An EtherCAT telegram received from a slave was a different size than the telegram originally sent. Telegram is corrupted! */
    QERR_INVALID_ETHERCAT_MASTER_STATE,                                 /* EtherCAT master cannot be set to the state requested. The state is not valid for the master. */
    QERR_INVALID_THREAD,                                                /* The given thread handle is not valid. */
    QERR_CANNOT_INITIALIZE_PA10,                                        /* The PA10 cannot be properly initialized due to an error. */
    QERR_CANNOT_CLOSE_PA10,                                             /* An error occurred while attempting to stop and close the PA10. */
    QERR_PGR_CANNOT_INITIALIZE_CAMERA,                                  /* An error occurred while attempting to initialize the PGR camera. */
    QERR_PGR_CANNOT_GRAB_IMAGE,                                         /* An error occurred while attempting to grab an image using the PGR camera. */
    QERR_PGR_GRAB_IMAGE_TIMEOUT,                                        /* A timeout occurred while attempting to grab an image using the PGR camera. */
    QERR_PGR_CANNOT_CLOSE,                                              /* An error occurred while attempting to close the PGR camera. */
    QERR_PGR_INVALID_CUSTOM_IMAGE_SIZE,                                 /* Starting the camera failed because the custom image size is invalid. */
    QERR_PGR_INVALID_IMAGE_DIMS,                                        /* The dimensions of the image are not valid. The image must have 3 dimensions. */
    QERR_IMAGE_CANNOT_CONVERT,                                          /* An error occurred attempting to convert the source image. */
    QERR_MISSING_ETHERCAT_COMMAND,                                      /* Missing Cmd node within an InitCmd in EtherCAT XML configuration file. The Cmd node identifies the EtherCAT command and is a required field. */
    QERR_MISSING_ETHERCAT_LOGICAL_ADDRESS,                              /* Missing Addr node within an InitCmd in EtherCAT XML configuration file. The Addr node identifies the logical address and is a required field when a LRD, LWR or LRW command is used. */
    QERR_MISSING_ETHERCAT_ADDRESS_PAGE,                                 /* Missing Adp node within an InitCmd in EtherCAT XML configuration file. The Adp node identifies the address page and is a required field when a command other than LRD, LWR or LRW is used. */
    QERR_MISSING_ETHERCAT_ADDRESS_OFFSET,                               /* Missing Ado node within an InitCmd in EtherCAT XML configuration file. The Ado node identifies the address offset and is a required field when a command other than LRD, LWR or LRW is used. */
    QERR_MISSING_ETHERCAT_COMMENT,                                      /* Missing Comment node within an InitCmd in EtherCAT XML configuration file. The Comments node provides information about the command and is a required field. */
    QERR_MISSING_ETHERCAT_DATA,                                         /* Missing Data or DataLength node within an InitCmd in EtherCAT XML configuration file. Either the Data node or the DataLength node is required because they provide the data for the command. */
    QERR_MISSING_ETHERCAT_VALIDATE_DATA,                                /* Missing Data node within the Validate section of an InitCmd in EtherCAT XML configuration file. The Data node provides the data used to validate the response from the slaves and is a required field in the Validate section. */
    QERR_MISSING_ETHERCAT_TRANSITION,                                   /* Missing Transition node within an InitCmd in EtherCAT XML configuration file. The Transition nodes indicate the state transitions forward to the command should be executed and is a required field. */
    QERR_MISSING_ETHERCAT_RETRIES,                                      /* Missing Retries node within an InitCmd in EtherCAT XML configuration file. The Retries node indicates how many times the EtherCAT stack attempts to resend the command and is a required field. */
    QERR_MISSING_ETHERCAT_SLAVE_INFO,                                   /* Missing Info node within a Slave in EtherCAT XML configuration file. The Info node includes information about the slave and is a required field. */
    QERR_MISSING_ETHERCAT_SLAVE_COMMANDS,                               /* Missing InitCmds section within a Slave in EtherCAT XML configuration file. The InitCmds section includes all the EtherCAT initialization commands for the slave and is required. */
    QERR_MISSING_ETHERCAT_SLAVE_COMMAND,                                /* Missing InitCmd node within a Slave in EtherCAT XML configuration file. The InitCmd node identifies an EtherCAT initialization command for a slave and is required. */
    QERR_MISSING_ETHERCAT_SLAVE_NAME,                                   /* Missing Name node within a Slave in EtherCAT XML configuration file. The Name node identifies the name of the slave and is required. */
    QERR_MISSING_ETHERCAT_CYCLIC_STATE,                                 /* Missing State node within a cyclic Cmd node in EtherCAT XML configuration file. The State nodes identify the states in which the cyclic command should be sent and one is required. */
    QERR_MISSING_ETHERCAT_MASTER_INFO,                                  /* Missing Info node within the Master section of an EtherCAT XML configuration file. The Info node includes information about the master and is a required field. */
    QERR_MISSING_ETHERCAT_MASTER_SOURCE,                                /* Missing Source node within the Master section of an EtherCAT XML configuration file. The Source node identifies the Mac address to be used by the master and is a required field. */
    QERR_MISSING_ETHERCAT_MASTER_COMMANDS,                              /* Missing InitCmds section within the Master section of an EtherCAT XML configuration file. The InitCmds section includes all the EtherCAT initialization commands for the master and is required. */
    QERR_MISSING_ETHERCAT_MASTER_COMMAND,                               /* Missing InitCmd node within the Master section of an EtherCAT XML configuration file. The InitCmd node identifies an EtherCAT initialization command for the master and is required. */
    QERR_MISSING_ETHERCAT_MAILBOX_START_ADDRESS,                        /* Missing StartAddr node within the MailboxStates section of an EtherCAT XML configuration file. The StartAddr node identifies the starting address of the mailbox and is required. */
    QERR_MISSING_ETHERCAT_MAILBOX_COUNT,                                /* Missing Count node within the MailboxStates section of an EtherCAT XML configuration file. The Count node identifies the length of the mailbox and is required. */
    QERR_MISSING_ETHERCAT_CONFIGURATION,                                /* Missing Config node within the EtherCAT XML configuration file. The Config node identifies the EtherCAT configuration and is required. */
    QERR_MISSING_ETHERCAT_SLAVE,                                        /* Missing Slave node within the EtherCAT XML configuration file. The Slave node identifies an EtherCAT Slave and at least one is required. */
    QERR_MISSING_ETHERCAT_MASTER,                                       /* Missing Master node within the EtherCAT XML configuration file. The Master node identifies the EtherCAT master and is required. */
    QERR_MISSING_ETHERCAT_PROCESS_IMAGE,                                /* Missing ProcessImage node within the EtherCAT XML configuration file. The ProcessImage node describes the EtherCAT process image configuration and is required. */
    QERR_MISSING_ETHERCAT_PROCESS_INPUTS,                               /* Missing Inputs node within the ProcessImage section of the EtherCAT XML configuration file. The Inputs node describes the EtherCAT input process image and is required. */
    QERR_MISSING_ETHERCAT_PROCESS_INPUTS_SIZE,                          /* Missing ByteSize node within the ProcessImage/Inputs section of the EtherCAT XML configuration file. The ByteSize node describes the size of the EtherCAT input process image and is required. */
    QERR_MISSING_ETHERCAT_PROCESS_OUTPUTS,                              /* Missing Outputs node within the ProcessImage section of the EtherCAT XML configuration file. The Outputs node describes the EtherCAT output process image and is required. */
    QERR_MISSING_ETHERCAT_PROCESS_OUTPUTS_SIZE,                         /* Missing ByteSize node within the ProcessImage/Outputs section of the EtherCAT XML configuration file. The ByteSize node describes the size of the EtherCAT output process image and is required. */
    QERR_NO_DYNAMIC_RECONFIGURATION_LICENSE,                            /* You do not have a valid license for the Dynamic Reconfiguration blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_COMMUNICATIONS_LICENSE,                                     /* You do not have a valid license for the Quanser Communications blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_ETHERCAT_LICENSE,                                           /* You do not have a valid license for the EtherCAT blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_CANNOT_OPEN_LICENSE_FILE,                                      /* Unable to open license file. Make sure that the file exists and you have permission to read the license file. Mapped network drives are not accessible with elevated privileges. Use the full UNC path, such as "\\server\licenses\john-doe.qlic", instead. */
    QERR_INVALID_LICENSE_FILE,                                          /* The license file is invalid. Choose a different license file. */
    QERR_CANNOT_CREATE_PREFERENCES_NODE,                                /* It was not possible to create the preferences node. You may not have sufficient privileges. */
    QERR_MISSING_ANALOG_MINIMUMS,                                       /* No analog minimums were specified when setting the analog ranges, even though the number of channels indicated was non-zero. */
    QERR_MISSING_ANALOG_MAXIMUMS,                                       /* No analog maximums were specified when setting the analog ranges, even though the number of channels indicated was non-zero. */
    QERR_CANNOT_READ_SCHUNK_GRIPPER,                                    /* An error occurred while attempting to read the state of the SCHUNK gripper. */
    QERR_SCHUNK_CANNOT_INIT,                                            /* An error occurred initializing the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_HALT,                                            /* Cannot halt the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_CLOSE,                                           /* An error occurred while attempting to close the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_MOVE_POS,                                        /* An error occurred attempting to issue a move command to the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_MOVE_VEL,                                        /* An error occurred attempting to issue a velocity command to the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_MOVE_CUR,                                        /* An error occurred attempting to issue a current command to the SCHUNK gripper device. */
    QERR_SCHUNK_CANNOT_HOME,                                            /* Cannot home the SCHUNK gripper device. */
    QERR_SCHUNK_INVALID_CONTROL_MODE,                                   /* The specified control mode for the Schunk gripper is invalid. */
    QERR_SCHUNK_EXT_MODE_NOT_CONNECTED,                                 /* The 'mode' input signal must be connected when the Control mode external parameter is set. */
    QERR_INVALID_ANALOG_INPUT_RANGE,                                    /* One of the ranges specified for an analog input channel is not valid for the selected hardware. */
    QERR_INVALID_ANALOG_OUTPUT_RANGE,                                   /* One of the ranges specified for an analog output channel is not valid for the selected hardware. */
    QERR_CARD_IDENTIFIER_ARGUMENT_IS_NULL,                              /* The card identifier argument to hil_open is NULL. */
    QERR_BOARD_IDENTIFIER_ARGUMENT_IS_NULL,                             /* The board identifier argument passed to the board-specific HIL driver is NULL. This situation should never occur unless the user is calling the board-specific driver directly or memory has been corrupted. */
    QERR_INVALID_BOARD_IDENTIFIER,                                      /* The board identifier is not valid. The zero-based index of the board is typically used as the board identifier, although NI boards may also be identified by their name in MAX. */
    QERR_INVALID_DEVICE_HANDLE,                                         /* The handle to the device is invalid. */
    QERR_CANNOT_OPEN_DRIVER_DIRECTORY,                                  /* An attempt to get the driver directory failed. */
    QERR_WIIMOTE_WRITE_REPORT_FAILED,                                   /* An attempt to write the wiimote report failed. */
    QERR_WIIMOTE_CANNOT_CALIBRATE,                                      /* Failed to read calibration information from the wiimote. Make sure the wiimote is on and connected to the receiving device. */
    QERR_WIIMOTE_CANNOT_OPEN,                                           /* Failed to open a connection to the wiimote. */
    QERR_WIIMOTE_READ_FAILED,                                           /* A wiimote read request failed. */
    QERR_WIIMOTE_NOT_FOUND,                                             /* Unable to find the wiimote with the specified wiimote number. Make sure the wiimote number is valid and that the wiimote is powered on and connected. */
    QERR_INVALID_WIIMOTE_DEVICE_HANDLE,                                 /* Unable to open a handle to the wiimote device. The wiimote is possibly already opened by another process. */
    QERR_DAQMX_CANNOT_CLEAR_TASK,                                       /* DAQmx was unable to clear or release a National Instruments task. Try restarting MATLAB.*/ /* DAQmx was unable to clear or release a National Instruments task. Try restarting LabVIEW.*/
    QERR_DAQMX_CANNOT_CREATE_TASK,                                      /* DAQmx was unable to create a new task. The resource may already be in use by another block.*/
    QERR_DAQMX_CANNOT_ATTACH_ADC_TO_TASK,                               /* DAQmx was unable to attach the specified analog input to the analog input task. */
    QERR_DAQMX_CANNOT_START_TASK,                                       /* DAQmx was unable to start the National Instruments device task. Make sure the device is not already open. If no devices are open, try restarting MATLAB.*/ /* DAQmx was unable to start the National Instruments device task. Make sure the device is not already open. If no devices are open, try restarting LabVIEW.*/
    QERR_DAQMX_ERROR_SAMPLING_ADC,                                      /* DAQmx failed to execute the National Instruments analog input task. */
    QERR_DAQMX_ERROR_RESETTING_DEVICE,                                  /* DAQmx failed to reset the device.*/
    QERR_DAQMX_CANNOT_ATTACH_DAC_TO_TASK,                               /* DAQmx was unable to attach the specified analog output to the National Instruments analog output task. */
    QERR_DAQMX_ERROR_WRITING_DAC,                                       /* DAQmx failed to output the requested analog value. */
    QERR_ANALOG_OUTPUT_RANGE_DIFF,                                      /* All analog output channels must have the same output range for this board. */
    QERR_ANALOG_INPUT_RANGE_DIFF,                                       /* All analog input channels must have the same input range for this board. */
    QERR_DAQMX_CANNOT_SET_HARDWARE_CLOCK_RATE,                          /* Error setting the hardware timing for the time-base block. */
    QERR_DAQMX_CLOCK_ERROR_WAITING_FOR_SAMPLE,                          /* Either the configuration is invalid, or a sample edge was missed before executing the wait.*/
    QERR_DAQMX_CANNOT_ATTACH_ENCODER_TO_TASK,                           /* DAQmx was unable to attach the specified channel to the National Instruments encoder input task. */
    QERR_DAQMX_ERROR_SAMPLING_ENCODER,                                  /* DAQmx failed to execute the National Instruments encoder input task. */
    QERR_DAQMX_ERROR_CHANGING_ENC_DIR_SRC,                              /* DAQmx failed to change the source for the encoder count direction. */
    QERR_DAQMX_CANNOT_ATTACH_DIGITAL_TO_TASK,                           /* DAQmx was unable to attach the specified digital lines to the National Instruments task. */
    QERR_DAQMX_ERROR_SAMPLING_DIGITAL,                                  /* DAQmx failed to execute the digital read task. */
    QERR_DAQMX_ERROR_WRITING_DIGITAL,                                   /* DAQmx failed to output the requested digital values. */
    QERR_JR3PCI_CANNOT_INIT,                                            /* Cannot initialize the JR3 PCI force torque sensor. */
    QERR_BUFFER_IS_NULL,                                                /* The buffer argument is NULL. It should be a valid pointer. */
    QERR_DIGITAL_OUTPUT_LOCKED,                                         /* The requested digital output is locked.  If you need access to this line, use the generic version of this driver. */
    QERR_ANALOG_OUTPUT_LOCKED,                                          /* The requested analog output is locked.  If you need access to this channel, use the generic version of this driver. */
    QERR_PWM_OUTPUT_LOCKED,                                             /* The requested PWM output is locked.  If you need access to this channel, use the generic version of this driver. */
    QERR_MISSING_URI_OPTION_NAME,                                       /* No option name was found even though a value was specified. */
    QERR_ENCODER_QUADRATURE_MODE_NOT_SUPPORTED,                         /* The selected quadrature decoding is not available for this board. */
    QERR_MISSING_ENCODER_QUADRATURE_MODES,                              /* Encoder input channels have been specified but not enough encoder quadrature modes have been provided. */
    QERR_INVALID_ENCODER_QUADRATURE_MODE,                               /* One of the encoder quadrature modes specified was not a valid mode. Valid modes are 0, 1, 2 or 4. */
    QERR_MISSING_ENCODER_FILTER_FREQUENCIES,                            /* Encoder input channels have been specified but not enough encoder filter frequencies have been provided. */
    QERR_INVALID_ENCODER_FILTER_FREQUENCY,                              /* One of the encoder filter frequencies specified was not a valid frequency. The frequency is out of range or negative. */
    QERR_HIL_READ_NOT_SUPPORTED,                                        /* The hil_read function in C or MATLAB and HIL Read block in QUARC are not supported by this particular card.*/ /* The Mixed polymorphic instance of the HIL Read VI is not supported by this card. Try using one of the more specific hil_read functions, HIL Read blocks or HIL Read polymorphic instances. */
    QERR_HIL_READ_ANALOG_NOT_SUPPORTED,                                 /* The hil_read_analog function in C or MATLAB and HIL Read Analog block in QUARC are not supported by this particular card.*/ /* The Analog polymorphic instances of the HIL Read VI are not supported by this card. */
    QERR_HIL_READ_ANALOG_BUFFER_NOT_SUPPORTED,                          /* The hil_read_analog_buffer function and HIL Read Analog Buffer block are not supported by this particular card. */
    QERR_HIL_READ_ANALOG_CODES_NOT_SUPPORTED,                           /* The hil_read_analog_codes function and HIL Read Analog Codes block are not supported by this particular card. */
    QERR_HIL_READ_ANALOG_WRITE_ANALOG_NOT_SUPPORTED,                    /* The hil_read_analog_write_analog function and HIL Read Analog Write Analog block are not supported by this particular card. */
    QERR_HIL_READ_ANALOG_WRITE_ANALOG_BUFFER_NOT_SUPPORTED,             /* The hil_read_analog_write_analog_buffer function and HIL Read Analog Write Analog Buffer block are not supported by this particular card. */
    QERR_HIL_READ_BUFFER_NOT_SUPPORTED,                                 /* The hil_read_buffer function and HIL Read Buffer block are not supported by this particular card. */
    QERR_HIL_READ_DIGITAL_NOT_SUPPORTED,                                /* The hil_read_digital function in C or MATLAB and HIL Read Digital block in QUARC are not supported by this particular card.*/ /* The Digital polymorphic instances of the HIL Read VI are not supported by this card. */
    QERR_HIL_READ_DIGITAL_BUFFER_NOT_SUPPORTED,                         /* The hil_read_digital_buffer function and HIL Read Digital Buffer block are not supported by this particular card. */
    QERR_HIL_READ_DIGITAL_WRITE_DIGITAL_NOT_SUPPORTED,                  /* The hil_read_digital_write_digital function and HIL Read Digital Write Digital block are not supported by this particular card. */
    QERR_HIL_READ_DIGITAL_WRITE_DIGITAL_BUFFER_NOT_SUPPORTED,           /* The hil_read_digital_write_digital_buffer function and HIL Read Digital Write Digital Buffer block are not supported by this particular card. */
    QERR_HIL_READ_ENCODER_NOT_SUPPORTED,                                /* The hil_read_encoder function in C or MATLAB and HIL Read Encoder block in QUARC are not supported by this particular card. */ /* The Encoder polymorphic instances of the HIL Read VI are not supported by this card. */
    QERR_HIL_READ_ENCODER_BUFFER_NOT_SUPPORTED,                         /* The hil_read_encoder_buffer function and HIL Read Encoder Buffer block are not supported by this particular card. */
    QERR_HIL_READ_ENCODER_WRITE_PWM_NOT_SUPPORTED,                      /* The hil_read_encoder_write_pwm function and HIL Read Encoder Write PWM block are not supported by this particular card. */
    QERR_HIL_READ_ENCODER_WRITE_PWM_BUFFER_NOT_SUPPORTED,               /* The hil_read_encoder_write_pwm_buffer function and HIL Read Encoder Write PWM Buffer block are not supported by this particular card. */
    QERR_HIL_READ_OTHER_NOT_SUPPORTED,                                  /* The hil_read_other function in C or MATLAB and HIL Read Other block in QUARC are not supported by this particular card. */ /* The Other polymorphic instances of the HIL Read VI are not supported by this card. */
    QERR_HIL_READ_OTHER_BUFFER_NOT_SUPPORTED,                           /* The hil_read_other_buffer function and HIL Read Other Buffer block are not supported by this particular card. */
    QERR_HIL_READ_OTHER_WRITE_OTHER_NOT_SUPPORTED,                      /* The hil_read_other_write_other function and HIL Read Write Other block are not supported by this particular card. */
    QERR_HIL_READ_OTHER_WRITE_OTHER_BUFFER_NOT_SUPPORTED,               /* The hil_read_other_write_other_buffer function and HIL Read Other Write Other Buffer block are not supported by this particular card. */
    QERR_HIL_READ_WRITE_NOT_SUPPORTED,                                  /* The hil_read_write function and HIL Read Write block are not supported by this particular card. Try using a more specific function or block. */
    QERR_HIL_READ_WRITE_BUFFER_NOT_SUPPORTED,                           /* The hil_read_write_buffer function and HIL Read Write Buffer block are not supported by this particular card. Try using a more specific function or block. */
    QERR_HIL_SET_ANALOG_INPUT_RANGES_NOT_SUPPORTED,                     /* The hil_set_analog_input_ranges function is not supported by this particular card. It may be necessary to uncheck the two "Set analog input parameters..." options in the HIL Initialize block. */
    QERR_HIL_SET_ANALOG_OUTPUT_RANGES_NOT_SUPPORTED,                    /* The hil_set_analog_output_ranges function is not supported by this particular card. It may be necessary to uncheck the two "Set analog output parameters..." options in the HIL Initialize block. */
    QERR_HIL_SET_CARD_SPECIFIC_OPTIONS_NOT_SUPPORTED,                   /* The hil_set_card_specific_options function is not supported by this particular card. It may be necessary to uncheck the two "Set clock parameters..." options in the HIL Initialize block. */
    QERR_HIL_SET_CLOCK_MODE_NOT_SUPPORTED,                              /* The hil_set_clock_mode function is not supported by this particular card. */
    QERR_HIL_SET_DIGITAL_DIRECTIONS_NOT_SUPPORTED,                      /* The hil_set_digital_directions function is not supported by this particular card. Set the "Digital input channels" and "Digital output channels" parameters in the HIL Initialize block to empty matrices: []. */
    QERR_HIL_SET_ENCODER_COUNTS_NOT_SUPPORTED,                          /* The hil_set_encoder_counts function and HIL Set Encoder Counts block are not supported by this particular card. It may be necessary to uncheck the two "Set initial encoder counts..." options in the HIL Initialize block. */
    QERR_HIL_SET_ENCODER_FILTER_FREQUENCY_NOT_SUPPORTED,                /* The hil_set_encoder_filter_frequency function is not supported by this particular card. It may be necessary to set the "Encoder filter frequency" parameter in the HIL Initialize block to an empty matrix: []. */
    QERR_HIL_SET_ENCODER_QUADRATURE_MODE_NOT_SUPPORTED,                 /* The hil_set_encoder_quadrature_mode function is not supported by this particular card. It may be necessary to set the "Encoder quadrature" parameter in the HIL Initialize block to an empty matrix: []. */
    QERR_HIL_SET_PWM_DUTY_CYCLE_NOT_SUPPORTED,                          /* The hil_set_pwm_duty_cycle function is not supported by this particular card. It may be necessary to uncheck the two "Set PWM output parameters..." options in the HIL Initialize block. */
    QERR_HIL_SET_PWM_FREQUENCY_NOT_SUPPORTED,                           /* The hil_set_pwm_frequency function is not supported by this particular card. It may be necessary to uncheck the two "Set PWM output parameters..." options in the HIL Initialize block. */
    QERR_HIL_SET_PWM_MODE_NOT_SUPPORTED,                                /* The hil_set_pwm_mode function is not supported by this particular card. It may be necessary to uncheck the two "Set PWM output parameters..." options in the HIL Initialize block. */
    QERR_HIL_TASK_CREATE_ANALOG_READER_NOT_SUPPORTED,                   /* The hil_task_create_analog_reader function and HIL Read Analog Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_ANALOG_READER_ANALOG_WRITER_NOT_SUPPORTED,     /* The hil_task_create_analog_reader_analog_writer function and HIL Read Analog Write Analog Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_DIGITAL_READER_NOT_SUPPORTED,                  /* The hil_task_create_digital_reader function and HIL Read Digital Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_DIGITAL_READER_DIGITAL_WRITER_NOT_SUPPORTED,   /* The hil_task_create_digital_reader_digital_writer function and HIL Read Digital Write Digital Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_DIGITAL_WRITER_NOT_SUPPORTED,                  /* The hil_task_create_digital_writer function that HIL Write Digital Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_ENCODER_READER_NOT_SUPPORTED,                  /* The hil_task_create_encoder_reader function and HIL Read Encoder Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_ENCODER_READER_PWM_WRITER_NOT_SUPPORTED,       /* The hil_task_create_encoder_reader_pwm_writer function and HIL Read Encoder Write PWM Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_OTHER_READER_NOT_SUPPORTED,                    /* The hil_task_create_other_reader function and HIL Read Other Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_OTHER_READER_OTHER_WRITER_NOT_SUPPORTED,       /* The hil_task_create_other_reader_other_writer function and HIL Read Other Write Other Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_OTHER_WRITER_NOT_SUPPORTED,                    /* The hil_task_create_other_writer function and HIL Write Other Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_PWM_WRITER_NOT_SUPPORTED,                      /* The hil_task_create_pwm_writer function and HIL Write PWM Timebase block are not supported by this particular card. */
    QERR_HIL_TASK_CREATE_READER_NOT_SUPPORTED,                          /* The hil_task_create_reader function and HIL Read Timebase block are not supported by this particular card. Try one of the more specific functions or blocks. */
    QERR_HIL_TASK_CREATE_READER_WRITER_NOT_SUPPORTED,                   /* The hil_task_create_reader_writer function and HIL Read Write Timebase block are not supported by this particular card. Try one of the more specific functions or blocks. */
    QERR_HIL_TASK_CREATE_WRITER_NOT_SUPPORTED,                          /* The hil_task_create_writer function and HIL Write Timebase block are not supported by this particular card. Try one of the more specific functions or blocks. */
    QERR_HIL_TASK_DELETE_NOT_SUPPORTED,                                 /* The hil_task_delete function is not supported by this particular card. If one of the hil_task_create... functions is supported then the hil_task_delete function MUST be supported! In this case, contact the driver manufacturer. */
    QERR_HIL_TASK_FLUSH_NOT_SUPPORTED,                                  /* The hil_task_flush function is not supported by this particular card. If one of the hil_task_write... functions is supported then the hil_task_flush function MUST be supported! In this case, contact the driver manufacturer. */
    QERR_HIL_TASK_READ_NOT_SUPPORTED,                                   /* The hil_task_read function is not supported by this particular card. Try one of the more specific functions. */
    QERR_HIL_TASK_READ_ANALOG_NOT_SUPPORTED,                            /* The hil_task_read_analog function is not supported by this particular card. */
    QERR_HIL_TASK_READ_ANALOG_WRITE_ANALOG_NOT_SUPPORTED,               /* The hil_task_read_analog_write_analog function is not supported by this particular card. */
    QERR_HIL_TASK_READ_DIGITAL_NOT_SUPPORTED,                           /* The hil_task_read_digital function is not supported by this particular card. */
    QERR_HIL_TASK_READ_DIGITAL_WRITE_DIGITAL_NOT_SUPPORTED,             /* The hil_task_read_digital_write_digital function is not supported by this particular card. */
    QERR_HIL_TASK_READ_ENCODER_NOT_SUPPORTED,                           /* The hil_task_read_encoder function is not supported by this particular card. */
    QERR_HIL_TASK_READ_ENCODER_WRITE_PWM_NOT_SUPPORTED,                 /* The hil_task_read_encoder_write_pwm function is not supported by this particular card. */
    QERR_HIL_TASK_READ_OTHER_NOT_SUPPORTED,                             /* The hil_task_read_other function is not supported by this particular card. */
    QERR_HIL_TASK_READ_OTHER_WRITE_OTHER_NOT_SUPPORTED,                 /* The hil_task_read_other_write_other function is not supported by this particular card. */
    QERR_HIL_TASK_READ_WRITE_NOT_SUPPORTED,                             /* The hil_task_read_write function is not supported by this particular card. Try one of the more specific functions. */
    QERR_HIL_TASK_START_NOT_SUPPORTED,                                  /* The hil_task_start function is not supported by this particular card. If one of the hil_task_create... functions is supported then the hil_task_start function MUST be supported! In this case, contact the driver manufacturer. */
    QERR_HIL_TASK_STOP_NOT_SUPPORTED,                                   /* The hil_task_stop function is not supported by this particular card. If one of the hil_task_create... functions is supported then the hil_task_stop function MUST be supported! In this case, contact the driver manufacturer. */
    QERR_HIL_TASK_WRITE_NOT_SUPPORTED,                                  /* The hil_task_write function is not supported by this particular card. Try one of the more specific functions. */
    QERR_HIL_TASK_WRITE_ANALOG_NOT_SUPPORTED,                           /* The hil_task_write_analog function is not supported by this particular card. */
    QERR_HIL_TASK_WRITE_DIGITAL_NOT_SUPPORTED,                          /* The hil_task_write_digital function is not supported by this particular card. */
    QERR_HIL_TASK_WRITE_OTHER_NOT_SUPPORTED,                            /* The hil_task_write_other function is not supported by this particular card. */
    QERR_HIL_TASK_WRITE_PWM_NOT_SUPPORTED,                              /* The hil_task_write_pwm function is not supported by this particular card. */
    QERR_HIL_WRITE_NOT_SUPPORTED,                                       /* The hil_write function in C or MATLAB and HIL Write block in QUARC are not supported by this particular card. */ /* The Mixed polymorphic instance of the HIL Write VI is not supported by this card. Try using one of the more specific hil_write functions, HIL Write blocks or HIL Write polymorphic instances. */
    QERR_HIL_WRITE_ANALOG_NOT_SUPPORTED,                                /* The hil_write_analog function in C or MATLAB and HIL Write Analog block in QUARC are not supported by this particular card. */  /* The Analog polymorphic instances of the HIL Write VI are not supported by this card. */
    QERR_HIL_WRITE_ANALOG_BUFFER_NOT_SUPPORTED,                         /* The hil_write_analog_buffer function and HIL Write Analog Buffer block are not supported by this particular card. */
    QERR_HIL_WRITE_ANALOG_CODES_NOT_SUPPORTED,                          /* The hil_write_analog_codes function and HIL Write Analog Codes block are not supported by this particular card. */
    QERR_HIL_WRITE_BUFFER_NOT_SUPPORTED,                                /* The hil_write_buffer function and HIL Write Buffer block are not supported by this particular card. Try using one of the more specific functions or blocks. */
    QERR_HIL_WRITE_DIGITAL_NOT_SUPPORTED,                               /* The hil_write_digital function in C or MATLAB and HIL Write Digital block in QUARC are not supported by this particular card. */ /* The Digital polymorphic instances of the HIL Write VI are not supported by this card. */
    QERR_HIL_WRITE_DIGITAL_BUFFER_NOT_SUPPORTED,                        /* The hil_write_digital_buffer function and HIL Write Digital Buffer block are not supported by this particular card. */
    QERR_HIL_WRITE_OTHER_NOT_SUPPORTED,                                 /* The hil_write_other function in C or MATLAB and HIL Write Other block in QUARC are not supported by this particular card. */ /* The Other polymorphic instances of the HIL Write VI are not supported by this card. */
    QERR_HIL_WRITE_OTHER_BUFFER_NOT_SUPPORTED,                          /* The hil_write_other_buffer function and HIL Write Other Buffer block are not supported by this particular card. */
    QERR_HIL_WRITE_PWM_NOT_SUPPORTED,                                   /* The hil_write_pwm function in C or MATLAB and HIL Write PWM block in QUARC are not supported by this particular card. */ /* The PWM polymorphic instances of the HIL Write VI are not supported by this card. */
    QERR_HIL_WRITE_PWM_BUFFER_NOT_SUPPORTED,                            /* The hil_write_pwm_buffer function and HIL Write PWM Buffer block are not supported by this particular card. */
    QERR_Q3_CONTROLPAQ_FW_CANNOT_OPEN_BOARD,                            /* The specified Q3 ControlPaQ-FW board could not be opened. Check that the board is powered and properly connected and that the board number is correct. */
    QERR_CANNOT_CREATE_GAME_CONTROLLER_WINDOW,                          /* Unable to create a window for the force feedback game controller. */
    QERR_CANNOT_SET_GAME_CONTROLLER_COOPERATIVE_LEVEL,                  /* Unable to set the cooperation level of the force feedback game controller. */
    QERR_CONNECTION_NOT_BOUND,                                          /* The connection has not been bound. This error typically occurs with UDP client sockets whenever a receive operation is attempted prior to the first send operation. UDP client sockets are implicitly bound to the UDP port by the first send operation. Hence, a send must always be done first after a UDP client connection is established. */
    QERR_NO_SIMULINK_DEVELOPMENT_LICENSE,                               /* You do not have a valid license for the QUARC Simulink Development Environment. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */ /* You do not have a valid license for this functionality. */
    QERR_INVALID_CIRCULAR_BUFFER,                                       /* The circular buffer is invalid. A circular buffer may not be used after it has been closed. */
    QERR_READ_TOO_LONG,                                                 /* The amount of data requested in a read operation is too long. For example, you cannot read more bytes from a circular buffer than are contained in the buffer. */
    QERR_WRITE_TOO_LONG,                                                /* The amount of data provided in a write operation is too long. For example, you cannot write more bytes to a circular buffer than can be contained in the buffer. */
    QERR_TOO_MANY_FORCE_FEEDBACK_EFFECTS,                               /* It is not possible to add another force feedback effect because the maximum number of force feedback effects has already been reached. Change the maximum number of force feedback effects in the Host Force Feedback Game Controller block. */
    QERR_INVALID_FORCE_FEEDBACK_AXIS,                                   /* An invalid axis number was specified for a force feedback effect. Axes numbers must range from 0 to 5, corresponding to x, y, z, Rx, Ry and Rz axes respectively. */
    QERR_CANNOT_CREATE_FORCE_FEEDBACK_EFFECT,                           /* Unable to create a force feedback effect. The device may be out of memory for effects or the effect is not supported. */
    QERR_CANNOT_START_FORCE_FEEDBACK_EFFECT,                            /* Unable to download or start a force feedback effect. The device may be out of memory. */
    QERR_CANNOT_STOP_FORCE_FEEDBACK_EFFECT,                             /* Unable to stop a force feedback effect. */
    QERR_CANNOT_SET_FORCE_FEEDBACK_EFFECT_PARAMETERS,                   /* Unable to set the parameters of a force feedback effect. The parameters may be incorrect or unsupported by the device. */
    QERR_INVALID_FORCE_FEEDBACK_EFFECT,                                 /* The given force feedback effect is invalid and does not belong to the game controller specified. The effect may not be supported by the game controller. Also, once an effect has been removed it cannot be used. */
    QERR_INVALID_GAME_CONTROLLER,                                       /* The specified game controller is invalid. */
    QERR_GAME_CONTROLLER_NOT_FOUND,                                     /* The specified game controller could not be found. A Host Force Feedback Game Controller block for the game controller is required in the same diagram to use the other Force Feedback blocks. There should only be one Host Force Feedback Game Controller block per game controller. Also ensure that the Host Force Feedback Game Controller block comes before the other Force Feedback blocks in the sorted (execution) order. */
    QERR_CANNOT_START_TARGET_MANAGER,                                   /* The QUARC Target Manager could not be started. */ /* The Target Manager could not be started. */
    QERR_CANNOT_STOP_TARGET_MANAGER,                                    /* The QUARC Target Manager could not be stopped. */ /* The Target Manager could not be stopped. */
    QERR_PEER_IGNORING_SHUTDOWN,                                        /* The peer is not responding to the connection being shut down. The receive operation has timed out. */
    QERR_INVALID_PERIODIC_EFFECT_TYPE,                                  /* An invalid periodic effect type was passed to the game_controller_add_periodic_force_effect function. */
    QERR_INVALID_CONDITION_EFFECT_TYPE,                                 /* An invalid condition effect type was passed to the game_controller_add_condition_force_effect function. */
    QERR_TOO_MANY_GAME_CONTROLLER_AXES,                                 /* No more than six axes may be specified for a game controller force effect. */
    QERR_INVALID_NUMBER_OF_CONDITIONS,                                  /* Invalid number of conditions for a condition force effect. There may be one condition for all axes or one condition for each axis. */
    QERR_INCOMPLETE_READ,                                               /* This error should never be returned. It is used internally by the Quanser Stream API. */
    QERR_EXCLUSIVE_ACCESS_ALREADY_GRANTED,                              /* Exclusive access to this card has already been granted to another process. Only one process may have exclusive access to the card at one time. Try again later. */
    QERR_EXCLUSIVE_ACCESS_NOT_GRANTED,                                  /* Exclusive access to this card was not granted to the process which is attempting to release it. Exclusive access can only be released by the process with exclusive access, and only from the same open handle. */
    QERR_CARD_LOCATION_IS_NULL,                                         /* The card location pointer passed as an argument is NULL. A valid pointer to a t_card_location object must be passed to the hil_get_exclusive_access and hil_release_exclusive_access functions. */
    QERR_HIL_ACQUIRE_EXCLUSIVE_ACCESS_NOT_SUPPORTED,                    /* The hil_acquire_exclusive_access function and Exclusive access to device option on the HIL Initialize block are not supported by this particular card. */
    QERR_HIL_RELEASE_EXCLUSIVE_ACCESS_NOT_SUPPORTED,                    /* The hil_release_exclusive_access function and Exclusive access to device option on the HIL Initialize block are not supported by this particular card. */
    QERR_DRIVER_MISSING_GET_OR_RELEASE_ACCESS,                          /* The hil_get_exclusive_access or hil_release_exclusive_access function is present in the driver while the other one is not. These functions are optional, but if one is included in the driver then both must be included. */
    QERR_CIRCULAR_BUFFER_NOT_FOUND,                                     /* The corresponding Circular Buffer Initialize could not be found. Make sure that a Circular Buffer Initialize block is present in the model. */
    QERR_INCOMPATIBLE_PIPE,                                             /* An attempt was made to create a named pipe for a pipe that already exists and the properties of the pipe are incompatible. Be aware that under the Windows target, the pipe name "localhost" is already used by the system. */
    QERR_SENSORAY_TOO_MANY_BOARDS,                                      /* The Sensoray driver supports a maximum of 16 boards. */
    QERR_SENSORAY_ILLEGAL_PARAM,                                        /* An illegal parameter was passed to the Sensoray driver. */
    QERR_SENSORAY_EEPROM_ERROR,                                         /* The Sensoray board failed to access its EEPROM during initialization.  Try unregistering the board and re-registering it.  If the error persists, then the problem is likely a hardware fault. */
    QERR_SENSORAY_UNSPECIFIED_ERROR,                                    /* The Sensoray board has experienced an unspecified fault. */
    QERR_KERNEL_CANNOT_REGISTER_BOARD,                                  /* The kernel-mode driver can't register the board.  This is usually caused by applications that fail to unlink from the system dll, or if the kernel model driver is improperly installed or registered. */
    QERR_DMA_BUFFER_LOCK,                                               /* A DMA buffer lock failed. */
    QERR_CANNOT_START_INTERRUPT_THREAD,                                 /* Failed to launch an interrupt thread */
    QERR_DAC_COMM_TIMEOUT,                                              /* Cannot communicate with analog output. */
    QERR_COUNTER_RESOURCE_CONFLICT,                                     /* Counter parameter is illegal in current operation mode.  The counter may already be in use by another operation such as providing a timebase. */
    QERR_STREAM_NOT_CONNECTED,                                          /* The non-blocking stream is in the process of connecting but is not yet connected. The stream_poll function or Stream Poll block must be invoked with the connect flag to complete the connection. */
    QERR_LIBRARY_LOAD_ERROR,                                            /* The dynamic link library was found, but an error occurred while loading it. */
    QERR_PHANTOM_OMNI_CANNOT_OPEN_BOARD,                                /* The specified PHANTOM Omni board could not be opened. Check that the device is powered and properly connected and that the board number is correct. */
    QERR_JR3PCI_CANNOT_SET_FULL_SCALES,                                 /* An error occurred attempting to set the full scales for the JR3 sensor. */
    QERR_ALTIA_ARGUMENT_IS_NULL,                                        /* The altia argument to altia_open is NULL. */
    QERR_INVALID_ALTIA,                                                 /* An invalid Altia handle was passed as an argument. Once an Altia connection has been closed using altia_close the Altia handle is invalid. */
    QERR_ALTIA_INPUT_IS_NULL,                                           /* The altia_input argument to altia_register_input is NULL. */
    QERR_ALTIA_OUTPUT_IS_NULL,                                          /* The altia_output argument to altia_register_output is NULL. */
    QERR_INVALID_ALTIA_EVENT_NAME,                                      /* An invalid event name was passed to an altia function. */
    QERR_INVALID_ALTIA_INPUT,                                           /* An invalid t_altia_input handle was passed as an argument. */
    QERR_INVALID_ALTIA_OUTPUT,                                          /* An invalid t_altia_output handle was passed as an argument. */
    QERR_BEEP_ARGUMENT_IS_NULL,                                         /* The beep argument to beep_open is NULL. */
    QERR_INVALID_BEEP,                                                  /* An invalid beep handle was passed as an argument. Once an beep handle has been closed using beep_close the beep handle is invalid. */
    QERR_BEEP_FAILED,                                                   /* A beep was attempted but it failed for some reason. It is possible that permission was denied. */
    QERR_BEEP_FREQUENCY_OUT_OF_RANGE,                                   /* The specified beep frequency is out of the acceptable range. See the documentation for valid beep frequencies. */
    QERR_SCAN_VALUE_IS_NULL,                                            /* An argument passed to a stream_scan function to store a value scanned is NULL. Arguments must contain the address of appropriately typed quantities. */
    QERR_CARD_SPECIFIC_OPTION_NOT_RECOGNIZED,                           /* The card specific option specified is not recognized. */
    QERR_CARD_SPECIFIC_OPTION_VALUE_NOT_RECOGNIZED,                     /* The value of a card specific option specified is not recognized. */
    QERR_CARD_SPECIFIC_OPTION_NOT_SUPPORTED,                            /* The card specific option specified is recognized, but is not supported by this board. */
    QERR_INVALID_ROOMBA,                                                /* The Roomba object is not valid. A Roomba object cannot be used after it has been closed. */
    QERR_INVALID_ROOMBA_SENSOR_ID,                                      /* The Roomba sensor id is not valid. It must be a value between 7 and 42 inclusive. */
    QERR_VISION_CAMERA_NOT_FOUND,                                       /* The camera could not be found or is not valid for image capture. */
    QERR_INVALID_IPLIMAGE,                                              /* Invalid IplImage structure. */
    QERR_SAVE_IMAGE,                                                    /* Failed to save IplImage using. */
    QERR_INIT_V4L2_DEVICE,                                              /* Failed to initialize v4l2 video input. */
    QERR_GRAB_V4L2_IMAGE,                                               /* Failed to grab image from v4l2 video input. */
    QERR_NO_RPC_SERVER_FOR_BEEP,                                        /* The RPC server is unavailable so the beep cannot be sounded. This problem has been seen on laptops running Vista. */
    QERR_MISMATCHED_CHARACTER,                                          /* A character in the input stream did not match the character sequence described in the format string when scanning the stream. */
    QERR_EMPTY_SCAN,                                                    /* The stream was closed before the first character was read. This error is used internally and should never be returned to the user. */
    QERR_URI_MISSING_HOST,                                              /* The hostname is missing from the URI. Although a hostname is not required for all URIs, the fact that you are getting this message indicates that it is required in this circumstance. */
    QERR_PATH_IN_PIPE_URI,                                              /* The form of the pipe URI must be pipe:name or pipe://server/name. The name cannot contain forward or backward slashes. */
    QERR_HOST_IN_PIPE_URI,                                              /* The pipe URI contains a hostname. Specifying a hostname is not supported on this target, because pipes may not be used to communicate between computers on the selected target. */
    QERR_HIQ_UNKNOWN_REPORT_TYPE,                                       /* The specified HiQ report type is unknown. Ensure that the selected HiQ report or mode is valid. */
    QERR_HIQ_RECEIVE_BLOCKED,                                           /* The HiQ thread failed to receive any data from the HiQ board. */
    QERR_HIL_WATCHDOG_SET_ANALOG_EXPIRATION_STATE_NOT_SUPPORTED,        /* The hil_watchdog_set_analog_expiration_state function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_SET_DIGITAL_EXPIRATION_STATE_NOT_SUPPORTED,       /* The hil_watchdog_set_digital_expiration_state function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_SET_PWM_EXPIRATION_STATE_NOT_SUPPORTED,           /* The hil_watchdog_set_pwm_expiration_state function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_SET_OTHER_EXPIRATION_STATE_NOT_SUPPORTED,         /* The hil_watchdog_set_other_expiration_state function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_START,                                            /* The hil_watchdog_start function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_STOP,                                             /* The hil_watchdog_stop function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_RELOAD,                                           /* The hil_watchdog_reload function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_IS_EXPIRED,                                       /* The hil_watchdog_is_expired function is not supported by this particular card. */
    QERR_HIL_WATCHDOG_CLEAR,                                            /* The hil_watchdog_clear function is not supported by this particular card. */
    QERR_HIL_INVALID_DIGITAL_STATE,                                     /* One of the digital states specified was not a valid state. Valid modes are 0 (low), 1 (high), 2 (tristate) or 3 (no change). */
    QERR_ANALOG_EXPIRATION_STATE_NOT_ZERO,                              /* This board only supports resetting the analog outputs to zero when the watchdog expires. */
    QERR_DIGITAL_EXPIRATION_STATE_NOT_TRISTATE,                         /* This board only supports resetting the digital outputs to tri-state when the watchdog expires. */
    QERR_CLOCK_NOT_WATCHDOG,                                            /* The specified clock is not a watchdog timer on this board. */
    QERR_ANALOG_EXPIRATIONS_NOT_CONFIGURED,                             /* Some of the analog output expiration states have not been configured. This board requires that if any of the expiration states have been configured then all the states must be configured, and the "Set analog outputs when a watchdog timer expires" must be enabled. */
    QERR_DIGITAL_EXPIRATIONS_NOT_CONFIGURED,                            /* Some of the digital output expiration states have not been configured. This board requires that if any of the expiration states have been configured then all the states must be configured, and the "Set digital outputs when a watchdog timer expires" must be enabled. */
    QERR_CLOCK_PERIOD_TOO_HIGH,                                         /* The clock period is too high for the specified clock. Try using a different clock. Hardware clocks are generally faster than the system clocks. */
    QERR_CLOCK_PERIOD_TOO_LOW,                                          /* The clock period is too low for the specified clock. Try using a different clock. System clocks are preferable for long periods so that hardware clocks remain available for operations requiring a shorter period. */
    QERR_HIL_TASK_CREATE_ANALOG_WRITER_NOT_SUPPORTED,                   /* The hil_task_create_analog_writer function and HIL Write Analog Timebase block are not supported by this particular card. */
    QERR_FALCON_FAILED_TO_INITIALIZE,                                   /* The Novint Falcon failed to initialize.  Make sure the Falcon is plugged in and powered. */
    QERR_FALCON_COULD_NOT_OPEN_DEVICE,                                  /* Could not open the Novint Falcon device. */
    QERR_FALCON_COULD_NOT_START_DEVICE,                                 /* Could not start the Novint Falcon control loop. */
    QERR_FALCON_COULD_NOT_CREATE_CALLBACK,                              /* Could not create a callback for the Novint Falcon. */
    QERR_FALCON_COULD_NOT_MAKE_CURRENT,                                 /* Novint Falcon error. */
    QERR_Q8_SERIES_EXPIRATIONS_NOT_CONFIGURED,                          /* Some of the analog or digital output expiration states have not been configured. The Q8-series of boards requires that all analog and digital output channels be configured to be reset on watchdog expiration, not just some of the channels. */
    QERR_CONNECTION_ABORTED,                                            /* An incoming connection was indicated, but was subsequently terminated by the remote peer prior to accepting the call. */
    QERR_INVALID_ROOMBA_SONG_NUMBER,                                    /* Roomba song number must be 0 to 15. */
    QERR_INVALID_ROOMBA_SONG_LENGTH,                                    /* Roomba song length must be 1 to 16. */
    QERR_INVALID_ROOMBA_NOTE_NUMBER,                                    /* The note number of Roomba song must be 31 to 127. */
    QERR_INVALID_ROOMBA_DIGITAL_OUTPUT,                                 /* Roomba digital output must be 0 to 7. */
    QERR_INVALID_ROOMBA_EVENT_NO,                                       /* Roomba event no must be 1 to 22. */
    QERR_INVALID_ROOMBA_MODE,                                           /* Roomba mode number must be 1 to 3. */
    QERR_INVALID_ROOMBA_DEMO,                                           /* Roomba demo number must be 1 to 11. */
    QERR_INVALID_ROOMBA_LED_BITS,                                       /* Roomba LED bits must be 0 to 10. */
    QERR_INVALID_ROOMBA_SCRIPT_LENGTH,                                  /* Data length mismatches according to the script length defined in the first byte. */
    QERR_PREFERENCES_VALUE_CONTAINS_ENVIRONMENT_VARIABLES,              /* The preferences value contains environment variable references, which cannot be expanded. */
    QERR_INVALID_TYPE_OF_PREFERENCES_VALUE,                             /* The preferences value is not a string. */
    QERR_INVALID_ROOMBA_STREAM_STATE,                                   /* Roomba stream state must be 0 to 1. */
    QERR_INVALID_ROOMBA_DRIVER_BITS,                                    /* Roomba low side driver number must be 0 to 7. */
    QERR_INVALID_ROOMBA_DUTY_CYCLE,                                     /* Roomba duty cycle must be 0 to 128. */
    QERR_INVALID_ROOMBA_PACKET_NUMBER,                                  /* The number of Roomba sensor packets requested must be 0 to 43 */
    QERR_INVALID_ROOMBA_STREAM_HEADER,                                  /* Roomba stream header must be 19.*/
    QERR_CORRUPTED_ROOMBA_STREAM,                                       /* Roomba stream is corrupted. */
    QERR_INVALID_ROOMBA_STREAM_SIZE,                                    /* Roomba stream size must be (number of packets + number of data bytes + 3) */
    QERR_INVALID_IMAGE_DIMENSION,                                       /* Invalid dimension for image data */
    QERR_INVALID_SERACCEL,                                              /* The SerAccel object is not valid. A SerAccel object cannot be used after it has been closed. */
    QERR_SERACCEL_COULD_NOT_OPEN_DEVICE,                                /* The SerAccel could not be opened. Make sure the SerAccel is connected and set to binary mode. */
    QERR_SERACCEL_COULD_NOT_START_DEVICE,                               /* The SerAccel could not be started. */
    QERR_SERACCEL_COULD_NOT_READ_DEVICE,                                /* The SerAccel could not be read. */
    QERR_NO_ALTIA_LICENSE,                                              /* You do not have a valid license for the Altia blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_IROBOT_ROOMBA_LICENSE,                                      /* You do not have a valid license for the IRobot Roomba blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_JR3_FORCE_TORQUE_LICENSE,                                   /* You do not have a valid license for the JR3 Force/Torque Sensor blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_MITSUBISHI_PA10_LICENSE,                                    /* You do not have a valid license for the Mitsubishi PA-10 blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_NINTENDO_WIIMOTE_LICENSE,                                   /* You do not have a valid license for the Nintendo Wiimote blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_NOVINT_FALCON_LICENSE,                                      /* You do not have a valid license for the Novint Falcon blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_POINTGREY_CAMERAS_LICENSE,                                  /* You do not have a valid license for the Point Grey Research Cameras blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_SCHUNK_GRIPPER_LICENSE,                                     /* You do not have a valid license for the Schunk Gripper blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_SENSABLE_OMNI_LICENSE,                                      /* You do not have a valid license for the SensAble Omni blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_INVALID_IMAGE_NAME,                                            /* The specified image does not exist. */
    QERR_NO_INTERNAL_USE_LICENSE,                                       /* The "Active during normal simulation" feature is only licensed for QUARC Home use. Due to safety and liability concerns, this feature is not enabled, and will not be enabled, for full QUARC installations. */
    QERR_DRAGANFLY_X6_CRC_FAILED,                                       /* The Draganfly X6 autopilot message failed the CRC check. */
    QERR_CANPCI_NOT_FOUND,                                              /* The specified CANPCI could not be found. */
    QERR_CANPCI_INIT_FAILED,                                            /* Initialization of the CANPCI driver failed. */
    QERR_CANPCI_INVALID_PARAMETERS,                                     /* Parameters supplied to a CANPCI driver function are invalid. */
    QERR_CANPCI_SEND_MESSAGE_FAILED,                                    /* The CANPCI device failed to send a CAN message. */
    QERR_CANPCI_GET_MESSAGE_FAILED,                                     /* The CANPCI device failed to receive a CAN message. */
    QERR_CANPCI_INVALID_CHANNEL,                                        /* The CANPCI channel specified is invalid. */
    QERR_CANPCI_START_FAILED,                                           /* Failed to start the CANPCI card(s). */
    QERR_INVALID_UBLOX,                                                 /* The Ublox object is not valid. A Ublox object cannot be used after it has been closed. */
    QERR_NO_UBLOX_MSG,                                                  /* No Ublox message */
    QERR_INVALID_UBLOX_MSG,                                             /* Invalid Ublox message */
    QERR_INVALID_UBLOX_IDENTIFIERS,                                     /* Invalid Ublox identifiers */
    QERR_INVALID_UBLOX_CHECKSUM,                                        /* Invalid Ublox checksum */
    QERR_INVALID_NMEA_MSG,                                              /* Invalid NMEA message */
    QERR_INVALID_NMEA_CHECKSUM,                                         /* Invalid NMEA checksum */
    QERR_INVALID_UBLOX_DATA,                                            /* Invalid Ublox data */
    QERR_UNSUPPORTED_GPS_DATA_FIELD,                                    /* Unsupported Ublox GPS data field */
    QERR_ROBOSTIX_INVALID_PROGRAM_VERSION,                              /* The program on the robostix has an invalid version information (i.e., is either too old or too new). */
    QERR_SPI_TRANSMIT,                                                  /* A transmit error occured using the Serial Peripheral Interface (SPI) protocol. */
    QERR_SPI_RECEIVE,                                                   /* A receive error occured using the Serial Peripheral Interface (SPI) protocol. */
    QERR_NO_SUCH_DEVICE,                                                /* No such device or address */
    QERR_INTIME_NOT_RUNNING,                                            /* A real-time object could not be created. The INtime real-time kernel may not be running. Use the INtime Status icon in the system tray to start the INtime kernel. */
    QERR_CANNOT_CONNECT_TO_LICENSE_MANAGER,                             /* It was not possible to connect to the license manager. */
    QERR_MISSING_PROPERTIES,                                            /* No properties were specified even though the number of properties is nonzero. */
    QERR_MISSING_PROPERTIES_BUFFER,                                     /* Properties have been specified but no values have been provided for the operation. */
    QERR_HIL_GET_INTEGER_PROPERTY_NOT_SUPPORTED,                        /* The hil_get_integer_property function and HIL Get Property block are not supported by this particular card. */
    QERR_HIL_GET_DOUBLE_PROPERTY_NOT_SUPPORTED,                         /* The hil_get_double_property function and HIL Get Property block are not supported by this particular card. */
    QERR_HIL_GET_STRING_PROPERTY_NOT_SUPPORTED,                         /* The hil_get_string_property function and HIL Get Property block are not supported by this particular card. */
    QERR_HIL_SET_INTEGER_PROPERTY_NOT_SUPPORTED,                        /* The hil_set_integer_property function and HIL Set Property block are not supported by this particular card. */
    QERR_HIL_SET_DOUBLE_PROPERTY_NOT_SUPPORTED,                         /* The hil_set_double_property function and HIL Set Property block are not supported by this particular card. */
    QERR_HIL_SET_STRING_PROPERTY_NOT_SUPPORTED,                         /* The hil_set_string_property function and HIL Set Property block are not supported by this particular card. */
    QERR_PROPERTY_NOT_RECOGNIZED,                                       /* One or more of the specified properties were not recognized by the board-specific driver. */
    QERR_GUMSTIX_WATCHDOG_CLOCK_PERIOD_TOO_HIGH,                        /* The watchdog timer period (a.k.a., timeout interval) is too high. The gumstix watchdog timer may be programmed with any integer value between 1 and 255 seconds. */
    QERR_GUMSTIX_WATCHDOG_CLOCK_PERIOD_TOO_LOW,                         /* The watchdog timer period (a.k.a., timeout interval) is too low. The gumstix watchdog timer may be programmed with any integer value between 1 and 255 seconds. */
    QERR_DIGITAL_INPUTS_NOT_INITIALIZED,                                /* The specified digital input channels are not initialized. This board requires that all the channels which will be used for digital inputs should be configured on the HIL Initialize block's "Digital Inputs" tab. Set the "Digital input channels" field to all the digital channels that will be used as digital inputs on the board.*/
    QERR_DIGITAL_OUTPUTS_NOT_INITIALIZED,                               /* The specified digital output channels are not initialized. This board requires that all the channels which will be used for digital outputs should be configured on the HIL Initialize block's "Digital Outputs" tab. Set the "Digital output channels" field to all the digital channels that will be used as digital outputs on the board.*/
    QERR_FILTER_PROTOCOLS_REQUIRE_URI,                                  /* Missing "uri" option. Filter protocols require a "uri" option in their URI to identify the underlying communication protocol. */
    QERR_CONFLICTING_COUNTER_MODES,                                     /* The specified counter is used as both an encoder and a PWM output channel. */
    QERR_DAQMX_ERROR_CHANGING_PWM_OUT_TERM,                             /* DAQmx failed to change the counter output terminal. */
    QERR_DAQMX_ERROR_WRITING_PWM,                                       /* DAQmx failed to output the requested PWM values. */
    QERR_DAQMX_CANNOT_ATTACH_PWM_TO_TASK,                               /* DAQmx was unable to attach the specified counter channel to the PWM output task. */
    QERR_DAQMX_ERROR_SETTING_IMPLICIT_TIMING,                           /* DAQmx was unable to configure implicit timing for the PWM output task. */
    QERR_DAQMX_CANNOT_GET_PWM_CHANNEL_NAME,                             /* DAQmx was unable to obtain the name of the PWM channel attached to the PWM output task. */
    QERR_NI_DUTY_CYCLE_OUT_OF_RANGE,                                    /* The specified PWM duty cycle is out of range. For National Instruments cards, the duty cycle should fall within the range between a minimum value of 0.1 % (0.001) and a maximum value of 99.9 % (0.999). */
    QERR_NI_FREQUENCY_OUT_OF_RANGE,                                     /* The specified PWM frequency is out of range. For National Instruments cards, the frequency must satisfy the following inequality: (Maximum Counter Output Frequency/Max Number of Counts) <= frequency <= (Maximum Counter Output Frequency/4). */
    QERR_DAQMX_ERROR_CHANGING_TIMEBASE_RATE,                            /* DAQmx was unable to set the counter timebase rate. */
    QERR_INVALID_DSR_CONTROL,                                           /* Invalid dsr option. Supported values are "off", "on" or "handshake". */
    QERR_OPTITRACK_RIGID_BODY_INIT_ERROR,                               /* Unable to initialize the OptiTrack Rigid Body API. Make sure the proper software is installed and the path variable is set. */
    QERR_OPTITRACK_POINT_CLOUD_INIT_ERROR,                              /* Unable to initialize the OptiTrack Point Cloud API. Make sure the proper software is installed and the path variable is set. */
    QERR_OPTITRACK_RIGID_BODY_ID_INVALID,                               /* The rigid body ID is invalid or not found in the rigid body definition file. Valid IDs are integers ranging from 1 to 1024. */
    QERR_OPTITRACK_ERROR_STARTING_CAMERAS,                              /* An error occurred starting the OptiTrack camera system. Make sure they are properly connected. */
    QERR_OPTITRACK_ERROR_STOPPING_CAMERAS,                              /* An error occurred stopping the OptiTrack camera system. */
    QERR_OPTITRACK_INVALID_CALIBRATION_FILE,                            /* Unable to load OptiTrack calibration file. Make sure the file path is correct or the calibration file is compatible with the Motive software version that you have installed. */
    QERR_OPTITRACK_INVALID_RIGID_BODY_FILE,                             /* Unable to load OptiTrack rigid body definition file. Make sure the file path is correct. */
    QERR_OPTITRACK_TOO_MANY_RIGID_BODIES,                               /* The number of specified OptiTrack rigid bodies exceeds the number of objects in the rigid body definition file. */
    QERR_VISION_INVALID_PARAMETER,                                      /* Invalid parameter for OpenCV functions */
    QERR_VISION_INVALID_NO_OF_CHANNELS,                                 /* Invalid number of color planes of the input image */
    QERR_NO_CANCELLATION_HANDLER,                                       /* An attempt was made to pop a cancellation handler when no cancellation handler was pushed on the stack! */
    QERR_VISION_INVALID_INPUT,                                          /* Invalid input for OpenCV functions */
    QERR_PORT_UNREACHABLE,                                              /* The port is unreachable. For UDP datagrams, a previous send operation resulted in an ICMP Port Unreachable message, indicating that there is likely no server listening on the UDP port. */
    QERR_CANNOT_SET_PORT_UNREACHABLE,                                   /* Cannot set the port unreachable option to disable reporting ICMP Port Unreachable messages for UDP datagrams */
    QERR_MUST_BE_ADMINISTRATOR,                                         /* The process lacks the appropriate privileges to perform the operation. Administrator privileges are required. Log in as an Administrator or run as Administrator. */
    QERR_MISMATCHED_ENCODER_FILTER_FREQUENCY,                           /* One of the encoder filter frequencies specified does not match the filter frequency of the other channels. This card only allows one filter frequency to be set for all encoder channels. */
    QERR_MISMATCHED_CLOCK_FREQUENCY,                                    /* One of the clock frequencies specified does not match the frequency of another channel which shares the same clock resources. */
    QERR_UNABLE_TO_OPEN_DIALOG,                                         /* The underlying operating system could not open the dialog. */
    QERR_HIL_SET_DIGITAL_OUTPUT_CONFIGURATION_NOT_SUPPORTED,            /* The hil_set_digital_output_configuration function is not supported by this particular card. */
    QERR_HIL_SET_PWM_CONFIGURATION_NOT_SUPPORTED,                       /* The hil_set_pwm_configuration function is not supported by this particular card. */
    QERR_HIL_SET_PWM_DEADBAND_NOT_SUPPORTED,                            /* The hil_set_pwm_deadband function is not supported by this particular card. */
    QERR_MISSING_DIGITAL_CONFIGURATIONS,                                /* Digital output channels have been specified but not enough digital output configurations have been provided. */
    QERR_MISSING_PWM_CONFIGURATIONS,                                    /* PWM output channels have been specified but not enough PWM configurations have been provided. */
    QERR_MISSING_PWM_ALIGNMENTS,                                        /* PWM output channels have been specified but not enough PWM alignments have been provided. */
    QERR_MISSING_PWM_POLARITIES,                                        /* PWM output channels have been specified but not enough PWM polarities have been provided. */
    QERR_MISSING_PWM_DEADBANDS,                                         /* PWM output channels have been specified but not enough PWM high-to-low or low-to-high deadband values have been provided. */
    QERR_INVALID_PWM_CONFIGURATION,                                     /* One of the PWM output configurations specified is not a valid configuration. Configurations must be in the range from 0 to 2 inclusive (0=independent, 1=complementary, 2=bipolar) */
    QERR_INVALID_PWM_ALIGNMENT,                                         /* One of the PWM output alignments specified is not a valid configuration. Configurations must be 0 (leading-edge-aligned), 1 (trailing-edge-aligned) or 2 (center-aligned) */
    QERR_INVALID_PWM_POLARITY,                                          /* One of the PWM output polarities specified is not a valid configuration. Configurations must be 1 (active high) or 0 (active low) */
    QERR_PWM_CONFIGURATION_NOT_SUPPORTED,                               /* One of the PWM output channels specified does not support the given PWM output configuration. For example, channel 7 of the QPID cannot be used in the complementary configuration as the primary channel because it is the last PWM channel. Alternatively, the given configuration may not be supported by the card at all. */
    QERR_INVALID_PWM_DEADBAND,                                          /* One of the PWM deadbands specified is negative. Deadband values must be non-negative. */
    QERR_BIPOLAR_PWM_ON_EVEN_CHANNELS_ONLY,                             /* The bipolar PWM configuration may only be configured on the even PWM channels for this card. See the card's documentation for details. */
    QERR_GPS_READ_FAILED,                                               /* A read of the GPS device failed. */
    QERR_PWM_ALIGNMENT_NOT_SUPPORTED,                                   /* One of the PWM output channels specified does not support the given PWM alignment. */
    QERR_PWM_POLARITY_NOT_SUPPORTED,                                    /* One of the PWM output channels specified does not support the given PWM polarity. */
    QERR_PWM_DEADBAND_NOT_SUPPORTED,                                    /* One of the PWM output channels specified does not support the given PWM deadband. */
    QERR_INVALID_CHANNEL_ORDER_FOR_BIPOLAR_PWM,                         /* The PWM output channels are not ordered correctly for the bipolar PWM output. Bipolar PWM outputs require that both the primary and secondary channel be written at the same time, and that the secondary channel be specified in the channel order immediately after the primary channel. */
    QERR_SUM_OF_PWM_DEADBANDS_EXCEEDS_PERIOD,                           /* The sum of the leading and trailing deadbands exceeds the PWM period. The deadbands cannot be so large that they exceed the PWM period. */
    QERR_PWM_MODES_NOT_ONE_SHOT,                                        /* At least one PWM channel is in one-shot mode, while others are not. The current card requires that all PWM channels be configured in one-shot mode, if this mode is used, not just some of the channels. */
    QERR_PWM_EXPIRATIONS_NOT_CONFIGURED,                                /* Some of the PWM output expiration states have not been configured. This board requires that if any of the expiration states have been configured then all the states must be configured, and the "Set PWM outputs when a watchdog timer expires" must be enabled. */
    QERR_PHANTOM_CANNOT_INITIALIZE,                                     /* Phantom block cannot initialize the device. */
    QERR_PHANTOM_SCHEDULER_ERROR,                                       /* Phantom block cannot start the Phantom API scheduler. */
    QERR_PHANTOM_SCHEDULER_RATE_ERROR,                                  /* Phantom API scheduler rate error. */
    QERR_PHANTOM_READ_FAILED,                                           /* Phantom block cannot read the outputs of the device. */
    QERR_PHANTOM_WRITE_FAILED,                                          /* Phantom block cannot write to inputs of the device. */
    QERR_PHANTOM_CANNOT_CLOSE,                                          /* Phantom block cannot close the device. */
    QERR_NO_PHANTOM_OMNI_LICENSE,                                       /* You do not have a valid license for the Phantom Omni blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_PHANTOM_DESKTOP_LICENSE,                                    /* You do not have a valid license for the Phantom Desktop blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_PHANTOM_PREMIUM_LICENSE,                                    /* You do not have a valid license for the Phantom Premium blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_PHANTOM_PREMIUM_6DOF_LICENSE,                               /* You do not have a valid license for the Phantom Premium 6DOF blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_VAL_QBOT_OPEN_FAILED,                                          /* Failed to open the Qbot VAL driver. */
    QERR_INVALID_KR5_SIXX_R850,                                         /* Invalid object. A KUKA robot object cannot be used after it has been closed. */
    QERR_KR5_SIXX_R850_COULD_NOT_OPEN_DEVICE,                           /* The KUKA robot device could not be opened. Make sure a 6-DOF KUKA robot is connected. */
    QERR_NO_KUKA_KR5_SIXX_R850_LICENSE,                                 /* You do not have a valid license for the KUKA RSI blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_VISION_INVALID_IMAGE_SIZE,                                     /* Invalid image dimension. */
    QERR_INVALID_HYMOTION_11000,                                        /* Invalid object. A HyMotion-11000 object cannot be used after it has been closed. */
    QERR_HYMOTION_11000_COULD_NOT_OPEN_DEVICE,                          /* The HyMotion-11000 could not be opened. Make sure the Rexroth HyMotion-11000 Motion System is connected. */
    QERR_NO_REXROTH_HYMOTION_11000_LICENSE,                             /* You do not have a valid license for the Rexroth HyMotion-11000 blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_INVALID_SHMEM_SCOPE,                                           /* The shmem protocol is designed for communicating between a real-time model and a foreground application. To use it for communicating between two Windows applications, the "local=true" option is required on the shmem URI. For example, "shmem://mymem:1?local=true". */
    QERR_NO_NATURALPOINT_OPTITRACK_LICENSE,                             /* You do not have a valid license for the NaturalPoint OptiTrack blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_VISUALIZATION_LICENSE,                                      /* You do not have a valid license for the Visualization blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_GPS_LICENSE,                                                /* You do not have a valid license for the GPS blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_INVALID_CIGI_HOST,                                             /* Invalid object. A CIGI host object cannot be used after it has been closed. */
    QERR_CIGI_HOST_COULD_NOT_OPEN_DEVICE,                               /* The CIGI Host could not be opened. */
    QERR_INVALID_DEFLATE_MODE,                                          /* The mode option specified for a deflate URI is invalid. */
    QERR_STATE_IS_NULL,                                                 /* The state argument is NULL. It should be a valid pointer. */
    QERR_WRONG_NUM_BYTES_POKED,                                         /* The wrong number of bytes have been sent to a persistent stream. Verify that the number of bytes configured when the stream was created matches the number of bytes sent. */
    QERR_WRONG_NUM_BYTES_PEEKED,                                        /* The wrong number of bytes have been received from a persistent stream. Verify that the number of bytes configured when the stream was created matches the number of bytes received. */
    QERR_NO_QBOT_LICENSE,                                               /* You do not have a valid license for the Qbot vehicle. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_UAV_LICENSE,                                                /* You do not have a valid license for the UAV components. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_PHANTOM_LIBRARY_OPEN_FAILED,                                   /* The SensAble PHANToM library failed to open. Make sure you have the OpenHaptics and PHANToM Device Driver software installed and the system PATH is set correctly. */
    QERR_WRONG_NUMBER_OF_INITIAL_VALUES,                                /* The wrong number of initial values were passed to visualization_open for the variables given. */
    QERR_INVALID_NEES,                                                  /* Invalid object. A NEES object cannot be used after it has been closed. */
    QERR_NEES_COULD_NOT_INITIALIZE,                                     /* The NEES block could not be initialized. */
    QERR_NEES_COULD_NOT_COMMUNICATE,                                    /* Could not communicate with the NEES daemon. */
    QERR_NEES_INVALID_DATA_FROM_DAEMON,                                 /* Received invalid data from the NEES daemon. */
    QERR_NEES_COULD_NOT_CLOSE,                                          /* Could not close the NEES block. */
    QERR_TCP_KEEPALIVES_NOT_SUPPORTED,                                  /* TCP/IP keep alive packets on individual socket connections does not appear to be supported. */
    QERR_CANNOT_SELECT_VARIABLE,                                        /* Variables cannot be selected after a visualization task has already been started. */
    QERR_INVALID_VARIABLE_NAME,                                         /* The variable indicated could not be found in the scene. */
    QERR_VARIABLE_ALREADY_SELECTED,                                     /* The variable has already been selected in the scene. Variables cannot be selected more than once. */
    QERR_INVALID_VARIABLE_DATATYPE,                                     /* The wrong data type is being used to set the value of the given variable. */
    QERR_QERR_CANNOT_SET_VARIABLE,                                      /* Variable values cannot be set until the visualization task has been started. Use the Visualization Start Task VI to start the task. */
    QERR_VARIABLE_NOT_SELECTED,                                         /* The given variable has not been selected for animation. Use the Visualization Select Variable VI to select the variable for animation prior to starting the visualization task. */
    QERR_VISUALIZATION_ALREADY_STARTED,                                 /* The visualization task has already been started. */
    QERR_UNABLE_TO_START_VIEWER,                                        /* The Quanser 3D Viewer could not be started. */
    QERR_INVALID_VISUALIZATION_HANDLE,                                  /* An invalid visualization handle was passed to a Visualization VI or function. */
    QERR_VIEWER_MAY_NOT_HAVE_EXITED,                                    /* The Quanser 3D Viewer may not have exited. An unexpected error may have occurred. */
    QERR_PCAN_CANNOT_INITIALIZE,                                        /* The Peak CAN device failed to initialize. Make sure the device is connected properly and the drivers and API have been installed. */
    QERR_WIIMOTION_PLUS_ACTIVATE_FAILED,                                /* The WiiMotion Plus extension failed to activate. Make sure the WiiMotion Plus extension is properly connected to the Wiimote. */
    QERR_WIIMOTION_PLUS_NOT_DETECTED,                                   /* The WiiMotion Plus extension was not detected. Make sure it is properly connected to the Wiimote. */
    QERR_WIIMOTE_EXT_CONTROLLER_CHECK_FAILED,                           /* Failed to read report for Wiimote extension controllers. Make sure your Wiimote is properly connected. */
    QERR_SOFTWARE_ALREADY_INSTALLED,                                    /* Another version of the software is already installed. Please uninstall the other version first. */
    QERR_NO_SPACE_ON_FILE_SYSTEM,                                       /* There is no space left on the file system. */
    QERR_FILE_SYSTEM_ERROR,                                             /* A physical I/O error occurred trying to access the file system. */
    QERR_INVALID_SETUP_OPERATION,                                       /* An invalid operation was detected in the installation database. The installation database appears to be corrupt. */
    QERR_PREMATURE_END_OF_FILE,                                         /* The end of the file was encountered prematurely. The file is corrupt. */
    QERR_PARTITION_NOT_FOUND,                                           /* The specified partition could not be found. Make sure you have created the partition and have enabled the appropriate scheduler. */
    QERR_PARTITIONING_SCHEDULER_NOT_RUNNING,                            /* The partitioning scheduler is not running. Be sure to set up your system to run the partitioning scheduler before attempting to use it. */
    QERR_JOINING_PARTITION_DENIED,                                      /* It was not possible to join the partition. Security constraints set up for partitioning do not allow it. */
    QERR_DIGITAL_EXPIRATION_STATE_TRISTATE_INVALID,                     /* This board does not support tristating the digital outputs when the watchdog expires. The digital outputs may only be set high or low on watchdog expiration. */
    QERR_INVALID_LICENSE_FOR_BUILDFILE,                                 /* The Configure Licensing tool can only generate a build file snippet for a network client license. Specify the -c option but not the -m option (client not server/manager) when configuring the license. */
    QERR_URI_OPTION_NOT_RECOGNIZED,                                     /* An option specified in the URI was not recognized as a valid option. */
    QERR_HIL_CONFLICTING_DIGITAL_OUTPUTS,                               /* Two or more digital outputs were specified with output values that conflict with one another. Refer to the device documentation for limitations. */
    QERR_DENSO_READ_TIMEOUT,                                            /* The Denso Read block has timed out since no data was received. Check that the IP settings of your PC are correct and that the PC is connected to the Denso controller. */
    QERR_NO_ROOM_IN_RECEIVE_BUFFER,                                     /* A communication protocol is being used that sends and receives data at the same time, such as SPI, and there is no room in the stream's receive buffer for the data that will be received during the send/flush operation. */
    QERR_NO_DATA_IN_RECEIVE_BUFFER,                                     /* A communication protocol is being used that sends and receives data at the same time, such as SPI, and there is no data in the stream's receive buffer to receive. A send/flush operation should be done first. The send/flush will receive data at the same time as data is sent and fill the receive buffer so that data can be received. */
    QERR_SPI_WRONG_BYTES_TO_SEND_AND_RECEIVE,                           /* The number of bytes being sent or received is not an integer multiple of the natural word size (1 bytes for 1-8 bits, 2 bytes for 9-16 bits and 4 bytes for 17-32 bit word lengths). */
    QERR_NO_SUCH_SPI_CHANNEL,                                           /* The SPI port specified in the URI is not available. */
    QERR_ONLY_SPI_MASTER_MODE_SUPPORTED,                                /* Only the SPI master mode is supported by the device being used for SPI communications. Different hardware is required for slave mode. */
    QERR_ONLY_SPI_MSB_FIRST_SUPPORTED,                                  /* The SPI device specified in the URI only supports sending and receiving the most-significant bit first. */
    QERR_NO_DENSO_LICENSE,                                              /* You do not have a valid license for the Denso blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_PTI_VISUALEYEZ_LICENSE,                                     /* You do not have a valid license for the PTI VisualEyez blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_PTI_VZSOFT_FAILED_TO_INITIALIZE,                               /* The VZSoft device failed to initialize. Make sure the system is setup properly and the VZSoft software is installed. */
    QERR_PTI_VZANALYZER_FAILED_TO_INITIALIZE,                           /* The VZAnalyzer device failed to initialize. Make sure the VZAnalyzer software is installed. */
    QERR_PWM_MODES_NOT_COMPATIBLE,                                      /* At least one PWM channel is in a mode that is incompatible with the other PWM channels. The current card has restrictions on the PWM modes. For example, the card may share the PWM period among all the channels so using duty cycle or time mode along with frequency or period mode is not permitted. See the card's documentation for details. */
    QERR_NP_TRACK_IR_OPEN_FAILED,                                       /* The TrackIR head tracker failed to initialize. Make sure that TrackIR is running and the Quanser Device ID is registered. Make sure the PATH environment variable is set correctly. */
    QERR_CANNOT_SET_POSITION,                                           /* The position of the stream cannot be set. */
    QERR_SEMAPHORE_COUNT_EXCEEDED,                                      /* A semaphore's maximum count has been reached. The semaphore cannot be signaled. */
    QERR_CONNECTION_REFUSED,                                            /* The remote peer refused the connection, most likely because no server application was listening for connections */
    QERR_MISSING_INTERRUPT_SOURCES,                                     /* No interrupt sources were specified even though the number of interrupt sources is nonzero. */
    QERR_MISSING_INTERRUPT_OCCURRED_BUFFER,                             /* Interrupt sources have been specified but not enough buffer space has been provided for the poll operation. */
    QERR_HIL_POLL_INTERRUPT_NOT_SUPPORTED,                              /* The hil_poll_interrupt function and HIL Poll Interrupt block are not supported by this particular card. */
    QERR_MONITOR_ARGUMENT_IS_NULL,                                      /* The monitor argument to a HIL function is NULL. */
    QERR_INVALID_MONITOR_HANDLE,                                        /* An invalid monitor handle was passed as an argument to a HIL function. */
    QERR_HIL_MONITOR_CREATE_INTERRUPT_READER_NOT_SUPPORTED,             /* The hil_monitor_create_interrupt_reader function and HIL Interrupt block are not supported by this particular card. */
    QERR_HIL_MONITOR_START_NOT_SUPPORTED,                               /* The hil_monitor_start function is not supported by this particular card. If the hil_monitor_create_interrupt_reader function is supported then the hil_monitor_stop function MUST be supported. Contact the device manufacturer. */
    QERR_HIL_MONITOR_STOP_NOT_SUPPORTED,                                /* The hil_monitor_stop function is not supported by this particular card. If the hil_monitor_create_interrupt_reader function is supported then the hil_monitor_stop function MUST be supported. Contact the device manufacturer. */
    QERR_HIL_MONITOR_DELETE_NOT_SUPPORTED,                              /* The hil_monitor_delete function is not supported by this particular card. If the hil_monitor_create_interrupt_reader function is supported then the hil_monitor_stop function MUST be supported. Contact the device manufacturer. */
    QERR_HIL_MONITOR_READ_INTERRUPT_NOT_SUPPORTED,                      /* The hil_monitor_read_interrupt function is not supported by this particular card. */
    QERR_INVALID_INTERRUPT_SOURCE,                                      /* One of the interrupt sources that was specified is not a valid interrupt source. Interrupt sources are typically divided into ranges according to functionality. Refer to the documentation for your card. */
    QERR_INVALID_INTERRUPT_OPERATION_HANDLE,                            /* An invalid interrupt operation handle was passed as an argument to the board-specific HIL driver. Once a monitor has been deleted using hil_monitor_delete the interrupt operation handle is invalid. */
    QERR_INTERRUPT_OPERATION_ARGUMENT_IS_NULL,                          /* The interrupt operation argument to a board-specific HIL driver is NULL. This situation should never occur unless the user is calling the board-specific driver directly or memory has been corrupted. */
    QERR_OPTITRACK_INVALID_LICENSE,                                     /* The license for the Optitrack tools being used is invalid or missing. Make sure you have configured your license. */
    QERR_OPTITRACK_FRAME_UPDATE_FAILED,                                 /* An attempt to process frames from Optitrack failed. See the QUARC console for additional information. */ /* An attempt to process frames from Optitrack failed. */
    QERR_TOO_MANY_INTERRUPT_SOURCES,                                    /* Too many interrupt sources were specified. */
    QERR_HIL_SET_CLOCK_FREQUENCY_NOT_SUPPORTED,                         /* The hil_set_clock_frequency function is not supported by this particular card. */
    QERR_VICON_CANNOT_CONNECT,                                          /* Cannot connect to the Vicon DataStream server. Check that the host name is correct and that the Tracker software is running. */
    QERR_VICON_FAILED_TO_SET_STREAM_MODE,                               /* The Vicon system failed to set the specified stream mode. Ensure the stream mode is valid and the Tracker software is running. */
    QERR_VICON_ENABLE_UNLABELED_MARKER_DATA_FAILED,                     /* The Vicon system failed to enable the unlabeled marker data stream. Make sure your system is connected and the Tracker software is running. */
    QERR_VICON_ENABLE_MARKER_DATA_FAILED,                               /* The Vicon system failed to enable the marker data stream. Make sure your system is connected and the Tracker software is running. */
    QERR_VICON_ENABLE_SEGMENT_DATA_FAILED,                              /* The Vicon system failed to enable the segment data stream. Make sure your system is connected and the Tracker software is running. */
    QERR_NO_VICON_LICENSE,                                              /* You do not have a valid license for the Vicon blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_DAQMX_ONLY_DEVICE_NAMES_SUPPORTED,                             /* Using a numeric board identifier for NI cards is not supported on this system. Please use the device name instead. */
    QERR_HIQ_BUILD_NUMBER_MISMATCH,                                     /* The HiQ firmware build number does not match the HiQ driver build number. Make sure your HiQ driver version is compatible with the HiQ hardware. */
    QERR_INVALID_HOST_PACKET,                                           /* A Host block appears to be incompatible with the current version of QUARC because it has sent invalid data. It may be necessary to rebuild the model. */ /* A Host block appears to be incompatible with the current version of QRCP because it has sent invalid data. It may be necessary to recompile the VI. */
    QERR_DRIVER_TIMED_OUT,                                              /* The HIL driver timed out trying to communicate with the card. The card may not be working or the version of the driver may not be compatible with the version of the card. */
    QERR_V4L2_VIDIOC_QBUF_FAILED,                                       /* Failed to enqueue a buffer with the video driver's incoming queue. */
    QERR_V4L2_COULD_NOT_CLOSE,                                          /* Failed to close the video driver. */
    QERR_V4L2_DEVICE_MISSING,                                           /* The specified video device could not be found. */
    QERR_V4L2_QUERY_FAILED,                                             /* Unable to query the video driver for its status. */
    QERR_V4L2_NOT_CAP_DEVICE,                                           /* The device does not support video capture. */
    QERR_V4L2_NOT_STREAMING_DEVICE,                                     /* The device does not support video streaming. */
    QERR_V4L2_FORMAT_NOT_VALID,                                         /* The image format is not valid for the device.  */
    QERR_V4L2_VIDIOC_REQBUFS_FAILED,                                    /* Failed to initiate memory-mapped or user-pointer I/O for the video device. */
    QERR_V4L2_VIDIOC_STREAM_FAILED,                                     /* Failed to start or stop video capture or streaming. */
    QERR_CASPA_CAPTURE_FAILED,                                          /* Failed to capture video. */
    QERR_CARD_NOT_ACTIVE,                                               /* The card is not valid. It may not have been made active during normal simulation in the HIL Initialize block and thus may be uninitialized. */
    QERR_AUTOPILOT_NOT_ACTIVE,                                          /* The autopilot is not valid. It may not have been made active during normal simulation in the VAL Initialize block and thus may be uninitialized. */
    QERR_PCAN_INVALID_CHANNEL,                                          /* The channel number specified for the Peak CAN device is not valid. Make sure the correct device type is selected and the channel number is valid. */
    QERR_PCAN_SET_MESSAGE_FILTER_FAILED,                                /* The Peak CAN device failed to set the message filter. Make sure the message IDs requested are valid. */
    QERR_INCOMPATIBLE_TARGET_TYPE,                                      /* The code being downloaded or run is not compatible with the type of target referenced by the target URI. For example, 32-bit code cannot be downloaded to a 64-bit target or vice versa. In Simulink, make sure the system target file selected in the model's active configuration is compatible with the target referred to by the target URI. */ /* The code being downloaded or run is not compatible with the type of target referenced by the target URI. */
    QERR_PCAN_WRITE_FAILED,                                             /* The Peak CAN device failed to write a message. Make sure you are connected to a CAN network with proper CAN bus termination resistance and that your baud rate is correct. */
    QERR_JACO_INVALID_JOINT,                                            /* The joint specified for the Jaco device is outside the valid range. */
    QERR_JACO_JOINT_INITIALIZATION_FAILED,                              /* Unable to initialize one of the Jaco joints. Make sure that the Jaco cables are properly connected, the emergency stop is released, and the Jaco power is on. */
    QERR_JACO_ACK_NOT_RECEIVED,                                         /* Jaco did not send an acknowledge message when one was expected. */
    QERR_SHARING_VIOLATION,                                             /* The process cannot access the file or object because it is being used by another process. */
    QERR_JACO_READ_FAILED,                                              /* Failed to read CANbus for the Jaco. Check that the CAN cables are properly connected, the emergency stop is released, and the Jaco power is on. */
    QERR_JACO_JOINT_ADDRESS_INVALID,                                    /* The Jaco joint address is invalid. */
    QERR_NO_ROBOTICS_LICENSE,                                           /* You do not have a valid license for the Robotics blockset you are using. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_INVALID_HOST,                                                  /* The host passed as an argument is invalid. It is likely NULL, indicating the host may not be not connected or listening. */
    QERR_JACO_READ_TIMEOUT,                                             /* A JACO read timeout expired. */
    QERR_JACO_SHUTDOWN,                                                 /* Unable to complete the operation because the JACO is shutting down. */
    QERR_PERIPHERAL_NOT_FOUND,                                          /* A peripheral device could not be found. It is possible the device is unplugged or otherwise inoperable. */
    QERR_ENVIRONMENT_VARIABLE_NOT_FOUND,                                /* The environment variable could not be found. */
    QERR_VIS_CANNOT_CREATE_FRAME_TIMER,                                 /* An error occured creating the frame-rate timer. */
    QERR_VIS_CANNOT_CREATE_VISUALIZATION_WINDOW,                        /* An error occured creating the visualization window. */
    QERR_VIS_CANNOT_REGISTER_WINDOW,                                    /* An error occured while attempting to register the windows class.  Windows error code %d. */
    QERR_VIS_CANNOT_GET_WINDOW_DC,                                      /* Cannot create device context.  Windows error %d. */
    QERR_VIS_FAILED_TO_SWITCH_TO_FULL_SCREEN,                           /* Could not switch to requested fullscreen mode. */
    QERR_VIS_CANNOT_FIND_SUITABLE_PIXEL_FORMAT,                         /* Cannot find suitable OpenGL pixel format. */
    QERR_VIS_CANNOT_SET_PIXEL_FORMAT,                                   /* Cannot set OpenGL pixel format. */
    QERR_VIS_CANNOT_CREATE_OPENGL_CONTEXT,                              /* Cannot create OpenGL context. */
    QERR_VIS_CANNOT_CREATE_EXTENDED_OPENGL_CONTEXT,                     /* Could not create a rendering context for the requested OpenGL version (%1.1f).  A different OpenGL version or updating your video drivers may resolve the issue. */
    QERR_VIS_CANNOT_MAKE_OPENGL_CONTEXT,                                /* Cannot make the specified OpenGL context the current context. */
    QERR_VIS_CANNOT_MAKE_EXTENDED_OPENGL_CONTEXT,                       /* Could not make the specified OpenGL context the current context for the requested OpenGL version (%1.1f). A different OpenGL version or updating your video drivers may resolve the issue. */
    QERR_VIS_UNABLE_TO_SWAP_GRAPHICS_BUFFERS,                           /* Unable to swap graphics buffers. */
    QERR_VIS_TOO_MANY_LIGHTS_IN_SCENE,                                  /* Too many lights in scene. A maximum of %d lights are supported by OpenGL. */
    QERR_VIS_CANNOT_FIND_VALID_X3D_MESH,                                /* Cannot find a valid X3D mesh in %s. */
    QERR_VIS_CANNOT_FIND_SPECIFIED_SHAPE_IN_X3D_MESH,                   /* Shape %d could not be found in %s. */
    QERR_VIS_CANNOT_FIND_SPECIFIED_ATTRIBUTE_IN_X3D_MESH,               /* Attribute %s could not be found in %s. */
    QERR_VIS_INVALID_SCENE_FILE_FORMAT,                                 /* Invalid XML scene file. */
    QERR_VIS_INVALID_MESH_FILE_FORMAT,                                  /* Invalid mesh file. */
    QERR_VIS_UNSUPPORTED_TEXTURE_FORMAT,                                /* The selected texture file %s is not a supported file type. */
    QERR_VIS_TEXTURE_NOT_POWER_OF_2,                                    /* To improve rendering efficiency, only textures with dimensions that are a power of 2 are supported (eg 512, 1024, 2048, etc).  Rectangular bitmaps are acceptable though (eg 512 x 1024). */
    QERR_VIS_TEXTURE_FILE_FORMAT_INVALID,                               /* The texture file is recognized, but the file is not in an expected format */
    QERR_VIS_TEXTURE_FILE_INVALID_COLOR_DEPTH,                          /* The texture file appears to be valid, but the color depth specified in this file is not supported.*/
    QERR_VIS_TEXTURE_FILE_INVALID_COMPRESSION,                          /* The texture file appears to be valid, but the compression scheme used is not supported. */
    QERR_VIS_OPENGL_REQUIRED_EXTENSION_NOT_FOUND,                       /* A necessary extension was not found for the requested OpenGL version (%1.1f).  Updating your video drivers may solve the issue. */
    QERR_VIS_MESH_INVALID_SHAPE_REFERENCE,                              /* The shape parameter specified for the mesh %s in the scene file must be greater or equal to zero. */
    QERR_VIS_MESH_INVALID_FACE_COUNT,                                   /* The face parameter specified for the mesh %s in the scene file must be an integer. */
    QERR_VIS_MESH_INVALID_STRIDE,                                       /* The stride parameter specified for the mesh %s, attribute %s in the scene file must be greater than zero. */
    QERR_VIS_MESH_INVALID_NUMBER_OF_ATTRIBUTE_ELEMENTS,                 /* The number of attribute elements was not the expected stride. */
    QERR_VIS_MESH_INVALID_NUMBER_OF_INDICES,                            /* The indices are expected to be a group of 4 numbers for each face. */
    QERR_VIS_MESH_INVALID_NUMBER_OF_NORMALS,                            /* The normals are expected to be a group of 3 numbers for each vertex. */
    QERR_VIS_MESH_INVALID_NUMBER_OF_TEXTURE_COORDINATES,                /* The texture coordinates are expected to be a group of 2 numbers for each vertex. */
    QERR_VIS_MESH_INVALID_NUMBER_OF_VERTICES,                           /* The vertices are expected to be in groups of 3 numbers. */
    QERR_VIS_MESH_INVALID_INDICES_INDEX,                                /* An index references a vertex that is outside of the expected range. */
    QERR_VIS_MESH_ATTRIBUTE_NOT_EQUAL_TO_OTHER_VERTICES,                /* The attribute %s in mesh %s has %d elements which does not match the %d elements found in other attributes or the vertices count in the scene file.  If the mesh is marked as a flexible mesh, try rescanning the mesh file to recount the vertices or uncheck the flexible mesh property.*/
    QERR_VIS_SHADER_VERTEX_NOT_SET,                                     /* The vertex shader has not been specified for %s. */
    QERR_VIS_SHADER_FRAGMENT_NOT_SET,                                   /* The fragment shader has not been specified for %s. */
    QERR_VIS_SHADER_VERTEX_COMPILE_FAILED,                              /* Failed to compile the vertex shader file %s. */
    QERR_VIS_SHADER_FRAGMENT_COMPILE_FAILED,                            /* Failed to compile the fragment shader file %s. */
    QERR_VIS_SHADER_NOT_COMPILED,                                       /* Internal error.  The graphics engine has attempted to use a shader that has not yet been successfully compiled. */
    QERR_VIS_OLD_SCENE_FILE_VERSION,                                    /* The scene file appears to be valid, but the version (%2.2f) is not compatible with the installed version of QUARC.  Version %2.2f was expected.  Please regenerate the scene file from your diagram. */ /* The scene file appears to be valid, but the version (%2.2f) is not compatible with the installed version of QRCP.  Version %2.2f was expected.  Please regenerate the scene file from your diagram. */
    QERR_VIS_UNRECOGNIZED_SCENE_FILE_VERSION,                           /* The scene file appears to be valid, but the version (%2.2f) is from a newer version of QUARC.  Please upgrade this viewer to the most recent version.  If this viewer is being used independently of QUARC, an installer for just the viewer is available on the QUARC DVD. */ /* The scene file appears to be valid, but the version (%2.2f) is from a newer version of QRCP.  Please upgrade this viewer to the most recent version.  If this viewer is being used independently of QRCP, an installer for just the viewer is available on the QRCP DVD. */
    QERR_VIS_SCENE_BACKGROUND_COLOR_INVALID,                            /* Invalid background color in the scene file. */
    QERR_VIS_SCENE_AMBIENT_COLOR_INVALID,                               /* Invalid ambient color specified in the scene file. */
    QERR_VIS_SCENE_FRAMERATE_INVALID,                                   /* Invalid frame rate specified in scene file. */
    QERR_VIS_SCENE_WIDTH_INVALID,                                       /* Invalid screen width specified in scene file. */
    QERR_VIS_SCENE_HEIGHT_INVALID,                                      /* Invalid screen height specified in scene file. */
    QERR_VIS_SCENE_MESH_ID_DUPLICATE,                                   /* A duplicate mesh ID %s was found.  All mesh ID's must be unique. */
    QERR_VIS_SCENE_MESH_ATTRIBUTE_ID_DUPLICATE,                         /* A duplicate mesh attribute ID %s was found was found in mesh %s.  All mesh attribute ID's must be unique. */
    QERR_VIS_SCENE_TEXTURE_ID_DUPLICATE,                                /* A duplicate texture ID %s was found.  All mesh ID's must be unique. */
    QERR_VIS_SCENE_SHADER_ID_DUPLICATE,                                 /* A duplicate shader ID %s was found.  All shader ID's must be unique. */
    QERR_VIS_SCENE_SHADER_VARIABLE_ID_DUPLICATE,                        /* A duplicate shader variable ID %s was found in shader %s.  Shader variable ID's must be unique within each shader. */
    QERR_VIS_SCENE_SHADER_ATTRIBUTE_ID_DUPLICATE,                       /* A duplicate shader attribute ID %s was found in shader %s.  Shader attribute ID's must be unique within each shader. */
    QERR_VIS_SCENE_NEAR_CLIPPING_INVALID,                               /* Near clipping plane must greater than or equal to 0. */
    QERR_VIS_SCENE_FAR_CLIPPING_INVALID,                                /* Near clipping plane must greater than 0. */
    QERR_VIS_SCENE_NEAR_FAR_COMBINATION_INVALID,                        /* Far clipping plane must be greater than the near clipping plane. */
    QERR_VIS_SCENE_VIEW_ANGLE_INVALID,                                  /* Camera viewing angle must greater than 0. */
    QERR_VIS_SCENE_KEYBOARD_CAMERA_CONTROL_KEY_INVALID,                 /* Unrecognized camera control key. */
    QERR_VIS_SCENE_MOUSE_CAMERA_CONTROL_KEY_INVALID,                    /* Unrecognized mouse button. */
    QERR_VIS_SCENE_GESTURE_CAMERA_CONTROL_KEY_INVALID,                  /* Unrecognized gesture control. */
    QERR_VIS_SCENE_FOG_MODE_INVALID,                                    /* The fog mode must be either linear, exp, or exp2. */
    QERR_VIS_SCENE_FOG_DENSITY_INVALID,                                 /* The fog density must defined and greater or equal to 0. */
    QERR_VIS_SCENE_FOG_COLOR_INVALID,                                   /* Invalid fog color. */
    QERR_VIS_SCENE_FOG_START_INVALID,                                   /* The fog start must greater or equal to 0. */
    QERR_VIS_SCENE_FOG_END_INVALID,                                     /* The fog end must greater than fog start. */
    QERR_VIS_SCENE_FOG_START_OR_END_UNDEFINED,                          /* If linear fog is used, the start and end distances must be defined. */
    QERR_VIS_SCENE_OPENGL_VERSION_INVALID,                              /* The requested OpenGL version number must greater or equal to 1.0. */
    QERR_VIS_SCENE_OBJECT_REFERENCES_UNKNOWN_MESH_ID,                   /* Object %s references an unknown mesh ID %s. */
    QERR_VIS_SCENE_OBJECT_REFERENCES_UNKNOWN_TEXTURE_ID,                /* Object %s references an unknown texture ID %s. */
    QERR_VIS_SCENE_OBJECT_ID_DUPLICATE,                                 /* A duplicate object ID %s was found.  All object ID's must be unique. */
    QERR_VIS_SCENE_ACTOR_REFERENCES_UNKNOWN_MESH_ID,                    /* Actor %s references an unknown mesh ID %s. */
    QERR_VIS_SCENE_ACTOR_REFERENCES_UNKNOWN_TEXTURE_ID,                 /* Actor %s references an unknown texture ID %s. */
    QERR_VIS_SCENE_ACTOR_REFERENCES_UNKNOWN_OBJECT_ID,                  /* Actor %s references an unknown object ID %s. */
    QERR_VIS_SCENE_ACTOR_REFERENCES_UNKNOWN_SHADER_ID,                  /* Actor %s references an unknown shader ID %s. */
    QERR_VIS_SCENE_ACTOR_REFERENCES_UNKNOWN_SHADER_VARIABLE_ID,         /* Actor %s references an unknown shader variable ID %s in shader %s. */
    QERR_VIS_SCENE_ACTOR_MISSING_SHADER_ID,                             /* Actor %s is missing a Shader reference. */
    QERR_VIS_SCENE_ACTOR_ID_DUPLICATE,                                  /* A duplicate actor ID %s was found.  All actor ID's must be unique. */
    QERR_VIS_SCENE_ACTOR_TYPE_UNKNOWN,                                  /* Actor type %s not recognized. */
    QERR_VIS_SCENE_ACTOR_POSITION_INVALID,                              /* Actor %s's position invalid. */
    QERR_VIS_SCENE_ACTOR_SCALE_INVALID,                                 /* Actor %s's scale invalid. */
    QERR_VIS_SCENE_ACTOR_FOG_INVALID,                                   /* Actor %s's fog override must be true or false. */   
    QERR_VIS_SCENE_ACTOR_ORIENTATION_INVALID,                           /* Actor %s's orientation invalid. */
    QERR_VIS_SCENE_ACTOR_CHILD_AND_SIBLING_PROCESSING_ERROR,            /* An internal error has occured processing the actor relationships.  Please report this error to Quanser.*/
    QERR_VIS_SCENE_ACTOR_INHERITANCE_INVALID,                           /* Actor %s's inheritance must be true or false.*/
    QERR_VIS_SCENE_ACTOR_COLOR_INVALID,                                 /* Actor %s's color invalid. */
    QERR_VIS_SCENE_ACTOR_EMISSIVE_INVALID,                              /* Actor %s's emissivity value invalid. */
    QERR_VIS_SCENE_ACTOR_SPECULAR_INVALID,                              /* Actor %s's specularity invalid. */
    QERR_VIS_SCENE_ACTOR_SHININESS_INVALID,                             /* Actor shininess invalid. */
    QERR_VIS_SCENE_ACTOR_ID_NOT_FOUND,                                  /* Actor ID not found.*/
    QERR_VIS_ACTOR_MESH_POOL_NOT_INITIALIZED,                           /* Internal error.  Failed attempted to attach a mesh to an actor because the mesh pool is not initialized. */
    QERR_VIS_ACTOR_TEXTURE_POOL_NOT_INITIALIZED,                        /* Internal error.  Failed attempted to attach a mesh to an actor because the texture pool is not initialized. */
    QERR_VIS_ACTOR_MESH_OUTSIDE_OF_MESH_POOL_BOUNDS,                    /* Attempted to attach a mesh that is outside of the array bounds of loaded meshes.*/
    QERR_VIS_ACTOR_TEXTURE_OUTSIDE_OF_TEXTURE_POOL_BOUNDS,              /* Attempted to attach a texture that is outside of the array bounds of loaded textures. */
    QERR_VIS_WRONG_MAGIC_NUMBER,                                        /* The connection was successful, but the received data was not in the expected format. */
    QERR_VIS_COMM_ACTOR_REFERENCE_NOT_VALID,                            /* The communications stream refers to more actors than exist in the scene file. */
    QERR_VIS_COMM_ACTOR_PARAMETER_NOT_VALID,                            /* The communications stream refers to an invalid actor parameter. */
    QERR_VIS_COMM_DATA_STREAM_PAYLOAD_NOT_OF_EXPECTED_SIZE,             /* Data stream payload is an unexpected size. */
    QERR_VIS_COMM_RECEIVE_BUFFER_TOO_SMALL,                             /* The receive buffer is too small for the volume of data needed each frame.  Increase the receive buffer size then retry communications. */
    QERR_VIS_COMM_RECEIVE_BUFFER_SIZE_INVALID,                          /* The receive buffer size is invalid */
    QERR_VIS_COMM_SEND_BUFFER_SIZE_INVALID,                             /* The send buffer size is invalid */
    QERR_VIS_COMM_CONFIGURATION_PAYLOAD_NOT_OF_EXPECTED_SIZE,           /* Configuration payload is an unexpected size. */
    QERR_VIS_OLDER_QUARC_VERSION,                                       /* The connection was successful, but the model was compiled with an older version of QUARC that is incompatible. Rebuild the model to make it compatible with the current version. */ /* The connection was successful, but the model was compiled with an older version of QRCP that is incompatible. Rebuild the model to make it compatible with the current version. */
    QERR_MULTISAMPLE_OPERATION_NOT_SUPPORTED_DURING_DECIMATED_SAMPLING, /* Multiple samples for the selected task operation are not supported with decimated sampling by this board.  Either set the decimation or the number of samples to 1. */
    QERR_HIL_SET_ANALOG_TERMINATION_STATE_NOT_SUPPORTED,                /* The hil_set_analog_termination_state function is not supported by this particular card. */
    QERR_HIL_SET_DIGITAL_TERMINATION_STATE_NOT_SUPPORTED,               /* The hil_set_digital_termination_state function is not supported by this particular card. */
    QERR_HIL_SET_PWM_TERMINATION_STATE_NOT_SUPPORTED,                   /* The hil_set_pwm_termination_state function is not supported by this particular card. */
    QERR_HIL_SET_OTHER_TERMINATION_STATE_NOT_SUPPORTED,                 /* The hil_set_other_termination_state function is not supported by this particular card. */
    QERR_HIL_AT_LEAST_ONE_CHANNEL_REQUIRED,                             /* The HIL function requires at least one channel to be specified. */
    QERR_HIL_INVALID_DIGITAL_DIRECTIONS,                                /* The combination of directions specified for the digital channels are not compatible with the capabilities of this particular card. Some cards have digital channels organized into ports for which all channels in a port must have the same direction. Check the documentation for the card. */ 
    QERR_HIL_WRITE_TERMINATION_STATES_NOT_SUPPORTED,                    /* The hil_write_termination_states function is not supported by this particular card. */
    QERR_RCP_INVALID_SMOOTH_GEN_FREQUENCY,                              /* The Smooth Signal Generator does not support the frequency entered. */
    QERR_RCP_INVALID_SMOOTH_GEN_AMPLITUDE,                              /* The Smooth Signal Generator does not support the amplitude entered. */
    QERR_RCP_INVALID_SMOOTH_GEN_INPUT_SIZE,                             /* The input array sizes should be equal and non-zero for the Smooth Signal Generator. */
    QERR_RCP_INVALID_SIGMOID_SAMPLE_TIME,                               /* The sample time is not valid for the Sigmoid VI. */
    QERR_MISMATCHED_SCHEDULING_POLICY,                                  /* The scheduling policy for the thread must match the system scheduling policy on this target operating system. */
    QERR_HIL_DRIVER_NOT_FOUND,                                          /* Support for the given board type does not appear to be installed. Verify that you have selected the correct card in the HIL Initialize block or hil_open function. */
    QERR_HIL_UNABLE_TO_READ_BITFILE,                                    /* The FPGA bitfile could not be read. Make sure the FPGA bitfile is actually installed on the target. */
    QERR_HIL_INVALID_FPGA_SIGNATURE,                                    /* The specified signature does not match the signature of the bitfile. If the bitfile has been recompiled, regenerate the C API and rebuild the application. */
    QERR_HIL_INVALID_RESOURCE_NAME,                                     /* Either the supplied resource name is invalid as a RIO resource name, or the device was not found. Use MAX to find the proper resource name for the intended device. */
    QERR_FORCE_DIMENSION_OPEN_FAILED,                                   /* An attempt to open a Force Dimension haptic device failed. Ensure that the Force Dimension device is powered on and has been calibrated. */
    QERR_FORCE_DIMENSION_READ_FAILED,                                   /* An attempt to read from the Force Dimension haptic device failed. */
    QERR_FORCE_DIMENSION_WRITE_FAILED,                                  /* An attempt to write to the Force Dimension haptic device failed. */
    QERR_FORCE_DIMENSION_CLOSE_FAILED,                                  /* An attempt to close a Force Dimension haptic device failed. */
    QERR_FORCE_DIMENSION_NOT_CALIBRATED,                                /* The Force Dimension haptic device has not been calibrated. Ensure that the device is properly calibrated before use. */
    QERR_NO_FORCE_DIMENSION_LICENSE,                                    /* You do not have a valid license for the Force Dimension blockset. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_RCP_CHASSIS_NOT_FOUND,                                         /* The driver could not determine the chassis attached to the real-time controller. */
    QERR_RCP_CHASSIS_NOT_SUPPORTED,                                     /* The NI chassis currently in use is not supported by this particular driver. Check the documentation to ensure a compatible chassis is in use. */
    QERR_RCP_INCORRECT_MODULE,                                          /* One or more of the modules in the NI chassis do not match the hardware configuration selected in the HIL Initialize. Be sure the correct modules are being used. Please correct the hardware configuration or select the proper configuration in the HIL Initialize block. */
    QERR_RCP_MODULE_IO_ERROR,                                           /* One or more of the modules in the NI chassis is causing an error which prevents I/O from being performed. */
    QERR_FPGA_ALREADY_RUNNING,                                          /* The FPGA is already running. */
    QERR_RESOURCE_NOT_INITIALIZED,                                      /* A required resource was not initialized. */
    QERR_CORRUPT_FPGA_BITFILE,                                          /* The specified bitfile is invalid or corrupt. */
    QERR_FPGA_BUSY,                                                     /* Operation could not be performed because the FPGA is busy. Stop all the activities on the FPGA before requesting this operation. */
    QERR_FPGA_BUSY_C_API,                                               /* Operation could not be performed because the FPGA is busy operating in FPGA Interface C API mode. Stop all the activities on the FPGA before requesting this operation. */
    QERR_FPGA_BUSY_SCAN_INTERFACE,                                      /* The chassis is in Scan Interface programming mode. In order to run FPGA VIs, you must go to the chassis properties page, select FPGA programming mode, and deploy settings. */
    QERR_FPGA_BUSY_FPGA_INTERFACE,                                      /* Operation could not be performed because the FPGA is busy operating in FPGA Interface mode. Stop all the activities on the FPGA before requesting this operation. */
    QERR_FPGA_BUSY_INTERACTIVE,                                         /* Operation could not be performed because the FPGA is busy operating in Interactive mode. Stop all the activities on the FPGA before requesting this operation. */
    QERR_FPGA_BUSY_EMULATION,                                           /* Operation could not be performed because the FPGA is busy operating in Emulation mode. Stop all the activities on the FPGA before requesting this operation. */
    QERR_QBUS_NO_MODULES_FOUND,                                         /* No QBus modules could be detected. */
    QERR_QBUS_UNRECOGNIZED_MODULE,                                      /* An unrecognized QBus module was found. */
    QERR_SPI_INSUFFICIENT_BYTES_TO_SEND_AND_RECEIVE,                    /* The given buffer is too small to do a single send or receive for this protocol. The protocol uses a word length larger than the number of bytes supplied. */
    QERR_PARITY_NOT_SUPPORTED,                                          /* The selected serial port does not support parity checking. Set the parity option on the URI to 'none'. */
    QERR_HARDWARE_FLOW_CONTROL_NOT_SUPPORTED,                           /* The selected serial port does not support hardware flow control. Set the flow option on the URI to 'none' or 'software' (if supported). */
    QERR_SOFTWARE_FLOW_CONTROL_NOT_SUPPORTED,                           /* The selected serial port does not support software flow control. Set the flow option on the URI to 'none' or 'hardware' (if supported). */
    QERR_DTR_DSR_NOT_SUPPORTED,                                         /* The selected serial port does not support the data-terminal-ready (DTR) and data-set-ready (DSR) lines. Set the dsr option on the URI to 'off'. */
    QERR_PARITY_VALUE_NOT_SUPPORTED,                                    /* The value specified for the parity is not supported by the given serial port. Use a different parity setting if possible or select 'none' for no parity checking. */
    QERR_STOP_BITS_VALUE_NOT_SUPPORTED,                                 /* The value specified for the stop bits is not supported by the given serial port. Use a different number of stop bits if possible. A value of 1 is recommended. */
    QERR_WORD_LENGTH_VALUE_NOT_SUPPORTED,                               /* The value specified for the word length is not supported by the given serial port. Use a different word length if possible. A value of 8 is recommended. */
    QERR_NO_DATA_TO_SEND,                                               /* There is no data to send. It is not possible to send zero-length arrays. If data will never be sent then configure the send options to not send data at all. Setting the enable input to false is not enough because the enable input is only intended to temporarily enable or disable transmission. If the stream is configured to send data then a valid data type must be connected even if the enable input is false. */
    QERR_RCP_MISSING_MODULE,                                            /* One or more of the modules in the NI chassis that is required by the hardware configuration selected in the HIL Initialize is missing. Please correct the hardware configuration or select the proper configuration in the HIL Initialize block. */
    QERR_RCP_MISSING_ANALOG_INPUT_MODULE,                               /* The module in the NI chassis required for the selected channels of analog input is missing. */
    QERR_RCP_MISSING_ANALOG_OUTPUT_MODULE,                              /* The module in the NI chassis required for the selected channels of analog output is missing. Make sure these channels are not being written by the HIL Initialize block by unchecking the Initial and Final output fields of the Analog Outputs tab. */
    QERR_RCP_MISSING_ENCODER_INPUT_MODULE,                              /* The module in the NI chassis required for the selected channels of encoder input is missing. */
    QERR_RCP_MISSING_PWM_OUTPUT_MODULE,                                 /* The module in the NI chassis required for the selected channels of PWM output is missing. Make sure these channels are not being written by the HIL Initialize block by unchecking the Initial and Final output fields of the PWM Outputs tab. */
    QERR_RCP_MISSING_DIGITAL_INPUT_MODULE,                              /* The module in the NI chassis required for the selected channels of digital input is missing. */
    QERR_RCP_MISSING_DIGITAL_OUTPUT_MODULE,                             /* The module in the NI chassis required for the selected channels of digital output is missing. Make sure these channels are not being written by the HIL Initialize block by unchecking the Initial and Final output fields of the Digital I/O tab. */
    QERR_RCP_MISSING_OTHER_INPUT_MODULE,                                /* The module in the NI chassis required for the selected channels of other input is missing. */
    QERR_RCP_MISSING_OTHER_OUTPUT_MODULE,                               /* The module in the NI chassis required for the selected channels of other output is missing. Make sure these channels are not being written by the HIL Initialize block by unchecking the Initial and Final output fields of the Other Outputs tab. */
    QERR_DEVICE_NOT_CONNECTED,                                          /* The device is not connected. If the device was connected then somehow that connection has been lost. */
    QERR_TOO_MANY_PROPERTIES,                                           /* Too many properties were specified. */
    QERR_PSTREAM_NOT_VARIABLE_SIZE,                                     /* The persistent stream has not been configured for variable-size signals in the direction attempted. */
    QERR_PSTREAM_VARIABLE_SIZE,                                         /* The persistent stream has been configured for variable-size signals in the direction attempted. */
    QERR_INVALID_DIMENSIONS,                                            /* The dimensions exceed the maximum dimensions specified. */
    QERR_LEAPMOTION_NOT_FOUND,                                          /* The Leap Motion device cannot be found on the system. */
    QERR_CANNOT_RESET_ENCODER_TO_NONZERO_VALUE,                         /* The encoder cannot be reset to a non-zero value on this device. */
    QERR_ENCODER_INPUT_ERROR,                                           /* An error has occurred reading an encoder input. Make sure the encoder is connected reliably, there are no ground loops and signal noise is minimized. */
    QERR_STALL_OCCURRED,                                                /* A stall condition was detected. Please ensure that your device is free to move and is functioning properly. */
    QERR_ONLY_I2C_MASTER_MODE_SUPPORTED,                                /* Only the I2C master mode is supported by the device being used for I2C communications. Different hardware is required for slave mode. */
    QERR_NO_DEVICE_ADDRESS,                                             /* No device address was specified. See the options for the communications protocol. */
    QERR_NO_ACKNOWLEDGEMENT,                                            /* Device did not send an acknowledgement. Device may not be present or an error may have occurred. */
    QERR_NO_KINECT_SENSOR,                                              /* No Kinect sensor was detected with the given index or identifier. */
    QERR_INVALID_KINECT,                                                /* Invalid Kinect sensor. */
    QERR_KINECT_NOT_FOUND,                                              /* The corresponding Kinect Initialize could not be found. Make sure that a Kinect Initialize block is present in the model. */
    QERR_KINECT_FEATURE_NOT_ENABLED,                                    /* The Kinect has been initialized without at least one of the requested features. Some of the features will not be available. */
    QERR_KINECT_NOT_INITIALIZED,                                        /* The Kinect sensor has not been initialized. */
    QERR_KINECT_ALREADY_INITIALIZED,                                    /* The Kinect sensor is already initialized so the requested settings can no longer be configured. Set options before calling the kinect_initialize function. */
    QERR_RESOLUTION_NOT_SUPPORTED,                                      /* The selected image resolution is not supported. */
    QERR_NO_SPI_CHIP_SELECT,                                            /* No SPI chip select signal was chosen using the frame or slave options of the URI. The current hardware requires that a chip select be used. */
    QERR_MULTIPLE_SPI_CHIP_SELECTS,                                     /* More than one SPI chip select signal was chosen by setting both the frame and slave options of the URI. The current hardware does not support both at the same time. Choose one or the other. */
    QERR_UNSUPPORTED_I2C_OPERATION,                                     /* The I2C protocol for the selected target only supports combined write-read messages. Other combinations of read and write operations are not supported in exclusive mode. */
    QERR_DIGITAL_EXPIRATION_STATE_NOT_ZERO,                             /* This board only supports resetting the digital outputs to zero when the watchdog expires. */
    QERR_PWM_EXPIRATION_STATE_NOT_ZERO,                                 /* This board only supports resetting the PWM outputs to zero when the watchdog expires. */
    QERR_OTHER_EXPIRATION_STATE_NOT_ZERO,                               /* This board only supports resetting the other outputs to zero when the watchdog expires. */
    QERR_KINECT_NOT_SUPPORTED,                                          /* The type of Kinect selected is not currently supported on this target. */
    QERR_INVALID_MICO,                                                  /* Invalid object. A Kinova MICO robot object cannot be used after it has been closed. */
    QERR_MICO_INVALID_JOINT,                                            /* The joint specified for the Kinova MICO device is outside the valid range. */
    QERR_MICO_MESSAGE_INVALID,                                          /* The Kinova MICO serial link message is invalid. */
    QERR_MICO_FIRMWARE_VERSION_NOT_READ,                                /* The Kinova MICO firmware version could not be read. Ensure the robot arm is powered up and properly connected to the external computer. */
    QERR_MICO_FIRMWARE_VERSION_NOT_SUPPORTED,                           /* The Kinova MICO joint and/or finger firmware version number is not supported. */
    QERR_MICO_ERROR,                                                    /* Error from the Kinova MICO device. */
    QERR_MICO_ERROR_CANNOT_READ,                                        /* Error from the Kinova MICO device: cannot perform the read operation. */
    QERR_MICO_ERROR_CANNOT_WRITE,                                       /* Error from the Kinova MICO device: cannot perform the write operation. */
    QERR_INVALID_ROS,                                                   /* The ROS property object is not valid. A ROS property object cannot be used after it has been closed. */
    QERR_ROS_ERROR,                                                     /* The ROS system is inaccessible. */
    QERR_INVALID_ROS_TOPIC,                                             /* The ROS topic is not recognized. */
    QERR_ROS_SHUTDOWN,                                                  /* The ROS system is shutdown. */
    QERR_ROS_INIT_ERROR,                                                /* There was a problem initializing ROS. */
    QERR_INVALID_BOARD_VERSION,                                         /* Version information retrieved from the HIL board does not match the driver. It may be necessary to update the QUARC software to get the latest drivers. */ /* Version information retrieved from the HIL board does not match the driver. It may be necessary to update the QRCP software to get the latest drivers. */
    QERR_UNABLE_TO_PROGRAM_FIRMWARE,                                    /* Unable to program firmware. */
    QERR_WRONG_NUMBER_OF_BYTES_RECEIVED,                                /* The wrong number of bytes was received from a device or peer. This mismatch may indicate a driver or protocol incompatibility. */
    QERR_INCOMPATIBLE_HARDWARE_VERSION,                                 /* The hardware version is incompatible with the firmware being flashed. No changes were made to the firmware. */
    QERR_INCOMPATIBLE_FIRMWARE_IMAGE,                                   /* The version of the firmware image is not compatible with the driver. No changes were made. */
    QERR_BOARD_ALREADY_OPEN,                                            /* The HIL board is already opened by another process. The board does not support access from more than one process at the same time. */
    QERR_UNSUPPORTED_VIDEO_FORMAT,                                      /* The video format is not supported. This may be due to the frame rate, frame size or native video formats of the device or source. */
    QERR_INVALID_PACKET,                                                /* The packet format is invalid. */
    QERR_INVALID_CHECKSUM,                                              /* The checksum is invalid. The data may have been corrupted. */
    QERR_NEWER_VERSION_INSTALLED,                                       /* A newer version is installed. No changes have been made. */
    QERR_INVALID_ALIGNMENT_TYPE,                                        /* The alignment type is invalid. */
    QERR_INVALID_ALLOCATION_CHUNK,                                      /* The maximum allocation chunk is invalid. */
    QERR_INVALID_BUFFER_MODE,                                           /* The buffer mode is invalid. */
    QERR_INVALID_COMPONENT_ID,                                          /* The component ID is invalid. */
    QERR_INVALID_CROP_REQUEST,                                          /* The crop request is invalid. */
    QERR_DCT_COEFFICIENT_OUT_OF_RANGE,                                  /* The DCT coefficient out of range. */
    QERR_IDCT_SIZE_NOT_SUPPORTED,                                       /* The specified IDCT output block size is not supported. */
    QERR_MISMATCHED_SAMPLING_RATIO,                                     /* The sampling ratio is mismatched. */
    QERR_INVALID_HUFFMAN_TABLE,                                         /* The Huffman table definition is invalid. */
    QERR_INVALID_INPUT_COLORSPACE,                                      /* The input colorspace is invalid. */
    QERR_INVALID_JPEG_COLORSPACE,                                       /* The JPEG colorspace is invalid. */
    QERR_INVALID_MARKER_LENGTH,                                         /* The marker length is invalid. */
    QERR_INVALID_MCU_SIZE,                                              /* The sampling factors are too large for an interleaved scan. */
    QERR_INVALID_POOL_ID,                                               /* The memory pool code is invalid. */
    QERR_INVALID_PRECISION,                                             /* The specified data precision is not supported. */
    QERR_INVALID_PROGRESSION,                                           /* The progressive image parameters are invalid. */
    QERR_INVALID_PROGRESSIVE_SCRIPT,                                    /* The progressive image parameters at the scan script entry are invalid. */
    QERR_INVALID_SAMPLING,                                              /* The sampling factors are invalid. */
    QERR_INVALID_SCAN_SCRIPT,                                           /* The scan script is invalid. */
    QERR_INVALID_LIBRARY_STATE,                                         /* A library call was made when the library is not in the proper state. Call sequence is likely invalid. */
    QERR_INVALID_STRUCT_SIZE,                                           /* The structure size was invalid. The library may not be the same version as the caller. */
    QERR_INVALID_VIRTUAL_ACCESS,                                        /* The virtual array access was invalid. */
    QERR_CANNOT_SUSPEND,                                                /* Suspension is not allowed at this point. */
    QERR_CCIR601_NOT_IMPLEMENTED,                                       /* CCIR601 sampling is not implemented yet. */
    QERR_COLOR_COMPONENT_COUNT,                                         /* There are too many color components. */
    QERR_COLOR_CONVERSION_NOT_IMPLEMENTED,                              /* The specified color conversion is not supported. */
    QERR_INVALID_DAC_INDEX,                                             /* Invalid DAC index. */
    QERR_INVALID_DAC_VALUE,                                             /* Invalid DAC value. */
    QERR_INVALID_DHT_INDEX,                                             /* Invalid DHT index. */
    QERR_INVALID_DQT_INDEX,                                             /* Invalid DQT index. */
    QERR_EMPTY_IMAGE,                                                   /* The image is empty. Empty images are not currently supported. */
    QERR_EMS_READ_FAILED,                                               /* A read from the EMS failed. */
    QERR_EMS_WRITE_FAILED,                                              /* A write to the EMS failed. */
    QERR_END_OF_INPUT_EXPECTED,                                         /* The end of the input was expected. There is too much input data. */
    QERR_FILE_READ_FAILED,                                              /* An error occurred reading from a file. */
    QERR_FILE_WRITE_FAILED,                                             /* An error occurred writing to a file. There may not be enough disk space. */
    QERR_FRACTIONAL_SAMPLING_NOT_IMPLEMENTED,                           /* Fractional sampling is not implemented yet. */
    QERR_HUFFMAN_TABLE_OVERFLOW,                                        /* The Huffman code size table overflowed. */
    QERR_HUFFMAN_MISSING_CODE,                                          /* A Huffman code table entry was missing. */
    QERR_IMAGE_TOO_BIG,                                                 /* The image was too big. */
    QERR_MISMATCHED_QUANTIZATION_TABLE,                                 /* It is not possible to transcode due to multiple uses of the quantization table. */
    QERR_MISSING_SCAN_DATA,                                             /* The scan script does not transmit all data. */
    QERR_COLOR_MODE_CHANGE_INVALID,                                     /* The color quantization mode change was invalid. */
    QERR_FEATURE_NOT_COMPILED,                                          /* The requested feature was omitted at compile time. */
    QERR_NO_ARITHMETIC_TABLE,                                           /* An arithmetic table was not defined. */
    QERR_BACKING_STORE_NOT_SUPPORTED,                                   /* A backing store is not supported. */
    QERR_NO_HUFFMAN_TABLE,                                              /* A Huffman table was not defined. */
    QERR_NO_QUANTIZATION_TABLE,                                         /* A quantization table was not defined. */
    QERR_INVALID_FILE_TYPE,                                             /* The file type is wrong. */
    QERR_TOO_MANY_QUANTIZATION_COMPONENTS,                              /* There were too many color components to quantize. */
    QERR_CANNOT_QUANTIZE_TO_FEW_COLORS,                                 /* It is not possible to quantize to so few colors. */
    QERR_CANNOT_QUANTIZE_TO_MANY_COLORS,                                /* It is not possible to quantize to so many colors. */
    QERR_SOF_DUPLICATE,                                                 /* There are too many SOF markers. The file structure is invalid. */
    QERR_NO_SOS_MARKER,                                                 /* The SOS marker is missing. The file structure is invalid. */
    QERR_SOF_NOT_SUPPORTED,                                             /* The SOF marker type is not supported. */
    QERR_SOI_DUPLICATE,                                                 /* There are too many SOI markers. The file structure is invalid. */
    QERR_SOS_BEFORE_SOF,                                                /* An SOS marker occurred before an SOF marker. The file structure is invalid. */
    QERR_CANNOT_CREATE_TEMPORARY_FILE,                                  /* Failed to create a temporary file. */
    QERR_CANNOT_READ_TEMPORARY_FILE,                                    /* Failed to read a temporary file. */
    QERR_CANNOT_SEEK_TEMPORARY_FILE,                                    /* Failed to seek on a temporary file. */
    QERR_CANNOT_WRITE_TEMPORARY_FILE,                                   /* Failed to write to a temporary file. There may not be enough disk space. */
    QERR_TOO_LITTLE_DATA,                                               /* Not enough data was supplied. */
    QERR_MARKER_NOT_SUPPORTED,                                          /* The marker type is not supported. */
    QERR_VIRTUAL_ARRAY_BUG,                                             /* The virtual array controller is confused. */
    QERR_IMAGE_TOO_WIDE,                                                /* The image is too wide for this implementation. */
    QERR_XMS_READ_FAILED,                                               /* A read from the XMS failed. */
    QERR_XMS_WRITE_FAILED,                                              /* A write to the XMS failed. */
    QERR_NO_DESTINATION_SET,                                            /* The operation cannot be performed because no destination has been configured for the operation. */
    QERR_COMPRESSED_IMAGE_TOO_LARGE,                                    /* The compressed image is too large to fit in the destination. If you are using the Image Compress block then make the output dimension larger. */
    QERR_HIL_NAME_NOT_ASSIGNED,                                         /* The specified virtual name for the HIL card has not been assigned to an actual device. */
    QERR_HIL_SET_ANALOG_INPUT_CONFIGURATION_NOT_SUPPORTED,              /* The hil_set_analog_input_configuration function is not supported by this particular card. */
    QERR_MISSING_ANALOG_INPUT_CONFIGURATION,                            /* No configurations were specified when setting the analog input configuration, even though the number of channels indicated was non-zero. */
    QERR_INVALID_ANALOG_INPUT_CONFIGURATION,                            /* One of the configurations specified for an analog input channel is not valid for the selected hardware. */
    QERR_INCOMPATIBLE_HARDWARE,                                         /* The hardware appears to be incompatible with the board type selected. */
    QERR_BAUD_RATE_EXCEEDS_MAXIMUM,                                     /* The baud rate exceeds the maximum baud rate set when the stream was created. */
    QERR_MISMATCHED_PWM_PERIOD_IN_BANK,                                 /* One of the PWM periods specified does not match the period of the other channels. This card only allows one PWM period to be set for all PWM channels in a bank. */
    QERR_CALIBRATION_FAILED,                                            /* Sensor calibration failed for some reason. Try running the model again. */
    QERR_INVALID_I2C_STATE,                                             /* The I2C channel has entered an unexpected state. */
    QERR_PARITY_ERROR,                                                  /* A parity error occurred */
    QERR_FRAMING_ERROR,                                                 /* A framing error occurred */
    QERR_FILE_TOO_LARGE,                                                /* The file has become too large for the given file format. */
    QERR_INVALID_MEDIA_TYPE,                                            /* The media type is not supported, either because parameters such as the frame rate are invalid or there is no codec for that media type. */ 
    QERR_DEVICE_DISCONNECTED,                                           /* Device was disconnected, this can be caused by outside intervention, by internal firmware error or due to insufficient power. */
    QERR_OS_ERROR,                                                      /* Error was returned from the underlying OS-specific layer. */
    QERR_WRONG_CALL_SEQUENCE,                                           /* Function precondition was violated. Functions were called in the wrong order. */
    QERR_DEVICE_RECOVERING,                                             /* Device is in recovery mode and might require firmware update. */
    QERR_DEVICE_IO_ERROR,                                               /* I/O device failure. */
    QERR_PROPERTY_IS_READ_ONLY,                                         /* The property is read-only. It cannot be set. */
    QERR_IMAGE_STREAM_NOT_FOUND,                                        /* The specified image stream could not be found. The stream type may not be supported by the camera or the stream index is too large. */
    QERR_MISSING_REALSENSE,                                             /* The RealSense 2 library is not installed. */
    QERR_EMITTER_CANNOT_BE_DISABLED,                                    /* The laser emitter on the depth camera cannot be disabled. */
    QERR_INVALID_CAMERA_PROPERTY_VALUE,                                 /* The property value specified is not supported by the camera. Check that the value corresponds with the camera selected. */
    QERR_INVALID_STRIDE,                                                /* The image stride was either too small or is not a multiple of the pixel size. */
    QERR_INVALID_FILE_HANDLE,                                           /* The file handle is not valid. An attempt was made to use a file that is not open. */
    QERR_BAROMETER_NOT_RESPONDING,                                      /* The barometer is not responding. The device may have been damaged. */
    QERR_MAGNETOMETER_NOT_RESPONDING,                                   /* The magnetometer is not responding. The device may have been damaged. */
    QERR_CONFLICTING_DIGITAL_MODES,                                     /* The specified digital IO is configured for a special purpose (e.g. PWM, Encoder, SPI, I2C, UART). Therefore it cannot be used as the specified function. Refer to the device documentation for precedents and limitations of the generic digital IO. */
    QERR_ELVISIII_TOP_BOARD_NO_POWER,                                   /* The NI ELVIS III top board is not powered, the top board must be powered before this board can be used. */
    QERR_ELVISIII_EEPROM_ERROR,                                         /* Failed to access the NI ELVIS III top board EEPROM during initialization.  Try power cycle the ELVIS III.  If the error persists, then the problem is likely a hardware fault. */
    QERR_ELVISIII_TOP_BOARD_INCOMPATIBLE,                               /* The top board attached to the NI ELVIS III is not compatbile with the driver, make sure the correct top board is attached that matches the board type as selected in HIL Initialize. */
    QERR_NO_ELVISIII_LICENSE,                                           /* You do not have a valid license for the NI ELVIS III you are using. Make sure you install QUARC with a license file that has NI ELVIS III support, and then run NI MAX to install QUARC on the NI ELVIS III. */
    QERR_NO_RIO_GENERIC_LICENSE,                                        /* You do not have a valid license for the myRIO or generic NI ELVIS III board. Make sure you install QUARC with a license file that has myRIO or generic NI ELVIS III board support, and then run NI MAX to install QUARC on the myRIO or NI ELVIS III. */
    QERR_BORDER_TYPE_NOT_SUPPORTED,                                     /* The border type selected for the operation is not supported by the current operation. */
    QERR_FILTER_MASK_SIZE_NOT_SUPPORTED,                                /* The mask size specified for the filter is not supported. Many filter operations only support 3x3 or 5x5 mask sizes. The mask should also be smaller than the image. */
    QERR_INVALID_ALGORITHM_HINT,                                        /* The specified algorithm hint is not supported. */
    QERR_INVALID_ROUNDING_MODE,                                         /* The specified rounding mode is not supported. */
    QERR_INVALID_DATA_TYPE,                                             /* The specified data type is not supported. */
    QERR_CANNOT_AUTODETECT_DSM_EXTERNAL,                                /* The type of DSM protocol cannot be auto-detected for external remotes. */
    QERR_PROPERTY_NOT_SUPPORTED,                                        /* The specified property is not supported. */
    QERR_CANNOT_INITIALIZE_OPENVR,                                      /* The OpenVR cannot be properly initialized due to an error. */
    QERR_HIL_TASK_SET_BUFFER_OVERFLOW_MODE_NOT_SUPPORTED,               /* The hil_task_set_buffer_overflow_mode function is not supported by this particular card. */
    QERR_HIL_TASK_GET_BUFFER_OVERFLOWS_NOT_SUPPORTED,                   /* The hil_task_get_buffer_overflows function is not supported by this particular card. */
    QERR_MACRO_NOT_TERMINATED,                                          /* A macro was missing the closing parenthesis. */
    QERR_INVALID_MACRO_NAME,                                            /* The macro does not match any of the standard macro names or the name of an environment variable. */
    QERR_UNSUPPORTED_IMAGE_CONVERSION,                                  /* Conversion between the two image formats selected is not currently supported. */
    QERR_CANNOT_CONVERT_CHARACTER,                                      /* A character was encountered that cannot be converted. */
    QERR_NO_DEVICE,                                                     /* The device is not available. Check that the device is plugged in or has not been reset. */
    QERR_PROTOCOL_BUFFER_TOO_SMALL,                                     /* The buffer for the underlying communication protocol is too small to send or receive the data requested. Try using the sndsize, rcvsize, bufsize or memsize options of the URI to increase the requisite buffer size. */
    QERR_INVALID_CALIBRATION,                                           /* The calibration data appears to be invalid. */
    QERR_RANGING_SENSOR_ERROR,                                          /* The ranging sensor could not detect the range due to an error. */
    QERR_IO_ERROR,                                                      /* An I/O error occurred. */
    QERR_DIVISION_BY_ZERO,                                              /* A division by zero occurred. */
    QERR_DEVICE_INITIALIZATION_FAILED,                                  /* Device initialization failed. */
    QERR_DEVICE_DRIVER_INCOMPATIBLE,                                    /* The device driver appears to be incompatible with the device. */
    QERR_HARDWARE_FAILURE,                                              /* The hardware appears to have failed. It is either not responding, or not responding as expected. Try powering down and back up. */
    QERR_SCALING_LOSES_ASPECT_RATIO,                                    /* The scaling of the width and height is not the same. The aspect ratio will be changed, which is not currently supported. */
    QERR_SCALE_FACTOR_NOT_SUPPORTED,                                    /* The given scale factor is not currently supported. */
    QERR_BUFFER_TOO_SMALL,                                              /* The supplied buffer is too small for the data requested. */
    QERR_INVALID_REALSENSE_VERSION,                                     /* The version of the Intel RealSense API expected does not match the version that is installed. The versions must match exactly. */
    QERR_INVALID_JSON,                                                  /* The JSON is invalid. JSON values must be objects, arrays, numbers, strings, true, false or null. */
    QERR_NO_CODEC_FOUND,                                                /* No suitable codec was found to encode or decode the content. */
    QERR_CANNOT_START_XMLRPC_SERVER,                                    /* The XMLRPC server cannot be started. */
    QERR_CANNOT_START_XMLRPC_CLIENT,                                    /* The XMLRPC client cannot be started. */
    QERR_CANNOT_TALK_TO_ROS_MASTER,                                     /* The XMLRPC client cannot establish communication with ROS master. */
    QERR_INVALID_ROS_MASTER_RESPONSE,                                   /* The ROS master has responded with invalid response. */
    QERR_ROS_MASTER_CALLER_ERROR,                                       /* The ROS master indicates that the ROS master API was called with caller error. In general, this means that the master/slave did not attempt to execute the action. */
    QERR_ROS_MASTER_CALLER_FAILURE,                                     /* The ROS master indicates that the ROS master API failed to complete completely.  In general, this means that the master/slave attempted the action and failed, and there may have been side-effects as a result. */
    QERR_INVALID_ROS_SLAVE_REQUEST,                                     /* The ROS slave API request is invalid. */
    QERR_UNSUPPORTED_ROS_PROTOCOL,                                      /* The requested ROS protocol is not supported. Currently this node only supports TCPROS and UDPROS protocols. */
    QERR_ROS_NOT_ACTIVE,                                                /* The ROS node is not valid. It may not have been made active during normal simulation in the ROS Initialize block and thus may be uninitialized. */
    QERR_CAMERA_IN_USE,                                                 /* The camera is already in use by another application. */
    QERR_MUTEX_ALREADY_EXISTS,                                          /* The named mutex already exists. */
    QERR_MUTEX_ABANDONED,                                               /* The mutex was owned by another thread but that thread terminated while the lock was still held so the mutex has been abandoned. The caller now owns the mutex but should check for consistency of the shared resource. */
    QERR_MUTEX_NOT_FOUND,                                               /* The named mutex could not be found. */
    QERR_IMAGE_DATA_TYPE_NOT_SUPPORTED,                                 /* The data type selected is not currently supported by the chosen image format. */
    QERR_PROTOCOL_DRIVER_NOT_FOUND,                                     /* Support for the given protocol type does not appear to be installed. Verify that you have entered the correct URI for the Stream blocks or stream_connect/stream_listen functions. */
    QERR_CPU_GPIO_IN_USE,                                               /* A GPIO is in use by another application. Some applications on Linux-based systems use the old sysfs (/sys/class/gpio) file system for GPIO. If a GPIO is exported it cannot be used by QUARC. Try rebooting the target. */
    QERR_OPTITRACK_LIBRARY_OPEN_FAILED,                                 /* The Motive library failed to open. Make sure you have the Motive software installed and the appropriate environment variables (refer to the device help page) set correctly. */
    QERR_OPTITRACK_UNSUPPORTED_API_FUNCTION,                            /* The required Motive API is not available. Make sure you have the correct version of the Motive software installed. E.g. older Motive software does not support loading of user profile (.xml or .motive) file and must use trackable (.tra) file for rigid bodies definitions. */
    QERR_OPTITRACK_UNSUPPORTED_RIGID_BODY_DEF_FILE,                     /* The specified rigid body definition is not supported. Currently only .xml, .motive, and .tra files are supported. */
    QERR_OPTITRACK_INVALID_PROFILE_FILE,                                /* Unable to load Motive user profile file. Make sure the file path is correct. */
    QERR_UNABLE_TO_LOAD_CUDA_KERNEL,                                    /* Unable to load CUDA kernel. The installed CUDA version may be incompatible with the CUDA code. */
    QERR_UNABLE_TO_GET_CUDA_FUNCTION,                                   /* Unable to get CUDA function from kernel. The mangled function name is likely incorrect. */
    QERR_CAN_BUS_IDENTIFIER_TOO_LARGE,                                  /* The CAN bus identifier is too large for the standard frame format. Use the flexible=1 option on the URI to allow extended CAN FD frames if your CAN device supports it. */
    QERR_INVALID_IPV6_ADDRESS,                                          /* The IPv6 address is invalid or incomplete. On Linux systems, the zone identifier must be used by clients to identify the network interface (e.g. eth0) through which a link local address is connecting e.g. tcpip6://[fe80::abcd:beef:1234:5678%eth0]:18000 */
    QERR_CANNOT_GET_CAMERA_PROPERTIES,                                  /* Unable to get the properties of the camera. This may indicate a hardware issue. */
    QERR_INVALID_CUDA_CONTEXT,                                          /* The CUDA context has not been initialized. This may indicate version mismatches. */
    QERR_MAP_FAILED,                                                    /* Failed to perform a mapping or register operation. */
    QERR_RESOURCE_IN_USE,                                               /* The desired resource is already in use for another operation. */
    QERR_CUDA_CONTEXT_IN_USE,                                           /* The CUDA context passed to an API call is already in use by another thread. */
    QERR_CUDA_COMPILATION_FAILED,                                       /* Compilation of CUDA PTX code failed. The CUDA PTX source is invalid or the JIT PTX compilation library was not found. */
    QERR_INVALID_GRAPHICS_CONTEXT,                                      /* The OpenGL or DirectX graphics context is invalid. */
    QERR_UNRECOVERABLE_ERROR,                                           /* An unrecoverable error occurred. The application will need to be re-run. */
    QERR_INCOMPATIBLE_TEXTURING_MODE,                                   /* The CUDA kernel launched using an incompatible texturing mode. */
    QERR_INVALID_PEER_ACCESS,                                           /* The peer access was invalid. It may not be enabled or may have already been enabled. */
    QERR_OBJECT_ALREADY_INITIALIZED,                                    /* The object was already initialized and cannot be re-initialized. */
    QERR_TOO_MANY_CUDA_BLOCKS,                                          /* Too many CUDA blocks were used with a cooperative kernel. */
    QERR_MISSING_FGLOVE,                                                /* The 5DT Data Glove SDK does not appear to be installed or is not in the PATH. See the help for the FDT Data Glove block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_FORCE_DIMENSION,                                       /* The Force Dimension SDK does not appear to be installed or is not in the PATH. See the help for the Force Dimension Write block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_FLY_CAPTURE,                                           /* The FlyCapture SDK does not appear to be installed or is not in the PATH. See the help for the PGR Grab Image block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_PCAN,                                                  /* The PCAN-Basic API does not appear to be installed or is not in the PATH. See the help for the Peak CAN block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_VICON,                                                 /* The Vicon DataStream SDK does not appear to be installed or is not in the PATH. See the help for the Vicon block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_LEAPMOTION,                                            /* The Leap SDK does not appear to be installed or is not in the PATH. See the help for the Leap Motion block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_CANPCI,                                                /* The CANPCI SDK does not appear to be installed or is not in the PATH. See the help for the CANPCI block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_SCHUNK,                                                /* The Schunk PowerCube software does not appear to be installed or is not in the PATH. See the help for the Schunk Gripper block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_MISSING_FALCON,                                                /* The HDAL software does not appear to be installed or is not in the PATH. See the help for the Novint Falcon block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_NO_THREAD_CANCELLATION_STATE,                                  /* The calling thread does not support setting the cancellation state of the thread. The thread was not created with qthread_create. */
    QERR_MISSING_OPENVR,                                                /* The OpenVR SDK software does not appear to be installed or is not in the PATH. See the help for the Tracker block for the installation requirements. Note that a reboot may be required after installing the SDK. */
    QERR_UNSUPPORTED_AUDIO_FORMAT,                                      /* The audio format is not supported. This may be due to a missing audio codec on some targets. */
    QERR_CORRUPT_FILE,                                                  /* The file is corrupt or is not the expected format. */
    QERR_WRONG_MODE_FOR_TRIGGERING,                                     /* The session is in the wrong mode for triggering. */
    QERR_CAMERA_NAME_NOT_ASSIGNED,                                      /* The specified virtual name for the camera has not been assigned to an actual device. */
    QERR_NOT_HIL_PROXY,                                                 /* The server to which a connection was attempted is not a HIL proxy server or HIL simulation. */
    QERR_NOT_VIDEO3D_PROXY,                                             /* The server to which a connection was attempted is not a Video3D proxy server or Video3D simulation. */
    QERR_NO_DEVICE_SIMULATION_LICENSE,                                  /* You do not have a valid license for using third-party devices in normal simulation. To configure licensing use the Configure License utility found under Start Menu/All Programs/Quanser for your product. */
    QERR_NO_HIL_PROXY,                                                  /* The connection to the HIL simulation or HIL Proxy Server was refused. If using a simulated device, make sure the simulation is running. */
    QERR_PRODUCT_NOT_IN_LICENSE_FILE,                                   /* The product code specified could not be found in the license file. */
    QERR_BUFFER_MODE_NOT_SUPPORTED,                                     /* The specified buffer mode is not supported. */
    QERR_MISSING_FORMAT_SPECIFIER,                                      /* A format specifier is missing in the option template. */
    QERR_INVALID_FORMAT_RESTRICTION,                                    /* An invalid restriction on a format specifier was specified. */
    QERR_INVALID_TIMER_SEMAPHORE,                                       /* The timer semaphore passed as an argument is invalid. */
    QERR_NOT_VIDEO_PROXY,                                               /* The server to which a connection was attempted is not a Video proxy server or Video simulation. */
    QERR_SAMPLES_LOST,                                                  /* Samples were lost or corrupted because the device cannot keep up. The sampling frequency is too fast or too many samples have been requested. Try fewer samples or a slower sampling frequency. */
    QERR_QARM_COMM_FAILURE_J0,                                          /* Communication to the Yaw motor has been lost or corrupted. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_COMM_FAILURE_J1_MASTER,                                   /* Communication to the Master Shoulder motor has been lost or corrupted. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_COMM_FAILURE_J1_SLAVE,                                    /* Communication to the Slave Shoulder motor has been lost or corrupted. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_COMM_FAILURE_J2,                                          /* Communication to the Elbow motor has been lost or corrupted. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_COMM_FAILURE_J3,                                          /* Communication to the Wrist motor has been lost or corrupted. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_COMM_FAILURE_END_EFFECTOR,                                /* Communication to the End Effector board has been lost or corrupted. Please turn off the arm device and check the cable connection.  */
    QERR_QARM_COMM_FAILURE_GRIPPER,                                     /* Communication to the Gripper motor has been lost or corrupted. Please turn off the arm device and check the motor's cable connection.  */
    QERR_QARM_OVERHEATING_J0,                                           /* Internal temperature of the Yaw motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERHEATING_J1_MASTER,                                    /* Internal temperature of the Master Shoulder motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERHEATING_J1_SLAVE,                                     /* Internal temperature of the Slave Shoulder motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERHEATING_J2,                                           /* Internal temperature of the Elbow motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERHEATING_J3,                                           /* Internal temperature of the Wrist motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERHEATING_GRIPPER,                                      /* Internal temperature of the Gripper motor has exceeded the configured operating temperature. Please turn off the arm and allow the motor to cool for at least 20 minutes.  */
    QERR_QARM_OVERLOAD_J0,                                              /* Detected a persistent load that exceeded the maximum output rating of the Yaw motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_OVERLOAD_J1_MASTER,                                       /* Detected a persistent load that exceeded the maximum output rating of the Master Shoulder motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_OVERLOAD_J1_SLAVE,                                        /* Detected a persistent load that exceeded the maximum output rating of the Slave Shoulder motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_OVERLOAD_J2,                                              /* Detected a persistent load that exceeded the maximum output rating of the Elbow motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_OVERLOAD_J3,                                              /* Detected a persistent load that exceeded the maximum output rating of the Wrist motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_OVERLOAD_GRIPPER,                                         /* Detected a persistent load that exceeded the maximum output rating of the Gripper motor. Please turn off the arm and apply a lighter load to the motor.  */
    QERR_QARM_MOTOR_ENCODER_J0,                                         /* Detected a malfunction of the Yaw motor's encoder. Please contact your local Quanser support team.  */
    QERR_QARM_MOTOR_ENCODER_J1_MASTER,                                  /* Detected a malfunction of the Master Shoulder motor's encoder. Please contact your local Quanser support team.  */
    QERR_QARM_MOTOR_ENCODER_J1_SLAVE,                                   /* Detected a malfunction of the Slave Shoulder motor's encoder. Please contact your local Quanser support team.  */
    QERR_QARM_MOTOR_ENCODER_J2,                                         /* Detected a malfunction of the Elbow motor's encoder. Please contact your local Quanser support team. */
    QERR_QARM_MOTOR_ENCODER_J3,                                         /* Detected a malfunction of the Wrist motor's encoder. Please contact your local Quanser support team.  */
    QERR_QARM_MOTOR_ENCODER_GRIPPER,                                    /* Detected a malfunction of the Gripper motor's encoder. Please contact your local Quanser support team.  */
    QERR_QARM_ELECTRICAL_SHOCK_J0,                                      /* Detected an electrical shock on the Yaw motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_ELECTRICAL_SHOCK_J1_MASTER,                               /* Detected an electrical shock on the Master Shoulder motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_ELECTRICAL_SHOCK_J1_SLAVE,                                /* Detected an electrical shock on the Slave Shoulder motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_ELECTRICAL_SHOCK_J2,                                      /* Detected an electrical shock on the Elbow motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_ELECTRICAL_SHOCK_J3,                                      /* Detected an electrical shock on the Wrist motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_ELECTRICAL_SHOCK_GRIPPER,                                 /* Detected an electrical shock on the Gripper motor's circuit or insufficient power to operate the motor. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_J0,                                         /* Input voltage of the Yaw motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_J1_MASTER,                                  /* Input voltage of the Master Shoulder motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_J1_SLAVE,                                   /* Input voltage of the Slave Shoulder motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_J2,                                         /* Input voltage of the Elbow motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_J3,                                         /* Input voltage of the Wrist motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_QARM_INPUT_VOLTAGE_GRIPPER,                                    /* Input voltage of the Gripper motor exceeded the configured operating voltage. Please power cycle the arm and contact your local Quanser support team if the issue continues.  */
    QERR_PDU_SIZE_TOO_SMALL,                                            /* The protocol data unit (PDU) is too small to handle the data required. */
	QERR_CANNOT_NEGOTIATE_PDU,                                          /* Unable to negotiate protocol data unit (PDU) size. */
    QERR_JOB_PENDING,                                                   /* A job is already pending. */
    QERR_TOO_MANY_VARIABLES,                                            /* There are too may items (>20) in multivariable read/write. */
    QERR_PDU_TOO_SMALL,                                                 /* The total data exceeds the PDU size. */
    QERR_INVALID_PLC_ANSWER,                                            /* The PLC returned an invalid answer. */
    QERR_CANNOT_START_PLC,                                              /* The PLC could not be started. */
    QERR_PLC_ALREADY_RUN,                                               /* The PLC is already running. */
    QERR_CANNOT_STOP_PLC,                                               /* The PLC canot be stopped. */
    QERR_CANNOT_COPY_RAM_TO_ROM,                                        /* Cannot copy RAM to ROM. */
    QERR_CANNOT_COMPRESS,                                               /* Cannot compress. */
    QERR_PLC_ALREADY_STOPPED,                                           /* The PLC has already been stopped. */
    QERR_UPLOAD_FAILED,                                                 /* The upload sequence failed. */
    QERR_INVALID_DATA_SIZE_RECEIVED,                                    /* Invalid data size received. */
    QERR_INVALID_BLOCK_TYPE,                                            /* Invalid block type. */
    QERR_INVALID_BLOCK_NUMBER,                                          /* Invalid block number. */
    QERR_INVALID_BLOCK_SIZE,                                            /* Invalid block size. */
    QERR_DOWNLOAD_FAILED,                                               /* Download sequence failed. */
    QERR_BLOCK_INSERT_REFUSED,                                          /* Block insert refused. */
    QERR_BLOCK_DELETE_REFUSED,                                          /* Block delete refused. */
    QERR_INVALID_PASSWORD,                                              /* Invalid password. */
    QERR_NO_PASSWORD_TO_SET_OR_CLEAR,                                   /* No password to set or clear. */
    QERR_FUNCTION_REFUSED,                                              /* Function refused by CPU (Unknown error). */
    QERR_DESTROYING_OBJECT,                                             /* Cannot perform the operation. Object is being destroyed. */
    QERR_CANNOT_CHANGE_PARAMETER,                                       /* The parameter cannot be changed at the present time. */
    QERR_ILLEGAL_MULTIBYTE_CHARACTER,                                   /* An illegal multi-byte character was encountered in the stream. */
    QERR_ILLEGAL_SURROGATE_CHARACTER,                                   /* An illegal surrogate character was encountered in the stream. */
    QERR_ILLEGAL_CONTROL_CHARACTER,                                     /* An illegal control character was encountered in the stream. */
    QERR_ILLEGAL_NON_CHARACTER,                                         /* An illegal non-character was encountered in the stream. */
    QERR_MISSING_END_TAG_NAME,                                          /* Missing end tag name e.g. </>. */
    QERR_UNEXPECTED_NULL_CHARACTER,                                     /* Unexpected null character in the input stream. */
    QERR_UNEXPECTED_QUESTION_MARK,                                      /* Unexpected question mark in the input stream. */
    QERR_END_BEFORE_TAG,                                                /* End of input stream encountered before tag name. */
    QERR_END_IN_TAG,                                                    /* End of input stream encountered within tag name. */
    QERR_INVALID_FIRST_CHARACTER_OF_NAME,                               /* Invalid first character of tag name. */
    QERR_INVALID_ARRAY_ELEMENT_SEPARATOR,                               /* Invalid array element separator when parsing. */
    QERR_FAILED_TO_PARSE_INTEGER,                                       /* Failed to parse an integer value in a string. Format is incorrect. */
    QERR_FAILED_TO_PARSE_REAL_NUMBER,                                   /* Failed to parse a real value in a string. Format is incorrect. */
    QERR_MATRIX_NOT_INVERTIBLE,                                         /* The matrix is not invertible. */
    QERR_FORCE_TORQUE_SENSOR_DISCONNECTED,                              /* The force/torque sensor appears to be disconnected. */
    QERR_END_QUOTE_EXPECTED,                                            /* The ending quote for a string was expected. */
    QERR_TEXT_MATRICES_NOT_SUPPORTED,                                   /* Text matrices are not currently supported. */
    QERR_SPARSE_MATRICES_NOT_SUPPORTED,                                 /* Sparse matrices are not currently supported.*/
    QERR_MATRIX_TYPE_NOT_RECOGNIZED,                                    /* The matrix type of the MAT-file was not recognized. File may be corrupt. */
    QERR_VARIABLE_NOT_FOUND,                                            /* The requested variable could not be found. */
    QERR_COMPLEX_NUMBERS_NOT_SUPPORTED,                                 /* Complex numbers are not currently supported. */
    QERR_BYTE_ORDER_NOT_SUPPORTED,                                      /* The specified byte order is not supported. For example, VAX and Cray byte ordering is not supported. */
    QERR_NUMBER_OF_ROWS_TOO_SMALL,                                      /* The number of rows of the matrix in the file is too small for the total rows implied by the parameters. */
    QERR_NUMBER_OF_COLUMNS_TOO_SMALL,                                   /* The number of columns of the matrix in the file is too small for the total columns implied by the parameters. */
    QERR_INVALID_I2C_TIMING_CONFIG,                                     /* Could not configure the I2C timing registers to the specified clock frequency. Please try using a different I2C clock frequency. */
    QERR_IMU_HARDWARE_ERROR,                                            /* The IMU is not responding properly. Please check the hardware. If necessary, the IMU may be disabled in the card-specific options, in which case the IMU outputs will be zero. */
    QERR_CONFLICTING_DIGITAL_FUNCTIONS,                                 /* The special purpose function (e.g. PWM, Encoder, SPI, I2C, UART) pins are already configured for Digital I/O. Please remove the appropriate Digital I/O channels inside the HIL Initialize block in order to use the specified function. Refer to the device help page for pinout diagrams. */
    QERR_ANALOG_OUTPUT_IS_NAN,                                          /* An attempt was made to write an analog output value that is Not-a-Number (NaN). */
    QERR_PWM_OUTPUT_IS_NAN,                                             /* An attempt was made to write a PWM output value that is Not-a-Number (NaN). */
    QERR_OTHER_OUTPUT_IS_NAN,                                           /* An attempt was made to write an other output value that is Not-a-Number (NaN). */
    QERR_DOUBLE_PROPERTY_IS_NAN,                                        /* An attempt was made to set a double property to a value that is Not-a-Number (NaN). */
    QERR_PWM_FREQUENCY_IS_NAN,                                          /* An attempt was made to set the PWM frequency to a value that is Not-a-Number (NaN). */
    QERR_PWM_DUTY_CYCLE_IS_NAN,                                         /* An attempt was made to set the PWM duty cycle to a value that is Not-a-Number (NaN). */
    QERR_PWM_DEADBAND_IS_NAN,                                           /* An attempt was made to set the PWM deadband to a value that is Not-a-Number (NaN). */
    QERR_CLOCK_FREQUENCY_IS_NAN,                                        /* An attempt was made to set the clock frequency to a value that is Not-a-Number (NaN). */
    QERR_ENCODER_FILTER_FREQUENCY_IS_NAN,                               /* An attempt was made to set the encoder filter frequency to a value that is Not-a-Number (NaN). */
    QERR_TOO_MANY_POINTS,                                               /* There are too many points specified for the algorithm to process. Resource or computation limits would be exceeded. */
    QERR_STACK_OVERFLOW,                                                /* An internal stack overflowed. */
    QERR_STACK_UNDERFLOW,                                               /* An internal stack underflowed. */
    QERR_NO_REFERENCE_SCAN,                                             /* No reference scan has been set. A scan match cannot be performed. */
    QERR_INVALID_SCAN,                                                  /* No valid points were found in the scan. */

    QERR_NUMBER_OF_ERRORS
};

/*
    Define the t_error type to make it clear where the above error codes are being
    used. Since these error codes are generally returned as negative values rather than
    than positive values, we do not define t_error as being the enumerated type itself.
    Furthermore, GCC would interpret such an enumerated type as being an unsigned
    integer so comparisons for negative return values would not work!
*/
typedef t_int t_error;

#endif

