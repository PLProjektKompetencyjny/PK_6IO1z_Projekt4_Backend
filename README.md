
# PK_6IO1z_Projekt4_Backend

Projekt PK_6IO1z_Projekt4_Backend jest aplikacją backendową napisaną w Pythonie, która...

## Wymagania

- Python 3.x
- pip

## Struktura Katalogów

- `src`: Katalog zawierający kod źródłowy aplikacji.
    - `config.py`: Plik konfiguracyjny aplikacji.
    - `model`: Katalog zawierający model bazy dancyh używany w aplikacji.
    - `controller`: Katalog zawierający wszystkie endpointy aplikacji.
    - `service`: Katalog zawierający całą logikę biznesową aplikacji.
- `test`: Katalog zawierający testy jednostkowe dla aplikacji.
    - `test_config.py`: Plik zawierający testy konfiguracji aplikacji.
    - `model`: Katalog zawierający testy dla modelu bazy danych.
    - `controller`: Katalog zawierający testy dla endpointów aplikacji.
    - `service`: Katalog zawierający testy dla logiki biznesowej aplikacji.

## Instalacja

Aby zainstalować wszystkie wymagane zależności, wykonaj następujące polecenia:

```bash
source ./env/bin/activate
pip install -r requirements.txt
```

## Uruchomienie aplikacji

Aby uruchomić aplikację, wykonaj następujące polecenia:

```bash
source ./env/bin/activate
python3 manage.py run
```

## Uruchomienie aplikacji poprzez Docker

- TODO

## Testy

Aby uruchomić testy, wykonaj następujące polecenia:

```bash
source ./env/bin/activate
python3 manage.py test
```

## Dokumentacja API

Opis API znajduje się w pliku `API.md`.

## Autorzy

- Grzegorz Kubicki
- Przemysław Kowalski
- Stanisław Horna
- Łukasz Soboń
- Arkadiusz Bienias
