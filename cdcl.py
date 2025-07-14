import os
import time


def lettura_file(file_path):
    matrice_originale = []
    inizia_lettura = False
    with open(file_path, 'r', encoding='utf-8') as file:
            for riga in file:
                if riga.startswith("p cnf"):
                    inizia_lettura = True
                    continue

                if inizia_lettura:
                    numeri = [int(numero) for numero in riga.split()[:-1]]
                    if numeri:
                        matrice_originale.append(numeri)
    return matrice_originale



def backjump(matrice, trail, level, decision_list, clause, first_assertion_literal, first_assertion_clause):
    first_assertion_clause.remove(first_assertion_literal)
    current_level = create_level_trail(trail,decision_list)
    while True:
        first_assertion_clause_negated = [-elemento for elemento in first_assertion_clause]
        
        if -first_assertion_literal in current_level:
            if all(elem in  trail[:-len(current_level)] for elem in first_assertion_clause_negated):
                x = decision_list.pop()
                y = trail.pop()
                
                if y != x and y not in decision_list:
                        clause.pop()
                        
                while x != y:
                    y = trail.pop()
                    
                    if y != x and y not in decision_list:
                        clause.pop()
                        
                trail.append(first_assertion_literal)
                level -= 1
                first_assertion_clause.append(first_assertion_literal)
                
                clause.append(first_assertion_clause)
                break
            
        else:
            x = decision_list.pop()
            level -= 1
            y = trail.pop()
            while x != y:
                y = trail.pop()
            current_level = create_level_trail(trail, decision_list)
    
            
    matrice_1 = controllo_righe(matrice,trail)
    
    conflict, riga = controllo_sat(matrice_1, trail)
       
    return matrice_1, trail, level, decision_list, clause, conflict, riga




def controllo_sat(matrice, trail):
    for riga in matrice:
        # Controlla se tutti i numeri nella riga hanno il loro negato presente nel trail
        if all(-numero in trail for numero in riga):
            return True,riga  # Restituisci True se tutti i numeri hanno il loro negato nel trail
    return False, None
 

def two_watched_literal(matrice, trail, clausule_prop):
    #mi serve per salvarmi i due letterali per poi inserirli insieme nella lista dei two_watched
    riga_two_watched = []
    implied_literal = []
    for riga in matrice:
        for elemento in riga:
            if -elemento not in trail: 
                riga_two_watched.append(elemento)
                
            if len(riga_two_watched) == 2:
                break
        
        if len(riga_two_watched) == 1:
            implied_literal = riga_two_watched.pop()
            trail.append(implied_literal) 
            clausule_prop.append(riga)
            matrice = controllo_righe(matrice, trail)
            conflict, riga_unsat = controllo_sat(matrice, trail) #if conflict = True c'è un errore
            if conflict == True:
                return False, True, riga_unsat
           
        riga_two_watched = [] 
        
    return False, False, None              



def eliminating_opposite_literals( list_1, list_2):
    list_3 = []
    
    if isinstance(list_1, int):
        list_1 = [list_1]

    if isinstance(list_2, int):
        list_2 = [list_2]
        
    for elemento in list_1:
        if -elemento not in list_2 and elemento not in list_3:
            list_3.append(elemento)
            
    for elemento in list_2:
        if -elemento not in list_1 and elemento not in list_3:
            list_3.append(elemento)
            
    return list_3



def create_level_trail(trail, decision_list):
  
    last_number_decision = decision_list[-1]
    indice_ultimo_numero_lista1 = trail.index(last_number_decision)
    trail_livello_corrente = trail[indice_ultimo_numero_lista1:]
    return trail_livello_corrente

def check_if_explaing (lista_1, lista_2):
    if any(-elem1 == elem2 for elem1 in lista_1 for elem2 in lista_2):
        return True
    else:
        return False
    

