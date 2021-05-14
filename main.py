# Project modules
import src.ui.mainwindow as ou
import app_main as AC
import sys



if __name__ == '__main__':
    #print(AC.QtWidgets.QStyleFactory.keys())
    MyFilterToolApp = AC.QtWidgets.QApplication(sys.argv)
    MyFilterToolApp.setStyle(AC.QtWidgets.QStyleFactory.create("Fusion"))
    MyFilterTool = AC.AppClass()
    MyFilterTool.show()
    sys.exit(MyFilterToolApp.exec_())

