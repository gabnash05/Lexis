from model.College import College
from typing import List, Dict, Tuple, Any
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

def getColleges(page=1, perPage=50, sortBy1="college_code", sortBy2="college_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
  return College.getCollegeRecords(page, perPage, sortBy1, sortBy2, sortOrder, searchField, searchTerm)

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

def batchRemoveColleges(collegeCodes: List[str]) -> str:
  isSuccesful = College.removeBatchCollegeRecordsById(collegeCodes)

  return "Colleges removed successfully." if isSuccesful else "Failed to remove colleges."