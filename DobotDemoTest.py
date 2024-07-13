
import re
import sys
import threading
import numpy as np
from time import sleep
from Packup import Packup
from CameraRead import OpenCamera
from dobot_api import DobotApiDashboard, DobotApiDashMove, DobotApiFeedBack,  alarmAlarmJsonFile

class DobotDemo:
    def __init__(self, ip):
        self.ip = ip
        self.dashboardPort = 29999
        self.feedPortFour = 30004
        self.dashboard = None
        self.feedFour = None
        self.__globalLockValue = threading.Lock()
        self.__robotSyncBreak = threading.Event()

        class item:
            def __init__(self):
                self.robotErrorState = ''
                self.robotEnableStatus = 0
                self.robotMode = 0
                self.robotCurrentCommandID = 0
                # 自定义添加所需反馈数据

        self.feedData = item()  # 定义结构对象

    def start(self):
        self.dashboard = DobotApiDashboard(self.ip, self.dashboardPort)
        self.feedFour = DobotApiFeedBack(self.ip, self.feedPortFour)
        self.dashboardmove = DobotApiDashMove(self.ip, self.dashboardPort,self.feedPortFour)
        enableState = self.parseResultId(self.dashboard.EnableRobot())
        if enableState[0] != 0:
            print("使能失败: 检查29999端口是否被占用)")
            return
        print("使能成功:)")

        feed_thread = threading.Thread(
            target = self.GetFeed)  # 机器状态反馈线程
        feed_thread.daemon = True
        feed_thread.start()

        feed_thread1 = threading.Thread(
            target = self.ClearRobotError)  # 机器错误状态清错线程
        feed_thread1.daemon = True
        feed_thread1.start()
        
        x0, y0 = 219.900, -83.0440
        STC_points_camera = np.array([[[ 830,  782,   29],
        [ 832,  212,   28],
        [ 834,  494,   29],
        [1112,  210,   28],
        [1416,  788,   29],
        [1404,  494,   30],
        [1114,  776,   30],
        [1406,  210,   29],
        [1112,  490,   27]]])
        STC_points_robot = Packup(STC_points_camera, STC_points_camera, x0, y0)
        bw = np.array([[np.average(STC_points_robot[:,0]) + 70, np.average(STC_points_robot[:,1]) + 178],
                       [np.average(STC_points_robot[:,0]) - 70, np.average(STC_points_robot[:,1]) + 178]])
        bw = np.array([[bw[0][0], bw[0][1], 68.7, -180, 0, 0], [bw[1][0], bw[1][1], 68.7, -180, 0, 0]])
        
        while True:
            sleep(1)
            circles_b, circles_w, circles_sorted = OpenCamera(0)
            circles_b1 = Packup(circles_b, STC_points_camera, x0, y0)
            circles_w1 = Packup(circles_w, STC_points_camera, x0, y0)

            for i in range(len(circles_b1)):
                while True:
                    p2Id = self.GraspPoint(circles_b1[i])
                    p2Id = self.DropPoint(bw[0])
                    if p2Id[0] == 0:  # 运动指令返回值正确
                        self.dashboardmove.WaitArrive(p2Id[1])  # 传入运动指令commandID ,进入等待指令完成
                        break
            for i in range(len(circles_w1)):
                while True:
                    p2Id = self.GraspPoint(circles_w1[i])
                    p2Id = self.DropPoint(bw[1])
                    if p2Id[0] == 0:
                        self.dashboardmove.WaitArrive(p2Id[1])
                        break

    def GetFeed(self):
        while True:
            feedInfo = self.feedFour.feedBackData()
            if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
                # Refresh Properties
                self.__globalLockValue.acquire()  # 互斥量    robotErrorState robotEnableStatus加锁
                self.feedData.robotErrorState = feedInfo['error_status'][0]
                self.feedData.robotEnableStatus = feedInfo['enable_status'][0]
                self.feedData.robotMode = feedInfo['robot_mode'][0]
                self.feedData.robotCurrentCommandID = feedInfo['currentcommandid'][0]
                self.__globalLockValue.release()
            sleep(0.01)

    def GraspPoint(self, point_list):
        self.dashboard.MovJ(
            point_list[0], point_list[1], 98.7000, point_list[3], point_list[4], point_list[5], 0)
        self.dashboard.MovJ(
            point_list[0], point_list[1], 68.7000, point_list[3], point_list[4], point_list[5], 0)
        self.CtrlIO(9,1,-1)
        self.CtrlIO(10,0,-1)
        recvmovemess = self.dashboard.MovJ(
            point_list[0], point_list[1], 98.7000, point_list[3], point_list[4], point_list[5], 0)
        print("Movj", recvmovemess)
        commandArrID = self.parseResultId(recvmovemess)  # 解析Movj指令的返回值
        return commandArrID
    
    def DropPoint(self, point_list):
        recvmovemess = self.dashboard.MovJ(
            point_list[0], point_list[1], 98.7000, point_list[3], point_list[4], point_list[5], 0)
        self.CtrlIO(9,0,-1)
        self.CtrlIO(10,1,500)
        print("Movj", recvmovemess)
        commandArrID = self.parseResultId(recvmovemess)  # 解析Movj指令的返回值
        return commandArrID
    
    def CtrlIO(self, index, status, t):
        self.dashboard.DO(index, status, time = t)
        print(str(self.dashboard.GetDO(index)))
        return self.dashboard.GetDO(index)

    def WaitArrive(self, p2Id):
        while True:
            while not self.__robotSyncBreak.is_set():
                self.__globalLockValue.acquire()  # robotEnableStatus加锁
                if self.feedData.robotEnableStatus:
                    if self.feedData.robotCurrentCommandID > p2Id:
                        self.__globalLockValue.release()
                        break
                    else:
                        isFinsh = (self.feedData.robotMode == 5)
                        if self.feedData.robotCurrentCommandID == p2Id and isFinsh:
                            self.__globalLockValue.release()
                            break
                self.__globalLockValue.release()
                sleep(0.01)
            self.__robotSyncBreak.clear()
            break

    def ExitSync(self):
        self.__robotSyncBreak.set()

    def parseResultId(self, valueRecv):
        if valueRecv.find("Not Tcp") != -1:  # 通过返回值判断机器是否处于tcp模式
            print("Control Mode Is Not Tcp")
            return [1]
        recvData = re.findall(r'-?\d+', valueRecv)
        recvData = [int(num) for num in recvData]
        #  返回tcp指令返回值的所有数字数组
        if len(recvData) == 0:
            return [2]
        return recvData

    def ErrorMess(self):
        
        return self.dashboard.GetAngle(), self.dashboard.GetPose()

    def ClearRobotError(self):
        dataController, dataServo = alarmAlarmJsonFile()    # 读取控制器和伺服告警码
        while True:
            self.__globalLockValue.acquire()  # robotErrorState加锁
            if self.feedData.robotErrorState:
                geterrorID = self.parseResultId(self.dashboard.GetErrorID())
                if geterrorID[0] == 0:
                    for i in range(1, len(geterrorID)):
                        alarmState = False
                        for item in dataController:
                            if geterrorID[i] == item["id"]:
                                print("机器告警 Controller GetErrorID",
                                      i, item["zh_CN"]["description"])
                                alarmState = True
                                break
                        if alarmState:
                            continue

                        for item in dataServo:
                            if geterrorID[i] == item["id"]:
                                print("机器告警 Servo GetErrorID", i,
                                      item["zh_CN"]["description"])
                                break

                    choose = input("输入1, 将清除错误, 机器继续运行: ")
                    if int(choose) == 1:
                        clearError = self.parseResultId(
                            self.dashboard.ClearError())
                        if clearError[0] == 0:
                            self.__globalLockValue.release()
                            print("--机器清错成功--")
                            break
            else:
                robotMode = self.parseResultId(self.dashboard.RobotMode())
                if robotMode[0] == 0 and robotMode[1] == 11:
                    print("机器发生碰撞")
                    choose = input("输入1, 将清除碰撞, 机器继续运行: ")
                    self.dashboard.ClearError()
            self.__globalLockValue.release()
            sleep(5)

    def __del__(self):
        del self.dashboard
        del self.feedFour

if __name__ == '__main__':
    dobot = DobotDemo("192.168.5.1")
    dobot.start()