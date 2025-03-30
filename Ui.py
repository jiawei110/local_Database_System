import sys
import re
from PyQt5.QtWidgets import QMenuBar,QPlainTextEdit,QMainWindow,QMessageBox, QApplication,QDateTimeEdit, QWidget, QPushButton, QMessageBox, QLineEdit, QAction,QTableWidget ,QTableWidgetItem ,QVBoxLayout,QTabWidget, QHBoxLayout,QGridLayout, QInputDialog, QComboBox,QRadioButton, QGroupBox, QCheckBox,QLabel
from PyQt5.QtGui import QIntValidator,QDoubleValidator, QRegExpValidator, QPixmap
from PyQt5.QtCore import QRegExp
import PyQt5.QtCore as QtCore

import pandas as pd
import os
import shutil
from tkinter import filedialog as fd
file_path = "D:\\DB\\database\\database/"
type_path = "D:\\DB\\database\\database_data_type/"

all_database = []
all_table = {}

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def intersection(lst1,lst2):
    return sorted(list(set(lst1) & set(lst2)))

def relayout(tab, new_layout):
    if tab.layout() is not None:
        QWidget().setLayout(tab.layout())
    tab.setLayout(new_layout)

def rowSelectcheck(table):
    row_selected = []
    for i in range(table.rowCount()):
        if table.item(i,0).checkState() == 2:
            row_selected.append(i)
    return row_selected


def dateTime_check(dateTime,types):
    print(str(dateTime))
    print(str(types))
    if types == "datetime":
       try:
            date,time = dateTime.split(" ")[0],dateTime.split(" ")[1]
            year,month,day = int(date.split("-")[0]),int(date.split("-")[1]),int(date.split("-")[2])
            hour,minute,second = int(time.split(":")[0]),int(time.split(":")[1]),int(time.split(":")[2])
       except:
           return types + " error, unknown error"
       
    elif types == "date":
        try:
            year,month,day = int(dateTime.split("-")[0]),int(dateTime.split("-")[1]),int(dateTime.split("-")[2])
            hour,minute,second = 23,59,0     #fake
        except:
            return types + " error, unknown error"
        
    elif types == "time":
        try:
            hour,minute,second = int(dateTime.split(":")[0]),int(dateTime.split(":")[1]),int(dateTime.split(":")[2])
            year,month,day = 0,12,31 #fake
        except:
            return types + " error, unknown error"

    if year <0 or year >9999:
        return types + " error,year must be between 0000~9999"
    
    if month<=0 or month>12:
        return types+ " error, month must be between 1~12"
    
    ###day
    if(month%2 == 0):
        if (month ==2 and (year%4 == 0 and (year%100!= 0 or year%400==0))):     #lunar
                if(day <=0 or day >=29):
                    return types+" error, day in Febuary must be between 0~28 in lunar year"
        else:               
            if((day <=0 or day >=31) and month < 8):     #2,4,6
                return types+ " error, day must be between 1~30"
            if((day <=0 or day >31) and month >= 8 ):    #8,10,12
                return types+ " error, day must be between 1~31"
    if(month%2 == 1):
        if((day<=0 or day>31) and month < 8):        #1,3,5,7
            return types+ " error, day must be between 1~31"
        if((day<=0 or day>=31) and month >=8):       #9,11
            return types+" error, day must be between 1~30"
        ###

    if hour <0 or hour>=24:
        return types+ " error, hour must be between 0~23"
    
    if minute < 0 or minute >= 60:
        return types+ " error, minutes must be between 0~59"
    if second < 0 or second >=60:
        return types+ " error, second must be between 0~59"

    
    ##check complete
    return "No problem!"


