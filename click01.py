import time
import tkinter as tk
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

                    
    def clickermann_script_time_corrector(self):            
            with open(self.filename, 'r', encoding='utf-8' ) as file:
                answer = file.read()
                if 'FILE_NO_SAN' in answer:            
                    type_of_file = 'со скриптом для NOSAN'
                    print(f'Выбран файл {type_of_file}')
                        
                if 'FILE_SAN' in answer:             
                    type_of_file = 'со скриптом для SAN'
                    print(f'Выбран файл {type_of_file}')
                        
            # time.sleep(2)
            
            # Можно добавить в tkinter ввод percent
            # Можно добавить в tkinter лог работы
            with open(self.filename, 'r', encoding='utf-8' ) as inputfile,\
                open('click_output.txt', 'w', encoding='utf-8' ) as outputfile:                

                try:
                    answer = input("Будем замедять или ускорять скрипт? Введи 'y' для замедления или 'n' для ускорения: ").lower()
                    if answer == "y":
                        percent = int(input('На сколько процентов замедляем? Введите от 1 до 99 и нажмите ENTER: '))
                        if percent < 1 or percent > 99:
                            raise ValueError("Были введены неверные рабочие данные")
                            sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0
                        percent += 100
                    elif answer == "n":                    
                        percent = int(input('На сколько процентов ускоряем? Введите от 1 до 99 и нажмите ENTER: '))
                        if percent < 1 or percent > 99:
                            raise ValueError("Были введены неверные рабочие данные")
                            sys.exit(1)  # Принудительная остановка программы с результатом 1, вместо 0
                    else:
                        print(f"Введены некорректные данные")
                        sys.exit(1)
               
                    input_script_working_time = 0
                    output_script_working_time = 0
                    
                    for i in inputfile.read().split('\n'):               
                        if i.startswith('waitms('):
                            s_index = i.index('(')
                            f_index = i.index(' ')
                            number = int(i[s_index + 1 : f_index])
                            input_script_working_time += number
                            if number < 10: number = 10                             
                            change_num = int(number * percent / 100)
                            output_script_working_time += change_num                                            
                            i = f'waitms({change_num} + $S_CORR)\n'
                            print(f'Меняемое число: {number}\n'
                                  f'Изменили число на: {change_num}\n'
                                  f'Пишем в файл: {i}')                
                            outputfile.write(i)
                        else:
                            i = f'{i}\n'
                            outputfile.write(i)
                            
                    if answer == 'y':
                        outputfile.write(f'// Данный скрипт замедлён на {percent-100} процентов\n')
                    if answer == 'n':
                        outputfile.write(f'// Данный скрипт ускорен на {percent} процентов\n')
                    outputfile.write(f'// Время работы скрипта до изменения {input_script_working_time/1000} секунд\n'
                                     f'// Время работы скрипта после изменения {output_script_working_time/1000} секунд')
                except Exception as _ex:
                    print(f'Ошибка {type(_ex).__name__}: {str(_ex.args[0])}.\n'                   
                          f'Прерывание! Работа окончена! Для продолжения - загрузите файл Clickermann!')
                    sys.exit(1)
                finally:        
                    print('----------------------------------------------------------------')
                    
            if answer in ['y', 'n']:
                print(f'Время работы скрипта до изменения {input_script_working_time/1000} секунд\n'
                      f'Время работы скрипта после изменения {output_script_working_time/1000} секунд\n'
                      f'Работа c {type_of_file} окончена, результат в click_output.txt')

            self.open_click_output()
            
            for symbol in "<------ GOOD LUCK! ------>":
                time.sleep(0.1)
                print(symbol, end='', flush=True)
            print()            

    def open_click_output(self):
        print("Открываю файл click_output_txt для сохранения в конечный скрипт!")
        webbrowser.open("click_output.txt")  # Открываем файл txt в приложении по-умолчанию


def main():
    click = ClickApp()
    click.geometry("300x50+760+500")  # Устанавливаем размеры окна и его положение на экране. БЕЗ ПРОБЕЛОВ!
    click.mainloop()

    
if __name__ == "__main__":
    main()
    

    
    
    
    
    
