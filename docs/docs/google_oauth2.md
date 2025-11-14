# Как получить Google OAuth2 ключи — просто и очень подробно (как для пятилетнего)

Представь, что у твоего приложения есть волшебный ключ (ключ и секрет), который позволяет ему входить в дом Google и просить разрешение посмотреть одну комнату (данные пользователя). Ниже шаги, что нужно сделать, с простыми пояснениями и примерами.

---

## Коротко в одном предложении
1. Создать проект в Google Cloud Console.  
2. Настроить экран согласия (OAuth consent screen).  
3. Создать учетные данные "OAuth 2.0 Client ID" (получишь client_id и client_secret).  
4. Добавить Redirect URI и сохранить JSON с данными.  
5. Хранить секрет безопасно и тестировать.

---

## Подробные шаги

### 1) Заходим в Google Cloud Console
- Открой https://console.cloud.google.com/.
- Если нет аккаунта Google — создай.
- Создай новый проект (нажми "Select a project" → "New Project"). Назови как хочешь.
- Проект — это как коробка, в которой будут все твои ключи.

### 2) Включаем нужные API (опционально, но часто нужно)
- Перейди в APIs & Services → Library.
- Найди API, который будешь использовать (например, Google People API, Gmail API и т.д.) и нажми Enable.
- Это как включить лампочку, чтобы приложение могло попросить нужные данные.

### 3) Настраиваем экран согласия (OAuth consent screen)
- Зайдите в APIs & Services → OAuth consent screen.
- Выбери тип пользователя:
    - Internal — только для G Suite организации (если у тебя корпоративный аккаунт).
    - External — для всех пользователей (обычно это нужно).
- Заполни поля (App name, User support email).
- Добавь логотип и домен, если есть (необязательно для теста).
- Scopes: укажи какие данные просишь (например, email, profile, https://www.googleapis.com/auth/userinfo.profile). Чем больше прав — тем строже проверка со стороны Google.
- Test users: если app type = External и проект не верифицирован, добавь своих тестовых пользователей (их Google аккаунты), чтобы они могли проходить авторизацию.
- Сохрани.

Пояснение как для ребёнка: экран согласия — это табличка, где Google спрашивает у человека: "Ты разрешаешь приложению смотреть твои вещи?" Ты говоришь, какие вещи оно может просмотреть.

### 4) Создаём учетные данные (Credentials)
- Перейди в APIs & Services → Credentials.
- Нажми "Create Credentials" → "OAuth client ID".
- Выбери тип приложения:
    - Web application — для веб-серверов (например, backend).
    - Desktop app — настольные приложения.
    - Android / iOS — мобильные.
    - Other (или "Desktop") — для командной строки, тестов.
- Для Web application укажи Authorized redirect URIs — обязательный шаг:
    - Пример для локальной разработки: http://localhost:3000/oauth2callback
    - Для production: https://yourdomain.com/oauth2callback
- Создай — получишь:
    - client_id (публичный идентификатор)
    - client_secret (секрет, как пароль)

Это и есть твои "ключи". Сохрани их.

### 5) Скачиваем JSON
- После создания рядом обычно есть иконка "Download" (JSON).
- Сохрани файл, например google_oauth_client.json.
- Пример содержимого (уменьшенный):
```
{
    "web": {
        "client_id": "12345-abcdef.apps.googleusercontent.com",
        "project_id": "my-project-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "GOCSPX-very_secret_value",
        "redirect_uris": ["http://localhost:3000/oauth2callback"]
    }
}
```

### 6) Как использовать (общая схема)
1. Приложение пересылает пользователя на Google URL авторизации с параметрами:
     - client_id, redirect_uri, response_type=code, scope, state.
2. Пользователь заходит, соглашается.
3. Google перенаправляет пользователя на redirect_uri с кодом (code).
4. Приложение отправляет POST на token_uri (https://oauth2.googleapis.com/token) с client_id, client_secret, code и получает access_token (и refresh_token).
5. С access_token можно вызывать API.

Пример запроса обмена кода на токен (curl):
```
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

client_id=...&client_secret=...&code=...&grant_type=authorization_code&redirect_uri=http://localhost:3000/oauth2callback
```

### 7) Refresh token и срок жизни
- access_token живёт недолго (обычно 1 час).
- refresh_token позволяет получить новый access_token без участия пользователя.
- Google выдает refresh_token при первом согласии; при повторных авторизациях его может не выдавать, если не указаны prompt=consent.

### 8) Безопасность (важно)
- client_secret — хранить в переменных окружения или секретном хранилище (не в публичных репозиториях).
- Не публикуй JSON с секретом.
- Настрой URI редиректов строго (в whitelist) — иначе ключи могут быть использованы посторонними.
- Ротация: если секрет скомпрометирован — сгенерируй новый и отозви старый.

### 9) Верификация приложения
- Если запрашиваешь чувствительные или restricted scopes (например Gmail, Drive, Calendar с изменением данных), Google может попросить пройти верификацию приложения — предоставь домен, политику конфиденциальности, видео того как работает приложение и т.д.
- Для разработки и тестирования обычно хватает режима тестовых пользователей.

### 10) Частые проблемы и их решения
- "redirect_mismatch" — redirect URI в запросе не совпадает с тем, что в настройках → исправь в консоли.
- "access_denied" — пользователь отказался или scope некорректен.
- Нет refresh_token — добавь параметр prompt=consent и access_type=offline в авторизационный запрос.
- Ошибки валидации при верификации — читай сообщения в консоли и следуй шагам.

---

## Полезные ссылки
- Google Cloud Console: https://console.cloud.google.com/
- Документация OAuth2 Google: https://developers.google.com/identity/protocols/oauth2

---

Если нужно, могу:
- Прописать пример авторизационного URL и обмена кода на токен для твоего redirect_uri.
- Сгенерировать пример конфигурации для Node.js / Python с использованием client_id/client_secret.