from datetime import datetime, timedelta
import pickle
from tabulate import tabulate




class Argomento:
    
    
    
    def __init__(self, nome_arg, n):
        self.nome = nome_arg
        self.nvolte_ripetuto = n
        self.data_inizio = None
        self.date = []

    def set_data(self, new_data):
        self.date.append(new_data)
        
   # def reset_date(self):
   #     self.date = []
        
    def set_data_inizio(self, data_inizio):
        self.data_inizio = data_inizio
        
    def shift_date(self, days_shift):
        data_corrente = datetime.now()
        
        for i in range(len(self.date)):
            # Converti la stringa data in un oggetto datetime
            data_argomento = datetime.strptime(self.date[i], '%Y-%m-%d')

            # Verifica se la data è maggiore di quella corrente
            if data_argomento > data_corrente:
                # Shift della data di n giorni
                nuova_data = data_argomento + timedelta(days=days_shift)

                # Aggiorna la data nella lista
                self.date[i] = nuova_data.strftime('%Y-%m-%d')

    def print_info(self):
        print(f"Argomento: {self.nome}  Ripetuto: {self.nvolte_ripetuto} volte.")


class Materia:
    def __init__(self, nome, argomenti):
        self.nome = nome
        self.N_argomenti = len(argomenti)
        self.argomenti = argomenti
        
        
    def set_data_esame(self, data_esame):
        self.data_esame = data_esame


    def print_info(self):
        print(f"Materia: {self.nome}")
        for argomento in self.argomenti:
            argomento.print_info()
        print()


'''
def leggi_file_e_crea_lista_materie(nome_file, materie_interessate):
    materie = []
    nome_materia = None

    with open(nome_file, 'r') as file:
        for line in file:
            line = line.strip().split()

            if line:
                if line[0].startswith('#'):
                    nome_materia = line[0]
                    if nome_materia in materie_interessate:
                        argomenti = []
                        materie.append(Materia(nome_materia, argomenti))
                elif len(line) >= 2 and nome_materia in materie_interessate:
                    nome_argomento = line[0]
                    n_ripetuto = int(line[1])
                    
                    try:
                        anno = int(line[2])
                        mese = int(line[3])
                        giorno = int(line[4])
                        data_inizio = datetime(anno,mese,giorno)
                    except:
                        data_inizio = None
                    
                    
                    argomento = Argomento(nome_argomento, n_ripetuto)
                    argomento.set_data_inizio(data_inizio)
                    
                    argomenti.append(argomento)

    return materie
'''

def leggi_file_e_crea_lista_materie(nome_file, materie_interessate):
    materie = []
    nome_materia = None

    with open(nome_file, 'r') as file:
        for line in file:
            line = line.strip().split()

            if line:
                if line[0].startswith('#'):
                    nome_materia = line[0]
                    if nome_materia in materie_interessate:
                        argomenti = []
                        M = Materia(nome_materia, argomenti)
                        
                        try:
                            anno = int(line[1])
                            mese = int(line[2])
                            giorno = int(line[3])
                            data_fine = datetime(anno,mese,giorno)
                            
                        except:
                            data_fine = None
                        
                        M.set_data_esame(data_fine)
                        materie.append(M)
                        
                elif len(line) > 4 and nome_materia in materie_interessate:
                    nome_argomento = line[0]
                    n_ripetuto = int(line[1])
                    
                    try:
                        anno = int(line[2])
                        mese = int(line[3])
                        giorno = int(line[4])
                        data_inizio = datetime(anno,mese,giorno)
                    except:
                        data_inizio = None
                    
                    
                    argomento = Argomento(nome_argomento, n_ripetuto)
                    argomento.set_data_inizio(data_inizio)
                    
                    argomenti.append(argomento)

    return materie






def ripetizione_spaziata(nome_file, materie_da_ripassare, ripetizioni, save=False):
    
    materie = leggi_file_e_crea_lista_materie(nome_file, materie_da_ripassare) #qui ho una lista di oggetti materia

    
    

    for idm, mat in enumerate(materie_da_ripassare):
        
        for idx, arg in enumerate(materie[idm].argomenti):
            
            giorni=[]
            
            dataI = arg.data_inizio
            dataF = materie[idm].data_esame
            
            if dataI != None:
                for giorno in range((dataF-dataI).days):
                    data_corrente = dataI + timedelta(days=giorno)
                    data_corrente = data_corrente.strftime('%Y-%m-%d')
                    giorni.append(data_corrente)
            
                
        
            
        
                correct_days = [int(n*(n+1)/2) for n in range(arg.nvolte_ripetuto,ripetizioni)]
            
                for idy, day in enumerate(giorni):
                    if idy in correct_days:
                        
                        
                        arg.set_data(day)
               
                    
                
    if save == True:
        output_file = "binary_output.pkl"
        with open(output_file, 'wb') as file:
            pickle.dump([materie, datetime.now()] , file)
            
        print(f"I risultati sono stati salvati nel file binario: {output_file}")
            
    return materie



