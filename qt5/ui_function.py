###########################################################################################
###                        CODE:       WRITTEN BY: ANJAL.P AUGUST 11 2020               ###
###                        PROJECT:    PELLIS Z1                                        ###
###                        PURPOSE:    WINDOWS/LINUX/MAC OS FLAT MODERN UI              ###
###                                    BASED ON QT DESIGNER, PySide2                    ###
###                        USE CASE:   TEMPLATE FOR SOFTWARES                           ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

###########################################################################################
#                                     DOCUMENTATION                                       #
#                                                                                         #
#                                                                                         #
#  Each line of the code described below is commented well, such as: the purpose of the   #
#  code, its function, returns e.t.c as in certain caes: the alternatives to that solul-  #
#  ution, other sources like included PDF document has also the working of the code.      #
#  CSS stylesheet of the buttons are given seperatly in the CSS.txt in the parent folder  #
###########################################################################################

###########################################################################################
#                                       CAUTION                                           #
#  SINCE MOST OF THE WORK IS DONE IN THE QT DESIGNER, YOU WAY NOT SEE THE STYLESHEET HERE #
#  FOR THAT PLEASE REFER THE CSS.txt FILE PROVIDED IN THIS SAME FILE.                     #
#  ALSO AMNY OF THE SETTINGS IS PREDEFINED IN THE QT DESIGNER ITSELF, SO HERE IN THIS FUN-#
#  CTION WHAY HAPPENS AFTER THIS I.E. WHEN THE USER CHANGES THE INPUT STATE, ONLY IS DELT #
#  HERE, SO IF YOU WANT TO MODIFY THE FILE, PLEASE OPEN THE CORRESPONDING .ui FILE IN QT  #
#  DESIGNER AND MADE THE MODIFICATION AND THENY COME BACK HERE TO ADD FUNCTIONALITY TO THE#
#  CHANGES.                                                                               #
########################################################################################### 


from main import *

from about import *

from PySide6 import QtCore, QtGui
from PySide6.QtGui import (QImage, QPixmap)
from PySide6.QtCore import (QPropertyAnimation)
from PySide6.QtWidgets import (QFrame)

import os
import cv2
import pickle
import numpy as np
from copy import deepcopy
import pandas as pd
import math
from matplotlib import pyplot as plt
from scipy import stats

import request_uvc
import dataset_down

GLOBAL_STATE = 1  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
init = False  # NECRESSERY FOR INITITTION OF THE WINDOW.


# tab_Buttons = ['bn_home', 'bn_bug', 'bn_android', 'bn_cloud'] #BUTTONS IN MAIN TAB
# android_buttons = ['bn_android_contact', 'bn_android_game', 'bn_android_clean', 'bn_android_world'] #BUTTONS IN ANDROID STACKPAGE

