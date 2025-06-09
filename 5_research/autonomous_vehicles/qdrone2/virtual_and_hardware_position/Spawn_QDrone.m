function Spawn_QDrone()
    %% Communications
    
    try
        qlabs = QuanserInteractiveLabs();
    catch ME
         if (strcmp(ME.identifier,'MATLAB:UndefinedFunction'))
             disp('Please make sure the QLabs API is in your Matlab path to use this script.')
         else
             rethrow(ME)
         end
         return
    end

    connection_established = qlabs.open('localhost');
    
    if connection_established == false
        disp("Failed to open connection to QLabs.  Please ensure QLabs is running and an open world environment is loaded.")
        return
    end

    disp('Connected to QLabs.')

    %% Reset environment
    
    num_destroyed = qlabs.destroy_all_spawned_actors();
    disp('Destroyed all actors.')



    %% Spawn new actors
    hShape = QLabsBasicShape(qlabs, true);
    
    box_mass = 10.0;
    
    hShape.spawn([8,-1,0.5], [0,0,0], [1,1,1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.8,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);
    
    hShape.spawn([8,1,0.5], [0,0,0], [1,1,1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.8,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);

    hShape.spawn([8,0,1.1], [0,0,0], [1,3,0.1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.6,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);

    hShape.spawn([8,-1,1.8], [0,0,0], [1,1,1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.8,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);

    hShape.spawn([8,1,1.8], [0,0,0], [1,1,1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.8,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);

    hShape.spawn([8,0,2.5], [0,0,0], [1,3,0.1], hShape.SHAPE_CUBE, true);
    hShape.set_material_properties([0.6,0,0], 1, false, true);
    hShape.set_physics_properties(true, box_mass, 0.01, 0.0, 0.0, 0.7, hShape.COMBINE_AVERAGE, 0.3, hShape.COMBINE_AVERAGE, true);

    disp('Created boxes.')


    % Destroy the previous QBot and respawn it in a starting position

    hQDrone = QLabsQDrone2(qlabs, true);
    hQDrone.spawn_id_degrees(0, [0, 0, 0.1], [0,0,0], [1,1,1], 0);
    hQDrone.possess(hQDrone.VIEWPOINT_TRAILING);

    fprintf('Created QDrone 2 with actor number %u.\n', hQDrone.actorNumber);


    %% Close communications
    qlabs.close()
    disp("Closed connection to QLabs.")
    disp("Done!")

end