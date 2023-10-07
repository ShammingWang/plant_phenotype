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
#  Each line of the code described below is commented well, such as: the purpose of the   #
#  code, its function, returns e.t.c as in certain case: the alternatives to that solul-  #
#  ution, other sources like included PDF document has also the working of the code.      #
#  CSS stylesheet of the buttons are given seperatly in the CSS.txt in the parent folder  #
###########################################################################################

###########################################################################################
#                                       CAUTION                                           #
#  SINCE MOST OF THE WORK IS DONE IN THE QT DESIGNER, YOU MAY NOT SEE THE STYLESHEET HERE #
#  FOR THAT PLEASE REFER THE Documentation.pdf                                            #
#  ALSO MANY OF THE SETTINGS IS PREDEFINED IN THE QT DESIGNER ITSELF, SO HERE IN THIS FUN-#
#  CTION WHAY HAPPENS AFTER THIS I.E. WHEN THE USER CHANGES THE INPUT STATE, ONLY IS DELT #
#  HERE, SO IF YOU WANT TO MODIFY THE FILE, PLEASE OPEN THE CORRESPONDING .ui FILE IN QT  #
#  DESIGNER AND MADE THE MODIFICATION AND THENY COME BACK HERE TO ADD FUNCTIONALITY TO THE#
#  CHANGES.                                                                               #
###########################################################################################    

import sys

# IMPORTING ALL THE NECESSARY PYSIDE2 MODULES FOR OUR APPLICATION.

from PySide6 import QtGui
from PySide6.QtCore import (Qt)
from PySide6.QtWidgets import *

from ui_main import Ui_MainWindow  # MAIN WINDOW CODE GENERATED BY THE QT DESIGNER AND pyside2-uic.

from ui_dialog import Ui_Dialog  # DIALOG BOX WINDOW GENERATED BY THE ABOVEW SAME

from ui_error import Ui_Error  # ERRORBOX WINDOW GENERATED BY THE ABOVE SAME

from ui_function import *


# DIALOGBOX CLASS WHICH MAKE THE DIALOGBOX WHEN CALLED.
# ------> DIALOG BOX CLASS : DIALOGBOX CONTAINING TWO BUTTONS, ONE MAEEAGE BAR, ONE ICON HOLDER, ONE HEADING DEFINING
class dialogUi(QDialog):
    def __init__(self, parent=None):
        super(dialogUi, self).__init__(parent)
        self.d = Ui_Dialog()
        self.d.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint)  # REMOVING WINDOWS TOP BAR AND MAKING IT FRAMELESS (AS WE HAVE AMDE A
        # CUSTOME FRAME IN THE WINDOW ITSELF)
        self.setAttribute(
            QtCore.Qt.WA_TranslucentBackground)  # MAKING THE WINDOW TRANSPARENT SO THAT TO GET A TRUE FLAT UI

        # ############################################################################################
        # -------(C1) SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED
        # FOR THE ALTERNATIVE BUTTONS IN OUR DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE -----> MINIMIZE
        # BUTTON OF DIALOGBOX
        self.d.bn_min.clicked.connect(lambda: self.showMimized())

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.d.bn_close.clicked.connect(lambda: self.close())

        # -----> THIS FUNCTION WILL CHECKT WEATHER THE BUTRTON ON THE DIALOGBOX IS CLICKED, AND IF SO DIRECTS TO THE
        # FUNCTINON : diag_return()
        self.d.bn_east.clicked.connect(lambda: self.close())
        self.d.bn_west.clicked.connect(lambda: self.close())
        ##############################################################################################

        # #################################################################################################
        # ------(C2) SINCE THERE I S NO TOP BAR TO MOVE THE DIALOGBOX OVER THE SCREEN WE HAVE TO DEFINE THE MOUSE
        # EVENT THAT IS RESPONSIBLE FOR THE MOVEMENT. THIS IS CARRIED BY THIS FUNCTION ---> MOVING THE WINDOW WHEN
        # LEFT MOUSE PRESSED AND DRAGGED OVER DIALOGBOX TOPBAR
        self.dragPos = self.pos()  # INITIAL POSOTION OF THE DIALOGBOX

        def movedialogWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.d.frame_top.mouseMoveEvent = movedialogWindow  # CALLING THE FUNCTION TO CJANGE THE POSITION OF THE
        # DIALOGBOX DURING MOUSE DRAG
        ################

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    #################################################################################################

    # ################################################################################################
    # ------(C3) THE DIALOG BOX IS DESIGNED TO BE CALLED FROM ANY WHERE IN THE UI WITH ABLE TO CHANGE THE STATRE OF
    # THE TEXT SHOWN, BUTTON NAMES E.T.C THIS IS MADE BY CALLING THIS FUNCTION WHICH TAKES: HEADING, MESSAGE, ICON,
    # BUTTON NAME 1, BUTTON NAME 2 AS ARUMENT. EMBED THE GIVEN PROPERT TO THE DIALOGBOX AND FINALLY DISPLAYS IT IN
    # THE WINDOW. -------> SETTING THE DIALOGBOX CONFIGRATION: TEXT IN BUTTON, LABEL, HEADING
    def dialogConstrict(self, heading, message, icon, btn1, btn2):
        self.d.lab_heading.setText(heading)
        self.d.lab_message.setText(message)
        self.d.bn_east.setText(btn2)
        self.d.bn_west.setText(btn1)
        pixmap = QtGui.QPixmap(icon)
        self.d.lab_icon.setPixmap(pixmap)
    ##################################################################################################