def explain(matrice, clause, riga_unsat,decision_list, value_literal, proof_generation, matrice_originale):

    
    proof = []
    value_literal = vsids_increment(riga_unsat, value_literal)
    letterali_falsificati = 0
    clause_copy = clause.copy()
    trail_livello_corrente = create_level_trail(trail,decision_list)
    
    proof.append(riga_unsat)
    
    livello_giusto = any(-elemento in riga_unsat for elemento in trail_livello_corrente)
    if not livello_giusto:
        x = decision_list.pop()
        y = trail.pop()
        while x != y:
            y = trail.pop()
        trail_livello_corrente = create_level_trail(trail,decision_list)
        livello_giusto = any(-elemento in riga_unsat for elemento in trail_livello_corrente)

    
    for literal in riga_unsat:
        
        if -literal in trail_livello_corrente:
            letterali_falsificati += 1
            first_assertion_literal = literal
            
    if letterali_falsificati > 1:
       
        while letterali_falsificati != 1:
            clause_prop = clause_copy.pop()
  
            if check_if_explaing(riga_unsat, clause_prop):
                proof.append(clause_prop)
                letterali_falsificati = 0
                riga_risultato = eliminating_opposite_literals(riga_unsat, clause_prop)
                proof_generation[tuple(riga_risultato)] = [riga_unsat , clause_prop]
                riga_unsat = riga_risultato

                for literal in riga_unsat:
                    
                    if -literal in trail_livello_corrente:
                        letterali_falsificati += 1
                        first_assertion_literal = literal

    first_assertion_clause = riga_unsat
    matrice = learn(matrice_originale, matrice, riga_unsat)

    return matrice, first_assertion_literal, first_assertion_clause



def vsids_init(matrice):
    value_literal = {}
    for riga in matrice:
        for elemento in riga:
            if elemento not in value_literal:
                value_literal[elemento] = 0
    return value_literal



def vsids_increment(conflict_clause, value_literal):
 
    for elemento in conflict_clause:
        value_literal[elemento] += 1
    return value_literal
  
    
    
def vsids_decrement(value_literal, constant):
    for elemento in value_literal:
        value_literal[elemento] *= constant
    return value_literal
            


def subsumption(matrice):
    nuova_matrice = []
    
    for riga1 in matrice:
        contiene = False
        for riga2 in matrice:
            if riga1 is not riga2 and set(riga2).issubset(set(riga1)):
                contiene = True
                break
        if not contiene:
            nuova_matrice.append(list(riga1))
    
    return nuova_matrice



def learn(matrice_originale, matrice_provvisoria, set_unsat):
    matrice_originale.append(set_unsat)
    matrice_provvisoria = controllo_righe(matrice_originale,trail)
    
    return matrice_provvisoria
        



def decision(matrice, trail, decision_list, level, value_literal):

    dizionario_copia = value_literal.copy()
    while True:
        numero_piu_frequente = max(dizionario_copia, key=dizionario_copia.get)
        if numero_piu_frequente not in trail and -numero_piu_frequente not in trail:
            break
        else:
            del dizionario_copia[numero_piu_frequente]
 
    trail.append(numero_piu_frequente)
    decision_list.append(numero_piu_frequente)

    #print('decision')
    #print(decision_list)
    level += 1
    matrice = controllo_righe(matrice, trail)
    return trail, matrice, decision_list, level, value_literal
   



def controllo_righe(matrice, trail):
    righe_da_tenere = [elemento for elemento in matrice if not any(x in trail for x in elemento)]
    return righe_da_tenere


def elimination_learned_clause(matrice_provvisoria, media):
    nuova_matrice = []
    for clausola in matrice_provvisoria:
        if len(clausola) < media * 3.0:
            nuova_matrice.append(clausola)
    return matrice_provvisoria


def calcola_media_lunghezza_clausole(matrice_originale):
    somma_lunghezze = 0
    numero_clausole = 0
    for clausola in matrice_originale:
        somma_lunghezze += len(clausola)
        numero_clausole += 1
    media = somma_lunghezze/numero_clausole
    return media
            

def last_proof(riga_unsat, clausole_prop, proof_generation):
    clause_prop = clausole_prop.pop()
    riga_risultato = eliminating_opposite_literals(riga_unsat, clause_prop)
    proof_generation[tuple(riga_risultato)] = [riga_unsat , clause_prop]
    riga_unsat = riga_risultato
    clause.append(riga_unsat)
    
    
    
    
def proof_tree(proof_generation, nodo):
    if nodo in proof_generation:
        genitori = proof_generation[nodo]
        #print(genitori)
        scrittura_file_unsat(output_file_path, f"Genitori di {nodo}: {genitori}")
        proof_tree(proof_generation,tuple(genitori[1]))
        proof_tree(proof_generation, tuple(genitori[0]))
        
            
            
