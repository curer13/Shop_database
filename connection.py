import pyodbc as po

# Connection variables
server = 'localhost'
database = 'market'
username = 'sa'
password = 'Abz09jvv1'

# Connection string
cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                  server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
