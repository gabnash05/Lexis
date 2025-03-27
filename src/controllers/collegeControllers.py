from model.Program import Program
from model.College import College
from typing import List, Dict, Any
from utils.inputUtils import *

COLLEGE_SEARCH_FIELDS = ["college_code", "college_name"]

def addCollege(collegeCode: str, collegeName: str) -> bool:
  if not all([collegeCode, collegeName]):
    return "Enter all required fields"
  
  if College.collegeCodeExists(collegeCode):
    return "College already exists"
  
  newCollege = College(collegeCode, collegeName)
  isSuccessful = College.addNewCollege(newCollege)

  return "College added successfully." if isSuccessful else "Failed to add college."

def getAllColleges() -> List[Dict[str, str]]:
  return College.getAllCollegeRecords()

def searchCollegesByField(value: str, field: str = None) -> List[Dict[str, str]]:
  if field and field not in COLLEGE_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []

  if field == COLLEGE_SEARCH_FIELDS[0]:
    return [College.getCollegeRecordByCode(value)]
  
  if field == COLLEGE_SEARCH_FIELDS[1]:
    return College.getCollegeRecordByName(value)

def updateCollege(originalCollegeCode: str, newCollegeCode: Any, newCollegeName: Any) -> bool:

  if not College.collegeCodeExists(originalCollegeCode):
    return "college_code does not exist"

  updateData = {
    "college_code": newCollegeCode, 
    "college_name": newCollegeName,
  }

  isSuccessful = College.updateCollegeRecord(originalCollegeCode, updateData)

  return "College updated successfully." if isSuccessful else "Failed to update college."

def removeCollege(collegeCode: str) -> str:
  if not collegeCode:
    return "College Code is required."

  isSuccessful = College.deleteCollegeRecord(collegeCode)

  return "College removed successfully." if isSuccessful else "Failed to remove college."