import os
import tkinter as tk
from tkinter import filedialog, messagebox
class FileSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title
        self.search_label = tk.Label(root, text="输入关键字：")
        self.search_label.pack()
        self.search_entry = tk.Entry(root)
        self.search_entry.pack()
        self.search_button = tk.Button(root, text="搜索", command=self.search_files)
        self.search_button.pack()
        self.result_listbox = tk.Listbox(root, width=100)
        self.result_listbox.pack()
        self.copy_button = tk.Button(root, text="复制", command=self.copy_file)
        self.copy_button.pack()
        self.paste_button = tk.Button(root, text="粘贴", command=self.paste_file)
        self.paste_button.pack()
        self.move_button = tk.Button(root, text="移动", command=self.move_file)
        self.move_button.pack()
        self.results = []
    def search_files(self):
        keyword = self.search_entry.get()
        self.results = []
        for root_dir, dirs, files in os.walk('C:/'):
            for file in files:
                if keyword in file:
                    file_path = os.path.join(root_dir, file)
                    self.results.append(file_path)
                    self.results_listbox.insert(tk.END, file_path)
    def copy_file(self):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_file = self.results[selected_index[0]]
            self.copy_path = selected_file
            messagebox.showinfo("提示", "文件已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "请选择要复制的文件")
    def paste_file(self):
        if hasattr(self, 'copy_path'):
            destination = filedialog.askdirectory()
            if destination:
                try:
                    shutil.copy2(self.copy_path, destination)
                    messagebox.showinfo("提示", "文件已粘贴到指定位置")
                except Exception as e:
                    messagebox.showerror("错误"， f"粘贴文件时出错:{e}")
        else:
            messagebox.showwarning("警告", "请先复制文件")
    def move_file(self):
        selected_index = self.result_listbox.curselection()
        if selected_index:
            selected_file = self.result_listbox.curselection()
            destination = filedialog.askdirectory()
            if destination:
                try:
                    shutil.move(selected_file, destination)
                    messagebox.showinfo("提示", "文件已移动到指定位置")
                    self.result_listbox.delete(selected_index)
                    del self.results[selected_index[0]]
                except Exception as e:
                    messagebox.showerror("错误", f"移动文件时出错:{e}")
        else:
            messagebox.showwarning("警告", "请选择要移动的文件")
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
                
                                        
