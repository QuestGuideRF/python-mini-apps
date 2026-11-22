import tkinter as tk
from tkinter import ttk ,messagebox
import os
import subprocess
import threading
import time
from datetime import datetime
class TrashCleanerApp :
    def __init__ (self ,root ):
        self .root =root
        self .root .title ("Автоматическая очистка корзины Windows")
        self .root .geometry ("600x500")
        self .root .configure (bg ='#f0f0f0')
        style =ttk .Style ()
        style .theme_use ('clam')
        self .cleaning =False
        self .setup_ui ()
    def setup_ui (self ):
        title_label =tk .Label (
        self .root ,
        text ="🗑️ Очистка корзины Windows",
        font =("Arial",16 ,"bold"),
        bg ='#f0f0f0',
        fg ='#2c3e50'
        )
        title_label .pack (pady =10 )
        info_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        info_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (info_frame ,text ="Информация о корзине:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        self .info_text =tk .Text (
        info_frame ,
        height =6 ,
        font =("Consolas",9 ),
        bg ='#ffffff',
        fg ='#2c3e50',
        wrap ='word',
        state ='disabled'
        )
        self .info_text .pack (fill ='x',pady =5 )
        button_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        button_frame .pack (fill ='x',padx =20 ,pady =10 )
        self .refresh_btn =tk .Button (
        button_frame ,
        text ="🔄 Обновить информацию",
        command =self .refresh_info ,
        bg ='#3498дб',
        fg ='white',
        font =("Arial",10 ,"bold"),
        relief ='flat',
        padx =20 ,
        pady =8
        )
        self .refresh_btn .pack (side ='left')
        self .clean_btn =tk .Button (
        button_frame ,
        text ="🗑️ Очистить корзину",
        command =self .start_cleaning ,
        bg ='#e74c3c',
        fg ='white',
        font =("Arial",10 ,"bold"),
        relief ='flat',
        padx =20 ,
        pady =8
        )
        self .clean_btn .pack (side ='left',padx =(10 ,0 ))
        options_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        options_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (options_frame ,text ="Опции очистки:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        self .force_clean_var =tk .BooleanVar ()
        self .show_details_var =tk .BooleanVar (value =True )
        tk .Checkbutton (
        options_frame ,
        text ="Принудительная очистка (игнорировать ошибки)",
        variable =self .force_clean_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).pack (anchor ='w')
        tk .Checkbutton (
        options_frame ,
        text ="Показать подробности процесса",
        variable =self .show_details_var ,
        bg ='#f0f0f0',
        font =("Arial",9 )
        ).pack (anchor ='w')
        auto_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        auto_frame .pack (fill ='x',padx =20 ,pady =10 )
        tk .Label (auto_frame ,text ="Автоматическая очистка:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        auto_options_frame =tk .Frame (auto_frame ,bg ='#f0f0f0')
        auto_options_frame .pack (fill ='x',pady =5 )
        self .auto_clean_var =tk .BooleanVar ()
        self .auto_clean_check =tk .Checkbutton (
        auto_options_frame ,
        text ="Включить автоматическую очистку",
        variable =self .auto_clean_var ,
        bg ='#f0f0f0',
        font =("Arial",9 ),
        command =self .toggle_auto_clean
        )
        self .auto_clean_check .pack (side ='left')
        self .interval_var =tk .StringVar (value ="7")
        interval_frame =tk .Frame (auto_options_frame ,bg ='#f0f0f0')
        interval_frame .pack (side ='left',padx =(20 ,0 ))
        tk .Label (interval_frame ,text ="Интервал (дни):",font =("Arial",9 ),bg ='#f0f0f0').pack (side ='left')
        interval_entry =tk .Entry (interval_frame ,textvariable =self .interval_var ,width =5 ,font =("Arial",9 ))
        interval_entry .pack (side ='left',padx =(5 ,0 ))
        log_frame =tk .Frame (self .root ,bg ='#f0f0f0')
        log_frame .pack (fill ='both',expand =True ,padx =20 ,pady =10 )
        tk .Label (log_frame ,text ="Лог операций:",font =("Arial",10 ,"bold"),bg ='#f0f0f0').pack (anchor ='w')
        self .log_text =tk .Text (
        log_frame ,
        height =8 ,
        font =("Consolas",9 ),
        bg ='#ffffff',
        fg ='#2c3e50',
        wrap ='word'
        )
        self .log_text .pack (fill ='both',expand =True ,pady =5 )
        scrollbar =tk .Scrollbar (self .log_text )
        scrollbar .pack (side ='right',fill ='y')
        self .log_text .config (yscrollcommand =scrollbar .set )
        scrollbar .config (command =self .log_text .yview )
        self .refresh_info ()
    def log_message (self ,message ):
        timestamp =datetime .now ().strftime ("%H:%M:%S")
        self .log_text .insert (tk .END ,f"[{timestamp }] {message }\n")
        self .log_text .see (tk .END )
        self .root .update ()
    def refresh_info (self ):
        self .info_text .config (state ='normal')
        self .info_text .delete (1.0 ,tk .END )
        try :
            result =subprocess .run (['powershell','-Command',
            'Get-ChildItem -Path "$env:USERPROFILE\\..\\$env:USERNAME\\$Recycle.Bin" -Recurse -Force | Измерение-Объект-Свойство Длина-Сумма'],
            capture_output =True ,text =True ,shell =True )
            if result .returncode ==0 :
                lines =result .stdout .strip ().split ('\n')
                for line in lines :
                    if 'Count'in line or 'Sum'in line :
                        self .info_text .insert (tk .END ,line +'\n')
            else :
                self .info_text .insert (tk .END ,"Не удалось получить информацию о корзине\n")
            try :
                result =subprocess .run (['cmd','/c','dir /s /a "$env:USERPROFILE\\..\\$env:USERNAME\\$Recycle.Bin"'],
                capture_output =True ,text =True ,shell =True )
                if result .returncode ==0 :
                    self .info_text .insert (tk .END ,"\nИнформация через каталог:\n")
                    self .info_text .insert (tk .END ,result .stdout [-500 :])
            except :
                pass
        except Exception as e :
            self .info_text .insert (tk .END ,f"Ошибка при получении информации: {e }\n")
        self .info_text .config (state ='disabled')
    def start_cleaning (self ):
        if self .cleaning :
            return
        result =messagebox .askyesno ("Подтверждение",
        "Вы уверены, что хотите очистить корзину?\nЭто действие нельзя отменить!")
        if not result :
            return
        self .cleaning =True
        self .clean_btn .config (state ='disabled')
        thread =threading .Thread (target =self .clean_trash )
        thread .daemon =True
        thread .start ()
    def clean_trash (self ):
        try :
            self .log_message ("Начинаем очистку корзины...")
            try :
                result =subprocess .run (['powershell','-Command',
                'Очистить-RecycleBin-Force'],
                capture_output =True ,text =True ,shell =True ,timeout =30 )
                if result .returncode ==0 :
                    self .log_message ("Корзина успешно очищена через PowerShell")
                else :
                    self .log_message (f"Ошибка PowerShell: {result .stderr }")
                    raise Exception ("PowerShell метод не сработал")
            except Exception as e :
                self .log_message (f"PowerShell метод не сработал: {e }")
                try :
                    recycle_bin_path =os .path .expanduser ("~\\..\\$Recycle.Bin")
                    if os .path .exists (recycle_bin_path ):
                        result =subprocess .run (['cmd','/c',f'rd /s /q "{recycle_bin_path }"'],
                        capture_output =True ,text =True ,shell =True ,timeout =30 )
                        if result .returncode ==0 :
                            self .log_message ("Корзина очищена через rd /s /q")
                        else :
                            self .log_message (f"Ошибка rd: {result .stderr }")
                    else :
                        self .log_message ("Путь к корзине не найден")
                except Exception as e2 :
                    self .log_message (f"Метод rd не сработал: {e2 }")
                    if self .force_clean_var .get ():
                        self .log_message ("Попытка принудительной очистки...")
                        self .manual_clean ()
                    else :
                        self .log_message ("Очистка не удалась. Попробуйте включить принудительную очистку.")
                        return
            self .log_message ("Очистка корзины завершена!")
            self .refresh_info ()
        except Exception as e :
            self .log_message (f"Ошибка при очистке: {e }")
        finally :
            self .cleaning =False
            self .clean_btn .config (state ='normal')
    def manual_clean (self ):
        try :
            recycle_bin_path =os .path .expanduser ("~\\..\\$Recycle.Bin")
            if os .path .exists (recycle_bin_path ):
                for root ,dirs ,files in os .walk (recycle_bin_path ,topdown =False ):
                    for file in files :
                        try :
                            file_path =os .path .join (root ,file )
                            os .remove (file_path )
                            if self .show_details_var .get ():
                                self .log_message (f"Удален файл: {file }")
                        except Exception as e :
                            if self .show_details_var .get ():
                                self .log_message (f"Не удалось удалить {file }: {e }")
                    for dir in dirs :
                        try :
                            dir_path =os .path .join (root ,dir )
                            os .rmdir (dir_path )
                            if self .show_details_var .get ():
                                self .log_message (f"Удалена папка: {dir }")
                        except Exception as e :
                            if self .show_details_var .get ():
                                self .log_message (f"Не удалось удалить папку {dir }: {e }")
        except Exception as e :
            self .log_message (f"Ошибка при ручной очистке: {e }")
    def toggle_auto_clean (self ):
        if self .auto_clean_var .get ():
            self .log_message ("Автоматическая очистка включена")
        else :
            self .log_message ("Автоматическая очистка отключена")
def main ():
    root =tk .Tk ()
    app =TrashCleanerApp (root )
    root .mainloop ()
if __name__ =="__main__":
    main ()