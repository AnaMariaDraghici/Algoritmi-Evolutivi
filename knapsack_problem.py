import random


# Definirea functiei de fitness
def fitness(solutie, greutati, capacitate, valori):
    """
        Funcția calculează valoarea unei soluții (o listă de 0 și 1) în raport cu greutățile și valorile obiectelor.

        Parametri:
        solutie (list): o listă de 0 și 1 reprezentând obiectele alese (1) sau nealese (0)
        greutati (list): o listă cu greutățile fiecărui obiect
        capacitate (float): capacitatea maximă a rucsacului
        valori (list): o listă cu valorile fiecărui obiect

        Returnează:
        float: valoarea soluției dacă aceasta respectă constrângerile de capacitate, altfel 0
        """
    greutate_totala = 0
    valoare_totala = 0
    for i in range(len(solutie)):
        if solutie[i] == 1:
            greutate_totala += greutati[i]
            valoare_totala += valori[i]
    if greutate_totala > capacitate:
        return 0
    else:
        return valoare_totala


def knapsack_problem(capacitate, greutati, valori, nr_generatii, dimensiune_populatie, prob_incrucisare, prob_mutatie):
    """
        Funcția rezolvă problema rucsacului utilizând un algoritm evolutiv.

        Parametri:
        capacitate (float): capacitatea maximă a rucsacului
        greutati (list): o listă cu greutățile fiecărui obiect
        valori (list): o listă cu valorile fiecărui obiect
        nr_generatii (int): numărul de generații ale algoritmului evolutiv
        dimensiune_populatie (int): numărul de soluții din fiecare generație
        prob_incrucisare (float): probabilitatea de încrucișare a soluțiilor
        prob_mutatie (float): probabilitatea de mutație a soluțiilor

        Returnează:
        tuple: o tuplă formată din soluția cea mai bună și valoarea acesteia
        """
    # Inițializarea populatiei de solutii
    populatie = []
    for i in range(dimensiune_populatie):
        solutie = [random.randint(0, 1) for _ in range(len(greutati))]
        populatie.append(solutie)
    # Repetarea algoritmului evolutiv
    for generatie in range(nr_generatii):
        # Evaluarea fiecarei solutii din populatie
        evaluari = [fitness(solutie,  greutati, capacitate, valori) for solutie in populatie]

        # Sortarea populatiei in ordinea descrescatoare a valorilor solutiilor
        populatie = [solutie for _, solutie in sorted(zip(evaluari, populatie), reverse=True)]

        # Selectia de parinti
        parinti = []
        for i in range(dimensiune_populatie):
            parinte1 = populatie[random.randint(0, dimensiune_populatie - 1)]
            parinte2 = populatie[random.randint(0, dimensiune_populatie - 1)]
            parinti.append((parinte1, parinte2))

        # Incrucisarea parintilor
        copii = []
        for parinte1, parinte2 in parinti:
            if random.random() < prob_incrucisare:
                punct_taiere = random.randint(1, len(greutati) - 1)
                copil = parinte1[:punct_taiere] + parinte2[punct_taiere:]
            else:
                copil = parinte1
            copii.append(copil)

        # Mutatia copiilor
        for i in range(len(copii)):
            if random.random() < prob_mutatie:
                pozitie = random.randint(0, len(greutati) - 1)
                copii[i][pozitie] = 1 - copii[i][pozitie]

        # Evaluarea fiecarei solutii din populatia de copii
        evaluari_copii = [fitness(solutie,  greutati, capacitate, valori) for solutie in copii]

        # Inlocuirea populatiei cu unirea populatiei curente cu populatia de copii
        populatie = populatie + copii

        # Sortarea populatiei in ordinea descrescatoare a valorilor solutiilor
        evaluari_populatie = evaluari + evaluari_copii
        populatie = [solutie for _, solutie in sorted(zip(evaluari_populatie, populatie), reverse=True)]

        # Selectarea celor mai bune solutii din populatie
        populatie = populatie[:dimensiune_populatie]
        cea_mai_buna_solutie = populatie[0]
        valoare_cea_mai_buna_solutie = fitness(cea_mai_buna_solutie,  greutati, capacitate, valori)

        return cea_mai_buna_solutie, valoare_cea_mai_buna_solutie
    # Algoritmul evolutiv folosește parametri precum numărul
    # de generații, dimensiunea populației, probabilitatea de
    # încrucișare și probabilitatea de mutație. Acești parametri
    # pot fi ajustați în funcție de problema specifică și de performanța
    # obținută. Implementarea utilizează o reprezentare a soluțiilor
    # sub formă de cod binar, selectarea părinților prin intermediul
    # turnirului, încrucișarea cu un singur punct de tăiere și
    # mutația cu probabilitatea dată.
