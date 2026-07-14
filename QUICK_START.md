# 🚀 Быстрый гайд по загрузке на GitHub

## За 5 минут до GitHub 🏃‍♂️

### 1️⃣ Удалите консольную версию
```powershell
Remove-Item upload_route_api.py
```

### 2️⃣ Инициализируйте Git
```bash
git init
git config --global user.name "Ваше имя"
git config --global user.email "email@example.com"
```

### 3️⃣ Добавьте все файлы
```bash
git add .
git status
```

### 4️⃣ Создайте коммит
```bash
git commit -m "Initial commit: MikroTik Routes Uploader"
```

### 5️⃣ Создайте репозиторий на GitHub
Перейдите на https://github.com/new и создайте пустой репозиторий с названием `mikrotik-routes-uploader`

### 6️⃣ Подключите репозиторий и отправьте
```bash
git branch -M main
git remote add origin https://github.com/ВАШЕ_ИМЯ/mikrotik-routes-uploader.git
git push -u origin main
```

### 7️⃣ Вводим учетные данные
- Если требуется пароль - используйте Personal Access Token (получить на https://github.com/settings/tokens)

---

## Что включать в репозиторий ✅

```
✓ upload_route_gui.py
✓ routes_handler.py
✓ chatgpt.txt (пример файла)
✓ requirements.txt
✓ README.md
✓ LICENSE
✓ .gitignore
✓ run.bat (запуск на Windows)
```

## Что НЕ включать ❌

```
❌ upload_route_api.py (консольная версия)
❌ __pycache__/
❌ *.pyc
❌ .venv/ / venv/
❌ .env (пароли!)
```

---

## Структура файлов после загрузки

```
mikrotik-routes-uploader/
├── README.md                      ← Отобразится на GitHub
├── LICENSE                        ← MIT License
├── .gitignore                     ← Какие файлы не загружать
├── GITHUB_INSTRUCTIONS.md         ← Детальная инструкция
│
├── upload_route_gui.py            ← Основное приложение
├── routes_handler.py              ← Логика работы
├── requirements.txt               ← Зависимости
│
├── run.bat                        ← Запуск на Windows
└── chatgpt.txt                    ← Пример файла со списками
```

---

## Проверка перед отправкой

```bash
# Посмотреть что будет загружено
git status

# Посмотреть дифф
git diff --cached

# Проверить конфиг
git config --global --list
```

---

## После первой загрузки

Все последующие изменения загружаются так:

```bash
git add .
git commit -m "Ваше описание изменений"
git push
```

---

## Полезные ссылки

- 📖 GitHub Docs: https://docs.github.com/
- 🔑 Создать токен: https://github.com/settings/tokens
- 📝 Git Cheat Sheet: https://github.githubassets.com/files/github/git-cheatsheet/git-cheatsheet.pdf
- 💬 Обсуждение проблем (Issues): https://github.com/YOUR_NAME/mikrotik-routes-uploader/issues

---

## Помощь

Если что-то не работает:

1. Проверьте установлен ли Git: `git --version`
2. Проверьте конфиг: `git config --global --list`
3. Посмотрите статус: `git status`
4. Прочитайте сообщения об ошибках внимательнее!

---

**После загрузки поделитесь ссылкой:**
```
https://github.com/ВАШЕ_ИМЯ/mikrotik-routes-uploader
```

Готово! 🎉
