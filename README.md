<h1>
  <img src="assets/LogoIcon.png" width="30" alt="Project Logo">
  Lexis - a Student Information System
</h1>

This project is developed in fulfillment of the requirements for the subject **CCC151 - Information Management Systems**.

<br></br>

## About This Project

**Lexis** is a student information system designed for efficient academic record management. Built with **Python**, **PyQt6**, and **MySQL**, it offers a streamlined user experience with **intuitive navigation**, **dynamic filtering**, and **bulk processing** for large datasets.

<br></br>

## **Features**
- **Comprehensive Record Management** – Store and manage Student, Program, and College records efficiently.

- **Full CRUD Support** – Easily Add, Edit, and Delete records with a user-friendly interface.

- **Advanced Search & Sorting** – Search by multiple fields and sort results dynamically.

- **Batch Operations** – Perform bulk updates and deletions for faster data management.

- **Intuitive UI with PyQt6** – Clean, responsive interface for seamless interaction.

- **MySQL Database Integration** – Ensures reliable and scalable data storage.

- **Unique ID System** – Prevents duplicate records and maintains data integrity.

- **Efficient Pagination** – Navigate large datasets smoothly without performance drops.

<br></br>

## **Added Updates**
- ✅ Refactor the table view to allow **multi-selection** of rows for **batch operations** (Batch deletions and edits)

## **Future Updates**
- 🔜 Add csv **importing** and **exporting**
- 🔜 Add **user authentication** and make operations **role-based**. (Admins can add new colleges, but regular users can only view, add, update, and delete student records.)
- 🔜Add a **dashboard** page to show program and college statistics and graphs

<br></br>

## **Setup Instructions**

### **1. Clone the Repository**

```sh
git clone https://github.com/gabnash05/CCC151-SSIS.git
cd CCC151-SSIS
```
### **2. Create and Activate a Virtual Environment**
- **Windows Command Prompt:**
  ```sh
  python -m venv ssis_env
  ```
- **Linux/macOS:**
  ```sh
  source venv/bin/activate
  ```
You’ll see (venv) appear in the terminal, indicating that you're inside the virtual environment.

### **3. Activate the Virtual Environment**

- **Windows Command Prompt:**
  ```sh
  ssis_env\Scripts\activate
  ```

- **Windows Powershell:**
  ```sh
  .\ssis_env\Scripts\Activate
  ```

- **Linux/macOS:**
  ```sh
  source ssis_env/bin/activate
  ```

### **4. Install Dependencies**

```sh
pip install -e .
```
This installs all required dependencies including PyQt6 and any other libraries listed in `requirements.txt`
___

<br></br>

## **Running the Project**

Make sure the virtual environment is activated and all dependencies were installed properly
```sh
python -m main
```
<br></br>

## **Deactivating the Virtual Environment**

When you're done working, deactivate the virtual environment:
```sh
deactivate
```

<br></br>

## **Troubleshooting**

If `pip install -e .` fails, try manually installing dependencies using:
```sh
pip install -r requirements.txt
```

If `pip install -r requirements.txt` fails, try updating `pip`:
```sh
pip install --upgrade pip
```

<br></br>

## **License**
This project is for educational purposes only.