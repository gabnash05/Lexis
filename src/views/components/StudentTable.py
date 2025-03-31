from operator import itemgetter

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon

from controllers.studentControllers import getStudents, removeStudent
from views.components.UpdateStudentDialog import UpdateStudentDialog
from views.components.UpdateBatchStudentDialog import UpdateBatchStudentDialog

class StudentTable(QtWidgets.QTableWidget):
  # Student variables
  headers = ["ID Number", "Name", "Gender", "Year Level", "Program", "College", "Operations"]
  sortByFields = [("id_number", "last_name"), ("first_name", "last_name"), ("last_name", "first_name"), ("gender", "last_name"), ("year_level", "last_name"), ("program_code", "last_name"), ("college_code", "last_name")]
  searchByFields = ["id_number", "first_name", "last_name", "gender", "year_level", "program_code", "college_code"]

  # Signals
  statusMessageSignal = pyqtSignal(str, int)
  editStudentSignal = pyqtSignal(list)
  deleteStudentSignal = pyqtSignal(str)

  def __init__(self, parent=None):
    super().__init__(parent)
    self.parentWidget = parent

    self.setupUI()
    self.students = []
    self.sortByIndex = 0
    self.sortingOrder = 0

    self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
    
    # For mouse features
    self.setMouseTracking(True)
    self.viewport().setMouseTracking(True)
    self.viewport().installEventFilter(self)

    self.initialStudentsToDisplay()

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
    
    self.verticalHeader().setDefaultSectionSize(40)
    self.verticalHeader().setFixedWidth(35)
    self.verticalHeader().setVisible(False)
    self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    header = self.horizontalHeader()
    header.setMinimumHeight(40)
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeMode.Fixed)
    
    self.setHorizontalHeaderLabels(self.headers)

  #--------------------------------------------------------------------------
  
  def refreshDisplayStudents(self):
    self.setRowCount(0)
    self.updateSortByIndex()
    primaryField, secondaryField = self.sortByFields[self.sortByIndex]
    sortingOrder = "ASC" if self.sortingOrder == 0 else "DESC"
    
    searchField = None
    searchValue = ""

    if self.parentWidget.isSearchActive:
      searchIndex = self.parentWidget.searchByComboBox.currentIndex()
      if searchIndex > 1:
        searchField = self.searchByFields[searchIndex]
      searchValue = self.parentWidget.searchBarLineEdit.text().strip()

    page = int(self.parentWidget.page)

    students, totalCount = getStudents(page=page, sortBy1=primaryField, sortBy2=secondaryField, sortOrder=sortingOrder, searchField=searchField, searchTerm=searchValue)
    self.students = students
    
    lastPage = (totalCount + 50 - 1) // 50
    self.parentWidget.lastPage = lastPage
    self.parentWidget.validator.setTop(lastPage)

    self.populateTable()

  def initialStudentsToDisplay(self):
    self.setRowCount(0)
    students, _ = getStudents()
    if not students:
      self.programs = []
      return
    
    self.students = students
    self.refreshDisplayStudents()

  def populateTable(self):
    self.setRowCount(len(self.students))
    
    for row, student in enumerate(self.students):
      self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(student["id_number"])))

      nameItem = QTableWidgetItem(f"{student['first_name']} {student['last_name']}")
      self.setItem(row, 1, nameItem)

      genderItem = QTableWidgetItem(student["gender"])
      genderItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 2, genderItem)

      yearLevelItem = QTableWidgetItem(str(student["year_level"]))
      yearLevelItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 3, yearLevelItem)

      programCodeItem = QTableWidgetItem(student["program_code"])
      programCodeItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 4, programCodeItem)
      
      collegeCodeItem = QTableWidgetItem(student["college_code"])
      collegeCodeItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
      self.setItem(row, 5, collegeCodeItem)
      
      operationsWidget = QtWidgets.QWidget()
      operationsLayout = QtWidgets.QHBoxLayout()
      operationsLayout.setContentsMargins(0, 0, 0, 0)
      operationsLayout.setSpacing(0)

      editButton = QtWidgets.QPushButton()
      editButton.setObjectName("editButton")
      editButton.setIcon(QIcon("assets/edit.png"))
      editButton.setFixedSize(30, 30)
      editButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      editButton.clicked.connect(lambda _, s=student: self.openUpdateStudentDialog(s))
      
      self.editOpacity = QGraphicsOpacityEffect()
      editButton.setGraphicsEffect(self.editOpacity)
      self.editOpacity.setOpacity(0.0) 

      deleteButton = QtWidgets.QPushButton()
      deleteButton.setObjectName("deleteButton")
      deleteButton.setIcon(QIcon("assets/delete.png"))
      deleteButton.setFixedSize(30, 30)
      deleteButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
      deleteButton.clicked.connect(lambda _, s=student: self.deleteSelectedRow(s))

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
      
      self.setCellWidget(row, 6, operationsWidget)

    self.viewport().installEventFilter(self)

  def updateSortByIndex(self):
    sortByIndex = self.parentWidget.sortByComboBox.currentIndex()
    sortingOrder = self.parentWidget.sortingOrderComboBox.currentIndex()
    
    self.sortByIndex = max(0, sortByIndex - 1)
    self.sortingOrder = max(0, sortingOrder)
  
  def openUpdateStudentDialog(self, studentRowData):
    selectedRows = list(set(index.row() for index in self.selectedIndexes()))
    if not selectedRows or len(selectedRows) == 1:
      studentData = list(studentRowData.values())
      self.updateDialog = UpdateStudentDialog(self, studentData)
      self.updateDialog.studentUpdatedTableSignal.connect(self.refreshDisplayStudents)
      self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)
      self.updateDialog.exec()
      return

    studentsData = [
      [
        self.item(row, 0).text() if self.item(row, 0) else "",  # ID Number
        self.item(row, 1).text().split()[0] if self.item(row, 1) else "",  # First Name
        " ".join(self.item(row, 1).text().split()[1:]) if self.item(row, 1) else "",  # Last Name
        self.item(row, 3).text() if self.item(row, 3) else "",  # Year Level
        self.item(row, 2).text() if self.item(row, 2) else "",  # Gender
        self.item(row, 4).text() if self.item(row, 4) else "",  # Program Code
        self.item(row, 5).text() if self.item(row, 5) else "",  # college_code
      ]
      for row in selectedRows
    ]

    self.updateDialog = UpdateBatchStudentDialog(self, studentsData)
    self.updateDialog.studentUpdatedTableSignal.connect(self.refreshDisplayStudents)
    self.updateDialog.statusMessageSignal.connect(self.parentWidget.displayMessageToStatusBar)
    self.updateDialog.exec()

  def deleteSelectedRow(self, student):
    selectedRows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
    selectedRowCount = len(selectedRows)

    # Multiple Deletions
    if len(selectedRows) > 1:
      studentNames = f'\n{"\n".join(f'{self.item(row, 1).text()}' for row in selectedRows)}'

      promptText = f"the following students?\n{studentNames}" if selectedRowCount < 20 else f"{selectedRowCount} students"

      if not self.showDeleteConfirmation(self, promptText):
        return
      
      failedDeletions = []

      for row in sorted(selectedRows, reverse=True):  # Reverse to avoid shifting indices
        student = self.students[row]
        result = removeStudent(student["id_number"])

        if result == "Student removed successfully.":
          self.students.pop(row)
          self.removeRow(row)
        else:
          failedDeletions.append(student["id_number"])

      # Emit status message
      if failedDeletions:
        self.statusMessageSignal.emit(f"Failed to remove: {', '.join(failedDeletions)}", 3000)
      else:
        self.statusMessageSignal.emit("Selected students removed successfully.", 3000)
    
    # Single Deletion
    else:
      if not self.showDeleteConfirmation(self, f'{student["first_name"]} {student["last_name"]}'):
        return

      # Remove from CSV
      result = removeStudent(student["id_number"])

      if result != "Student removed successfully.":
        self.statusMessageSignal.emit(result, 3000)
        return

      # Find the row index of the student
      rowToRemove = -1
      for row in range(self.rowCount()):
        if self.item(row, 0) and self.item(row, 0).text() == str(student["id_number"]):
          rowToRemove = row
          break

      if rowToRemove == -1:
        self.statusMessageSignal.emit("Error: Student not found in table.", 3000)
        return

      # Remove student from internal list
      self.students.remove(student)

      # Remove row from QTableWidget
      self.removeRow(rowToRemove)

      self.statusMessageSignal.emit(result, 3000)

  def showDeleteConfirmation(self, parent, studentName):
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setWindowTitle("Confirm Deletion")
    msgBox.setText(f"Are you sure you want to delete {studentName}?")
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
  
  def handleStudentDeleted(self, message, duration):
    self.refreshDisplayStudents()
    self.statusMessageSignal.emit(message, duration)

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
      operationsWidget = self.cellWidget(r, 6)
      if operationsWidget:
        for i in range(operationsWidget.layout().count()):
          widget = operationsWidget.layout().itemAt(i).widget()
          if widget and isinstance(widget.graphicsEffect(), QGraphicsOpacityEffect):
            widget.graphicsEffect().setOpacity(1.0 if r == row else 0.0)
  