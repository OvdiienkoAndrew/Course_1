import sqlite3

def creat_database(name_db):
    with sqlite3.connect(name_db) as db:
        cursor = db.cursor()

        РОБОЧА_ІНФОРМАЦІЯ = """
        CREATE TABLE IF NOT EXISTS РОБОЧА_ІНФОРМАЦІЯ (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            "посада" TEXT NOT NULL, 
            "вчене_звання_вчена_ступінь" TEXT
        )
        """

        ЛЮДСЬКА_ІНФОРМАЦІЯ = """
        CREATE TABLE IF NOT EXISTS ЛЮДСЬКА_ІНФОРМАЦІЯ (
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
            "ім'я" TEXT,
            "прізвище" TEXT,
            "по-батькові" TEXT,
            "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
            FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
        )
        """

        ІНФОРМАЦІЯ_ВАКАНСІЯ = """
        CREATE TABLE IF NOT EXISTS ІНФОРМАЦІЯ_ВАКАНСІЯ (
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
            "назва" TEXT,
            "номер" INTEGER,
            "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
            FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
        )
        """

        ПЕРШИЙ_СЕМЕСТР = """
        CREATE TABLE IF NOT EXISTS ПЕРШИЙ_СЕМЕСТР (
           id INTEGER PRIMARY KEY AUTOINCREMENT, 
            "ставка" REAL,
            "знак_сумісності" TEXT,
            "лекції" REAL,
            "практичні_(семінарські)_заняття" REAL,
            "лабораторні_роботи" REAL,
            "екзамени" REAL,
            "консультації_перед_екзаменами" REAL,
            "заліки" REAL,
            "кваліфікаційна_робота" REAL,
            "атестаційний_екзамен" REAL,
            "виробнича_практика" REAL,
            "навчальна_практика" REAL,
            "поточні_консультації" REAL,
            "індивідуальні" REAL,
            "курсові_роботи" REAL,
            "аспірантські_екзамени" REAL,
            "керівництво_аспірантами" REAL,
            "консультування_докторантів_здобувачів" REAL,
            "керівництво_ФПК" REAL,
            "робота_приймальної_комісії" REAL,
            "інше" REAL,
            "всього" REAL,
    
            "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
            FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
        )
        """

        ДРУГИЙ_СЕМЕСТР = """
           CREATE TABLE IF NOT EXISTS ДРУГИЙ_СЕМЕСТР (
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
               "ставка" REAL,
               "знак_сумісності" TEXT,
               "лекції" REAL,
               "практичні_(семінарські)_заняття" REAL,
               "лабораторні_роботи" REAL,
               "екзамени" REAL,
               "консультації_перед_екзаменами" REAL,
               "заліки" REAL,
               "кваліфікаційна_робота" REAL,
               "атестаційний_екзамен" REAL,
               "виробнича_практика" REAL,
               "навчальна_практика" REAL,
               "поточні_консультації" REAL,
               "індивідуальні" REAL,
               "курсові_роботи" REAL,
               "аспірантські_екзамени" REAL,
               "керівництво_аспірантами" REAL,
               "консультування_докторантів_здобувачів" REAL,
               "керівництво_ФПК" REAL,
               "робота_приймальної_комісії" REAL,
               "інше" REAL,
               "всього" REAL,
    
               "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
               FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
           )
           """

        АКАДЕМІЧНИЙ_РІК = """
              CREATE TABLE IF NOT EXISTS  АКАДЕМІЧНИЙ_РІК (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  "ставка" REAL,
                  "знак_сумісності" TEXT,
                  "лекції" REAL,
                  "практичні_(семінарські)_заняття" REAL,
                  "лабораторні_роботи" REAL,
                  "екзамени" REAL,
                  "консультації_перед_екзаменами" REAL,
                  "заліки" REAL,
                  "кваліфікаційна_робота" REAL,
                  "атестаційний_екзамен" REAL,
                  "виробнича_практика" REAL,
                  "навчальна_практика" REAL,
                  "поточні_консультації" REAL,
                  "індивідуальні" REAL,
                  "курсові_роботи" REAL,
                  "аспірантські_екзамени" REAL,
                  "керівництво_аспірантами" REAL,
                  "консультування_докторантів_здобувачів" REAL,
                  "керівництво_ФПК" REAL,
                  "робота_приймальної_комісії" REAL,
                  "інше" REAL,
                  "всього" REAL,
                  "розподіл_ставок_навчального_навантаження" TEXT,
    
                  "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
                  FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
              )
              """
        КОД_РІК = """
            CREATE TABLE IF NOT EXISTS  КОД_РІК (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "назва_кафедри" TEXT,
                "роки" TEXT,
                "посилання_на_РОБОЧУ_ІНФОРМАЦІЮ" INTEGER NOT NULL,
    
                FOREIGN KEY ("посилання_на_РОБОЧУ_ІНФОРМАЦІЮ") REFERENCES РОБОЧА_ІНФОРМАЦІЯ (id) ON DELETE CASCADE
            )
             """
        ПЕРЕВІРКА = """
                   CREATE TABLE IF NOT EXISTS  ПЕРЕВІРКА (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       "прізвище" TEXT,
                       "ім'я" TEXT,
                       "по-батькові" TEXT,
                       "ставка" REAL,
                       "знак_сумісності" TEXT,
                       "загальна_кількость_годин" REAL,
                       "мінімум" INTEGER,
                       "максимум" INTEGER,
                       "загальний_мінімум" INTEGER,
                       "загальний_максимум" INTEGER
                   )
                    """
        ПЕРЕВІРКА_АСИСТЕНТ_СТ_ВИКЛАДАЧ = """
                   CREATE TABLE IF NOT EXISTS  ПЕРЕВІРКА_АСИСТЕНТ_СТ_ВИКЛАДАЧ (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       "прізвище" TEXT,
                       "ім'я" TEXT,
                       "по-батькові" TEXT,
                       
                       "кафедра" INTEGER,
                       "роки" INTEGER,
                       "помилка" INTEGER
                   )
                    """
        
        cursor.execute(РОБОЧА_ІНФОРМАЦІЯ)
        cursor.execute(ЛЮДСЬКА_ІНФОРМАЦІЯ)
        cursor.execute(ІНФОРМАЦІЯ_ВАКАНСІЯ)
        cursor.execute(ПЕРШИЙ_СЕМЕСТР)
        cursor.execute(ДРУГИЙ_СЕМЕСТР)
        cursor.execute(АКАДЕМІЧНИЙ_РІК)
        cursor.execute(КОД_РІК)
        cursor.execute(ПЕРЕВІРКА)
        cursor.execute(ПЕРЕВІРКА_АСИСТЕНТ_СТ_ВИКЛАДАЧ)

        db.commit()