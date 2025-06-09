#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/thomas/ros1/src/Quanser"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/thomas/ros1/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/thomas/ros1/install/lib/python3/dist-packages:/home/thomas/ros1/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/thomas/ros1/build" \
    "/usr/bin/python3" \
    "/home/thomas/ros1/src/Quanser/setup.py" \
     \
    build --build-base "/home/thomas/ros1/build/Quanser" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/thomas/ros1/install" --install-scripts="/home/thomas/ros1/install/bin"