def preventMistakeDialog(table,mode,folder="",file=""):
    reply = QMessageBox.information(mainWindow,'Drop data',"Are you sure?",QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
    if reply == QMessageBox.Ok: 
        print('Ok clicked')
        if len(rowSelectcheck(table))<1:
            no_row_msg = QMessageBox.information(mainWindow,'Drop data Error',"No row selected",QMessageBox.Ok)
            return
        drop(table,mode,folder,file)
        if mode == 0:                               #drop table
            refresh_leftside_bar()
            refresh_structure_tab_db(folder)
        if mode == 1:                               #drop column
            refresh_structure_tab_tb(folder,file)
            refresh_browse_tab_tb(folder,file)
        if mode == 2: 
            refresh_browse_tab_tb(folder,file)      #drop row

    

################
def refresh_sql_tab():
    def clr():
        sql_insertbox.setPlainText("")
    

    def runSQL():
        def whereConditioncheck(db,table):             #single condition only
            operator = ["<","<=","=",">=",">"]
            operator_select = -1
            row_selected = []
            #sql_text.split("where")[1]
            condition = re.split("where",sql_text,flags=re.IGNORECASE)[1]
            print(condition)
            print(len(condition.split("<")))
            if len(condition.split("=")) < 2:       #not include "="
                if len(condition.split("<")) == 2:           #<
                    operator_select = 0
                elif len(condition.split(">"))  == 2:           #>
                    operator_select = 4
                else:
                    empty_where_condition_error_msg = QMessageBox.information(mainWindow,'WHERE CONDITION ERROR',"UNDENTIFIED CONDITION",QMessageBox.Ok)
                    print("EMPTY WHERE CONDITION")      ###
                    return False
            else:              #include "="
                if "<" == condition.split("=")[0][-1]:  #<=
                    operator_select = 1
                elif ">" ==  condition.split("=")[0][-1]:    #>=
                    operator_select = 3
                else:                   #=
                    operator_select = 2
            print(operator_select)
            col1 , col2 = condition.split(operator[operator_select])[0].lstrip().rstrip() , condition.split(operator[operator_select])[1].lstrip().rstrip()
            col1_tb,col1_attr = "" ,""
            col2_tb,col2_attr = "" ,""
            default_table_ncsv = re.sub(".csv","",table,flags=re.IGNORECASE)
            print(default_table_ncsv)
            print(col1)
            if "." in col1:
                col1_tb,col1_attr = col1.split(".")[0],col1.split(".")[1]
            else:
                #table.replace(".csv","")
                col1_tb = default_table_ncsv
                col1_attr = col1
            if "." in col2 and  not is_float(col2):
                col2_tb,col2_attr = col2.split(".")[0],col2.split(".")[1]
            else:
                col2_tb = default_table_ncsv
                col2_attr = col2
            if col1_tb+".csv" not in all_table[str(current_lockon_database.text())] or col2_tb+".csv" not in all_table[str(current_lockon_database.text())]:
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT IN DATABASE",QMessageBox.Ok)
                return False  
            table_csv1 = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+col1_tb+".csv",encoding = "utf-8-sig")
            type_csv1 = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+col1_tb+".csv",encoding = "utf-8-sig")
            attributes1 = table_csv1.columns.tolist()
            if col1_attr not in attributes1:
                print("error, SELECTED COL:"+str(col1_attr)+" NOT IN TABLE: "+str(col1_tb))
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED COL:"+str(col1_attr)+" NOT IN TABLE: "+str(col1_tb),QMessageBox.Ok)
                return False  
            type_attr1 = type_csv1["type"].tolist()[attributes1.index(col1_attr)]

            table_csv2 = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+col2_tb+".csv",encoding = "utf-8-sig")
            type_csv2 = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+col1_tb+".csv",encoding = "utf-8-sig")
            attributes2 = table_csv2.columns.tolist()
            if "." in col2 and (not is_float(col2_attr)) and col2_attr not in attributes2:                #check col2 if col2 is attribute not value
                print("error, SELECTED COL:"+str(col2_attr)+" NOT IN TABLE: "+str(col2_tb))
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED COL:"+str(col2_attr)+" NOT IN TABLE: "+str(col2_tb),QMessageBox.Ok)
                return False  
            
            if (col1_tb == col2_tb) and (col1_attr in attributes1 and col2_attr in  attributes1):        #condition : table.xxx = table.yyy / xxx = yyy   #table set as select table
                colchk = table_csv1[[col1_attr,col2_attr]].values
                type_attr1 = type_csv2["type"].tolist()[attributes1.index(col1_attr)]
                type_attr2 = type_csv2["type"].tolist()[attributes1.index(col2_attr)]
                if(type_attr1 != type_attr2):
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: Different types in where condition: ("+str(type_attr1)+" , "+str(type_attr2)+")",QMessageBox.Ok)
                    return False  
                for rowchk in range(0,len(colchk)):
                    if operator_select ==0:
                        if colchk[rowchk][0] < colchk[rowchk][1]:
                            row_selected.append(rowchk)
                    elif operator_select == 1:
                        if colchk[rowchk][0] <= colchk[rowchk][1]:
                            row_selected.append(rowchk)

                    elif operator_select == 2:
                        if colchk[rowchk][0] == colchk[rowchk][1]:
                            row_selected.append(rowchk)
                    elif operator_select == 3:
                        if colchk[rowchk][0] >= colchk[rowchk][1]:
                            row_selected.append(rowchk)
                    elif operator_select == 4:
                        if colchk[rowchk][0] > colchk[rowchk][1]:
                            row_selected.append(rowchk)


            elif (col1_tb != col2_tb):                                      #equijoin
                type_attr1 = type_csv1["type"].tolist()[attributes1.index(col1_attr)]
                type_attr2 = type_csv2["type"].tolist()[attributes2.index(col2_attr)]
                if(type_attr1 != type_attr2):
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: Different types in where condition: ("+str(type_attr1)+" , "+str(type_attr2)+")",QMessageBox.Ok)
                    return False
                colchk1 = table_csv1[col1_attr].values
                colchk2 = table_csv2[col2_attr].values
                for i in range(len(colchk1)):
                    for j in range(len(colchk2)):
                        if colchk1[i] == colchk2[j]:
                            row_selected.append([i,j])
                    
            else:                                                           #condition : table.xxx = value / xxx = value
                type_attr1 = type_csv1["type"].tolist()[attributes1.index(col1_attr)]
                try:
                    if type_attr1 == "int" or type_attr1=="float":
                        col2_attr = float(col2_attr)
                    else:
                        if "'" not in col2_attr and '"' not in col2_attr:
                            error_type_msg = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"Type Error: "+str(type_attr1)+" : must include '' ",QMessageBox.Ok)
                            return False
                        col2_attr = col2_attr.replace("'","").replace('"',"")
                        if type_attr1 != "varchar":
                            response = dateTime_check(col2_attr,type_attr1)
                            if response != "No problem!":
                                stackErrorDialog = QMessageBox.information(mainWindow,"SQL_ERROR","value error, "+response, QMessageBox.Ok)
                                return False
                        
                except Exception as error:
                    print(error)
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: Different types in where condition: ("+str(type_attr1)+" , varchar)",QMessageBox.Ok)
                    return False
                
                colchk = table_csv1[col1_attr].values
                for rowchk in range(0,len(colchk)):
                    if operator_select == 0:
                        if colchk[rowchk] < col2_attr:
                            row_selected.append(rowchk)

                    elif operator_select == 1:
                        if colchk[rowchk] <= col2_attr:
                            row_selected.append(rowchk)

                    elif operator_select == 2:
                        if colchk[rowchk] == col2_attr:
                            row_selected.append(rowchk)

                    elif operator_select == 3:
                        if colchk[rowchk] >= col2_attr:
                            row_selected.append(rowchk)

                    elif operator_select == 4:
                        if colchk[rowchk] > col2_attr:
                            row_selected.append(rowchk)

            return row_selected

        def crafting_preprocessing(db,table,data_in,mode,row_selected = "",all_set = ""):           #all_set use for update
            print(data_in)
            data_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
            types_csv = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
            primary_key = types_csv.loc[types_csv["primary"] == 1].values
            primary_key = primary_key[0][0]
            data_type = types_csv["type"].values
            print(data_csv)
            
            attributes = data_csv.columns.tolist()
            attr_cnt = 0
            #data_preprocessed = {}
            for attr in attributes:
                attr_cnt = attributes.index(attr)
                #data_preprocessed[attr] = []
                #print(data_in)
                for count in range(len(data_in[attr])):
                    if mode == "update" or mode == "insert":
                        count = 0
                    if mode == "update" and attr not in all_set.keys():         #scan only set value and first value
                        #data_preprocessed[attr].append(data_in[attr][count])
                        break
                    print(type(data_in[attr][count]))
                    if attr == primary_key:
                        if len(data_in[attr][count].lstrip().strip()) <1:
                            empty_primary_error_msg = QMessageBox.information(mainWindow,'Primary Key Error',"null primary key not accepted: " + data_in[attr][count],QMessageBox.Ok)
                            print("null primary key")      ###
                            return False
                        if data_type[attr_cnt] == "int":
                            try:
                                prim = int(data_in[attr][count])
                            except:
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_type[attr_cnt]+" : int error",QMessageBox.Ok)
                                return False

                        elif data_type[attr_cnt] == "float":
                            try:
                                prim = float(data_in[attr][count])
                            except:
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_type[attr_cnt]+" : float error",QMessageBox.Ok)
                                return False     
                        else:
                            if "'" not in data_in[attr][count] and '"' not in data_in[attr][count]:
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_type[attr_cnt]+" : must include '' ",QMessageBox.Ok)
                                return False
                            prim = data_in[attr][count].replace("'","").replace('"',"")
                
                        if prim in data_csv[attr].values.tolist():
                                duplicate_name_primary_error_msg = QMessageBox.information(mainWindow,'Primary Key Error',"Primary key value duplicate: " + data_in[attr][count],QMessageBox.Ok)
                                print("primary key duplicate")      ###
                                return False

                    #print(data_type[attr_cnt])
                    if data_type[attr_cnt] == "int" or data_type[attr_cnt]=="float" or data_type[attr_cnt] == "varchar":
                        if data_type[attr_cnt] == "int" and  data_in[attr][count] != "":
                            try:
                                data_in[attr][count] = int(data_in[attr][count])
                            except Exception as error:
                                print(error)
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_in[attr][count]+" : int error",QMessageBox.Ok)
                                return False
                        if data_type[attr_cnt] == "float" and  data_in[attr][count] != "":
                            try:
                                data_in[attr][count] = float(data_in[attr][count])
                            except Exception as error:
                                print(error)
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_in[attr][count]+" : float error",QMessageBox.Ok)
                                return False
                        if data_type[attr_cnt] == "varchar" and data_in[attr][count] != "":
                            if "'" not in data_in[attr][count] and '"' not in data_in[attr][count]:
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_type[attr_cnt]+" : must include '' ",QMessageBox.Ok)
                                return False
                            
                            data_in[attr][count] = data_in[attr][count].replace("'","").replace('"',"")

                        if data_in[attr][count] == "":
                            if (types_csv["null"].values)[attr_cnt] == 1:
                                data_in[attr][count] = "_null_"


                    elif data_type[attr_cnt] == "date" or data_type[attr_cnt] == "time" or data_type[attr_cnt] == "datetime":
                        #print(len(data_in[attr][count].replace(":","").replace("-","").replace(" ","")))

                        if len(data_in[attr][count].replace(":","").replace("-","").replace(" ","")) == 0:    #處理 none default of time,datetime,date
                            if data_type[attr_cnt]=="datetime":
                                data_in[attr][count] = "0000-00-00 00:00:00"
                            elif data_type[attr_cnt]=="date":
                                data_in[attr][count] = "0000-00-00"
                            elif data_type[attr_cnt]=="time":
                                data_in[attr][count] = "00:00:00"
                        else:
                            if "'" not in data_in[attr][count] and '"' not in data_in[attr][count]:
                                error_type_msg = QMessageBox.information(mainWindow,"SQL_ERROR","Type Error: "+data_type[attr_cnt]+" : must include '' ",QMessageBox.Ok)
                                return False
                            data_in[attr][count] = data_in[attr][count].replace("'","").replace('"',"")                            
                            response = dateTime_check(data_in[attr][count],data_type[attr_cnt])
                            if response != "No problem!":
                                stackErrorDialog = QMessageBox.information(mainWindow,"SQL_ERROR","value error, "+response, QMessageBox.Ok)
                                return False
                    #data_preprocessed[attr].append(data_in[attr][count])
                    if mode == "insert" or mode == "update":        #only one row
                        break

            if mode == "insert":
                add_and_edit_rowData(data_in, mode = "add", folder = db, file = table, row_selected="")
            elif mode == "update":
                add_and_edit_rowData(data_in, mode = "edit", folder = db, file = table, row_selected=row_selected)
            

            refresh_browse_tab_tb(folder=db, file=table)
            tabs.setCurrentIndex(0)      
        def selectSQL():
            try:
                tables_list = re.split("where",re.split("from", sql_text, flags = re.IGNORECASE)[1], flags = re.IGNORECASE)[0].split(",")
                print(tables_list)
                if tables_list[0] == "":
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: INVALID TABLE SELECTED",QMessageBox.Ok)
                    return False  
                
                for i in range(len(tables_list)):
                    tables_list[i] = tables_list[i].lstrip().rstrip()
                    if tables_list[i]+".csv" not in all_table[str(current_lockon_database.text())]:
                        sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT IN DATABASE",QMessageBox.Ok)
                        return False  
                #print(tables_list)
                table = tables_list[0]

                equijoin_active = False
                equijoin_use_col = {}
                equijoin_use_len = 0
                toShowCol = []
                toShowRow = []
                if len(tables_list)>1:              #equijoins
                    for col in re.split("from" , re.sub("select","", sql_text, flags=re.IGNORECASE) , flags=re.IGNORECASE)[0].split(","):
                        print(col)
                        col = col.lstrip().rstrip()
                        try:
                            if col == "*":
                                for table_col in tables_list:
                                    table_col = table_col.lstrip().rstrip()
                                    col_table_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table_col+".csv",encoding = "utf-8-sig")
                                    equijoin_use_col[table_col] = col_table_csv.columns.tolist()
                                equijoin_active = True
                                break
                            table_col = col.split(".")[0].lstrip().rstrip()
                            if table_col not in tables_list:
                                print("error, select table not included")
                                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT INCLUDED",QMessageBox.Ok)
                                return False  
                            attr_col = col.split(".")[1].lstrip().rstrip()

                            col_table_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table_col+".csv",encoding = "utf-8-sig")
                            if equijoin_use_len<len(col_table_csv): equijoin_use_len = len(col_table_csv)
                            cas = col_table_csv.columns.tolist()
                            if attr_col == "*":
                                for cas_i in cas:
                                    if table_col not in equijoin_use_col.keys():
                                        equijoin_use_col[table_col] = []
                                    equijoin_use_col[table_col].append(cas_i)
                        
                            elif attr_col in cas:
                                if table_col not in equijoin_use_col.keys():
                                    equijoin_use_col[table_col] = []
                                equijoin_use_col[table_col].append(attr_col)
                            else:
                                print("error ,col:"+str(attr_col)+"not in table:"+str(table_col))
                                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED COL:"+str(attr_col)+" NOT IN TABLE: "+str(table_col),QMessageBox.Ok)
                                return False  
                            
                            equijoin_active = True
                        except Exception as error:
                            print("An error occurred:", error)
                            return
                else:
                    table = tables_list[0].rstrip().lstrip()
                    table = table+".csv"
                    condition = ""

                    table_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
                    attributes = table_csv.columns.tolist()
                    search_result ={}
                    aggregration_func = ["count","avg","sum","max","min"]
                    aggr_active = False
                    #
                    #sql_text.replace("select","").split("from")[0].split(",")
                    for col in re.split("from" , re.sub("select","", sql_text, flags=re.IGNORECASE) , flags=re.IGNORECASE)[0].split(","):
                        col = col.lstrip().rstrip()
                        col_raw = col
                        if col.split("(")[0].lstrip().rstrip() in aggregration_func:
                            aggr_active = True
                            col = re.find(r'\(.*?\)',col).replace("(","").replace(")","")
                        if col == "*":
                            if aggr_active:
                                toShowCol.append(col_raw)
                            toShowCol = attributes.copy()
                            break
                        elif col in attributes:
                            if aggr_active:
                                toShowCol.append(col_raw)
                            toShowCol.append(col)
                        else:
                            print("error ,select col:"+str(col)+" not in table: "+str(table))
                            sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED COL:"+str(col)+" NOT IN TABLE: "+str(table),QMessageBox.Ok)
                            return False  
                print(equijoin_use_col)
                if "where" in sql_text:  #....
                    toShowRow = whereConditioncheck(current_lockon_database.text(),table)
                else:
                    if equijoin_active:
                        key = list(equijoin_use_col.keys())
                        print(key)
                        table_csv1 = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+key[0]+".csv",encoding = "utf-8-sig")
                        rowcount1 = len(table_csv1)
                        table_csv2 = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+key[1]+".csv",encoding = "utf-8-sig")
                        rowcount2 = len(table_csv2)
                        for i in range(rowcount1):
                            for j in range(rowcount2):
                                toShowRow.append([i,j])
                    else:
                        table_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
                        toShowRow = range(len(table_csv))
                if equijoin_active:
                    toShowRowSing = []
                    toShowTable = list(equijoin_use_col.keys())[0]
                    for i in range(len(toShowRow)):
                        toShowRowSing.append(toShowRow[i][0])
                    print(toShowRowSing)

                    csv_table = refresh_browse_tab_tb(str(current_lockon_database.text()),str(toShowTable)+".csv",[toShowRowSing , equijoin_use_col[toShowTable]] ,equijoin= "Yes")
                    for t in equijoin_use_col.keys():
                        if t == list(equijoin_use_col.keys())[0]:
                            continue
                        toShowRowSing = []
                        toShowTable = t
                        toShowCol = equijoin_use_col[toShowTable]
                        print(toShowCol)
                        for i in range(len(toShowRow)):
                            toShowRowSing.append(toShowRow[i][1])
                        currentcol = csv_table.columnCount()
                        csv_table.setColumnCount(currentcol+len(toShowCol))
                        table_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+toShowTable+".csv",encoding = "utf-8-sig")   
                        types_csv = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+toShowTable+".csv",encoding = "utf-8-sig")   
                        for i in range(len(toShowCol)):
                            print(toShowCol[i])
                            csv_table.setHorizontalHeaderItem(currentcol+i,QTableWidgetItem(toShowTable+"."+toShowCol[i]))
                        for col in range(len(toShowCol)):
                            data_col = table_csv[toShowCol[col]].values.tolist()
                            datatype = types_csv["type"].values.tolist()[col]
                            print(datatype)
                            rowindisplay = 0
              #select
                            data_col_select = []
                            for rowc in toShowRowSing:
                                data_col_select.append(data_col[rowc])
                            data_col = data_col_select
                            #print(data_col)
                            for data in data_col:
                                if str(data) == "nan": data = ""   
                                elif str(data) == "_null_": data = "null" 
                                elif datatype == "int":
                                    data = int(data)
                                elif datatype == "float":
                                    data = float(data)

                                item = QTableWidgetItem(str(data))
                                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                                csv_table.setItem(rowindisplay,currentcol+col,item)
                                rowindisplay = rowindisplay+1
                             
                else:
                    refresh_browse_tab_tb(str(current_lockon_database.text()),table,[toShowRow,toShowCol])
                tabs.setCurrentIndex(0)
                        
            except Exception as error:
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR "+str(table),QMessageBox.Ok)
                print("An error occurred:", error)
                return False   
            
        def insertSQL():
            try: 
                db = str(current_lockon_database.text())
                #re.split("from" , re.sub("insert into","", sql_text, flags=re.IGNORECASE) , flags=re.IGNORECASE)[0].split(",")
                table = re.sub("insert into","", sql_text, flags=re.IGNORECASE).lstrip().rstrip().split(" ")[0].split("(")[0]+".csv"
                if table not in all_table[db]:
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT IN DATABASE",QMessageBox.Ok)
                    return False  

                data_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
                types_csv = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")

                data_type = types_csv["attribute"].values
                #print(data_csv)
                
                attributes = data_csv.columns.tolist()
                txt_in_paran = re.findall(r'\(.*?\)',sql_text)
                
                attributes_select,values = [],[]
                if len(txt_in_paran)== 1:       #values only
                    attributes_select = attributes
                    values = txt_in_paran[0].replace("(","").replace(")","").split(",")
                    for i in range(len(values)):
                        values[i] = values[i].lstrip().rstrip()

                elif len(txt_in_paran) == 2:
                    attributes_select = txt_in_paran[0].replace("(","").replace(")","").split(",")
                    print(attributes_select)
                    for i in range(len(attributes_select)):
                        attributes_select[i] = attributes_select[i].lstrip().rstrip()
                    values = txt_in_paran[1].replace("(","").replace(")","").split(",")
                    print(values)
                    for i in range(len(values)):
                        values[i] = values[i].lstrip().rstrip()
                    if intersection(attributes_select,attributes) != sorted(attributes_select):
                        sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: OBTAIN ATTRIBUTE NOT IN TABLE",QMessageBox.Ok)
                        print("obtain attribute not in table")
                        return False
                else:
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SET AND VALUES NOT INSERTED",QMessageBox.Ok)
                    return False   
                if len(attributes_select) != len(values):
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SET AND VALUES NOT SAME SIZE",QMessageBox.Ok)
                    print("col and value size not same")
                    return False

                data_in = {}
                for attr in attributes:
                    if attr in attributes_select:
                        data_in[attr] = []
                        data_in[attr].append(values[attributes_select.index(attr)])
                    else:
                        data_in[attr]=[]
                        data_in[attr].append("")
                    print(data_in)
                crafting_preprocessing(db,table,data_in,mode="insert")    

                
            except Exception as error:
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"UNDEFINED SQL ERROR",QMessageBox.Ok)
                print("An error occurred:", error)
                return False  
            
        def updateSQL():
            try:
                db = current_lockon_database.text()
                #re.sub("update","", sql_text, flags=re.IGNORECASE)
                table = re.sub("update","", sql_text, flags=re.IGNORECASE).lstrip().split(" ")[0]+".csv"
                if table not in all_table[db]:
                    sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT IN DATABASE",QMessageBox.Ok)
                    return False  
                    
                data_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
                types_csv = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
                primary_key = types_csv.loc[types_csv["primary"] == 1].values
                primary_key = primary_key[0][0]
                attributes = types_csv["attribute"].values.tolist()
                types = types_csv["type"].values
                set_string = ""
                data_in = {}
                all_set = {}
                contition = []
                row_selected = []
                replace_result = re.sub("update "+table.replace(".csv","")+" set ","", sql_text, flags=re.IGNORECASE)
                split_result = re.split("where",replace_result,flags=re.IGNORECASE)
                if "where" in sql_text:
                    #sql_text.replace("update "+table.replace(".csv","")+" set ","").split("where")[0]
                    set_string = split_result[0]
                    row_selected = whereConditioncheck(db,table)
                   
                else:
                    set_string = split_result[0]
                    print(set_string)
                    row_selected = range(len(data_csv))
                for target in set_string.split(","):
                    if len(target.split("="))<2:
                        sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SET ERROR",QMessageBox.Ok)
                        return False  
                    
                    attribute = target.split("=")[0].lstrip().rstrip()
                    value = target.split("=")[1].lstrip().rstrip()
                    print(value)
                    
                    print(attributes)
                    if attribute not in attributes:
                        sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: ATTRIBUTE NOT IN TABLE",QMessageBox.Ok)
                        print("attribute error")
                        return False    
                    if attribute == primary_key and len(row_selected)>1:       
                        sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: Duplicate entry "+str(value)+" for key 'PRIMARY'",QMessageBox.Ok)
                        return False
                    """
                    if types[attributes.index(attribute)] == "int" or types[attributes.index(attribute)] == "varchar":
                        if types[attributes.index(attribute)] == "int" and  value != "":
                            try:
                                value = int(value)
                            except Exception as error:
                                error_type_msg = QMessageBox.Information(mainWindow,"Type Error: "+value+" : "+error,QMessageBox.Ok)
                                return False
                            
                        if value == "":
                            if (types_csv["null"].values.tolist())[attributes.index(attribute)] == 1:
                                value = "null"
                    elif types[attributes.index(attribute)] == "date" or types[attributes.index(attribute)] == "time" or types[attributes.index(attribute)] == "datetime":
                        #print(len(data_in[attr][count].replace(":","").replace("-","").replace(" ","")))
                        if len(value.replace(":","").replace("-","").replace(" ","")) == 0:    #處理 none default of time,datetime,date
                            if types[attributes.index(attribute)]=="datetime":
                                value = "0000-00-00 00:00"
                            elif types[attributes.index(attribute)]=="date":
                                value = "0000-00-00"
                            elif types[attributes.index(attribute)]=="time":
                                value = "00:00"
                        else:
                            response = dateTime_check(value,types[attributes.index(attribute)])
                            if response != "No problem!":
                                stackErrorDialog = QMessageBox.information(mainWindow,"Error message","value error, "+response, QMessageBox.Ok)
                                return False
                                """
                    
                    all_set[attribute] = value       

                for attribute in attributes:
                    data_prev_all = data_csv[attribute].values
                    data_in[attribute] = []
                    for rowc in row_selected:
                        if attribute in all_set.keys():
                            data_in[attribute].append(all_set[attribute])
                        else:
                            data_in[attribute].append(data_prev_all[rowc])
                
                crafting_preprocessing(db=db,table=table,data_in=data_in,mode="update",row_selected=row_selected,all_set = all_set)      #scan all(slower) , new: scan changed attribute only
                #print(data_in)
                #add_and_edit_rowData(data_in, mode = "edit", folder = db, file = table, row_selected=row_selected)
                #refresh_browse_tab_tb(folder = db,file = table)
                
                
            except Exception as error:
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"UNDEFINED SQL ERROR",QMessageBox.Ok)
                print("An error occurred:", error)
                return False 

        def deleteSQL():
            #sql_text.replace("delete from","")         
            table = re.sub("delete from","",sql_text,flags=re.IGNORECASE).lstrip().split(" ")[0] + ".csv"
            db = str(current_lockon_database.text())
            if table not in all_table[db]:
                sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: SELECTED TABLE NOT IN DATABASE",QMessageBox.Ok)
                return False  
            data_csv = pd.read_csv(file_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
            types_csv = pd.read_csv(type_path+str(current_lockon_database.text())+"/"+table,encoding = "utf-8-sig")
            row_selected = []
            if "where" in sql_text:
                row_selected = whereConditioncheck(db,table)
            else:
                row_selected = range(len(data_csv.index))
            drop(file=table, folder = db, mode="deleteSQL" , table = "",row_selected = row_selected)
            refresh_browse_tab_tb(folder=db,file =table)
            tabs.setCurrentIndex(0)

        sql_text = str(sql_insertbox.toPlainText())
        sql_text_lower = str(sql_insertbox.toPlainText()).lower()
        lst = (str(sql_insertbox.toPlainText()).lower()).split(" ")
        #print(lst)
        func_name = lst[0]
        if "select " in  sql_text_lower and sql_text_lower.index("select") == 0 and "from" in sql_text_lower:
        #if func_name == "select":
            selectSQL()
        elif "insert into" in sql_text_lower and sql_text_lower.index("insert into") == 0 and "values" in sql_text_lower:
            insertSQL()
        elif "update" in sql_text_lower and "set" in sql_text_lower and sql_text_lower.index("update") == 0:
            updateSQL()
        elif "delete from" in sql_text_lower and sql_text_lower.index("delete from") == 0:
            deleteSQL()
        else:
            sql_error_message = QMessageBox.information(mainWindow,'SQL_SYNTAX_ERROR',"SQL_SYNTAX_ERROR: 無指令符合",QMessageBox.Ok)
            return False      

    
    main_layout = QVBoxLayout()
    layoutbtn = QHBoxLayout()

    sql_insertbox = QPlainTextEdit()
    runbtn = QPushButton("Run")
    runbtn.clicked.connect(runSQL)
    clearbtn = QPushButton("Clear")
    clearbtn.clicked.connect(clr)
    layoutbtn.addStretch(3)
    layoutbtn.addWidget(runbtn)
    layoutbtn.addStretch(1)
    layoutbtn.addWidget(clearbtn)
    layoutbtn.addStretch(3)
    main_layout.addWidget(sql_insertbox)
    main_layout.addLayout(layoutbtn)
    relayout(Sql_tab,main_layout)
    
def refresh_leftside_bar():

    leftside_table.clearContents()
    leftside_table.setColumnCount(2)
    leftside_table.setHorizontalHeaderItem(0,QTableWidgetItem("DataBase"))
    leftside_table.setHorizontalHeaderItem(1,QTableWidgetItem("Table"))
    for root,dirs,files in os.walk(file_path):
        i = 0
        all_database=[]
        for folder in  dirs:
            all_database.append(folder)
            leftside_table.setRowCount(i+1)
            item = QTableWidgetItem(folder)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            leftside_table.setItem(i,0,item)
            block = QTableWidgetItem("")
            block.setFlags(QtCore.Qt.NoItemFlags)
            leftside_table.setItem(i,1,block)
            i = i + 1
            all_table[folder]=[]
            for root,dirs,files  in os.walk(file_path+folder+"/"):
                for file in files:
                    all_table[folder].append(file)
                    leftside_table.setRowCount(i+1)

                    file = file.replace(".csv","")
                    item = QTableWidgetItem(file)
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled )
                    leftside_table.setItem(i,1,item)
                    item_fol = QTableWidgetItem(folder)
                    item_fol.setFlags(QtCore.Qt.NoItemFlags)
                    leftside_table.setItem(i,0,item_fol)
                    i = i + 1

    leftside_table.doubleClicked.connect(open_both)
    leftside_table.setFixedWidth(300)
