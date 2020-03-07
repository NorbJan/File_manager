
from PyQt5 import QtCore, QtGui, QtWidgets

class View(QtWidgets.QMainWindow):

    # Defining custom signals
    signal_copy = QtCore.pyqtSignal()
    signal_open = QtCore.pyqtSignal()
    signal_make = QtCore.pyqtSignal()
    signal_delete = QtCore.pyqtSignal()

    signal_changePath = QtCore.pyqtSignal(QtWidgets.QLineEdit, QtWidgets.QTreeView)
    signal_writeToPath = QtCore.pyqtSignal(QtWidgets.QTreeView, QtWidgets.QLineEdit)

    # Creating UI
    def __init__(self):
        super(View, self).__init__()  # Making self a MainWindow
        self.setObjectName("MainWindow")
        self.resize(1250, 750)
        self.setMinimumSize(QtCore.QSize(1200, 650))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grpBox_buttons = QtWidgets.QGroupBox(self.centralwidget)
        self.grpBox_buttons.setEnabled(True)
        self.grpBox_buttons.setAutoFillBackground(False)
        self.grpBox_buttons.setObjectName("grpBox_buttons")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.grpBox_buttons)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pB_4 = QtWidgets.QPushButton(self.grpBox_buttons)
        self.pB_4.setObjectName("pB_4")
        self.gridLayout_3.addWidget(self.pB_4, 0, 4, 1, 1)
        self.pB_3 = QtWidgets.QPushButton(self.grpBox_buttons)
        self.pB_3.setObjectName("pB_3")
        self.gridLayout_3.addWidget(self.pB_3, 0, 2, 1, 1)
        self.pB_1 = QtWidgets.QPushButton(self.grpBox_buttons)
        self.pB_1.setObjectName("pB_1")
        self.gridLayout_3.addWidget(self.pB_1, 0, 0, 1, 1)
        self.pB_2 = QtWidgets.QPushButton(self.grpBox_buttons)
        self.pB_2.setObjectName("pB_2")
        self.gridLayout_3.addWidget(self.pB_2, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.grpBox_buttons)
        self.lay_patheditions = QtWidgets.QHBoxLayout()
        self.lay_patheditions.setObjectName("lay_patheditions")
        self.lE_treePathL = QtWidgets.QLineEdit(self.centralwidget)
        self.lE_treePathL.setObjectName("lE_treePathL")
        self.lay_patheditions.addWidget(self.lE_treePathL)
        self.rbL = QtWidgets.QRadioButton(self.centralwidget)
        self.rbL.setText("")
        self.rbL.setChecked(True)
        self.rbL.setObjectName("rbL")
        self.lay_patheditions.addWidget(self.rbL)
        self.rbR = QtWidgets.QRadioButton(self.centralwidget)
        self.rbR.setEnabled(True)
        self.rbR.setText("")
        self.rbR.setChecked(False)
        self.rbR.setObjectName("rbR")
        self.lay_patheditions.addWidget(self.rbR)
        self.lE_treePathR = QtWidgets.QLineEdit(self.centralwidget)
        self.lE_treePathR.setObjectName("lE_treePathR")
        self.lay_patheditions.addWidget(self.lE_treePathR)
        self.verticalLayout.addLayout(self.lay_patheditions)
        self.lay_trees = QtWidgets.QHBoxLayout()
        self.lay_trees.setContentsMargins(12, 0, 12, -1)
        self.lay_trees.setSpacing(20)
        self.lay_trees.setObjectName("lay_trees")
        self.tV_treeL = QtWidgets.QTreeView(self.centralwidget)
        self.tV_treeL.setObjectName("tV_treeL")
        self.lay_trees.addWidget(self.tV_treeL)
        self.tV_treeR = QtWidgets.QTreeView(self.centralwidget)
        self.tV_treeR.setObjectName("tV_treeR")
        self.lay_trees.addWidget(self.tV_treeR)
        self.verticalLayout.addLayout(self.lay_trees)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self._retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Preparing model
        self.file_model = QtWidgets.QFileSystemModel()
        self._file_model_setup()
        self._prepare_columns(370,90,100)

        #Adding auto completion
        autoC = QtWidgets.QCompleter()
        autoC.setModel(self.file_model)
        self.lE_treePathL.setCompleter(autoC)
        self.lE_treePathR.setCompleter(autoC)
        
        # Signal connection
        self.pB_1.clicked.connect(self.click_copy)
        self.pB_2.clicked.connect(self.click_open)
        self.pB_3.clicked.connect(self.click_make)
        self.pB_4.clicked.connect(self.click_delete)

        self.lE_treePathL.returnPressed.connect(self.lineEdit_return_pressed)
        self.lE_treePathR.returnPressed.connect(self.lineEdit_return_pressed)

        self.tV_treeL.clicked.connect(self.tree_clicked_item)
        self.tV_treeR.clicked.connect(self.tree_clicked_item)

    def _retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.grpBox_buttons.setTitle(_translate("MainWindow", "Tools"))
        self.pB_4.setText(_translate("MainWindow", "Delete"))
        self.pB_3.setText(_translate("MainWindow", "Make Directory"))
        self.pB_1.setText(_translate("MainWindow", "Copy"))
        self.pB_2.setText(_translate("MainWindow", "Edit (if file)"))

    def _file_model_setup(self):
        # MyComputer view
        self.file_model.setRootPath('')                   

        self.tV_treeL.setModel(self.file_model)
        self.tV_treeR.setModel(self.file_model)
        # Changing TreeView Display
        self.modIndx = self.file_model.index(self.file_model.rootPath())  
        self.tV_treeL.setRootIndex(self.modIndx)                
        self.tV_treeR.setRootIndex(self.modIndx)                

    def _prepare_columns(self, w0, w1, w2):
        self.tV_treeL.setColumnHidden(3, True)
        self.tV_treeL.setColumnWidth(0,w0)
        self.tV_treeL.setColumnWidth(1,w1)
        self.tV_treeL.setColumnWidth(2,w2)

        self.tV_treeR.setColumnHidden(3, True)
        self.tV_treeR.setColumnWidth(0,w0)
        self.tV_treeR.setColumnWidth(1,w1)
        self.tV_treeR.setColumnWidth(2,w2)