# ERRORBOX CREATES A SAMLL WINDOW TO DISPLAY THAT SOMETHING THAT THE USER PERFORMED HAS WENT WRONG. THIS CLASS ALSO
# HAS THE SAME PROPERTY AS THE DIALOGBOX CLASS WITH THE EXCEPTION THAT BOTH HAVE DIFFERENT UI INTERFACE ANS DIFFERENT
# APPLICATION. ------> ERROR BOX GIVING THE ERROR OCCURED IN THE PROCESS: TAKES THE HEADING, ICON AND BUTTON NAME
class errorUi(QDialog):
    def __init__(self, parent=None):
        super(errorUi, self).__init__(parent)
        self.e = Ui_Error()
        self.e.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # -----> CLOSE APPLICATION FUNCTION BUTTON: CORRESPONDING TO THE bn_ok OF THE ERRORBOX
        self.e.bn_ok.clicked.connect(lambda: self.close())

        # SAME AD DESCRIBED IN COMMEND (C2)
        # ---> MOVING THE WINDOW WHEN LEFT MOUSE PRESSED AND DRAGGED OVER ERRORBOX TOPBAR
        self.dragPos = self.pos()  # INITIAL POSOTION OF THE ERRORBOX

        def moveWindow(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.e.frame_top.mouseMoveEvent = moveWindow  # CALLING THE FUNCTION TO CJANGE THE POSITION OF THE ERRORBOX
        # DURING MOUSE DRAG
        ################

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    #############################################

    # SAME AS DESCRIBED IN COMMEND (C3)
    # -------> SETTING THE ERRORBOX CONFIGRATION: TEXT IN BUTTON, LABEL, HEADING
    def errorConstrict(self, heading, icon, btnOk):
        self.e.lab_heading.setText(heading)
        self.e.bn_ok.setText(btnOk)
        pixmap2 = QtGui.QPixmap(icon)
        self.e.lab_icon.setPixmap(pixmap2)


# OUR APPLICATION MAIN WINDOW :
# -----> MAIN APPLICATION CLASS
class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # title
        applicationName = "这是一个主窗体"
        self.setWindowTitle(applicationName)
        UIFunction.labelTitle(self, applicationName)

        ###############################

        # -----> INITIAL STACKED WIDGET PAGE WIDGET AND TAB THIS MAKE THE INITIAL WINDOW OF OUR APPLICATION,
        # I.E. THE FIRST PAGE OR THE WELCOME PAGE/SCREEN            ---------(C5) IN OUR APPLICATION THIS IS THE MENU
        # BAR, TOODLE SWITCH, MIN, MAX, CLOSE BUTTONS, AND THE HOME PAGE. ALL THIS GET INITIALISED HERE. SINCE ALL
        # THE FUNCTION RELATED STUFF IS DONE IN THE ui_function.py FILE, IT GOES THERE REMEMBER THIS FUNCTION CAN
        # ALSO BE DONE HERE, BUT DUE TO CONVINENCE IT IS SHIFTD TO A NEW FILE.
        UIFunction.initStackTab(self)
        ############################################################

        UIFunction.constantFunction(self)  # 加载最大最小化关闭功能
        #############################################################

        # ----> TOODLE THE MENU HERE
        # THIS CODE DETETS THE BUTTON IN THE RIGHT TOP IS PRESSED OR NOT AND IF PRESSED IT CONNECT  TO A FUNCTION IN THE ui_function.py                 ---------(C7)
        # FILE, WHICH EXPANDS THE MENU BAR TO DOUBLE ITS WIDTH MAKING ROOM FOR THE ABOUT PAGES.
        # THIS EFFECT CALLED AS TOODLE, CAN BE MADE USE IN MANY WAYS. CHECK THE FUNCTION: toodleMenu: IN THE ui_function.py
        # FILE FOR THE CLEAR WORKING
        self.ui.toodle.clicked.connect(lambda: UIFunction.toodleMenu(self, 160, True))  # 控制about页面离左边菜单栏距离，同时附加其他功能
        #############################################################

        # ----> MENU BUTTON PRESSED EVENTS NOW SINCE OUR DEMO APPLICATION HAS ONLY 4 MENU BUTTONS: Home, Bug,
        # Android, Cloud, WHEN USER PRESSES IT THE FOLLOWING CODE             ---------(C8) REDIRECTS IT TO THE
        # ui_function.py FILE buttonPressed() FUNCTION TO MAKE THE NECESSERY RESPONSES TO THE BUTTON PRESSED. IT
        # TAKES SELF AND THE BUTTON NAME AS THE RGUMENT, THIS IS ONLY TO RECOGNISE WHICH BUTTON IS PRESSED BY THE
        # buttonPressed() FUNCTION.
        self.ui.bn_home.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_home'))
        self.ui.bn_plant.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_plant'))
        self.ui.bn_bug.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_bug'))
        self.ui.bn_android.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_android'))
        self.ui.bn_cloud.clicked.connect(lambda: UIFunction.buttonPressed(self, 'bn_cloud'))
        #############################################################

        # -----> STACK PAGE FUNCTION
        # OUR APPLICATION CHANGES THE PAGES BY USING THE STACKED WIDGET, THIS CODE POINTS TO A FUNCTION IN ui_function.py FILE             ---------(C9)
        # WHICH GOES AND SETS THE DEFAULT IN THESE PAGES AND SEARCHES FOR THE RESPONSES MADE BY THE USER IN THE CORRSPONDING PAGES.
        UIFunction.stackPage(self)  ########## 各个页面基本的分页主题、按键的绑定等等，包括plant的
        #############################################################

        # ----> EXECUTING THE ERROR AND DIALOG BOX MENU : THIS HELP TO CALL THEM WITH THE FUNCTIONS.
        # THIS CODE INITIALISED THE DIALOGBOX AND THE ERRORBOX, MAKES AN OBJECT OF THE CORRESPONDING CLASS, SO THAT WE CAN CALL THEM         ---------(C10)
        # WHENEVER NECESSERY.
        self.diag = dialogUi()
        self.error = errorUi()
        #############################################################

        #############################################################

        # UNCOMMENT THE RESPECTIVE LINES OF CODE AS REQUIRED:
        # WARNING: MAKE SURE THAT YOU COMMENT OUT CODES THAT IS ENTERED IN THIS FILE AND FILE ui_function.py FOR THE SMAE
        # WIDGET PERFORMING THE SAME FUNCTION.

        # --ADDING A NEW MENU BUTTON------------------:
        # REFER THE DOCUMENTATION: Documentation.pdf FILE

        # --CALLING A DIALOG BOX----------------------:和小窗口相关
        # dialogexec("Heading", "Message", "icon", "Button1name", "button2name")

        # --CALLING A ERROR BOX-----------------------:和错误窗口相关
        # errorexec("Message", "icon", "buttonname")

        # --PAGE HOME---------------------------------:home分页的主题
        # self.ui.lab_home_main_hed.setText("heading")
        # self.ui.lab_home_stat_hed.setText("Sata heading")

        # --LABEL------------------------:home两个分页的内容设置
        # self.ui.lab_home_main_disc.setText("-----------")
        # self.ui.lab_home_stat_disc.setText("--------------")

        # --USING PROGRESS BAR VALUE-----:                   bug页面使用进度条,填入整数，表示进度条到达的程度
        # self.ui.progressBar_bug.setValue(90)

        # --PAGE CLOUD--------------------------------:
        # --CHANGE HEADING---------------:
        # self.ui.lab_cloud_main.setText("heading")

        # --CHANGING LABELS--------------:
        # self.ui.label_2.setText("change: Clint ID")
        # self.ui.label_3.setText("change: Server Adress")
        # self.ui.label_4.setText("change: Proxy")

        # --USING THE PUSH BUTTONS-------:
        # self.ui.bn_cloud_clear.clicked.connect(function to execute)
        # self.ui.bn_cloud_connect.clikced.connect(function to execute)

        # --PAGE ANDROID:CONTACT----------------------:
        # --CHANGING THE HEADING---------:
        # self.ui.lab_android_contact.setText("Heading")

        # --CHANGING LABELS--------------:
        # self.ui.label.setText("-----")
        # perform the same for the label with obeject tname: 'label_5', 'label_6', 'label_7', 'label_8'

        # --USING TEXT FIELD-------------:
        # sefl.ui.line_android_name.setText("---")
        # self.ui.lineandroid_name.text() #TO GET WHAT THE USER HAS ENTERED.
        # PERFORM THE SAME CODE FOR THE: OBJECT NAME: 'line_android_adress', 'line_android_eamil', 'line_android_ph', 'line_android_org'

        # --USING PUSH BUTTONS-----------:
        # self.ui.bn_adroid_contact_edit.clicked.connect("function goes here")
        # self.ui.bn_adroid_contact_share.clicked.connect("function goes here")
        # self.ui.bn_adroid_contact_delete.clicked.connect("function goes here")
        # self.ui.bn_adroid_contact_save.clicked.connect("function goes here")

        # self.ui.bn_android_contact_save.setEnable(True) #TO ENABLE THE BUTTON
        # DO THE SAME FOR THE REST OF THE BUTTON WHEREEVER NECESSERY.

        # --PAGE ANDROID:GAME-------------------------:
        # --CHANGING THE HEADING---------:
        # self.ui.lab_gamepad.setText("-----")

        # --USING TEXT BROWSER-----------:
        # self.ui.textEdit_gamepad.setText("----")

        # FOR REST OF THE WIDGET GOTO THE Documentation.pdf AND CHECK THE LAYOUT FOR MORE DETAILS.

        # ---> MOVING THE WINDOW WHEN LEFT MOUSE PRESSED AND DRAGGED OVER APPNAME LABEL
        # SAME TO SAY AS IN COMMENT (C2)
        self.dragPos = self.pos()
        self.showMaximized()

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunction.returStatus(self) == 1:  # 使窗口缩小并可以移动，等于0时窗口放大并可移动
                UIFunction.maximize_restore(self)

            # 窗口可移动
            # if event.buttons() == Qt.LeftButton:
            #     self.errorexec('窗口不允许移动', 'icons/1x/error.png', 'Ok')
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE: WE CHOOSE THE TOPMOST FRAME WHERE THE APPLICATION NAME IS PRESENT AS THE AREA TO MOVE THE WINDOW.
        self.ui.frame_appname.mouseMoveEvent = moveWindow  # CALLING THE FUNCTION TO CJANGE THE POSITION OF THE WINDOW DURING MOUSE DRAG

    # ----> FUNCTION TO CAPTURE THE INITIAL POSITION OF THE MOUSE: NECESSERY FOR THE moveWindow FUNCTION
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    #############################################################

    # -----> FUNCTION WHICH OPENS THE DIALOG AND DISPLAYS IT: SO TO CALL DIALOG BOX JUST CALL THE FUNCTION dialogexec() WITH ALL THE PARAMETER
    # NOW WHENEVER YOU WANT A DIALOG BOX TO APPEAR IN THE APP LIKE IN PRESS OF CLODE BUTTON, THIS CAN BE DONE BY CALLING THIS FUNCTION.        ----------(C11)
    # IT TAKES DIALOG OBJECT(INITIALISED EARLIER), HEADER NAME OF DIALOG BOX, MESSAGE TO BE DISPLAYED, ICON, BUTTON NAMES.
    # THIS CODE EXECUTES THE DIALOGBOX AND SO WE CAN SEE THE DIALOG BOX IN THE SCREEN.
    # DURING THE APPEARENCE OF THIS WINDOW, YOU CANNOT USE THE MAINWINDOW, YOU SHPULD EITHER PRESS ANY ONE OFT HE PROVIDED BUTTONS
    # OR JUST CLODE THE DIALOG BOX.
    def dialogexec(self, heading, message, icon, btn1, btn2):
        dialogUi.dialogConstrict(self.diag, heading, message, icon, btn1, btn2)
        self.diag.exec_()

    #############################################################

    # -----> FUNCTION WHICH OPENS THE ERROR BOX AND DISPLAYS IT: SO TO CALL DIALOG BOX JUST CALL THE FUNCTION errorexec() WITH ALL THE PARAMETER
    # SAME AS COMMEND (C11), EXCEPT THIS IS FOR THE ERROR BOX.
    def errorexec(self, heading, icon, btnOk):
        errorUi.errorConstrict(self.error, heading, icon, btnOk)
        self.error.exec_()

    ##############################################################

    def getPixel_plant_display(self, event):  # 点击图片展示页面产生的功能
        if self.ui.g_img_plant_source is None:
            self.errorexec('请先点击 Process 按钮刷新图片显示！', 'icons/1x/error.png', 'Ok')
            # self.dialogexec('你好','请登录','icons/1x/error.png','取消','取消')#查看登录窗口
            return
        pixelX = event.pos().x()  # 获取鼠标像素坐标
        pixelY = event.pos().y()
        ratio = self.ui.g_int_plant_display_zoom_ratio
        img = self.ui.g_img_plant_source
        imgWidth = self.ui.g_int_plant_display_img_width
        imgHeight = self.ui.g_int_plant_display_img_height
        if pixelX > imgWidth or pixelY > imgHeight:
            self.ui.labTab_plant_display.setText(f'图片当前缩小倍数为{ratio}倍，'
                                                 f'请勿点击区域外')
            return
        (valueB, valueG, valueR) = (img[pixelY, pixelX])
        self.ui.labTab_plant_display.setText(f'图片当前缩小倍数为{ratio}倍，'
                                             f'当前坐标为({pixelX}, {pixelY})，'
                                             f'R,G,B ({valueR},{valueG},{valueB})')

        if self.ui.g_list_plant_result_object is not None:
            if self.ui.g_bool_plant_result_mode_cursor:
                objectNum = self.ui.g_img_plant_maskSUM[pixelY, pixelX]
                APFunction.select_object_objectNum(self, objectNum)
                self.ui.comboBox_plant_result_objectList.setCurrentIndex(objectNum - 1)  # 设置鼠标点中后当前下拉框为第几条数据


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # app.exec_()其实就是QApplication的方法，原来这个exec_()方法的作用是“进入程序的主循环直到exit()被调用


if __name__ == "__main__":
    main()