def elabora_clausola(clausola_prop):
    nodo_unsat = []
    clausola1 = []
    res = []
    for i in range(len(clausola_prop)-1, +1, -1):
        if len(clausola1) == 0:
            clausola1 = clausola_prop[i]
        res = clausola1
        clausola2 = clausola_prop[i-1]
        if check_if_explaing(res, clausola2):
            clausola1 = eliminating_opposite_literals(res, clausola2)
            proof_generation[tuple(clausola1)] = [res , clausola2]
    nodo_unsat.append(clausola_prop[0])
    nodo_unsat.append(clausola1)
    return nodo_unsat
    
def scrittura_file_sat(elapsed_time, trail, output_file_path):
    with open(output_file_path, 'a') as file:
        # Scrivi il percorso ('trail')
        file.write('Trail:\n')
        for elemento in trail:
            file.write(f"{elemento}\n")

        # Scrivi il tempo di esecuzione
        file.write(f'Tempo di esecuzione: {elapsed_time:.5f} secondi\n')

        # Scrivi la stringa 'SAT'
        file.write('SAT\n')
            
def scrittura_file_unsat(output_file_path, text):
    with open(output_file_path, 'a') as file:
        file.write(text + '\n')
    





#files = [f for f in os.listdir(r'test\uf20-91') if f.endswith(".cnf")]

file_path = input("Inserisci il percorso del file: ").strip('\"')
file_path = file_path.replace("'", "\\'")
file_path_2 = file_path 
input_file_name = os.path.splitext(os.path.basename(file_path_2))[0]
output_file_path = f"{input_file_name}_output.txt"
output_file_path = os.path.join("output", output_file_path)
start_time = time.time()
matrice_originale = lettura_file(file_path)
media = calcola_media_lunghezza_clausole(matrice_originale)
contatore_iterazioni = 0
clausole_prop = []
proof_generation = {}
proof = {}
trail = []
unsat = False
conflict = False
level = 0 
controllo = True
matrice_originale = subsumption(matrice_originale)
matrice_provvisoria = matrice_originale
#lista delle clausulo in seguito alla 'decision'
decision_list = []
value_literal = vsids_init(matrice_provvisoria)
while True:
    contatore_iterazioni += 1
    value_literal = vsids_decrement(value_literal, 0.95) 
    
    controllo, conflict, riga_unsat = two_watched_literal (matrice_provvisoria, trail, clausole_prop)
    
    matrice_provvisoria = controllo_righe(matrice_provvisoria, trail)
    if len(matrice_provvisoria) == 0:
        break 
    if conflict == False:
        trail, matrice_provvisoria, decision_list, level, value_literal = decision(matrice_provvisoria, trail, decision_list, level, value_literal)
        conflict, riga_unsat = controllo_sat(matrice_provvisoria,trail)
    if conflict == True: #qui c'era else     
        while conflict == True: 
            if level != 0: 
                matrice_provvisoria, first_assertion_literal, first_assertion_clause = explain(matrice_provvisoria, clausole_prop, riga_unsat, decision_list, value_literal, proof_generation, matrice_originale)               
                matrice_provvisoria = subsumption(matrice_provvisoria)            
            
                matrice_provvisoria, trail, level,decision_list, clause, conflict, riga_unsat  = backjump(matrice_originale,trail,level, decision_list, clausole_prop, first_assertion_literal, first_assertion_clause)
                
            else:
                print(trail)
                unsat = True
                break
        if unsat == True:
            break
    if contatore_iterazioni % 15 == 0:
        matrice_provvisoria = elimination_learned_clause(matrice_provvisoria, media)
    controllo = True
    matrice_provvisoria = controllo_righe(matrice_provvisoria, trail)
    if len(matrice_provvisoria) == 0:
        break
##print(f"File: {testo}")

if unsat == False:
    end_time = time.time()
    elapsed_time = end_time - start_time
    scrittura_file_sat(elapsed_time,trail, output_file_path)
else:
    scrittura_file_unsat(output_file_path, 'PROOF GENERATION:')
    scrittura_file_unsat(output_file_path, '\n')
    last_proof(riga_unsat, clausole_prop, proof_generation)
    nodo_unsat = elabora_clausola(clausole_prop)
    for nodo in nodo_unsat:
        proof_tree(proof_generation, tuple(nodo))
    end_time = time.time()
    elapsed_time = end_time - start_time
    scrittura_file_unsat(output_file_path, f'Tempo di esecuzione: {elapsed_time:.5f} secondi\n')
    scrittura_file_unsat(output_file_path, '\n')
    scrittura_file_unsat(output_file_path, 'UNSAT')





