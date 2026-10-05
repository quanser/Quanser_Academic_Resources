#-----------------------------------------------------------------------------#
#----------------------Skills Progression 2 - Surveying-----------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 2 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_xy_scope(numSignals=5, 
                    name = 'Estimated Pose XY',
                    signalNames=['Integrated Pose Rate', 
                                 'Scan Match', 
                                 'Fused Compl.', 
                                 'Fused EKF',
                                 'Ref LiDAR Scan'])

observer.add_scope(numSignals=3, name = 'Acceleration', 
                   signalNames=['X', 'Y', 'Z'])

observer.add_scope(numSignals=3, name = 'Forward Speed', 
                   signalNames=['Integrated Accel', 
                                'Odom', 
                                'Fused'])

observer.add_scope(numSignals=3, name = 'Turn Speed',
                   signalNames=['Integrated Gyro Rate', 
                                'Odom', 
                                'Fused'])

observer.add_scope(numSignals=4, name = 'X Position Estimates',
                   signalNames=['Integrated Rate', 
                                'Correction', 
                                'Compl. Fused',
                                'EKF Fused'])
observer.add_scope(numSignals=4, name = 'Y Position Estimates',
                   signalNames=['Integrated Rate', 
                                'Correction', 
                                'Compl. Fused',
                                'EKF Fused'])
observer.add_scope(numSignals=4, name = 'Theta Estimates',
                   signalNames=['Integrated Rate', 
                                'Correction', 
                                'Compl. Fused',
                                'EKF Fused'])

# observer.add_scope(numSignals=3, name = 'EKF Pose Estimates',
#                    signalNames=['X', 'Y', 'theta'])

observer.launch()