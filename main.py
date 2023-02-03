import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageFilter

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(700, 400)

bt_dir = QPushButton('Папка')
bt_left = QPushButton('Лево')
bt_right = QPushButton('Право')
bt_screen = QPushButton('Зеркало')
bt_sharpness = QPushButton('Резкость')
bt_BW = QPushButton('Ч/Б')

image_label = QLabel('Картинка')

dir_image_list = QListWidget()

lay_1 = QHBoxLayout()

lay_2 = QVBoxLayout()
lay_2.addWidget(bt_dir)
lay_2.addWidget(dir_image_list)

lay_3 = QVBoxLayout()
lay_3.addWidget(image_label, 95)

lay_4 = QHBoxLayout()
lay_4.addWidget(bt_left)
lay_4.addWidget(bt_right)
lay_4.addWidget(bt_screen)
lay_4.addWidget(bt_sharpness)
lay_4.addWidget(bt_BW)

lay_3.addLayout(lay_4)

lay_1.addLayout(lay_2, 20)
lay_1.addLayout(lay_3, 80)

win.setLayout(lay_1)

workdir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    dir_image_list.clear()
    for filename in filenames:
        dir_image_list.addItem(filename)


bt_dir.clicked.connect(showFilenamesList)


class ImageProcessor():

    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        image_label.hide()
        pixmapimage = QPixmap(path)
        w, h = image_label.width(), image_label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmapimage)
        image_label.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_screen(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


def showChosenImage():
    if dir_image_list.currentRow() >= 0:
        filename = dir_image_list.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


workimage = ImageProcessor()
dir_image_list.currentRowChanged.connect(showChosenImage)

bt_left.clicked.connect(workimage.do_left)
bt_right.clicked.connect(workimage.do_right)
bt_screen.clicked.connect(workimage.do_screen)
bt_sharpness.clicked.connect(workimage.do_sharpness)
bt_BW.clicked.connect(workimage.do_bw)


def showChosenImage():
    if dir_image_list.currentRow() >= 0:
        filename = dir_image_list.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


dir_image_list.currentRowChanged.connect(showChosenImage)

win.show()
app.exec()