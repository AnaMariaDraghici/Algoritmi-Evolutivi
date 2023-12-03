import math
from knapsack_problem import knapsack_problem
from tsp import tsp
from tsp2 import tsp2


def main():
    print("Choose the problem you want to solve: ")
    print("1. Knapsack Problem")
    print("2. TSP")
    print("3. Exit")

    op = input()
    if op == '1':
        # Citirea datelor din fisier
        with open("inputKP200.txt", "r") as f:
            lines = f.readlines()
        numbar_elemente = int(lines[0])
        capacitate = int(lines[1])

        items = []
        valori = []
        greutati = []
        for line in lines[1:-1]:
            parts = line.strip().split()
            if len(parts) >= 3:
                index = int(parts[0])
                valoare = int(parts[1])
                valori.append(valoare)
                greutate = int(parts[2])
                greutati.append(greutate)
                items.append((index, valori, greutati))


        nr_generatii = 10
        dimensiune_populatie = 10
        prob_incrucisare = 0.8
        prob_mutatie = 0.1

        cea_mai_buna_solutie, valoare_cea_mai_buna_solutie = knapsack_problem(capacitate, greutati, valori,
                                                                              nr_generatii, dimensiune_populatie,
                                                                              prob_incrucisare, prob_mutatie)

        print("Solutia optima este:", cea_mai_buna_solutie)
        print("Valoarea solutiei optime este:", valoare_cea_mai_buna_solutie)
    elif op == '2':
        with open("inputTSP100.txt") as f:
            numar_orase = int(f.readline().strip())
            orase = []
            for line in f:
                orase.append(line.strip().split())
        distante = [[0 for j in range(numar_orase)] for i in range(numar_orase)]
        for i in range(numar_orase):
            for j in range(numar_orase):
                if i != j:
                    oras1 = orase[i]
                    oras2 = orase[j]
                    x1, y1 = float(oras1[1]), float(oras1[2])
                    x2, y2 = float(oras2[1]), float(oras2[2])
                    distante[i][j] = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

        dimensiune_populatie = 2
        numar_generatii = 3
        probabilitate_mutatie = 0.1

        cea_mai_buna_solutie, cea_mai_buna_evaluare = tsp2(dimensiune_populatie, numar_generatii,
                                                         probabilitate_mutatie, numar_orase,
                                                          distante)

        print(f"Cea mai buna solutie gasita este {cea_mai_buna_solutie} cu o evaluare de {cea_mai_buna_evaluare}.")

    elif op == '3':
        ok = 0
    else:
        ok = 0


main()
