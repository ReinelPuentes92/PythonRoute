import pytest
from importlib.util import spec_from_file_location, module_from_spec
import sys

# Load the module dynamically
spec = spec_from_file_location("calculate", "01.calculate.py")
calculate = module_from_spec(spec)
spec.loader.exec_module(calculate)

operaciones_basicas = calculate.operaciones_basicas


def test_operaciones_basicas_suma():
    suma, _, _, _ = operaciones_basicas(5, 3)
    assert suma == 8


def test_operaciones_basicas_resta():
    _, resta, _, _ = operaciones_basicas(10, 4)
    assert resta == 6


def test_operaciones_basicas_multiplicacion():
    _, _, multiplicacion, _ = operaciones_basicas(6, 7)
    assert multiplicacion == 42


def test_operaciones_basicas_division():
    _, _, _, division = operaciones_basicas(20, 4)
    assert division == 5


def test_operaciones_basicas_division_por_cero():
    _, _, _, division = operaciones_basicas(10, 0)
    assert division == "No se puede dividir por cero"


def test_operaciones_basicas_numeros_negativos():
    suma, resta, multiplicacion, division = operaciones_basicas(-5, 3)
    assert suma == -2
    assert resta == -8
    assert multiplicacion == -15
    assert division == pytest.approx(-5/3)