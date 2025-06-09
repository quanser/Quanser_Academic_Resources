#if !defined(_quanser_memory_h)
#define _quanser_memory_h

#include <stddef.h>

#include "quanser_extern.h"
#include "quanser_types.h"

#define memory_free_and_nullify(object) \
    do {                                \
        memory_free(object);            \
        object = NULL;                  \
    } while (0)

/*
    Description:

    This function allocates the given number of bytes of memory
    on the stack. This memory is owned by the process. It returns a pointer
    to the allocated memory. It generates a stack overflow exception
    if the memory could not be allocated so do not use this function
    for large memory allocations!

    The memory is not zero-initialized. It does not need to be freed
    as it will be free automatically when the variable goes out of scope.

    NOTE: stack_free MUST be called to release the allocated memory as some
          platforms use the heap instead of the stack.

    Parameters:

    num_bytes = the number of bytes to allocate

    Return values:

    A pointer to the allocated memory.
*/
#if defined(_WIN32) || defined(_WIN64)
#include <malloc.h>
#define stack_allocate(num_bytes)   _alloca(num_bytes)
#define stack_free(ptr)             do {} while (false)
#elif  defined(__vxworks)
#define stack_allocate(num_bytes)   memory_allocate(num_bytes)
#define stack_free(ptr)             memory_free(ptr)
#else
#include <alloca.h>
#define stack_allocate(num_bytes)   alloca(num_bytes)
#define stack_free(ptr)             do {} while (false)
#endif

/*
    Description:

    This function allocates the given number of bytes of memory.
    This memory is owned by the process. It returns a pointer
    to the allocated memory or NULL if the allocation failed.
    The memory is not zero-initialized.

    Parameters:

    num_bytes = the number of bytes to allocate

    Return values:

    A pointer to the allocated memory. If there's not enough memory
    available then NULL is returned.
*/
EXTERN void *
memory_allocate(size_t num_bytes);

/*
    Description:

    This function resizes a memory block. The memory must be
    owned by the process. It returns a pointer to the reallocated
    memory or NULL if the reallocation failed. The returned pointer
    is not guaranteed to be the same as the original memory
    pointer. In this case, the original memory is copied over
    to the new memory. If the size of the memory block is increased
    the extra memory is not zero-initialized.

    If the memory pointer passed in is NULL then a new memory block
    is allocated.

    If the reallocation fails then the original memory block remains
    valid so be sure to maintain a pointer to the original memory.

    However, if the reallocation succeeds and new memory had to be
    allocated than the original memory block will be no longer be
    valid.

    Parameters:

    memory    = a pointer to the original memory block (may be NULL)
    num_bytes = the number of bytes to which to resize the memory block

    Return values:

    A pointer to the reallocated memory. If there's not enough memory
    available then NULL is returned.
*/
EXTERN void *
memory_reallocate(void * memory, size_t num_bytes);

/*
    Description:

    This function frees the memory allocated by memory_allocate.
    If the argument is NULL then this function does nothing.

    Parameters:

    memory = the allocated memory to free
*/
EXTERN void
memory_free(void * memory);

/*
    Description:

    This function copies bytes from source address to the destination
    address. The source and destination should not overlap.

    Parameters:

    destination = the address to which to copy the bytes
    num_bytes   = the number of bytes to copy
    source      = the address from which to copy the bytes
*/
EXTERN void
memory_copy(void * destination, size_t num_bytes, const void * source);

/*
    Description:

    This function copies bytes from source address to the destination
    address. The source and destination may overlap.

    Parameters:

    destination = the address to which to copy the bytes
    num_bytes   = the number of bytes to copy
    source      = the address from which to copy the bytes
*/
EXTERN void
memory_move(void * destination, size_t num_bytes, const void * source);

/*
    Description:

    This function sets the memory to zero.

    Parameters:

    destination = the address to zero
    num_bytes   = the number of bytes to zero
*/
EXTERN void
memory_zero(void * destination, size_t num_bytes);

/*
    Description:

    This function compares the left and right buffers.
    It returns true if the two are equal and false otherwise.

    Parameters:

    left      = the address of the first buffer to compare
    num_bytes = the number of bytes to compare
    right     = the address of the second buffer to compare
*/
EXTERN t_boolean
memory_equal(const void * left, size_t num_bytes, const void * right);

/*
    Description:

    This function searches the source for the contents of the buffer.
    It returns the address in the source of the location found or
    NULL if the buffer contents could not be found in the source.
    This function is similar to string_find_substring except that
    it operates on arbitrary bytes rather than strings.

    Parameters:

    source      = the address of the source buffer to search
    source_size = the number of bytes in the source buffer
    buffer      = the address of the contents for which to search
    buffer_size = the number of bytes in the buffer
*/
EXTERN const void *
memory_find(const void * source, size_t source_size, const void * buffer, size_t buffer_size);

#endif
