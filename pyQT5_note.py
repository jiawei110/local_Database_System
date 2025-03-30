#REFERENCES
#https://hackmd.io/@kaneyxx/HJdX8DXCr
#https://blog.csdn.net/qq_39019547/article/details/109718288
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QMessageBox, QLineEdit

def buttonClick():
    print("BUtton Clicked")

"""
app = QApplication(sys.argv)        #app變數將用sys來控制我們的程式離開

qwidget = QWidget()# 建構我們的視窗
qwidget.setWindowTitle("First GUI window") # 設定視窗標題

button = QPushButton("First Button", qwidget)       #("按鍵名稱", 放置的widget)
#setToolTip是鼠標移動到按鍵上顯示的提示(不用按)
button.setToolTip("This will display message when I take mouse on button")

button.move(100,100)    #視窗左上=(0, 0)  向右為+x, 向下為+y
button.clicked.connect(buttonClick)

qwidget.show() #讓視窗顯現出來

sys.exit(app.exec_()) #sys.exit()當我們關閉程式時可以幫助我們離開
"""

"""
from PyQt5.QtWidgets import QMessageBox
app = QApplication(sys.argv)

qwidget = QWidget()
qwidget.setWindowTitle("First_DialogBox")

#(放置的widget, 標題, 問題/敘述, 選項, 預設值)
button_reply_from_user = QMessageBox.question(qwidget,"PyQt5 Diaglog", "Do you like this program?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
# 辨識使用者的選擇
if button_reply_from_user == QMessageBox.Yes:
    print("Thanks!")
else:
    print("Don't worry, we will be better!")

#如果不想顯示視窗可以註解掉<或是放到if/else中按鍵後產生
qwidget.show()

sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QLineEdit
app = QApplication(sys.argv)

#建構一個函式給click用來抓取inputbox的內容
def getTextValue():
    print("You type: " + inputbox.text())
    #獲取後要移除內容
    inputbox.setText("")

# 建構主視窗
mainwindow = QMainWindow()
mainwindow.resize(300, 100)
mainwindow.setWindowTitle("Python Window with Input Text")

# 建構文本框
inputbox = QLineEdit(mainwindow)
# 重新調整大小, 並移動位置
inputbox.resize(200, 20) #(寬, 高)
inputbox.move(10, 20)

# 建構按鈕並移動位置
button = QPushButton("Click This", mainwindow)
button.move(60, 60)
button.clicked.connect(getTextValue)

mainwindow.show()

sys.exit(app.exec_())

"""

"""
from PyQt5.QtWidgets import QAction
# 建構給下面目錄選項用的函式
def EditClick():
    print("Edit clicked!")

def OpenClick():
    print("Open clicked")

app = QApplication(sys.argv)

mainwindow = QMainWindow()
mainwindow.resize(300, 200)

# 建構目錄條
mainMenu = mainwindow.menuBar()
# 在目錄條上加入主選項
fileMenu = mainMenu.addMenu("File")
#加入子選項
openMenu = fileMenu.addMenu("Open")
# 加入"可點擊"的項目
openAction = QAction("Open File")
openAction.triggered.connect(OpenClick)
openMenu.addAction(openAction)

editMenu = mainMenu.addMenu("Edit")
# 為選項連結功能(方式類似按鍵), 記得連結後還要addAction
editAction = QAction("Edit")
editAction.triggered.connect(EditClick)
editMenu.addAction(editAction)

mainwindow.show()
sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidget ,QTableWidgetItem ,QVBoxLayout
# 此函式為點擊表格中物件會列印品項及位置
def getSelectedItemData():
    for currentItem in tableWidget.selectedItems():
        print("Row: " + str(currentItem.row()) + " Column: " + str(currentItem.column()) + " Item:" + currentItem.text())

app = QApplication(sys.argv)

qwidget = QWidget()
qwidget.setWindowTitle("First Table")
qwidget.resize(300, 200)

# 建構垂直布局
layout = QVBoxLayout()

# 建構表格
tableWidget = QTableWidget()
tableWidget.setRowCount(4)  # 設定row數 (從0算起)
tableWidget.setColumnCount(3)  # 設定column數 (從0算起)
# 設定欄目
tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Age"))
tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Job"))
# 表格內放入物件 (row, column, 物件)
tableWidget.setItem(0, 0, QTableWidgetItem("Peter"))
tableWidget.setItem(0, 1, QTableWidgetItem("18"))
tableWidget.setItem(0, 2, QTableWidgetItem("student"))

tableWidget.setItem(1, 0, QTableWidgetItem("Allen"))
tableWidget.setItem(1, 1, QTableWidgetItem("34"))
tableWidget.setItem(1, 2, QTableWidgetItem("worker"))

tableWidget.setItem(2, 0, QTableWidgetItem("John"))
tableWidget.setItem(2, 1, QTableWidgetItem("23"))
tableWidget.setItem(2, 2, QTableWidgetItem("thief"))

tableWidget.setItem(3, 0, QTableWidgetItem("Hilton"))
tableWidget.setItem(3, 1, QTableWidgetItem("27"))
tableWidget.setItem(3, 2, QTableWidgetItem("lawyer"))

# 將函式作連結
tableWidget.doubleClicked.connect(getSelectedItemData)
# 把表格layout出來
layout.addWidget(tableWidget)
qwidget.setLayout(layout)

qwidget.show()
sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget

app = QApplication(sys.argv)
mainwindow = QMainWindow()
mainwindow.setWindowTitle("Tab Test")
mainwindow.resize(300, 500)

qwidget = QWidget()
layout = QVBoxLayout()

# 創建tabs
tabs = QTabWidget()
tabs.resize(200,300)
# 創建tab items
tab1 = QWidget()
tab2 = QWidget()
# 把tab items加到tab上
tabs.addTab(tab1, "Tab 1")
tabs.addTab(tab2, "Tab 2")

tablayout1 = QVBoxLayout()
editBox1 = QLineEdit()
button1 = QPushButton("Tab 1 Item")
tablayout1.addWidget(editBox1)
tablayout1.addWidget(button1)
tab1.setLayout(tablayout1)

tablayout2 = QVBoxLayout()
editBox2 = QLineEdit()
button2 = QPushButton("Tab 2 Item")
tablayout2.addWidget(editBox2)
tablayout2.addWidget(button2)
tab2.setLayout(tablayout2)

# Add tab to main layout(first one)
layout.addWidget(tabs)
# set this layout to QWidget
qwidget.setLayout(layout)

# set QWidget to main window
mainwindow.setCentralWidget(qwidget)

mainwindow.show()
sys.exit(app.exec_())

"""

