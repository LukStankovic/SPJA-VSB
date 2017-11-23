# -*- coding: utf-8 -*-

import math
import random
import sys
from PyQt4 import QtGui, QtCore


# http://www.riverbankcomputing.co.uk/software/pyqt/download
# self.map = QtGui.QPixmap(self.img.transformed(QtGui.QTransform(self.flip, 0, 0, 0, 1, 0, 0, 0, 1)))

class Fish(object):
    def __init__(self, file_name, living_area):
        self.img = QtGui.QImage(QtCore.QString(file_name))
        self.map = QtGui.QPixmap(self.img)
        self.img_rect = QtCore.QRectF(0, 0, self.img.width(), self.img.height())
        self.flip = 0
        self.size = random.uniform(200, 300)
        self.aspect = self.img.height() / float(self.img.width())
        self.living_area = living_area

        self.x = random.uniform(self.half_width(), self.living_area.width())
        self.y = random.uniform(self.half_height(), self.living_area.height())
        self.azimuth = random.uniform(0, 2 * math.pi)
        self.velocity = random.uniform(1, 10)

    def half_width(self):
        return self.size * 0.5

    def half_height(self):
        return self.size * self.aspect * 0.5

    def move(self, dt=1):
        change = 1
        self.x += self.velocity * math.cos(self.azimuth) * dt
        self.y += self.velocity * math.sin(self.azimuth) * dt
        if self.x < self.half_width():
            print (self.x)

            self.half_width()
            self.x = self.half_width()
            change = 0

        elif self.x + self.half_width() > self.living_area.width():
            self.x = self.living_area.width() - self.half_width()
            change = 0

        if self.y < self.half_height():
            self.y = self.half_height()
            change = 0

        elif self.y + self.half_height() > self.living_area.height():
            self.y = self.living_area.height() - self.half_height()
            change = 0

        if change * random.uniform(0, 1) < 0.001:
            self.velocity = random.uniform(1, 10)
            self.azimuth = random.uniform(0, 2 * math.pi)

        flip = 1
        if ds[0] < 0:
            flip = -1
        if self.flip != flip:
            self.flip = flip
            self.map = QtGui.QPixmap(self.img.transformed(QtGui.QTransform(self.flip, 0, 0, 0, 1, 0, 0, 0, 1)))

    def draw(self, painter):
        rectangle = QtCore.QRectF(QtCore.QPointF(self.x - self.half_width(), self.y - self.half_height()),
                                  QtCore.QSizeF(self.size, self.size * self.aspect))
        painter.drawPixmap(rectangle, self.map, self.img_rect)


class Aquarium(QtGui.QWidget):
    def __init__(self):
        super(Aquarium, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Aquarium")

        self.playground = QtGui.QPixmap()
        self.playground.load(QtCore.QString("aquarium_1024.jpg"))
        self.playground_rect = QtCore.QRectF(0, 0, self.playground.width(), self.playground.height())
        self.setMinimumSize(10, 10)
        self.setMaximumSize(self.playground.width(), self.playground.height())

        self.setGeometry(20, 40, self.playground.width(), self.playground.height())

        self.fishes = []

        self.show()

        self.timer = QtCore.QTimer(self)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.moveFishes)
        self.timer.start(10)

    def addFish(self, fish):
        self.fishes.append(fish)

    def moveFishes(self):
        for fish in self.fishes:
            fish.move(0.15)
        self.update()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Aquarium', "Do you really want to devitalize all those fishes?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)

        rectangle = QtCore.QRectF(QtCore.QPoint(0, 0), QtCore.QSizeF(self.playground.width(), self.playground.height()))
        painter.drawPixmap(rectangle, self.playground, self.playground_rect)

        for fish in self.fishes:
            fish.draw(painter)

        painter.end()


def main():
    app = QtGui.QApplication(sys.argv)
    aquarium = Aquarium()
    aquarium.addFish(Fish("little_fish.png", aquarium))
    aquarium.addFish(Fish("medium_fish.png", aquarium))
    aquarium.addFish(Fish("big_fish.png", aquarium))
    aquarium.addFish(Fish("clown_fish.png", aquarium))

    a = 0
    b = 100

    x = random.uniform(a, b)
    y = random.uniform(a, b)

    velocity = random.uniform(a, 20)
    azimuth = 20

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()