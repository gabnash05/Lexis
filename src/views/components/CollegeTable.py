from operator import itemgetter

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QTableWidgetItem
from PyQt6.QtGui import QIcon

from views.components.UpdateCollegeDialog import UpdateCollegeDialog

from controllers.collegeControllers import getColleges, removeCollege, batchRemoveColleges

class CollegeTable(QtWidgets.QTableWidget):
  # Student variables
  headers = ["College Code", "College Name", "Operations"]
  sortByFields = [("college_code", "college_name"), ("college_name", "college_code")]
  searchByFields = ["college_code", "college_name"]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editCollegeSignal = pyqtSignal(list)
  deleteCollegeSignal = pyqtSignal(str)
  updateTablesSignal = pyqtSignal()

  def __init__(self, parent=None):
    super().__init__(parent)

    self.parentWidget = parent

    self.setupUI()
    self.colleges = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

    # For mouse features
    self.setMouseTracking(True)
    self.viewport().setMouseTracking(True)
    self.viewport().installEventFilter(self)

    self.initialCollegesToDisplay()
    
  def setupUI(self):
    self.setColumnCount(len(self.headers))
    self.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
    self.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
    self.setSortingEnabled(False)
    self.setStyleSheet("""
                        QHeaderView::section { 
                          font-weight: bold; 
                          font-size: 9pt;
                        }
                       QHeaderView::section:vertical {
                          font-weight: normal; 
                          font-size: 9pt;
                        }
                        QPushButton { 
                          font: 9pt "Inter"; 
                          font-weight: bold; 
                          padding: 0px 15px; 
                          border-radius: 3px; 
                        } 
                       
                        QTableWidget {
                            gridline-color: transparent;
                        }
                        QTableWidget::item {
                            border-bottom: 1px solid rgb(120, 139, 140); 
                            border-right: 1px solid transparent;
                        }
                        QTableWidget::item:selected {
                          background-color: rgb(105, 105, 105); 
                        }
                       
                        #deleteButton { background-color: rgb(160, 63, 63); } 
                        #editButton { background-color: rgb(63, 150, 160); } 
                        #editButton::hover { background-color: rgb(83, 170, 180); } 
                        #deleteButton::hover { background-color: rgb(180, 83, 83); } 
                        QFrame { border: none; background: transparent; } 
                        QLabel { border: none; background: transparent; font: 9pt "Inter"; }
                      """)
    
    self.verticalHeader().setDefaultSectionSize(40)  # Increase row height
    self.verticalHeader().setFixedWidth(35)
    self.verticalHeader().setVisible(False)
    self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    header = self.horizontalHeader()
    header.setMinimumHeight(40)
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    self.setHorizontalHeaderLabels(self.headers)

  #--------------------------------------------------------------------------
  
  def refreshDisplayColleges(self):
    self.setRowCount(0)
    self.updateSortByIndex()
    primaryField, secondaryField = self.sortByFields[self.sortByIndex]
    sortingOrder = "ASC" if self.sortingOrder == 0 else "DESC"
    
    searchField = None
    searchValue = ""

    if self.parentWidget.isSearchActive:
      searchIndex = self.parentWidget.searchByComboBox.currentIndex()
      if searchIndex > 1:
        searchField = self.searchByFields[searchIndex - 2]
      searchValue = self.parentWidget.searchBarLineEdit.text().strip()

    page = int(self.parentWidget.page)

    colleges, totalCount = getColleges(page=page, sortBy1=primaryField, sortBy2=secondaryField, sortOrder=sortingOrder, searchField=searchField, searchTerm=searchValue)
    self.colleges = colleges
    
    lastPage = (totalCount + 50 - 1) // 50
    self.parentWidget.lastPage = lastPage
    self.parentWidget.validator.setTop(lastPage)
    self.parentWidget.lastPageInfo.setText(f"of {lastPage}")

    self.populateTable()
  
  def initialCollegesToDisplay(self):
    self.setRowCount(0)
    colleges, _ = getColleges()
    if not colleges:
      self.colleges = []
      return
    
    self.colleges = colleges
    self.refreshDisplayColleges()

  def populateTable(self):
    self.setRowCount(len(self.colleges))
    
    for row, college in enumerate(self.colleges):
      self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(college["college_code"])))

      collegeName = QTableWidgetItem(college["college_name"])
      self.setItem(row, 1, collegeName)
      
      operationsWidget = QtWidgets.QWidget()
      operationsLayout = QtWidgets.QHBoxLayout()
      operationsLayout.setContentsMargins(0, 0, 0, 0)
      operationsLayout.setSpacing(0)

      editButton = QtWidgets.QPushButton()
      editButton.setObjectName("editButton")
      editButton.setIcon(QIcon("assets/edit.png"))
      editButton.setFixedSize(30, 30)
      editButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      editButton.clicked.connect(lambda _, s=college: self.openUpdateCollegeDialog(s))
      
      self.editOpacity = QGraphicsOpacityEffect()
      editButton.setGraphicsEffect(self.editOpacity)
      self.editOpacity.setOpacity(0.0) 

      deleteButton = QtWidgets.QPushButton()
      deleteButton.setObjectName("deleteButton")
      deleteButton.setIcon(QIcon("assets/delete.png"))
      deleteButton.setFixedSize(30, 30)
      deleteButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      deleteButton.clicked.connect(lambda _, s=college: self.deleteSelectedRow(s))

      self.deleteOpacity = QGraphicsOpacityEffect()
      deleteButton.setGraphicsEffect(self.deleteOpacity)
      self.deleteOpacity.setOpacity(0.0)

      operationsLayout.addWidget(editButton)
      operationsLayout.addWidget(deleteButton)
      operationsWidget.setLayout(operationsLayout)
      operationsWidget.setStyleSheet(operationsWidget.setStyleSheet("""
        QPushButton { font: 9pt "Inter"; font-weight: bold; padding: 0px 15px; border-radius: 3px; }
        QPushButton#editButton { background-color: rgb(63, 150, 160); }
        QPushButton#deleteButton { background-color: rgb(160, 63, 63); }
        QPushButton#editButton:hover { background-color: rgb(83, 170, 180); }
        QPushButton#deleteButton:hover { background-color: rgb(180, 83, 83); }
      """))
      
      self.setCellWidget(row, 2, operationsWidget)

    self.viewport().installEventFilter(self)
  
  def updateSortByIndex(self):
    sortByIndex = self.parentWidget.sortByComboBox.currentIndex()
    sortingOrder = self.parentWidget.sortingOrderComboBox.currentIndex()

    self.sortByIndex = max(0, sortByIndex - 1)
    self.sortingOrder = max(0, sortingOrder)
  
  def openUpdateCollegeDialog(self, collegeRowData):
    selectedRows = list(set(index.row() for index in self.selectedIndexes()))
    collegeData = list(collegeRowData.values())
    self.updateDialog = UpdateCollegeDialog(self, collegeData)
    self.updateDialog.collegeUpdatedTableSignal.connect(self.refreshDisplayColleges)
    self.updateDialog.updateTablesSignal.connect(self.updateTablesSignal)
    self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)

    if len(selectedRows) > 1:
      self.statusMessageSignal.emit("Colleges can only be updated one at a time.", 3000)
      
    self.updateDialog.exec()

  def deleteSelectedRow(self, college):
    selectedRows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
    selectedRowCount = len(selectedRows)

    # Multiple Deletions
    if len(selectedRows) > 1:
      collegeCodesText = f'\n{"\n".join(f'{self.item(row, 0).text()}' for row in selectedRows)}'
      promptText = f"the following colleges?\n{collegeCodesText}" if selectedRowCount < 20 else f"{selectedRowCount} colleges"
      if not self.showDeleteConfirmation(self, promptText):
        return

      collegeCodes = []
      for row in sorted(selectedRows, reverse=True):      # Reverse to avoid shifting indices
        collegeCodes.append(self.colleges[row]["college_code"])

      result = batchRemoveColleges(collegeCodes)
      if result != "Colleges removed successfully.":
        self.statusMessageSignal.emit("Failed to remove selected colleges.", 3000)
        return

      for row in sorted(selectedRows, reverse=True):  
        self.colleges.pop(row)
        self.removeRow(row)
      
      self.statusMessageSignal.emit("Selected colleges removed successfully.", 3000)
    
    # Single Deletion
    else:
      if not self.showDeleteConfirmation(self, college["college_name"]):
        return

      # Remove from CSV
      result = removeCollege(college["college_code"])

      if result != "College removed successfully.":
        self.statusMessageSignal.emit(result, 3000)
        return

      # Find the row index of the program
      rowToRemove = -1
      for row in range(self.rowCount()):
        if self.item(row, 0) and self.item(row, 0).text() == str(college["college_code"]):
          rowToRemove = row
          break

      if rowToRemove == -1:
        self.statusMessageSignal.emit("Error: College not found in table.", 3000)
        return

      # Remove program from internal list
      self.colleges.remove(college)

      # Remove row from QTableWidget
      self.removeRow(rowToRemove)
      self.statusMessageSignal.emit(result, 3000)
    
    self.updateTablesSignal.emit()

  def showDeleteConfirmation(self, parent, collegeName):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setWindowTitle("Confirm Deletion")
    msgBox.setText(f"Are you sure you want to delete {collegeName}?")
    msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

    for button in msgBox.findChildren(QtWidgets.QPushButton):
      button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

    msgBox.setStyleSheet("""
      QMessageBox {
        background-color: rgb(37, 37, 37);
        color: white;
        border-radius: 10px;
      }
      QMessageBox QLabel {
        color: white;
        font-family: \"Inter\";
      }
      QMessageBox QPushButton {
        font: 9pt "Inter";
        font-weight: bold;
        padding: 0px, 15px;
        background-color: rgb(63, 150, 160);
        border-radius: 3px;
        padding: 5px 15px;
      }
                         
      QMessageBox QPushButton::hover {
        background-color: rgb(83, 170, 180);
      }
    """)

    # Show the dialog and return the user's choice
    return msgBox.exec() == QtWidgets.QMessageBox.StandardButton.Yes
  
  def eventFilter(self, obj, event):
    if obj == self.viewport():
      if event.type() == QtCore.QEvent.Type.MouseMove:
        index = self.indexAt(event.pos())  # Get index of row under mouse
        if index.isValid():
          self.toggleButtons(index.row())
        else:
          self.toggleButtons(-1)  # Hide buttons when not over a valid row
      elif event.type() == QtCore.QEvent.Type.Leave:
        self.toggleButtons(-1)  # Hide buttons when mouse leaves the table
    return super().eventFilter(obj, event)

  def toggleButtons(self, row):
    for r in range(self.rowCount()):
      operationsWidget = self.cellWidget(r, 2)
      if operationsWidget:
        for i in range(operationsWidget.layout().count()):
          widget = operationsWidget.layout().itemAt(i).widget()
          if widget and isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            widget.graphicsEffect().setOpacity(1.0 if r == row else 0.0)
