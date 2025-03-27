import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db import getConnection

def migrateStudents():
  conn = getConnection()
  print("database connected!")
  cursor = conn.cursor()

  try:
    with open("data/students.csv", "r", encoding="utf-8") as file:
      reader = csv.reader(file)
      next(reader)

      for row in reader:
        idNumber, firstName, lastName, yearLevel, gender, programCode = row
        
        if gender == "Others":
          gender = "Other"

        cursor.execute("""
          INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
          VALUES (%s, %s, %s, %s, %s, %s)
        """, (idNumber, firstName, lastName, int(yearLevel), gender, programCode))
        print((idNumber, firstName, lastName, int(yearLevel), gender, programCode))

      conn.commit()
      
  except Exception as e:
    print(f"Error: {e}")
  finally:
    cursor.close()
    conn.close()

  print("Students migration done!")

def migratePrograms():
  conn = getConnection()
  print("database connected!")
  cursor = conn.cursor()

  try:
    with open("data/programs.csv", "r", encoding="utf-8") as file:
      reader = csv.reader(file)
      next(reader)

      for row in reader:
        programCode, programName, collegeCode = row
        cursor.execute("""
          INSERT INTO programs (program_code, program_name, college_code)
          VALUES (%s, %s, %s)
        """, (programCode, programName, collegeCode))
        print((programCode, programName, collegeCode))

      conn.commit()
  except Exception as e:
    print(f"Error: {e}")
  finally:
    cursor.close()
    conn.close()

  print("Programs migration done!")


if __name__ == "__main__":
  migrateStudents()