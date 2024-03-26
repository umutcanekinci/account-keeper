#-# Import Packages #-#
from sqlite3 import connect
from os import path, makedirs, remove

#-# Database Class #-#
class Database():

    def __init__(self, name='database') -> None:

        self.name = name
        self.path = "databases/" + self.name + ".db"

    def Connect(self) -> bool:
        
        try:
        
            if not path.exists('databases/'):

                makedirs('databases/')

            self.connection = connect((self.path)) 

        except Exception as error:
            
            print("==> Failed to connect to database!", error)

            return False
        
        else:

            return True
        
    def GetCursor(self) -> None:

        return self.connection.cursor()
    
    def Execute(self, sql, *paramaters) -> any:
        
        try:
            
            return self.GetCursor().execute(sql, paramaters)
            
        except Exception as error:

            print("An error occured during execute sql code:", error)
            
            return None

    def Commit(self) -> None:

        self.connection.commit()

    def Disconnect(self) -> None:

        self.connection.close()

    def Delete(self) -> None:

        self.Disconnect()
        remove(self.path)
        self.Connect()