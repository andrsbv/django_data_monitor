# backend_analytics_server/__init__.py
try:
    import MySQLdb  # mysqlclient (binario)
except ModuleNotFoundError:
    import pymysql
    pymysql.install_as_MySQLdb()
