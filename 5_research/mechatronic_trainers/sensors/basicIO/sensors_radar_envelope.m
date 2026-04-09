function [out_dist, out_env] = sensors_radar_envelope
%TEST_HIL_MECH_SENSORS_TRAINER_USB_RADAR_ENVELOPE Reads radar envelope data and plots it in real-time.

% persistent last_points

b = hil_open('mech_sensors_trainer_usb', '0');
try
    % Configure the radar for the envelope service and the full 0 to 7m range
    hil_set_card_specific_options(b, 'accel_avg=1;accel_filter=246;accel_fs=16;accel_rate=1125;adc1_os=64;adc2_os=64;adc3_os=16;btn0_pol=1;btn1_pol=1;color_ag=4.0;color_dg=4;color_int=50;dio0_mode=digital;dio1_mode=digital;dio2_mode=digital;dio3_mode=digital;enc_dir=0;enc_mode=encoder;enc_freq=240000000;gyro_avg=1;gyro_filter=196.6;gyro_fs=2000;gyro_rate=1125;hum_over=2;knob_dir=0;load_gain=128;load_rate=320;press_over=4;radar_bins=0;radar_down=1;radar_gain=0.3;radar_hwaas=30;radar_len=2;radar_mur=6;radar_noise=0;radar_prof=3;radar_run=0.7;radar_samp=A;radar_serv=envelope;radar_start=0.2;radar_sweeps=16;radar_swprate=0;temp_filter=7932;temp_over=8;tof_freq=15;tof_int=2;tof_order=close;tof_res=8x8;tof_sharp=14;ultra_int=100;ultra_len=2.4;ultra_serv=none;ultra_start=0;weather_filt=2;weather_standby=0.5;');
    
    disp("Press ESC to exit.");

    last_points = 0;

    % Read some radar envelope data
    other_input_channels = [10000000:10014454 21000000:21014454];
    
    env = hil_read_other(b, other_input_channels);
    dist = env(1:14455);
    env  = env(14456:end);
    

    plt = plot(dist, env);

    while ~qc_get_key_state(27)
        env = hil_read_other(b, other_input_channels);
        %dist = env(1:14455);
        %env  = env(14456:end);
        dist = env(1:4131); % with points being 4131
        env  = env(14456:14456+4130);
        plt.XData = dist;
        plt.YData = env;
        drawnow;

        points = hil_read_other(b, [13064]); 

        if isempty(last_points) || any(points ~= last_points)
            fprintf(1, 'points=%f\r', points);
            last_points = points;
        end

    end

    hil_close(b);

catch me
    hil_close(b);
    me.rethrow;
end

if nargout > 0
    out_dist = dist;
end
if nargout > 1
    out_env = env;
end

end
