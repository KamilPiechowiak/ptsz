# API v2

### Instrukcja:
1. Robimy submodule id${nasz_indeks} w src (na przykładzie id000000).
2. Implementujemy co trzeba (znowu - po przykład do id000000).
3. Wypełniamy my_properties.py naszym indeksem i go nie commitujemy.
4. `python3 p2/runner.py -h`
5. Jeżeli korzystamy z jakiś dodatkowych modułów, to wsadzamy je do requirements.txt.
Projekt ma innym działać po zainstalowaniu zależności z requirements.txt i odpaleniu.

### Założenia:
* tylko python
* bez io systemowego i kodowania znaków
* proste API - implementujemy klasy, które mają pojedynczą funkcję o ściśle określonym in/out [type hinting], które jest od razu walidowane

W celu skorzystania z mechanizmów typu type hinting należy wyjść z vima.