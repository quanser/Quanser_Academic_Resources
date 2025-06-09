classdef QLabsSplineLine < QLabsActor
    properties (Constant)
        ID_SPLINE_LINE = 180
%       Class ID
    
        FCN_SPLINE_LINE_SET_POINTS = 12
        FCN_SPLINE_LINE_SET_POINTS_ACK = 13
    
        LINEAR = 0
%       See configurations
        CURVE = 1
%       See configurations
        CONSTANT = 2
%       See configurations
        CLAMPED_CURVE = 3
%       See configurations
    end
    methods
        function obj = QLabsSplineLine(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_SPLINE_LINE;
        end
        

        function success = set_points(obj, color, pointList, alignEndPontTangents, waitForConfirmation)
            arguments 
                obj QLabsSplineLine
                color (1,3) single
                pointList (:,4) single
                alignEndPontTangents logical = false
                waitForConfirmation logical = true
            end
            success = false;

%             After spawning the origin of the spline actor, this method is used to create the individual points. At least 2 points must be specified to make a line.

            obj.c.classID = obj.ID_SPLINE_LINE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_SPLINE_LINE_SET_POINTS;         
            obj.c.payload = [flip(typecast(single(color(1)), 'uint8')) ...
                             flip(typecast(single(color(2)), 'uint8')) ...
                             flip(typecast(single(color(3)), 'uint8')) ...
                             uint8(alignEndPontTangents)];
            
            for point = 1:size(pointList, 1)
                obj.c.payload = [obj.c.payload ...
                                 flip(typecast(single(pointList(point, 1)), 'uint8')) ...
                                 flip(typecast(single(pointList(point, 2)), 'uint8')) ...
                                 flip(typecast(single(pointList(point, 3)), 'uint8')) ...
                                 flip(typecast(single(pointList(point, 4)), 'uint8'))];
                
            end

            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive()
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_SPLINE_LINE, obj.actorNumber, obj.FCN_SPLINE_LINE_SET_POINTS_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end
                success = true;
                return
            end
        end

        function success = circle_from_center(obj, radius, lineWidth, color, numSplinePoints, waitForConfirmation)
            arguments
                obj QLabsSplineLine
                radius single
                lineWidth single = 0.1
                color (1,3) single = [1 0 0]
                numSplinePoints single = 8
                waitForConfirmation logical = true
            end

%             After spawning the origin of the spline actor, this method is used to create a circle. Configuration 1 is recommended when spawning the line.


            points = [];
            for angle = 0:(numSplinePoints-1)
                points = [points
                          radius*sin(angle/numSplinePoints*pi*2), radius*cos(angle/numSplinePoints*pi*2), 0, lineWidth];
            end

            points = [points
                      points(1,:)];
            
            pointList = points;
            alignEndPointTangents = true;
            success = obj.set_points(color, pointList, alignEndPointTangents, waitForConfirmation);
            return
        end

        function success = arc_from_center(obj, radius, startAngle, endAngle, lineWidth, color, numSplinePoints, waitForConfirmation)
            arguments
                obj QLabsSplineLine
                radius single
                startAngle single = 0
                endAngle single = pi/2
                lineWidth single = 1
                color (1,3) single = [1 0 0]
                numSplinePoints single = 8
                waitForConfirmation logical = true
            end
            success = false;

%             After spawning the origin of the spline actor, this method is used to create an arc. Configuration 1 is recommended when spawning the line.

            points = [];

            for angle = 0:numSplinePoints
                points = [points
                          radius*cos(angle/numSplinePoints*(endAngle-startAngle)+startAngle), radius*sin(angle/numSplinePoints*(endAngle-startAngle)+startAngle), 0, lineWidth];
            end  

            alignEndPointTangents = false;
            pointList = points;
            success = obj.set_points(color, pointList, alignEndPointTangents);
            return
        end

        function success = arc_from_center_degrees(obj, radius, startAngle, endAngle, lineWidth, color, numSplinePoints, waitForConfirmation)
            arguments
                obj QLabsSplineLine
                radius single
                startAngle single = 0
                endAngle single = 90
                lineWidth single = 1
                color (1,3) single = [1 0 0]
                numSplinePoints single = 4
                waitForConfirmation logical = true
            end
            success = false;

%             After spawning the origin of the spline actor, this method is used to create an arc. Configuration 1 is recommended when spawning the line.

            startAngle = startAngle/180*pi;
            endAngle = endAngle/180*pi;
            success = obj.arc_from_center(radius, startAngle, endAngle, lineWidth, color, numSplinePoints, waitForConfirmation);
            return
        end

        function success = rounded_rectangle_from_center(obj, cornerRadius, xWidth, yLength, lineWidth, color, waitForConfirmation)
            arguments
                obj QLabsSplineLine
                cornerRadius single
                xWidth single
                yLength single
                lineWidth single = 0.1
                color (1,3) single = [1 0 0]
                waitForConfirmation logical = true
            end
            success = false;

%             After spawning the origin of the spline actor, this method is used to create a rounded rectangle. Configuration 1 is recommended when spawning the line.

            points = obj.spawn_spline_rounded_rectangle_from_center_point_list(cornerRadius, xWidth, yLength, lineWidth);

            alignEndPointTangents = true;
            success = obj.set_points(color, points, alignEndPointTangents);
            return
        end

        function success = spawn_spline_rounded_rectangle_from_center_point_list(obj, cornerRadius, xWidth, yLength, lineWidth)
            arguments
                obj QLabsSplineLine
                cornerRadius single
                xWidth single
                yLength single
                lineWidth single = 1
            end
            success = false;

            if (xWidth <= cornerRadius*2)
                xWidth = cornerRadius*2;
            end

            if (yLength <= cornerRadius*2)
                yLength = cornerRadius*2;
            end

            circleSegmentLength = pi*cornerRadius*2/8;

            xCount = ceil((xWidth - 2*cornerRadius)/circleSegmentLength);
            yCount = ceil((yLength - 2*cornerRadius)/circleSegmentLength);

            % Y
            % ▲
            % │
            % ┼───► X
            %
            %   4───────3
            %   │       │
            %   │   ┼   │
            %   │       │
            %   1───────2

            offset225deg = cornerRadius-cornerRadius*sin(pi/8);
            offset45deg = cornerRadius-cornerRadius*sin(pi/8*2);
            offset675deg = cornerRadius-cornerRadius*sin(pi/8*3);

            % corner 1

            points = [-xWidth/2, -yLength/2+cornerRadius, 0, lineWidth
                      -xWidth/2+offset675deg, -yLength/2+offset225deg, 0, lineWidth
                      -xWidth/2+offset45deg, -yLength/2+offset45deg, 0, lineWidth
                      -xWidth/2+offset225deg, -yLength/2+offset675deg, 0, lineWidth
                      -xWidth/2+cornerRadius,-yLength/2, 0, lineWidth];

            

            % x1
            if (xWidth > cornerRadius*2)
                sideSegmentLength = (xWidth - 2*cornerRadius)/xCount;

                for sideCount = 1:(xCount-1)
                    points = [points
                              -xWidth/2+cornerRadius + sideCount*sideSegmentLength,-yLength/2, 0, lineWidth];
                end

                points = [points
                          xWidth/2-cornerRadius,-yLength/2, 0, lineWidth];
            end

            

            % corner 2
            points = [points
                      xWidth/2-offset225deg, -yLength/2+offset675deg, 0, lineWidth
                      xWidth/2-offset45deg, -yLength/2+offset45deg, 0, lineWidth
                      xWidth/2-offset675deg, -yLength/2+offset225deg, 0, lineWidth
                      xWidth/2, -yLength/2+cornerRadius, 0, lineWidth];

           

            % y1
            if (yLength > cornerRadius*2)
                sideSegmentLength = (yLength - 2*cornerRadius)/yCount;

                for sideCount = 1:(yCount-1)
                   points = [points
                             xWidth/2, -yLength/2+cornerRadius  + sideCount*sideSegmentLength, 0, lineWidth];
                end

                points = [points
                          xWidth/2, yLength/2-cornerRadius, 0, lineWidth];
            end

            % corner 3
            points = [points
                      xWidth/2-offset675deg, yLength/2-offset225deg, 0, lineWidth
                      xWidth/2-offset45deg, yLength/2-offset45deg, 0, lineWidth
                      xWidth/2-offset225deg, yLength/2-offset675deg, 0, lineWidth
                      xWidth/2-cornerRadius, yLength/2, 0, lineWidth];
            
            % x2
            if (xWidth > cornerRadius*2)
                sideSegmentLength = (xWidth - 2*cornerRadius)/xCount;
                
                for sideCount = 1:(xCount-1)
                    points = [points
                              xWidth/2-cornerRadius - sideCount*sideSegmentLength, yLength/2, 0, lineWidth];
                end
                
                points = [points
                          -xWidth/2+cornerRadius, yLength/2, 0, lineWidth];
            end

            % corner 4
            points = [points
                      -xWidth/2+offset225deg, yLength/2-offset675deg, 0, lineWidth
                      -xWidth/2+offset45deg, yLength/2-offset45deg, 0, lineWidth
                      -xWidth/2+offset675deg, yLength/2-offset225deg, 0, lineWidth
                      -xWidth/2, yLength/2-cornerRadius, 0, lineWidth];

            % y2
            if (yLength > cornerRadius*2)
                sideSegmentLength = (yLength - 2*cornerRadius)/yCount;
                    
                for sideCount = 1:(yCount-1)
                    points = [points
                              -xWidth/2, yLength/2-cornerRadius - sideCount*sideSegmentLength, 0, lineWidth];
                end

                points = [points
                      points(1,:)];

                success = points;
                return
            end
        end
    end
end