def shifting(filePKL, materiaX, argomentoX, numero_di_giorni):
    with open(filePKL, 'rb') as file:
        materie, data_creazione = pickle.load(file)
        

        materia_trovata = next((materia for materia in materie if materia.nome == materiaX), None)

        lista_argomenti = materia_trovata.argomenti
        
        argomento_trovato = next((arg for arg in lista_argomenti if arg.nome == argomentoX), None)
        
        argomento_trovato.shift_date(numero_di_giorni)

    output_file = "binary_output.pkl"
    with open(output_file, 'wb') as file:
        pickle.dump([materie, datetime.now()] , file)
        
    print(f"I risultati shiftati sono stati correttamente salvati nel file binario: {output_file}")
        
  
def date_esame(filePKL):
    with open(filePKL, 'rb') as file:
        materie, data_creazione = pickle.load(file)
    
    for mat in materie:    
        print("Materia: ", mat.nome, " Data esame: ", mat.data_esame.strftime('%Y-%m-%d'), "#giorni rimanenti: ", (mat.data_esame-datetime.now()).days, "\n") 
    
    print("")




def stampa_lista_materie(filePKL, nome_file_output):
    with open(filePKL, 'rb') as file:
        materie, data_creazione = pickle.load(file)

    argomenti_per_data = {}

    for materia in materie:
        for argomento in materia.argomenti:
            for data in argomento.date:
                if data not in argomenti_per_data:
                    argomenti_per_data[data] = {}

                if materia.nome not in argomenti_per_data[data]:
                    argomenti_per_data[data][materia.nome] = []

                argomenti_per_data[data][materia.nome].append(argomento)

    # Ordino le date in modo crescente
    date_ordinate = sorted(argomenti_per_data.keys())


    print(date_ordinate)
    
    
    
    with open(nome_file_output, 'w') as file:
        
        # Scrivo gli argomenti raggruppati per data (in ordine)
        for data in date_ordinate:
            file.write(f"\tData: {data}\n")
            for materia in argomenti_per_data[data].keys():
                file.write(f"\t\tMateria: {materia}\n")
                
                argomenti = argomenti_per_data[data][materia]
                for argomento in argomenti:
                    file.write(f"\t\t\tArgomento: {argomento.nome}\n")
                file.write("\n")


    
    
    
    


def stampa_tabella_materie(filePKL, nome_file_output):
    with open(filePKL, 'rb') as file:
        materie, data_creazione = pickle.load(file)

    argomenti_per_data = {}

    for materia in materie:
        for argomento in materia.argomenti:
            for data in argomento.date:
                if data not in argomenti_per_data:
                    argomenti_per_data[data] = {}

                if materia.nome not in argomenti_per_data[data]:
                    argomenti_per_data[data][materia.nome] = []

                argomenti_per_data[data][materia.nome].append(argomento)

    # Ordino le date in modo crescente
    date_ordinate = sorted(argomenti_per_data.keys())

    # Creo una lista di righe per la tabella
    table_rows = []

    for data in date_ordinate:
        row = [data]
        for materia in materie:
            if materia.nome in argomenti_per_data[data]:
                argomenti = argomenti_per_data[data][materia.nome]
                row.append(", ".join(argomento.nome for argomento in argomenti))
            else:
                row.append("")
        table_rows.append(row)

    # Creo l'intestazione della tabella con i nomi delle materie
    headers = ["Data"] + [materia.nome for materia in materie]

    # Creo la tabella utilizzando tabulate
    table = tabulate(table_rows, headers, tablefmt="grid")

    # Scrivo la tabella nel file
    with open(nome_file_output, 'w') as file:
        file.write(table)  
    
    print(f"I risultati shiftati sono stati correttamente salvati nel file binario: {nome_file_output}")
    
    
    
    
    
    
    
    
    
    
    
    


