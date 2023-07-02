# Deployment Guide

Follow the steps below to deploy the Book Management System to a deployment platform (e.g., Heroku, AWS, etc.).

## Prerequisites
- Account on a deployment platform (e.g., Heroku, AWS)
- PostgreSQL database (either provided by the platform or a separate database service)

## Deployment Steps (Heroku)
1. Create a new app on Heroku
2. Set up the PostgreSQL database on Heroku
3. Clone the repository locally:
   ```
   git clone https://github.com/abdurrahaman8035/book_management_system.git
   ```
4. Create a new branch for deployment:
   ```
   git checkout -b deployment
   ```
5. Create a Heroku configuration file:
   ```
   touch Procfile
   ```
6. Add the following content to the Procfile:
   ```
   web: gunicorn book_management_system.wsgi
   ```
7. Commit and push the changes to the deployment branch:
   ```
   git add .
   git commit -m "Prepare for deployment"
   git push heroku deployment:main
   ```
8. Set the necessary environment variables on Heroku:
   - SECRET_KEY: your_secret_key
   - DEBUG: False
   - DATABASE_URL: your_database_url
9. Scale the Heroku dynos (if needed)
10. Run the database migrations:
    ```
    heroku run python manage.py migrate
    ```
11. Access the application using the provided Heroku URL

## Troubleshooting
- If you encounter any issues during the deployment process, please refer to the deployment platform's documentation or seek help from their support team.