################
def refresh_structure_tab_db(folder):
    
        
    main_layout = QVBoxLayout()
    print(folder)
    table_list = QTableWidget()
    table_list.setColumnCount(2)
    table_list.setHorizontalHeaderItem(0,QTableWidgetItem("checkbox"))
    table_list.setHorizontalHeaderItem(1,QTableWidgetItem("table"))
    #table_list.setHorizontalHeaderItem(2,QTableWidgetItem("row"))
    table_list.setRowCount(0)
    for root,dirs,files in os.walk(file_path+folder+"/"):
        table_list.setRowCount(len(files))
        row = 0
        for file in files:
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            table_list.setItem(row,0,chkBoxItem)
            item = QTableWidgetItem(file)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            table_list.setItem(row,1,item)
            row = row+1
    addTableButton = QPushButton("Add table")
    addTableButton.clicked.connect(lambda: refresh_craft_tab(2,folder))
    dropTableButton = QPushButton("Drop table")
    dropTableButton.clicked.connect(lambda:preventMistakeDialog(table_list,0,folder))
    main_layout.addWidget(table_list)
    main_layout.addWidget(addTableButton)
    main_layout.addWidget(dropTableButton)
    relayout(Structure_tab,main_layout)
    #Structure_tab.setLayout(main_layout)
    tabs.setCurrentIndex(1)

