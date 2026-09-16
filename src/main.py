import os #имя пользователя
import socket #hostname
import sys #завершение программы
import shlex #парсер команд
import tkinter as tk #window and button
from tkinter import scrolledtext #textarea

class TerminalUNIXOS:
    def __init__(self):
        self.username = os.getlogin()
        self.hostname = socket.gethostname()

        self.window = tk.Tk()
        title = f"Эмулятор - [{self.username}@{self.hostname}]"
        self.window.title(title)

        self.terminal = scrolledtext.ScrolledText(self.window) # создание текстового окна в главном окне 
        self.terminal.pack()

        self.terminal.bind("<Return>", self.command_handler)

        self.window.mainloop() # ожидание действий пользователя

    def command_handler(self, event):
        command = self.terminal.get("insert linestart", "insert")

        try:
            parts = shlex.split(command)
        except ValueError: # ошибка значения
            self.terminal.insert("insert", "\n")
            self.terminal.insert("end", "Error Value")
            return "break"


        if parts:
            command_name = parts[0]
            arguments = parts[1:]

            self.terminal.insert("insert", "\n")

            match command_name:
                case "ls":
                    self.terminal.insert("end", command_name + " " + str(arguments) + "\n ") # пишем после всего содержимого
                case "cd":
                    self.terminal.insert("end", command_name + " " + str(arguments) + "\n")
                case "exit":
                    self.window.destroy() # закрытие окна
                case _:
                     self.terminal.insert("end", "Unknown command: " + command_name+ "\n")
            
        return "break" # чтобы не выполнялось действие Enter
        
           

terminal = TerminalUNIXOS()
