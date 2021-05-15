# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/popup.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(573, 335)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.piano_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.piano_button.sizePolicy().hasHeightForWidth())
        self.piano_button.setSizePolicy(sizePolicy)
        self.piano_button.setText("")
        icon = QtGui.QIcon()
        prePath = os.path.dirname(__file__).replace('\\', '/') + '/'
        prePath = prePath.replace('/src/ui', '') + 'assets/'
        icon.addPixmap(QtGui.QPixmap(prePath + "piano.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.piano_button.setIcon(icon)
        self.piano_button.setIconSize(QtCore.QSize(60, 60))
        self.piano_button.setCheckable(True)
        self.piano_button.setObjectName("piano_button")
        self.gridLayout.addWidget(self.piano_button, 0, 0, 1, 1)
        self.drums_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drums_button.sizePolicy().hasHeightForWidth())
        self.drums_button.setSizePolicy(sizePolicy)
        self.drums_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(prePath + "drums.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.drums_button.setIcon(icon1)
        self.drums_button.setIconSize(QtCore.QSize(60, 60))
        self.drums_button.setCheckable(True)
        self.drums_button.setObjectName("drums_button")
        self.gridLayout.addWidget(self.drums_button, 0, 1, 1, 1)
        self.flute_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flute_button.sizePolicy().hasHeightForWidth())
        self.flute_button.setSizePolicy(sizePolicy)
        self.flute_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(prePath + "flute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flute_button.setIcon(icon2)
        self.flute_button.setIconSize(QtCore.QSize(60, 60))
        self.flute_button.setCheckable(True)
        self.flute_button.setObjectName("flute_button")
        self.gridLayout.addWidget(self.flute_button, 0, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.violin_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.violin_button.sizePolicy().hasHeightForWidth())
        self.violin_button.setSizePolicy(sizePolicy)
        self.violin_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(prePath + "violin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.violin_button.setIcon(icon3)
        self.violin_button.setIconSize(QtCore.QSize(60, 60))
        self.violin_button.setCheckable(True)
        self.violin_button.setObjectName("violin_button")
        self.gridLayout.addWidget(self.violin_button, 1, 0, 1, 1)
        self.trumpet_button = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trumpet_button.sizePolicy().hasHeightForWidth())
        self.trumpet_button.setSizePolicy(sizePolicy)
        self.trumpet_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(prePath + "trumpet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.trumpet_button.setIcon(icon4)
        self.trumpet_button.setIconSize(QtCore.QSize(60, 60))
        self.trumpet_button.setCheckable(True)
        self.trumpet_button.setObjectName("trumpet_button")
        self.gridLayout.addWidget(self.trumpet_button, 1, 1, 1, 1)
        self.guitar_button = QtWidgets.QPushButton(Dialog)
        self.guitar_button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(prePath + "guitar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.guitar_button.setIcon(icon5)
        self.guitar_button.setIconSize(QtCore.QSize(60, 60))
        self.guitar_button.setCheckable(True)
        self.guitar_button.setObjectName("guitar_button")
        self.gridLayout.addWidget(self.guitar_button, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