"""
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication

app = QApplication(sys.argv)

mainWindow = QMainWindow()
mainWindow.setWindowTitle("H/V Layout")
qwidget = QWidget()

'''
講一下要做的目標, 3個文本框 + 3個按鈕, 文本框在上 按鍵在下
所以最終會是文本框和按鍵各自的水平布局, 
而文本框及按鍵這倆群體則呈現垂直布局
'''
# 建構三個文本框
input_1 = QLineEdit()
input_2 = QLineEdit()
input_3 = QLineEdit()

# 建構三個按鈕
button1 = QPushButton("Button 1")
button2 = QPushButton("Button 2")
button3 = QPushButton("Button 3")

# 分別將文本框及按鍵放入水平布局
horizontal_layout_1 = QHBoxLayout()
horizontal_layout_1.addWidget(input_1)
horizontal_layout_1.addWidget(input_2)
horizontal_layout_1.addWidget(input_3)

horizontal_layout_2 = QHBoxLayout()
horizontal_layout_2.addWidget(button1)
horizontal_layout_2.addWidget(button2)
horizontal_layout_2.addWidget(button3)

# 建構倆群體要放的垂直布局, 並放上去
vertical_layout = QVBoxLayout(qwidget) #不要qwidget也可以因為最終下方還是得setLayout
vertical_layout.addLayout(horizontal_layout_1)
vertical_layout.addLayout(horizontal_layout_2)

qwidget.setLayout(vertical_layout) #qwidget設定上主layout
mainWindow.setCentralWidget(qwidget) #主視窗放上qwidget
mainWindow.show()

sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QGridLayout, QWidget, QVBoxLayout, QHBoxLayout

app = QApplication(sys.argv)

qwidget = QWidget()
mainWindow = QMainWindow()
mainWindow.setWindowTitle("Calculator")

# 建構方形布局, 並以座標形式加上物件
grid_layout = QGridLayout()
# grid_layout.addWidget(QLineEdit(), 0, 0)
grid_layout.addWidget(QPushButton("1"), 1, 0)
grid_layout.addWidget(QPushButton("2"), 1, 1)
grid_layout.addWidget(QPushButton("3"), 1, 2)
grid_layout.addWidget(QPushButton("4"), 2, 0)
grid_layout.addWidget(QPushButton("5"), 2, 1)
grid_layout.addWidget(QPushButton("6"), 2, 2)
grid_layout.addWidget(QPushButton("7"), 3, 0)
grid_layout.addWidget(QPushButton("8"), 3, 1)
grid_layout.addWidget(QPushButton("9"), 3, 2)
# 將佈局中物件之間的空白去除
grid_layout.setVerticalSpacing(0)
grid_layout.setHorizontalSpacing(0)

# 建構一個水平布局來放文本框, 因為如果放在方形布局內會直接限制住它的大小
horizontal_layout = QHBoxLayout()
editLine = QLineEdit()
horizontal_layout.addWidget(editLine)

# 再用垂直布局放這倆布局群體
vertical_layout = QVBoxLayout(qwidget)
vertical_layout.addLayout(horizontal_layout)
vertical_layout.addLayout(grid_layout)

qwidget.setLayout(vertical_layout)
mainWindow.setCentralWidget(qwidget)
mainWindow.show()

sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QVBoxLayout, QInputDialog

def showNumberDialog():
    # (widget, 視窗標題, 標籤名稱, 預設值, 最小值, 最大值, 步伐)
    data = QInputDialog.getInt(qwidget, "Number Dialog", "Number", 1, 1, 10, 1)
    # 回傳一個tuple(數值, True/False), 當點擊ok會是True, cancel則是False
    if data[1]:
        print("Pressed OK: Value is "+ str(data[0]))
    else:
        print("Pressed Cancel: Value is " + str(data[0]))

def showTextDialog():
    # (widget, 視窗標題, 標籤名稱, QLineEdit.Normal, 預設值)
    data = QInputDialog.getText(qwidget, "Text Dialog", "Text Label", QLineEdit.Normal, "")
    if data[1]:
        print("Pressed OK: Text is "+ str(data[0]))
    else:
        print("Pressed Cancel: Text is " + str(data[0]))        #data不收值

def showChoiceDialog():
    # 用tuple建構一些選項
    items = ("Red", "Blue", "Green")
    # (widget, 視窗標題, 標籤名稱, tuple items, 預設值索引)
    data = QInputDialog.getItem(qwidget, "Choice Dialog", "Colors", items, 0)
    if data[1]:
        print("Pressed OK: Choice is " + str(data[0]))
    else:
        print("Pressed Cancel")


app = QApplication(sys.argv)

mainWindow = QMainWindow()
mainWindow.resize(400, 500)
mainWindow.setWindowTitle("All GUI Element")

qwidget = QWidget()

vertical_layout = QVBoxLayout()
# 建構input number dialog button
button_number_dialog = QPushButton("Show Number Dialog")
button_number_dialog.clicked.connect(showNumberDialog)
vertical_layout.addWidget(button_number_dialog)
# 再建構個文本的
button_text_dialog = QPushButton("Show Text Dialog")
button_text_dialog.clicked.connect(showTextDialog)
vertical_layout.addWidget(button_text_dialog)
# 再建構個選單的
button_choice_dialog = QPushButton("Show Choice Dialog")
button_choice_dialog.clicked.connect(showChoiceDialog)
vertical_layout.addWidget(button_choice_dialog)

qwidget.setLayout(vertical_layout)

mainWindow.setCentralWidget(qwidget)
mainWindow.show()

sys.exit(app.exec_())
"""

