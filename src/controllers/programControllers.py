from model.Program import Program
from model.College import College
from typing import List, Dict, Any
from utils.inputUtils import *

PROGRAM_SEARCH_FIELDS = ["program_code", "program_name", "college_code"]

def addProgram(programCode: str, programName: str, collegeCode: str) -> bool:
  if not all([programCode, programName, collegeCode]):
    return("Enter all required fields")
  
  if not College.collegeCodeExists(collegeCode):
    return "College Code does not exist"
  
  if Program.programCodeExists(programCode):
    return "Program already exists"
  
  newProgram = Program(programCode, programName, collegeCode)
  isSuccessful = Program.addNewProgram(newProgram)

  return "Program added successfully." if isSuccessful else "Failed to add program."

def getAllPrograms() -> List[Dict[str, str]]:
  return Program.getAllProgramRecords()

def searchProgramsByField(value: str, field: str = None) -> List[Dict[str, str]]:
  if field and field not in PROGRAM_SEARCH_FIELDS:
    print("Search field not valid")
    return []
  
  if not isinstance(value, str):
    print("Search value not valid")
    return []
  
  if field == PROGRAM_SEARCH_FIELDS[0]:
    return [Program.getProgramRecordByCode(value)]
  
  if field == PROGRAM_SEARCH_FIELDS[1]:
    return Program.getProgramRecordsByName(value)
    
  if field == PROGRAM_SEARCH_FIELDS[2]:
    return Program.getProgramRecordsByCollege(value)

def updateProgram(originalProgramCode: str, newProgramCode: Any, newProgramName: Any, newCollegeCode: Any) -> bool:
  
  if not College.collegeCodeExists(newCollegeCode):
    return "College Code does not exist"

  updateData = {
    "program_code": newProgramCode,
    "program_name": newProgramName,
    "college_code": newCollegeCode,
  }

  isSuccessful = Program.updateProgramRecordByCode(originalProgramCode, updateData)

  return "Program updated successfully." if isSuccessful else "Failed to update program."

def removeProgram(programCode: str) -> str:
  if not programCode:
    return "Program Code is required."

  isSuccessful = Program.deleteProgramRecord(programCode)

  return "Program removed successfully." if isSuccessful else "Failed to remove program." 