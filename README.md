# Income-Expenses-Dashboard
This Dashboard is built to manage your expenses and income and to use your income carefully. It's built using HTML, CSS, Python, JavaScript. 
Using this dashboard your can add your expenses, read them edit them and also delete them. For adding of expenses you need to input it's description, date, category.
Same goes with Income also. You can set your preferred currency and change on changing your station. 
You can visualise your income and expenses and look on which category you spent how much. 
You can even get your expenses exported to your local system as .csv or .xls based upon your clicking of buttons. 

# Collaborators 
- [Shrutayu Aggarwal](https://github.com/Shrut26)
- [Sanidhya S. Johri](https://github.com/UnstoppableVenom)

- This is a seperate branch. The main repo link- [link](https://github.com/Shrut26/Income-Expenses-Dashboard)

To run on Localhost follow the below steps<br>

<strong>Installations:</strong>
- Download [python](https://www.python.org/downloads/) and set up this with your local system
- Download [Postman](https://subscription.packtpub.com/book/web_development/9781838983994/1/ch01lvl1sec13/postman)
- Download [PostgreSQL](https://www.pgadmin.org/) and follow the below steps.
   - make a Database and name it as incomeexpensesdb
   - git clone this repo and edit the .env file.
   - Mention this 4 lines of code
      - export DB_USER_PASSWORD =                # Your database password
      - export EMAIL_HOST_PASSWORD =             # your email id password with which you will be sending mails
      - export EMAIL_HOST_USER =  ''               # your email id (mention instead quotes)
      - export DEFAULT_FROM_EMAIL = ''             # your email id (mention instead quotes)

- Go to Authentication.views.py -> Go to line number 84 and 184 and enter your email address  


<strong>Procedure to run on local Host:</strong>

- Navigate to the clone repository 
   ```
    cd <repository name>       
   ```

- Create a new virtual environment:
   ```
   py -3 -m venv {folder name}
   ```
   
- Activate the environment and enter the next command: 

   ```
   .env\Scripts\activate
   ```
   
- Make Database migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   ```
   code .
   ```

- Open new Terminal and run the following Command:

   ```
   pipenv runshell
   ```
   
- Install the following dependencies:
   - [Django](https://www.djangoproject.com/download/)
   - [xlwt](https://pypi.org/project/xlwt/)
   - [re](https://pypi.org/project/regex/)
   - [email](https://docs.python.org/3/library/email.examples.html)
   - [Django Heroku](https://devcenter.heroku.com/articles/django-app-configuration)
   
- For Windows User, Install following dependencies:
   - [Python Waitress](https://pypi.org/project/waitress/)
- For Mac User, Install following dependencies:
   - [Gunicorn](https://gunicorn.org/)

- Run the server:
   ```
   python manage.py runserver
   ```
