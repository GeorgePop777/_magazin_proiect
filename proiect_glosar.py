import csv

# Structura principala de date
glosar = {}


# 1. Adaugare termen
def adauga_termen():
    termen = input("Introduceti termenul: ").strip()

    if termen in glosar:
        print("Termenul exista deja!")
        return

    definitie = input("Definitie: ")
    categorie = input("Categorie: ")
    exemplu = input("Exemplu: ")

    glosar[termen] = {
        "definitie": definitie,
        "categorie": categorie,
        "exemplu": exemplu
    }

    print("Termen adaugat cu succes!")


# 2. Cautare exacta
def cautare_exacta():
    termen = input("Introduceti termenul cautat: ")

    if termen in glosar:
        info = glosar[termen]
        print(f"\nTermen: {termen}")
        print("Definitie:", info["definitie"])
        print("Categorie:", info["categorie"])
        print("Exemplu:", info["exemplu"])
    else:
        print("Termenul nu exista.")


# 3. Cautare partiala
def cautare_partiala():
    fragment = input("Introduceti fragmentul de cautare: ")

    gasit = False

    for termen in glosar:
        if fragment.lower() in termen.lower():
            print(f"\n{termen}")
            print("Definitie:", glosar[termen]["definitie"])
            print("Categorie:", glosar[termen]["categorie"])
            print("Exemplu:", glosar[termen]["exemplu"])
            gasit = True

    if not gasit:
        print("Nu exista termeni care sa contina acest fragment.")



# 4. Actualizare termen
def actualizare_termen():
    termen = input("Introduceti termenul de actualizat: ")

    if termen not in glosar:
        print("Termenul nu exista.")
        return

    print("Ce doriti sa modificati?")
    print("1. Definitie")
    print("2. Categorie")
    print("3. Exemplu")

    opt = input("Optiune: ")

    if opt == "1":
        glosar[termen]["definitie"] = input("Noua definitie: ")
    elif opt == "2":
        glosar[termen]["categorie"] = input("Noua categorie: ")
    elif opt == "3":
        glosar[termen]["exemplu"] = input("Noul exemplu: ")
    else:
        print("Optiune invalida.")
        return

    print("Termen actualizat.")


# 5. Stergere termen
def stergere_termen():
    termen = input("Introduceti termenul de sters: ")

    if termen in glosar:
        del glosar[termen]
        print("Termen sters.")
    else:
        print("Termenul nu exista.")


# 6. Afisare completa
def afisare_glosar():
    if not glosar:
        print("Glosarul este gol.")
        return

    for termen, info in glosar.items():
        print("\nTermen:", termen)
        print("Definitie:", info["definitie"])
        print("Categorie:", info["categorie"])
        print("Exemplu:", info["exemplu"])


# 7. Statistici
def statistici():
    total = len(glosar)
    categorii = {}

    for termen in glosar:
        cat = glosar[termen]["categorie"]

        if cat not in categorii:
            categorii[cat] = 0

        categorii[cat] += 1

    print("\nNumar total termeni:", total)
    print("Termeni pe categorii:")

    for cat, nr in categorii.items():
        print(cat, ":", nr)


# 8. Salvare CSV
def salvare_csv():
    nume_fisier = input("Nume fisier CSV: ")

    with open(nume_fisier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["termen", "definitie", "categorie", "exemplu"])

        for termen, info in glosar.items():
            writer.writerow([
                termen,
                info["definitie"],
                info["categorie"],
                info["exemplu"]
            ])

    print("Glosar salvat in CSV.")


# 9. Incarcare CSV
def incarcare_csv():
    nume_fisier = input("Nume fisier CSV: ")

    try:
        with open(nume_fisier, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            glosar.clear()

            for row in reader:
                glosar[row["termen"]] = {
                    "definitie": row["definitie"],
                    "categorie": row["categorie"],
                    "exemplu": row["exemplu"]
                }

        print("Glosar incarcat.")
    except FileNotFoundError:
        print("Fisierul nu exista.")


# 10. Meniu interactiv
def meniu():
    while True:
        print("\n===== MENIU GLOSAR =====")
        print("1. Adauga termen")
        print("2. Cautare exacta")
        print("3. Cautare partiala")
        print("4. Actualizare termen")
        print("5. Stergere termen")
        print("6. Afisare glosar")
        print("7. Statistici")
        print("8. Salvare CSV")
        print("9. Incarcare CSV")
        print("0. Iesire")

        opt = input("Alege optiunea: ")

        if opt == "1":
            adauga_termen()
        elif opt == "2":
            cautare_exacta()
        elif opt == "3":
            cautare_partiala()
        elif opt == "4":
            actualizare_termen()
        elif opt == "5":
            stergere_termen()
        elif opt == "6":
            afisare_glosar()
        elif opt == "7":
            statistici()
        elif opt == "8":
            salvare_csv()
        elif opt == "9":
            incarcare_csv()
        elif opt == "0":
            print("Program inchis.")
            break
        else:
            print("Optiune invalida!")


# Pornirea programului
meniu()