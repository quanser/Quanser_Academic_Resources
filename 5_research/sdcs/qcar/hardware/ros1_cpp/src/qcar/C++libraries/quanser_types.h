#if !defined(_quanser_types_h)
#define _quanser_types_h

#ifdef __cplusplus
/*
    The QNX compiler, QCC, for C++ maintains the __cplusplus
    preprocessor symbol even in header files that are included
    within extern "C" scope. Hence, C++ constructs are compiled
    as C code causing multiple errors. Hence, we need to revert
    to C++ scope when including system header files under C++!
*/
extern "C++" {
#endif

#if defined(__vxworks)
#include <stddef.h>
#undef WCHAR_MAX
#define WCHAR_MAX 0xffff
#elif !defined (__dsPIC30F__) && !defined (__dsPIC33F__)
#include <wchar.h>
#endif

#include <limits.h>
#include <float.h>

#if defined(__linux) || defined(__QNX__) || defined(__APPLE__)
#include <stdint.h> /* defines intmax_t and uintmax_t */
#endif

#if defined(_MSC_VER) && (_MSC_VER <= 1100) && !defined(__INTIME__)
#undef WCHAR_MAX
#define WCHAR_MAX 0xffff
typedef int intptr_t;
#endif

#ifdef __cplusplus
}
#endif

#if defined(__INTIME__)

#if !defined(_W64)
#if !defined(__midl) && (defined(_X86_) || defined(_M_IX86)) && _MSC_VER >= 1300
#define _W64 __w64
#else
#define _W64
#endif
#endif

#ifndef _INTPTR_T_DEFINED
#ifdef  _WIN64
typedef __int64             intptr_t;
#else
typedef _W64 int            intptr_t;
#endif
#define _INTPTR_T_DEFINED
#endif

#undef WCHAR_MIN
#undef WCHAR_MAX

#define WCHAR_MIN 0x0000
#define WCHAR_MAX 0xffff

#endif

#define ARRAY_LENGTH(array) (sizeof(array)/sizeof((array)[0]))

#if !defined(__cplusplus) && !defined(false) && !defined(true)
enum {
    false,
    true
};
#endif

#if !defined(QUOTE)
#define QUOTE1(text)    # text
#define QUOTE(text)     QUOTE1(text)
#endif

#define WIDE1(text)         L ## text
#define WIDE(text)          WIDE1(text)

#if defined(_UNICODE)
typedef wchar_t        t_char;      /* 16 bits in this case */
#else
typedef char           t_char;      /* 8 bits in this case */
#endif

#if !defined(_TXT)
#if defined(_UNICODE)
#define _TXT(text)     WIDE(text)
#else
#define _TXT(text)     text
#endif
#endif /* _TXT */

/*
    UPPER_DWORD - return upper 32-bits of an integer (0 if 32-bit Windows)
    LOWER_DWORD - return lower 32-bits of an integer
*/
#if INT_MAX > 2147483647
#define UPPER_DWORD(value)  ((t_uint32) ((value) >> 32))
#define LOWER_DWORD(value)  ((t_uint32) (value))
#else
#define UPPER_DWORD(value)  (0U)
#define LOWER_DWORD(value)  ((t_uint32) (value))
#endif

/*
    UPPER_WORD - return upper 16-bits of a 32-bit integer (0 if 32-bit Windows)
    LOWER_WORD - return lower 16-bits of a 32-bit integer
*/
#define UPPER_WORD(value)   ((t_uint16) ((value) >> 16))
#define LOWER_WORD(value)   ((t_uint16) (value))

/*
    UPPER_BYTE - return upper 8-bits of a 16-bit integer (0 if 32-bit Windows)
    LOWER_BYTE - return lower 8-bits of a 16-bit integer
*/
#define UPPER_BYTE(value)   ((t_uint8) ((value) >> 8))
#define LOWER_BYTE(value)   ((t_uint8) (value))


typedef char           t_boolean;   /* must always be 8 bits */
typedef signed char    t_byte;      /* must always be 8 bits */
typedef unsigned char  t_ubyte;     /* must always be 8 bits */
typedef signed short   t_short;     /* must always be 16 bits */
typedef unsigned short t_ushort;    /* must always be 16 bits */

#if INT_MAX < 0x7fffffff
#if LONG_MAX < 0x7fffffff
#error A 32-bit integer data type does not appear to exist!
#endif
typedef signed long    t_int;       /* must always be 32 bits */
#else
typedef signed int     t_int;       /* must always be 32 bits */
#endif

#if UINT_MAX < 0xffffffffU
#if ULONG_MAX < 0xffffffffU
#error A 32-bit integer data type does not appear to exist!
#endif
typedef unsigned long  t_uint;      /* must always be 32 bits */
#else
typedef unsigned int   t_uint;      /* must always be 32 bits */
#endif

typedef float          t_single;    /* must always be 4 bytes */

#if DBL_MANT_DIG < 53
#if LDBL_MANT_DIG < 53
#error A 64-bit floating-point data type does not appear to exist!
#endif
typedef long double    t_double;
#else
typedef double         t_double;    /* must always be 8 bytes */
#endif

typedef t_byte         t_int8;
typedef t_ubyte        t_uint8;
typedef t_short        t_int16;
typedef t_ushort       t_uint16;
typedef t_int          t_int32;
typedef t_uint         t_uint32;

#if defined (WCHAR_MAX)

/* Type used to get a wide character in Simulink */
typedef wchar_t        t_wide_char;

#if WCHAR_MAX < 0x0100 /* wide characters are UTF-8 */
typedef wchar_t        t_utf8_char;
typedef t_uint16       t_utf16_char;
typedef t_uint32       t_utf32_char;
#elif WCHAR_MAX < 0x010000 /* wide characters are UTF-16 */
typedef char           t_utf8_char;
typedef wchar_t        t_utf16_char;
typedef t_uint32       t_utf32_char;
#else /* wide characters are UTF-32 */
typedef char           t_utf8_char;
typedef t_uint16       t_utf16_char;
typedef wchar_t        t_utf32_char;
#endif
#endif

#ifndef NO_64_BITS

#if defined(__QNX__) || defined(__APPLE__)

typedef int64_t  t_long;
typedef uint64_t t_ulong;

#else

#ifdef _MSC_VER
typedef __int64        t_long;
#else 
typedef long long      t_long;
#endif

#ifdef _MSC_VER
typedef unsigned __int64   t_ulong;
#else
typedef unsigned long long t_ulong;
#endif

#endif

typedef t_long             t_int64;      /* must always be 64 bits */
typedef t_ulong            t_uint64;     /* must always be 64 bits */

#endif /* NO_64_BITS */

#if !defined(__linux) && !defined(__QNX__) && !defined(__APPLE__)
typedef t_int64  intmax_t;
typedef t_uint64 uintmax_t;
#endif

#endif /* t_types_h */
