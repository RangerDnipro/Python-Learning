# Як інтегрувати асинхронний код у вже існуючий синхронний проект на Python

Щоб додати новий асинхронний код до старого проекту, потрібно поступово адаптувати функціонал, зберігаючи баланс між старими та новими частинами.

## Як додати новий асинхронний код

1. **Почати використовувати asyncio та event loop**

   Можна зробити так, щоб старий код і новий асинхронний код працювали разом. Якщо потрібно виконати новий код, можна використовувати спеціальні функції, як `asyncio.run()`.

   **Приклад:**

   ```python
   import asyncio

   def sync_function():
       print("Це синхронна функція")

   async def async_function():
       loop = asyncio.get_event_loop()
       await loop.run_in_executor(None, sync_function)

   if __name__ == "__main__":
       asyncio.run(async_function())
   ```

2. **Змішування старого і нового коду**

   Можна залишити старий код і додати асинхронні задачі для нових функцій, які потребують неблокуючого виконання (наприклад, запити до API або тривалі обчислення). Це допоможе зробити виконання швидшим.

   **Приклад:**

   ```python
   import asyncio
   import time

   def sync_function():
       print("Це синхронна функція")
       time.sleep(2)
       print("Синхронна функція завершена")

   async def async_function():
       print("Це асинхронна функція")
       await asyncio.sleep(1)
       print("Асинхронна функція завершена")

   async def main():
       loop = asyncio.get_event_loop()
       await loop.run_in_executor(None, sync_function)
       await async_function()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

3. **Використання окремих потоків або процесів**

   Якщо старий код не можна змінити, його можна запускати в окремому потоці або процесі. Це дозволить йому працювати одночасно з новим асинхронним кодом.

   **Приклад з потоками:**

   ```python
   import threading
   import time

   def sync_function():
       print("Це синхронна функція")
       time.sleep(2)
       print("Синхронна функція завершена")

   def main():
       thread = threading.Thread(target=sync_function)
       thread.start()
       print("\nПаралельне виконання триває...")
       thread.join()

   if __name__ == "__main__":
       main()
   ```

   **Приклад з процесами:**

   ```python
   import multiprocessing
   import time

   def sync_function():
       print("Це синхронна функція")
       time.sleep(2)
       print("Синхронна функція завершена")

   def main():
       process = multiprocessing.Process(target=sync_function)
       process.start()
       print("Паралельне виконання триває...")
       process.join()

   if __name__ == "__main__":
       main()
   ```

# Підводні камені використання асинхронних бібліотек при роботі з базами даних

1. **Бібліотеки для роботи з базами даних**

   Не всі бібліотеки баз даних підтримують асинхронний код. Можна використовувати спеціальні бібліотеки, як `aiomysql` або `asyncpg`, які зроблені для асинхронного використання.

2. **Блокування коду**

   Навіть асинхронні бібліотеки іноді можуть блокувати код, роблячи його повільнішим. Можна використовувати спеціальні інструменти, щоб уникнути блокування та прискорити виконання.

   **Приклад:**

   ```python
   import asyncio
   import time
   from concurrent.futures import ThreadPoolExecutor

   def blocking_function():
       time.sleep(2)
       print("Блокуюча операція завершена")

   async def main():
       loop = asyncio.get_event_loop()
       with ThreadPoolExecutor() as executor:
           await loop.run_in_executor(executor, blocking_function)

   if __name__ == "__main__":
       asyncio.run(main())
   ```

3. **Робота з транзакціями**

   Коли вносяться зміни до бази даних, важливо, щоб ці зміни виконувалися правильно, навіть якщо щось піде не так. Треба перевіряти, щоб код міг скасувати зміни, якщо сталася помилка.

   **Приклад з SQLite:**

   ```python
   import aiosqlite
   import asyncio

   async def run_transaction():
       async with aiosqlite.connect('example.db') as db:
           try:
               await db.execute('BEGIN')
               await db.execute('INSERT INTO users(name) VALUES(?)', ("Ім'я користувача",))
               await db.execute('INSERT INTO orders(user_id, amount) VALUES(?, ?)', (1, 100))
               await db.commit()
           except Exception as e:
               await db.rollback()
               print(f"Помилка при виконанні транзакції: {e}")

   if __name__ == "__main__":
       asyncio.run(run_transaction())
   ```

4. **Змішування старого і нового коду**

   Змішування старого синхронного та нового асинхронного коду може бути складним. Старий код може зупинити виконання нового асинхронного коду, якщо вони не працюють правильно разом. Щоб уникнути цього, можна використовувати спеціальні обгортки або інструменти, щоб вони могли працювати паралельно без перешкод.
