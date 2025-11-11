import sys
import platform
import os
import math

######################### MODULAR CONTAINER CLASS #########################

class QLabsRealTime:
    """ The QLabsRealTime class is a collection of methods to start and stop pre-compiled real-time models to support open worlds in QLabs."""

    _URIPort = 17001

    # Initialize class
    def __init__(self):
       """ Constructor Method """
       return

    #def start_real_time_model(self, modelName, actorNumber=0, QLabsHostName='localhost', userArguments=True, additionalArguments=""):
    def start_real_time_model(self, modelName, actorNumber=0, QLabsHostName='localhost', RTModelHostName='localhost', userArguments=True, additionalArguments=""):
        """Starts pre-compiled real-time code made with QUARC or the Quanser APIs that has been designed to provide a real-time dynamic model and a virtual hardware interface. This function is for local execution only, but QLabs can still be running remotely.

        :param modelName: Filename of the model without extension.
        :param actorNumber: (Optional) The user defined identifier corresponding with a spawned actor of the same class and actor number. Only used for models with "workspace" in the model name.
        :param QLabsHostName: (Optional) The host name or IP address of the machine running QLabs. Only used for models with "workspace" in the model name.
        :param userArguments: (Optional) Enables using non-standard device unmbers and uris
        :param additionalArguments: (Optional) See QUARC documentation for additional quarc_run arguments.
        :type modelName: string
        :type actorNumber: uint32
        :type QLabsHostName: string
        :type additionalArguments: string
        :return: If the platform is supported, returns the command line used to start the model execution.
        :rtype: string

        """
        qlabs_rt_model = False
        if 'workspace' in modelName.lower() or 'spawn' in modelName.lower(): qlabs_rt_model = True

        if platform.system() == "Windows":
            if qlabs_rt_model:
                self._URIPort = 17001 + actorNumber
                if userArguments:
                    # this is a qlabs rt model, and use the QLabsHostName, _URIPort and actorNumber parameters
                    cmdString="start \"QLabs_{}_{}\" \"%QUARC_DIR%\\quarc_run\" -D -r -t tcpip://localhost:17000 \"{}.rt-win64\" -uri tcpip://localhost:{} -hostname {} -devicenum {} {}".format(modelName, actorNumber, modelName, self._URIPort, QLabsHostName, actorNumber, additionalArguments)
                else:
                    # this is a qlabs rt model, but don't use additional parameters
                    cmdString="start \"QLabs_{}_{}\" \"%QUARC_DIR%\\quarc_run\" -D -r -t tcpip://localhost:17000 \"{}.rt-win64\" {}".format(modelName, actorNumber, modelName, additionalArguments)

            else:
                # this is not a qlabs rt model, but a generic one for windows
                cmdString="start \"Generic_{}\" \"%QUARC_DIR%\\quarc_run\" -D -r -t tcpip://localhost:17000 \"{}.rt-win64\" {}".format(modelName, modelName, additionalArguments)
        elif platform.system() == "Linux":
            if platform.machine() == "armv7l":
                if qlabs_rt_model:
                    #Raspberry Pi 3, 4
                    if userArguments:
                        # this is a qlabs rt model, and use the QLabsHostName, _URIPort and actorNumber parameters
                        cmdString="quarc_run -D -r -t tcpip://localhost:17000 {}.rt-linux_pi_3 -uri tcpip://localhost:{} -hostname {} -devicenum {} {}".format(modelName, self._URIPort, QLabsHostName, actorNumber, additionalArguments)
                    else:
                        # this is a qlabs rt model, but don't use additional parameters
                        cmdString="quarc_run -D -r -t tcpip://localhost:17000 {}.rt-linux_pi_3 {}".format(modelName, additionalArguments)
                else:
                    print("This method cannot be used to deploy generic real-time models to this platform. Please refer to the QUARC command line tools documentation for more information.")
            elif platform.machine() == "x86_64":
                if qlabs_rt_model:
                    #Ubuntu x86_64
                    if userArguments:
                        # this is a qlabs rt model, and use the QLabsHostName, _URIPort and actorNumber parameters
                        #cmdString="quarc_run -D -r -t tcpip://host.docker.internal:17000 {}.rt-linux_x86_64 -uri tcpip://host.docker.internal:{} -hostname {} -devicenum {} {}".format(modelName, self._URIPort, QLabsHostName, actorNumber, additionalArguments)
                        cmdString="quarc_run -D -r -t tcpip://{}:17000 {}.rt-linux_x86_64 -uri tcpip://localhost:{} -hostname {} -devicenum {} {}".format(RTModelHostName, modelName, self._URIPort, QLabsHostName, actorNumber, additionalArguments)
                    else:
                        # this is a qlabs rt model, but don't use additional parameters
                        #cmdString="quarc_run -D -r -t tcpip://host.docker.internal:17000 {}.rt-linux_x86_64 {}".format(modelName, additionalArguments)
                        cmdString="quarc_run -D -r -t tcpip://{}:17000 {}.rt-linux_x86_64 {}".format(RTModelHostName, modelName, additionalArguments)
                else:
                    print("This method cannot be used to deploy generic real-time models to this platform. Please refer to the QUARC command line tools documentation for more information.")
            else:
                print("This Linux machine not supported for real-time model execution")
                return
        else:
            if qlabs_rt_model:
                print("Platform not supported for real-time model execution")
            else:
                print("This method cannot be used to deploy generic real-time models to this platform. Please refer to the QUARC command line tools documentation for more information.")
            return

        os.system(cmdString)

        self._URIPort = self._URIPort + 1
        return cmdString

    def terminate_real_time_model(self, modelName, RTModelHostName='localhost', additionalArguments=''):
        """Stops a real-time model specified by name that is currently running.

        :param modelName: Filename of the model without extension.
        :param additionalArguments: (Optional) See QUARC documentation for additional quarc_run arguments.
        :type modelName: string
        :type additionalArguments: string
        :return: If the platform is supported, returns the command line used to stop the model execution.
        :rtype: string

        """
        if platform.system() == "Windows":
            cmdString="start \"QLabs_Spawn_Model\" \"%QUARC_DIR%\\quarc_run\" -q -Q -t tcpip://localhost:17000 {}.rt-win64 {}".format(modelName, additionalArguments)
        elif platform.system() == "Linux":
            if platform.machine() == "armv7l":
                cmdString="quarc_run -q -Q -t tcpip://localhost:17000 {}.rt-linux_pi_3 {}".format(modelName, additionalArguments)
            elif platform.machine() == "x86_64":
                #cmdString="quarc_run -q -Q -t tcpip://host.docker.internal:17000 {}.rt-linux_x86_64 {}".format(modelName, additionalArguments)
                cmdString="quarc_run -q -Q -t tcpip://{}:17000 {}.rt-linux_x86_64 {}".format(RTModelHostName, modelName, additionalArguments)
            else:
                print("This Linux machine not supported for real-time model execution")
                return

        else:
            print("Platform not supported for real-time model execution")
            return

        os.system(cmdString)
        return cmdString

    def terminate_all_real_time_models(self, RTModelHostName='localhost', additionalArguments=''):
        """Stops all real-time models currently running.

        :param additionalArguments: (Optional) See QUARC documentation for additional quarc_run arguments.
        :type additionalArguments: string
        :return: If the platform is supported, returns the command line used to stop the model execution.
        :rtype: string

        """
        if platform.system() == "Windows":
            cmdString="start \"QLabs_Spawn_Model\" \"%QUARC_DIR%\\quarc_run\" -q -Q -t tcpip://localhost:17000 *.rt-win64 {}".format(additionalArguments)
        elif platform.system() == "Linux":
            if platform.machine() == "armv7l":
                cmdString="quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_pi_3 {}".format(additionalArguments)
            elif platform.machine() == "x86_64":
                #cmdString="quarc_run -q -Q -t tcpip://host.docker.internal:17000 *.rt-linux_x86_64 {}".format(additionalArguments)
                cmdString="quarc_run -q -Q -t tcpip://{}:17000 *.rt-linux_x86_64 {}".format(RTModelHostName, additionalArguments)
            else:
                print("This Linux machine not supported for real-time model execution")
                return

        else:
            print("Platform not supported for real-time model execution")
            return

        os.system(cmdString)
        return cmdString