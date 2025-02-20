import sqlite3

db_name = input("Write the name Workout: ")

if not db_name.endswith('.sqlite'):
    db_name += '.sqlite'

conn = sqlite3.connect(db_name)
cur = conn.cursor()

try:
    cur.executescript('''
    DROP TABLE IF EXISTS Allenamento;
    DROP TABLE IF EXISTS Ripetizioni;
    DROP TABLE IF EXISTS Recupero;

    CREATE TABLE Allenamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        
    );

    CREATE TABLE "Ripetizioni" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ripetizioni INTEGER NOT NULL,
        id_allenamento INTEGER,
        FOREIGN KEY(id_allenamento) REFERENCES Allenamento(id)
    );

    CREATE TABLE "Recupero" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recupero INTEGER NOT NULL,
        id_allenamento INTEGER,
        FOREIGN KEY(id_allenamento) REFERENCES Allenamento(id)
    );
    ''')
    print("Creazione Tabella")

except sqlite3.OperationalError as e:
    print("Errore creazione tabella", e)

while True:
    nome = input("Inserisci il nome dell'esercizio (o digita 'fine' per terminare): ")

    if nome.lower() == 'fine':  # Se l'utente digita "fine", interrompiamo il ciclo
        break

    # Aggiungiamo il tempo di recupero
    try:
        esecuzioni = input(f"Inserisci il numero di ripetizioni per '{nome}' (es. 7*3): ")
        parte1, parte2 = esecuzioni.split('*')
        ripetizioni = int(parte2)
        recupero = int(input(f"Inserisci il tempo di recupero per '{nome}' (in secondi): "))
    except ValueError:
        print(
            "Errore: il formato della ripetizione deve essere corretto (es. 7*3) e il tempo di recupero deve essere un numero intero.")
        continue

    # inserire allenamento
    cur.execute('''INSERT INTO Allenamento (nome) VALUES (?)''', (nome,))
    conn.commit()

    allenamento_id = cur.lastrowid

    # inserire ripetizioni
    cur.execute('''INSERT INTO Ripetizioni (ripetizioni, id_allenamento) VALUES (?, ?)''', (ripetizioni, allenamento_id))
    conn.commit()

    ripetizioni_id = cur.lastrowid

    # inserire recupero
    cur.execute('''INSERT INTO Recupero (recupero, id_allenamento) VALUES (?, ?)''', (recupero, allenamento_id))
    conn.commit()

    recupero_id = cur.lastrowid

    print(
        f"Allenamento '{nome}' inserito con ID {allenamento_id}, ripetizioni {ripetizioni} con ID {ripetizioni_id}, recupero {recupero} secondi con ID {recupero_id}.")

conn.close()