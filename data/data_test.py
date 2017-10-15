import sqlite3

# Создаем курсор - это специальный объект который делает запросы и получает их результаты

class SqlBase:
    def __init__(self):
        self._list_hospitals = []
        self._conn = sqlite3.connect('E://День Донора/SAMI/data_test/DonorSpb_Sqlite.sqlite')
        self._cursor = self._conn.cursor()
        print(2)

    def fetchall_hospital(self):
        print(3)
        sql_statement = 'SELECT * FROM Hospital'
        self._cursor.execute(sql_statement)
        result = self._cursor.fetchall()
        self._list_hospitals = result
        

    def description_hospital(self, num): #param num of hospital
        if (num < len(self._list_hospitals)):
            print(self._list_hospitals[num][2])
        else:
            print("Error #1. Uncorrect value of num")

    def clode_connection(self):
        self._conn.close()

print(1)
x = SqlBase()
x.fetchall_hospital()
x.description_hospital(0)




