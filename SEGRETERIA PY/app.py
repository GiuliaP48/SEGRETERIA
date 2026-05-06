# Script per usare le CRUD che andiamo a scrivere
# In un contesto reale, le CRUD delle repository vanno usate tramite Service (ed eventualmente Controller)

from model.studente import Studente
from repository import studente_repository
from datetime import date

print("****** DELETE *****")
studente_repository.delete_all() # Pulisco il DB all'avvio: DIDATTICO!!!!

print("****** CREATE *****")

s1 = Studente(None, "Nome Studente 1", "STU-0101", False, date(2026, 5,4))
s2 = Studente(None, "Nome Studente 2", "STU-0102", False, date(2026, 4,4))
s3 = Studente(None, "Nome Studente 3", "STU-0103", False, date(2026, 3,4))

# Voglio aggiornare i valori di s con i dati che mi vengono dal database (id, creato_il..)
s1 = studente_repository.create(s1) 
s2 = studente_repository.create(s2) 
s3 = studente_repository.create(s3) 

print("****** READ ALL *****")

for s in studente_repository.get_all(): 
    print(s)

s3.nome = "Nome Studente S3 AGGIORNATO"
s3 = studente_repository.update(s3.id, s3); 
print(s3)

print(studente_repository.get_by_id("2"))
print(studente_repository.delete_by_id("3"))