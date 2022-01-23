
<h1>Currency-Exchange-Rate</h1>

A web service which has a single GET endpoint /rate
The API endpoint requires the following GET query parameters:
- From currency
- To currency
- date

And responds with the exchange rate between the two currencies on that particular date.
The source of the currency exchange data is an external public API, however in order to
minimize the requests we make to that external API, each result we retrieve from the external
API needs to be stored in a local database and upon every request we receive at the /rate
endpoints we need to check if the data is available first in our database before requesting the
data from the external API.

<h2>To run locally, do the usual:</h2>

1- Install pipenv<br>
    pip install pipenv
    
2- Activate the venv<br>
    pipenv shell
    
3- Install the dependencies<br>
    pipenv install
    
4- Create databse in mysql
    mysql -u root -p
    mysql>CREATE DATABASE exchange_rate;
    
5- Update MySql configuration<br>
    update in file my.cnf
    
6- Run Migrations<br>
    python manage.py migrate
    
7- Get Currencies data and rates from 2020-01-01 to 2020-01-31<br>
    python manage.py seed --mode=refresh
    
8- Start the django server<br>
    python manage.py runserver
    

