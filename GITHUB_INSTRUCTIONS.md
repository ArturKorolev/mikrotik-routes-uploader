# 📤 Инструкция по загрузке на GitHub

## Шаг 1: Подготовка локального репозитория

1. **Откройте терминал/PowerShell** в папке с вашим проектом:
   ```
   c:\Users\artur\OneDrive\Рабочий стол\ZapretНастройка\lists\Загрузка в микрот
   ```

2. **Инициализируйте Git репозиторий:**
   ```bash
   git init
   ```

3. **Конфигурируйте Git** (первый раз):
   ```bash
   git config --global user.name "Ваше имя"
   git config --global user.email "ваш.email@example.com"
   ```

## Шаг 2: Подготовка файлов

Убедитесь, что в папке находятся:
```
✓ upload_route_gui.py      (основное приложение)
✓ routes_handler.py         (модуль с логикой)
✓ chatgpt.txt              (пример файла со списком)
✓ requirements.txt         (зависимости)
✓ README.md                (документация)
✓ LICENSE                  (лицензия MIT)
✓ .gitignore               (исключенные файлы)
```

❌ **Удалите консольную версию:**
```bash
rm upload_route_api.py
# или через PowerShell:
# Remove-Item upload_route_api.py
```

## Шаг 3: Добавить файлы в Git

```bash
git add .
```

Проверить, какие файлы будут добавлены:
```bash
git status
```

## Шаг 4: Первый коммит

```bash
git commit -m "Initial commit: MikroTik Routes Uploader GUI"
```

## Шаг 5: Создание репозитория на GitHub

1. **Откройте** https://github.com/new

2. **Заполните форму:**
   - **Repository name:** `mikrotik-routes-uploader`
   - **Description:** `GUI application for uploading routes to MikroTik`
   - **Public** (публичный)
   - **Add a README file:** НЕ СТАВЬТЕ (у вас уже есть README.md)
   - **Add .gitignore:** НЕ СТАВЬТЕ (у вас уже есть .gitignore)
   - **Choose a license:** MIT License (опционально, у вас уже есть LICENSE)

3. **Нажмите** "Create repository"

## Шаг 6: Подключение локального репозитория к GitHub

GitHub покажет команды. Выполните их в терминале:

```bash
git branch -M main
git remote add origin https://github.com/ВАШ_ЮЗЕРНЕЙМ/mikrotik-routes-uploader.git
git push -u origin main
```

**Заменьте `ВАШ_ЮЗЕРНЕЙМ`** на ваше имя пользователя GitHub.

## Шаг 7: Аутентификация

При первой отправке GitHub может запросить аутентификацию.

### Вариант A: Personal Access Token (рекомендуется)

1. Перейдите на https://github.com/settings/tokens
2. Нажмите "Generate new token"
3. Выберите scopes: `repo` (полный доступ к репозиториям)
4. Скопируйте токен
5. Когда Git запросит пароль, вставьте токен (не пароль!)

### Вариант B: GitHub Desktop

Установите GitHub Desktop (проще для начинающих):
https://desktop.github.com/

## Шаг 8: Проверка

1. Откройте https://github.com/ВАШ_ЮЗЕРНЕЙМ/mikrotik-routes-uploader
2. Проверьте, что все файлы загружены
3. README.md должен отобразиться красиво

## Последующие обновления

Когда вы меняете файлы:

```bash
# 1. Добавить изменения
git add .

# 2. Создать коммит
git commit -m "Описание изменений"

# 3. Отправить на GitHub
git push
```

## Полезные Git команды

```bash
# Проверить статус
git status

# Посмотреть историю коммитов
git log --oneline

# Отменить последний коммит (если не отправили)
git reset --soft HEAD~1

# Посмотреть отличия
git diff

# Удалить файл из Git (но не с диска)
git rm --cached имя_файла.txt
git commit -m "Remove file"
```

## Структура GitHub репозитория

После загрузки на GitHub репозиторий должен выглядеть так:

```
mikrotik-routes-uploader/
├── upload_route_gui.py
├── routes_handler.py
├── chatgpt.txt
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── GITHUB_INSTRUCTIONS.md  (этот файл)
```

## Теги и релизы (опционально)

Для удобства можно создавать теги версий:

```bash
git tag -a v1.0 -m "Version 1.0 - Initial Release"
git push origin v1.0
```

После этого в GitHub появится раздел "Releases".

## Бейджи для README.md (опционально)

Добавьте в начало README.md для красоты:

```markdown
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
```

## Ошибки и их решения

**Ошибка: "fatal: not a git repository"**
```bash
git init
```

**Ошибка: "Permission denied" при git push**
- Используйте Personal Access Token вместо пароля

**Ошибка: "rejected ... non-fast-forward"**
```bash
git pull origin main
git push origin main
```

---

После загрузки вы сможете поделиться ссылкой: `https://github.com/ВАШ_ЮЗЕРНЕЙМ/mikrotik-routes-uploader`
