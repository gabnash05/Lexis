from typing import List, Dict, Tuple, Any
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
      print(f"College Model Error checking if college code exists: {e}")
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
        print(f"College Model Error inserting college: {e}")
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
        SELECT * FROM colleges 
        WHERE college_code = %s
        ORDER BY college_code;
      """

      try:
        cursor.execute(query, (collegeCode,))

        college = cursor.fetchone()
      
      except Exception as e:
        print(f"College Model Error fetching colleges by code: {e}")
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
        SELECT * FROM colleges 
        WHERE college_name = %s
        ORDER BY college_code;
      """

      try:
        cursor.execute(query, (collegeName,))

        college = cursor.fetchone()
      
      except Exception as e:
        print(f"College Model Error fetching colleges by name: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return college
  
  # Get all college records
  @staticmethod
  def getCollegeRecords(page=1, perPage=50, sortBy1="college_code", sortBy2="college_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
    conn = getConnection()

    if not conn:
      return [], 0
    
    cursor = conn.cursor(dictionary=True)
    
    params = []
    colleges = []
    offset = (page - 1) * perPage
    searchTerms = searchTerm.split()
    searchQuery = "WHERE ("

    
    if searchField:
      searchQuery += f"c.{searchField} LIKE %s"
      params.append(f"%{searchTerm}%")
    else:
      searchQuery += """
        c.college_code LIKE %s 
        OR c.college_name LIKE %s
      """
      params.extend([f"%{searchTerm}%"] * 2)

    searchQuery += ")"

    # Query to get the total count of matching records
    countQuery = f"""
      SELECT COUNT(*) as total 
      FROM colleges c 
      {searchQuery}
    """

    try:
      cursor.execute(countQuery, params)
      totalRecords = cursor.fetchone()["total"]
    except Exception as e:
      print(f"College Model Error fetching colleges: {e}")
      totalRecords = 0

    query = f"""
      SELECT * 
      FROM colleges c 
      {searchQuery}
      ORDER BY {sortBy1} {sortOrder}, {sortBy2} ASC
      LIMIT %s OFFSET %s
    """

    params.extend([perPage, offset])

    try:
      cursor.execute(query, params)
      colleges = cursor.fetchall()
    except Exception as e:
      print(f"College Model Error fetching colleges: {e}")
    finally:
      cursor.close()
      conn.close()
    
    return colleges, totalRecords

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

      return cursor.rowcount >= 0

    except Exception as e:
      print(f"College Model Error updating college: {e}")
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
      print(f"College Model Error deleting college: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Batch Removes college records
  @staticmethod
  def removeBatchCollegeRecordsById(collegeCodes: List[str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    idNumberPlaceholders = ", ".join(["%s"] * len(collegeCodes))
    whereClause = f"WHERE college_code IN ({idNumberPlaceholders})"
    values = tuple(collegeCodes)

    query = f"""
      DELETE FROM colleges
      {whereClause}
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"College Model Error batch deleting colleges: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()