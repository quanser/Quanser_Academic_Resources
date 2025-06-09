#if !defined(_quanser_version_h)
#define _quanser_version_h

#include "quanser_types.h"

typedef struct tag_version
{
    t_uint32 size;      /* initialize to the size in bytes of the version structure */
    t_uint16 major;
    t_uint16 minor;
    t_uint16 release;
    t_uint16 build;
} t_version;

#endif
