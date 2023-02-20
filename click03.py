import time
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import sys
import webbrowser
  

class ClickApp(tk.Tk):
    def __init__(self):
        super().__init__()
        btn_select_file = tk.Button(self,
                                    text="Выбрать файл Clickermann",
                                    command=self.choose_file)
        btn_select_file.pack(padx=60, pady=10)        
        

    def choose_file(self):
        # Создаём ограничение на типы открываемых файлов: txt и cms - файл Clickermann
        # передаём кортеж из кортежей
        self.filetypes = (("Clickermann файл", "*.cms"), ("Текстовый файл", "*.txt"))
        
        self.filename = fd.askopenfilename(title="Открыть файл",
                                           initialdir="/",
                                           filetypes=self.filetypes)
        if self.filename:            
            print(f'Выбран файл скрипта: {self.filename}')            
            self.clickermann_script_time_corrector()

        if not self.filename:
            print("Файл не выбран")            
            return "Файл не выбран"

    # Можно добавить в tkinter ввод self.percent
    # Можно добавить в tkinter лог работы                
    def clickermann_script_time_corrector(self):            
            self.type_of_file = self.filename[self.filename.rfind('/') + 1:]           
            
            with open(self.filename, 'r', encoding='utf-8' ) as inputfile,\
                open('click_output.txt', 'w', encoding='utf-8' ) as self.outputfile:                

                try:
                    self.select_mode()
                    self.input_percent()                    
                    self.input_script_working_time = 0
                    self.output_script_working_time = 0
                    
                    for i in inputfile.read().split('\n'):               
                        if i.startswith('waitms('):
                            s_index = i.index('(')
                            f_index = i.index(' ')
                            number = int(i[s_index + 1 : f_index])
                            self.input_script_working_time += number
                            if number < 2: number = 2   # устанавливаем изменение для малых таймингов                             
                            change_num = int(number * self.percent / 100)
                            self.output_script_working_time += change_num                                            
                            i = f'waitms({change_num} + $S_CORR)\n'
                            print(f'Меняемое число: {number}\n'
                                  f'Изменили число на: {change_num}\n'
                                  f'Пишем в файл: {i}')                
                            self.outputfile.write(i)
                        else:
                            i = f'{i}\n'
                            self.outputfile.write(i)

                    self.statistics_to_file()
                    
                except Exception as _ex:
                    print(f'Ошибка {type(_ex).__name__}: {str(_ex.args[0])}.\n'                   
                          f'Прерывание! Работа окончена! Для продолжения - загрузите файл Clickermann!')
                    sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0
                finally:        
                    print('---------------------------------------------------------------------------')                    
            
            self.statistics_to_print()
            self.open_click_output()
            self.farewell()
            

    def select_mode(self):
        try:
            print(f'Будем замедять или ускорять скрипт?\n'
                  f"Введи 'y' для замедления или 'n' для ускорения: ", end='')
            self.answer = input().lower()
            if not self.answer in ['y', 'n']:
                raise ValueError(f"Нет такого режима работы программы: {self.answer}")              
        except Exception as _ex:
            print(f'Ошибка {type(_ex).__name__}: {str(_ex.args[0])}. Повторите загрузку файла')                  
            sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0


    def input_percent(self):
        try:            
            if self.answer == 'y':
                self.percent = int(input('На сколько процентов замедляем? Введите от 1 до 99 и нажмите ENTER: '))
                if self.percent < 1 or self.percent > 99:
                    raise ValueError("Были введены неверные рабочие данные")                    
                self.percent += 100
            elif self.answer == 'n':
                self.percent = int(input('На сколько процентов ускоряем? Введите от 1 до 99 и нажмите ENTER: '))
                if self.percent < 1 or self.percent > 99:
                    raise ValueError("Были введены неверные рабочие данные")
                    sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0                     
        except Exception as _ex:
            print(f'Ошибка {type(_ex).__name__}: {str(_ex.args[0])}. Повторите загрузку файла')  
            sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0
        
            

    def statistics_to_file(self):
        # пишем статистику в файл
        if self.answer == 'y':
            self.outputfile.write(f'// Процент замедления скрипта: {self.percent-100}\n')
        if self.answer == 'n':
            self.outputfile.write(f'// Процент ускорения скрипта: {self.percent}\n')
        self.outputfile.write(f'// Время работы исходного скрипта {self.input_script_working_time/1000} секунд\n'
                              f'// Время работы конечного скрипта {self.output_script_working_time/1000} секунд')


            
    def statistics_to_print(self):
        # выводим статистику на экран
        if self.answer in ['y', 'n']:
                print(f'Время работы исходного скрипта {self.input_script_working_time/1000} секунд\n'
                      f'Время работы конечного скрипта {self.output_script_working_time/1000} секунд\n'
                      f'Работа c файлом {self.type_of_file} окончена, результат в click_output.txt')

                       

    def open_click_output(self):
        print("Открываю файл click_output_txt для сохранения в конечный скрипт!")
        webbrowser.open("click_output.txt")  # Открываем файл txt в приложении по-умолчанию


    def farewell(self):
        for symbol in "<------ GOOD LUCK! ------>":
            time.sleep(0.1)
            print(symbol, end='')
        print() 


def main():
    click = ClickApp()
    click.title('CSTC')
    #!!!! Надо поправить !!!!
    click.iconbitmap('ico.ico')  # устанавливаем иконку заголовка окна
    click.iconphoto(False, tk.PhotoImage(file='ico.png'))
    label = ttk.Label(text=f'Clickermann Script Time Corrector.\n'
                           f'Check terminal for changes!\n'
                           f'The program works in terminal!'
                           )
    # label = ttk.Label(text='Check terminal for changes')
    label.pack()
    click.geometry("350x120+760+500")  # Устанавливаем размеры окна и его положение на экране. БЕЗ ПРОБЕЛОВ!
    click.mainloop()

    
if __name__ == "__main__":
    main()
    