#############
def refresh_structure_tab_tb(folder,file):
    main_layout = QVBoxLayout()
    dataDetail_csv = pd.read_csv(type_path+folder+"/"+file,engine = "python",encoding='utf-8-sig')
    columns = dataDetail_csv.columns.tolist()
    primary_check_lst = dataDetail_csv["primary"].tolist()
    primary_key = ""
    for i in range(len(primary_check_lst)):
        if primary_check_lst[i] == 1:
            primary_key = i
        
    table =QTableWidget()
    table.setColumnCount(len(dataDetail_csv.columns)-1 + 1)             #+1 for checkbox
    table.setHorizontalHeaderItem(0,QTableWidgetItem("checkbox"))
    for i in range(len(columns)-1):
        table.setHorizontalHeaderItem(i+1,QTableWidgetItem(columns[i]))

    row_count = len(dataDetail_csv[columns[0]].values.tolist())
    table.setRowCount(row_count)
    for i in range(row_count):
        if i == primary_key:
            block = QTableWidgetItem("")
            block.setFlags(QtCore.Qt.NoItemFlags)
            table.setItem(i,0,block)
            continue
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        table.setItem(i,0,chkBoxItem)

    for col in range(len(columns)-1):
        data_col = dataDetail_csv[columns[col]].values.tolist()
        #table.setRowCount(len(data_col))
        row = 0
        for data in data_col:
            #print(type(data))
            if columns[col] == "null":
                if data == 0:
                    data = "No"
                elif data == 1:
                    data = "Yes"
            if columns[col] == "attribute":
                if row ==primary_key:
                    data = str(data)+" (primary key)"

            if str(data) == "nan": data = "none"                #type of nan ->float
            if str(data) == "_null_": data = "null" 
            item = QTableWidgetItem(str(data))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            table.setItem(row,col+1,item)
            row = row+1
    addColButton = QPushButton("Add Column")
    dropColButton = QPushButton("Drop Column")
    addColButton.clicked.connect(lambda: refresh_craft_tab(3,folder= folder,file=file))     #add col
    dropColButton.clicked.connect(lambda: preventMistakeDialog(table,mode=1,folder= folder,file = file))

    main_layout.addWidget(table)
    main_layout.addWidget(addColButton)
    main_layout.addWidget(dropColButton)
    relayout(Structure_tab,main_layout)
        
        


    
def refresh_browse_tab_tb(folder,file,select_result="None", equijoin="No"):
    main_layout = QVBoxLayout()
    row_count = 0
    types_csv = pd.read_csv(type_path+folder+"/"+file,encoding = "utf-8-sig")
    header = types_csv["attribute"].values.tolist()
    print(header)
    try:
        primary_key = (types_csv['primary'].values.tolist()).index(1)
        primary_attr = header[primary_key]
        header[primary_key] = str(header[primary_key]) + " (primary key)"
    except:
        print("auto_detect no primary,jump")
    
    db= pd.read_csv(file_path+folder+"/"+file,encoding = 'utf-8-sig', names = header)
    #print(db)
    db = db.drop(0)
    csv_table = QTableWidget()
    row_count = len( db[header[primary_key]].values.tolist() )
    print(row_count)
    
    #Step1: set row,col count, set header
    if select_result !="None":          #select
        row_count = len(select_result[0])
        header = select_result[1]
        print(row_count)
        print(header)

    csv_table.setRowCount(row_count)
    csv_table.setColumnCount(len(header)+1)

    csv_table.setHorizontalHeaderItem(0,QTableWidgetItem("checkbox"))
    for i in range(len(header)):
        if header[i] == primary_attr:
            header[i] = str(header[i])+" (primary key)"
        csv_table.setHorizontalHeaderItem(i+1,QTableWidgetItem(header[i]))

    #Step2: add item
    for i in range(row_count):
        chkBoxItem = QTableWidgetItem()
        if equijoin == "No":
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
        else:
            chkBoxItem.setFlags(QtCore.Qt.NoItemFlags)
        csv_table.setItem(i,0,chkBoxItem)

    for col in range(len(header)):
        data_col = db[header[col]].values.tolist()
        datatype = types_csv["type"].values.tolist()[col]
        print(datatype)
        if len(data_col)>row_count and row_count != len(select_result[0]):
            csv_table.setRowCount(len(data_col))
            row_count = len(data_col)
        row = 0
        if select_result !="None":              #select
            data_col_select = []
            for rowc in select_result[0]:
                data_col_select.append(data_col[rowc])
            data_col = data_col_select
        #print(data_col)
        for data in data_col:
            if str(data) == "nan": data = ""    
            elif str(data) == "_null_":data = "null"
            elif datatype == "int":
                data = int(data)
            elif datatype == "float":
                data = float(data)

            item = QTableWidgetItem(str(data))
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            csv_table.setItem(row,col+1,item)
            row = row+1

            
    addRowButton = QPushButton("Add Row")
    dropRowButton = QPushButton("Drop Row")
    editRowButton = QPushButton("Edit Row")
    searchTableButton = QPushButton("Search")
    addRowButton.clicked.connect(lambda:refresh_craft_tab(4,folder,file,csv_table))             #add rowData
    dropRowButton.clicked.connect(lambda:preventMistakeDialog(csv_table,2,folder,file))
    editRowButton.clicked.connect(lambda:refresh_craft_tab(5,folder,file,csv_table))            #edit rowData
    searchTableButton.clicked.connect(lambda:searchDialog(csv_table,"searchInTable"))
    main_layout.addWidget(csv_table)
    if equijoin == "Yes":
        relayout(Browse_tab,main_layout)
        return csv_table
    main_layout.addWidget(addRowButton)
    main_layout.addWidget(dropRowButton)
    main_layout.addWidget(editRowButton)
    main_layout.addWidget(searchTableButton)
    relayout(Browse_tab,main_layout)
    #Browse_tab.setLayout(main_layout)
    tabs.setCurrentIndex(0)