####################################
    # Checking which tree user wants to interact with (checks with radio buttons)
    def checkWhichTree(self):
            if self.rbL.isChecked():
                return self.lE_treePathL, self.lE_treePathR

            elif self.rbR.isChecked():
                return self.lE_treePathR, self.lE_treePathL

    def prepare_del_dialog(self):
        # Assing first element, because first element is choosen path editor
        source = self.checkWhichTree()[0]
        # Striping path and catching index of path chosen in source editor
        path = source.text().strip()
        src_i = self.file_model.index(path)

        # If path for delete is valid ( no '' or ' '... )
        if src_i.isValid():
            # Getting information for user to warn him about using correct panel
            if self.rbL.isChecked():  
                side = 'LEFT'
            else:
                side = 'RIGHT'

            if self.file_model.isDir(src_i):
                directory = QtCore.QDir(path)
                # Popup dialog to be sure to delete
                q = QtWidgets.QMessageBox.question(    
                    self.centralwidget,
                    side+' Panel '+'Delete Directory',
                    'Are you sure you want to delete \''+str(self.file_model.filePath(src_i))+'\' directory recursively ?',
                    buttons= QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )        
                if q == QtWidgets.QMessageBox.Yes:
                    return directory, True

            else:
                file = QtCore.QFile(path)
                # Popup dialog to be sure to delete
                q = QtWidgets.QMessageBox.question(    
                    self.centralwidget,
                    side+' Panel '+'Delete File',
                    'Are you sure you want to delete \''+str(self.file_model.filePath(src_i))+'\' file ?',
                    buttons= QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
                if q == QtWidgets.QMessageBox.Yes:
                    return file, False

            return None, None

        else:
            print('Path do not exist')
            return None, None
####################################
    # Functions that emits signals for presenter
    def click_copy(self):
        self.signal_copy.emit()
    
    def click_open(self):
        self.signal_make.emit()

    def click_make(self):
        self.signal_make.emit()

    def click_delete(self):
        self.signal_delete.emit()

    def lineEdit_return_pressed(self):
        sender = self.sender()
        if sender is self.lE_treePathL:
            destination = self.tV_treeL
        else:
            destination = self.tV_treeR

        self.signal_changePath.emit(sender, destination)

    def tree_clicked_item(self):
        sender = self.sender()
        if sender is self.tV_treeL:
            destination = self.lE_treePathL   
        else: 
            destination = self.lE_treePathR
                   
        self.signal_writeToPath.emit(sender, destination)    
