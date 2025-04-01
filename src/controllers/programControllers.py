from model.Program import Program
from model.College import College
from typing import List, Dict, Tuple, Any
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

def getPrograms(page=1, perPage=50, sortBy1="program_code", sortBy2="program_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
  return Program.getProgramRecords(page, perPage, sortBy1, sortBy2, sortOrder, searchField, searchTerm)

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

def batchRemovePrograms(programCodes: List[str]) -> str:
  isSuccesful = Program.removeBatchProgramRecordsById(programCodes)

  return "Programs removed successfully." if isSuccesful else "Failed to remove programs."