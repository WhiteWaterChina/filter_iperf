#!/usr/bin/env python
# -*- coding:cp936 -*-
# Author:yanshuo@inspur.com
import wx
import matplotlib.pyplot as plyt
import os
import time
import re
import numpy

filename_iperf = ''


class FilterIPerf(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Iperf测试结果过滤工具", pos=wx.DefaultPosition,
                          size=wx.Size(343, 334), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"选择网络速率", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        self.m_staticText1.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText1.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        combox_speedChoices = [u"100", u"1000", u"10000", u"25000", u"40000", u"100000"]
        self.combox_speed = wx.ComboBox(self, wx.ID_ANY, u"1000", wx.DefaultPosition, wx.DefaultSize,
                                        combox_speedChoices, wx.CB_READONLY)
        self.combox_speed.SetSelection(1)
        bSizer9.Add(self.combox_speed, 0, wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Mb", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        bSizer9.Add(self.m_staticText6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer2.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"选择及格线百分比", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        self.m_staticText3.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText3.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer4.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer81 = wx.BoxSizer(wx.HORIZONTAL)

        combox_ratioChoices = [u"60", u"70", u"80", u"90", u"100"]
        self.combox_ratio = wx.ComboBox(self, wx.ID_ANY, u"90", wx.DefaultPosition, wx.DefaultSize, combox_ratioChoices,
                                        0)
        self.combox_ratio.SetSelection(3)
        bSizer81.Add(self.combox_ratio, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText51 = wx.StaticText(self, wx.ID_ANY, u"%", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText51.Wrap(-1)
        self.m_staticText51.SetForegroundColour(wx.Colour(0, 0, 0))

        bSizer81.Add(self.m_staticText51, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer4.Add(bSizer81, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"选择是多线程还是单线程测试结果", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        self.m_staticText5.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText5.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer7.Add(self.m_staticText5, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        combox_threadChoices = [u"单线程", u"多线程"]
        self.combox_thread = wx.ComboBox(self, wx.ID_ANY, u"多线程", wx.DefaultPosition, wx.DefaultSize,
                                         combox_threadChoices, wx.CB_READONLY)
        self.combox_thread.SetSelection(1)
        bSizer10.Add(self.combox_thread, 0, wx.ALL, 5)

        bSizer7.Add(bSizer10, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer7, 0, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"选择Iperf结果文件", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        self.m_staticText4.SetForegroundColour(wx.Colour(255, 0, 0))
        self.m_staticText4.SetBackgroundColour(wx.Colour(255, 255, 0))

        bSizer5.Add(self.m_staticText4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.textctrl_path = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.textctrl_path, 1, wx.ALL, 5)

        self.button_chose_file = wx.Button(self, wx.ID_ANY, u"选择文件", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.button_chose_file, 0, wx.ALL, 5)

        bSizer5.Add(bSizer6, 0, wx.EXPAND, 5)

        bSizer1.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.button_show_all = wx.Button(self, wx.ID_ANY, u"GO", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.button_show_all, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.button_close = wx.Button(self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.button_close, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer8, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_chose_file.Bind(wx.EVT_BUTTON, self.chose_file)
        self.button_show_all.Bind(wx.EVT_BUTTON, self.show_all)
        self.button_close.Bind(wx.EVT_BUTTON, self.windows_close)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def windows_close(self, event):
        self.Close()

    def chose_file(self, event):
        global filename_iperf
        filename_iperf_dialog = wx.FileDialog(self, message="选择Iperf结果文件".decode('gbk'), defaultDir=os.getcwd(), defaultFile="")
        if filename_iperf_dialog.ShowModal() == wx.ID_OK:
            filename_iperf = filename_iperf_dialog.GetPath()
            self.textctrl_path.SetValue(filename_iperf)
            filename_original_shouli = filename_iperf
            filename_iperf_dialog.Destroy()

    def calculte(self, list_data, ratio, speed):
        data_lowest = min(list_data)
        index_lowest = list_data.index(data_lowest)
        data_time = []
        length = len(list_data)
        jigexian = int(ratio) * float(speed) / 100
        for item in range(1, length + 1):
            data_time.append(item)
        data_x = numpy.array(data_time)
        data_y = numpy.array(list_data)
        data_list_jige = []
        for count in range(len(list_data)):
            data_list_jige.append(jigexian)
        filename_to_write = 'Iperf_Filter_Result-%s'.decode('gbk') % time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        figure_to_show = plyt.figure(filename_to_write)
        figure_sub = figure_to_show.add_subplot(111)
        plyt.title(filename_to_write)
        plyt.xlabel("Time(S)")
        plyt.ylabel("Speed(Mbits)")
        plyt.plot(data_x, data_y, color='red')
        plyt.plot(data_x, numpy.array(data_list_jige), color='blue')

        middle_location_data = int(length / 2)
        end_location = int(length / 3 * 2)

        figure_sub.annotate('Lowest(x,y) = (%s,%s)' % (index_lowest, data_lowest), xy=(index_lowest, data_lowest), xytext=(index_lowest, data_lowest))
        figure_sub.annotate('Pass_Line = %s' % jigexian, xy=(middle_location_data, jigexian), xytext=(end_location, jigexian))
        filename_to_write_all = filename_to_write + '_image.png'
        figure_to_show.savefig(filename_to_write_all)
        diag_finish = wx.MessageDialog(None, '处理结果已经保存到文件《%s》中.如果无需其他动作，请点击退出按钮退出程序'.decode('gbk') % (filename_to_write_all), '提示'.decode('gbk'), wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        diag_finish.ShowModal()

    def show_all(self, event):
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.button_show_all.Disable()
        handler_iperf = open(filename_iperf, mode='r')
        all_line_iperf = handler_iperf.readlines()
        list_data_iperf = []
        mode_thread = self.combox_thread.GetValue()
        speed = self.combox_speed.GetValue()
        ratio = self.combox_ratio.GetValue()
        for line in all_line_iperf:
            if mode_thread == '多线程'.decode('gbk'):
                if re.search(r'SUM', line):
                    data_speed = re.search(r'(\d*.\d*)\s*([a-zA-Z])[a-zA-Z]*/sec', line)
                    if data_speed is not None:
                        number_speed = data_speed.groups()[0]
                        unit_speed = data_speed.groups()[1]
                        if unit_speed == 'G':
                            number_speed_write = float(number_speed) * 1000
                            list_data_iperf.append(number_speed_write)
                        elif unit_speed == 'M':
                            list_data_iperf.append(float(number_speed))
            if mode_thread == '单线程'.decode('gbk'):
                data_speed = re.search(r'(\d*.\d*)\s*([a-zA-Z])[a-zA-Z]*/sec', line)
                if data_speed is not None:
                    number_speed = data_speed.groups()[0]
                    unit_speed = data_speed.groups()[1]
                    if unit_speed == 'G':
                        number_speed_write = float(number_speed) * 1000
                        list_data_iperf.append(number_speed_write)
                    elif unit_speed == 'M':
                        list_data_iperf.append(float(number_speed))
        self.calculte(list_data_iperf, ratio, speed)
        self.button_show_all.Enable()
        handler_iperf.close()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == '__main__':
    app = wx.App()
    frame = FilterIPerf(None)
    frame.Show()
    app.MainLoop()
