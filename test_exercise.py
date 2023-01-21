import unittest

import json

repetidos = [1, 2, 3, "1", "2", "3", 3, 4, 5]

# Genere una lista con los valores no repetidos de la lista ‘repetidos’.
sin_repetidos = list(set(repetidos))

repetidos = [1, 2, 3, "1", "2", "3", 3, 4, 5]
r = [1, "5", 2, "3"]

d_str = '{"valor":125.3,"codigo":123}'

# Genere una lista con los valores en común entre la lista ‘r’ y ‘repetidos’
elementos_comunes = list(set(r).intersection(repetidos))

# Transforme ‘d_str’ en un diccionario.
diccionario = json.loads(d_str)


class TestUtils(unittest.TestCase):

    def test_sin_repetidos_tiene_8_elementos(self):
        self.assertEqual(8, len(sin_repetidos))

    def test_sin_repetidos_tiene_los_elementos_esperados(self):
        self.assertTrue(1 in sin_repetidos)
        self.assertTrue(2 in sin_repetidos)
        self.assertTrue(3 in sin_repetidos)
        self.assertTrue(4 in sin_repetidos)
        self.assertTrue(5 in sin_repetidos)
        self.assertTrue("1" in sin_repetidos)
        self.assertTrue("2" in sin_repetidos)
        self.assertTrue("3" in sin_repetidos)

    def test_elementos_comunes_tiene_3_elementos(self):
        self.assertEqual(3, len(elementos_comunes))

    def test_elementos_comunes_tiene_los_elementos_esperados(self):
        self.assertTrue(1 in sin_repetidos)
        self.assertTrue(2 in sin_repetidos)
        self.assertTrue("3" in sin_repetidos)

    def test_diccionario_tiene_el_valor_esperado(self):
        self.assertEqual(diccionario["valor"], 125.3)

    def test_diccionario_tiene_el_codigo_esperado(self):
        self.assertEqual(diccionario["codigo"], 123)


if __name__ == '__main__':
    unittest.main()
