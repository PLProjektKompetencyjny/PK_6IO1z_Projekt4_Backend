## Opis query params
 
- `!` : Wartość różna od podanej
- `*` : Wartość zawiera podany ciąg znaków
- `<` : Wartość jest mniejsza od podanej
- `>` : Wartość jest większa od podanej
- `^` : Wartość jest jednym z podanych elementów (wartości oddzielone są znakiem '|')
- `/` : Wartość jest pomiędzy dwoma podanymi wartościami (wartości oddzielone są znakiem '|')

## Przykłady użycia

- 127.0.0.1:5000/database/users?user_id=/1|5&user_e_mail=*wp* -> Zwróci użytkowników o id 1 lub 5, których e-mail zawiera wp
- 127.0.0.1:5000/database/users?user_id=1 -> Zwróci użytkownika o id 1
- 127.0.0.1:5000/database/users?user_id=>3 -> Zwróci użytkowników o id większym od 3
- 127.0.0.1:5000/database/users?user_id=<3 -> Zwróci użytkowników o id mniejszym od 3
- 127.0.0.1:5000/database/users?user_id=!1 -> Zwróci użytkowników o id różnym od 1

## JWT
Generowane przy wywołaniu żądania na endpoint `auth/sign-in` lub `auth/sign-up`.
Przy wywołaniu ww. endpoint'ów zostanie zwrócony obiekt:
```javascript
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lzX2FkbWluIjp0cnVlLCJ1c2VyX2lkIjo0LCJlbWFpbCI6IkFETUlOIiwiZXhwIjoxNzE3NzgyMDg5LCJpYXQiOjE3MTc3Nzg0ODksInN1YiI6NH0.zYRVrJ8nNjDq69moa6_Lbl9KQDemof91f-RuUs-_rTw",
  "auth_schema": "Bearer",
  "email": "ADMIN",
  "is_admin": true,
  "user_id": 4
}
```
który zawiera:
- `access_token` - token autoryzujący, który powinien być umieszczony w nagłówku `Authorization` przy żądaniu do API,
- `auth_schema` - typ/schemat tego co znajduje się w nagłówku `Authorization`. **Tę wartość nie zmieniamy powinna być równa `Bearer`**,
- `email` - e-mail użytkownika/klienta, który się loguje (głównie używany na UI),
- `is_admin` - czy użytkownik, który się loguje jest administratorem (przysłowiową recepcjonistką),
- `user_id` - ID użytkownika w bazie danych.

Przykład żądania autoryzowanego przy wykorzystaniu pól `access_token` oraz `auth_schema`:
```
POST http://localhost:5000/api/auth/secured HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lzX2FkbWluIjp0cnVlLCJ1c2VyX2lkIjo0LCJlbWFpbCI6IkFETUlOIiwiZXhwIjoxNzE3NzgyMDg5LCJpYXQiOjE3MTc3Nzg0ODksInN1YiI6NH0.zYRVrJ8nNjDq69moa6_Lbl9KQDemof91f-RuUs-_rTw
```

### Jak tego używać?
#### Zabezpieczanie endpoint'a
Wystarczy, że do endpoint'u zostanie dopisany dekorator `@jwt_required()`, który należy zaimportować z:
```python
from flask_jwt_extended import jwt_required
```
następnie zaaplikować go na endpoint:
```python
@auth.route("auth/secured", methods=["POST"])
@jwt_required()
def secured():
  return jsonify(True)
```

#### Wyciągnięcie danych "sesyjnych" z JWT (access tokena)
W pliku [auth.py](src\controller\blueprint\auth.py) znajduje się metoda `decode_access_token`, która odszyfrowuje token przekazany w nagłówku `Authorization` przekazany wraz z żądaniem.
Jeśli nagłówek `Authorization` jest pusty to metoda `decode_access_token` zwróci `None`.
Przykład wykorzystania ww. metody:
```python
from src.controller.blueprint.auth import decode_access_token

@auth.route("twoj/endpoint", methods=["POST"])
# @jwt_required() - opcjonalne
def your_endpoint():
  data = decode_access_token()
  is_admin = data['user_is_admin']
  # alternatywnie data.get('user_is_admin')
  return jsonify(is_admin)
```
Dzięki temu jesteśmy w stanie zweryfikować czy użytkownik ma uprawnienia m.in. do modyfikacji ustawień pokoi, dostępnych serwisów czy zarządzaniem klientami.
