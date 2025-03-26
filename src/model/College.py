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
    conn = getConnection()
    
    if not conn:
      return False 

    try:
      cursor = conn.cursor()

      query = "SELECT 1 FROM colleges WHERE college_code = %s LIMIT 1;"
      cursor.execute(query, (collegeCode,))

      return cursor.fetchone() is not None

    except Exception as e:
      print(f"Error checking if college code exists: {e}")
      return False

    finally:
      cursor.close()
      conn.close()

  # Add new college
  @staticmethod
  def addNewCollege(college: Any) -> bool:
    conn = getConnection()
    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        INSERT INTO colleges (college_code, college_name)
        VALUES (%s, %s);
      """
      newCollege = college.toDict()

      try:
        cursor.execute(query, (newCollege["College Code"], newCollege["College Name"]))
        conn.commit()

        return cursor.rowcount > 0
      
      except Exception as e:
        print(f"Error inserting college: {e}")
        return False
      finally:
        cursor.close()
        conn.close()
  
  # Get college record
  @staticmethod
  def getCollegeRecordByCode(collegeCode: str) -> Dict[str, str]:
    conn = getConnection()
    college = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM colleges WHERE college_code = %s;
      """

      try:
        cursor.execute(query, (collegeCode,))

        college = cursor.fetchone()
      
      except Exception as e:
        print(f"Error fetching colleges by code: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return college
  
  # Get college record
  @staticmethod
  def getCollegeRecordByName(collegeName: str) -> Dict[str, str]:
    conn = getConnection()
    college = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM colleges WHERE college_name = %s;
      """

      try:
        cursor.execute(query, (collegeName,))

        college = cursor.fetchone()
      
      except Exception as e:
        print(f"Error fetching colleges by name: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return college
  
  # Get all college records
  @staticmethod
  def getAllCollegeRecords() -> List[Dict[str, str]]:
    conn = getConnection()
    colleges = []

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM colleges;
      """

      try:
        cursor.execute(query)

        colleges = cursor.fetchall()
      
      except Exception as e:
        print(f"Error fetching all colleges: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return colleges

  # Get program record
  @staticmethod
  def updateCollegeRecord(collegeCode: str, updateData: Dict[str, str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    setClause = ", ".join(f'{key} = %s' for key in updateData.keys())
    values = tuple(updateData.values()) + (collegeCode,)

    query = f"""
      UPDATE colleges
      SET {setClause}
      WHERE college_code = %s;
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Error updating college: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Remove college
  @staticmethod
  def deleteCollegeRecord(collegeCode: str) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    query = f"""
      DELETE FROM colleges WHERE college_code = %s;
    """

    try:
      cursor.execute(query, (collegeCode,))
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Error deleting college: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Searches for college records without a search field
  @staticmethod
  def searchForCollege(searchValue: str) -> List[Dict[str, str]]:
    return csvUtils.getRowsByFieldCsv(College.COLLEGE_CSV_FILEPATH, searchValue, None)