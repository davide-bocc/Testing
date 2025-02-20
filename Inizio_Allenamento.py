import sqlite3
import time
from colorama import Fore, init
import sys
import winsound
init()


def countdown_timer(duration):
    for remaining in range(duration, 0, -1):
        sys.stdout.write(f'\rTempo di recupero: {remaining} secondi restanti')
        sys.stdout.flush()
        time.sleep(1)
    print("\nRecupero terminato!")
    for _ in range(4):
        winsound.Beep(1000, 250)
        time.sleep(0.5)

db_name = input("Write the name Workout: ")

if not db_name.endswith('.sqlite'):
    db_name += '.sqlite'

conn = sqlite3.connect(db_name)
cur = conn.cursor()

# Verifica se le tabelle esistono
try:
    cur.execute('''SELECT name FROM sqlite_master WHERE type="table";''')
    tables = cur.fetchall()
    table_names = [table[0] for table in tables]
    print(f"Tabelle nel database: {table_names}")
    print(f"database {db_name} esistente")
    # Verifica che tutte le tabelle siano presenti
    required_tables = ['Allenamento', 'Ripetizioni', 'Recupero']

    if not all(table in table_names for table in required_tables):
        print(
            f"Errore: una o più tabelle necessarie ({', '.join(required_tables)}) non esistono nel database '{db_name}'.")
        sys.exit()
except sqlite3.Error as e:
    print(f"Errore nella verifica delle tabelle: {e}")
    sys.exit()

# Esegui la query per ottenere i dati
try:
    print("Eseguendo la query per ottenere i dati...")
    cur.execute("SELECT * FROM Allenamento")
    allenamenti = cur.fetchall()

    cur.execute("SELECT * FROM Ripetizioni")
    ripetizioni = cur.fetchall()

    cur.execute("SELECT * FROM Recupero")
    recuper = cur.fetchall()

    # Verifica le associazioni tra le tabelle
    cur.execute('SELECT A.id, R.id_allenamento, Re.id_allenamento '
                'FROM Allenamento A '
                'JOIN Ripetizioni R ON A.id = R.id_allenamento '
                'JOIN Recupero Re ON A.id = Re.id_allenamento')
    data = cur.fetchall()
    print("Dati di debug sulle associazioni:", data)


    cur.execute('''
        SELECT A.nome, R.ripetizioni, Re.recupero 
        FROM Allenamento A
        JOIN Ripetizioni R ON A.id = R.id_allenamento
        JOIN Recupero Re ON A.id = Re.id_allenamento
    ''')

    esercizio = cur.fetchall()

    print(f"Dati recuperati: {esercizio}")

    if not esercizio:
        print("Nessun esercizio trovato")

except sqlite3.Error as e:
    print(f"Errore nell'esecuzione della query: {e}")
    conn.close()
    sys.exit()


for esercizio in esercizio:
    nome, ripetizioni, recupero = esercizio
    count = 0
    total_reps = ripetizioni
    print(f"Inizia l'esercizio: {nome}")

    # Ciclo per il conteggio delle ripetizioni dell'esercizio corrente
    while count < int(total_reps):
        rep = input(Fore.GREEN + "Premi ENTER quando completi una ripetizione: ")
        if not rep:
            count += 1
            print(Fore.CYAN + f"Ripetizione {count}/{total_reps} completata.")
            print(f"\nTempo di recupero di {recupero} secondi")
            countdown_timer(int(recupero))
        else:
            print(Fore.RED + "Rifare. Premi solo ENTER.")

    print(Fore.MAGENTA + f"Esercizio {nome} completato!")
    print("\nPassando al prossimo esercizio...\n")

conn.close()