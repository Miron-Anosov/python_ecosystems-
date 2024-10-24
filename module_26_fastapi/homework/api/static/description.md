
# Рецепты API

## Endpoints

### `GET /recipes/status-ok`
Возвращает статус "OK" для проверки работоспособности API.

### `GET /recipes/`
Возвращает список всех рецептов.

### `POST /recipes/`
Создает новый рецепт.

### `GET /recipes/{recipe_id}`
Возвращает рецепт по его ID.

### `POST /recipes/collection`
Создает несколько новых рецептов за один запрос.

# Data schemes:

## Request API:
### Recipe
- `name *`: Название блюда (строка от 2 до 50 символов)
- `time *`: Время приготовления (целое число)
- `ingredients *`: Список ингредиентов (строка от 3 до 250 символов)
- `description *`: Инструкция по приготовлению (строка от 10 до 500 символов)


## Response API:
### Recipe
- `name *`: Название блюда (строка от 2 до 50 символов)
- `recipe_id `: Уникальный идентификатор рецепта (целое число). Создается автоматически при создании записи в базе
- `time *`: Время приготовления (целое число)
- `ingredients *`: Список ингредиентов (строка от 3 до 250 символов)
- `description *`: Инструкция по приготовлению (строка от 10 до 500 символов)


### List all Recipes:
     Рецепты отсортированы по популярности (количество просмотров - сколько раз открыли детальный рецепт)
     чем чаще открывают рецепт, тем он популярнее. В случае совпадения значений сортировать по времени готовки.
- `recipe_id *` Уникальный идентификатор рецепта (целое число). Создается автоматически при создании записи в базе
- `time *`: Время приготовления (целое число)
- `view *`: Кол-во обновляется при `GET /recipes/{recipe_id}`

### Validation Error
- `detail`: Массив объектов с информацией об ошибках валидации
  - `loc`: Путь к полю с ошибкой
  - `msg`: Сообщение об ошибке
  - `type`: Тип ошибки