"""
from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox, QVBoxLayout
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp

def showItem(text):
    print("Your choice is " + text)
# 建構只接受數字輸入的文本框number input box

app = QApplication(sys.argv)

mainWindow = QMainWindow()
mainWindow.resize(400, 500)
mainWindow.setWindowTitle("All GUI Element")

qwidget = QWidget()

vertical_layout = QVBoxLayout()

numberLabel = QLabel("Number Input")
# setGeometry跟resize一樣能調整尺寸, 但後面還能放座標
numberLabel.setGeometry(200, 20, 10, 10) 
inputNumber = QLineEdit()
int_validator = QIntValidator()
inputNumber.setValidator(int_validator)
vertical_layout.addWidget(numberLabel)
vertical_layout.addWidget(inputNumber)

# 建構只接受文字(a-z)輸入的文本框 character input box
stringLabel = QLabel("ABC Input")
stringLabel.setGeometry(200, 20, 10, 10)
vertical_layout.addWidget(stringLabel)
letterInput = QLineEdit()
reg = QRegExp("[A-Za-z_]+") # + 表示可以打多個字
str_validator = QRegExpValidator(reg) # setup what you accept
letterInput.setValidator(str_validator)
vertical_layout.addWidget(letterInput)

# 建構下拉式選單
dropDown = QComboBox()
drop_down_items = ["Red", "Green", "Blue", "Yellow"]
dropDown.addItems(drop_down_items) # 也能用additem一個一個加
dropDown.activated[str].connect(showItem) #顯示選擇, []內放變數為int或str
vertical_layout.addWidget(dropDown)

qwidget.setLayout(vertical_layout)

mainWindow.setCentralWidget(qwidget)
mainWindow.show()
sys.exit(app.exec_())
#"""