############
def refresh_craft_tab(mode,folder =0 ,file = 0 , table = 0):
    main_layout = QVBoxLayout()
    if mode == 0:           #create   database
        create_database_tab(main_layout)
    if mode == -1:          #drop database
        drop_database_tab(main_layout)
    if mode == 2:           #create_table
        createAndAdd_table_tab(main_layout,"create",folder)
        tabs.setCurrentIndex(2)
    if mode == 3:           #addon table
        createAndAdd_table_tab(main_layout,"add",folder,file)
        tabs.setCurrentIndex(2)
    if mode == 4:           #add rowData
        addRowData_editRowData_element_tab(main_layout,"add",table,folder,file)
        tabs.setCurrentIndex(2)
    if mode == 5:           #edit rowData
        if len(rowSelectcheck(table))<1:
            no_row_msg = QMessageBox.information(mainWindow,'Drop data Error',"No row selected",QMessageBox.Ok)
            return
        addRowData_editRowData_element_tab(main_layout,"edit",table,folder,file)
        tabs.setCurrentIndex(2)
    relayout(Craft_tab,main_layout)  
    #Craft_tab.setLayout(main_layout)

def refresh_import_tab(folder,file):
    imported_csv_path = ""
    def inputFileDialog():
        filetypes = (
            ('csv files (*.csv)', '*.csv'),
            ('All files', '*.*')
        )
        imported_csv_path = fd.askopenfilename(
            title="import a csv",
            initialdir='/',
            filetypes=filetypes)
        go_button.setEnabled(True)
        csv.setText(str(imported_csv_path).split("/")[-1])
        full_imported_file_path.setText(imported_csv_path)

    main_layout = QVBoxLayout()
    horizontal_layout2 = QHBoxLayout()
    Title = QLabel("Importing into table :'"+file+"'")

    text1 = QLabel("Browse your computer: ")
    import_button = QPushButton("Choose File")
    csv = QLabel("No file chosen")
    full_imported_file_path = QLabel("")
    go_button = QPushButton("Go")
    import_button.clicked.connect(inputFileDialog)
    go_button.clicked.connect(lambda: import_csv(full_imported_file_path.text(),folder,file))
    horizontal_layout2.addWidget(text1)
    horizontal_layout2.addWidget(import_button)
    horizontal_layout2.addWidget(csv)
    horizontal_layout2.addStretch(5)
    main_layout.addWidget(Title)
    main_layout.addLayout(horizontal_layout2)
    main_layout.addWidget(go_button)
    main_layout.addStretch(5)
    relayout(Import_tab,main_layout)
    #Import_tab.setLayout(main_layout)
    tabs.setCurrentIndex(3)
    

        

#############  
def create_database_tab(main_layout):
    horizon_interface = QHBoxLayout()
    Text = QLabel("Create DataBase: ")
    textbox = QLineEdit()
    #textbox.resize(100, 20)
    create_btn = QPushButton("Create")
    create_btn.clicked.connect(lambda: create_database(textbox.text()))
    horizon_interface.addWidget(Text)
    horizon_interface.addWidget(textbox)
    horizon_interface.addWidget(create_btn)

    main_layout.addLayout(horizon_interface)
    tabs.setCurrentIndex(2)

def create_database(new_db):
    for root,dirs,files in os.walk(file_path):
        if new_db in files:
            print(new_db,": database already exists")
            return False
    os.makedirs(file_path+new_db, exist_ok=False)
    os.makedirs(type_path+new_db, exist_ok=False)
    refresh_leftside_bar()
    relayout(Craft_tab,QVBoxLayout())
    
###################
def drop_database_tab(main_layout):
    horizon_interface = QHBoxLayout()
    horizon_interface.setSpacing(0)
    Text = QLabel("Drop DataBase: ")
    delete_btn = QPushButton("Drop")
    delete_btn.clicked.connect(lambda: drop_database(str(dataBase_lst.currentText())))
    dataBase_lst = QComboBox()
    #dataBase_lst.activated[str].connect(drop_database)
    for root,dirs,files in os.walk(file_path):
        print(dirs)
        dataBase_lst.addItems(dirs)
    horizon_interface.addWidget(Text)
    horizon_interface.addWidget(dataBase_lst)
    horizon_interface.addWidget(delete_btn)
    main_layout.addLayout(horizon_interface)
    tabs.setCurrentIndex(2)

def drop_database(db_to_drop):
    shutil.rmtree(file_path+db_to_drop)
    shutil.rmtree(type_path+db_to_drop)
    refresh_leftside_bar()  
    relayout(Craft_tab,QVBoxLayout())


