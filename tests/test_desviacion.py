"""HU-04: validación de la desviación contra el cálculo manual.

Uso: python -m unittest discover tests
No necesita MySQL: prueba solo la fórmula.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.environ.setdefault("DB_NAME", "agua_cocacola")

from desviacion import calcular_desviacion  # noqa: E402


class TestDesviacion(unittest.TestCase):
    # Cálculo manual, septiembre 2026 (suma de las 4 semanas del CSV):
    def test_leve_tratamiento_residuales(self):
        # 95 + 96 + 96,9 + 97,9 = 385,8 ; (385,8 - 380) / 380 * 100 = 1,526... -> 1,53
        self.assertEqual(calcular_desviacion(385.8, 380), 1.53)

    def test_moderada_refrigeracion(self):
        # 80 + 80,8 + 99,6 + 82,4 = 342,8 ; (342,8 - 320) / 320 * 100 = 7,125 -> 7,13
        self.assertEqual(calcular_desviacion(342.8, 320), 7.13)

    def test_critica_lavado_envases(self):
        # 120 + 121,2 + 122,4 + 145,8 = 509,4 ; (509,4 - 432) / 432 * 100 = 17,916... -> 17,92
        self.assertEqual(calcular_desviacion(509.4, 432), 17.92)

    def test_por_debajo_de_la_referencia(self):
        # 45 + 45,5 + 45,9 + 46,4 = 182,8 ; (182,8 - 185) / 185 * 100 = -1,189... -> -1,19
        self.assertEqual(calcular_desviacion(182.8, 185), -1.19)

    def test_referencia_cero_se_rechaza(self):
        with self.assertRaises(ValueError):
            calcular_desviacion(100, 0)


if __name__ == "__main__":
    unittest.main()
