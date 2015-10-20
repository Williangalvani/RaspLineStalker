__author__ = 'will'
from vreptest import vrep
import time

class RobotInterface():

    def __init__(self):
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        vrep.simxStartSimulation(self.clientID,vrep.simx_opmode_oneshot)

        vrep.simxSynchronous(self.clientID, False)
        print "connected with id ", self.clientID

        self.left_wheel = None
        self.right_wheel = None
        self.camera = None
        self.setup()
        self.lastimageAcquisitionTime = 0

    def finish_iteration(self):
        vrep.simxSynchronousTrigger(self.clientID)

    def set_right_speed(self, speed):
        vrep.simxSetJointTargetVelocity(self.clientID, self.right_wheel, speed, vrep.simx_opmode_oneshot_wait)

    def set_left_speed(self, speed):
        vrep.simxSetJointTargetVelocity(self.clientID, self.left_wheel, speed, vrep.simx_opmode_oneshot_wait)

    def read_camera(self):
        data = vrep.simxGetVisionSensorImage(self.clientID,self.camera,1,vrep.simx_opmode_buffer)
        if data[0] == vrep.simx_return_ok :
            return data
        else:
            time.sleep(0.001)
        return None

    def stop(self):
        vrep.simxStopSimulation(self.clientID,vrep.simx_opmode_oneshot_wait)

    def setup(self):
        if self.clientID != -1:
            errorCode, handles, intData, floatData, array = vrep.simxGetObjectGroupData(self.clientID,
                                                                                        vrep.sim_appobj_object_type,
                                                                                        0,
                                                                                        vrep.simx_opmode_oneshot_wait)
            data = dict(zip(array, handles))

            self.camera = [value for key, value in data.iteritems() if "Vision" in key][0]
            self.left_wheel = [value for key, value in data.iteritems() if "DynamicLeftJoint" in key][0]
            self.right_wheel = [value for key, value in data.iteritems() if "DynamicRightJoint" in key][0]
            vrep.simxGetVisionSensorImage(self.clientID,self.camera,1,vrep.simx_opmode_streaming)