#"""
from PyQt5.QtWidgets import QRadioButton, QHBoxLayout, QGroupBox, QCheckBox, QVBoxLayout,QLabel
from PyQt5.QtGui import QPixmap
def radioCheck(radiobutton):
    if radiobutton.isChecked():
        print("Checked: " + str(radiobutton.color))
    else:
        print("Unchecked: " + str(radiobutton.color))

def radioCheck2(radiobutton):
    if radiobutton.isChecked():
        print("Checked: " + str(radiobutton.country))
    else:
        print("Unchecked: " + str(radiobutton.country))

def getCheckValue(checkbox):
    if checkbox.isChecked():
        print("Checked: " + str(checkbox.text()))
    else:
        print("Unchecked: " + str(checkbox.text()))

app = QApplication(sys.argv)

mainWindow = QMainWindow()
mainWindow.resize(400, 500)
mainWindow.setWindowTitle("All GUI Element")

qwidget = QWidget()

vertical_layout = QVBoxLayout()
# 建構選項按鈕(radiobutton),要注意的地方是raidobutton選項是一個一個的群組, 
# 不同群組的選擇不會互相影響, 為了達到這個目的我們用groupbox
radiobutton1 = QRadioButton("Red")
radiobutton1.color = "Red" # 加入按鈕內的"資料"
radiobutton1.toggled.connect(lambda: radioCheck(radiobutton1))
radiobutton2 = QRadioButton("Blue")
radiobutton2.color = "Blue"
radiobutton2.toggled.connect(lambda: radioCheck(radiobutton2))
radiobutton3 = QRadioButton("Green")
radiobutton3.color = "Green"
radiobutton3.toggled.connect(lambda: radioCheck(radiobutton3))
# 做成水平布局並放上去
horizontal_layout1 = QHBoxLayout()
horizontal_layout1.addWidget(radiobutton1)
horizontal_layout1.addWidget(radiobutton2)
horizontal_layout1.addWidget(radiobutton3)
# 建構一個groupbox來放radiobutton
groupbox_radio1 = QGroupBox()
groupbox_radio1.setLayout(horizontal_layout1) # 放上去
vertical_layout.addWidget(groupbox_radio1) #再放到主要的垂直佈局上

# 建構第二個radio button group
radiobutton4 = QRadioButton("Taiwan")
radiobutton4.country = "Taiwan" # 加入按鈕內的"資料"
radiobutton4.toggled.connect(lambda: radioCheck2(radiobutton4))
radiobutton5 = QRadioButton("Japan")
radiobutton5.country = "Japan"
radiobutton5.toggled.connect(lambda: radioCheck2(radiobutton5))
radiobutton6 = QRadioButton("America")
radiobutton6.country = "America"
radiobutton6.toggled.connect(lambda: radioCheck2(radiobutton6))
# 做成水平布局並放上去
horizontal_layout2 = QHBoxLayout()
horizontal_layout2.addWidget(radiobutton4)
horizontal_layout2.addWidget(radiobutton5)
horizontal_layout2.addWidget(radiobutton6)
# 建構一個groupbox來放radiobutton
groupbox_radio2 = QGroupBox()
groupbox_radio2.setLayout(horizontal_layout2) # 放上去
vertical_layout.addWidget(groupbox_radio2)

# 建構核取方塊(check box)
checkbox1 = QCheckBox("Python")
checkbox1.stateChanged.connect(lambda: getCheckValue(checkbox1))
checkbox2 = QCheckBox("JAVA")
checkbox2.stateChanged.connect(lambda: getCheckValue(checkbox2))
checkbox3 = QCheckBox("PHP")
checkbox3.stateChanged.connect(lambda: getCheckValue(checkbox3))
horizontal_layout3 = QHBoxLayout()
horizontal_layout3.addWidget(checkbox1)
horizontal_layout3.addWidget(checkbox2)
horizontal_layout3.addWidget(checkbox3)
vertical_layout.addLayout(horizontal_layout3)

# 建構個放圖片的物件
image_label = QLabel()
img_px = QPixmap("pythonicon.png")
image_label.setPixmap(img_px)
vertical_layout.addWidget(image_label)


qwidget.setLayout(vertical_layout)

mainWindow.setCentralWidget(qwidget)
mainWindow.show()
sys.exit(app.exec_())
#"""