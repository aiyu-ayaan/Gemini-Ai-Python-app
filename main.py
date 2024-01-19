from database.Database import Database
from screens.MainScreen import MainScreen

if __name__ == '__main__':
    main = MainScreen(database=Database())
    main.mainloop()
