import csv
import json


def citeste_produse_csv(fisier):
    produse = {}
    with open(fisier, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linie in reader:
                id_produs = linie["id"]
                produse[id_produs] = {
                    "nume": linie["nume"],
                    "pret": float(linie["pret"]),
                    "stoc": int(linie["stoc"])
                }
    return produse


def citeste_reduceri_json(fisier):
    reduceri = {}
    with open(fisier, mode="r", encoding="utf-8") as f:
            reduceri = json.load(f)

    return reduceri


def afiseaza_meniu(produse):
    print("\n--- MENIU PRODUSE ---")
    for id_produs, detalii in produse.items():
        print(
            f"ID: {id_produs} | "
            f"Nume: {detalii['nume']} | "
            f"Pret: {detalii['pret']:.2f} lei | "
            f"Stoc: {detalii['stoc']}"
        )
    print()


def adauga_produs(comanda, produse, id_produs, cantitate):
    if id_produs not in produse:
        print("ID produs invalid.")
        return

    if cantitate <= 0:
        print("Cantitatea trebuie sa fie mai mare decat 0.")
        return

    cantitate_deja_comandata = comanda.get(id_produs, 0)
    stoc_disponibil_real = produse[id_produs]["stoc"] - cantitate_deja_comandata

    if cantitate > stoc_disponibil_real:
        print("Cantitatea depaseste stocul disponibil.")
        return

    comanda[id_produs] = cantitate_deja_comandata + cantitate
    print("Produs adaugat in comanda.")


def scade_produs(comanda, id_produs, cantitate):
    if id_produs not in comanda:
        print("Produsul nu exista in comanda.")
        return

    if cantitate <= 0:
        print("Cantitatea trebuie sa fie mai mare decat 0.")
        return

    if cantitate > comanda[id_produs]:
        print("Cantitatea de scazut este mai mare decat cea din comanda.")
        return

    comanda[id_produs] -= cantitate

    if comanda[id_produs] == 0:
        del comanda[id_produs]

    print("Comanda a fost actualizata.")


def calculeaza_total(comanda, produse):
    total = 0
    for id_produs, cantitate in comanda.items():
        total += cantitate * produse[id_produs]["pret"]
    return total


def calculeaza_reducere(total, tip_reducere, reduceri):
    if tip_reducere == "" or tip_reducere == "fara reducere":
        return 0

    if tip_reducere not in reduceri:
        print("Tip de reducere invalid.")
        return 0

    regula = reduceri[tip_reducere]
    prag = regula["prag"]
    tip = regula["tip"]
    valoare = regula["valoare"]

    if total < prag:
        print(f"Total insuficient pentru reducerea {tip_reducere}.")
        return 0

    if tip == "procent":
        reducere = total * valoare / 100
    elif tip == "fix":
        reducere = valoare
    else:
        print("Tip de reducere necunoscut in JSON.")
        return 0

    if reducere > total:
        reducere = total

    return reducere


def genereaza_bon(comanda, produse, total, reducere):
    linii = []
    linii.append("========== BON FISCAL ==========")

    for id_produs, cantitate in comanda.items():
        nume = produse[id_produs]["nume"]
        pret = produse[id_produs]["pret"]
        subtotal = cantitate * pret
        linii.append(
            f"{nume} | cantitate: {cantitate} | pret unitar: {pret:.2f} lei | subtotal: {subtotal:.2f} lei"
        )

    total_final = total - reducere
    if total_final < 0:
        total_final = 0

    linii.append("--------------------------------")
    linii.append(f"Total: {total:.2f} lei")
    linii.append(f"Reducere: {reducere:.2f} lei")
    linii.append(f"Total final: {total_final:.2f} lei")
    linii.append("================================")

    return "\n".join(linii)


def scrie_bon_txt(fisier, text_bon):
    try:
        with open(fisier, mode="w", encoding="utf-8") as f:
            f.write(text_bon)
        print(f"Bonul a fost salvat in fisierul {fisier}.")
    except Exception as e:
        print(f"Eroare la scrierea bonului: {e}")


def goleste_comanda(comanda):
    comanda.clear()


def afiseaza_meniu_principal():
    print("\n=== CAFENEA - MENIU PRINCIPAL ===")
    print("1 - Afisare meniu produse")
    print("2 - Adaugare produs in comanda")
    print("3 - Scadere/eliminare produs din comanda")
    print("4 - Aplicare reducere")
    print("5 - Finalizare comanda")
    print("6 - Anulare comanda")
    print("0 - Iesire")


def afiseaza_submeniu_reduceri():
    print("\n--- SUB-MENIU REDUCERI ---")
    print("1 - student")
    print("2 - happy")
    print("3 - cupon")
    print("4 - fara reducere")
    print("0 - inapoi")


# Initializare
produse = citeste_produse_csv("produse.csv")
reduceri = citeste_reduceri_json("reduceri.json")
comanda = {}
reducere_curenta = ""

# Daca fisierele nu au fost citite corect, programul se poate opri
if not produse:
    print("Nu exista produse disponibile. Programul se inchide.")
else:
    while True:
        afiseaza_meniu_principal()
        optiune = input("Alege o optiune: ")

        if optiune == "1":
            afiseaza_meniu(produse)

        elif optiune == "2":
            id_produs = input("Introdu ID-ul produsului: ")
            try:
                cantitate = int(input("Introdu cantitatea: "))
                adauga_produs(comanda, produse, id_produs, cantitate)
            except ValueError:
                print("Cantitatea trebuie sa fie numar intreg.")

        elif optiune == "3":
            id_produs = input("Introdu ID-ul produsului: ")
            try:
                cantitate = int(input("Introdu cantitatea de scazut: "))
                scade_produs(comanda, id_produs, cantitate)
            except ValueError:
                print("Cantitatea trebuie sa fie numar intreg.")

        elif optiune == "4":
            total = calculeaza_total(comanda, produse)

            if total == 0:
                print("Comanda este goala.")
            else:
                afiseaza_submeniu_reduceri()
                opt_reducere = input("Alege o optiune: ")

                if opt_reducere == "1":
                    reducere_test = calculeaza_reducere(total, "student", reduceri)
                    if reducere_test > 0:
                        reducere_curenta = "student"
                        print("Reducerea student a fost aplicata.")
                    else:
                        reducere_curenta = ""

                elif opt_reducere == "2":
                    reducere_test = calculeaza_reducere(total, "happy", reduceri)
                    if reducere_test > 0:
                        reducere_curenta = "happy"
                        print("Reducerea happy a fost aplicata.")
                    else:
                        reducere_curenta = ""

                elif opt_reducere == "3":
                    reducere_test = calculeaza_reducere(total, "cupon", reduceri)
                    if reducere_test > 0:
                        reducere_curenta = "cupon"
                        print("Reducerea cupon a fost aplicata.")
                    else:
                        reducere_curenta = ""

                elif opt_reducere == "4":
                    reducere_curenta = ""
                    print("Reducerea a fost resetata.")

                elif opt_reducere == "0":
                    print("Revenire in meniul principal.")

                else:
                    print("Optiune invalida.")

        elif optiune == "5":
            total = calculeaza_total(comanda, produse)

            if total == 0:
                print("Nu exista produse in comanda.")
            else:
                reducere = calculeaza_reducere(total, reducere_curenta, reduceri)
                text_bon = genereaza_bon(comanda, produse, total, reducere)

                print("\n" + text_bon)
                scrie_bon_txt("bon.txt", text_bon)

                for id_produs, cantitate in comanda.items():
                    produse[id_produs]["stoc"] -= cantitate

                goleste_comanda(comanda)
                reducere_curenta = ""
                print("Comanda a fost finalizata.")

        elif optiune == "6":
            goleste_comanda(comanda)
            reducere_curenta = ""
            print("Comanda a fost anulata.")

        elif optiune == "0":
            print("Programul s-a inchis.")
            break

        else:
            print("Optiune invalida.")