import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--arg" , type=int ,help ='Mode to be run - 1 for interactive and 2 for static',required=True)
parser.add_argument("--config" , type=str ,help ='Configuration Json to be provided',required=True)
parser.add_argument("--rule",type=str,help='Choose the rule to be invoked',required=False)

args = parser.parse_args()

import numpy as np
import json
import xlsxwriter
import pandas as pd
from pprint import pprint
print args.config
with open(args.config) as f:
    
    data = json.load(f)


df=pd.read_csv(data['Source_File'])
df_source = df.copy
df_Di= pd.read_csv(data['Dictionary'])
df_merged = pd.DataFrame({})

import datetime as datetime
from datetime import datetime
now=datetime.now()
current_date=now.strftime("%m/%d/%Y")

current_date = datetime.strptime(current_date, '%m/%d/%Y')


#Pre-Processing as per configuration set

def rename_columns(df,df_Di):

    rename_Dictionary_Column = None
    rename_Source_Column = None

    if data['Column_rename'] is not None :
        if data['Column_rename']['Source_File_Column_input'] is not None:

            print data['Column_rename']
            print data['Column_rename']['Source_File_Column_input']
            rename_Source_Column = dict(list(zip(data['Column_rename']['Source_File_Column_input'],data['Column_rename']['Source_File_Column_output'])))
        if data['Column_rename']['Dictionary_Column_input'] is not None:
            print ('Is not None')
            rename_Dictionary_Column = dict(list(zip(data['Column_rename']['Dictionary_Column_input'],data['Column_rename']['Dictionary_Column_output'])))

    if rename_Dictionary_Column is not None :
        for i in iter(rename_Dictionary_Column):
            print i , rename_Dictionary_Column[i]
            df_Di=df_Di.rename(columns = {i:rename_Dictionary_Column[i]})
            print True
    if rename_Source_Column is not None :
        for i in iter(rename_Source_Column):
            print i , rename_Source_Column[i]
            df=df.rename(columns = {i:rename_Source_Column[i]})
            print True
    return df,df_Di


if data['Column_rename'] is not None :
    df,df_Di = rename_columns(df,df_Di)

print ('Check for renamed Columns')
print df
print df_Di



def rule():

    rule=raw_input('Please enter the rule to be configured (Find_and_Replace/Select_mapped_Coloumns) : ')

    if rule == 'Find_and_Replace':
        
        num_cells_to_change = raw_input('Enter the number of cell whose values need to be changed')
        Source_Cell = []
        Dictionary_Cell = []
        for k in range(int(num_cells_to_change)):
            val = raw_input('Enter the cell value to be changed as in the source file')
            Source_Cell.append(val)
        for g in range(int(num_cells_to_change)):
            val_dict= raw_input('Enter the cell value to be changed as per the Dictionary')
            Dictionary_Cell.append(val_dict)

        Source_Column = raw_input('Enter the Source Column name of interest')
        #Source_Column_Value = raw_input('Enter the Source Column value of interest')
        Dictionary_Column = raw_input('Enter the Dictionary Column name of interest')
        #Dictionary_Column_Value = raw_input('Enter the Dictionary Column value of interest')
        
        data[rule]['Content']['First Column Name']=Source_Column
        data[rule]['Content']['First Column Value']=Source_Cell
        data[rule]['Content']['Second Column Name'] = Dictionary_Column
        data[rule]['Content']['Second Column Value'] = Dictionary_Cell
        

    
        print ('Rule is',rule)
        Source_Column_loaded= data[rule]['Content']['First Column Name']
        print Source_Column_loaded
        Source_Column_V= data[rule]['Content']['First Column Value']
        print Source_Column_V
        Dict_Column_loaded= data[rule]['Content']['Second Column Name'] 
        print Dict_Column_loaded
        Dict_Column_Value_loaded= data[rule]['Content']['Second Column Value'] 
        print Dict_Column_Value_loaded
        
        
    
    
    if rule == 'Select_mapped_Coloumns':
        
        

    
    


        Source_mapped_column = []
        Dictionary_mapped_column=[]
        print rule
        Num_Columns_source = raw_input('Enter number of columns to be entered from the source file : ')
        Num_Columns_dictionary = raw_input('Enter number of columns to be entered from the Dictionary : ')

        for i in range(int(Num_Columns_source)):

            Col_Name= raw_input('Enter the column to be mapped from source : ')
            Source_mapped_column.append(Col_Name)
        print Source_mapped_column
        for i in range(int(Num_Columns_dictionary)):
            Col_Name_= raw_input('Enter the column to be mapped from the dictionary : ')
            Dictionary_mapped_column.append(Col_Name_)
        print Dictionary_mapped_column
        data[rule]['Output Column Selection']['First File Columns'] = Source_mapped_column
        data[rule]['Output Column Selection']['Second File Columns'] = Dictionary_mapped_column
        l_dict=[]
        l_source=[]

        Count_mapping= raw_input('Enter the number of columns to be mapped on')
        print ('Enter the columns to be mapped from the Dictionary ')
        for i in range(int(Count_mapping)):
            a = raw_input('Enter the Column')
            l_dict.append(a)
            data['Select_mapped_Coloumns']['Dictionary_Column_Map']=l_dict
        print ('Dictionary Columns to be mapped on are entered')

        print ('Enter the columns to be mapped at Source end ')
        for i in range(int(Count_mapping)):
            a = raw_input('Enter the Column')
            l_source.append(a)
            data['Select_mapped_Coloumns']['Source_Column_Mapped']=l_source
        print ('Source Columns to be mapped on are entered')
        
