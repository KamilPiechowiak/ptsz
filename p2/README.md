# API v2

### Instrukcja:
1. Robimy submodule id${nasz_indeks} w src (na przykładzie id000000)
1. Implementujemy co trzeba (znowu - po przykład do id000000)
1. Wypełniamy my_properties.py naszym indeksem i go nie commitujemy. Żeby nie commitować, można skorzystać z `git update-index --assume-unchanged p2/my_properties.py`
1. `python3 p2/runner.py -h`
1. Po wrzuceniu instancji dopisujemy indeks do `INDICES` w `properties.py`.
1. W `properties.py` jest też `EPS` - z taką dokładnością sprawdzamy wynik. Różnica względna lub różnica bezwzględna wyników `< EPS`

### Założenia:
* tylko python
* bez io systemowego i kodowania znaków
* proste API - implementujemy klasy, które mają pojedynczą funkcję o ściśle określonym in/out [type hinting], które jest od razu walidowane

W celu skorzystania z mechanizmów typu type hinting należy wyjść z vima.