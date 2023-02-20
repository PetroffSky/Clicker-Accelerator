from unittest import TestCase, main
from click03 import ClickApp


class ClickTest(TestCase):

    def setUp(self):
        self.click = ClickApp()

    def test_input_y(self):
        """Проверяем ввод 'y' для замедления скрипта"""
        self.assertEqual(self.click.select_mode('y'), 'y')

    def test_input_n(self):
        """Проверяем ввод 'y' для ускорения скрипта"""
        self.assertEqual(select_mode('n'), 'n')

    #def test_input_n(self):
    #   """Проверяем некорректный ввод при выборе замедления скрипта"""
     #   with self.assertRaises(ValueError):
            
            


        
if __name__ == "__main__":
    main()
