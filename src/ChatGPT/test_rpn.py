import unittest
from unittest.mock import patch
import io
import sys
import math

# Importamos nuestro programa
from rpn import evaluar_rpn, RPNError, main

class TestRPN(unittest.TestCase):

    def test_operaciones_basicas(self):
        self.assertEqual(evaluar_rpn("3 4 +"), 7)
        self.assertEqual(evaluar_rpn("5 1 2 + 4 * + 3 -"), 14)
        self.assertEqual(evaluar_rpn("10 2 /"), 5)
        self.assertEqual(evaluar_rpn("2.5 1.5 +"), 4.0)
        self.assertEqual(evaluar_rpn("-5 2 *"), -10)

    def test_comandos_pila(self):
        self.assertEqual(evaluar_rpn("5 dup +"), 10)
        self.assertEqual(evaluar_rpn("2 3 swap -"), 1)  # La pila queda: 3 2, luego 3 - 2 = 1
        self.assertEqual(evaluar_rpn("5 4 drop"), 5)
        self.assertEqual(evaluar_rpn("5 10 clear 3"), 3)

    def test_constantes_y_matematicas(self):
        self.assertAlmostEqual(evaluar_rpn("p"), math.pi)
        self.assertAlmostEqual(evaluar_rpn("e"), math.e)
        self.assertEqual(evaluar_rpn("9 sqrt"), 3)
        self.assertEqual(evaluar_rpn("100 log"), 2)
        self.assertAlmostEqual(evaluar_rpn("e ln"), 1.0)
        self.assertAlmostEqual(evaluar_rpn("2 ex"), math.exp(2))
        self.assertEqual(evaluar_rpn("3 10x"), 1000)
        self.assertEqual(evaluar_rpn("2 3 yx"), 8)
        self.assertEqual(evaluar_rpn("10 1/x"), 0.1)
        self.assertEqual(evaluar_rpn("5 chs"), -5)

    def test_trigonometria(self):
        self.assertAlmostEqual(evaluar_rpn("90 sin"), 1.0)
        self.assertAlmostEqual(evaluar_rpn("0 cos"), 1.0)
        self.assertAlmostEqual(evaluar_rpn("45 tg"), 1.0)
        self.assertAlmostEqual(evaluar_rpn("1 asin"), 90.0)
        self.assertAlmostEqual(evaluar_rpn("1 acos"), 0.0)
        self.assertAlmostEqual(evaluar_rpn("1 atg"), 45.0)

    def test_memoria(self):
        # STO y RCL separados por espacio
        self.assertEqual(evaluar_rpn("10 STO 01 5 RCL 01 +"), 15)
        # STO y RCL pegados al registro
        self.assertEqual(evaluar_rpn("20 STO02 10 RCL02 +"), 30)

    def test_manejo_de_errores(self):
        with self.assertRaisesRegex(RPNError, "División por cero"):
            evaluar_rpn("3 0 /")
        with self.assertRaisesRegex(RPNError, "División por cero en 1/x"):
            evaluar_rpn("0 1/x")
        with self.assertRaisesRegex(RPNError, "Pila insuficiente"):
            evaluar_rpn("3 +")
        with self.assertRaisesRegex(RPNError, "Raíz cuadrada de un número negativo"):
            evaluar_rpn("-4 sqrt")
        with self.assertRaisesRegex(RPNError, "Token inválido"):
            evaluar_rpn("3 hola +")
        with self.assertRaisesRegex(RPNError, "Memoria inválida"):
            evaluar_rpn("10 STO 99")
        with self.assertRaisesRegex(RPNError, "quedar 1 valor en la pila"):
            evaluar_rpn("3 4")

    # --- Pruebas para la interfaz de consola (main) ---

    @patch('sys.argv', ['rpn.py', '3', '4', '+'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_argumentos(self, mock_stdout):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "7")

    @patch('sys.argv', ['rpn.py'])
    @patch('builtins.input', side_effect=['5 5 *'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_input_stdin(self, mock_stdout, mock_input):
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "25")

    @patch('sys.argv', ['rpn.py', '3', '0', '/'])
    @patch('sys.stderr', new_callable=io.StringIO)
    def test_main_error_impresion(self, mock_stderr):
        with self.assertRaises(SystemExit):
            main()
        self.assertIn("División por cero", mock_stderr.getvalue())

    @patch('sys.argv', ['rpn.py'])
    @patch('builtins.input', side_effect=['   ']) # Input vacío
    def test_main_input_vacio(self, mock_input):
        # Si el input es vacío, main() simplemente hace un return
        main()

    @patch('sys.argv', ['rpn.py'])
    @patch('builtins.input', side_effect=EOFError) # Simula Ctrl+D
    def test_main_eof(self, mock_input):
        # Si hay EOFError, main() hace return silencioso
        main()

if __name__ == '__main__':
    unittest.main()