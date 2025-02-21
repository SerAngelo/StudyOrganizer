import study_organizer as so
import time
import subprocess

def print_loading_bar(percentage):
    bar_length = 20
    progress = int(bar_length * percentage / 100)
    bar = "[" + "=" * progress + " " * (bar_length - progress) + "]"
    return f"{bar} {percentage}% Complete"

def generate_startup_output():
    print("*" * 80)
    print(r"""
   _____ _             _          ____                        _              
  / ____| |           | |        / __ \                      (_)             
 | (___ | |_ _   _  __| |_   _  | |  | |_ __ __ _  __ _ _ __  _ _______ _ __ 
  \___ \| __| | | |/ _` | | | | | |  | | '__/ _` |/ _` | '_ \| |_  / _ \ '__|
  ____) | |_| |_| | (_| | |_| | | |__| | | | (_| | (_| | | | | |/ /  __/ |   
 |_____/ \__|\__,_|\__,_|\__, |  \____/|_|  \__, |\__,_|_| |_|_/___\___|_|   
                          __/ |              __/ |                           
                         |___/              |___/                            

                                   
""")
    print("*" * 80)
    print("Welcome to STUDY ORGANIZER - Your Ultimate Study Companion")
    print("*" * 80)
    
def schermata_iniziale():
    while True:
        input("\nPremi qualsiasi tasto per ritornare alla schermate iniziale:")
        break
    
def crea_nuovo_calendario():
    
    nome_file = input("\nInserisci il nome del file.txt che contiene le materie, i rispettivi argomenti e le loro informazioni: ")
    ripetizioni = int(input("\nInserisci il numero di ripetizioni ideale per ogni argomento: "))
    lista_di_materie = input("Inserisci la lista di materie separate da spazi e con # iniziale (es° #HEP): ")
    materie_interessate = lista_di_materie.split()
    
    so.ripetizione_spaziata(nome_file, materie_interessate, ripetizioni, save=True)
    
    nome_file_output = input("\nInserisci il nome del file.txt in cui salvare il calendario sottoforma di tabella: ")
    
    so.stampa_tabella_materie('binary_output.pkl', nome_file_output)
    
    schermata_iniziale()
    
    
    
def modifica_calendario():
    
    materiaX = input("\nInserisci il nome della materia la cui programmazione deve cambiare: ")
    argomentoX = input("\nInserisci il nome dell'argomento di la cui programmazione deve cambiare: ")
    shift = int(input("Inserisci di quanti giorni shiftare: "))
    
    so.shifting('binary_output.pkl', materiaX, argomentoX, shift)
    
    nome_file_output = input("\nInserisci il nome del file.txt in cui salvare il calendario sottoforma di tabella: ")
    
    so.stampa_tabella_materie('binary_output.pkl', nome_file_output)
    
    schermata_iniziale()

def date():
    
    try:
        so.date_esame('binary_output.pkl')
    except:
        print("Errore: file binary_output.pkl non trovato\n")
        
    schermata_iniziale()
    
def mostra_help():
    print("-" * 80)
    print("Il file deve essere diviso in blocchi di questo tipo:\n")
    print(r"""

            #Nome_materia 2024 2 19 <- [data esame]
            Nome_argomento1 0 2024 2 1 -
            Nome_argomento2 0 2024 2 2 |
            Nome_argomento3 0 2024 2 3 |
            Nome_argomento4 0 2024 2 3 |-> [date in cui si inizierà a ripetere]
            Nome_argomento5 0 2024 2 4 |
            Nome_argomento6 0 2024 2 5 |
            Nome_argomento7 0 2024 2 6 -
                            ^
                            |
    
                [numero di volte che è stato ripetuto un certo argomento]
            """)
    print("-" * 80)
    
    schermata_iniziale()
    
def mostra_calendario(nome_file_output):
    
    try:
        # Esegui il comando cat output.txt
        subprocess.call(["cat", nome_file_output])
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
    
    schermata_iniziale()

# Chiamata alla funzione per generare l'output di avvio
generate_startup_output()

check=True

while check:
    
    print("1. Creare un nuovo calendario\n")
    print("2. Modificare un calendario esistente\n")
    print("3. Date esami\n")
    print("4. Mostra calendario\n")
    print("5. Help\n")
    print("6. Exit")
    answer = int(input("Cosa desideri fare? "))
    
    
    if answer == 1:
        crea_nuovo_calendario()
    
    elif answer == 2:
        modifica_calendario()
    
    elif answer == 3:
        date()
        
    elif answer == 4:
        nome_file_output = input("\nInserisci il nome del file.txt in cui è salvato il calendario: ")
        mostra_calendario(nome_file_output)
        
    elif answer == 5:
        mostra_help()
    
    elif answer == 6:
        break
        
        
    





