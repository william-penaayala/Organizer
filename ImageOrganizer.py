#!/usr/bin/env python3

# launch parameters: "nogui", "populate_hans"

import sys
from DesignerUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
from MagicUIBrewery import *
from ImageSpells import *
from SpellReference import *

def setup_ui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    return app, MainWindow, ui

def setup_backend():
    pool = MagicPool()
    saveloader = MagicSaveLoader()

    search_engine = MagicSearchEngine()

    return pool, saveloader, search_engine

def test_populate_scrollArea(ui, pool):
    test_image = pool.get(0)
    print("test_image path:" + test_image.path)
    innerWidget = ui.resultsDisplay_innerWidget
    innerWidget_layout = ui.resultsDisplay_innerWidget_layout
    for i in range(5):
        for j in range(3):
            image = MagicImageIcon(innerWidget, test_image)
            # image.setGeometry(10, 10, 400, 100)
            innerWidget_layout.addWidget(image, i, j)

if __name__ == "__main__":
    # Setting up program objects/Model + Backend
    pool, saveloader, search_engine = setup_backend()
    # Populating the pool with a sample set of MagicImages
    saveloader.load(pool, force_flag = True)

    # Launch gui if the "nogui" argument is not given
    if "nogui" not in sys.argv:
        # Setting up UI/View
        app, MainWindow, ui = setup_ui()
        # Setting up presenter
        presenter = MagicPresenter(pool, search_engine, ui)

    # Populate the scroll area with Hanses on startup
    if "populate_hans" in sys.argv:
        test_populate_scrollArea(ui, pool)

    if 'app' in vars():
        MainWindow.show()

        sys.exit(app.exec_())