# THIS CLASS HOUSES ALL FUNCTION NECESSERY FOR OUR PROGRAMME TO RUN.
class UIFunction(MainWindow):

    # ----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE
    # INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def __init__(self):
        super().__init__()
        self.sizegrip = None

    def initStackTab(self):  # &&&&&
        global init
        if init == False:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.lab_tab.setText("Home")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True

    ################################################################################################

    # ------> SETING THE APPLICATION NAME IN OUR CUSTOME MADE TAB, WHERE LABEL NAMED: lab_appname()
    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)

    ################################################################################################

    # ----> MAXIMISE/RESTORE FUNCTION
    # THIS FUNCTION MAXIMISES OUR MAINWINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOEN OVER THE TOPFRMAE.
    # THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.

    # 放大缩小窗口
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/restore.png"))  # CHANGE THE MAXIMISE ICON TO RESTOR ICON
            self.ui.frame_drag.hide()  # HIDE DRAG AS NOT NECESSERY
        else:
            GLOBAL_STATE = 0
            # 取消窗口缩小
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QtGui.QIcon("icons/1x/max.png"))  # CHANGE BACK TO MAXIMISE ICON
            self.ui.frame_drag.show()

    ################################################################################################

    # ----> RETURN STATUS MAX OR RESTROE
    # NECESSERY OFR THE MAXIMISE FUNCTION TRO WORK.
    def returStatus(self):
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # ------> TOODLE MENU FUNCTION
    # THIS FUNCTION TOODLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    # ASLO IT SETS THE ABOUT>HOME AS THE FIRST PAGE.
    # IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMMING BACK TO THE
    # HOME PAGE.
    def toodleMenu(self, maxWidth, clicked):  # &&&&&&&&&&& 控制about界面离左边菜单栏的距离

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if clicked:
            currentWidth = self.ui.frame_bottom_west.width()  # Reads the current width of the frame
            minWidth = 80  # MINIMUN WITDTH OF THE BOTTOM_WEST FRAME
            if currentWidth == 80:
                extend = maxWidth
                # ----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            else:
                extend = minWidth
                # -----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            # THIS ANIMATION IS RESPONSIBLE FOR THE TOODLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(self.ui.frame_bottom_west, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    ################################################################################################

    # -----> DEFAULT ACTION FUNCTION
    def constantFunction(self):
        # -----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # ----> REMOVE NORMAL TITLE BAR
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick

        else:  # 原始标题栏，不建议
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        # -----> RESIZE USING DRAG                                       THIS CODE TO DRAG AND RESIZE IS IN PROTOTYPE.
        self.sizegrip = QSizeGrip(self.ui.frame_drag)

        # SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        # DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        # -----> MINIMIZE BUTTON FUNCTION
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: self.close())

    ################################################################################################################

    # ----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKEDWIDGET PAGES
    def buttonPressed(self, buttonName):  # &&&&&&&&&&&& 左侧菜单栏，可以附加页面

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName == 'bn_home':
            if self.ui.frame_bottom_west.width() == 80 and index != 2:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.lab_tab.setText("Home")
                self.ui.frame_home.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width() == 160 and index != 3:  ############### 这个可以附加功能 ##################
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.lab_tab.setText("About > Home")
                self.ui.frame_home.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_plant':
            if self.ui.frame_bottom_west.width() == 80 and index != 0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_plant)
                self.ui.lab_tab.setText("Plant")
                self.ui.frame_plant.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width() == 160 and index != 1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_plant)
                self.ui.lab_tab.setText("About > Plant")
                self.ui.frame_plant.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST


        elif buttonName == 'bn_bug':
            if self.ui.frame_bottom_west.width() == 80 and index != 7:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.lab_tab.setText("Bug")
                self.ui.frame_bug.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width() == 160 and index != 6:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)
                self.ui.lab_tab.setText("About > Bug")
                self.ui.frame_bug.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_android':
            if self.ui.frame_bottom_west.width() == 80 and index != 9:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_android)
                self.ui.lab_tab.setText("Android")
                self.ui.frame_android.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                UIFunction.androidStackPages(self, "page_contact")

            elif self.ui.frame_bottom_west.width() == 160 and index != 5:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_android)
                self.ui.lab_tab.setText("About > Android")
                self.ui.frame_android.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_cloud':
            if self.ui.frame_bottom_west.width() == 80 and index != 8:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.lab_tab.setText("Cloud")
                self.ui.frame_cloud.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_bottom_west.width() == 160 and index != 4:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_cloud)
                self.ui.lab_tab.setText("About > Cloud")
                self.ui.frame_cloud.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.

    ########################################################################################################################

    # ----> STACKWIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFOMR THE TASK IN THE STACKED WIDGET PAGE 
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.
    def stackPage(self):

        ######### PAGE_HOME ############# BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_HOME
        self.ui.lab_home_main_hed.setText("Profile")  # home第一个分页的主题
        self.ui.lab_home_stat_hed.setText("Statrs")  # home第二个分页的主题

        ######### PAGE_BUG ############## BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET page_bug
        self.ui.bn_bug_start.clicked.connect(
            lambda: APFunction.addNumbers(self, self.ui.comboBox_bug.currentText(), True))

        # THIS CALLS A SIMPLE FUNCTION LOOPS THROW THE NUMBER FORWARDED BY THE COMBOBOX 'comboBox_bug' AND DISPLAY IN PROGRESS BAR
        # ALONGWITH MOVING THE PROGRESS CHUNK FROM 0 TO 100%

        #########PAGE CLOUD #############
        self.ui.bn_cloud_connect.clicked.connect(lambda: APFunction.cloudConnect(self))
        # self.ui.bn_cloud_clear.clicked.connect(lambda: self.dialogexec("Warning", "Do you want to save the file", "icons/1x/errorAsset 55.png", "Cancel", "Save"))
        self.ui.bn_cloud_clear.clicked.connect(lambda: APFunction.cloudClear(self))

        #########PAGE ANDROID WIDGET AND ITS STACKANDROID WIDGET PAGES
        self.ui.bn_android_contact.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_contact"))
        self.ui.bn_android_game.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_game"))
        self.ui.bn_android_clean.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_clean"))
        self.ui.bn_android_world.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_world"))

        ######ANDROID > PAGE CONTACT >>>>>>>>>>>>>>>>>>>>
        self.ui.bn_android_contact_delete.clicked.connect(
            lambda: self.dialogexec("Warning", "The Contact Infromtion will be Deleted, Do you want to continue.",
                                    "icons/1x/errorAsset 55.png", "Cancel", "Yes"))

        self.ui.bn_android_contact_edit.clicked.connect(lambda: APFunction.editable(self))

        self.ui.bn_android_contact_save.clicked.connect(lambda: APFunction.saveContact(self))

        #######ANDROID > PAGE GAMEPAD >>>>>>>>>>>>>>>>>>>  android页面内容
        self.ui.textEdit_gamepad.setVerticalScrollBar(self.ui.vsb_gamepad)  # SETTING THE TEXT FILED AREA A SCROLL BAR
        self.ui.textEdit_gamepad.setText("Type Here Something, or paste something here")

        ######ANDROID > PAGE CLEAN >>>>>>>>>>>>>>>>>>>>>> 拖动条和勾选框
        # NOTHING HERE
        self.ui.horizontalSlider_2.valueChanged.connect(
            lambda: print("Slider: Horizondal: ", self.ui.horizontalSlider_2.value()))  # 接收水平条的数值打印到终端
        self.ui.checkBox.stateChanged.connect(
            lambda: self.errorexec("Happy to Know you liked the UI", "icons/1x/smile2Asset 1.png",
                                   "Ok"))  # WHEN THE CHECK BOX IS CHECKED IT ECECUTES THE ERROR BOX WITH MESSAGE.
        self.ui.checkBox_2.stateChanged.connect(
            lambda: self.errorexec("Even More Happy to hear this", "icons/1x/smileAsset 1.png", "Ok"))

        ##########PAGE: ABOUT HOME #############
        self.ui.text_about_home.setVerticalScrollBar(self.ui.vsb_about_home)
        self.ui.text_about_home.setText(aboutHome)

        #########PAGE PLANT #############
        ########## 最最重要的页面 plant页面########################################################## 307 ##########
        self.ui.bn_plant.setToolTip('Plant')  # 鼠标放上去显示按键的内容

        self.ui.lab_plant_function_hed.setText("Function")  # plant三个区块的主题
        self.ui.lab_plant_display_hed.setText("Display")
        self.ui.lab_plant_result_hed.setText("Result")

        self.ui.label_about_plant.setText("Empty")

        # defaultList = {'datasetName' : 'Bean'} #这个和variablesDefault内容一样,bean和Bean都可
        # defaultList = {'datasetName' : 'None'}
        tmpFileRead = open('./lib/variablesDefault', 'rb')  ###### 读取这个文件内容，在get按键旁的编辑框引入数据集 {{可改}}
        defaultList = pickle.load(tmpFileRead)
        tmpFileRead.close()  ###### 关闭文件，节省资源
        if defaultList['datasetName'] != 'None':  ###### 编辑框赋值
            self.ui.line_plant_function_datasetName.setText(defaultList['datasetName'])

        #########PAGE PLANT _function #############
        self.ui.lab_plant_function_datasetName.setText(self.ui.STR_lab_plant_function_datasetName)  # “数据集名称”

        self.ui.bn_plant_function_get.setText(self.ui.STR_bn_plant_function_get)  # “get”
        self.ui.bn_plant_function_process.setText(self.ui.STR_bn_plant_function_process)  # "process"
        self.ui.bn_plant_function_get.clicked.connect(lambda: APFunction.get_photo_list(self))  # get触发按键 {{可改}}
        self.ui.bn_plant_function_process.clicked.connect(
            lambda: APFunction.process_and_display(self))  # process按键 {{可改}}

        self.ui.radioBn_plant_download_select.setText(self.ui.STR_radioBn_plant_function_select)  ######### 下载数据集勾选框
        self.ui.radioBn_plant_download_select.clicked.connect(lambda: APFunction.ratioBn_function_download(self))

        self.ui.lab_plant_function_photoList.setText(self.ui.STR_lab_plant_function_photoList)  # “图片列表”
        self.ui.comboBox_plant_function_photoList.setItemText(0, u"例.图1.使用 Get 按钮获取")  ###### {{可改}}
        self.ui.comboBox_plant_function_photoList.setItemText(1, u"例.图2.使用 Get 按钮获取")
        self.ui.comboBox_plant_function_photoList.setItemText(2, u"例.图3.使用 Get 按钮获取")

        self.ui.lab_plant_function_jilu.setText(self.ui.STR_lab_plant_function_jilu)  # “下载过的数据集”
        self.ui.lab_plant_function_jilu1.setText(self.ui.STR_lab_plant_function_jilu1)
        self.ui.lab_plant_function_jilu2.setText(self.ui.STR_lab_plant_function_jilu2)
        self.ui.lab_plant_function_jiluable.setText(self.ui.STR_lab_plant_function_jiluable)  # "可下载的数据集"
        self.ui.lab_plant_function_jiluable1.setText(self.ui.STR_lab_plant_function_jiluable1)
        self.ui.lab_plant_function_jiluable2.setText(self.ui.STR_lab_plant_function_jiluable2)
        self.ui.bn_plant_function_pass.setText(self.ui.STR_bn_plant_function_pass)  # "刷新下一批"
        self.ui.bn_plant_function_pass.clicked.connect(lambda: APFunction.pass_for_next(self))

        self.ui.labTab_plant_display.setText('点击 Process 按钮刷新图片显示')  ####### plant分页中，下方text显示内容

        self.ui.g_img_empty = cv2.imread(u"icons/1x/empty.png")

        APFunction.update_plant_display(self)  ########## {{可改}}

        #########PAGE PLANT _display #############
        self.ui.g_img_plant_singleObject_gray = cv2.cvtColor(self.ui.g_img_empty, cv2.COLOR_BGR2GRAY)  ##### empty 背景图
        self.ui.g_img_plant_singleObject_gray = cv2.cvtColor(self.ui.g_img_plant_singleObject_gray, cv2.COLOR_GRAY2BGR)
        self.ui.g_img_plant_singleObject_black = (self.ui.g_img_empty > 255) * 255
        self.ui.g_img_plant_singleObject_black = self.ui.g_img_plant_singleObject_black.astype('uint8')

        self.ui.radioBn_plant_display_mode_color.setText(  ########## 以下三个为勾选框，勾中相应的，进行相应展示
            self.ui.STR_radioBn_plant_display_mode_color)
        self.ui.radioBn_plant_display_mode_color.clicked.connect(lambda: APFunction.ratioBn_function_color(self))

        self.ui.radioBn_plant_display_mode_singleObject_gray.setText(
            self.ui.STR_radioBn_plant_display_mode_singleObject_gray)
        self.ui.radioBn_plant_display_mode_singleObject_gray.clicked.connect(
            lambda: APFunction.ratioBn_function_gray(self))

        self.ui.radioBn_plant_display_mode_singleObject_black.setText(
            self.ui.STR_radioBn_plant_display_mode_singleObject_black)
        self.ui.radioBn_plant_display_mode_singleObject_black.clicked.connect(
            lambda: APFunction.ratioBn_function_black(self))

        #########PAGE PLANT _result #############
        self.ui.lab_plant_result_select_object.setText(self.ui.STR_lab_plant_result_select_object)  # “结果目标选定”

        self.ui.comboBox_plant_result_objectList.setItemText(0, u"例.目标1.使用 Process 按钮获取")  ##### {{可改}}
        self.ui.comboBox_plant_result_objectList.setItemText(1, u"例.目标2.使用 Process 按钮获取")
        self.ui.comboBox_plant_result_objectList.setItemText(2, u"例.目标3.使用 Process 按钮获取")

        self.ui.bn_plant_result_select_object.setText(
            self.ui.STR_bn_plant_result_select_object)  ##### select按钮 {{可改}} !存在图片刷新的bug(系参数文件问题)
        self.ui.bn_plant_result_select_object.clicked.connect(
            lambda: APFunction.select_object(self))  ######周长、面积等信息需要改（已改）

        self.ui.radioBn_plant_result_mode_select.setText(self.ui.STR_radioBn_plant_result_mode_select)  ##### 鼠标选择模式
        self.ui.radioBn_plant_result_mode_select.clicked.connect(
            lambda: APFunction.ratioBn_function_cursor(self))  # 定义了一些bool功能

        self.ui.bn_plant_result_show_pc.setText(
            self.ui.STR_bn_plant_result_show_pc)  ######### show_pc按钮，待开发，有和点云相关的功能 {{可改}}
        self.ui.bn_plant_result_show_pc.clicked.connect(lambda: APFunction.show_pc_result(self))

        self.ui.radioBn_plant_result_mode_draw_contour.setText(
            self.ui.STR_radioBn_plant_result_mode_draw_contour)  ####语义轮廓线
        self.ui.radioBn_plant_result_mode_draw_contour.clicked.connect(
            lambda: APFunction.ratioBn_function_contour(self))
        # 下为右边标签
        self.ui.lab_plant_result_img_binary.setText(self.ui.STR_lab_plant_result_img_binary)

        self.ui.lab_plant_result_img_binary_filled.setText(self.ui.STR_lab_plant_result_img_binary_filled)

        self.ui.lab_plant_result_img_color.setText(self.ui.STR_lab_plant_result_img_color)

        self.ui.lab_plant_result_info_line_length.setText(self.ui.STR_lab_plant_result_info_line_length)

        self.ui.lab_plant_result_info_line_width.setText(self.ui.STR_lab_plant_result_info_line_width)

        self.ui.lab_plant_result_info_line_perimeter.setText(self.ui.STR_lab_plant_result_info_line_perimeter)

        self.ui.lab_plant_result_info_line_area.setText(self.ui.STR_lab_plant_result_info_line_area)

    ################################################################################################################################

    # -----> FUNCTION TO SHOW CORRESPONDING STACK PAGE WHEN THE ANDROID BUTTONS ARE PRESSED: CONTACT, GAME, CLOUD, WORLD
    # SINCE THE ANDROID PAGE AHS A SUB STACKED WIDGET WIT FOUR MORE BUTTONS, ALL THIS 4 PAGES CONTENT: BUTTONS, TEXT, LABEL E.T.C ARE INITIALIED OVER HERE. 
    def androidStackPages(self, page):  ########### android 中的控件
        # ------> THIS LINE CLEARS THE BG COLOR OF PREVIOUS TABS
        for each in self.ui.frame_android_menu.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if page == "page_contact":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_contact)
            self.ui.lab_tab.setText("Android > Contact")
            self.ui.frame_android_contact.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_game":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_game)
            self.ui.lab_tab.setText("Android > GamePad")
            self.ui.frame_android_game.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_clean":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_clean)
            self.ui.lab_tab.setText("Android > Clean")
            self.ui.frame_android_clean.setStyleSheet("background:rgb(91,90,90)")

        elif page == "page_world":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_world)
            self.ui.lab_tab.setText("Android > World")
            self.ui.frame_android_world.setStyleSheet("background:rgb(91,90,90)")

        # ADD A ADDITIONAL ELIF STATEMNT WITH THE SIMILAR CODE UP ABOVE FOR YOUR NEW SUBMENU BUTTON IN THE ANDROID STACK PAGE.
    ##############################################################################################################


