
from flask_sqlalchemy import SQLAlchemy
from .config import Setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine




conf = Setting()



write_connection_string = conf.createSqlWriteConnetionLink("PSQL")
if write_connection_string: 
	WriteSession = sessionmaker()
	write_engine = create_engine(write_connection_string)
	WriteSession.configure(bind=write_engine)


read_connection_string = conf.createSqlReadConnetionLink("PSQL")
if read_connection_string:
	ReadSession = sessionmaker()
	read_engine = create_engine(read_connection_string)
	ReadSession.configure(bind=read_engine)


# mysql://scott:tiger@localhost/mydatabase

# print("write_connection_string: ", write_connection_string)
# print("read_connection_string: ", read_connection_string)

db = SQLAlchemy()