Программа для очистки текстов от обсценной лексики.

Версия Python 2.7

Необходимые библиотеки:
gensim
pymorphy2
nltk

Программа обработает ваш текстовый документ, удалит предложения с обсценной лексикой и создаст обновленный документ.

Для работы требуется текстовый документ - список "стоп-слов".

Запуск программы происходит со следующими аргументами:

clear.py cursed.txt cured.txt stoplist.txt

где:
cursed - исходный файл
cured - итоговый файл     ### Если в папке нет такого документа - создается новый. Иначе он стирается и записывается по новой 
stoplist - путь к списку "стоп-слов"

При запуске без аргументов программа использует путь к файлам по умолчанию, который можно править в самой программе.
