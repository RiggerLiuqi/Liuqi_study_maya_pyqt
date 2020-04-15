# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------#
# .@FileName:    openImport_window
# .@Author:      CousinRig67
# .@Date:        2020-04-15
# .@Contact:     842076056@qq.com
# -------------------------------------------------------------------------------#

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as cmds




def get_maya_main_window():

    maya_main_wnd = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_wnd), QtWidgets.QWidget)

class TestUIWindow(QtWidgets.QDialog):

    FILE_FILTERS = 'Maya(*.ma *mb);;Maya ASCII(*.ma);;Maya Binary(*.mb);;All Files(*.*)'
    selected_filter = 'Maya(*.ma *.mb)'

    def __init__(self, parent = get_maya_main_window()):
        super(TestUIWindow, self).__init__(parent)

        self.setWindowTitle('Open/Import/Reference')
        self.setMaximumSize(700, 90)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        '''

        :return:
        '''
        self.file_path_line_edit = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton()
        self.select_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.select_file_path_btn.setToolTip('Select File')

        self.open_radio = QtWidgets.QRadioButton('Open')
        self.open_radio.setChecked(True)
        self.import_radio = QtWidgets.QRadioButton('Import')
        self.reference_radio = QtWidgets.QRadioButton('Reference')

        self.force_check_box = QtWidgets.QCheckBox('Force')

        self.apply_btn = QtWidgets.QPushButton('Apply')
        self.close_btn = QtWidgets.QPushButton('Close')

    def create_layouts(self):
        '''

        :return:
        '''
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.file_path_line_edit)
        file_path_layout.addWidget(self.select_file_path_btn)

        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.open_radio)
        radio_btn_layout.addWidget(self.import_radio)
        radio_btn_layout.addWidget(self.reference_radio)

        apply_close_btn_layout = QtWidgets.QHBoxLayout()
        apply_close_btn_layout.addStretch()
        apply_close_btn_layout.addWidget(self.apply_btn)
        apply_close_btn_layout.addWidget(self.close_btn)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('File:', file_path_layout)
        form_layout.addRow('', radio_btn_layout)
        form_layout.addRow('', self.force_check_box)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(apply_close_btn_layout)

    #___Connect___
    def create_connections(self):
        '''

        :return:
        '''
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)

        self.open_radio.toggled.connect(self.update_force_visibility)

        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)


    #___Slots___
    def show_file_select_dialog(self):
        '''

        :return:
        '''
        file_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select File',
                                                                           '',
                                                                           self.FILE_FILTERS,
                                                                           self.selected_filter)
        if file_path:
            self.file_path_line_edit.setText(file_path)

    def update_force_visibility(self, checked):
        '''

        :return:
        '''
        self.force_check_box.setVisible(checked)

    def load_file(self):
        '''

        :return:
        '''
        file_path = self.file_path_line_edit.text()

        if not file_path:
            return

        file_info = QtCore.QFileInfo(file_path)
        if not file_info.exists():
            om.MGlobal.displayError('File does not exsit: {0}'.format(file_path))
            return

        if self.open_radio.isChecked():
            self.open_file(file_path)
        elif self.import_radio.isChecked():
            self.import_file(file_path)
        else:
            self.reference_file(file_path)

    def open_file(self, file_path):

        force = self.force_check_box.isChecked()
        if not force and cmds.file(q = True, modified = True):
            result = QtWidgets.QMessageBox.question(self, "Modified", "Current scene has unsaved changes. Continue?")
            if result == QtWidgets.QMessageBox.StandardButton.Yes:
                force = True
            else:
                return
        cmds.file(file_path, open = True, iv = True, force = force)

    def import_file(self, file_path):
        cmds.file(file_path, i = True, ignoreVersion = True)

    def reference_file(self, file_path):
        cmds.file(file_path, reference = True, iv = True)
if __name__ == '__main__':

    try:
        myTest_ui.close() # pylint:disable = E0601
        myTest_ui.deleteLater() # pylint:disable = E0601
    except:
        pass

    myTest_ui = TestUIWindow()
    myTest_ui.show()