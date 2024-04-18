from manager import Manager

manager = Manager()


@manager.assign("saldo")
def saldo(manager):
    dodaj_odejmij_srodki = int(input("Chcesz dodać środki [0] do konta czy odjąć środki z konta [1]? "))
    if dodaj_odejmij_srodki not in [0, 1]:
        print("Coś poszło nie tak... musisz podać 0 -> dodanie środków lub 1 -> wypłatę środków")
        return

    kwota_operacji = int(input("Podaj kwotę operacji: "))
    if dodaj_odejmij_srodki == 0:
        manager.budzet_firmy += kwota_operacji
        manager.lista_operacji.append(f"Dodano środki w wysokości {kwota_operacji}")
    else:
        manager.budzet_firmy -= kwota_operacji
        manager.lista_operacji.append(f"Wypłacono środki w wysokości {kwota_operacji}")


@manager.assign("sprzedaz")
def sprzedaz(manager):
    nazwa = input("Podaj nazwę produktu, który chcesz sprzedać: ")
    producent_produktu = input("Podaj producenta produktu, który chcesz sprzedać: ")
    ilosc_do_sprzedazy = int(input("Ile sztuk chcesz sprzedać? "))
    znaleziono_produkt = False
    sprzedano_produkt = False

    for produkt in manager.magazyn:
        if produkt.get("nazwa_produktu") == nazwa and produkt.get("producent") == producent_produktu:
            znaleziono_produkt = True
            if produkt.get("ilosc_sztuk") >= ilosc_do_sprzedazy > 0:
                sprzedano_produkt = True
            else:
                print("Brak zadanej ilości produktu lub wynosi ona 0")
                print("Stan magazynowy produktu: ", produkt["ilosc_sztuk"])
                break

            if sprzedano_produkt:
                manager.budzet_firmy += (produkt.get("cena") * ilosc_do_sprzedazy)
                produkt["ilosc_sprzedanych_sztuk"] += ilosc_do_sprzedazy
                produkt["ilosc_sztuk"] -= ilosc_do_sprzedazy
                manager.lista_operacji.append(f"Sprzedano {ilosc_do_sprzedazy} sztuk produktu {nazwa}")
        else:
            print("Brak takiej pozycji w magazynie")
            break


@manager.assign("zakup")
def zakup(manager):
    nazwa_produktu = input("Podaj nazwę produktu, który chcesz kupić: ")
    producent = input("Podaj producenta produktu, który chcesz kupić: ")
    ilosc_sztuk_do_zakupu = int(input("Podaj ilość sztuk, które chcesz kupić: "))
    cena_jednostkowa = float(input("Podaj cenę produktu, który chcesz kupić: "))
    produkt_w_magazynie = False

    if ilosc_sztuk_do_zakupu > 0 and cena_jednostkowa > 0:
        if manager.budzet_firmy >= ilosc_sztuk_do_zakupu * cena_jednostkowa:
            for produkt in manager.magazyn:
                if produkt.get("nazwa_produktu") == nazwa_produktu and produkt.get("producent") == producent:
                    produkt_w_magazynie = True
                    if produkt_w_magazynie:
                        produkt["ilosc_sztuk"] += ilosc_sztuk_do_zakupu
                        break
            else:
                cena_do_sprzedazy = float(input("Podaj cenę do sprzedaży dla nowego produktu: "))
                manager.magazyn.append({
                    "nazwa_produktu": nazwa_produktu,
                    "producent": producent,
                    "ilosc_sztuk": ilosc_sztuk_do_zakupu,
                    "cena": cena_do_sprzedazy,
                    "ilosc_sprzedanych_sztuk": 0
                })

            manager.budzet_firmy -= (ilosc_sztuk_do_zakupu * cena_jednostkowa)
            manager.lista_operacji.append(
                f"Zakupiono {ilosc_sztuk_do_zakupu} sztuk produktu {producent} {nazwa_produktu}")
        else:
            print(f'Nie stać cię, twój budżet to {manager.budzet_firmy}')
    else:
        print("Ilość sztuk do zakupu oraz cena powinny być większe od 0!")


@manager.assign("konto")
def konto(manager):
    print(f"Bieżący stan konta: {manager.budzet_firmy}")


@manager.assign("lista")
def wyswietl_magazyn(manager):
    print("Lista produktów w magazynie:")
    for produkt in manager.magazyn:
        print(produkt)


@manager.assign("magazyn")
def stan_magazynu(manager):
    nazwa_produktu = input("Podaj nazwę produktu, dla którego chcesz wyświetlić stan magazynowy: ")
    producent = input("Podaj producenta produktu, dla którego chcesz wyświetlić stan magazynowy: ")
    for produkt in manager.magazyn:
        if produkt.get("nazwa_produktu") == nazwa_produktu and produkt.get("producent") == producent:
            print(produkt)
            break
    else:
        print("Brak poszukiwanego produktu w magazynie")


@manager.assign("przeglad")
def przeglad(manager):
    od = input("Podaj mi początkowy zakres: ")
    do = input("Podaj mi końcowy zakres: ")
    if od != "" and do != "":
        if not od.isnumeric() or not do.isnumeric():
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        elif int(od) < 0 or int(od) > len(manager.lista_operacji) or int(do) > len(manager.lista_operacji) or int(
                do) < int(od):
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        else:
            print(manager.lista_operacji[int(od):int(do)])
    elif od != "" and do == "":
        if not od.isnumeric():
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        elif int(od) < 0 or int(od) > len(manager.lista_operacji):
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        else:
            print(manager.lista_operacji[int(od):])
    elif od == "" and do != "":
        if not do.isnumeric():
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        elif int(do) > len(manager.lista_operacji):
            print(f'Podano liczbę spoza zakresu, zakres wynosi od 0 do {len(manager.lista_operacji)}')
        else:
            print(manager.lista_operacji[:int(do)])
    else:
        print(manager.lista_operacji)


@manager.assign("koniec")
def zakoncz(manager):
    manager.koniec_programu = True
    manager.instancja_file_handlera.zapis_do_pliku_z_magazynem_i_saldem(budzet_firmy=manager.budzet_firmy,
                                                                        magazyn=manager.magazyn)
    manager.instancja_file_handlera.zapis_do_pliku_z_historia(lista_operacji=manager.lista_operacji)


print("Witaj w naszym systemie zarządzania magazynem!")
while not manager.koniec_programu:
    operacja = input(
        "Wybierz co chcesz zrobić:\n1. Saldo\n2. Sprzedaż\n3. Zakup\n4. Konto\n5. Lista\n6. Magazyn\n7. Przegląd\n8. "
        "Zakończ program\n")
    if operacja == "1":
        manager.execute("saldo")
    elif operacja == "2":
        manager.execute("sprzedaz")
    elif operacja == "3":
        manager.execute("zakup")
    elif operacja == "4":
        manager.execute("konto")
    elif operacja == "5":
        manager.execute("lista")
    elif operacja == "6":
        manager.execute("magazyn")
    elif operacja == "7":
        manager.execute("przeglad")
    elif operacja == "8":
        manager.execute("koniec")


