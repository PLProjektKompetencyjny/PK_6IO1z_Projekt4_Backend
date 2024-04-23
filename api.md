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