def createAndAdd_table_tab(main_layout,mode,folder="",file=""):        
    
    def editMain():
        #print(tableName_input.text())
        def typeComboboxTriggerEvent(attr_type):
            #widget = 
            index = int(attr_type.split(".")[0])
            attr_type = attr_type.split(".")[1]
            length_in[index].setText("")
            default_in[index].setText("")
            if attr_type == "int":
                length_int_validator = QIntValidator()
                length_int_validator.setRange(0,255)
                #top not activated
                length_in[index].setValidator(length_int_validator)

                default_int_validator = QIntValidator()
                integer = QLineEdit()
                default_in[index] = integer
                default_in[index].setValidator(default_int_validator)

            if attr_type == "float":
                length_int_validator = QIntValidator()
                length_in[index].setValidator(length_int_validator)

                default_float_validator = QDoubleValidator()
                floating_num = QLineEdit()
                default_in[index] = floating_num
                default_in[index].setValidator(default_float_validator)


            if attr_type == "varchar":
                length_int_validator = QIntValidator()
                length_in[index].setValidator(length_int_validator)

                varchar = QLineEdit()
                default_in[index] = varchar

            if attr_type == "date":
                length_int_validator = QIntValidator()
                length_in[index].setValidator(length_int_validator)
                
                date = QLineEdit()
                date.setInputMask("0000-00-00")
                #date = QDateTimeEdit()
                #date.setDisplayFormat("dd-MM-yyyy")
                default_in[index] = date

            if attr_type == "datetime":
                length_int_validator = QIntValidator()
                length_int_validator.setRange(0,6)
                length_in[index].setValidator(length_int_validator)

                datetime = QLineEdit()
                datetime.setInputMask("0000-00-00 00:00:00")
                #datetime = QDateTimeEdit()
                #datetime.setDisplayFormat("dd-MM-yyyy HH:mm")
                default_in[index] = datetime

            if attr_type == "time":
                length_int_validator = QIntValidator()
                length_int_validator.setRange(0,6)
                length_in[index].setValidator(length_int_validator)

                time = QLineEdit()
                time.setInputMask("00:00:00")
                #time = QDateTimeEdit()
                #time.setDisplayFormat("HH:mm")
                default_in[index] = time

            editlayout.addWidget(length_in[index],index+1,2)
            editlayout.addWidget(default_in[index],index+1,4)
                

        def clearEditLayout():
            for i in range(len(attributes_in)):
                attributes_in[i].setText("")
                types_in[i].setCurrentIndex(0)
                length_in[i].setText("")
                null_in[i].setChecked(False)
                default_in[i].setText("")
                primary_in[i].setChecked(False)
        def crafting_preprocessing():
            try:
                attr_in_table = []
                if mode == "add":
                    type_csv =pd.read_csv(type_path+folder+"/"+file,encoding="utf-8-sig")
                    attr_in_table = type_csv["attribute"].values.tolist()
                attributes = []
                types=[]
                length=[]
                null=[]
                default=[]
                primary = []
                for i in range(len(attributes_in)):
                    if len(attributes_in[i].text())<1:
                        add_attribute_error_msg = QMessageBox.information(mainWindow,'Add Error',"empty attribute detected: " + str(attributes_in[i].text()),QMessageBox.Ok)
                        return False                   
                    if str(attributes_in[i].text()) in attr_in_table:
                        add_attribute_error_msg = QMessageBox.information(mainWindow,'Add Error',"Attributes already exist: " + str(attributes_in[i].text()),QMessageBox.Ok)
                        return False
                    if str(attributes_in[i].text()) in attributes:
                        duplicate_attribute_name_error_msg = QMessageBox.information(mainWindow,'Add Error',"Duplicate attributes name added: " + str(attributes_in[i].text()),QMessageBox.Ok)
                        return False
                    attributes.append(str(attributes_in[i].text()))
                    types.append(str(types_in[i].currentText().split(".")[1]))
                    if len(length_in[i].text())<1:
                        if types[-1] == "int" or types[-1] == "float":
                            length_in[i].setText(str(4))
                        elif types[-1] == "varchar":
                            length_in[i].setText(str(10))
                        elif types[-1] == "datetime" or types[-1] == "date" or types[-1] == "time":
                            length_in[i].setText(str(6))

                    length.append(length_in[i].text())
                    if null_in[i].isChecked() is False:
                        null.append(0)
                        if len(default_in[i].text())<1:         #no insert
                            default.append("")
                    else:
                        null.append(1)
                        if len(default_in[i].text())<1:         #no insert
                            default.append("_null_")
                    
                    if len(default_in[i].text())>=1:
                    
                        if types[i] == "date" or types[i] == "time" or types[i] == "datetime":
                                if len(default_in[i].text().replace(":","").replace("-","").replace(" ","")) == 0:    #處理 none default of time,datetime,date
                                    if types[i]=="datetime":
                                        default_in[i].setText("0000-00-00 00:00:00")
                                    elif types[i]=="date":
                                        default_in[i].setText("0000-00-00")
                                    elif types[i]=="time":
                                        default_in[i].setText("00:00:00")
                                else:
                                    response = dateTime_check(default_in[i].text(),types[i])
                                    if response != "No problem!":
                                        stackErrorDialog = QMessageBox.information(mainWindow,"Error message","default error, row: "+str(i)+" "+response, QMessageBox.Ok)
                                        return
                                
                        default.append(str(default_in[i].text()))
                    if primary_in[i].isChecked() is False:
                        primary.append(0)
                    else:
                        primary.append(1)
                if 1 not in primary and mode == "create":
                    primary[0] = 1
                if mode == "create":
                    create_table(attributes,types,length,null,default,primary,tableName_input.text(),current_lockon_database.text())
                    refresh_structure_tab_db(current_lockon_database.text())
                    #refresh_browse_tab_tb(folder = folder,file = tableName_input.text()+".csv")
                    refresh_leftside_bar()
                    #tabs.setCurrentIndex(0)
                    relayout(Craft_tab,QVBoxLayout())
                if mode == "add":
                    add_colAttribute(attributes,types,length,null,default,primary,tableName_input.text(),current_lockon_database.text())
                    refresh_browse_tab_tb(current_lockon_database.text(),tableName_input.text())
                    refresh_structure_tab_tb(current_lockon_database.text(),tableName_input.text())
                    tabs.setCurrentIndex(0)
                    relayout(Craft_tab,QVBoxLayout())
            except Exception as error:
                print("An error occurred:", error)
                return False

        

        types=["int","float","varchar","date","datetime","time"]
        #types=["int","varchar",,"date","datetime","time"]
        attrNum = int(attrNum_input.text())
        if str(tableName_input.text()).rstrip().lstrip()+".csv" in all_table[current_lockon_database.text()] and mode == "create":
            duplicate_table_error_msg = QMessageBox.information(mainWindow,'Table Error',"Table already exist: " + tableName_input.text(),QMessageBox.Ok)
            return False
    
        craftButton.setEnabled(False)
        clearButton.setEnabled(False)
        attrNum_input.setReadOnly(True)
        tableName_input.setReadOnly(True)

             

        editlayout = QGridLayout()
        attributes_in = []
        types_in = []
        length_in = []
        null_in = []
        default_in = []
        primary_in = []
        editlayout.addWidget(QLabel("name"),0,0)
        editlayout.addWidget(QLabel("type"),0,1)
        editlayout.addWidget(QLabel("length"),0,2)
        editlayout.addWidget(QLabel("null"),0,3)
        editlayout.addWidget(QLabel("default"),0,4)
        editlayout.addWidget(QLabel("primary"),0,5)

        for i in range(attrNum):
            attributes_in.append(QLineEdit())
            types_in.append(QComboBox())
            types_withIndex = []
            for typeName in types:
                types_withIndex.append(str(i)+"."+typeName)
            types_in[i].addItems(types_withIndex)
            
            types_in[i].activated[str].connect(typeComboboxTriggerEvent)  
            l = QLineEdit()
            int_validator = QIntValidator()
            l.setValidator(int_validator)
            l.setPlaceholderText("只可輸入號碼")
            length_in.append(l)
            null_in.append(QCheckBox())
            default_in.append(QLineEdit())

            radiobutton = QRadioButton()
            if i == 0 and mode == "create":
                radiobutton.setChecked(True)
            if mode == "add":
                radiobutton.setCheckable(False)

            primary_in.append(radiobutton)
            editlayout.addWidget(attributes_in[i],i+1,0)
            editlayout.addWidget(types_in[i],i+1,1)
            editlayout.addWidget(length_in[i],i+1,2)
            editlayout.addWidget(null_in[i],i+1,3)
            editlayout.addWidget(default_in[i],i+1,4)
            editlayout.addWidget(primary_in[i],i+1,5)

        buttonlayout = QHBoxLayout()
        start_craft = QPushButton()
        if mode == "create":
            start_craft.setText("Create table")
        if mode == "add":
            start_craft.setText('Add column')
        clear_edit = QPushButton("Clear")
        start_craft.clicked.connect(crafting_preprocessing)
        clear_edit.clicked.connect(clearEditLayout)
        buttonlayout.addStretch(3)
        buttonlayout.addWidget(start_craft)
        buttonlayout.addStretch(1)
        buttonlayout.addWidget(clear_edit)
        buttonlayout.addStretch(3)
        
        main_layout.addLayout(editlayout)
        main_layout.addLayout(buttonlayout)
        main_layout.addStretch(5)

    def clearInput1():
        if mode == "create":
            tableName_input.setText("")
        attrNum_input.setText("")
   
    buttonlayout = QHBoxLayout()  


    Title = QLabel()
    craftButton = QPushButton("")
    craftButton.clicked.connect(editMain)
    if mode == "create":
        Title.setText("Create Table")
        craftButton.setText("Create")
        
    if mode == "add":
        Title.setText("Add columns")
        craftButton.setText("Add")
        

    Text_tableName  =QLabel("Table Name:")
    tableName_input = QLineEdit()
    reg = QRegExp("[A-Za-z_]+")
    str_validator = QRegExpValidator(reg)
    tableName_input.setValidator(str_validator)
    tableName_input.setPlaceholderText("只可輸入字母")
    if mode == "add":
        tableName_input.setText(file)
        tableName_input.setReadOnly(True)

    Text_attrNum = QLabel("How many attributes?")
    attrNum_input = QLineEdit()
    int_validator = QIntValidator()
    attrNum_input.setValidator(int_validator)
    attrNum_input.setPlaceholderText("只可輸入號碼")


    clearButton = QPushButton("Clear")
    clearButton.clicked.connect(clearInput1)
    buttonlayout.addStretch(3)
    buttonlayout.addWidget(craftButton)
    buttonlayout.addStretch(1)
    buttonlayout.addWidget(clearButton)
    buttonlayout.addStretch(3)

    main_layout.addWidget(Title)
    main_layout.addStretch(1)
    main_layout.addWidget(Text_tableName)
    main_layout.addStretch(0)
    main_layout.addWidget(tableName_input)
    main_layout.addWidget(QLabel("       "))
    main_layout.addWidget(Text_attrNum)
    main_layout.addWidget(attrNum_input)
    main_layout.addWidget(QLabel("       "))
    main_layout.addLayout(buttonlayout)

    main_layout.addStretch(2)
    #main_layout.setSpacing(0)

