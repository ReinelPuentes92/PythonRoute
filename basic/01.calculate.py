# Calculadora de operaciones básicas
bienvenido = "Bienvenido a la calculadora de operaciones básicas"
print(bienvenido)

# Solicitar al usuario que ingrese dos números
num1 = float(input("Ingrese el primer número: "))
num2 = float(input("Ingrese el segundo número: "))

# cree una funcion que calcule las operaciones basicas 
# suma, resta, multiplicacion y division entre dos numeros
def operaciones_basicas(num1, num2):
    return (
        num1 + num2,
        num1 - num2,
        num1 * num2,
        num1 / num2 if num2 != 0 else "No se puede dividir por cero"
    )

# Llamar a la función y mostrar los resultados
suma, resta, multiplicacion, division = operaciones_basicas(num1, num2)
print(f"Suma: {suma}")
print(f"Resta: {resta}")
print(f"Multiplicación: {multiplicacion}")
print(f"División: {division}")