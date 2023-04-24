from __future__ import absolute_import
from builtins import object
import os

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from .qgsmaptooladdlinebuffer import QgsMapToolAddLineBuffer

from . import settings

class DigitizrPlugin(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self._iface = iface
        self.toolAddLineBuffer = None # добавляем инициализацию переменной

    def initGui(self):
        self.toolAddLineBuffer = QgsMapToolAddLineBuffer(self._iface.mapCanvas(), self._iface.cadDockWidget())

        self.addToolAddLineBufferButton()

        self._iface.mapCanvas().mapToolSet.connect(self.disableTools)

    def unload(self):
        self.removeToolAddLineBufferButton()
    
    def disableTools(self, new_tool):
        if self.toolAddLineBuffer is not None and new_tool != self.toolAddLineBuffer: # добавляем проверку на None
            self.actionAddLineBuffer.setChecked(False)

    def activateToolAddLineBuffer(self, status):
        self.actionAddLineBuffer.setChecked(True)
        self._iface.mapCanvas().setMapTool(self.toolAddLineBuffer)

    def addToolAddLineBufferButton(self):
        self.toolAddLineBufferButton = QToolButton()
        self.toolAddLineBufferButton.setMenu(QMenu())
        self.toolAddLineBufferButton.setPopupMode(QToolButton.MenuButtonPopup)
        self._iface.addToolBarWidget(self.toolAddLineBufferButton)

        self.actionAddLineBuffer = QAction(self.tr("Add line buffer"), self._iface.mainWindow())
        self.actionAddLineBuffer.setIcon(QIcon(os.path.join(settings.icons_dir, "line_buffer.svg")))
        self.actionAddLineBuffer.setCheckable(True)
        self.actionAddLineBuffer.setEnabled(self.toolAddLineBuffer.isAvailable()) # изменяем на isAvailable()
        self.actionAddLineBuffer.triggered.connect(self.activateToolAddLineBuffer)

        # убираем следующую строку, так как она приводит к ошибке
        # self.toolAddLineBuffer.setAction(self.actionAddLineBuffer)

        # добавляем проверку на None и изменяем на isAvailable()
        if self.toolAddLineBuffer is not None:
            self.toolAddLineBuffer.availabilityChanged.connect(self.actionAddLineBuffer.setEnabled)

        self.actionAddLineBufferSettings = QAction(self.tr("Settings"), self._iface.mainWindow())
        self.actionAddLineBufferSettings.setIcon(QIcon(os.path.join(settings.icons_dir,"settings.svg")))
        self.actionAddLineBufferSettings.triggered.connect(self.showToolAddLineBufferButtonSettings)

        m = self.toolAddLineBufferButton.menu()
        m.addAction(self.actionAddLineBuffer) # добавляем кнопку в меню
        m.addAction(self.actionAddLineBufferSettings)
        self.toolAddLineBufferButton.setDefaultAction(self.actionAddLineBuffer)

    def removeToolAddLineBufferButton(self):
        self._iface.removeToolBarWidget(self.toolAddLineBufferButton) # изменяем на removeToolBarWidget

    # добавляем функцию для проверки доступности инструмента
    def isAvailable(self):
        vlayer = self._iface.activeLayer() # изменяем на activeLayer()

        if not vlayer:
            return False

        if not vlayer.isEditable():
            return False

        if vlayer.geometryType() != QgsWkbTypes.PolygonGeometry: # изменяем на PolygonGeometry
            return False

        return True
