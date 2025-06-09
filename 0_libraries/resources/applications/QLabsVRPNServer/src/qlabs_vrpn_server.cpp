#include "qlabs_vrpn_server.h"

/* ctrl+C handler */
volatile sig_atomic_t stop = 0;
static void control_c_handler(int signum) 
{ 
    stop = 1; 
}

/* QVIRTUALPOSE */
QVirtualPose::QVirtualPose(const char* uri, t_boolean nonblocking,
                           t_int send_buffer_size, t_int receive_buffer_size)
    : urid{uri}
    , _nonblocking{nonblocking}
    , _send_buffer_size{send_buffer_size}
    , _receive_buffer_size{receive_buffer_size}
{
}

// Connect - for opening a client stream to QLabs RT model server
int QVirtualPose::connect()
{
    // Attempt connection to QLabs server
    result_conn = stream_connect(urid, _nonblocking, _send_buffer_size,
                                  _receive_buffer_size, &_client);
    // Unable to connect
    if (result_conn != 0) 
    {
        msg_get_error_messageA(_locale, result_conn, _message,
                               sizeof(_message));
        printf("Unable to connect to URI '%s'.\n%s.\n", urid, _message);
    }

    // Connection established
    if (result_conn == 0)
        printf("Connected to uri: %s.\n", urid);

    return result_conn;
}

// Receive_data - x, y, z, roll, pitch, yaw, qw, qx, qy, qz
void QVirtualPose::receive_data()
{
    // Attempt data reception
    _result_client_stream = stream_receive_double_array(_client, data_array, 10); 
    
    // If an error occurs or not enough data available
    if (_result_client_stream <= 0) 
    {
        stream_close(_client);
        cout << "Connection closed! " << endl;
        msg_get_error_messageA(_locale, result_conn, _message,
                               sizeof(_message));
        printf("Error communicating with URI '%s'. %s\n", urid, _message);
    }

}

/* TRACKER */
QTracker::QTracker(QVirtualPose *pose, const char* name, vrpn_Connection* c)
    : vrpn_Tracker(name, c), vpose(pose)
{
}

// Transmit_data - for updating tracker pose with received data
void QTracker::transmit_data()
{
    vpose->receive_data();

    // Update the Qtracker pos array with received positions
    pos[0] = vpose->data_array[0];
    pos[1] = vpose->data_array[1]; 
    pos[2] = vpose->data_array[2];

    // Update the Qtracker d_quat array with the received quaternion. 
    // N/B: vrpn_Tracker uses the JPL convention.
    d_quat[0] = vpose->data_array[7];
    d_quat[1] = vpose->data_array[8];
    d_quat[2] = vpose->data_array[9];
    d_quat[3] = vpose->data_array[6];
};

// Tracker mainloop 
void QTracker::mainloop()
{
    // Timing
    vrpn_gettimeofday(&_timestamp, NULL);
    vrpn_Tracker::timestamp = _timestamp;

    // Call transmit_data to update pos and d_quat
    QTracker::transmit_data();

    // Pack and send via vrpn
    char msgbuf[1000];
    d_sensor = 0;
    int len = vrpn_Tracker::encode_to(msgbuf);

    if (d_connection->pack_message(len, _timestamp, position_m_id, d_sender_id,
        msgbuf, vrpn_CONNECTION_LOW_LATENCY)) {
        fprintf(stderr, "Can't write message: tossing\n");
    }
    server_mainloop();
}


int main(int argc, char *argv[])
{
    // Get user input as command line argument if available
    int number_of_drones = kMinNumQDrones;
    if (argc != 1) {
        stringstream user_input{argv[1]};
        user_input >> number_of_drones;
        
        if (number_of_drones > kMaxNumQDrones || number_of_drones < kMinNumQDrones) {
            cout << "Number of virtual QDrones has been set to "
                 << number_of_drones << endl;
            cout << "Please set to a number between " << kMinNumQDrones
                 << " and " << kMaxNumQDrones << " and rerun the batch script." << endl;
            cout << "Terminating..." << endl;

            return 1;
        }
    }
    cout << "No. of virtual QDrones: " << number_of_drones << endl;

    std::vector<std::tuple<QVirtualPose*, int>> poses;
    std::vector<QTracker*> trackers;
    poses.reserve(number_of_drones);
    trackers.reserve(number_of_drones);
    
    // Register Ctrl+C handler
    signal(SIGINT, control_c_handler);
    
    // Create a network server connection
    vrpn_Connection_IP *m_Connection = new vrpn_Connection_IP();

    // Create virtual poses    
    for (int i = 0; i < number_of_drones; ++i) 
    {
        std::string uri = URI_DEFAULT + PORTS[i];        
        QVirtualPose *qd_pose = new QVirtualPose(uri.c_str());
        int result = qd_pose->connect();
        poses.emplace_back(std::make_tuple(qd_pose, result));
    }
        
    // Create a tracker for each pose
    for (int i = 0; i < number_of_drones; ++i) 
    {
        QTracker* server_tracker = new QTracker(std::get<0>(poses[i]), TRACKER_NAMES[i], m_Connection);
        trackers.emplace_back(server_tracker);
    }

    std::vector<int> connection_result;
    for (int i = 0; i < number_of_drones; ++i) 
    {
        if ( std::get<1>(poses[i]) != 0 ) 
        {
            connection_result.emplace_back(i);
        }
    }

    // If there's an error connecting to QLabs
    if (connection_result.size() > 0) 
    {
        cout << "Make sure QLabs is running and the RT model(s) is loaded." << endl;
    }
    else 
    {   
        // receive and send the data via vrpn
        while (!stop) 
        {
            for (int i = 0; i < number_of_drones; ++i) 
            {
                trackers[i]->mainloop();
            }
            m_Connection->mainloop();
        }
    }

    // Housekeeping
    for (auto &tracker : trackers) {
        delete tracker;
    }
    for (int i = 0; i < number_of_drones; ++i) {
        delete std::get<0>(poses[i]);
    }    
    cout << "\nPress any key to exit..." << endl;
    getch();
    return 0;
}