def rule2(df):
    dict_ = {}

    print ('Rule 2 is invoked')
    l1=data['Find_and_Replace']['Content']['First Column Value']
    l2=data['Find_and_Replace']['Content']['Second Column Value']
    dict_ = dict(zip(l1,l2))
    for j in dict_.keys():
        df.loc[df[data['Find_and_Replace']['Content']['First Column Name']]==j,data['Find_and_Replace']['Content']['First Column Name']]=dict_[j]
    return df


def rule3(df):
    if data['Select_mapped_Coloumns']['Output Column Selection']['First File Columns'] is not None and data['Select_mapped_Coloumns']['Output Column Selection']['Second File Columns'] is not None :
        df_merged = pd.merge(df[data['Select_mapped_Coloumns']['Output Column Selection']['First File Columns']], df_Di[data['Select_mapped_Coloumns']['Output Column Selection']['Second File Columns']], how='left', left_on = data['Select_mapped_Coloumns']['Source_Column_Mapped'] , right_on= data['Select_mapped_Coloumns']['Dictionary_Column_Map'])
        print ('Rule 3 is invoked')
        return df_merged
    else :
        df_merged = pd.merge(df,df_Di,how='left', left_on=data['Select_mapped_Coloumns']['Source_Column_Mapped'],right_on=data['Select_mapped_Coloumns']['Dictionary_Column_Map'])
        l = list(df.columns)
        g = ['End of Sale','End of Support Life','End of Extended Support Life']
        col_pick = l+g
        df_merged_col_selected = df_merged[col_pick]
	print ('Default case in progress')
        return df_merged_col_selected



    
def GetQuarter(mon):
       
       

       if (mon >= 1 and mon <= 3):
           
           return 1
       elif (mon >= 4 and mon <= 6):
           return 2
       elif (mon >= 7 and mon <= 9):
           return 3
       else: 
           return 4


