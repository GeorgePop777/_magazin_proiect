import json

# ------------------------------
# Structura competitor
# ------------------------------
class Competitor:
    def __init__(self, nume, punctaj, timp):
        self.nume = nume
        self.punctaj = punctaj
        self.timp = timp

    def __repr__(self):
        return f"{self.nume} - Punctaj: {self.punctaj}, Timp: {self.timp}"


# ------------------------------
# Citire din JSON
# ------------------------------
def incarca_din_json(fisier):
    try:
        with open(fisier, 'r', encoding='utf-8') as f:
            data = json.load(f)
            competitori = []
            for c in data:
                competitori.append(Competitor(c['nume'], c['punctaj'], c['timp']))
            return competitori
    except FileNotFoundError:
        print("Fisierul nu a fost gasit!")
        return []


# ------------------------------
# Afisare lista
# ------------------------------
def afiseaza_competitori(lista):
    if not lista:
        print("Lista este goala!")
        return

    print("\nLista competitori:")
    for c in lista:
        print(c)


# ------------------------------
# Adaugare competitor
# ------------------------------
def adauga_competitor(lista):
    nume = input("Nume: ").strip()
    if not nume:
        print("Numele nu poate fi gol!")
        return

    try:
        punctaj = int(input("Punctaj: "))
        timp = int(input("Timp: "))
    except ValueError:
        print("Date invalide!")
        return

    lista.append(Competitor(nume, punctaj, timp))
    print("Competitor adaugat!")


# ------------------------------
# Actualizare competitor
# ------------------------------
def actualizeaza_competitor(lista):
    nume = input("Introdu numele competitorului de actualizat: ")

    for c in lista:
        if c.nume.lower() == nume.lower():
            try:
                c.punctaj = int(input("Nou punctaj: "))
                c.timp = int(input("Nou timp: "))
                print("Actualizare realizata!")
                return
            except ValueError:
                print("Date invalide!")
                return

    print("Competitor inexistent!")


# ------------------------------
# Functie comparare
# ------------------------------
def compara(a, b):
    # punctaj descrescator
    if a.punctaj != b.punctaj:
        return a.punctaj > b.punctaj

    # timp crescator
    if a.timp != b.timp:
        return a.timp < b.timp

    # nume alfabetic
    return a.nume.lower() < b.nume.lower()


# ------------------------------
# Quicksort
# ------------------------------
def quicksort(lista):
    if len(lista) <= 1:
        return lista

    pivot = lista[len(lista) // 2]
    stanga = []
    egal = []
    dreapta = []

    for elem in lista:
        if compara(elem, pivot):
            stanga.append(elem)
        elif compara(pivot, elem):
            dreapta.append(elem)
        else:
            egal.append(elem)

    return quicksort(stanga) + egal + quicksort(dreapta)


# ------------------------------
# Clasament
# ------------------------------
def afiseaza_clasament(lista):
    if not lista:
        print("Lista este goala!")
        return

    lista_sortata = quicksort(lista)

    print("\nClasament:")
    print(f"{'Loc':<5}{'Nume':<20}{'Punctaj':<10}{'Timp':<10}")

    loc = 1
    for i, c in enumerate(lista_sortata):
        if i > 0:
            prev = lista_sortata[i - 1]
            if c.punctaj != prev.punctaj or c.timp != prev.timp:
                loc = i + 1

        print(f"{loc:<5}{c.nume:<20}{c.punctaj:<10}{c.timp:<10}")


# ------------------------------
# Statistici
# ------------------------------
def statistici(lista):
    if not lista:
        print("Lista este goala!")
        return

    punctaje = [c.punctaj for c in lista]
    timpi = [c.timp for c in lista]

    print("\nStatistici:")
    print("Numar competitori:", len(lista))
    print("Punctaj maxim:", max(punctaje))
    print("Punctaj minim:", min(punctaje))
    print("Media punctajelor:", sum(punctaje) / len(lista))
    print("Cel mai bun timp:", min(timpi))


# ------------------------------
# Meniu
# ------------------------------
def meniu():
    lista = incarca_din_json("competitori.json")

    while True:
        print("\n--- MENIU ---")
        print("1. Afisare competitori")
        print("2. Adauga competitor")
        print("3. Actualizeaza competitor")
        print("4. Sorteaza (Quicksort)")
        print("5. Afiseaza clasament")
        print("6. Statistici")
        print("0. Iesire")

        opt = input("Alege optiunea: ")

        if opt == '1':
            afiseaza_competitori(lista)
        elif opt == '2':
            adauga_competitor(lista)
        elif opt == '3':
            actualizeaza_competitor(lista)
        elif opt == '4':
            lista = quicksort(lista)
            print("Lista sortata!")
        elif opt == '5':
            afiseaza_clasament(lista)
        elif opt == '6':
            statistici(lista)
        elif opt == '0':
            print("La revedere!")
            break
        else:
            print("Optiune invalida!")


# ------------------------------
# Start
# ------------------------------
if __name__ == "__main__":
    meniu()
