# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from algorithms.simplex import Simplex, expression_util
from ui.alert import Ui_Dialog


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(363, 500)
        MainWindow.setMinimumSize(QtCore.QSize(363, 500))
        MainWindow.setMaximumSize(QtCore.QSize(363, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("icons/python.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.campoFO = QtWidgets.QLineEdit(self.centralwidget)
        self.campoFO.setGeometry(QtCore.QRect(20, 50, 201, 25))
        self.campoFO.setObjectName("campoFO")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 67, 17))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(240, 50, 91, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 191, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/solve.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.resultPanel = QtWidgets.QTextEdit(self.centralwidget)
        self.resultPanel.setGeometry(QtCore.QRect(20, 330, 321, 131))
        self.resultPanel.setReadOnly(True)
        self.resultPanel.setObjectName("resultPanel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 300, 141, 17))
        self.label_3.setObjectName("label_3")
        self.saBlock = QtWidgets.QTextEdit(self.centralwidget)
        self.saBlock.setGeometry(QtCore.QRect(20, 110, 311, 131))
        self.saBlock.setObjectName("saBlock")
        self.btnClear = QtWidgets.QPushButton(self.centralwidget)
        self.btnClear.setGeometry(QtCore.QRect(228, 260, 101, 25))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClear.setIcon(icon2)
        self.btnClear.setObjectName("btnClear")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(240, 20, 91, 17))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.execute_simplex)
        self.btnClear.clicked.connect(self.clear)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simplex"))
        self.campoFO.setToolTip(
            _translate(
                "MainWindow",
                "Utilize incógnitas diferentes para cada termo. ex: 3x + 3y ao invés de 3x1 + 3x2",  # noqa: E501
            )
        )
        self.label.setText(_translate("MainWindow", "Função Objetivo:"))
        self.label_2.setText(_translate("MainWindow", "SA:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "MAX"))
        self.comboBox.setItemText(1, _translate("MainWindow", "MIN"))
        self.pushButton.setText(_translate("MainWindow", "Resolver"))
        self.label_3.setText(_translate("MainWindow", "Resultado:"))
        self.saBlock.setToolTip(
            _translate(
                "MainWindow",
                "Utilize incógnitas diferentes para cada termo de uma restrição",  # noqa: E501
            )
        )
        self.btnClear.setText(_translate("MainWindow", "Limpar"))
        self.label_4.setText(_translate("MainWindow", "Objetivo:"))

    def clear(self):
        self.resultPanel.clear()
        self.campoFO.setText(None)
        self.saBlock.setText(None)

    def execute_simplex(self):
        try:
            objective_function = self.campoFO.text()
            obj = self.comboBox.currentIndex()
            simplex = Simplex(objective_function, obj)
            constraint_block = self.saBlock.toPlainText()
            constraints = constraint_block.split("\n")
            if constraints:
                for constraint in constraints:
                    simplex.add_constraints(constraint)

                meta = simplex.solve()
                variables = ""
                for incognita in expression_util.get_incognitas(objective_function):
                    variables += f"<br/>Valor de {incognita}: {meta[incognita]}"

                self.resultPanel.setText(
                    f"<b>Solução Ótima: <span style='color:green;'>{meta['solution']}</span></b>{variables}"  # noqa: E501
                )

        except Exception as e:
            self.show_exception(str(e))

    def show_exception(self, e: str):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog, e)
        Dialog.exec()
