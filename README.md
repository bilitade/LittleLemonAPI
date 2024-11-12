
# Little Lemon API - Django REST Framework Project

Welcome to the Little Lemon API! This is a hands-on project I completed as part of Meta’s “API” course, where I learned to build powerful RESTful APIs with Django REST Framework (DRF).

### Project Highlights

- **Role-Based Access Control**: Custom roles (Manager, Delivery Crew, Customer) with tailored permissions for each user group.
- **Dynamic Cart Management**: Smart cart system that updates item quantity and price for easy order management.
- **Flexible Search & Filtering**: Partial match search, supporting intuitive filtering across menu items.
- **JWT Authentication**: Secure, token-based login system using JWT and Djoser.
- **Testing Ready**: Configured for Insomnia/Postman testing with provided export file.

---

## Getting Started

### Prerequisites

- **Python** 3.x
- **pipenv** for dependency management
- **VS Code** (recommended for ease of setup)

### Setup Instructions

1. **Download and Extract**  
   Download the project files and extract them to a chosen directory.

2. **Open in VS Code**  
   Open the extracted project folder in Visual Studio Code.

3. **Open Terminal**  
   Navigate to **Terminal > New Terminal** in VS Code.

4. **Navigate to Project Directory**  
   ```bash
   cd littleLemonAPI
   ```

### Set Up Virtual Environment

- **Create the virtual environment**:
  ```bash
  python3 -m venv .venv
  ```
- **Activate the virtual environment**:
  - **Windows**:
    ```bash
    .venv\Scripts\activate
    ```
  - **Mac/Linux**:
    ```bash
    source .venv/bin/activate
    ```

### Install Pipenv and Dependencies

- **Install pipenv**:
  ```bash
  pip install pipenv
  ```
- **Install project dependencies**:
  ```bash
  pipenv install
  ```

### Run Django Commands

- **Create database migrations**:
  ```bash
  python manage.py makemigrations
  ```
- **Apply the migrations**:
  ```bash
  python manage.py migrate
  ```
- **Start the Django server**:
  ```bash
  python manage.py runserver
  ```

### View Project

Open a browser and navigate to [http://127.0.0.1:8000/api/menu-items](http://127.0.0.1:8000/api/menu-items) to view the project.

For easy API testing, import the provided Insomnia file (`Insomnia_2024-11-11.json`) into **Insomnia** or **Postman**.

### Admin Credentials

- **Username**: `bilitade`
- **Password**: `12345678`

---

This project was all about mastering API development fundamentals, from DRF basics to advanced features like JWT auth, search filtering, and API throttling. Excited to use these skills in real-world projects! 🎉
