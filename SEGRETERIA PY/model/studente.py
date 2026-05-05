# Modello che mappa la tabella 1:1 (potrei non inserire i campi come 
# created_at, updated_at..)

class Studente: 

    def __init__(self, id, nome, matricola, diplomato, data_iscrizione): 
        self.id = id 
        self.nome = nome
        self.matricola = matricola
        self.diplomato = diplomato 
        self.data_iscrizione = data_iscrizione
        # Eventualmente anche il creato_il

    def __repr__(self): 
       return f"[Student]: id: {self.id} matricola:{self.matricola} nome: {self.nome}"

    def __str__(self): 
       return f"[Student]: id: {self.id} matricola:{self.matricola} nome: {self.nome}"

    def __eq__(self, other): 
        if not isinstance(other, self):
            return False
        
        # non ho usato id per potenziale criticità di un ricalcolo degli id a database. 
        # In contesti operativi normali non sarebbe un errore usare l'id come discriminante
        return self.matricola == other.matricola

    # Ricorda il to_dic()