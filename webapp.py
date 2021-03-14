import psycopg2
import os
import json
from psycopg2 import Error
from flask import Flask, render_template

app = Flask(__name__)

def get_secret_file():
    #try to get the location from env variable, default is blank
    db_cred_location = os.environ.get('PY_DB_CRED_LOCATION', '')
    #credential file must be named secret
    #expecting user, and pass values in json
    filepath = db_cred_location + "secret"

    #secret file must be json
    file = open(filepath , "r")
    filecontent = json.load(file)
    return filecontent


def connect_to_db(filecontent):    
    #get these details from env when running in k8s vs local
    db_name = os.environ.get('PY_APP_DB_NAME', 'postgres')
    db_host = os.environ.get('PY_APP_DB_HOST', '127.0.0.1')
    db_port = os.environ.get('PY_APP_DB_PORT', '5432')

    db_username = filecontent["user"]
    db_password = filecontent["pass"]
    print("username: " + db_username)
    print("passwword: " + db_password)
    db_details = []
    db_details.append(db_username)
    db_details.append(db_password)
    db_details.append(db_name)

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=db_username,
                                      password=db_password,
                                      host=db_host,
                                      port=db_port,
                                      database=db_name)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        db_record = cursor.fetchone()
        print("You are connected to - ", db_record, "\n")
        db_details.append(db_record)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return db_details        

@app.route("/")
def home():
    secrets = get_secret_file()
    db_details = connect_to_db(secrets)
    return render_template("index.html", db=db_details)
    
if __name__ == "__main__":
    app.run(debug=True)        