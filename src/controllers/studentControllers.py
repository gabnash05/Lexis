from model.Student import Student
from model.Program import Program
from model.College import College
from typing import List, Dict, Tuple, Any
from utils.inputUtils import *

STUDENT_SEARCH_FIELDS = ["id_number", "first_name", "last_name", "program_code", "college_code"]

def addStudent(idNumber: str, firstName: str, lastName: str, yearLevel: str, gender: str, programCode: str, collegeCode: str) -> str:
  if not all([idNumber, firstName, lastName, gender, programCode]):
    return("Enter all required fields")
  
  # converts year level into an int
  if isinstance(yearLevel, str) and yearLevel.isdigit():
    yearLevel = int(yearLevel)
  if not validateYearLevel(yearLevel):
    return("Year Level must be a positive integer.")
  
  if not validateIdNumber(idNumber):
    return("Invalid ID Number")
  
  if not validateGender(gender):
    return "Gender must be Male, Female, or Others."
  
  if Student.idNumberExists(idNumber):
    return "ID number already exists"

  if not Program.programCodeExists(programCode):
    return "Program Code does not exist"
  
  if not College.collegeCodeExists(collegeCode):
    return "College Code does not exist"
  
  newStudent = Student(idNumber, firstName, lastName, yearLevel, gender, programCode, collegeCode)
  isSuccessful = Student.addStudentRecord(newStudent)

  return "Student added successfully." if isSuccessful else "Failed to add student."

def getStudents(page=1, perPage=50, sortBy1="id_number", sortBy2="last_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
  return Student.getStudentRecords(page, perPage, sortBy1, sortBy2, sortOrder, searchField, searchTerm)

def updateStudent(originalId, newIdNumber: str, newFirstName: str, newLastName: str, newYearLevel: int, newGender: str, newProgramCode: str, newCollegeCode: str, validateParameters: bool) -> str:
  if validateParameters:
    if newProgramCode == None:
      return("Select a Valid Program Code")
    
    if newCollegeCode == None:
      return("Select a Valid College Code")

  if not validateIdNumber(originalId):
    return("Invalid ID Number")
  
  # converts year level into an int
  if isinstance(newYearLevel, str) and newYearLevel.isdigit():
    newYearLevel = int(newYearLevel)
  if newYearLevel and not validateYearLevel(newYearLevel):
    return("Year Level must be a positive integer.")
  
  if newGender and not validateGender(newGender):
    return "Gender must be Male, Female, or Other."
  
  if newProgramCode and not Program.programCodeExists(newProgramCode):
    return "Program Code does not exist"
  
  if newCollegeCode and not College.collegeCodeExists(newCollegeCode):
    return "College Code does not exist"
  
  updateData = {
    key: value
    for key, value in {
      "id_number": newIdNumber,
      "first_name": newFirstName,
      "last_name": newLastName,
      "year_level": newYearLevel,
      "gender": newGender,
      "program_code": newProgramCode,
    }.items()
    if value is not None
  }

  isSuccessful = Student.updateStudentRecordById(originalId, updateData)

  return "Student updated successfully." if isSuccessful else "Failed to update student."

def batchUpdateStudents(studentIds: List[str], newYearLevel: int, newGender: str, newProgramCode: str, newCollegeCode: str, validateParameters: bool) -> str:
  if validateParameters:
    if newProgramCode is None:
      return "Select a Valid Program Code"
    if newCollegeCode is None:
      return "Select a Valid College Code"

  if isinstance(newYearLevel, str) and newYearLevel.isdigit():
    newYearLevel = int(newYearLevel)

  if newYearLevel and not validateYearLevel(newYearLevel):
    return "Year Level must be a positive integer."

  if newGender and not validateGender(newGender):
    return "Gender must be Male, Female, or Other."

  if newProgramCode and not Program.programCodeExists(newProgramCode):
    return "Program Code does not exist"

  if newCollegeCode and not College.collegeCodeExists(newCollegeCode):
    return "College Code does not exist"

  updateData = {
    key: value
    for key, value in {
      "year_level": newYearLevel,
      "gender": newGender,
      "program_code": newProgramCode,
      "college_code": newCollegeCode
    }.items()
    if value is not None 
  }

  isSuccessful = Student.updateBatchStudentRecordsById(studentIds, updateData)

  return "Students updated successfully." if isSuccessful else "Failed to update students."

def removeStudent(idNumber: str) -> str:
  if not validateIdNumber(idNumber):
    return("Invalid ID Number")
  
  isSuccessful = Student.removeStudentRecordById(idNumber)

  return "Student removed successfully." if isSuccessful else "Failed to remove student."