# Generar codigo markdown de los comentarios expuestos

## en Python

### Descripción
Este repositorio contiene ejemplos y ejercicios para aprender los comandos principales de GitHub Copilot.

### Recursos
- /doc: Agrega comentarios al codigo especificado o seleccionado.
- /explain: obtiene explicaciones sobre el codigo.
- /generate: genera codigo para responder a la pregunta especificada.
- /help: obtiene ayuda sobre como usar el chat de copilot
- /optimize: analiza y mejora el tiempo de ejecucion del codigo seleccionado
- /test: crea pruebas unitarias para el codigo seleccionado
- /fix: ayuda a resolver algun problema que se tenga en el codigo.
- /new: para crear un nuevo proyecto con las necesidades especificas.
- @terminal: Preguntas relacionadas con la linea de comando.
- @vscode: Agente para formular preguntas relacionadas con visual studio.
- #file:nameFile: Ayuda a copilot a centrarse en unicamente un archivo.

### Ejemplos de uso
- @workspace /explain #file:controller.js: traduce, dentro del entorno explique el archivo controller.js.
- #selection /fix: de la seleccion busque una posible solucion del error o bug
- /generate texto (especificar archivo): se le eindica que cree una determinada logica en un archivo.
- /optimize (el metodo) #file:nameFile.js: Optimizar un metodo en un archivo determinado.
- /test using mocha: Crea pruebas unitarias para un codigo seleccionado.


