#if !defined(_quanser_messages_h)
#define _quanser_messages_h

#include "quanser_runtime.h"
#include "quanser_errors.h"

EXTERN t_error
msg_get_current_localeA(char * buffer, size_t buffer_size);

EXTERN t_error
msg_get_current_localeW(wchar_t * buffer, size_t buffer_size);

#if defined(_UNICODE)
#define msg_get_current_locale   msg_get_current_localeW
#else
#define msg_get_current_locale   msg_get_current_localeA
#endif

EXTERN t_error
msg_set_current_localeA(int category, const char * locale);

EXTERN t_error
msg_set_current_localeW(int category, const wchar_t * locale);

#if defined(_UNICODE)
#define msg_set_current_locale   msg_set_current_localeW
#else
#define msg_set_current_locale   msg_set_current_localeA
#endif

/*
    All the functions in this header file take a locale argument. The current locale
    may be retrieved or set using the msg_get_current_locale or msg_set_current_locale
    functions respectively. Passing a NULL pointer as the locale for any of these
    functions bolos causes the current locale to be used. The locale string is
    assumed to take the form:

        <lang>[_<country>[.<codepage>]]

    For example:

        "English_United States.1252"
        "English_Canada.1252"
        "English_Canada"
        "English"
        "French_France.1252"
        "French_France"
        "French"
        "Japanese"
 
    Carefully review the information about the setlocale function (esp. in MSDN online)
    for more information on the language, country codes and code pages available.
*/

/*
    This function looks up an error message code and returns the corresponding error message.
    If the corresponding error message is found then the number of characters copied into the
    supplied buffer is returned. Otherwise a negative error code is returned.

    The buffer argument may be NULL in which case the length of the error message is returned.
    In this case, the length parameter should be the maximum buffer size allowable because
    the error message length will be truncated to the given length.

    Error messages are stored in UTF-8 text files in the folder specified by the error_folder
    argument. The name of the text file is given in the error_filename argument. Error
    messages are expected to be organized in a hierarchical directory structure with the
    error_folder as the root folder. For example:

        <error_folder>\
            <error_filename>            - file containing the error messages for the default locale
            English\
                <error_filename>        - file containing the error messages that are specific to the English culture
            English_United States\
                <error_filename>        - file containing the error messages that are specific to the US English subculture
            English_Canada\
                <error_filename>        - file containing the error messages that are specific to the Canadian English subculture
            ...

    This function searches in the subculture first, then the culture and finally in the error messages for the default locale.
    By doing so, only those error messages which are different in a particular subculture need to be recorded in the error
    file for the subculture. Likewise for the culture. This format also allows the user or distributor to readily extend the 
    number of languages supported in the error messages.

    The error_folder is typically read from the registry or from the path to the application executable and the error file name
    is usually fixed.
*/
EXTERN t_error
msg_read_error_messageW(const wchar_t * error_folder, const wchar_t * error_filename, const wchar_t * locale,
                        t_error error_code, wchar_t * buffer, size_t length);

/*
    This function looks up an error message code and returns the corresponding error message.
    If the corresponding error message is found then the number of characters copied into the
    supplied buffer is returned. Otherwise a negative error code is returned.

    The buffer argument may be NULL in which case the length of the error message is returned.
    In this case, the length parameter should be the maximum buffer size allowable because
    the error message length will be truncated to the given length.

    Error messages are stored in UTF-8 text files in the folder specified by the error_folder
    argument. The name of the text file is given in the error_filename argument. Error
    messages are expected to be organized in a hierarchical directory structure with the
    error_folder as the root folder. For example:

        <error_folder>\
            <error_filename>            - file containing the error messages for the default locale
            English\
                <error_filename>        - file containing the error messages that are specific to the English culture
            English_United States\
                <error_filename>        - file containing the error messages that are specific to the US English subculture
            English_Canada\
                <error_filename>        - file containing the error messages that are specific to the Canadian English subculture
            ...

    This function searches in the subculture first, then the culture and finally in the error messages for the default locale.
    By doing so, only those error messages which are different in a particular subculture need to be recorded in the error
    file for the subculture. Likewise for the culture. This format also allows the user or distributor to readily extend the 
    number of languages supported in the error messages.

    The error_folder is typically read from the registry or from the path to the application executable and the error file name
    is usually fixed.
*/
EXTERN t_error
msg_read_error_messageA(const char * error_folder, const char * error_filename, const char * locale, 
                        t_error error_code, char * buffer, size_t length);

