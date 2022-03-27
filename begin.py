import sys
from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter,\
    QComboBox, QLabel, QSpinBox, QFileDialog, QApplication
from paintboard import *
from util import *
from PIL import Image, ImageQt

class MainWidget(QWidget):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.__InitData()
        self.__InitView()
        
    def __InitData(self):
        #初始化数据
        #变量名前有两个下划线代表类的私有变量
        #获取QT中的颜色列表(字符串的List)
        self.__paintBoard = PaintBoard(self)
        self.__colorList = QColor.colorNames() 
    
    def __InitView(self):
        #初始化界面
        #设置窗体固定尺寸，宽800px,高800px
        self.setBaseSize(800,750)
        #设置窗体标题
        self.setWindowTitle("PaintBoard")
        #新建一个水平布局作为本窗体的主布局
        main_layout = QHBoxLayout(self) 
        #设置主布局内边距以及控件间距为10px
        main_layout.setSpacing(10)
        
        #新建垂直子布局用于放置按键
        sub_layout = QVBoxLayout() 
        #设置此子布局和内部控件的间距为10px
        sub_layout.setContentsMargins(10, 10, 10, 10) 

        self.__btn_Clear = QPushButton("新建")
        self.__btn_Clear.setParent(self) #设置父对象为本界面
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_Quit = QPushButton("退出")
        self.__btn_Quit.setParent(self) #设置父对象为本界面
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)

        self.__btn_Open = QPushButton("打开")
        self.__btn_Open.setParent(self)
        self.__btn_Open.clicked.connect(self.on_btn_Open_Clicked)
        sub_layout.addWidget(self.__btn_Open)

        self.__btn_Save = QPushButton("保存")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        sub_layout.addWidget(self.__btn_Save)

        splitter1 = QSplitter(self) #占位符
        sub_layout.addWidget(splitter1)

        self.__cbtn_Eraser = QPushButton("橡皮擦")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)

        self.__cbtn_Pencil = QPushButton("画笔")
        self.__cbtn_Pencil.setParent(self)
        self.__cbtn_Pencil.clicked.connect(self.on_cbtn_Pencil_clicked)
        sub_layout.addWidget(self.__cbtn_Pencil)

        self.__cbtn_Barrel = QPushButton("颜料桶")
        self.__cbtn_Barrel.setParent(self)
        self.__cbtn_Barrel.clicked.connect(self.on_cbtn_Barrel_clicked)
        sub_layout.addWidget(self.__cbtn_Barrel)      

        splitter2 = QSplitter(self) #占位符
        sub_layout.addWidget(splitter2)

        self.__cbtn_Converse = QPushButton("反转")
        self.__cbtn_Converse.setParent(self)
        self.__cbtn_Converse.clicked.connect(self.on_cbtn_Converse_clicked)
        sub_layout.addWidget(self.__cbtn_Converse)

        self.__cbtn_Blur = QPushButton("模糊")
        self.__cbtn_Blur.setParent(self)
        self.__cbtn_Blur.clicked.connect(self.on_cbtn_Blur_clicked)
        sub_layout.addWidget(self.__cbtn_Blur)

        self.__cbtn_Emboss = QPushButton("浮雕")
        self.__cbtn_Emboss.setParent(self)
        self.__cbtn_Emboss.clicked.connect(self.on_cbtn_Emboss_clicked)
        sub_layout.addWidget(self.__cbtn_Emboss)

        splitter3 = QSplitter(self) #占位符
        sub_layout.addWidget(splitter3)

        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("画笔粗细")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)

        self.__spinBox_penThickness = QSpinBox(self) #调整画笔粗细
        self.__spinBox_penThickness.setMaximum(20)
        self.__spinBox_penThickness.setMinimum(2)
        self.__spinBox_penThickness.setValue(10) #默认粗细为10
        self.__spinBox_penThickness.setSingleStep(1) #最小变化值为2
        self.__spinBox_penThickness.valueChanged.connect(self.on_PenThicknessChange)#关联spinBox值变化信号和函数on_PenThicknessChange
        sub_layout.addWidget(self.__spinBox_penThickness)

        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("画笔颜色")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)

        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor) #用各种颜色填充下拉列表
        self.__comboBox_penColor.currentIndexChanged.connect(self.on_PenColorChange) #关联下拉列表的当前索引变更信号与函数on_PenColorChange
        sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout) #将子布局加入主布局
        main_layout.addWidget(self.__paintBoard)

    # Quit app
    def Quit(self):
        self.close()

    # Open img
    def on_btn_Open_Clicked(self):
        openPath = QFileDialog.getOpenFileName(self, 'path to open', '.\\', '*.png *.jpg' )
        print(openPath)
        if openPath[0] == "":
            print("Open cancel")
            return
        self.__paintBoard.LoadLocalFile(openPath[0])

    # Save img
    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'path to saved', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])

    # click Eraser button
    def on_cbtn_Eraser_clicked(self):
        self.__paintBoard.PencilMode = False
        self.__paintBoard.EraserMode = True #进入橡皮擦模式
        self.__paintBoard.BarrelMode = False
        self.__paintBoard.setCursor(Qt.CrossCursor)
        print("Eraser Mode start!")
    
    # click Pencil button
    def on_cbtn_Pencil_clicked(self):
        self.__paintBoard.PencilMode = True #进入画笔模式
        self.__paintBoard.EraserMode = False 
        self.__paintBoard.BarrelMode = False
        self.__paintBoard.setCursor(Qt.CrossCursor)
        print("Pencil Mode start!")
    
    def on_cbtn_Barrel_clicked(self):
        self.__paintBoard.PencilMode = False
        self.__paintBoard.EraserMode = False #进入橡皮擦模式
        self.__paintBoard.BarrelMode = True
        self.__paintBoard.setCursor(Qt.CrossCursor)
        print("Barrel Mode start!")
    
    def on_cbtn_Converse_clicked(self):
        self.__paintBoard.PencilMode = False 
        self.__paintBoard.EraserMode = False 
        self.__paintBoard.BarrelMode = False
        self.__paintBoard.ImageConverse()

    def on_cbtn_Blur_clicked(self):
        self.__paintBoard.PencilMode = False 
        self.__paintBoard.EraserMode = False 
        self.__paintBoard.BarrelMode = False
        self.__paintBoard.ImageBlur()

    def on_cbtn_Emboss_clicked(self):
        self.__paintBoard.PencilMode = False 
        self.__paintBoard.EraserMode = False 
        self.__paintBoard.BarrelMode = False
        self.__paintBoard.ImageEmboss()

    # change pencil thickness
    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)
    
    # change pencil color
    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)
    
    def __fillColorList(self, comboBox):
        index_black = 0
        index = 0
        for color in self.__colorList: 
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(70,20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix),None)
            comboBox.setIconSize(QSize(70,20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)



def main():
    app = QApplication(sys.argv) # sys.argv即命令行参数
    mainWidget = MainWidget() #新建一个主界面
    mainWidget.show()	#显示主界面
    exit(app.exec_()) # app.exec_() 进入消息循环
    
if __name__ == '__main__':
    main()
