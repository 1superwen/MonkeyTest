# -*- coding: UTF-8 -*-
import unittest
from RunMonkeyTest.config_parser import cconfigparser
import os
import time
import HTMLTestRunner2
import codecs


class RunMonkey(unittest.TestCase):
    def setUp(self):
        self.config = cconfigparser(r'./config.ini')
        self.package_name = self.read_config()[4]
        self.monkey_cliccount = self.read_config()[2]
        self.apk_path = self.read_config()[3]
        self.execCount = self.read_config()[1]
        self.iphone_series = self.read_config()[0]

    def test_runMain(self):
        execCount =int(self.execCount)
        self.execMonkeyCounts(execCount)

    def execMonkeyCounts(self,execCount):
        for runm in range(execCount):
            self.runmonkey()


    def runmonkey(self):
        package_name = self.package_name
        apk_path = self.apk_path
        monkey_cliccount = self.monkey_cliccount

        self.uninstall_app(package_name)
        time.sleep(5)
        self.install_apk(apk_path)
        time.sleep(5)
        self.monkey_scripts(package_name, monkey_cliccount)

    '''
        #adb shell monkey -p com.aerozhonghuan.serialporttool --pct-touch 30 --ignore-crashes  --ignore-timeouts --throttle 250 -s 2  -v -v -v 5000000
        #触摸事件占30%，忽略crash和超时，每个事件间隔250ms，输出最详细日志，执行500万次
    '''
    def monkey_scripts(self,package_name,monkey_cliccount):
        cmd = 'adb shell monkey -p {} --pct-touch 30 --ignore-crashes  --ignore-timeouts --throttle 250 -s 2 -v -v {}'.format(package_name,monkey_cliccount)
        print('monkey的命令为:',cmd)
        text= self.exe_cmd(cmd)
        self.mik_monkeyLog(text)


    def read_config(self):
        config = self.config
        iphone_series = config.get('parama', 'phoneSeries')
        exec_count = config.get('parama', 'execCount')
        monkey_clickcount = config.get('parama', 'mokeyClickcount')
        apk_path = config.get('parama', 'apkpath')
        package_name = config.get('parama', 'package_name')
        return iphone_series,exec_count,monkey_clickcount,apk_path,package_name

    def install_apk(self,apk_path):
        cmd = 'adb install {}'.format(apk_path)
        print('安装的命令为:',cmd)
        text = self.exe_cmd(cmd)
        if 'Success' in text:
            print('安装成功')
        else:
            print('安装失败')

    def exe_cmd(self,cmd):
        result_file = os.popen(cmd,'r')
        try:
            #print('命令输出结果为:',result_file.read())
            text = result_file.read()
            return text
        except IOError:
            print('文件错误')
        finally:
            result_file.close()

    def uninstall_app(self,package_name):
        cmd = 'adb uninstall {}'.format(package_name)
        list_installedPackages = self.list_installedPackage()
        for line in list_installedPackages.splitlines():
            if package_name in line:
                text = self.exe_cmd(cmd)
                if 'Success' in text:
                    print('卸载安装包成功')
                else:
                    print('卸载失败')
        print('当前无此安装包')

    def list_installedPackage(self):
        cmd = 'adb shell pm list package'
        list_installedPackages = self.exe_cmd(cmd)
        return list_installedPackages

    def suite(self):
        suite = unittest.TestSuite()
        print("执行了suite函数")
        monkey_tests = [
            RunMonkey("test_runMain")]
        suite.addTests(monkey_tests)
        return suite

    def mik_monkeyLog(self,text):
        iphone_series = self.iphone_series
        today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = r'./monkey/'+ iphone_series + '/'
        logPath =path + today + ".log"
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print('已创建了新的文件夹')
        with codecs.open(logPath,'w') as file:
                file.write(text)


    def tearDown(self):
        pass

    # 编码一直有问题未解决
    def check_packagename(self, apk_path):
        # cmd = 'aapt dump badging {}'.format(apk_path)
        # print('check_packagename的执行命令为',cmd)
        # self.exe_cmd(cmd)
        pass
if __name__ == '__main__':
    unittest.main()
    print('运行主函数')
    today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    reportPath = r"./new" + ".html"
    with open(reportPath, 'wb+') as fp:
        runner = HTMLTestRunner2.HTMLTestRunner(stream=fp, title='WebTestReport',
                                                description='This  is Web  Report')
        runner.run(RunMonkey().suite())  # 运行测试用例
