# Income-Expenses-Dashboard
This Dashboard is built to manage your expenses and income and to use your income carefully. It's built using HTML, CSS, Python, JavaScript. 
Using this dashboard your can add your expenses, read them edit them and also delete them. For adding of expenses you need to input it's description, date, category.
Same goes with Income also. You can set your preferred currency and change on changing your station. 
You can visualise your income and expenses and look on which category you spent how much. 
You can even get your expenses exported to your local system as .csv or .xls based upon your clicking of buttons. 

To run on Local machine follow the below steps<br>

<strong>Installations:</strong>
- Download [python](https://www.python.org/downloads/) and set up this with your local system
- Download [PostgreSQL](https://www.pgadmin.org/) and follow the below steps.
   - make a Database and name it as incomeexpensesdb
   - git clone this repo and edit the .env file.
   - Mention this 4 lines of code
      - export DB_USER_PASSWORD =                # Your database password
      - export EMAIL_HOST_PASSWORD =             # your email id password with which you will be sending mails
      - export EMAIL_HOST_USER =  ''               # your email id (mention instead quotes)
      - export DEFAULT_FROM_EMAIL = ''             # your email id (mention instead quotes)
