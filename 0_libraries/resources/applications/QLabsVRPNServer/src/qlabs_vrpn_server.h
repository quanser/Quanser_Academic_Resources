#include <stdio.h>
#include <math.h>
#include <signal.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <tuple>
#include <array>
#include <conio.h>
#include "vrpn_Text.h"
#include "vrpn_Tracker.h"
#include "vrpn_Connection.h"
#include "quanser_messages.h"
#include "quanser_persistent_stream.h"
#include "quanser_thread.h"
#include "quanser_stream.h"


using std::cout;
using std::endl;
using std::stringstream;


// URIs to listen for connections for QLabs/RT models and tracker names
const std::string URI_DEFAULT = "tcpip://localhost:";
const std::array<std::string, 6> PORTS = {"18800", "18801", "18802",
                                          "18803", "18804", "18805"};
const std::array<char *, 6> TRACKER_NAMES = {"RigidBody",  "RigidBody1",
                                             "Rigidbody2", "RigidBody3",
                                             "RigidBody4", "RigidBody5"};

// Max and default no. of virtual drones
const int kMinNumQDrones = 1;
const int kMaxNumQDrones = 6;

// Ctrl+C handler
static void control_c_handler(int signum);

// Class to stream pose data from QLabs (virtual)
class QVirtualPose {
public:
    t_double *data_array = new t_double[10];
    const char *urid;
    t_error result_conn = 0;

    QVirtualPose(const char *uri, t_boolean nonblocking = false,
                 t_int send_buffer_size = 1460,
                 t_int receive_buffer_size = 1460);

    virtual ~QVirtualPose(){};
    int connect();
    void receive_data();

private:
    // Config parameters
    t_boolean _nonblocking = false;
    t_int _send_buffer_size = 80;
    t_int _receive_buffer_size = 80;;
    char *_locale = NULL;
    t_stream _client = NULL;
    t_error _result_client_stream = 0;
    char _message[512] = {};
};


/* TRACKER */
// Tracker class inherits from vrpn_Tracker class
class QTracker : public vrpn_Tracker {
public:
    QVirtualPose *vpose;

    QTracker(QVirtualPose *pose, const char *name = NULL, vrpn_Connection *c = 0);
    virtual ~QTracker(){};

    void transmit_data();
    virtual void mainloop();
 
protected:
    struct timeval _timestamp = {0, 0};
};


