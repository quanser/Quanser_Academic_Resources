function [out_dist, out_iq] = sensors_ultrasonic_iq
%TEST_HIL_MECH_SENSORS_TRAINER_USB_ULTRASONIC_IQ Reads ultrasonic IQ data and plots it in real-time.

b = hil_open('mech_sensors_trainer_usb', '0');
try
    % Configure the ultrasonic sensor for the IQ service and the full 0 to 5m range
    hil_set_card_specific_options(b, 'accel_avg=1;accel_filter=246;accel_fs=16;accel_rate=1125;adc1_os=64;adc2_os=64;adc3_os=16;btn0_pol=1;btn1_pol=1;color_ag=4.0;color_dg=4;color_int=50;dio0_mode=digital;dio1_mode=digital;dio2_mode=digital;dio3_mode=digital;enc_dir=0;enc_mode=encoder;enc_freq=240000000;gyro_avg=1;gyro_filter=196.6;gyro_fs=2000;gyro_rate=1125;hum_over=2;knob_dir=0;load_gain=128;load_rate=320;press_over=4;radar_bins=0;radar_down=1;radar_gain=0.3;radar_hwaas=30;radar_len=1;radar_mur=6;radar_noise=0;radar_prof=3;radar_run=0.7;radar_samp=A;radar_serv=none;radar_start=0.2;radar_sweeps=16;radar_swprate=0;temp_filter=7932;temp_over=8;tof_freq=15;tof_int=2;tof_order=close;tof_res=8x8;tof_sharp=14;ultra_int=100;ultra_len=1.5;ultra_serv=iq;ultra_start=0.2;weather_filt=2;weather_standby=0.5;');
    
    disp("Press ESC to exit.");

    last_points = 0;

    % Read some ultrasonic IQ data
    other_input_channels = [10050000:10050449 21050000:21050899];
    
    data = hil_read_other(b, other_input_channels);
    dist = data(1:450);
    iq   = reshape(data(451:end), [2 450])';
    env  = sqrt(iq(:,1).^2 + iq(:,2).^2);

    figure(1);
    plt = plot(dist, iq);
    xlim([0 2.4]);
    ylim([-1 1]);

    figure(2);
    env_plt = plot(dist, env);
    
    while ~qc_get_key_state(27)
        data = hil_read_other(b, other_input_channels);
        dist = data(1:450);
        iq   = reshape(data(451:end), [2 450])';
        env  = sqrt(iq(:,1).^2 + iq(:,2).^2);
        length(data);
        length(dist);
        plt(1).XData = dist;
        plt(1).YData = iq(:,1);
        plt(2).XData = dist;
        plt(2).YData = iq(:,2);

        env_plt(1).XData = dist;
        env_plt(1).YData = env;
        
        drawnow;

        points = hil_read_other(b, [13065]); 
        if isempty(last_points) || any(points ~= last_points)
            fprintf(1, 'points=%f\r', points);
            last_points = points;
        end

    end

    hil_close(b);

catch me
    hil_close_all;
    me.rethrow;
end

if nargout > 0
    out_dist = dist;
end
if nargout > 1
    out_iq = iq;
end

end
