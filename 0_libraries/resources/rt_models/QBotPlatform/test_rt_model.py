import os
from qvl.real_time import QLabsRealTime

rtModel = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        'QBotPlatform_Workspace'
    )
)

QLabsRealTime().start_real_time_model(rtModel)
