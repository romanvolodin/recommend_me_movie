# Посоветуй мне кино

Скрипт рекомендует похожее кино основываясь на введенном названии фильма.

## Требования

Для запуска нужен Python 3.6 или выше.  
Также потребуется ключ для доступа к API [The Movie Database](https://www.themoviedb.org/). Подробная инструкция [как получить ключ](https://developers.themoviedb.org/3/getting-started/introduction).

## Переменные окружения

Настройки проекта берутся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `recommend_me_movie.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ = значение`.

Доступные переменные:

- `RMM_API_KEY` — ключ для доступа к API The Movie Database. Подробная инструкция [как получить ключ](https://developers.themoviedb.org/3/getting-started/introduction).
- `RMM_LANGUAGE` — язык ответа API, на котором будет название фильма, его описание и др.

Пример:

```env
RMM_API_KEY = e6be2438b008ef8093630b28
RMM_LANGUAGE = ru-RU
```

## Запуск

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Запустите скрипт:

```sh
python recommend_me_movie.py Terminator
```

Пример вывода:
```sh

```

## Цели проекта

Код написан в учебных целях.