def addRowData_editRowData_element_tab(main_layout,mode,table,folder,file):
    data_csv = pd.read_csv(file_path+folder+"/"+file, encoding = "utf-8-sig")
    dataDetail_csv = pd.read_csv(type_path+folder+"/"+file , encoding= "utf-8-sig")
    attribute = dataDetail_csv["attribute"].values.tolist()
    print(attribute)
    data_type = dataDetail_csv["type"].values.tolist()
    print(data_type)

    data_len = dataDetail_csv["size"].values.tolist()
    primary_chk = dataDetail_csv["primary"].values.tolist()
    primary_key = ""

    def editMain():
        row_selected = []
        def clearEditLayout():
            for key in data_in.keys():
                for valueC in range(len(data_in[key])):
                    data_in[key][valueC].setText("")
        def crafting_preprocessing():
            try:
                attr_cnt = 0
                for attr in data_in.keys():
                    data_preprocessed[attr] = []
                    for count in range(len(data_in[attr])):
                        
                        if attr == primary_key:
                            if data_in[attr][count].text() in data_csv[attr].values.tolist():
                                if data_in[attr][count].text() != data_in[attr][count].placeholderText():
                                    duplicate_name_primary_error_msg = QMessageBox.information(mainWindow,'Primary Key Error',"Primary key value duplicate: " + data_in[attr][count].text(),QMessageBox.Ok)
                                    print("primary key duplicate")      ###
                                    return False
                            if str(data_in[attr][count].text()) == "":
                                empty_primary_error_msg = QMessageBox.information(mainWindow,'Primary Key Error',"null primary key not accepted",QMessageBox.Ok)
                                print("null primary key")      ###
                                return False
                        print(data_type[attr_cnt])
                        if data_type[attr_cnt] == "int" or data_type[attr_cnt] == "float" or data_type[attr_cnt] == "varchar"  :
                            if len(data_in[attr][count].text()) <1 or str(data_in[attr][count].text()) == "null":
                                if (dataDetail_csv["null"].values)[attr_cnt] == 1:
                                    data_preprocessed[attr].append("_null_")
                                    continue
                        if data_type[attr_cnt] == "date" or data_type[attr_cnt] == "time" or data_type[attr_cnt] == "datetime":
                            if len(data_in[attr][count].text().replace(":","").replace("-","").replace(" ","")) == 0:    #處理 none default of time,datetime,date
                                if data_type[attr_cnt]=="datetime":
                                    data_in[attr][count].setText("0000-00-00 00:00:00")
                                elif data_type[attr_cnt]=="date":
                                    data_in[attr][count].setText("0000-00-00")
                                elif data_type[attr_cnt]=="time":
                                    data_in[attr][count].setText("00:00:00")
                            else:
                                response = dateTime_check(data_in[attr][count].text(),data_type[attr_cnt])
                                if response != "No problem!":
                                    stackErrorDialog = QMessageBox.information(mainWindow,"Error message","default error, row: "+str(i)+" "+response, QMessageBox.Ok)
                                    return False
                        data_preprocessed[attr].append(data_in[attr][count].text())
                    attr_cnt +=1
                add_and_edit_rowData(data_preprocessed, mode,folder,file,row_selected)

                refresh_browse_tab_tb(folder=folder, file=file)
                tabs.setCurrentIndex(0)
                relayout(Craft_tab,QVBoxLayout())
            except Exception as error:
                print("An error occurred:", error)
                return False
            

        editlayout = QGridLayout()
        data_in = {}
        data_preprocessed= {}
        
        editlayout.addWidget(QLabel("Row"),0,0)
        count = 0
        for attr in attribute:
            data_in[attr]=[]
            data_preprocessed[attr]= []
            attr_head =QLabel(attr+" ("+data_type[count]+")")
            if int(primary_chk[count])==1:
                primary_key = attr
                attr_head.setText(attr+" ("+data_type[count]+")"+" [primary key]")
            editlayout.addWidget(attr_head,0,count+1)
            count +=1


        if mode == "add":
            currentRowCount = table.rowCount()
            if len(addRow_input.text())<1:
                empty_row_input_error_msg = QMessageBox.information(mainWindow,'Row input Error',"Please insert row to add: ",QMessageBox.Ok)
                print("null primary key")      ###
                return False
            row_selected = ""
            addRow_input.setReadOnly(True)
            addRowButton.setEnabled(False)
            addRowCount = int(addRow_input.text())
            
            for i in range(addRowCount):
                editlayout.addWidget(QLabel(str(currentRowCount + i+1)),i+1,0)
                for c in range(len(attribute)):
                    print(c)
                    attr_in = QLineEdit()
                    if data_type[c] == "int":
                        attr_in.setValidator(QIntValidator())

                    elif data_type[c] == "float":
                        attr_in.setValidator(QDoubleValidator())
                    
                    elif data_type[c] == "varchar":
                        print("varchar no 限制")

                    elif data_type[c] == "date":
                        attr_in.setInputMask("0000-00-00")
                    
                    elif data_type[c] == "datetime":
                        attr_in.setInputMask("0000-00-00 00:00:00")
                    
                    elif data_type[c] == "time":
                        attr_in.setInputMask("00:00:00")
                    
                    data_in[attribute[c]].append(attr_in)
                    editlayout.addWidget(data_in[attribute[c]][i],i+1,c+1)
        
        if mode == "edit":
            row_selected = rowSelectcheck(table)

            count = 0
            for i in row_selected:
                editlayout.addWidget(QLabel(str(i+1)),count+1,0)
                for c in range(len(attribute)):
                    attr_in = QLineEdit()

                    pre_data = table.item(i,c+1).text()
                    if attribute[c] == primary_key:
                        attr_in.setPlaceholderText(pre_data)
                    
                    if data_type[c] == "int":
                        attr_in.setValidator(QIntValidator())
                        #pre_data = int(pre_data)

                    elif data_type[c] == "float":
                        attr_in.setValidator(QDoubleValidator())

                    elif data_type[c] == "varchar":
                        print("varchar no 限制")

                    elif data_type[c] == "date":
                        attr_in.setInputMask("0000-00-00")
                        #pre_data = pre_data.replace('-','')
                        #pre_data = int(pre_data)
                    
                    elif data_type[c] == "datetime":
                        attr_in.setInputMask("0000-00-00 00:00:00")
                        #pre_data = pre_data.replace('-','').replace(' ','').replace(':','')
                        #pre_data = int(pre_data)
                    
                    elif data_type[c] == "time":
                        attr_in.setInputMask("00:00:00")
                        #pre_data = pre_data.replace(':')
                        #pre_data = int(pre_data)
                    
                    attr_in.setText(pre_data)
                    data_in[attribute[c]].append(attr_in)
                    editlayout.addWidget(data_in[attribute[c]][count],count+1,c+1)
                count +=1


        buttonlayout = QHBoxLayout()
        start_craft = QPushButton()
        if mode == "add":
            start_craft.setText("add Row Data")
        if mode == "edit":
            start_craft.setText('edit Row Data')
        clear_edit = QPushButton("Clear")
        start_craft.clicked.connect(crafting_preprocessing)
        clear_edit.clicked.connect(clearEditLayout)
        buttonlayout.addStretch(3)
        buttonlayout.addWidget(start_craft)
        buttonlayout.addStretch(1)
        buttonlayout.addWidget(clear_edit)
        buttonlayout.addStretch(3)

        main_layout.addLayout(editlayout)
        main_layout.addLayout(buttonlayout)
        main_layout.addStretch(5)
            




            

    title = QLabel("")
    main_layout.addWidget(title)
    main_layout.addStretch(1)
    if mode == "add":
        title.setText("Add data")
        addRow_text = QLabel("Number of Row to add: ")

        addRow_input = QLineEdit()
        addRow_input.setValidator(QIntValidator())
        addRow_input.setPlaceholderText("只可輸入號碼")

        addRowButton = QPushButton("Add Row Data")
        addRowButton.clicked.connect(editMain)
        main_layout.addStretch(1)
        main_layout.addWidget(addRow_text)      
        main_layout.addWidget(addRow_input)
        main_layout.addWidget(addRowButton)
        main_layout.addStretch(3)
        

    elif mode =="edit":
        title.setText("Edit data")
        editMain()

def import_csv(imported_csv_path,folder,file):
    def time_chk(time):
        try:
            hour= time.split(":")[0]
            min = time.split(":")[1]
            second = time.split(":")[2]
            if not (hour.isnumeric() and len(hour)<3):
                return False
            if not (min.isnumeric() and len(min)<3):
                return False
            if not (second.isnumeric() and len(second)<3):
                return False
            return True
        except:
            return False
    def date_chk(date):
        try:
            year = date.split("-")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]
            if not (year.isnumeric() and len(year)<=4):
                return False
            if not (month.isnumeric() and len(month)<=2):
                return False
            if not (day.isnumeric() and len(day)<=2):
                return False
            return True
        except:
            return False

    actual_table = pd.read_csv(file_path+folder+"/"+file,encoding = "utf-8-sig")
    types_table = pd.read_csv(type_path+folder+"/"+file,encoding = "utf-8-sig")

    headers = types_table["attribute"].values.tolist()
    types = types_table["type"].values.tolist()
    isNull = types_table["null"].values.tolist()
    primary_chk = types_table.loc[types_table["primary"] == 1].values
    primary_chk = primary_chk[0][0]
    print(headers)
    print(types)
    print(primary_chk)
    print(imported_csv_path)
    try:
        imported_csv = pd.read_csv(str(imported_csv_path),encoding = "utf-8-sig", names = headers)
        imported_csv = pd.DataFrame(imported_csv)
        print(imported_csv)
        #check 
        type_index = 0
        for head in headers:
            toAddItems = imported_csv[head].values.tolist()
            print(toAddItems)
            itemRow = 0
            falseTrigger = 0
            for item in toAddItems:
                if head ==primary_chk:
                    if item in actual_table[primary_chk].values.tolist():
                        ErrorImportMsg = QMessageBox.information(mainWindow,"Error import","Duplicate primary key value: "+ item + " in row "+str(itemRow))
                        return False
                    if str(item) == "nan":
                        ErrorImportMsg = QMessageBox.information(mainWindow,"Error import","NaN primary key is not allowed in row "+str(itemRow))
                        return False
                if types[type_index] == "int":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = ""
                        else:
                            imported_csv[head][itemRow] = "_null_"
                    elif not str(item).isdigit():
                        print(item+" not integer in row "+itemRow)
                        falseTrigger = 1

                elif types[type_index] == "float":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = ""
                        else:
                            imported_csv[head][itemRow] = "_null_"
                    elif not str(item).replace(".","").isdigit():
                        print(item+" not float in row "+itemRow)
                        falseTrigger = 1

                elif types[type_index] == "varchar":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = ""
                        else:
                            imported_csv[head][itemRow] = "_null_"
                    print("varchar will be alright")
                

                elif types[type_index] == "time":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = "00:00:00"
                        else:
                            imported_csv[head][itemRow] = "00:00:00"
                    elif not time_chk(item):
                        print(item+" not time in row "+itemRow)
                        falseTrigger = 1

                elif types[type_index] == "date":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = "0000-00-00"
                        else:
                            imported_csv[head][itemRow] = "0000-00-00"
                    elif not date_chk(item):
                        print(item+" not date in row "+itemRow)
                        falseTrigger = 1

                elif types[type_index] == "datetime":
                    if str(item) == "nan":
                        if isNull(type_index) == 0:
                            imported_csv[head][itemRow] = "0000-00-00 00:00:00"
                        else:
                            imported_csv[head][itemRow] = "0000-00-00 00:00:00"
                    else:
                        try:
                            date = item.split(" ")[0]
                            time = item.split(" ")[1]
                            if not (date_chk(date) and time_chk(time)):
                                print(item+" not datetime in row "+str(itemRow))
                                falseTrigger = 1
                        except:
                            print(item+" not datetime in row "+str(itemRow))
                            falseTrigger = 1
                if falseTrigger == 1:
                    ErrorImportMsg = QMessageBox.information(mainWindow,"Error import",item+" not "+types[type_index]+" in row "+str(itemRow))
                    return False
                itemRow +=1
            type_index +=1
                
        for rowDataIndex in imported_csv.index:
            print(imported_csv.loc[rowDataIndex].tolist())
            actual_table.loc[len(actual_table.index)] = imported_csv.loc[rowDataIndex].tolist()
            
        actual_table.to_csv(file_path+folder+"/"+file,encoding = "utf-8-sig", index = False)
        relayout(Craft_tab,QVBoxLayout())

        refresh_browse_tab_tb(folder,file)

    except Exception as error:
        add_attribute_error_msg = QMessageBox.information(mainWindow,'Import Error',"Unknown data error ",QMessageBox.Ok)
        print("An error occurred:", error)
        return False    


def create_table(attributes,types,length,null,default,primary, new_table , database=""):

    if database == "":
        database = current_lockon_database.text()
    print(database)
    print(new_table,attributes,types,length,null,default,primary)

    type_csv = {"attribute":attributes,"type":types,"size":length,"null":null,"default":default,"primary":primary}
    type_csv = pd.DataFrame(type_csv)
    type_csv.to_csv(type_path+database+"/"+new_table+".csv", encoding="utf-8-sig",index=False)
    data_dict = {}
    for i in range(len(attributes)):
        data_dict[attributes[i]]=[]
    data_csv = pd.DataFrame(data_dict)
    data_csv.to_csv(file_path+database+"/"+new_table+".csv",encoding="utf-8-sig",index=False)

