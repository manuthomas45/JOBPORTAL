# Job Portal

This is a Django web application for job seekers and employers to connect. The application allows job seekers to search for job listings and apply to them, while employers can post job listings and review applications.

# Features

# 1. company Features:
      -Registration and login
      -create company profile and edit profile
      -post job listing with description
      -Review job applications and send mail to candidate about the status of application.
# 2. candidate Features:
     -registration and login
     -create candidate profile and edit profile
     -search for job 
     -apply for desired jobs
     -obtain mail from the company about status of application


#  Installation

- To run the application on your local machine,follow these steps:
   - Clone the project: Start by cloning the project repository from a version control system like Git. Use the following command to clone the repository to your local machine.
      - ` git clone <repository-url>`
   - Create a virtual environment (optional): It is recommended to create a virtual environment for the project to keep the dependencies isolated. Navigate to the project directory and create a virtual environment using the following command.
      - ` python -m virtualenv venv `
    - activate the virtual environment (optional): Activate the virtual environment you created in the previous step. The command may vary depending on your operating system,For Windows:
      - `venv\Scripts\activate.bat`
    - Install dependencies: With the virtual environment activated, install the project dependencies.
       - `pip install django`
    - Perform database migrations: Django uses database migrations to create the necessary database tables based on your project's models. Run the following command to apply the migrations.
      - `python manage.py migrate`
     - Perform database migrations: Django uses database migrations to create the necessary database tables based on your project's models. Run the following command to apply the migrations.
       - `python manage.py runserver`
    - Access the project: Open a web browser and visit http://localhost:8000 to access the Django project. You should see the default Django landing page if everything is set up correctly.
    

    


    
 


