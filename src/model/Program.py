from typing import List, Dict, Tuple, Any
from pathlib import Path

from database.db import getConnection

class Program:
  PROGRAM_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "programs.csv"

  PROGRAM_HEADERS = ["Program Code", "Program Name", "College Code"]

  def __init__(self, programCode: str, name: str, collegeCode: str):
    self.programCode = programCode
    self.name = name
    self.collegeCode = collegeCode
  
  def toDict(self) -> Dict:
    return {
      "Program Code": self.programCode, 
      "Program Name": self.name,
      "College Code": self.collegeCode,
    }
  
  # Checks if Program Code already exists
  @staticmethod
  def programCodeExists(programCode: str) -> bool:
    conn = getConnection()
      
    if not conn:
      return False 

    try:
      cursor = conn.cursor()

      query = "SELECT 1 FROM programs WHERE program_code = %s LIMIT 1;"
      cursor.execute(query, (programCode,))

      return cursor.fetchone() is not None

    except Exception as e:
      print(f"Program Model Error checking if program code exists: {e}")
      return False

    finally:
      cursor.close()
      conn.close()

  # Add new program
  @staticmethod
  def addNewProgram(program: Any) -> bool:
    conn = getConnection()

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        INSERT INTO programs (program_code, program_name, college_code)
        VALUES (%s, %s, %s);
      """
      newProgram = program.toDict()

      try:
        cursor.execute(query, (newProgram["Program Code"], newProgram["Program Name"], newProgram["College Code"]))
        conn.commit()

        return cursor.rowcount > 0
      
      except Exception as e:
        print(f"Program Model Error inserting program: {e}")
        return False
      finally:
        cursor.close()
        conn.close()

  # Get student records with page, search value, and sorting order
  @staticmethod
  def getProgramRecords(page=1, perPage=50, sortBy1="program_code", sortBy2="program_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
    conn = getConnection()

    if not conn:
      return [], 0
    
    cursor = conn.cursor(dictionary=True)
    
    params = []
    programs = []
    offset = (page - 1) * perPage
    searchQuery = "WHERE ("

    if searchField:
      if searchField == "program_code" and searchTerm != "":
        searchQuery += f"{searchField} = %s"
        params.append(f"{searchTerm}")
      else:
        searchQuery += f"{searchField} LIKE %s"
        params.append(f"%{searchTerm}%")
    else:
      searchQuery += """
        program_code LIKE %s 
        OR program_name LIKE %s
        OR college_code LIKE %s
      """
      params.extend([f"%{searchTerm}%"] * 3)

    searchQuery += ")"

    # Query to get the total count of matching records
    countQuery = f"""
      SELECT COUNT(*) as total 
      FROM programs p 
      {searchQuery}
    """

    try:
      cursor.execute(countQuery, params)
      totalRecords = cursor.fetchone()["total"]
    except Exception as e:
      print(f"Program Model Error fetching program: {e}")
      totalRecords = 0

    query = f"""
      SELECT * 
      FROM programs
      {searchQuery}
      ORDER BY {sortBy1} {sortOrder}, {sortBy2} ASC
      LIMIT %s OFFSET %s
    """

    params.extend([perPage, offset])
    
    try:
      cursor.execute(query, params)
      programs = cursor.fetchall()
    except Exception as e:
      print(f"Program Model Error fetching programs: {e}")
    finally:
      cursor.close()
      conn.close()
    
    return programs, totalRecords

  # Get program record by code
  @staticmethod
  def getProgramRecordByCode(programCode: str) -> Dict[str, str]:
    conn = getConnection()
    program = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM programs 
        WHERE program_code = %s
        ORDER BY program_code;
      """

      try:
        cursor.execute(query, (programCode,))

        program = cursor.fetchone()
      
      except Exception as e:
        print(f"Program Model Error fetching programs by code: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return program

  # Get program record by name
  @staticmethod
  def getProgramRecordsByName(programName: str) -> Dict[str, str]:
    conn = getConnection()
    program = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM programs 
        WHERE program_name = %s
        ORDER BY program_code;
      """

      try:
        cursor.execute(query, (programName,))

        program = cursor.fetchone()
      
      except Exception as e:
        print(f"Program Model Error fetching program by name: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return program
  
  # Get program record by college
  @staticmethod
  def getProgramRecordsByCollege(collegeCode: str) -> List[Dict[str, str]]:
    conn = getConnection()
    programs = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM programs 
        WHERE college_code = %s
        ORDER BY program_code;
      """

      try:
        cursor.execute(query, (collegeCode,))

        programs = cursor.fetchall()
      
      except Exception as e:
        print(f"Program Model Error fetching programs by college code: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return programs
  
  # Get program record
  @staticmethod
  def updateProgramRecordByCode(programCode: str, updateData: Dict[str, str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    setClause = ", ".join(f'{key} = %s' for key in updateData.keys())
    values = tuple(updateData.values()) + (programCode,)

    query = f"""
      UPDATE programs
      SET {setClause}
      WHERE program_code = %s;
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount >= 0

    except Exception as e:
      print(f"Program Model Error updating program: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Remove program from college
  @staticmethod
  def deleteProgramRecord(programCode: str) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    query = f"""
      DELETE FROM programs WHERE program_code = %s;
    """

    try:
      cursor.execute(query, (programCode,))
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Program Model Error deleting program: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Batch Removes program records
  @staticmethod
  def removeBatchProgramRecordsById(programCodes: List[str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    idNumberPlaceholders = ", ".join(["%s"] * len(programCodes))
    whereClause = f"WHERE program_code IN ({idNumberPlaceholders})"
    values = tuple(programCodes)

    query = f"""
      DELETE FROM programs
      {whereClause}
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Program Model Error batch deleting programs: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()