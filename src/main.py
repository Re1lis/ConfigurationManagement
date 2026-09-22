import os #имя пользователя
import socket #hostname
import sys #завершение программы
import shlex #парсер команд
import tkinter as tk #окно
from tkinter import scrolledtext #textarea

if len(sys.argv) != 3:
    print("Error: expected VFS path and startup script path")
    sys.exit(1)

vfs_path = sys.argv[1]
startup_script_path = sys.argv[2]

print("VFS path: ", vfs_path)
print("Startup script path:", startup_script_path)

        

class TerminalUNIXOS:
    def __init__(self, startup_script_path):
        self.startup_script_path = startup_script_path
        self.username = os.getlogin()
        self.hostname = socket.gethostname()

        self.window = tk.Tk()
        self.window.configure(bg="#1e1e1e") # dark bg
        title = f"Эмулятор - [{self.username}@{self.hostname}]"
        self.window.title(title)

        self.terminal = scrolledtext.ScrolledText(
            self.window,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            font=("Consolas", 12)
        )

        self.terminal.tag_configure("error", foreground="#ff5555")
        self.terminal.tag_configure("unknown", foreground="#D2691E")

        self.terminal.pack()

        self.terminal.bind("<Return>", self.command_handler)

        with open(self.startup_script_path) as startup_file:
            for line in startup_file:
                self.terminal.insert("end", line.rstrip("\n") + "\n")
                self.execute_command(line)

                

        self.window.mainloop() # ожидание действий пользователя

    def command_handler(self, event):
        command = self.terminal.get("insert linestart", "insert")

        self.terminal.insert("insert", "\n")
        self.execute_command(command)

        return "break"  # предотвращение добавления новой строки в текстовое окно

    
    def execute_command(self, command): # обработчик команд
        try:
            parts = shlex.split(command)
        except ValueError: # ошибка значения
            self.terminal.insert("end", "Error: Invalid command syntax\n", "error")
            return

        if parts:
            command_name = parts[0]
            arguments = parts[1:]

            match command_name:
                case "ls":
                    self.terminal.insert("end", command_name + " " + str(arguments) + "\n") # пишем после всего содержимого
                case "cd":
                    self.terminal.insert("end", command_name + " " + str(arguments) + "\n")
                case "exit":
                    self.window.destroy() # закрытие окна
                case _:
                     self.terminal.insert("end", "Unknown command: " + command_name+ "\n", "unknown") # пишем после всего содержимого

        
           

terminal = TerminalUNIXOS(startup_script_path)
