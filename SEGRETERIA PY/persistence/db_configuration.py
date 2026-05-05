# Modulo id utility per la connessione al database di PostgreSQL, centralizza la configurazione 
# in un solo punto del progetto (che abbiamo messo su pgAdmin)
import psycopg2

# PREREQUISITI: 
#   1 - Postgresql attivo su endpoint localhost:5432
#   2 - Script DDL eseguito
#   3 - pip install psycopg2-binary

# La password non dovrebbe MAI essere committata/scritta nel progetto :)
# Questa configurazione in un progetto reale andrebbe in un file .env non committato
DB_CONFIG = {"host": "127.0.0.1", 
                       "port":5432, 
                       "dbname":"Segreteria", 
                       "user":"postgres", 
                       "password":"postgres8"}

# Metodo che apre la connessione al Database
# L'operatore ** si applica ai dizionari e si chiama "dictionary unpacking"
# Sarebbe equivalente a scrivere (host="", port=5432..)
def get_connection():
    return psycopg2.connect(**DB_CONFIG)