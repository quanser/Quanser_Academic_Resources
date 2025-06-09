#if !defined(_quanser_video_h)
#define _quanser_video_h

/*
#if !defined(__cplusplus)
#error Use of the Quanser Image Processing blockset requires the C++ language. Be sure to select C++ for the Language option of the Code Generation/Target selection section of the Configuration Parameters dialog for the model.
#endif
*/

#include "quanser_errors.h"
#include "quanser_extern.h"

#if 0
#if defined(__cplusplus) && !defined(__LINUX_RT_ARMV7__)
#include <opencv2/core/core.hpp>
typedef class cv::Mat              t_image;
#endif
#endif

typedef struct tag_video_capture * t_video_capture;
typedef struct tag_video_display * t_video_display;
typedef struct tag_video_window  * t_video_window;
typedef struct tag_video_sink    * t_video_sink;

typedef enum tag_image_format
{
    IMAGE_FORMAT_COL_MAJOR_PLANAR_RGB,      /* column-major planar RGB H x W x 3 */
    IMAGE_FORMAT_COL_MAJOR_GRAYSCALE,       /* column major H x W */
    IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR, /* row-major interleaved BGR 3 x W x H suitable for OpenCV CV_8UC3 matrices (image data type must be IMAGE_DATA_TYPE_UINT8 in this case) */
    IMAGE_FORMAT_ROW_MAJOR_GRAYSCALE,       /* column major W x H suitable for OpenCV CV_8UC1 matrices (image data type must be IMAGE_DATA_TYPE_UINT8 or IMAGE_DATA_TYPE_UINT16 in this case) */
    IMAGE_FORMAT_COMPRESSED,                /* compressed image (image data type must be IMAGE_DATA_TYPE_UINT8 in this case) */

    NUMBER_OF_IMAGE_FORMATS
} t_image_format;

typedef enum tag_video_output_format
{
    VIDEO_OUTPUT_FORMAT_H264,  /* H.264 video. */
    VIDEO_OUTPUT_FORMAT_WMV3,  /* Windows Media Video 9 codec. */

    NUMBER_OF_VIDEO_OUTPUT_FORMATS
} t_video_output_format;

typedef enum tag_image_data_type
{
    IMAGE_DATA_TYPE_UINT8,
    IMAGE_DATA_TYPE_UINT16,
    IMAGE_DATA_TYPE_UINT32,
    IMAGE_DATA_TYPE_SINGLE,
    IMAGE_DATA_TYPE_DOUBLE,

    NUMBER_OF_IMAGE_DATA_TYPES
} t_image_data_type;

typedef void (* t_video_display_menu_callback)(t_video_window window);

typedef enum tag_video_capture_property_code
{
    VIDEO_CAPTURE_PROPERTY_BRIGHTNESS,
    VIDEO_CAPTURE_PROPERTY_CONTRAST,
    VIDEO_CAPTURE_PROPERTY_HUE,
    VIDEO_CAPTURE_PROPERTY_SATURATION,
    VIDEO_CAPTURE_PROPERTY_SHARPNESS,
    VIDEO_CAPTURE_PROPERTY_GAMMA,
    VIDEO_CAPTURE_PROPERTY_COLOREFFECT,             /* see t_video_capture_color_effect below for valid values */
    VIDEO_CAPTURE_PROPERTY_WHITEBALANCE,
    VIDEO_CAPTURE_PROPERTY_BACKLIGHTCOMPENSATION,
    VIDEO_CAPTURE_PROPERTY_GAIN,

    VIDEO_CAPTURE_PROPERTY_PAN,
    VIDEO_CAPTURE_PROPERTY_TILT,
    VIDEO_CAPTURE_PROPERTY_ROLL,
    VIDEO_CAPTURE_PROPERTY_ZOOM,
    VIDEO_CAPTURE_PROPERTY_EXPOSURE,
    VIDEO_CAPTURE_PROPERTY_IRIS,
    VIDEO_CAPTURE_PROPERTY_FOCUS,

    NUMBER_OF_VIDEO_CAPTURE_PROPERTIES
    
} t_video_capture_property_code;