def add_colAttribute(attributes,types,length,null,default,primary,table,database):
    type_csv = pd.read_csv(type_path+database+"/"+table, encoding = 'utf-8-sig')
    for i in range(len(attributes)):
        type_csv.loc[len(type_csv.index)] = [attributes[i],types[i],length[i],null[i],default[i],primary[i]]
    type_csv.to_csv(type_path+database + "/"+table,encoding="utf-8-sig",index = False)

    data_csv = pd.read_csv(file_path+database+"/"+table, encoding="utf-8-sig")
    for i in range(len(attributes)):
        default_lst=[]
        for num  in data_csv.index:
            default_lst.append(default[i])
        data_csv[str(attributes[i])]=default_lst
    data_csv.to_csv(file_path+database+"/"+table, encoding="utf-8-sig",index = False)
    
def add_and_edit_rowData(data_preprocessed, mode,folder,file,row_selected=""):
    data_csv = pd.read_csv(file_path+folder+"/"+file,encoding = "utf-8-sig")
    header = data_csv.columns
    currentRowCount = len(data_csv.index)
    if mode == "add":
        row_selected=[]
        for i in range(len(data_preprocessed[header[0]])):
            row_selected.append(len(data_csv.index)+i)
    print(row_selected)
    print(data_preprocessed)
    for i in range(len(row_selected)):
        data_set = []
        for head in  header:
            data_set.append(data_preprocessed[head][i])
        data_csv.loc[row_selected[i]] = data_set

    print(data_csv)
    data_csv.to_csv(file_path+folder+"/"+file,encoding = "utf-8-sig",index =False)


def drop(table,mode,folder="",file="",row_selected="None"):

    if row_selected == "None":
        rowcount = table.rowCount()   
        row_selected = rowSelectcheck(table)
    print(row_selected)         #ascending order
    if mode == 0:       #drop table
        for i in row_selected:
            filename = table.item(i,1).text()
            os.remove(file_path+folder+"/"+filename)
            os.remove(type_path+folder+"/"+filename)

    if mode == 1:      #drop col
        type_csv = pd.read_csv(type_path+folder+"/"+file,encoding='utf-8-sig')
        data_csv = pd.read_csv(file_path+folder+"/"+file,encoding='utf-8-sig')
        attr_to_del = []
        for i in row_selected:
            attr_to_del.append(str(table.item(i,1).text()))
        #print(attr_to_del)
        index = []
        try:
            for attr in attr_to_del:         
                index.append(int((type_csv[type_csv["attribute"]==attr].index)[0]))
                #print(index)
                data_csv = data_csv.drop(columns=attr)
                
            type_csv = type_csv.drop(index=index)
            type_csv.to_csv(type_path+folder+"/"+file,encoding='utf-8-sig',index = False)
            data_csv.to_csv(file_path+folder+"/"+file,encoding = 'utf-8-sig',index =False)
        except:
            print("attribute delete fail: ",attr)

    if mode ==2 :       #drop row
        data_csv = pd.read_csv(file_path+folder+"/"+file , encoding = "utf-8-sig")
        primaryKeyIndex = 0
        #print(data_csv)
        while str(table.horizontalHeaderItem(primaryKeyIndex).text()).find("primary key") == -1:
            primaryKeyIndex +=1
        print(primaryKeyIndex)
        primaryKey = str(table.horizontalHeaderItem(primaryKeyIndex).text()).split(" ")[0]
        for i in row_selected:
            primary_to_delete=str(table.item(int(i),primaryKeyIndex).text())
            print(primary_to_delete)
            if(str(data_csv.iloc[i][primaryKey]) != primary_to_delete):
                print("read error")
        data_csv = data_csv.drop(index = row_selected)
        data_csv.to_csv(file_path+folder+"/"+file , encoding = "utf-8-sig",index = False)
    if mode == "deleteSQL":
       data_csv = pd.read_csv(file_path+folder+"/"+file , encoding = "utf-8-sig")
       data_csv = data_csv.drop(index = row_selected)
       data_csv.to_csv(file_path+folder+"/"+file , encoding = "utf-8-sig",index = False)

    
    
    



def open_both():
    relayout(Browse_tab,QVBoxLayout())
    relayout(Structure_tab,QVBoxLayout())
    relayout(Craft_tab,QVBoxLayout())
    relayout(Import_tab,QVBoxLayout())
    relayout(Sql_tab,QVBoxLayout())
    for currentItem in leftside_table.selectedItems():
        if str(currentItem.column()) == "0":                         #database
            refresh_structure_tab_db(currentItem.text())
            refresh_sql_tab()
            current_lockon_database.setText(str(currentItem.text()))
            current_lockon_table.setText("")
            tabs.setCurrentIndex(1)
            
        else:                                                        #file
            file = currentItem.text()
            folder = leftside_table.item(currentItem.row(),0).text()
            current_lockon_database.setText(folder)
            current_lockon_table.setText(file)
            file = currentItem.text()+".csv"
            print("file: ",file, ", folder: ",folder)
            refresh_browse_tab_tb(folder,file)
            refresh_structure_tab_tb(folder,file)
            refresh_import_tab(folder,file)
            refresh_sql_tab()
            tabs.setCurrentIndex(0)
      

def searchDialog(table,mode="searchDB_TB"):
    sdialog = QInputDialog.getText(mainWindow,"search","search: ",QLineEdit.Normal,"")
    if sdialog[1] and str(sdialog[0])!="":
        print("Pressed OK: Text is "+ str(sdialog[0]))
        searchlll(str(sdialog[0]),table,mode)
        return
    else:
        return
def searchlll(target,table,mode):            #mode = "searchDB_TB" -> search db and tb   mode= "searchInTable" -> search row     
    table_pre = QTableWidget()
    print(target)
    #copy table
    table_pre.setRowCount(table.rowCount())
    table_pre.setColumnCount(table.columnCount())
    for col in range(table.columnCount()):
        table_pre.setHorizontalHeaderItem(col,QTableWidgetItem(table.horizontalHeaderItem(col).text()))
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = QTableWidgetItem(str(table.item(row,col).text()))
            table_pre.setItem(row,col,item)
            
    table.clearContents()
    table.setRowCount(0)
    current_row = 0
    for row in range(table_pre.rowCount()):
        for col in range(table_pre.columnCount()):
            #print(str(table_pre.item(row,col).text()))
            if target == str(table_pre.item(row,col).text()):
                table.setRowCount(current_row+1)
                for current_col in range(table_pre.columnCount()):
                    item = QTableWidgetItem(str(table_pre.item(row,current_col).text()))
                    #print(table.horizontalHeaderItem(current_col).text())
                    if mode == "searchDB_TB":
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

                        if str(item.text()) == "":
                            item.setFlags(QtCore.Qt.NoItemFlags)
                            
                    else:  #mode == "searchInTable"
                        if table.horizontalHeaderItem(current_col).text() == "checkbox":
                            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                            item.setCheckState(QtCore.Qt.Unchecked)
                        else:
                            item.setFlags(QtCore.Qt.NoItemFlags)

                    table.setItem(current_row,current_col,item)
                current_row+=1    
                break
    if mode == "searchDB_TB":
        table.doubleClicked.connect(open_both)
    



app = QApplication(sys.argv)
mainWindow = QMainWindow()
#mainWindow.resize(400,500)
mainWindow.setWindowTitle("DBMS")
widget = QWidget()

vertical_layout_main = QVBoxLayout()
mainmenu = mainWindow.menuBar()
createDB = QAction("Create DataBase")
createDB.triggered.connect(lambda:refresh_craft_tab(0))
dropDB = QAction("Drop DataBase")

dropDB.triggered.connect(lambda:refresh_craft_tab(-1))
findDB = QAction("Find Database")
findDB.triggered.connect(lambda:searchDialog(leftside_table,"searchDB_TB"))
findTB = QAction("Find Table")
findTB.triggered.connect(lambda:searchDialog(leftside_table,"searchDB_TB"))
refreshLeftsideBarBtn = QAction("Refresh")
refreshLeftsideBarBtn.triggered.connect(refresh_leftside_bar)
mainmenu.addAction(createDB)
mainmenu.addAction(dropDB)
mainmenu.addAction(findDB)
mainmenu.addAction(findTB)
mainmenu.addAction(refreshLeftsideBarBtn)

horizontal_layout1 = QHBoxLayout()
#leftside_bar = QWidget()
vertical_layout1 = QVBoxLayout()
leftside_table = QTableWidget()
refresh_leftside_bar()


tabs = QTabWidget()
tabs.resize(300,100)
Browse_tab = QWidget()
Structure_tab = QWidget()
Craft_tab = QWidget()
Import_tab = QWidget()
Sql_tab = QWidget()
#Drop_tab = QWidget()

tabs.addTab(Browse_tab,"Browse")
tabs.addTab(Structure_tab,"Structure")
tabs.addTab(Craft_tab,"Craft")
tabs.addTab(Import_tab,"Import")
tabs.addTab(Sql_tab,"SQL")


current_lockon_database = QLabel()
current_lockon_table = QLabel()
footer = QHBoxLayout()
footer.addWidget(QLabel("Current database: "))
footer.addWidget(current_lockon_database)
footer.addWidget(QLabel("Current table: "))
footer.addWidget(current_lockon_table)



#horizontal_layout1.addWidget(leftside_table)
vertical_layout1.addWidget(leftside_table)
horizontal_layout1.addLayout(vertical_layout1)
horizontal_layout1.addWidget(tabs)
vertical_layout_main.addLayout(horizontal_layout1)
vertical_layout_main.addLayout(footer)
widget.setLayout(vertical_layout_main)
mainWindow.setCentralWidget(widget)
mainWindow.show()
mainWindow.showMaximized()

sys.exit(app.exec_())





#UNUSED FUNC
"""
def open_database(fol):
    folder = fol.text()
    print(folder)

def open_table(tb):
    file = str(tb.text())
    db = pd.read_csv(file_path+folder+"/"+file, encoding='utf-8-sig')
    print(db)
    """