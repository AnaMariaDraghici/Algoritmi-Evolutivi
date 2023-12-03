import random


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


def tsp2(dimensiune_populatie, nr_generatii, prob_mutatie, nr_orase, distante):
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
    # Inițializarea populatiei de solutii
    populatie = []
    for i in range(dimensiune_populatie):
        solutie = list(range(nr_orase))
        random.shuffle(solutie)
        populatie.append(solutie)
    # Repetarea algoritmului evolutiv
    for generatie in range(nr_generatii):
        # Evaluarea fiecarei solutii din populatie
        evaluari = [fitness(solutie, nr_orase, distante) for solutie in populatie]

        # Sortarea populatiei in ordinea descrescatoare a distantelor solutiilor
        populatie = [solutie for _, solutie in sorted(zip(evaluari, populatie))]

        # Selectia de parinti
        parinti = []
        for i in range(dimensiune_populatie):
            parinte1 = populatie[random.randint(0, dimensiune_populatie - 1)]
            parinte2 = populatie[random.randint(0, dimensiune_populatie - 1)]
            parinti.append((parinte1, parinte2))
        copii=[]
        # Incrucisarea parintilor
        for parinte1, parinte2 in parinti:
            punct_de_taiere = random.randint(1, nr_orase - 1)
            copil1= parinte1[:punct_de_taiere] + [gena for gena in parinte2 if gena not in parinte1[:punct_de_taiere]]
            copil2 = parinte2[:punct_de_taiere] + [gena for gena in parinte1 if gena not in parinte2[:punct_de_taiere]]
            copii.append(copil1)
            copii.append(copil2)

        # Mutatia copiilor prin permutari
        if random.random() < prob_mutatie:
            index1 = random.randint(0, nr_orase - 1)
            index2 = random.randint(0, nr_orase - 1)
            solutie[index1], solutie[index2] = solutie[index2], solutie[index1]

        # Evaluarea fiecarei solutii din populatia de copii
        evaluari_copii = [fitness(solutie, nr_orase, distante) for solutie in copii]

        # Inlocuirea populatiei cu unirea populatiei curente cu populatia de copii
        populatie = populatie + copii

        # Sortarea populatiei in ordinea descrescatoare a distantelor solutiilor
        evaluari_populatie = evaluari + evaluari_copii
        populatie = [solutie for _, solutie in sorted(zip(evaluari_populatie, populatie))]

        # Selectarea celor mai bune solutii din populatie
        populatie = populatie[:dimensiune_populatie]
        cea_mai_buna_solutie = populatie[0]
        valoare_cea_mai_buna_solutie = fitness(cea_mai_buna_solutie,  nr_orase, distante)

        return cea_mai_buna_solutie, valoare_cea_mai_buna_solutie
