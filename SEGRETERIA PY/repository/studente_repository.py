# Repository --> Unico punto di contatto con il database, qui scriviamo l'SQL (plain o con l'ORM)
# Rispetto al progetto precedente, non ho una persistenza "dummy/fake" ma avrò query reali

from model.studente import Studente
from persistence.db_configuration import get_connection

# Create
# L'oggetto viene dal Service (FE, CSV, Excel, Servizio REST esterno..)
def create(studente): 

    # Operatore with: 
    #   - Se tutto ok --> Commit automatico a database dei dati 
    #   - Se abbiamo errore dal database --> ROLLBACK automatico
    #   - Alla fine dell'esecuzione la connessione viene chiusa (deallocazione risorse)
    # as conn -> dalla get_connection abbiamo un oggetto connessione con cui possiamo lavorare
    with get_connection() as conn:

        # il cursore è un oggetto py che punta come una testina di un nastro alla riga corrente
        # Una query cosi è soggetto al SQL Injection
        #  VALUES (' """ + studente.nome + """', 'STU-0002', '04-05-2026');

        with conn.cursor() as cur: 

            #returing --> Mi da indietro i dati inseriti a DB, mi serve soprattutto per l'id visto che è autogenerato
            # tra la INSERT, VALUES e (studente.nome, studente.matricola,studente.data_iscrizione)
            # rapporto 1:1
            cur.execute(
                """INSERT INTO public.studenti(nome, matricola, data_iscrizione) 
                    VALUES (%s, %s, %s)
                    RETURNING id, nome, matricola, diplomato, data_iscrizione""", 
                (studente.nome, studente.matricola,studente.data_iscrizione)
            )

            # Prendo la riga dal risultato che torna dal db e l'assegno ad una variabile (ne ho una sola essendo ina inserte)
            row = cur.fetchone()

    return _row_to_studente(row)
    

# Update
# Posso passare l'oggetto creato nel service oppure elenco di attributi da aggiornare
# student_id lo passo a parte perchè potrei avere aggiornamento ANCHE dell'id
def update(old_studente_id, student_2_update): 
    with get_connection() as conn:
        with conn.cursor() as cur: 

            #creato_il se voglio visualizzarlo in maschera devo aggiungerlo
            cur.execute(
                """UPDATE public.studenti
                    SET id=%s, nome=%s, matricola=%s, diplomato=%s, data_iscrizione=%s 
                    WHERE id=%s
                    RETURNING id, nome, matricola, diplomato, data_iscrizione""", 
                (student_2_update.id, student_2_update.nome,  student_2_update.matricola,   student_2_update.diplomato,  student_2_update.data_iscrizione, old_studente_id))

            row = cur.fetchone()

            # Se scrivo condizione nel Service di check, non dovrei avere questa situazione
            if row is None: 
                return None

            return _row_to_studente(row)
        
    
# Delete by ID

# Delete ALL
def delete_all(): 
    with get_connection() as conn:
        with conn.cursor() as cur:
            # ALTER SEQUENCE --> Resetto anche la sequence per far ripartire id da 1 
            cur.execute("DELETE FROM public.studenti; ALTER SEQUENCE studenti_id_seq RESTART WITH 1; ")

def delete_by_id(studente_id): 
    with get_connection() as conn:
        with conn.cursor() as cur:
            # ALTER SEQUENCE --> Resetto anche la sequence per far ripartire id da 1 
            cur.execute("DELETE FROM public.studenti WHERE id = %s RETURNING id, nome, matricola, diplomato, data_iscrizione ", (studente_id,))

            row = cur.fetchone()

            if row is None:
                return None

            return _row_to_studente(row)

    

# Get All / Get by ID
def get_all(): 
    with get_connection() as conn:
         with conn.cursor() as cur: 
            # eventualmente aggiunere "creato_il"
            cur.execute("SELECT id, nome, matricola, diplomato, data_iscrizione FROM studenti")

            # fetchall() legge tutte le righe come liste di tuple
            rows = cur.fetchall()

            # itera su tutte le tuple lette dal database e ritorna una lista di oggetti (da _row_to_studente)
            return [_row_to_studente(row) for row in rows]
         
def get_by_id(studente_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, matricola, diplomato, data_iscrizione FROM studenti WHERE id = %s", (studente_id,))

            row = cur.fetchone()

            if row is None:
                return None

            return _row_to_studente(row)



# _row_to_student --> Metodo di appoggio per convertire SQL --> Oggetto Python
# Postgresql restituisce le righe dei record (row) come tuple, noi però lavoriamo con oggetti python (OOP)
def _row_to_studente(row): 

    # ordine del  RETURNING per row[i]
    # Devo passare da tupla ad oggetto Py usando il suo costruttore
    return Studente(id=row[0],
                            nome= row[1],
                            matricola= row[2],
                            diplomato= row[3],
                            data_iscrizione= row[4])

# UPDATE

# DELETE

# DELETE BY ID


# GET ALL


# GET BY ID

# _row_to_student --> metodo di appoggio per convertire SQL --> Oggetto Python

