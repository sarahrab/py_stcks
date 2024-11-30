from urllib import parse

from sqlalchemy import create_engine
import  pyodbc

def mssql_engine(host = '(LocalDB)\MSSQLLocalDB' ,db = 'sara_try'):
    params = parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                     "SERVER=(LocalDB)\MSSQLLocalDB;"
                                     "DATABASE=sara_try;"
                                     "Trusted_Connection=yes")

    #engine = create_engine(f'mssql+pyodbc://{host}/{db}?driver=SQL+Server')
    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    return engine