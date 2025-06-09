#if !defined(_quanser_inline_h)
#define _quanser_inline_h

/* Undefine __inline since the new INTime network7 header files define it (and it is intended to be a keyword)! */
#undef __inline

#if defined(__cplusplus)
#define INLINE inline
#elif defined(_MSC_VER)
#define INLINE __inline
#else
/* GCC uses "extern __inline__" to ensure the function is always inlined (see http://gcc.gnu.org/onlinedocs/gcc/Inline.html at bottom of page) */
#define INLINE static __inline__
#endif

#endif
