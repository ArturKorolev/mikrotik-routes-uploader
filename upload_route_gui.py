import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from routes_handler import (
    upload_routes_to_mikrotik,
    load_networks_from_file,
    validate_ip,
    validate_gateway,
    ValidationError
)

class MikroTikUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Загрузка маршрутов в MikroTik")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Переменные
        self.upload_thread = None
        self.is_uploading = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Построение пользовательского интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Конфигурирование сетки
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Заголовок
        title = ttk.Label(main_frame, text="Параметры подключения", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Router IP
        ttk.Label(main_frame, text="Router IP:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_ip = ttk.Entry(main_frame, width=30)
        self.entry_ip.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Username
        ttk.Label(main_frame, text="Username:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_user = ttk.Entry(main_frame, width=30)
        self.entry_user.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Password
        ttk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_pass = ttk.Entry(main_frame, width=30, show="*")
        self.entry_pass.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Gateway
        ttk.Label(main_frame, text="Gateway:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_gateway = ttk.Entry(main_frame, width=30)
        self.entry_gateway.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0))
        self.entry_gateway.insert(0, "192.168.27.250")
        
        # Comment
        ttk.Label(main_frame, text="Comment:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_comment = ttk.Entry(main_frame, width=30)
        self.entry_comment.grid(row=5, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Список файлов
        ttk.Label(main_frame, text="", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=3, pady=(15, 10))
        ttk.Label(main_frame, text="Файл со списком сетей:", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Выбор файла
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.entry_file = ttk.Entry(file_frame, width=35)
        self.entry_file.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_browse = ttk.Button(file_frame, text="Обзор...", command=self.choose_file, width=10)
        btn_browse.pack(side=tk.LEFT, padx=(5, 0))
        
        # Информация о файле
        self.label_info = ttk.Label(main_frame, text="", foreground="gray", font=("Arial", 9))
        self.label_info.grid(row=8, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        self.btn_upload = ttk.Button(button_frame, text="Загрузить маршруты", command=self.start_upload)
        self.btn_upload.pack(side=tk.LEFT, padx=2)
        
        btn_cancel = ttk.Button(button_frame, text="Выход", command=self.root.quit)
        btn_cancel.pack(side=tk.LEFT, padx=2)
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Лог вывода
        ttk.Label(main_frame, text="Логирование:", font=("Arial", 9, "bold")).grid(row=11, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_log = tk.Text(log_frame, height=8, width=60, yscrollcommand=scrollbar.set, state=tk.DISABLED)
        self.text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_log.yview)
        
        # Конфигурирование весов строк
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(12, weight=1)
    
    def choose_file(self):
        """Выбор файла"""
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Выберите файл со списком сетей"
        )
        if filename:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, filename)
            
            # Показываем информацию о файле
            try:
                networks = load_networks_from_file(filename)
                self.label_info.config(text=f"✓ Файл валидный. Сетей: {len(networks)}", foreground="green")
            except Exception as e:
                self.label_info.config(text=f"✗ {str(e)[:50]}...", foreground="red")
    
    def log_message(self, message):
        """Добавление сообщения в лог"""
        self.text_log.config(state=tk.NORMAL)
        self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)
        self.text_log.config(state=tk.DISABLED)
        self.root.update()
    
    def clear_log(self):
        """Очистка лога"""
        self.text_log.config(state=tk.NORMAL)
        self.text_log.delete(1.0, tk.END)
        self.text_log.config(state=tk.DISABLED)
    
    def validate_inputs(self):
        """Валидация входных данных"""
        router_ip = self.entry_ip.get().strip()
        if not router_ip:
            raise ValidationError("Введите IP роутера")
        validate_ip(router_ip)
        
        username = self.entry_user.get().strip()
        if not username:
            raise ValidationError("Введите имя пользователя")
        
        password = self.entry_pass.get()
        if not password:
            raise ValidationError("Введите пароль")
        
        gateway = self.entry_gateway.get().strip()
        if not gateway:
            raise ValidationError("Введите адрес шлюза")
        validate_gateway(gateway)
        
        file_path = self.entry_file.get().strip()
        if not file_path:
            raise ValidationError("Выберите файл со списком сетей")
        
        return {
            'router_ip': router_ip,
            'username': username,
            'password': password,
            'gateway': gateway,
            'comment': self.entry_comment.get().strip(),
            'file_path': file_path
        }
    
    def upload_thread_worker(self, params):
        """Рабочая функция потока загрузки"""
        try:
            self.log_message("Загрузка параметров из файла...")
            networks = load_networks_from_file(params['file_path'])
            self.log_message(f"✓ Загружено {len(networks)} сетей")
            
            self.log_message("\nПодключение к MikroTik...")
            self.log_message(f"  Router IP: {params['router_ip']}")
            self.log_message(f"  Gateway: {params['gateway']}")
            
            result = upload_routes_to_mikrotik(
                router_ip=params['router_ip'],
                username=params['username'],
                password=params['password'],
                gateway=params['gateway'],
                networks=networks,
                comment=params['comment']
            )
            
            self.log_message("\n" + "="*50)
            self.log_message("РЕЗУЛЬТАТЫ:")
            self.log_message(f"✓ Успешно добавлено: {result['success']}")
            self.log_message(f"✗ Ошибок: {result['failed']}")
            
            if result['errors']:
                self.log_message("\nОшибки:")
                for error in result['errors'][:5]:
                    self.log_message(f"  - {error}")
                if len(result['errors']) > 5:
                    self.log_message(f"  ... и ещё {len(result['errors']) - 5} ошибок")
            
            self.log_message("="*50)
            
            if result['failed'] == 0:
                messagebox.showinfo("Успех", f"Все {result['success']} маршрутов успешно загружены!")
            else:
                messagebox.showwarning(
                    "Завершено с ошибками",
                    f"Загружено: {result['success']}\nОшибок: {result['failed']}"
                )
        
        except ValidationError as e:
            self.log_message(f"✗ Ошибка валидации: {e}")
            messagebox.showerror("Ошибка валидации", str(e))
        except FileNotFoundError as e:
            self.log_message(f"✗ {e}")
            messagebox.showerror("Ошибка файла", str(e))
        except Exception as e:
            self.log_message(f"✗ Ошибка: {e}")
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.is_uploading = False
            self.progress.stop()
            self.btn_upload.config(state=tk.NORMAL)
    
    def start_upload(self):
        """Запуск загрузки"""
        if self.is_uploading:
            messagebox.showwarning("Предупреждение", "Загрузка уже в процессе")
            return
        
        try:
            params = self.validate_inputs()
        except ValidationError as e:
            messagebox.showerror("Ошибка валидации", str(e))
            return
        
        # Подтверждение
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Загрузить маршруты?\n\n"
            f"Router IP: {params['router_ip']}\n"
            f"Gateway: {params['gateway']}\n"
            f"Файл: {os.path.basename(params['file_path'])}"
        )
        
        if not confirm:
            return
        
        self.is_uploading = True
        self.btn_upload.config(state=tk.DISABLED)
        self.progress.start()
        self.clear_log()
        self.log_message("Начало загрузки маршрутов...\n")
        
        # Запуск загрузки в отдельном потоке
        self.upload_thread = threading.Thread(target=self.upload_thread_worker, args=(params,), daemon=True)
        self.upload_thread.start()

def main():
    root = tk.Tk()
    app = MikroTikUploadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()