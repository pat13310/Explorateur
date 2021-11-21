from PyQt5 import QtGui, QtWidgets, QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QSplitter, QTreeView, QMenu

import sys

from explorer.Explorer import Ui_Explorer


class XTreeView(QTreeView):
    signal_changed = pyqtSignal(int, int, name="selectionChanged")

    def selectionChanged(self, *args, **kwds):
        print('selection changed')
        self.signal_changed.connect(self.handle_selected)
        self.signal_changed.emit(args)
        super(QTreeView, self).selectionChanged(*args, **kwds)

    def handle_selected(self, i, o):
        print(i, 0)


class ExploreClockScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Explorer()
        self.ui.setupUi(self)
        # self.ui.treeView.setSelectionCallback(self.select_item())
        # suppression de la barre des titres
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.ui.treeView= TreeView(self)
        self.setup_gui()

    def setup_gui(self):
        path = QDir.rootPath()
        #self.ui.treeView=QTreeView()
        splitter = QSplitter(Qt.Horizontal)

        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.ui.treeView.setModel(self.dirModel)
        self.ui.treeView.setRootIndex(self.dirModel.index(path))
        self.ui.treeView.clicked.connect(self.on_clicked)
        #self.ui.treeView.setSelectionModel(self.dirModel)
        # self.ui.treeView.setSelectionCallback(self.select_item())
        # self.ui.treeView.setContextMenuPolicy()

        self.ui.treeView.show()
        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)
        self.ui.listView.setModel(self.fileModel)
        self.ui.listView.setRootIndex(self.dirModel.index(path))

        self.ui.treeView.hideColumn(1)
        self.ui.treeView.hideColumn(2)
        self.ui.treeView.hideColumn(3)
        self.ui.treeView.installEventFilter(self)
        #self.ui.treeView.CurrentChanged

        # self.ui.treeView.itemSelectionChanged.connect(self.loadAllMessages)

    def loadAllMessages(self, folder):
        item = self.treeWidget.currentItem()

    def eventFilter(self, obj, event):
        if obj == self.ui.treeView:

            if event.type() == QtCore.QEvent.KeyRelease: # jamais sur key down
                if event.key() == QtCore.Qt.Key_Return:
                    print("enter pressed")

                if event.key() == QtCore.Qt.Key_Up:
                    sel = self.ui.treeView.selectedIndexes()[0]
                    self.on_clicked(sel)

                if event.key() == QtCore.Qt.Key_Down:
                    sel=self.ui.treeView.selectedIndexes()[0]
                    self.on_clicked(sel)

        return super(QMainWindow, self).eventFilter(obj, event)

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.ui.listView.setRootIndex(self.fileModel.setRootPath(path))

    def context_menu(self):
        menu = QMenu()
        open = menu.addAction("Ouvrir")
        open.triggered.connect(self.menu_open)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def menu_open(self):
        pass

    def select_item(self):
        print("selected")

    def close_window(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ExploreClockScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