def date_conversion(df1,column):
    df=df1
    end_of_support_life_dates = df[column]
    #end_of_sale=df['EOS']
    
    for counter,eosl_date in enumerate(end_of_support_life_dates):
        if not (isinstance(eosl_date,float)):
            
            print eosl_date
            
            
            
            expiry_date = eosl_date

            #print type(i)

            try:
                #print i
                expiry_date = datetime.strptime(eosl_date, "%m-%d-%y").strftime("%m/%d/%Y")
                print expiry_date

            except ValueError:

                try:
                    expiry_date = datetime.strptime(eosl_date, "%d-%m-%Y").strftime("%m/%d/%Y")
                    print expiry_date
                except ValueError:
                    print 'Came to except'
                    try:
                        expiry_date = datetime.strptime(eosl_date, "%m/%d/%y %H:%M").strftime("%m/%d/%Y")
                        print expiry_date
                    except:
                        try:
                            print ('Came to last except')
                            expiry_date = datetime.strptime(eosl_date, "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y")
                            print expiry_date

                        except:
                            
                            continue

            df.loc[df[column] == eosl_date, column] = expiry_date
        

    return df



def Eosl(df,column):

    df=df
    
    a=df[column]


    for i in a:
        #print type(i)
        if i != '' :
            print ('i is',i)
            try:
                
                expiry_date = datetime.strptime(i, '%m/%d/%Y')
            except ValueError:
                print 'Value Error Occurred'
            
                try:
                    print 'Came inside 2nd try'

                    expiry_date = datetime.strptime(i, '%d/%m/%Y')
                except ValueError:
                    print 'Value Error Occurred'
            
            
            
                
                



            s=i.split('/')

            month=int(s[0])
            Year=s[2]
            print ('Year is',Year)
            print ('month is',month)

            Quarter = GetQuarter(int(month))
            print i,current_date,month,Year,Quarter
            Expiring_quarter= Year + " "+"Q"+str(Quarter)
            delta = expiry_date - current_date
            delta_days=delta.days

            delta_quarters= int(round(delta_days/91.25))



            #print ('Expiring Quarter',Expiring_quarter)
            print ('Expiring Year',Year)

            print ('Delta Quarters',delta_quarters,delta_days)
            if delta_days > 0:
                Quarter_diff= "Expiring after" + " " + str(delta_quarters) + " " + "Quarters"
            else :
                Quarter_diff = "Expired"
            print Quarter_diff

            df.loc[df[column]==i,'Status'] =  Quarter_diff
            df.loc[df[column]==i,'Expiring Year'] = Year
            df.loc[df[column]==i,'Expiring Quarter'] = Expiring_quarter

        else:
            df.loc[df[column]==i,'Status'] =  'NA'
            df.loc[df[column]==i,'Expiring Year'] = 'NA'
            df.loc[df[column]==i,'Expiring Quarter'] = 'NA'
            
    return df


if not args.rule:


    mode = args.arg

    mode = int(mode)

    if mode == 1:

        Required = raw_input('Are there any changes to be made ? Y/N')
        while Required == 'Y':
            rule()
            Required = raw_input('Are there any changes to be made ? Y/N')
        print ('The configuration file has the needed inputs')
    elif mode == 2:

        print ('Generating output file')
        df_merged_ = rule2(df)
        df_output = rule3(df_merged_)
        print ('Output Dataset is  df_output')
        print df_output
	df_output.to_excel('Output_Details.xlsx',index=False)
else:
    if args.rule == 'Find_and_Replace':
        df_output = rule2(df)
        print df_output
	df_output.to_excel('Generated_Output.xlsx')
    elif args.rule == 'Select_mapped_Coloumns':
        df_output = rule3(df)
        print df_output
	df_output.to_excel('Generated_Output.xlsx')



df_out=df_output

if data['Date-Time-Columns'] is not None:
    for i in data['Date-Time-Columns']:
        print i
    	df_out = date_conversion(df_out,i)


df_preout = df_out.replace(np.nan, '', regex=True)

if data['Expiry_Reference_Column'] is not None:
    print data['Expiry_Reference_Column']


    Df = Eosl(df_preout,data['Expiry_Reference_Column'])


Df.to_excel('Expiry_Output_final.xlsx',index=False)










