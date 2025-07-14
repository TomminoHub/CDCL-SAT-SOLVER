import numpy as np
import os

def lettura_file():
    matrice = []
    inizia_lettura = False
    with open(r'test\uf20-91\uf20-024.cnf', 'r', encoding='utf-8') as file:
        for riga in file:
            if riga.startswith("p cnf"):
                inizia_lettura = True
                continue

            if inizia_lettura:
                numeri = [int(numero) for numero in riga.split()[:-1]]
                if numeri:
                    matrice.append(numeri)
    return matrice



def backjump(matrice, trail, level, decision_list, clausole_prop):
    x = decision_list.pop()
    y = trail.pop()
    flag = 0
    while x != y:
        y = trail.pop()
    for riga in matrice:
        if len(riga) == 1:
            trail, matrice = single_clause(matrice, trail, clausole_prop)
            flag = 1
    if flag != 1:
        print('removed decision e aggiunto opposto:')
        print(-x)
        trail.append(-x)
        clausole_prop.append(-x)
    level -= 1
    matrice_1 = controllo_righe(matrice,trail)
    return matrice_1, trail, level, decision_list



def controllo_sat(matrice, trail):
    flag = 0
    for riga in matrice:
        # Controlla se tutti i numeri nella riga hanno il loro negato presente nel trail
        if all(-numero in trail for numero in riga):
            print('clausola unsat:')
            print(riga)
            flag = 1
            return True,riga  # Restituisci True se tutti i numeri hanno il loro negato nel trail
    if flag == 0:
        return False, None
 


def two_watched_literal(matrice, trail, clausule_prop):
    riga_two_watched = []
    two_watched = []
    riga_prop = []
    for riga in matrice:
        for elemento in riga:
            if -elemento not in trail:
                riga_two_watched.append(elemento)
            if len(riga_two_watched) == 2:
                two_watched.append(riga_two_watched)
                break
        if len(riga_two_watched) == 1:
            implied_literal = riga_two_watched.pop()
            riga_prop = riga.copy()
            flag = 1
    if flag == 1:
        trail.append(implied_literal) 
        clausole_prop.append(riga_prop)
        matrice = controllo_righe(matrice, trail) 
    return matrice, trail, clausule_prop
                
        
        
        


def eliminating_opposite_literals( list_1, list_2):
    list_3 = []
    
    if isinstance(list_1, int):
        list_1 = [list_1]

    # Se list_2 è un intero, convertilo in una lista con un unico elemento
    if isinstance(list_2, int):
        list_2 = [list_2]
        
    for elemento in list_1:
        if -elemento not in list_2 and elemento not in list_3:
            list_3.append(elemento)
            
    for elemento in list_2:
        if -elemento not in list_1 and elemento not in list_3:
            list_3.append(elemento)
            
    return list_3


      
def explain(matrice, clause, riga_unsat, proof):
    #contiene i singoli elementi delle righe unsat
    clause_prop = clause.pop()
    
    while True:
        riga_unsat = eliminating_opposite_literals(riga_unsat, clause_prop)
        if len(riga_unsat) <= 1 or len(clause) <= 0:
            break
        else:
            print('lunghezza')
            print(riga_unsat)
            print('clause')
            print(clause)
            clause_prop = clause.pop()

    print('importante')
    print(riga_unsat)
    print(proof)
    if proof:
        proof = eliminating_opposite_literals(proof, riga_unsat)
    else:
        proof = riga_unsat.copy()
    
          
    print('explain:')
    print(riga_unsat)
    if proof:
        print('proof')
        print(proof)
    matrice = learn(matrice, proof)

    
    return matrice, proof


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



def learn(matrice, set_unsat):
    matrice.append(set_unsat)
    return matrice
        


def propagation(matrice, trail, clause):
    for riga in matrice:
        conteggio_uguali = 0
        for elemento in riga:
            for negato in trail:
                if elemento == -negato:
                    conteggio_uguali += 1

        if conteggio_uguali == len(riga) - 1:
            for elem in riga:
                if -elem not in trail :
                    print('elemento propagation:')
                    print(elem)
                    trail.append(elem)
            clause.append(list(riga))
            
            matrice = controllo_righe(matrice, trail)

    
    return trail, matrice, clause