typedef enum tag_video_capture_color_effect
{
    COLOR_EFFECT_NONE,
    COLOR_EFFECT_BLACK_AND_WHITE,
    COLOR_EFFECT_SEPIA,
    COLOR_EFFECT_NEGATIVE,
    COLOR_EFFECT_EMBOSS,
    COLOR_EFFECT_SKETCH,
    COLOR_EFFECT_SKY_BLUE,
    COLOR_EFFECT_GRASS_GREEN,
    COLOR_EFFECT_SKIN_WHITEN,
    COLOR_EFFECT_VIVID,
    COLOR_EFFECT_AQUA,
    COLOR_EFFECT_ART_FREEZE,
    COLOR_EFFECT_SILHOUETTE,
    COLOR_EFFECT_SOLARIZATION,
    COLOR_EFFECT_ANTIQUE,

    NUMBER_OF_COLOR_EFFECTS

} t_video_capture_color_effect;

typedef struct tag_video_window_attributes
{
    /* Size of the structure. Set to sizeof(t_video_window_attributes). */
    size_t size;

    /* Window position and size */
    int x;
    int y;
    int cx;
    int cy;
} t_video_window_attributes;

/*typedef struct tag_video_sink_attributes
{
    char * filename;
    t_double frame_rate;
    t_uint bit_rate;
    t_uint frame_width;
    t_uint frame_height;
    t_video_output_format video_format;
    t_image_format image_format;
    t_image_data_type data_type;
} t_video_sink_attributes;*/

typedef struct tag_video_capture_attribute
{
    t_double                      value;            /* value when property is being set manually (either 0..100% or 1..N) */
    t_video_capture_property_code property_code;    /* property code */
    t_boolean                     manual;           /* whether property is being set manually or is being configured as automatic */
    t_boolean                     is_enumeration;   /* value specified as 1..N rather than 0..100% */
} t_video_capture_attribute;

/*
 * Valid URLs:
 *
 *     C:\Users\Me\Videos     - capture video from a file (path specified without file: scheme)
 *     file://localhost/path  - capture video from a file
 *     http://host/path       - capture video from the web (only supported in Windows). The https scheme should also be supported (or other valid Internet schemes supported by Media Foundation).
 *     video://localhost:id   - capture video from a camera or other device
 *
 * Note that additional options could potentially be specified as query options in the URL.
 *
 * The format argument describes the format expected in the image_data. The image_data is a pointer to the buffer in which
 * to store one frame of the captured image. It must remain valid for the life of the t_video_capture handle. Its size must
 * be H x W x C bytes, where C = 3 for colour images and C = 1 for grayscale images.
 *
 * If the image format is IMAGE_FORMAT_OPENCV_BGR then the data is stored in CV_8UC3 format, which is a row-major interleaved format.
 * In other words, the BGR components of each pixel are stored contiguously, with one byte per colour component, and pixels are stored
 * row-by-row.
 *
 * If the image format is IMAGE_FORMAT_OPENCV_GRAYSCALE then the data is stored in CV_8UC1 format, which is a row-major format.
 * In other words, there is one byte per pixel, and pixels are stored row-by-row.
 *
 * If the image format is IMAGE_FORMAT_SIMULINK_RGB then the data is stored in a column-major planar format.
 * In other words, pixels are stored column-by-column, with all the red components stored together, followed by all the green
 * components and finally all the blue components.
 *
 * If the image format is IMAGE_FORMAT_SIMULINK_GRAYSCALE then the data is stored in column-major format.
 * In other words, there is one byte per pixel, and pixels are stored column-by-column.
 */
EXTERN t_error
video_capture_open(const char * url, t_double frame_rate, t_uint frame_width, t_uint frame_height, t_image_format format, t_image_data_type data_type,
                   void * image_data, t_video_capture * capture, const t_video_capture_attribute * attributes, t_uint num_attributes);

/*
** Set properties for the video capture. The property values will be updated when the next frame is read.
*/
EXTERN t_error
video_capture_set_property(t_video_capture capture, t_video_capture_attribute * attributes, t_uint num_attributes);

