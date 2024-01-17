from RegDb import RegDb
from RegGuiCtk import RegGuiCtk

def main():
    db = RegDb(init=False, dbName='RegDb.csv')
    app = RegGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()