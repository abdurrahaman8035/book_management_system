# Book Management System for Tertiary Institutions

This is a Book Management System designed for tertiary institutions to manage their book inventory, student records, and book borrowing process.

## Features
- Manage student profiles
- Track book inventory
- Borrow and return books
- Generate reports
- Search functionality

## Installation
Follow the steps below to install and run the project locally.

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Create a virtual environment:
   ```
   python -m venv env
   ```
3. Activate the virtual environment:
   - For Windows:
     ```
     .\env\Scripts\activate
     ```
   - For macOS/Linux:
     ```
     source env/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up the database:
   ```
   python manage.py migrate
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```
7. Access the application at http://localhost:8000

## Usage
- Register as a student or staff member
- Log in with your credentials
- Explore the available features and functionalities
- Manage student profiles, book inventory, and borrowing process
- Generate reports and search for specific books or users

## Contributing
Contributions are welcome! To contribute to the project, follow these steps:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License
This project is licensed under the MIT License LICENSE.
```