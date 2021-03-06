from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen, QColor, QSize
from PyQt5.QtCore import Qt
import PyQt5
from PIL import Image, ImageQt, ImageOps, ImageFilter
import time
class PaintBoard(QWidget):
    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)
        self.__InitData() #先初始化数据，再初始化界面
        self.__InitView()
        self.update()
        
    def __InitData(self):
        
        self.__size = QSize(800,600)
        
        #新建QPixmap作为画板，尺寸为__size
        self.__board = QPixmap(self.__size)
        self.__board.fill(Qt.white) #用白色填充画板
        
        self.__IsEmpty = True #默认为空画板 
        self.EraserMode = False #默认为禁用橡皮擦模式
        self.PencilMode = False #默认为禁用画笔模式
        self.BarrelMode = False #默认为禁用油漆桶模式

        self.__lastPos = QPoint(0,0)#上一次鼠标位置
        self.__currentPos = QPoint(0,0)#当前的鼠标位置
        
        self.__painter = QPainter()#新建绘图工具
        
        self.__thickness = 10       #默认画笔粗细为10px
        self.__penColor = QColor("black")#设置默认画笔颜色为黑色
        self.__colorList = QColor.colorNames() #获取颜色列表
     
    def __InitView(self):
        #设置界面的尺寸为__size
        self.setFixedSize(self.__size)
        
    def Clear(self):
        #清空画板
        self.__board = QPixmap(self.__size)
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True
        self.setCursor(Qt.ArrowCursor)
        self.EraserMode = False 
        self.PencilMode = False
        
    def ChangePenColor(self, color="black"):
        #改变画笔颜色
        self.__penColor = QColor(color)
        
    def ChangePenThickness(self, thickness=10):
        #改变画笔粗细
        self.__thickness = thickness
        
    def IsEmpty(self):
        #返回画板是否为空
        return self.__IsEmpty
    
    def GetContentAsQImage(self):
        #获取画板内容（返回QImage）
        image = self.__board.toImage()
        return image

    def ImageConverse(self):
        if self.__IsEmpty:
            return

        ori_img = Image.fromqimage(self.__board.toImage())
        inverted_image = ImageOps.invert(ori_img)
        temp_name = "./temp/{}.png".format(str(time.time()))
        inverted_image.save(temp_name)
        self.__board.load(temp_name)
        self.__board = self.__board.scaled(QSize(800,600), Qt.KeepAspectRatio)
        self.update()
    
    def ImageBlur(self):
        if self.__IsEmpty:
            return
        ori_img = Image.fromqimage(self.__board.toImage())
        blured_image =  ori_img.filter(ImageFilter.BLUR)
        temp_name = "./temp/{}.png".format(str(time.time()))
        blured_image.save(temp_name)
        self.__board.load(temp_name)
        self.__board = self.__board.scaled(QSize(800,600), Qt.KeepAspectRatio)
        self.update()
    
    def ImageEmboss(self):
        if self.__IsEmpty:
            return
        ori_img = Image.fromqimage(self.__board.toImage())
        blured_image =  ori_img.filter(ImageFilter.EMBOSS)
        temp_name = "./temp/{}.png".format(str(time.time()))
        blured_image.save(temp_name)
        self.__board.load(temp_name)
        self.__board = self.__board.scaled(QSize(800,600), Qt.KeepAspectRatio)
        self.update()

    def LoadLocalFile(self, filePath):
        self.__board.load(filePath)
        self.__board = self.__board.scaled(QSize(800,600), Qt.KeepAspectRatio)
        print(self.__board.size())
        self.update()
        self.__IsEmpty = False

    def paintEvent(self, QPaintEvent):
        #绘图事件
        #绘图时必须使用QPainter的实例，此处为__painter
        #绘图在begin()函数与end()函数间进行
        #begin(param)的参数要指定绘图设备，即把图画在哪里
        #drawPixmap用于绘制QPixmap类型的对象
        
        self.__painter.begin(self)
        # 0,0为绘图的左上角起点的坐标，__board即要绘制的图
        self.__painter.drawPixmap(0,0,self.__board)
        self.__painter.end()
        
    def mousePressEvent(self, mouseEvent):
        #鼠标按下时，获取鼠标的当前位置保存为上一次位置
        self.__currentPos =  mouseEvent.pos()
        self.__lastPos = self.__currentPos
        if self.BarrelMode:
            self.__board.fill(self.__penColor)
            self.update()
        
        
    def mouseMoveEvent(self, mouseEvent):
        #鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        self.__currentPos =  mouseEvent.pos()
        if self.EraserMode or self.PencilMode:
            self.__painter.begin(self.__board)
            if not self.EraserMode and self.PencilMode:
                #画笔模式
                self.__painter.setPen(QPen(self.__penColor,self.__thickness)) #设置画笔颜色，粗细
            elif self.EraserMode and not self.PencilMode: 
                #橡皮擦模式下画笔为纯白色
                self.__painter.setPen(QPen(Qt.white, self.__thickness))

            #画线    
            self.__painter.drawLine(self.__lastPos, self.__currentPos)
            self.__painter.end()
            self.__lastPos = self.__currentPos
                    
            self.update() #更新显示
        # elif self.BarrelMode:
        #     self.__board.fill(self.__penColor)
        #     self.update()
        
    def mouseReleaseEvent(self, mouseEvent):
        if self.EraserMode or self.PencilMode or self.BarrelMode:
            self.__IsEmpty = False #画板不再为空
