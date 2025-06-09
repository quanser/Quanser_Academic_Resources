#if !defined(_quanser_extern_h)
#define _quanser_extern_h

#if defined(__cplusplus)
#define EXTERN extern "C"
#else
#define EXTERN extern
#endif

#if defined(_WIN32)

#if !defined(STDCALL)
#define STDCALL     __stdcall
#endif

#if !defined(CFUNCTION)
#define CFUNCTION   __cdecl
#endif

#if !defined(IMPORT)
#define IMPORT      __declspec(dllimport)
#endif

#if !defined(EXPORT)
#define EXPORT      __declspec(dllexport)
#endif

#else /* !WIN32 */

#if !defined(STDCALL)
#define STDCALL
#endif

#if !defined(CFUNCTION)
#define CFUNCTION
#endif

#if !defined(IMPORT)
#define IMPORT
#endif

#if !defined(EXPORT)
#if defined(__GNUC__)
#define EXPORT __attribute__((visibility("default")))
#else
#define EXPORT
#endif
#endif

#endif

#endif