#if defined(_UNICODE)
#define msg_read_error_message   msg_read_error_messageW
#else
#define msg_read_error_message   msg_read_error_messageA
#endif

/*
    This function looks up an error message code and returns the corresponding error message
    from the common error files.

    If the corresponding error message is found then the number of characters copied into the
    supplied buffer is returned. Otherwise a negative error code is returned.

    The buffer argument may be NULL in which case the length of the error message is returned.
    In this case, the length parameter should be the maximum buffer size allowable because
    the error message length will be truncated to the given length.

    Common error messages are stored in UTF-8 text files in the [Common Files]\Quanser\errors folder
    (on Windows). The name of the text file is "quanser_errors.txt". Error messages are expected to be
    organized in a hierarchical directory structure with the errors folder as the root folder. For example:

        [Common Files]\Quanser\errors\
            quanser_errors.txt            - file containing the error messages for the default locale
            English\
                quanser_errors.txt        - file containing the error messages that are specific to the English culture
            English_United States\
                quanser_errors.txt        - file containing the error messages that are specific to the US English subculture
            English_Canada\
                quanser_errors.txt        - file containing the error messages that are specific to the Canadian English subculture
            ...

    This function searches in the subculture first, then the culture and finally in the error messages for the default locale.
    By doing so, only those error messages which are different in a particular subculture need to be recorded in the error
    file for the subculture. Likewise for the culture. This format also allows the user or distributor to readily extend the 
    number of languages supported in the error messages.
*/
EXTERN t_error
msg_get_error_messageW(const wchar_t * locale, t_error error_code, wchar_t * buffer, size_t length);

/*
    This function looks up an error message code and returns the corresponding error message
    from the common error files.

    If the corresponding error message is found then the number of characters copied into the
    supplied buffer is returned. Otherwise a negative error code is returned.

    The buffer argument may be NULL in which case the length of the error message is returned.
    In this case, the length parameter should be the maximum buffer size allowable because
    the error message length will be truncated to the given length.

    Common error messages are stored in UTF-8 text files in the [Common Files]\Quanser\errors folder
    (on Windows). The name of the text file is "quanser_errors.txt". Error messages are expected to be
    organized in a hierarchical directory structure with the errors folder as the root folder. For example:

        [Common Files]\Quanser\errors\
            quanser_errors.txt            - file containing the error messages for the default locale
            English\
                quanser_errors.txt        - file containing the error messages that are specific to the English culture
            English_United States\
                quanser_errors.txt        - file containing the error messages that are specific to the US English subculture
            English_Canada\
                quanser_errors.txt        - file containing the error messages that are specific to the Canadian English subculture
            ...

    This function searches in the subculture first, then the culture and finally in the error messages for the default locale.
    By doing so, only those error messages which are different in a particular subculture need to be recorded in the error
    file for the subculture. Likewise for the culture. This format also allows the user or distributor to readily extend the 
    number of languages supported in the error messages.
*/
EXTERN t_error
msg_get_error_messageA(const char * locale, t_error error_code, char * buffer, size_t length);

#if defined(_UNICODE)
#define msg_get_error_message   msg_get_error_messageW
#else
#define msg_get_error_message   msg_get_error_messageA
#endif

/*
    This function returns a default error message and is generally called when msg_get_error_message returns
    a negative error code because it is unable to find the error message code in the error files.
*/
EXTERN t_error
msg_get_default_error_messageW(const wchar_t * locale, t_error error_code, wchar_t * buffer, size_t length);

/*
    This function returns a default error message and is generally called when msg_get_error_message returns
    a negative error code because it is unable to find the error message code in the error files.
*/
EXTERN t_error
msg_get_default_error_messageA(const char * locale, t_error error_code, char * buffer, size_t length);

#endif
