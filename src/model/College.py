from typing import List, Dict, Any
import utils.csvUtils as csvUtils
from pathlib import Path

from database.db import getConnection

class College:
  COLLEGE_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "colleges.csv"
  COLLEGE_HEADERS = ["College Code", "College Name"]

  def __init__(self, collegeCode, name):
    self.collegeCode = collegeCode
    self.name = name
  
  def toDict(self) -> Dict:
    return {
      "College Code": self.collegeCode,
      "College Name": self.name,
    }
  
  # Checks if College Code already exists
  @staticmethod
  def collegeCodeExists(collegeCode: str) -> bool:
    return csvUtils.checkIdIfExistsCsv(College.COLLEGE_CSV_FILEPATH, collegeCode)

  # Add new college
  @staticmethod
  def addNewCollege(college: Any) -> bool:
    conn = getConnection()
    if conn:
      cursor = conn.cursor()
      query = """
        INSERT INTO colleges (college_code, college_name)
        VALUES (%s, %s)
      """
      newCollege = college.toDict()

      try:
        cursor.execute(query, (newCollege["College Code"], newCollege["College Name"]))
        conn.commit()
      except Exception as e:
        print(f"Error inserting student: {e}")
      finally:
        cursor.close()
        conn.close()
  
  # Get college record
  @staticmethod
  def getCollegeRecordByCode(collegeCode: str) -> Dict[str, str]:
    return csvUtils.getRowByIdCsv(College.COLLEGE_CSV_FILEPATH, collegeCode)
  
  # Get college record
  @staticmethod
  def getCollegeRecordByName(collegeName: str) -> Dict[str, str]:
    return csvUtils.getRowsByFieldCsv(College.COLLEGE_CSV_FILEPATH, collegeName, College.COLLEGE_HEADERS[1])
  
  # Get all college records
  @staticmethod
  def getAllCollegeRecords() -> List[Dict[str, str]]:
    return csvUtils.readCsv(College.COLLEGE_CSV_FILEPATH)

  # Get program record
  @staticmethod
  def updateCollegeRecord(collegeCode: str, updateData: Dict[str, str]) -> bool:
    return csvUtils.updateRowByFieldCsv(College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS[0], collegeCode, updateData)
  
  # Remove college
  @staticmethod
  def deleteCollegeRecord(collegeCode: str) -> bool:
    return csvUtils.deleteRowByFieldCsv(College.COLLEGE_CSV_FILEPATH, College.COLLEGE_HEADERS[0], collegeCode)
  
  # Searches for college records without a search field
  @staticmethod
  def searchForCollege(searchValue: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(College.COLLEGE_CSV_FILEPATH, searchValue, None)