import sqlite3
import os

# Datenbank initialisieren
DB_PATH = "zebra_printer.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS print_jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        file_path TEXT,
                        status TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"✅ Benutzer {username} wurde erfolgreich registriert.")
    except sqlite3.IntegrityError:
        print("⚠ Benutzername bereits vergeben!")
    conn.close()

# ❌ UNSICHERE LOGIN-FUNKTION (SQL-Injection möglich!)
def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ⚠ Sicherheitslücke: Unsichere SQL-Abfrage (kein Parameterbinding)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)  # ❌ SQL-Injection möglich!
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        print(f"✅ Login erfolgreich! Willkommen {username}.")
        return user[0]  # User-ID zurückgeben
    else:
        print("❌ Falscher Benutzername oder Passwort.")
        return None

def upload_zpl_file(user_id, filename, content):
    BASE_DIRECTORY = "C:\\ZebraLabels\\"
    
    # ⚠ Sicherheitslücke: Kein Dateiname-Check (Path Traversal möglich!)
    file_path = os.path.join(BASE_DIRECTORY, filename)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO print_jobs (user_id, file_path, status) VALUES (?, ?, 'pending')",
                   (user_id, file_path))
    conn.commit()
    conn.close()
    
    print(f"✅ Datei {filename} hochgeladen und Druckauftrag erstellt.")

def main():
    init_db()
    
    while True:
        print("\n1. Registrieren\n2. Login\n3. Datei hochladen\n4. Beenden")
        choice = input("Wähle eine Option: ")
        
        if choice == "1":
            username = input("Benutzername: ")
            password = input("Passwort: ")
            register_user(username, password)
        
        elif choice == "2":
            username = input("Benutzername: ")
            password = input("Passwort: ")
            user_id = login_user(username, password)
        
        elif choice == "3":
            if 'user_id' not in locals() or user_id is None:
                print("⚠ Bitte zuerst einloggen!")
                continue
            
            filename = input("Dateiname (.zpl): ")
            content = input("ZPL-Inhalt: ")
            upload_zpl_file(user_id, filename, content)
        
        elif choice == "4":
            print("Programm beendet.")
            break
        
        else:
            print("⚠ Ungültige Eingabe!")

if __name__ == "__main__":
    main()
