import tkinter as tk
from tkinter import ttk ,messagebox ,filedialog
import os
import threading
from datetime import datetime
import re
class LineCounterApp :
    def __init__ (self ,root ):
        self .root =root
        self .root .title ("Подсчёт строк в файле")
        self .root .geometry ("800x700")
        self .root .configure (bg ='#f0f0f0')
        style =ttk .Style ()
        style .theme_use ('clam')
        self .counting =False
        self .setup_ui ()
    def setup_ui (self ):
        title_label =tk .Label (
        self .root ,
        text ="📊 Подсчёт строк в файле",
        font =("Arial",16 ,"bold"),
        bg ='#f0f0f0',
        fg ='#2c3e50'
        )
        title_label .pack (pady =10 )
        input_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        input_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (input_frame ,text ="Файл или папка для анализа:",font =("Arial",10 ),bg ='#f0f0f0').pack (anchor ='w')
        input_select_frame =tk .Frame (input_frame ,bg ='#f0f0f0')
        input_select_frame .pack (fill ='x',pady =5 )
        self .input_var =tk .StringVar ()
        self .input_entry =tk .Entry (input_select_frame ,textvariable =self .input_var ,width =60 ,font =("Arial",10 ))
        self .input_entry .pack (side ='left',fill ='x',expand =True )
        file_btn =tk .Button (
        input_select_frame ,
        text ="Файл",
        command =self .browse_file ,
        bg ='#3498дб',
        fg ='white',
        font =("Arial",9 ),
        relief ='flat',
        padx =15
        )
        file_btn .pack (side ='right',padx =(5 ,0 ))
        folder_btn =tk .Button (
        input_select_frame ,
        text ="Папка",
        command =self .browse_folder ,
        bg ='#9b59b6',
        fg ='white',
        font =("Arial",9 ),
        relief ='flat',
        padx =15
        )
        folder_btn .pack (side ='right',padx =(5 ,0 ))
        options_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        options_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (options_frame ,text ="Опции подсчёта:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        checkboxes_frame =tk .Frame (options_frame ,bg ='#f0f0f0')
        checkboxes_frame .pack (fill ='x',pady =5 )
        self .count_empty_var =tk .BooleanVar (value =True )
        self .count_comments_var =tk .BooleanVar (value =True )
        self .count_whitespace_var =tk .BooleanVar (value =True )
        self .recursive_var =tk .BooleanVar (value =True )
        self .include_hidden_var =tk .BooleanVar ()
        tk .Checkbutton (
        checkboxes_frame ,
        text ="Считать пустые строки",
        variable =self .count_empty_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).grid (row =0 ,column =0 ,sticky ='w')
        tk .Checkbutton (
        checkboxes_frame ,
        text ="Считать комментарии",
        variable =self .count_comments_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).grid (row =0 ,column =1 ,sticky ='w',padx =(20 ,0 ))
        tk .Checkbutton (
        checkboxes_frame ,
        text ="Считать строки только с пробелами",
        variable =self .count_whitespace_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).grid (row =1 ,column =0 ,sticky ='w')
        tk .Checkbutton (
        checkboxes_frame ,
        text ="Рекурсивно по подпапкам",
        variable =self .recursive_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).grid (row =1 ,column =1 ,sticky ='w',padx =(20 ,0 ))
        tk .Checkbutton (
        checkboxes_frame ,
        text ="Включать скрытые файлы",
        variable =self .include_hidden_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).grid (row =2 ,column =0 ,sticky ='w')
        filter_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        filter_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (filter_frame ,text ="Фильтры файлов:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        filter_input_frame =tk .Frame (filter_frame ,bg ='#f0f0f0')
        filter_input_frame .pack (fill ='x',pady =5 )
        tk .Label (filter_input_frame ,text ="Включить расширения:",font =("Arial",9 ),bg ='#f0f0f0').pack (side ='left')
        self .include_ext_var =tk .StringVar (value =".py,.txt,.js,.html,.css,.cpp,.c,.java,.php,.rb,.go,.rs")
        include_ext_entry =tk .Entry (filter_input_frame ,textvariable =self .include_ext_var ,width =50 ,font =("Arial",9 ))
        include_ext_entry .pack (side ='left',padx =(5 ,0 ))
        tk .Label (filter_input_frame ,text ="Исключить расширения:",font =("Arial",9 ),bg ='#f0f0f0').pack (side ='left',padx =(20 ,0 ))
        self .exclude_ext_var =tk .StringVar (value =".pyc,.pyo,.exe,.dll,.so,.dylib")
        exclude_ext_entry =tk .Entry (filter_input_frame ,textvariable =self .exclude_ext_var ,width =30 ,font =("Arial",9 ))
        exclude_ext_entry .pack (side ='left',padx =(5 ,0 ))
        action_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        action_frame .pack (fill ='x',padx =20 ,pady =10 )
        self .count_btn =tk .Button (
        action_frame ,
        text ="📊 Подсчитать строки",
        command =self .start_counting ,
        bg ='#27ae60',
        fg ='white',
        font =("Arial",12 ,"bold"),
        relief ='flat',
        padx =30 ,
        pady =10
        )
        self .count_btn .pack (side ='left')
        self .stop_btn =tk .Button (
        action_frame ,
        text ="⏹️ Остановить",
        command =self .stop_counting ,
        bg ='#e74c3c',
        fg ='white',
        font =("Arial",12 ,"bold"),
        relief ='flat',
        padx =30 ,
        pady =10 ,
        state ='disabled'
        )
        self .stop_btn .pack (side ='left',padx =(10 ,0 ))
        clear_btn =tk .Button (
        action_frame ,
        text ="🗑️ Очистить",
        command =self .clear_results ,
        bg ='#95a5a6',
        fg ='white',
        font =("Arial",12 ,"bold"),
        relief ='flat',
        padx =30 ,
        pady =10
        )
        clear_btn .pack (side ='left',padx =(10 ,0 ))
        results_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        results_frame .pack (fill ='both',expand =True ,padx =20 ,pady =10 )
        tk .Label (results_frame ,text ="Результаты подсчёта:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        columns =('Файл','Строк','Пустых','Комментариев','Код','Размер')
        self .results_tree =ttk .Treeview (results_frame ,columns =columns ,show ='headings',height =10 )
        self .results_tree .heading ('Файл',text ='Файл')
        self .results_tree .heading ('Строк',text ='Всего строк')
        self .results_tree .heading ('Пустых',text ='Пустых')
        self .results_tree .heading ('Комментариев',text ='Комментариев')
        self .results_tree .heading ('Код',text ='Код')
        self .results_tree .heading ('Размер',text ='Размер (КБ)')
        self .results_tree .column ('Файл',width =300 )
        self .results_tree .column ('Строк',width =80 )
        self .results_tree .column ('Пустых',width =80 )
        self .results_tree .column ('Комментариев',width =100 )
        self .results_tree .column ('Код',width =80 )
        self .results_tree .column ('Размер',width =100 )
        self .results_tree .pack (side ='left',fill ='both',expand =True )
        results_scrollbar =ttk .Scrollbar (results_frame ,orient ='vertical',command =self .results_tree .yview )
        results_scrollbar .pack (side ='right',fill ='y')
        self .results_tree .config (yscrollcommand =results_scrollbar .set )
        self .stats_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        self .stats_frame .pack (fill ='x',padx =20 ,pady =5 )
        self .stats_label =tk .Label (
        self .stats_frame ,
        text ="",
        font =("Arial",10 ,"bold"),
        bg ='#f0f0f0',
        fg ='#2c3e50'
        )
        self .stats_label .pack (anchor ='w')
        log_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        log_frame .pack (fill ='both',expand =True ,padx =20 ,pady =10 )
        tk .Label (log_frame ,text ="Лог операций:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        self .log_text =tk .Text (
        log_frame ,
        height =6 ,
        font =("Consolas",9 ),
        bg ='#ffffff',
        fg ='#2c3e50',
        wrap ='word'
        )
        self .log_text .pack (fill ='both',expand =True ,pady =5 )
        log_scrollbar =tk .Scrollbar (self .log_text )
        log_scrollbar .pack (side ='right',fill ='y')
        self .log_text .config (yscrollcommand =log_scrollbar .set )
        log_scrollbar .config (command =self .log_text .yview )
    def browse_file (self ):
        file_path =filedialog .askopenfilename (
        title ="Выберите файл для анализа",
        filetypes =[
        ("Все файлы","*.*"),
        ("Текстовые файлы","*.текст"),
        ("Python файлы","*.py"),
        ("JavaScript файлы","*.js"),
        ("HTML-файлы","*.html"),
        ("CSS файлы","*.css")
        ]
        )
        if file_path :
            self .input_var .set (file_path )
    def browse_folder (self ):
        folder_path =filedialog .askdirectory (title ="Выберите папку для анализа")
        if folder_path :
            self .input_var .set (folder_path )
    def log_message (self ,message ):
        timestamp =datetime .now ().strftime ("%H:%M:%S")
        self .log_text .insert (tk .END ,f"[{timestamp }] {message }\n")
        self .log_text .see (tk .END )
        self .root .update ()
    def clear_results (self ):
        for item in self .results_tree .get_children ():
            self .results_tree .delete (item )
        self .stats_label .config (text ="")
        self .log_text .delete (1.0 ,tk .END )
    def start_counting (self ):
        input_path =self .input_var .get ().strip ()
        if not input_path :
            messagebox .showwarning ("Предупреждение","Выберите файл или папку для анализа!")
            return
        if not os .path .exists (input_path ):
            messagebox .showerror ("Ошибка","Выбранный путь не существует!")
            return
        self .counting =True
        self .count_btn .config (state ='disabled')
        self .stop_btn .config (state ='normal')
        self .clear_results ()
        thread =threading .Thread (target =self .count_lines ,args =(input_path ,))
        thread .daemon =True
        thread .start ()
    def stop_counting (self ):
        self .counting =False
        self .count_btn .config (state ='normal')
        self .stop_btn .config (state ='disabled')
        self .log_message ("Подсчёт остановлен пользователем")
    def count_lines (self ,path ):
        try :
            self .log_message (f"Начинаем анализ: {path }")
            total_files =0
            total_lines =0
            total_empty =0
            total_comments =0
            total_code =0
            total_size =0
            if os .path .isfile (path ):
                files_to_process =[path ]
            else :
                files_to_process =self .get_files_to_process (path )
            self .log_message (f"Найдено {len (files_to_process )} файлов для анализа")
            for file_path in files_to_process :
                if not self .counting :
                    break
                try :
                    result =self .analyze_file (file_path )
                    if result :
                        total_files +=1
                        total_lines +=result ['total_lines']
                        total_empty +=result ['empty_lines']
                        total_comments +=result ['comment_lines']
                        total_code +=result ['code_lines']
                        total_size +=result ['file_size']
                        filename =os .path .basename (file_path )
                        self .results_tree .insert ('','end',values =(
                        filename ,
                        result ['total_lines'],
                        result ['empty_lines'],
                        result ['comment_lines'],
                        result ['code_lines'],
                        f"{result ['file_size']/1024 :.1f}"
                        ))
                        self .log_message (f"Обработан: {filename }")
                except Exception as e :
                    self .log_message (f"Ошибка при анализе {file_path }: {e }")
            self .stats_label .config (
            text =f"Всего файлов: {total_files } | "
            f"Всего строк: {total_lines } | "
            f"Пустых: {total_empty } | "
            f"Комментариев: {total_comments } | "
            f"Код: {total_code } | "
            f"Размер: {total_size /1024 :.1f} KB"
            )
            self .log_message ("Анализ завершён!")
        except Exception as e :
            self .log_message (f"Ошибка при анализе: {e }")
        finally :
            self .counting =False
            self .count_btn .config (state ='normal')
            self .stop_btn .config (state ='disabled')
    def get_files_to_process (self ,folder ):
        files =[]
        include_extensions =[ext .strip ().lower ()for ext in self .include_ext_var .get ().split (',')if ext .strip ()]
        exclude_extensions =[ext .strip ().lower ()for ext in self .exclude_ext_var .get ().split (',')if ext .strip ()]
        for root ,dirs ,filenames in os .walk (folder ):
            if not self .recursive_var .get ()and root !=folder :
                continue
            for filename in filenames :
                if not self .include_hidden_var .get ()and filename .startswith ('.'):
                    continue
                file_path =os .path .join (root ,filename )
                file_ext =os .path .splitext (filename )[1 ].lower ()
                if include_extensions and file_ext not in include_extensions :
                    continue
                if exclude_extensions and file_ext in exclude_extensions :
                    continue
                files .append (file_path )
        return files
    def analyze_file (self ,file_path ):
        try :
            encodings =['utf-8','cp1251','latin-1']
            content =None
            for encoding in encodings :
                try :
                    with open (file_path ,'r',encoding =encoding )as file :
                        content =file .read ()
                    break
                except UnicodeDecodeError :
                    continue
            if content is None :
                return None
            lines =content .split ('\n')
            total_lines =len (lines )
            empty_lines =0
            comment_lines =0
            code_lines =0
            file_ext =os .path .splitext (file_path )[1 ].lower ()
            comment_patterns =self .get_comment_patterns (file_ext )
            for line in lines :
                stripped_line =line .strip ()
                if not stripped_line :
                    empty_lines +=1
                    if self .count_empty_var .get ():
                        total_lines +=0
                elif not self .count_whitespace_var .get ()and stripped_line .isspace ():
                    empty_lines +=1
                else :
                    is_comment =False
                    for pattern in comment_patterns :
                        if re .match (pattern ,stripped_line ):
                            is_comment =True
                            break
                    if is_comment :
                        comment_lines +=1
                    else :
                        code_lines +=1
            file_size =os .path .getsize (file_path )
            return {
            'total_lines':total_lines ,
            'empty_lines':empty_lines ,
            'comment_lines':comment_lines ,
            'code_lines':code_lines ,
            'file_size':file_size
            }
        except Exception as e :
            raise Exception (f"Ошибка при анализе файла: {e }")
    def get_comment_patterns (self ,file_ext ):
        patterns ={
        '.py':[r'^\s*#',r'^\s*"""',r"^\s*'''"],
        '.js':[r'^\s*//',r'^\s*/\*'],
        '.html':[r'^\s*<!--'],
        '.css':[r'^\s*/\*'],
        '.cpp':[r'^\s*//',r'^\s*/\*'],
        '.c':[r'^\s*//',r'^\s*/\*'],
        '.java':[r'^\s*//',r'^\s*/\*'],
        '.php':[r'^\s*//',r'^\s*#',r'^\s*/\*'],
        '.rb':[r'^\s*#'],
        '.go':[r'^\s*//',r'^\s*/\*'],
        '.rs':[r'^\s*//',r'^\s*/\*']
        }
        return patterns .get (file_ext ,[])
def main ():
    root =tk .Tk ()
    app =LineCounterApp (root )
    root .mainloop ()
if __name__ =="__main__":
    main ()