from typing import List, Dict, Tuple, Any
from pathlib import Path

from database.db import getConnection

class Student:  
  STUDENT_CSV_FILEPATH = Path(__file__).parent.parent.parent / "data" / "students.csv"
  STUDENT_HEADERS = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code", "College Code"]

  def __init__(self, idNumber: str, firstName: str, lastName: str, yearLevel: int, gender: str, programCode: str, collegeCode: str):
    self.idNumber = idNumber
    self.firstName = firstName
    self.lastName = lastName
    self.yearLevel = str(yearLevel)
    self.gender = gender
    self.programCode = programCode
    self.collegeCode = collegeCode

  def toDict(self) -> None:
    return {
      "ID Number": self.idNumber,
      "First Name": self.firstName,
      "Last Name": self.lastName,
      "Year Level": self.yearLevel,
      "Gender": self.gender,
      "Program Code": self.programCode,
    }
  
  # Checks if a ID number already exists
  @staticmethod
  def idNumberExists(idNumber: str) -> bool:
    conn = getConnection()
      
    if not conn:
      return False 

    try:
      cursor = conn.cursor()

      query = "SELECT 1 FROM students WHERE id_number = %s LIMIT 1;"
      cursor.execute(query, (idNumber,))

      return cursor.fetchone() is not None

    except Exception as e:
      print(f"Student Model Error checking if ID number exists: {e}")
      return False

    finally:
      cursor.close()
      conn.close()
  
  # Adds a new student record
  @staticmethod
  def addStudentRecord(student: Any) -> bool:
    conn = getConnection()

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
        VALUES (%s, %s, %s, %s, %s, %s);
      """
      newStudent = student.toDict()

      try:
        cursor.execute(query, (newStudent["ID Number"], newStudent["First Name"], newStudent["Last Name"], newStudent["Year Level"], newStudent["Gender"], newStudent["Program Code"]))
        conn.commit()

        return cursor.rowcount > 0
      
      except Exception as e:
        print(f"Student Model Error inserting student: {e}")
        return False
      finally:
        cursor.close()
        conn.close()
  
  # Gets a student record
  @staticmethod
  def getStudentRecord(studentId: str) -> Dict[str, str]:
    conn = getConnection()
    student = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT * FROM students WHERE id_number = %s;
      """

      try:
        cursor.execute(query, (studentId,))

        student = cursor.fetchone()
      
      except Exception as e:
        print(f"Student Model Error fetching student by ID number: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return student
  
  # Get student records with page, search value, and sorting order
  @staticmethod
  def getStudentRecords(page=1, perPage=50, sortBy1="id_number", sortBy2="last_name", sortOrder="ASC", searchField=None, searchTerm="") -> Tuple[List[Dict[str, str]], int]:
    conn = getConnection()

    if not conn:
      return [], 0
    
    cursor = conn.cursor(dictionary=True)
    
    params = []
    programs = []
    offset = (page - 1) * perPage
    searchTerms = searchTerm.split()
    searchQuery = "WHERE ("

    if searchField:
      searchQuery += f"s.{searchField} LIKE %s" if searchField != "college_code" else f"c.{searchField} LIKE %s"
      params.append(f"%{searchTerm}%")
    else:
      searchQuery += """
        s.id_number LIKE %s 
        OR s.first_name LIKE %s
        OR s.last_name LIKE %s
        OR s.year_level LIKE %s
        OR s.gender LIKE %s
        OR s.program_code LIKE %s
        OR c.college_code LIKE %s
        OR CONCAT(s.first_name, ' ', s.last_name) LIKE %s
      """
      params.extend([f"%{searchTerm}%"] * 8)

    searchQuery += ")"

    # Query to get the total count of matching records
    countQuery = f"""
      SELECT COUNT(*) as total 
      FROM students s 
      LEFT JOIN programs p ON s.program_code = p.program_code
      LEFT JOIN colleges c ON p.college_code = c.college_code
      {searchQuery}
    """

    try:
      cursor.execute(countQuery, params)
      totalRecords = cursor.fetchone()["total"]
    except Exception as e:
      print(f"Student Model Error fetching student count: {e}")
      totalRecords = 0

    query = f"""
      SELECT s.*, c.college_code 
      FROM students s 
      LEFT JOIN programs p ON s.program_code = p.program_code
      LEFT JOIN colleges c ON p.college_code = c.college_code
      {searchQuery}
      ORDER BY {sortBy1} {sortOrder}, {sortBy2} ASC
      LIMIT %s OFFSET %s
    """

    params.extend([perPage, offset])

    try:
      cursor.execute(query, params)
      programs = cursor.fetchall()
    except Exception as e:
      print(f"Student Model Error fetching students: {e}")
    finally:
      cursor.close()
      conn.close()
    
    return programs, totalRecords

  # Get all student records by first name
  @staticmethod
  def getAllStudentRecordsByFirstName(firstName: str) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.*, c.college_code 
        FROM students s 
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE first_name = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (firstName,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by first name: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students
  
  # Get all student records by last name
  @staticmethod
  def getAllStudentRecordsByLastName(lastName: str) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.*, c.college_code 
        FROM students s 
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE last_name = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (lastName,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by last name: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students
  
  # Get all student records by year level
  @staticmethod
  def getAllStudentRecordsByYearLevel(yearLevel: int) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.*, c.college_code 
        FROM students s 
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE year_level = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (yearLevel,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by year level: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students

  # Get all student records by gender
  @staticmethod
  def getAllStudentRecordsByGender(gender: str) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.*, c.college_code 
        FROM students s 
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE gender = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (gender,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by gender: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students

  # Get all student records by program code
  @staticmethod
  def getAllStudentRecordsByProgram(program: str) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.*, c.college_code 
        FROM students s 
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE program_code = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (program,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by program code: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students

  # Get all student records by college
  @staticmethod
  def getAllStudentRecordsByCollege(college: str) -> List[Dict[str, str]]:
    conn = getConnection()
    students = None

    if conn:
      cursor = conn.cursor(dictionary=True)
      query = """
        SELECT s.id_number, s.first_name, s.last_name, s.year_level, s.gender p.program_code, c.college_code
        FROM students s
        LEFT JOIN programs p ON s.program_code = p.program_code
        LEFT JOIN colleges c ON p.college_code = c.college_code
        WHERE c.college_code = %s
        ORDER BY id_number;
      """

      try:
        cursor.execute(query, (college,))

        students = cursor.fetchall()
      
      except Exception as e:
        print(f"Student Model Error fetching students by college code: {e}")
      finally:
        cursor.close()
        conn.close()
    
    return students
  
  # Updates student information
  @staticmethod
  def updateStudentRecordById(studentId: str, updateData: Dict[str, str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    setClause = ", ".join(f'{key} = %s' for key in updateData.keys())
    values = tuple(updateData.values()) + (studentId,)

    query = f"""
      UPDATE students
      SET {setClause}
      WHERE id_number = %s;
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount >= 0

    except Exception as e:
      print(f"Student Model Error updating student: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()
  
  # Batch updates student information
  @staticmethod
  def updateBatchStudentRecordsById(studentIds: List[str], updateData: Dict[str, str]) -> bool:
    conn = getConnection()
    
    if not studentIds:
      return False
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    setClause = ", ".join(f'{key} = %s' for key in updateData.keys())
    values = tuple(updateData.values())

    idNumberPlaceholders = ", ".join(["%s"] * len(studentIds))
    whereClause = f"WHERE id_number IN ({idNumberPlaceholders})"
    values += tuple(studentIds)

    query = f"""
      UPDATE students
      SET {setClause}
      {whereClause}
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount >= 0

    except Exception as e:
      print(f"Student Model Error batch updating students: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()

  # Removes a student record
  @staticmethod
  def removeStudentRecordById(studentId: str) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    query = f"""
      DELETE FROM students WHERE id_number = %s;
    """

    try:
      cursor.execute(query, (studentId,))
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Student Model Error deleting student: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()

  # Batch Removes a student record
  @staticmethod
  def removeBatchStudentRecordsById(studentIds: List[str]) -> bool:
    conn = getConnection()
    
    if not conn:
      return False
    
    cursor = conn.cursor(dictionary=True)

    idNumberPlaceholders = ", ".join(["%s"] * len(studentIds))
    whereClause = f"WHERE id_number IN ({idNumberPlaceholders})"
    values = tuple(studentIds)

    query = f"""
      DELETE FROM students 
      {whereClause}
    """

    try:
      cursor.execute(query, values)
      conn.commit()

      return cursor.rowcount > 0

    except Exception as e:
      print(f"Student Model Error batch deleting students: {e}")
      return False
    
    finally:
      cursor.close()
      conn.close()