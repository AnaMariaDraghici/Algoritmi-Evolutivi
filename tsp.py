import random


# Definirea operatorilor genetici
def incrucisare_permutari(parinte1, parinte2, numar_orase):
    """
       Aceasta functie implementeaza operatorul de incrucisare pentru problemele de tip TSP, utilizand reprezentarea solutiilor sub forma de permutari.

       Args:
       parinte1: o lista de dimensiune numar_orase, reprezentand prima solutie-parinte
       parinte2: o lista de dimensiune numar_orase, reprezentand a doua solutie-parinte
       numar_orase: un intreg, reprezentand numarul total de orase din problema TSP

       Returns:
       copil1: o lista de dimensiune numar_orase, reprezentand primul copil obtinut prin incrucisarea celor doi parinti
       copil2: o lista de dimensiune numar_orase, reprezentand al doilea copil obtinut prin incrucisarea celor doi parinti
       """
    punct_de_taie = random.randint(1, numar_orase - 1)
    copil1 = parinte1[:punct_de_taie] + [gena for gena in parinte2 if gena not in parinte1[:punct_de_taie]]
    copil2 = parinte2[:punct_de_taie] + [gena for gena in parinte1 if gena not in parinte2[:punct_de_taie]]
    return copil1, copil2


def mutatie_permutari(solutie, probabilitate_mutatie, numar_orase):
    """Aplică mutația prin interschimbarea a două poziții ale soluției.

       Args:
           solutie (list): Reprezentarea sub formă de permutare a soluției curente.
           probabilitate_mutatie (float): Probabilitatea de a aplica mutația.
           numar_orase (int): Numărul total de orașe din problemă.

       Returns:
           list: Soluția obținută prin aplicarea mutației sau soluția inițială, dacă mutația nu este aplicată.
       """
    if random.random() < probabilitate_mutatie:
        index1 = random.randint(0, numar_orase - 1)
        index2 = random.randint(0, numar_orase - 1)
        solutie[index1], solutie[index2] = solutie[index2], solutie[index1]
    return solutie


# Definirea functiei de fitness pentru a calcula distanta totala pentru o solutie data
def fitness(solutie, numar_orase, distante):
    """
    Calculeaza distanta totala a unei solutii date folosind matricea de distante.
    Args:
    - solutie (list): o lista care contine orasele in ordinea in care trebuie parcurse
    - numar_orase (int): numarul total de orase din problema
    - distante (list): o matrice de dimensiune numar_orase x numar_orase care contine distantele intre orase

    Returns:
    - distanta_totala (float): distanta totala a solutiei date, ca suma a distantei dintre fiecare pereche de orase
    """
    distanta_totala = 0
    for i in range(numar_orase-1):
        oras1 = solutie[i]
        oras2 = solutie[i + 1]
        if oras1 >= numar_orase or oras2 >= numar_orase:
            print(f"Invalid indices: oras1={oras1}, oras2={oras2}")
            return float('inf')
        else:
            distanta_totala += distante[oras1][oras2]
    return distanta_totala + distante[solutie[numar_orase - 1]][solutie[0]]


def tsp(dimensiune_populatie, numar_generatii,  probabilitate_mutatie, numar_orase, distante):
    ''' Algoritmul genetic pentru problema Comis-Voiajorului.
        Args:
        dimensiune_populatie (int): Dimensiunea populatiei
        numar_generatii (int): Numarul de generatii pentru evolutie
        probabilitate_incrucisare (float): Probabilitatea de incrucisare a doua solutii
        probabilitate_mutatie (float): Probabilitatea de mutatie a unui gene
        numar_orase (int): Numarul de orase din problema
        distante (list): Matricea distantelor intre orase

    Returns:
        tuple: O tupla formata din cea mai buna solutie gasita si evaluarea acesteia
    '''

    # Definirea reprezentarii solutiilor sub forma de permutari
    populatie = []
    for i in range(dimensiune_populatie):
        solutie = list(range(numar_orase))
        random.shuffle(solutie)
        populatie.append(solutie)

    # Evaluarea populatiei
    for generatie in range(numar_generatii):
        # Evaluarea tuturor solutiilor din populatie
        evaluari = [fitness(solutie, numar_orase, distante) for solutie in populatie]

        # Repararea solutiilor invalide (in cazul in care exista)
        for i in range(dimensiune_populatie):
            while len(set(populatie[i])) < numar_orase:
                for j in range(numar_orase):
                    if populatie[i].count(j) > 1:
                        index1 = populatie[i].index(j)
                        index2 = populatie[i].index(random.choice([x for x in range(numar_orase) if x != j]))
                        populatie[i][index1], populatie[i][index2] = populatie[i][index2], populatie[i]
    # Selectarea celor mai bune solutii din populatie
    elite = []
    for i in range(5):
        index_cel_mai_bun = evaluari.index(min(evaluari))
        elite.append(populatie[index_cel_mai_bun])
        populatie.pop(index_cel_mai_bun)
        evaluari.pop(index_cel_mai_bun)

    # Selectia urmatoarei generatii de solutii
    urmatoarea_generatie = []
    while len(urmatoarea_generatie) < dimensiune_populatie - 5:
        parinte1 = random.choices(populatie, weights=[1 / evaluare for evaluare in evaluari])[0]
        parinte2 = random.choices(populatie, weights=[1 / evaluare for evaluare in evaluari])[0]
        copil1, copil2 = incrucisare_permutari(parinte1, parinte2,numar_orase)
        copil1 = mutatie_permutari(copil1, probabilitate_mutatie, numar_orase)
        copil2 = mutatie_permutari(copil2, probabilitate_mutatie, numar_orase)
        urmatoarea_generatie.append(copil1)
        urmatoarea_generatie.append(copil2)

    # Adaugarea celor mai bune solutii din populatie in urmatoarea generatie
    urmatoarea_generatie += elite

    # Inlocuirea populatiei curente cu urmatoarea generatie
    populatie = urmatoarea_generatie
    cea_mai_buna_solutie = elite[0]
    cea_mai_buna_evaluare = fitness(cea_mai_buna_solutie, numar_orase, distante)

    return cea_mai_buna_solutie, cea_mai_buna_evaluare


# Este important de mentionat ca aceasta implementare este o
# abordare simpla si nu ia in considerare optimizari avansate
# pentru algoritmul evolutiv pentru problema comis-voiajorului.
# De asemenea, codul poate fi adaptat si imbunatatit pentru a se
# potrivi nevoilor specifice ale problemei si ale datelor de intrare.
