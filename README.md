# Documentacion del contenido del repositorio

## Vision general
Este proyecto contiene un ejercicio pequeno en Python para realizar operaciones basicas entre dos numeros y un archivo de pruebas automatizadas con `pytest`.

## Archivos del repositorio

| Archivo | Lo que contiene |
| --- | --- |
| `01.calculate.py` | Script interactivo de calculadora basica. |
| `test_01.calculate.py` | Pruebas unitarias para la funcion principal del script. |
| `.gitignore` | Reglas para excluir archivos temporales, entornos virtuales y artefactos de Python del control de versiones. |

## Detalle por archivo

### `01.calculate.py`
Este archivo implementa una calculadora simple y mezcla logica de negocio con ejecucion interactiva en el nivel principal del script.

Contiene lo siguiente:

1. Un mensaje de bienvenida almacenado en la variable `bienvenido`.
2. Un `print` que muestra ese mensaje al iniciar el programa.
3. Dos lecturas por teclado con `input(...)` para capturar los valores `num1` y `num2`.
4. Conversion de ambos valores a `float`, lo que permite trabajar con enteros y decimales.
5. La funcion `operaciones_basicas(num1, num2)`, que devuelve una tupla con:
   - suma
   - resta
   - multiplicacion
   - division
6. Una validacion en la division para evitar error cuando `num2` es `0`; en ese caso devuelve el texto `"No se puede dividir por cero"`.
7. La llamada a la funcion para desempaquetar los resultados en `suma`, `resta`, `multiplicacion` y `division`.
8. Cuatro `print` finales para mostrar cada resultado en pantalla.

### `test_01.calculate.py`
Este archivo define pruebas con `pytest` para validar el comportamiento de `operaciones_basicas`.

Contiene lo siguiente:

1. Importa `pytest`.
2. Importa `spec_from_file_location` y `module_from_spec` desde `importlib.util` para cargar el archivo `01.calculate.py` de forma dinamica.
3. Importa `sys`, aunque en el contenido actual no se usa.
4. Crea una especificacion de modulo llamada `"calculate"` apuntando al archivo `01.calculate.py`.
5. Construye el modulo dinamico y lo ejecuta con `spec.loader.exec_module(calculate)`.
6. Extrae la funcion `operaciones_basicas` desde el modulo cargado.
7. Define seis pruebas:
   - `test_operaciones_basicas_suma`: verifica que `5 + 3` sea `8`.
   - `test_operaciones_basicas_resta`: verifica que `10 - 4` sea `6`.
   - `test_operaciones_basicas_multiplicacion`: verifica que `6 * 7` sea `42`.
   - `test_operaciones_basicas_division`: verifica que `20 / 4` sea `5`.
   - `test_operaciones_basicas_division_por_cero`: verifica el mensaje `"No se puede dividir por cero"`.
   - `test_operaciones_basicas_numeros_negativos`: valida suma, resta, multiplicacion y una division aproximada con `pytest.approx`.

Observacion importante: como `01.calculate.py` ejecuta `input(...)` en el nivel principal, al importar ese archivo tambien se dispara la parte interactiva del programa.

### `.gitignore`
Este archivo usa una plantilla amplia para proyectos Python y herramientas relacionadas.

Incluye reglas para ignorar:

1. Archivos compilados y caches, por ejemplo `__pycache__/`, `*.pyc` y `*$py.class`.
2. Artefactos de empaquetado y distribucion, como `build/`, `dist/`, `*.egg-info/` y `wheels/`.
3. Reportes de pruebas y cobertura, como `.coverage`, `htmlcov/`, `.pytest_cache/` y `coverage.xml`.
4. Entornos virtuales y archivos de entorno, como `.venv`, `venv/`, `env/` y `.env`.
5. Archivos generados por herramientas como Jupyter, mypy, Pyre, Ruff, Cython y PyInstaller.
6. Configuraciones o carpetas locales de editores y herramientas, por ejemplo `.idea/` comentado, `.cursorignore`, `.cursorindexingignore` y archivos relacionados con VS Code.

En la practica, este `.gitignore` sirve para mantener el repositorio limpio y evitar subir archivos locales o generados automaticamente.

## Directorios visibles

| Directorio | Descripcion |
| --- | --- |
| `.venv` | Entorno virtual local de Python para aislar dependencias del proyecto. |
| `__pycache__` | Carpeta generada por Python para almacenar bytecode compilado. |
