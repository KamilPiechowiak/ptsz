# PTSZ

## Instancje
Instancje nazywamy według schematu `{numer_indeksu}_{rozmiar}.in`, np. `136780_50.in`. Umieszczamy je w {numer_projektu}/instances. Każdy musi wygenerować po jednej instancji dla rozmiarów `n in range(50, 501, 50)`. Po dodaniu instancji, aktualizujemy listę `indices` w pliku metadata.py. Do arkusza wpisujemy się w tej samej kolejności co do listy `indices`.

## Algorytm
Swój algorytm umieszczamy w `{numer_projektu}/src`. Po dodaniu programu, aktualizujemy słownik `program_commands` w pliku metadata.py, podając dla klucza będącego swoim numerem indeksu polecenie do uruchomienia programu.

## Weryfikator
Weryfikator każdy pisze sam. Jednak, żeby skorzystać ze skryptów obliczających wyniki zbiorcze, powinien on przestrzegać następujących wymagań:
1. Weryfikator przyjmuje dokładnie 3 argumenty:
    1. W przypadku testowania pliku wynikowego są to `ścieżka_do_instancji o ścieżka_do_pliku_wynikowego`, np. `1/instances/136780_50.in o seq.out`.
    1. W przypadku testowania programu są to `ścieżka_do_instancji p komenda_wywołująca_program`, np. `1/instances/136780_50.in p 1/src/sample136780.py`.
1. Weryfikator wypisuje na standardowe wyjście:
    1. W przypadku testowania pliku wynikowego wypisuje **dokładnie** 2 liczby oddzielone pojedynczą spacją. Są to `czy_poprawny wartość_kryterium`. Wartość `czy_poprawny` wynosi 1, jeśli obliczone wartości kryterium się zgadzają, 0 w przeciwnym przypadku.
    1. W przypadku testowania algorytmu wypisuje **dokładnie** 3 liczby oddzielone pojedynczymi spacjami. Są to `czy_poprawny wartość_kryterium czas_wykonania`. Dwa pierwsze argumenty są takie jak powyżej. Czas wykonania zwracamy w ms.

## Weryfikacja weryfikatorów
Aby uruchomić swój weryfikator na wszystkich instancjach, można skorzystać ze skryptu `validate_validator.py`. Przyjmuje on 2 argumenty: `numer_projektu polecenie_wywołujące_weryfikator`

## Testowanie algorytmów
Aby uruchomić wszystkie algorytmy na swoich instancjach, można skorzystać ze skryptu `test_programs.py`. Przyjmuje on 3 argumenty: `numer_projektu polecenie_wywołujące_weryfikator numer_indeksu`