#la decision viene fatta in base alla clausola più frequente
def decision(matrice, trail, decision_list, level):
    frequenze = {}
    for riga in matrice:
        for elemento in riga:
            if elemento in trail or -elemento in trail:
                continue
            else:
                if elemento not in frequenze:
                    frequenze[elemento] = 1
                else:
                    frequenze[elemento] += 1
    
    if frequenze:
        numero_piu_frequente = max(frequenze, key=frequenze.get)
        print('decision:')
        print(numero_piu_frequente)
        trail.append(numero_piu_frequente)
        decision_list.append(numero_piu_frequente)
        level += 1
    matrice = controllo_righe(matrice, trail)
    return trail, matrice, decision_list, level




def single_clause(matrice, trail, clause):
    found = 0
    for riga in matrice:
        if len(riga) == 1:
            found = 1
            print('single clause:')
            print(riga)
            trail.append(riga[0])
            clause.append(list(riga[0]))
    matrice = controllo_righe(matrice, trail)
    return found, trail, matrice




def controllo_righe(matrice, trail):
    righe_da_tenere = [elemento for elemento in matrice if not any(x in trail for x in elemento)]
    return righe_da_tenere



files = [f for f in os.listdir(r'test\uf20-91') if f.endswith(".cnf")]
for testo in files[0:1]:
    matrice_originale = []
    inizia_lettura = False
    with open(fr'test\uf20-91\{testo}', 'r', encoding='utf-8') as file:
        for riga in file:
            if riga.startswith("p cnf"):
                inizia_lettura = True
                continue

            if inizia_lettura:
                numeri = [int(numero) for numero in riga.split()[:-1]]
                if numeri:
                    matrice_originale.append(numeri)
        matrice_provvisoria = matrice_originale
        print(matrice_provvisoria)
        #contiene le righe che hanno causato l'aggiunta di un elemento al trail, è il 'motivo' della propagation
        clausole_prop = []
        proof_generation = []
        trail = []
        unsat = False
        level = 0 
        print(matrice_originale)
        matrice_originale = subsumption(matrice_originale)
        print(matrice_originale)
        #lista delle clausulo in seguito alla 'decision'
        decision_list = []
        while True:
            controllo, matrice_provvisoria, trail, clausole_prop = two_watched_literal (matrice_provvisoria, trail, clausole_prop)
            found, trail, matrice_provvisoria = single_clause(matrice_provvisoria, trail, clausole_prop)
            matrice_provvisoria, trail, clausole_prop = two_watched_literal (matrice_provvisoria, trail, clausole_prop)
            if found: 
                matrice_provvisoria, trail, clausole_prop = two_watched_literal (matrice_provvisoria, trail, clausole_prop)
                trail, matrice_provvisoria = propagation(matrice_provvisoria, trail, clausole_prop)
                matrice_provvisoria, trail, clausole_prop = two_watched_literal (matrice_provvisoria, trail, clausole_prop)
                found = 0
            trail, matrice_provvisoria, decision_list, level = decision(matrice_provvisoria, trail, decision_list, level)
            trail, matrice_provvisoria, clausole_prop = propagation(matrice_provvisoria, trail, clausole_prop)
            #controllo che la lunghezza del trail sia aumentata
            #riga contiene la riga che non puo essere sat
            controllo , riga = controllo_sat(matrice_provvisoria,trail)
            #significa che una clausola non puo essere soddisfatta
            if controllo:
                matrice_provvisoria, proof_generation = explain(matrice_provvisoria, clausole_prop, riga, proof_generation)
                matrice_provvisoria = subsumption(matrice_provvisoria)            
                if level != 0:
                    matrice_provvisoria, trail, level, decision_list = backjump(matrice_originale,trail,level, decision_list, clausole_prop)
                    trail, matrice_provvisoria, clausole_prop = propagation(matrice_provvisoria, trail, clausole_prop)
                else:
                    unsat = True
                    break
            #print('ok')
            if len(matrice_provvisoria) == 0:
                break
            print('trail')
            print(trail)
        print(f"File: {testo}")
        
        if unsat == False:
            print(trail)
            print('SAT')
        else:
            print('UNSAT')
        print('\n\n\n\n\n\n\n')

