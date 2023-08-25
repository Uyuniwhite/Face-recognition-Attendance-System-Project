import psycopg2

host = "10.10.20.103"
port = "5432"
database = "ATD"
name = "postgres"
password = "1234"

class DBconnect:
    def __init__(self, controller):
        self.controller = controller
        self.conn = None

    def start_conn(self):
        self.conn = psycopg2.connect(host=host, database=database, user=name, password=password, port=port)
        cur = self.conn.cursor()

        return cur

    def end_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def log_in(self):
        c = self.start_conn()

    def regiseter_info(self):
        c = self.start_conn()



