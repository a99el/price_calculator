# Price Calculator

## Installation Instructions

### 1. Install Git

Ensure that Git is installed on your system. You can download and install it from [git-scm.com](https://git-scm.com/).

### 2. Clone the Repository

Open a terminal or command prompt and navigate to the directory where you want to clone the repository. Then run the following command:

### 1. After cloning, navigate into the project directory:

cd repository

### 2. Set Up a Virtual Environment (Optional but Recommended):

pip install virtualenv

### 3. Create and activate a virtual environment:

# For Windows

1. python -m venv venv

2. venv\Scripts\activate

# For macOS/Linux
1. python3 -m venv venv
2. source venv/bin/activate

### 4. Install Project Dependencies:

pip install -r requirements.txt

### 5. Apply Migrations:

1. python manage.py makemigrations
2. python manage.py migrate

### 6. Run the Development Server:

python manage.py runserver

