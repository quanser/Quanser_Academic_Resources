#if !defined(_quanser_packing_h)
#define _quanser_packing_h

/*
** To pack a structure on any platform, use the following syntax:
**
** #if defined(_WIN32)
** #pragma pack (push, 1)
** #endif
**
** struct PACKED_ATTRIBUTE mystruct {
**     ...
** };
**
** #if defined(_WIN32)
** #pragma pack (pop)
** #endif
**/

#if defined(__QNX__) || defined(__linux) || defined(__APPLE__) || defined(ALT_SYSTEM_NAME) /* NIOS */
#define PACKED_ATTRIBUTE    __attribute__ ((__packed__))
#define ALIGNED_ATTRIBUTE   __attribute__ ((__aligned__))
#else
#define PACKED_ATTRIBUTE
#define ALIGNED_ATTRIBUTE
#endif

#endif