# ------> CLASS WHERE ALL THE ACTION OF TH SOFTWARE IS PERFORMED:
# THIS CLASS IS WHERE THE APPLICATION OF THE UI OR THE BRAINOF THE SOFTWARE GOES
# UNTILL NOW WE SEPCIFIED THE BUTTON CLICKS, SLIDERS, E.T.C WIDGET, WHOSE APPLICATION IS EXPLORED HERE. THOSE FUNCTION WHEN DONE IS 
# REDIRECTED TO THIS AREA FOR THE PROCESSING AND THEN THE RESULT ARE EXPOTED.
# REMEMBER THE SOFTWARE UI HAS A FUNCTION WHOSE CODE SHOULD BE HERE


class APFunction():
    def update_plant_display(self):
        if self.ui.g_img_plant_source is None:  # 图片为空时
            APFunction.setImg_plant_display(self, self.ui.g_img_empty)
            return

        if self.ui.g_int_plant_display_mode == 0:  #### 三种模式下，展示三种图片
            APFunction.setImg_plant_display(self, self.ui.g_img_plant_display_color)
        if self.ui.g_int_plant_display_mode == 1:
            APFunction.setImg_plant_display(self, self.ui.g_img_plant_singleObject_gray)
        if self.ui.g_int_plant_display_mode == 2:
            APFunction.setImg_plant_display(self, self.ui.g_img_plant_singleObject_black)

        if self.ui.g_img_plant_result_color is not None:  # 存在彩色图时，经过下面处理
            APFunction.setImg_plant_result_color(self, self.ui.g_img_plant_result_color)
            APFunction.setImg_plant_result_binary(self, self.ui.g_img_plant_result_binary)
            APFunction.setImg_plant_result_binary_filled(self, self.ui.g_img_plant_result_binary_filled)
            # added by scalpa
            self.ui.infoLine_plant_result_length.setText(self.ui.g_string_plant_result_length)
            self.ui.infoLine_plant_result_width.setText(self.ui.g_string_plant_result_width)
            self.ui.infoLine_plant_result_perimeter.setText(self.ui.g_string_plant_result_perimeter)
            self.ui.infoLine_plant_result_area.setText(self.ui.g_string_plant_result_area)

    def select_object(self):  ####### select 按钮
        if self.ui.g_list_plant_result_object is None:  ######### 当该变量为None时
            self.errorexec('请先点击 Process 按钮获取目标对象！', 'icons/1x/error.png', 'Ok')
            return

        objectNum = self.ui.comboBox_plant_result_objectList.currentIndex() + 1  #################### 确定获取第几条内容 ###############

        APFunction.refresh_result_images(self, objectNum)  ################### 该功能在选择好目标叶片时进行相应的操作和显示 ################
        APFunction.refresh_result_parameter(self,
                                            objectNum)  ################### 该功能在点击select按钮就可以输出参数 #####################

        # 选中目标进行结果显示后，一定配合暗淡模式，就是首先打开暗淡模式
        if self.ui.g_int_plant_display_mode != 1:
            self.ui.radioBn_plant_display_mode_color.setChecked(False)
            self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(True)
            self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(False)
            self.ui.g_int_plant_display_mode = 1

        APFunction.update_plant_display(self)

    def select_object_objectNum(self, objectNum):  ######################## 鼠标点中后进行相应的操作和参数显示 #########################
        APFunction.refresh_result_images(self, objectNum)  ################### 该功能在选择好目标叶片时进行相应的操作和显示 ################
        APFunction.refresh_result_parameter(self,
                                            objectNum)  ################### 该功能在点击select按钮就可以输出参数 #####################

        # 选中目标进行结果显示后，一定配合暗淡模式
        if self.ui.g_int_plant_display_mode != 1:
            self.ui.radioBn_plant_display_mode_color.setChecked(False)
            self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(True)
            self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(False)
            self.ui.g_int_plant_display_mode = 1

        APFunction.update_plant_display(self)

    def show_pc_result(self):  ############ 展示pcl
        if self.ui.g_int_plant_result_cropX is None:
            self.errorexec('请先选择目标！', 'icons/1x/error.png', 'Ok')
            return

        # self.ui.g_pc_plant_source = pcl.PointCloud_PointXYZRGB()
        #
        # # Fill in the cloud data
        # # self.ui.g_pc_plant_source.width = self.ui.g_int_plant_result_cropW
        # # self.ui.g_pc_plant_source.height = self.ui.g_int_plant_result_cropH
        # # self.ui.g_pc_plant_source.points.resize(self.ui.g_pc_plant_source.width * self.ui.g_pc_plant_source.height)
        # # self.ui.g_pc_plant_source.resize(np.array([self.ui.g_pc_plant_source.width, self.ui.g_pc_plant_source.height],
        # #                                           dtype=np.float))
        # points = np.zeros((self.ui.g_int_plant_result_cropW * self.ui.g_int_plant_result_cmdcropH, 4), dtype=np.float32)
        #
        # # 加载 pclMat
        # pclMat = cv2.imread(r'../dataset_workplace/{}ALL/pclMat/{}'.format(self.ui.g_str_plant_datasetName,
        #                                                                    self.ui.g_str_plant_imageName),
        #                     cv2.IMREAD_UNCHANGED)
        #
        # objectNum = self.ui.comboBox_plant_result_objectList.currentIndex() + 1
        # # mask_objectNum 是通过匹配目标编号得到的掩码图
        # mask_objectNum = self.ui.g_list_img_plant_mask[objectNum - 1]
        #
        # for i in range(len(points)):
        #     # 从点数编号到点坐标索引
        #     pointX = (i % self.ui.g_int_plant_result_cropW) + self.ui.g_int_plant_result_cropX
        #     pointY = int(i / self.ui.g_int_plant_result_cropW) + self.ui.g_int_plant_result_cropY
        #
        #     if mask_objectNum[pointY, pointX] > 0:
        #         # set Point Plane
        #         points[i][0] = (pclMat[pointY, pointX][0] - 32768) / 1000.0
        #         points[i][1] = (pclMat[pointY, pointX][1] - 32768) / 1000.0
        #         points[i][2] = (pclMat[pointY, pointX][2] - 32768) / 1000.0
        #         points[i][3] = self.ui.g_img_plant_source[pointY, pointX][2] << 16 | \
        #                        self.ui.g_img_plant_source[pointY, pointX][1] << 8 | \
        #                        self.ui.g_img_plant_source[pointY, pointX][0]
        #     else:
        #         # set Point Plane
        #         points[i][0] = 0.0
        #         points[i][1] = 0.0
        #         points[i][2] = 0.0
        #         points[i][3] = 0 << 16 | 0 << 8 | 0
        #
        # self.ui.g_pc_plant_source.from_array(points)
        #
        # pcl.save(self.ui.g_pc_plant_source, r'..\lib\test.pcd')
        #
        # pointList = []
        # for i in range(len(points)):
        #     # 从点数编号到点坐标索引
        #     pointX = (i % self.ui.g_int_plant_result_cropW) + self.ui.g_int_plant_result_cropX
        #     pointY = int(i / self.ui.g_int_plant_result_cropW) + self.ui.g_int_plant_result_cropY
        #
        #     if mask_objectNum[pointY, pointX] > 0:
        #         pointList.append([(pclMat[pointY, pointX][0] - 32768) / 1000.0,
        #                           (pclMat[pointY, pointX][1] - 32768) / 1000.0,
        #                           (pclMat[pointY, pointX][2] - 32768) / 1000.0,
        #                           self.ui.g_img_plant_source[pointY, pointX][2],
        #                           self.ui.g_img_plant_source[pointY, pointX][1],
        #                           self.ui.g_img_plant_source[pointY, pointX][0]])
        #     else:
        #         pointList.append([0, 0, 0, 0, 0, 0])
        #
        # pointPD = pd.DataFrame(pointList, columns=['x', 'y', 'z', 'r', 'g', 'b'])
        # pointPD.to_csv(r'..\lib\test.csv')

    # added by scalpa
    def refresh_result_parameter(self, objectNum):  ########### 展示更新参数 来显示，非常注意这里 ########################
        if objectNum > len(self.ui.g_list_plant_result_object):
            self.errorexec('目标选择有误！', 'icons/1x/error.png', 'Ok')
            return

        self.ui.g_list_plant_result_all = []

        txt_plant_result_path = "data/test" + str(objectNum) + ".txt"
        f = open(txt_plant_result_path)
        while True:
            line = f.readline()  # 包括换行符
            if not line:
                break
            # line = line[:-1]
            line.strip()
            self.ui.g_list_plant_result_all.append(line)
        f.close()
        ####  四个参数值  ##########
        self.ui.g_string_plant_result_length = self.ui.g_list_plant_result_all[0]
        self.ui.g_string_plant_result_width = self.ui.g_list_plant_result_all[1]
        self.ui.g_string_plant_result_perimeter = self.ui.g_list_plant_result_all[2]
        self.ui.g_string_plant_result_area = self.ui.g_list_plant_result_all[3]

    # end

    def refresh_result_images(self, objectNum):  ####### 选择第几条内容后对其进行相应处理
        if objectNum > len(self.ui.g_list_plant_result_object):  #### 条数超过识别的数目
            self.errorexec('目标选择有误！', 'icons/1x/error.png', 'Ok')
            return
        # 刷新一 g_img_plant_result_binary 二值图刷新

        # mask_objectNum 是通过匹配目标编号得到的掩码图
        mask_objectNum = self.ui.g_list_img_plant_mask[objectNum - 1]

        # 图像"与"操作
        # mask_objectNum 的来源图 g_list_img_plant_mask 来自彩色图的语义分析结果
        # g_img_plant_depthImg_binary 来自深度图的有效值的二值化
        # img_plant_result_binary_source 是语义分析结果中目标对象下的有效深度值的二值化
        img_plant_result_binary_source = (mask_objectNum & self.ui.g_img_plant_depthImg_binary)
        img_plant_result_binary_source_BGR = cv2.cvtColor(img_plant_result_binary_source, cv2.COLOR_GRAY2BGR)

        # 裁剪之前绘制语义轮廓线
        if self.ui.g_bool_plant_result_mode_draw_contour:
            cv2.drawContours(img_plant_result_binary_source_BGR, self.ui.g_list_contour_plant_mask[objectNum - 1],
                             -1, (0, 0, 255), 2)

        # g_img_plant_result_binary 需要裁剪才更好显示
        # 得到所有非零点以便后面进行crop，findNonZero 方法必须 grayscale 图输入
        tmpX, tmpY, tmpW, tmpH = cv2.boundingRect(self.ui.g_list_contour_plant_mask[objectNum - 1])
        self.ui.g_int_plant_result_cropX = tmpX
        self.ui.g_int_plant_result_cropY = tmpY
        self.ui.g_int_plant_result_cropW = tmpW
        self.ui.g_int_plant_result_cropH = tmpH
        img_plant_result_binary_crop = img_plant_result_binary_source_BGR[
                                       self.ui.g_int_plant_result_cropY:self.ui.g_int_plant_result_cropY + self.ui.g_int_plant_result_cropH,
                                       self.ui.g_int_plant_result_cropX:self.ui.g_int_plant_result_cropX + self.ui.g_int_plant_result_cropW
                                       ]

        self.ui.g_img_plant_result_binary = APFunction.image_add_margin(img_plant_result_binary_crop, 20)

        # 刷新二 g_img_plant_result_binary_filled 二值填充图刷新
        # edited by scalpa
        # self.ui.g_img_plant_result_binary_filled = APFunction.depthImg_filling_hole_algo(self, objectNum)
        self.ui.g_img_plant_result_binary_filled = APFunction.image_add_margin(img_plant_result_binary_crop, 20)

        # 刷新三 g_img_plant_result_color 彩图刷新
        img_plant_result_color_source = cv2.bitwise_and(self.ui.g_img_plant_source, self.ui.g_img_plant_source,
                                                        mask=img_plant_result_binary_source)

        # 裁剪之前绘制语义轮廓线
        if self.ui.g_bool_plant_result_mode_draw_contour:
            cv2.drawContours(img_plant_result_color_source, self.ui.g_list_contour_plant_mask[objectNum - 1],
                             -1, (0, 0, 255), 2)

        img_plant_result_color_crop = img_plant_result_color_source[tmpY:tmpY + tmpH, tmpX:tmpX + tmpW]
        self.ui.g_img_plant_result_color = APFunction.image_add_margin(img_plant_result_color_crop, 20)

        # 刷新四 g_img_plant_display_color 原彩模式显示图刷新
        self.ui.g_img_plant_display_color = self.ui.g_img_plant_source.copy()

        # 在最后绘制语义轮廓线
        if self.ui.g_bool_plant_result_mode_draw_contour:
            cv2.drawContours(self.ui.g_img_plant_display_color, self.ui.g_list_contour_plant_mask[objectNum - 1],
                             -1, (0, 0, 255), 2)

        # 刷新五 g_img_plant_singleObject_gray 暗淡模式显示图刷新
        img_plant_source_gray = cv2.cvtColor(self.ui.g_img_plant_source, cv2.COLOR_BGR2GRAY)

        # 以下图像操作可参考 https://docs.opencv.org/3.4/d0/d86/tutorial_py_image_arithmetics.html
        img_plant_result_binary_source_inv = cv2.bitwise_not(img_plant_result_binary_source)
        img_background = cv2.bitwise_and(img_plant_source_gray, img_plant_source_gray,
                                         mask=img_plant_result_binary_source_inv)
        img_background = cv2.cvtColor(img_background, cv2.COLOR_GRAY2BGR)
        img_frontground = img_plant_result_color_source
        self.ui.g_img_plant_singleObject_gray = cv2.add(img_background, img_frontground)

        # 在最后绘制语义轮廓线
        if self.ui.g_bool_plant_result_mode_draw_contour:
            cv2.drawContours(self.ui.g_img_plant_singleObject_gray, self.ui.g_list_contour_plant_mask[objectNum - 1],
                             -1, (0, 0, 255), 2)

        # 刷新六 g_img_plant_singleObject_black 黑暗模式显示图刷新
        self.ui.g_img_plant_singleObject_black = img_plant_result_color_source.copy()

        # 在最后绘制语义轮廓线
        if self.ui.g_bool_plant_result_mode_draw_contour:
            cv2.drawContours(self.ui.g_img_plant_singleObject_black, self.ui.g_list_contour_plant_mask[objectNum - 1],
                             -1, (0, 0, 255), 2)

    def depthImg_filling_hole_algo(self, objectNum):
        mask_objectNum = self.ui.g_list_img_plant_mask[objectNum - 1]
        depth = cv2.bitwise_and(self.ui.g_img_plant_depthImg, self.ui.g_img_plant_depthImg,
                                mask=mask_objectNum)
        depthArr = np.asarray(depth, dtype='float64')
        depthArr = (depthArr - 32768) / 1000.0
        depthArrCrop = depthArr[
                       self.ui.g_int_plant_result_cropY:self.ui.g_int_plant_result_cropY + self.ui.g_int_plant_result_cropH,
                       self.ui.g_int_plant_result_cropX:self.ui.g_int_plant_result_cropX + self.ui.g_int_plant_result_cropW
                       ]
        valueZ = depthArrCrop.flatten()

        # 过滤奇异值和突出值
        valueZ = valueZ[valueZ > 0]
        valueZ = valueZ[valueZ < 5]

        split_num = math.ceil((valueZ.max() - valueZ.min()) / 0.003)

        bins = np.linspace(valueZ.min(), valueZ.max(), split_num)
        plt.xlim([valueZ.min() - 0.003, valueZ.max() + 0.003])

        hist = plt.hist(valueZ, bins=bins)
        plt.close()

        histX_left = hist[1][hist[1] < valueZ.mean()]
        histX_right = hist[1][hist[1] > valueZ.mean()]

        histY_left = hist[0][0:histX_left.size]
        histY_right = hist[0][histX_left.size:hist[1].size]

        histX_left = histX_left[::-1]
        histY_left = histY_left[::-1]

        thresh_left = 0
        thresh_right = 0

        for idx, num in enumerate(histY_left):
            thresh_left = histX_left[idx]
            if num < 10:
                thresh_left = histX_left[idx]
                break

        for idx, num in enumerate(histY_right):
            thresh_right = histX_right[idx]
            if num < 10:
                thresh_right = histX_right[idx]
                break

        for row, valueRow in enumerate(depthArrCrop):
            for col, value in enumerate(valueRow):
                if value < thresh_left or value > thresh_right:
                    depthArrCrop[row, col] = 0

        depthArrCrop_binary = (depthArrCrop > 0) * 255
        depthArrCrop_binary = depthArrCrop_binary.astype('uint8')

        depthArrCrop_binary_rgb = cv2.cvtColor(depthArrCrop_binary, cv2.COLOR_GRAY2BGR)

        if self.ui.g_bool_plant_result_mode_draw_contour:
            contour_draw = self.ui.g_list_contour_plant_mask[objectNum - 1]
            contour_draw[:, 0][:, 0] = contour_draw[:, 0][:, 0] - self.ui.g_int_plant_result_cropX
            contour_draw[:, 0][:, 1] = contour_draw[:, 0][:, 1] - self.ui.g_int_plant_result_cropY
            cv2.drawContours(depthArrCrop_binary_rgb, contour_draw,
                             -1, (0, 0, 255), 2)
            contour_draw[:, 0][:, 0] = contour_draw[:, 0][:, 0] + self.ui.g_int_plant_result_cropX
            contour_draw[:, 0][:, 1] = contour_draw[:, 0][:, 1] + self.ui.g_int_plant_result_cropY

        return APFunction.image_add_margin(depthArrCrop_binary_rgb, 20)

    def image_add_margin(img, size):
        return cv2.copyMakeBorder(img, size, size, size, size, cv2.BORDER_CONSTANT)

    def process_and_display(self):  ################# process和显示的功能 ################################################
        if self.ui.g_list_plant_image is None:
            self.errorexec('请先点击 Get 按钮获取图片列表！', 'icons/1x/error.png', 'Ok')
            return

        # 刷新图片各参数
        self.ui.g_str_plant_datasetName = self.ui.line_plant_function_datasetName.text()
        tmpFileRead = open('./lib/variablesDefault', 'rb')
        defaultList = pickle.load(tmpFileRead)
        tmpFileRead.close()
        defaultList['datasetName'] = self.ui.g_str_plant_datasetName
        tmpFilewrite = open('./lib/variablesDefault', 'wb')
        pickle.dump(defaultList, tmpFilewrite)
        tmpFilewrite.close()

        self.ui.g_str_plant_imageName = self.ui.comboBox_plant_function_photoList.currentText()  ####### 文件路径{{可改}}
        self.ui.g_str_plant_imageAddress = r'../dataset_workplace/{}ALL/{}/{}'.format(self.ui.g_str_plant_datasetName,
                                                                                      self.ui.g_str_plant_datasetName,
                                                                                      self.ui.g_str_plant_imageName)

        if not os.path.isfile(self.ui.g_str_plant_imageAddress):
            self.errorexec('文件不存在，请检查！', 'icons/1x/error.png', 'Ok')
            return
        self.ui.g_img_plant_source = cv2.imread(self.ui.g_str_plant_imageAddress, cv2.IMREAD_COLOR)  ######### 获取原图
        self.ui.g_img_plant_display_color = self.ui.g_img_plant_source

        ##################@############## 获取 mask 组合图 #######
        masksFolderPath = r'../dataset_workplace/{}ALL/{}_masks/{}'.format(self.ui.g_str_plant_datasetName,  #### {{可改}}
                                                                           self.ui.g_str_plant_datasetName,
                                                                           os.path.splitext(
                                                                               self.ui.g_str_plant_imageName)[0])
        masksPath = [f for f in os.listdir(masksFolderPath) if os.path.isfile(os.path.join(masksFolderPath, f))]

        # maskSUM 是 mask 的合并图，对于不同编号的每个 object，将其所属的所有
        # 像素值都赋值为其编号
        maskSUM = None
        self.ui.g_list_img_plant_mask = []
        self.ui.g_list_contour_plant_mask = []
        self.ui.g_list_plant_result_object = []
        for idx, maskPath in enumerate(masksPath):
            mask = cv2.imread(os.path.join(masksFolderPath, maskPath), cv2.IMREAD_GRAYSCALE)
            self.ui.g_list_img_plant_mask.append(mask)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contour = max(contours, key=len)
            self.ui.g_list_contour_plant_mask.append(contour)

            # 0 为背景值，idx+1 是编号要从 自然数1 开始
            ret, maskTH = cv2.threshold(mask, 0, idx + 1, cv2.THRESH_BINARY)
            if idx + 1 == 1:
                maskSUM = maskTH
            else:
                # 将后一个 mask 覆盖并累加到前一个 mask，所以大于当前 mask
                # 编号值的为重叠部分，赋值为当前编号值
                maskSUM = cv2.add(maskSUM, maskTH)
                mask_intersection = (maskSUM > idx + 1)
                maskSUM[mask_intersection] = idx + 1
            self.ui.g_list_plant_result_object.append(f'object_{str(idx + 1)}')

        self.ui.g_img_plant_maskSUM = maskSUM
        self.ui.g_int_plant_object_quantity = len(masksPath)

        APFunction.update_plant_display(self)

        self.dialogexec('提示',
                        f'当前图片扫描到{self.ui.g_int_plant_object_quantity}个目标，在结果窗口选择目标个体查看具体分析结果',
                        "icons/1x/hint.png", "确认", "取消")

        self.ui.comboBox_plant_result_objectList.clear()
        self.ui.comboBox_plant_result_objectList.addItems(self.ui.g_list_plant_result_object)

        depthImgPath = r'../dataset_workplace/{}ALL/depth_z/{}'.format(self.ui.g_str_plant_datasetName,
                                                                       ########读取深度图，路径 {{可改}}
                                                                       self.ui.g_str_plant_imageName)
        self.ui.g_img_plant_depthImg = cv2.imread(depthImgPath, cv2.IMREAD_UNCHANGED)
        self.ui.g_img_plant_depthImg_binary = (self.ui.g_img_plant_depthImg > 0) * 255  ######### 这图片并没有被使用#########
        self.ui.g_img_plant_depthImg_binary = self.ui.g_img_plant_depthImg_binary.astype('uint8')

    def pass_for_next(self):  ##### 刷新历史数据集记录
        try:
            v = request_uvc.request_history_init()  ### 得到列表对象,键对应的值变成了列表，需用列表的方式读取
            print(v)
            self.ui.lab_plant_function_jilu1.setText(v['value1'][0])
            self.ui.lab_plant_function_jilu2.setText(v['value2'][0])
            self.ui.lab_plant_function_jiluable1.setText(v['va1'][0])
            self.ui.lab_plant_function_jiluable2.setText(v['va2'][0])
        except:
            self.errorexec('请检查网络连接！', 'icons/1x/error.png', 'Ok')

    def get_photo_list(self):  #############  get按键 ，超重点 ########################################### 817 ##{{可改}}
        datasetName = self.ui.line_plant_function_datasetName.text()  #### 获取数据集名称，如bean
        if self.ui.g_bool_plant_function:  ############ 本地加载
            try:
                photoNames = [f for f in
                              os.listdir(r'../dataset_workplace/{}ALL/{}'.format(datasetName, datasetName))]  ### {{可改}}
            ##### 文件路径
            # photoNames = [f for f in os.listdir(r'./download_dataset/{}All/{}'.format(datasetName, datasetName))]

            except FileNotFoundError:
                self.errorexec('数据集不存在,请下载！', 'icons/1x/error.png', 'Ok')
                return
            else:
                self.ui.comboBox_plant_function_photoList.clear()  #### 清理原来的list内容
                self.ui.comboBox_plant_function_photoList.addItems(photoNames)  ##### 添加新名字
                self.ui.g_list_plant_image = photoNames  ####### 用于判断列表中是否有图片名
                self.errorexec('本地加载成功！', 'icons/1x/error.png', 'Ok')
        else:  ####### 网络下载
            try:
                request_uvc.request_init()  ####### 向服务器传输指令    (测试)
                # request_uvc.request_init(datasetName) ####### 向服务器传输指令

                dataset_down.dataset_init()  ######### 向cos下载图片   （测试）
                # dataset_down.dataset_init(datasetName)  ######### 向cos下载图片

                # 文件是否存在，以及是否为空
                file = './download_dataset/usr1_eve/masks/input1'  ##############    (测试)
                filedata = './download_text/bean'  #############    (测试)
                # filedata='./download_text/{}'.format(datasetName)

                # file = './download/usr1_eve/masks/{}'.format(datasetName)
                v = request_uvc.dataset_save(datasetName)
                if os.path.exists(file) and os.path.exists(filedata) and v['status'] == 'success':
                    ##### 数据集存在后，将数据集名称存进数据库
                    self.errorexec('数据集下载成功！', 'icons/1x/error.png', 'Ok')
                else:
                    self.errorexec('数据集不存在，请检查下载的文件路径！', 'icons/1x/error.png', 'Ok')

            except:
                self.errorexec('请检查网络连接、数据集路径！', 'icons/1x/error.png', 'Ok')
                return

    ##############################
    def setImg_plant_display(self, img):  ######### 展示框界面
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        (img, ratio, imgWidth, imgHeight) = APFunction.limited_resize(img, 960, 640)
        imgDisplay = QImage(img, img.shape[1], img.shape[0],
                            img.strides[0], QImage.Format_RGB888)
        self.ui.labImg_plant_display.setPixmap(QPixmap.fromImage(imgDisplay))

        self.ui.g_int_plant_display_zoom_ratio = ratio
        self.ui.g_int_plant_display_img_width = imgWidth
        self.ui.g_int_plant_display_img_height = imgHeight

    def setImg_plant_result_color(self, img):  ####### 小展示框界面，下面两个相同
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        (img, ratio, imgWidth, imgHeight) = APFunction.limited_resize(img, 192, 128)
        imgDisplay = QImage(img, img.shape[1], img.shape[0],
                            img.strides[0], QImage.Format_RGB888)
        self.ui.labImg_plant_result_img_color.setPixmap(QPixmap.fromImage(imgDisplay))

    def setImg_plant_result_binary(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        (img, ratio, imgWidth, imgHeight) = APFunction.limited_resize(img, 192, 128)
        imgDisplay = QImage(img, img.shape[1], img.shape[0],
                            img.strides[0], QImage.Format_RGB888)
        self.ui.labImg_plant_result_img_binary.setPixmap(QPixmap.fromImage(imgDisplay))

    def setImg_plant_result_binary_filled(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        (img, ratio, imgWidth, imgHeight) = APFunction.limited_resize(img, 192, 128)
        imgDisplay = QImage(img, img.shape[1], img.shape[0],
                            img.strides[0], QImage.Format_RGB888)
        self.ui.labImg_plant_result_img_binary_filled.setPixmap(QPixmap.fromImage(imgDisplay))

    def limited_resize(img, width, height, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = img.shape[:2]

        ratioWidth = float(w) / width
        ratioHeight = float(h) / height

        if ratioWidth <= 1 and ratioHeight <= 1:
            return (img, 1, w, h)

        if ratioWidth >= ratioHeight:
            dim = (width, int(h / ratioWidth))
            # resize the image
            resized = cv2.resize(img, dim, interpolation=inter)
            # return the resized image
            return (resized, ratioWidth, width, int(h / ratioWidth))
        else:
            dim = (int(w / ratioHeight), height)
            # resize the image
            resized = cv2.resize(img, dim, interpolation=inter)
            # return the resized image
            return (resized, ratioHeight, int(w / ratioHeight), height)

    #######################################
    def ratioBn_function_download(self):  ########## 下载数据集勾选功能
        if self.ui.g_bool_plant_function == True:
            self.ui.g_bool_plant_function = False
            self.ui.radioBn_plant_download_select.setChecked(True)
        else:
            self.ui.g_bool_plant_function = True
            self.ui.radioBn_plant_download_select.setChecked(False)

    def ratioBn_function_color(self):
        self.ui.radioBn_plant_display_mode_color.setChecked(True)  ###### 模式0，第一个勾选框勾选
        self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(False)
        self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(False)
        self.ui.g_int_plant_display_mode = 0

        APFunction.update_plant_display(self)

    def ratioBn_function_gray(self):
        if self.ui.g_list_plant_result_object is None:
            self.errorexec('暗淡模式只能在选定结果目标后使用！', 'icons/1x/error.png', 'Ok')
            self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(False)
            return
        self.ui.radioBn_plant_display_mode_color.setChecked(False)
        self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(True)
        self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(False)
        self.ui.g_int_plant_display_mode = 1

        APFunction.update_plant_display(self)

    def ratioBn_function_black(self):
        if self.ui.g_list_plant_result_object is None:
            self.errorexec('黑暗模式只能在选定结果目标后使用！', 'icons/1x/error.png', 'Ok')
            self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(False)
            return
        self.ui.radioBn_plant_display_mode_color.setChecked(False)
        self.ui.radioBn_plant_display_mode_singleObject_gray.setChecked(False)
        self.ui.radioBn_plant_display_mode_singleObject_black.setChecked(True)
        self.ui.g_int_plant_display_mode = 2

        APFunction.update_plant_display(self)

    def ratioBn_function_cursor(self):  ######### 鼠标选择的
        if self.ui.g_bool_plant_result_mode_cursor == True:
            self.ui.radioBn_plant_result_mode_select.setChecked(False)
            self.ui.g_bool_plant_result_mode_cursor = False
            self.ui.comboBox_plant_result_objectList.setEnabled(True)
            self.ui.bn_plant_result_select_object.setEnabled(True)
        else:
            self.ui.radioBn_plant_result_mode_select.setChecked(True)
            self.ui.g_bool_plant_result_mode_cursor = True
            self.ui.comboBox_plant_result_objectList.setEnabled(False)
            self.ui.bn_plant_result_select_object.setEnabled(False)

    def ratioBn_function_contour(self):  ######## 轮廓线的
        if self.ui.g_bool_plant_result_mode_draw_contour:
            self.ui.g_bool_plant_result_mode_draw_contour = False
            self.ui.radioBn_plant_result_mode_draw_contour.setChecked(False)
        else:
            self.ui.g_bool_plant_result_mode_draw_contour = True
            self.ui.radioBn_plant_result_mode_draw_contour.setChecked(True)

        objectNum = self.ui.comboBox_plant_result_objectList.currentIndex() + 1
        APFunction.refresh_result_images(self, objectNum)

        APFunction.update_plant_display(self)

    # -----> ADDING NUMBER TO ILLUSTRATE THE CAPABILITY OF THE PROGRESS BAR WHEN THE 'START' BUTTON IS PRESSED
    def addNumbers(self, number, enable):
        if enable:
            lastProgress = 0
            for x in range(0, int(number), 1):
                progress = int((x / int(number)) * 100)
                if progress != lastProgress:
                    self.ui.progressBar_bug.setValue(progress)
                    lastProgress = progress
            self.ui.progressBar_bug.setValue(100)

    ###########################

    # ---> FUNCTION TO CONNECT THE CLOUD USING ADRESS AND RETURN A ERROR STATEMENT
    def cloudConnect(self):
        textID = self.ui.line_cloud_id.text()
        textADRESS = self.ui.line_cloud_adress.text()
        if textID == 'asd' and textADRESS == '1234':
            self.ui.line_cloud_adress.setText("")
            self.ui.line_cloud_id.setText("")
            self.ui.line_cloud_proxy.setText("Connection established")
            self.ui.bn_cloud_clear.setEnabled(False)  # 这句可让clear按键不可点击，也就是不可清理
        else:
            self.errorexec("Incorrect Credentials", "icons/1x/errorAsset 55.png", "Retry")

    def cloudClear(self):
        self.ui.line_cloud_proxy.setText("")
        self.ui.line_cloud_adress.setText("")
        self.ui.line_cloud_id.setText("")

    # -----> FUNCTION IN ACCOUNT OF CONTACT PAGE IN ANDROID MENU
    def editable(self):
        self.ui.line_android_name.setEnabled(True)
        self.ui.line_android_adress.setEnabled(True)
        self.ui.line_android_org.setEnabled(True)
        self.ui.line_android_email.setEnabled(True)
        self.ui.line_android_ph.setEnabled(True)

        self.ui.bn_android_contact_save.setEnabled(True)
        self.ui.bn_android_contact_edit.setEnabled(False)
        self.ui.bn_android_contact_share.setEnabled(False)
        self.ui.bn_android_contact_delete.setEnabled(False)

    # -----> FUNCTION TO SAVE THE MODOFOED TEXT FIELD
    def saveContact(self):
        self.ui.line_android_name.setEnabled(False)
        self.ui.line_android_adress.setEnabled(False)
        self.ui.line_android_org.setEnabled(False)
        self.ui.line_android_email.setEnabled(False)
        self.ui.line_android_ph.setEnabled(False)

        self.ui.bn_android_contact_save.setEnabled(False)
        self.ui.bn_android_contact_edit.setEnabled(True)
        self.ui.bn_android_contact_share.setEnabled(True)
        self.ui.bn_android_contact_delete.setEnabled(True)
# ##############################################################################################################################################################