/*
** Start video capture. This function should be called from the same thread as video_capture_read.
*/
EXTERN t_error
video_capture_start(t_video_capture capture);

/*
 * Read one frame from the image source. The image is stored in the image buffer supplied to the video_capture_open function.
*  This function returns 1 if a new image is read. Returns 0 if no new image is currently available.
 * Otherwise returns a negative error code.
 */
EXTERN t_error
video_capture_read(t_video_capture capture);

/*
** Stop video capture. This function should be called from the same thread as video_capture_read.
*/
EXTERN t_error
video_capture_stop(t_video_capture capture);

/* Close the video capture handle */
EXTERN t_error
video_capture_close(t_video_capture capture);

/*
** Open a video display window. The title of the window will be the given name.
*/
EXTERN t_error
video_display_open(const char * name, const t_video_window_attributes * attributes, t_video_window * window);

/*
** Change the title of the video display window.
*/
EXTERN t_error
video_display_set_caption(t_video_window window, const char * text);

/*
** Add a menu item to the context menu of the specified video display window. The menu item is given the specified name
** and the callback is invoked when the menu item is selected.
*/
EXTERN t_error
video_display_add_menu_item(t_video_window window, const char * name, t_video_display_menu_callback callback);

/*
** Add a menu separator to the context menu of the specified video display window.
*/
EXTERN t_error
video_display_add_menu_separator(t_video_window window);

/*
** Attach a video stream to the specified window. Video frames should be written to the window
** at the given frame rate and dimensions, and with the given format and data type. If hardware_accelerated is true
** then GPU hardware acceleration will be used for the video. If no hardware acceleration is available then it should
** fall back to software rendering even if this flag is set, so it is highly recommended to enable hardware acceleration.
**
** In the case of the IMAGE_FORMAT_COMPRESSED image format, the frame_width and frame_height may be zero. They will be
** set internally based on the image data. Images compressed as BMP, PNG, ICO, JPEG, TIFF, GIF and HD Photo should be
** supported. The data_type in this case should always be IMAGE_DATA_TYPE_UINT8.
*/
EXTERN t_error
video_display_attach(t_video_window window, t_double frame_rate, t_uint frame_width, t_uint frame_height, t_image_format format, t_image_data_type data_type,
                     t_boolean hardware_accelerated, t_video_display * display);

/*
** Write a frame to the video display. The length in elements must be specified, particularly for the IMAGE_FORMAT_COMPRESSED
** image format, for which data is not a constant size. The image_data must match the image format, data type and dimensions
** specified in the video_display_attach call. Note that the length is not in bytes, but in elements based on the image data type.
*/
EXTERN t_error
video_display_write(t_video_display display, const void * image_data, size_t image_data_length);

/*
** Detach the video stream from the display. No more video frames should be written to the display
** after detaching the video stream.
*/
EXTERN t_error
video_display_detach(t_video_display display);

/*
** Force the video display window to be visible.
*/
EXTERN t_error
video_display_show(t_video_window window);

/*
** Get the attributes of the window.
*/
EXTERN t_error
video_display_get_attributes(t_video_window window, t_video_window_attributes * attributes);

/*
** Close the video display window. The window should not be used after it is closed.
*/
EXTERN t_error
video_display_close(t_video_window window);

/*
** Open a video sink. The name can be a file or URL.
*/
EXTERN t_error
video_sink_open(char * filename, t_double frame_rate, t_uint bit_rate, t_uint frame_width, t_uint frame_height, t_video_output_format video_format, t_image_format image_format, t_image_data_type data_type, t_video_sink * sink);

/*
** Write a frame to the video sink. The length in elements must be specified, particularly for the IMAGE_FORMAT_COMPRESSED
** image format, for which data is not a constant size. Note that the length is not in bytes, but in elements based on the
** image data type.
*/
EXTERN t_error
video_sink_write(t_video_sink sink, const void * image_data, size_t image_data_length);

/*
** Close the video sink. The sink should not be used after it is closed.
*/
EXTERN t_error
video_sink_close(t_video_sink sink);

#endif
