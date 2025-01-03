## Теоретична частина:

1. Дайте визначення наступним термінам: XSS, SQL injection, CSRF, clickjacking, параметризовані запити, middleware, salt, hashing.
2. Опишіть основні вразливості, до яких може бути схильний додаток на Django, та способи їх запобігання.
3. Як захистити конфіденційні дані користувачів у Django-додатку? Які механізми шифрування можна використовувати?
4. Які способи аутентифікації та авторизації користувачів передбачені в Django? Опишіть їх переваги та недоліки.
5. Як забезпечити безпеку сесій користувачів? Які загрози можуть виникнути і як їх уникнути?
6. Які заходи можна вжити для захисту Django-додатка від DDoS атак?
7. Як захистити форми від підробки міжсайтових запитів (CSRF)?

## Практична частина:

### 1. Створіть мінімальний Django-додаток:

- Реалізуйте модель користувача з полями: username, email, password.
- Створіть форму для реєстрації та авторизації.
- Забезпечте безпечне зберігання паролів (hashing, salting).
- Встановіть CSRF protection.
- Додайте валідацію даних, що вводяться користувачем.
- Реалізуйте логіку виходу з системи.

### 2. Напишіть middleware:

- Створіть middleware, який буде логувати всі спроби доступу до захищених сторінок.
- Напишіть middleware для обробки помилок 404 та 500.

### 3. Перевірка безпеки:

- Використовуючи онлайн-сервіс для сканування вразливостей (наприклад, OWASP ZAP), проведіть сканування вашого локального Django-додатка.
- Виправте всі виявлені вразливості.

### 4. Захист від XSS:

- Продемонструйте, як захистити свій додаток від XSS атак за допомогою фільтрації даних та використання шаблонізатора Django.

### 5. Захист від SQL injection:

- Напишіть функцію для безпечного виконання SQL-запитів з використанням параметризованих запитів.

### 6. Захист від CSRF:

- Поясніть, як працює CSRF токен в Django і як його правильно використовувати.

## Додаткові завдання (за бажанням):

- Додайте захист від clickjacking до ваших шаблонів.
- Дослідіть додаткові методи захисту від DDoS атак, такі як використання CDN або WAF.
- Реалізуйте власну систему управління сесіями з використанням cookies або session storage.
- Проведіть аудит безпеки вашого Django-застосунку за допомогою інструментів статичного аналізу коду.

### Рекомендовані онлайн-сервіси для перевірки безпеки:

- OWASP ZAP: Безкоштовний інструмент з відкритим кодом для сканування веб-застосунків.
- Netsparker: Популярний комерційний сканер веб-застосунків.
- Burp Suite: Потужний інструмент для пентестування, який також може використовуватися для сканування веб-застосунків.

### Поради:

- Чим більше ви практикуватимете, тим краще ви будете розуміти принципи безпеки в Django.
- Офіційна документація Django містить багато корисної інформації щодо безпеки.
- Слідкуйте за новинами в сфері веб-безпеки, щоб бути в курсі нових загроз і способів їх запобігання.
