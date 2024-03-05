**Документация**\
Tester - приложение для проверки знаний учащихся по отдельным предметам на языке Python c быстрой проверкой и доступом ответов.
Можно решать задачи по выбранному предмету на выбранную тему в своем аккаунте или без регистрации. Полученные ответы записываются в отдельный файл.

**Настройка программы**\
Необходимые для работы приложения модули перечислены в файле requirements.txt
Для установки модулей ввести в терминал команду **$ pip install -r requirements.txt**

**Установка программы не требуется.**

**Запуск программы**\
Запустить приложение из файла Tester\dist\main.exe

**Инструкция**\
При запуске открывается главное окно. В нем содержатся кнопки "Войти" и "Зарегестрироваться", при нажатии которых открываются окна входа и регистрации соответственно. При регистрации данные добавляются в базу данных и сохраняются там, чтобы новый пользователь смог войти.

Есть фильтр по предметам и темам. Нужно выбрать сначала предмет, затем нужную тему. Затем нажать кнопку "Отфильтровать", после чего появится список тестов. Если список пустой, значит тема выбрана не верно и не соответствует предмету, или вообще не выбрана. Следует попробовать еще раз.
Далее выбираете нужный тест и переходите к задачам, нажав соответствующую кнопку. 

Открывается окно с задачами. В нем можно вернуться в главное окно, нажав кнопку "Назад". Задачи перелистываются стрелочками. Если вы заходите пропустить задачу и вернуться к ней позже, то другие ответы не сохрянятся и придется вводить ответы заново. Поэтому решать задания следует по порядку.

При нажатии кнопки "Завершить" открывается окно статистики, содержащее в себе таблицу с результатами. После завершения ответы записываются в файл answers.txt, где будет указана вся нужная информация для учителя.