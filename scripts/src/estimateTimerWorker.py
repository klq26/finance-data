import os
import subprocess
import time
from datetime import datetime, timedelta
from tools.dingtalk import dingtalk
from config.pathManager import pathManager
import pandas as pd

class estimateTimerWorker:

    def __init__(self):
        self.pm = pathManager()
        self.prepareTimePeriod()
        self.run()
        pass

    # 准备今天的时间戳
    def prepareTimePeriod(self):
        dateStr = datetime.now().strftime('%Y-%m-%d')
        morningPeriod = [(datetime.strptime(dateStr + ' 09:30:00','%Y-%m-%d %H:%M:%S') + timedelta(minutes=15 * i)) for i in range(0,9)]
        afternoonPeriod = [(datetime.strptime(dateStr + ' 13:00:00','%Y-%m-%d %H:%M:%S') + timedelta(minutes=15 * i)) for i in range(0,10)]
        self.allDateTime = morningPeriod + afternoonPeriod
        # print(self.allDateTime)
        self.allTimeStamp = [x.timestamp() for x in self.allDateTime]

        self.index = 0
        targetTimeStamp = self.allTimeStamp[self.index]
        currentTimeStamp = datetime.now().timestamp()
        while currentTimeStamp > targetTimeStamp:
            self.index += 1
            targetTimeStamp = self.allTimeStamp[self.index]

        self.tomorrowStart = datetime.strptime(dateStr + ' 09:15:00','%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        self.tomorrowTimeStamp = self.tomorrowStart.timestamp()
        self.targetTimeStamp = targetTimeStamp
        self.nextDayDelta = self.tomorrowTimeStamp - currentTimeStamp
        # DEBUG
        keys = ['下次估值时间','当前索引值','明天准备时间','到明天的等待时长']
        values = [self.allDateTime[self.index].strftime('%Y-%m-%d %H:%M:%S'), self.index, self.tomorrowStart, self.nextDayDelta]
        print(dict(zip(keys,values)))

    def analytics(self):
        args = [r"powershell","python",os.path.join(self.pm.parentDir, 'assetAllocationCombine.py'),"d"]
        print('[Executing] {0} a...'.format(os.path.join(self.pm.parentDir, 'assetAllocationCombine.py')))
        p = subprocess.Popen(args)

    def run(self):
        while True:
            currentTimeStamp = datetime.now().timestamp()
            if currentTimeStamp < self.targetTimeStamp:
                # 下次估值时刻到来之前，还需等待
                delta = self.targetTimeStamp - currentTimeStamp - 10
                if delta > 0:
                    m, s = divmod(delta, 60)
                    h, m = divmod(m, 60)
                    print('下次估值之前还需等待：' + "%02d:%02d:%02d" % (h, m, s))
                    time.sleep(delta)
                else:
                    time.sleep(0.1)
            else:
                print('进行估值...')
                self.analytics()
                self.index += 1
                self.targetTimeStamp = self.allTimeStamp[self.index]
                print(u'下次估值时间：{0}'.format(self.allDateTime[self.index]))
        pass

if __name__ == "__main__":
    worker = estimateTimerWorker()
    worker.run()
    pass

