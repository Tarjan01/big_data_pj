import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import duckdb
import random
from ttkbootstrap import Style

# Connect to DuckDB
connection = duckdb.connect(database='demo.db', read_only=True)
cur = connection.cursor()


def get_rand():
    cur.execute("SELECT antecedent, consequent, confidence, lift, support FROM modesearch WHERE id = ?", [random.randint(0, 319267)])
    display_results(cur.fetchall())

def get_data(antecedent):
    if antecedent:
        antecedent = '+'.join(antecedent.split())
        cur.execute("SELECT antecedent, consequent, confidence, lift, support FROM modesearch WHERE antecedent = ?", [antecedent])
        display_results(cur.fetchall())
    else:
        tkinter.messagebox.showinfo(title='Empty Input', message='Please enter an antecedent for the query.')

def display_results(info):
    if info:
        result_window = tk.Tk()
        result_window.title('Query Results')
        result_window.geometry("800x500")
        
        style = Style('flatly')  # You can choose a different style from the available themes
        
        tk.Label(result_window, text='\nQuery Results in the table below:\n', font=(
            18)).pack()

        scrollbar = tk.Scrollbar(result_window)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('Antecedent', 'Consequent', 'Confidence', 'Lift', 'Support')
        headers = ('Antecedent', 'Consequent', 'Confidence', 'Lift', 'Support')
        widths = (200, 140, 140, 140, 140)
        
        res_list = ttk.Treeview(result_window, style="mystyle", show='headings', columns=columns, height=15, yscrollcommand=scrollbar.set)
        for column, header, width in zip(columns, headers, widths):
            res_list.column(column, width=width, anchor='center')
            res_list.heading(column, text=header, anchor='center')
        
        for i, result in enumerate(info):
            res_list.insert('', i, values=result)
        
        res_list.pack()
        scrollbar.config(command=res_list.yview)
        
        result_window.mainloop()
    else:
        tkinter.messagebox.showinfo(title='No Result', message='Search result is empty')


if __name__ == '__main__':
    # User login page
    windows = tk.Tk()
    windows.title('Frequent Pattern Query')
    windows.geometry("800x500")
    
    style = Style('flatly')  # You can choose a different style from the available themes
    style.configure('TButton', borderwidth=5, relief="ridge", font=('Helvetica', 12))
    
    tk.Label(windows, text='\n\nPlease enter the following information:\n', font=(14)).pack()
    tk.Label(windows, text='For example: product site www 佳能\n', font=(14)).pack()
    
    antecedent_var = tk.StringVar()
    tk.Entry(windows, show=None, font=(14), textvariable=antecedent_var).pack(ipadx=150, ipady=10)
    tk.Label(windows, text='\n\n\n', font=(14)).pack()

    query_button = ttk.Button(windows, text='Query', style="mystyle.TButton", command=lambda: get_data(antecedent_var.get()))
    query_button.place(x=400, y=250)
    
    random_query_button = ttk.Button(windows, text='Random Query', style="mystyle.TButton", command=get_rand)
    random_query_button.place(x=550, y=250)

    windows.mainloop()

    # Close the DuckDB connection
    connection.close()
