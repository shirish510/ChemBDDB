#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import os
import django
import subprocess
import sys
# sys.path.insert(0, parentdir)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from chembddb.models import MolGraph, Publication, MolProp, Data, Method
# df1=pd.read_csv('pol_RI_val1.csv', index_col=0)
# df = df1.replace(np.nan,'', regex = True)
# smiles = df['Mol_Smiles'].tolist()

# print("Installing MySQL")

# To install .msi file use the below command
# os.system('msiexec /i ./chembddb/mysql-installer-community-5.7.17.0.msi')
#Input Project name from user 
# proj_name = raw_input('Project name:')

#Input Application name from user
app_name = raw_input('App name:')

#Input property from user
num = 0
num = int(raw_input('Number of properties for chemical compounds:'))
print("Specify the property names:")
list_name = []
for i in range(num):
    list_name.append(raw_input(('Property %d :') % (i+1)))
    i+=1

#Input units from user
print("Specify the units for each property:")
unit_list = []
for lists in list_name:
    unit_list.append(raw_input(("Unit for property - %s :") % lists))

# smiles = df['SMILES'].tolist()
# # This reads each property into individual dataframes.
# for val in list_name:
#     val = df[val].tolist()

#For adding the property names to the database.
for j in range(num):
    mp=MolProp.objects.all()
    if len(mp) ==0:
        pob = MolProp.objects.all()
        prop_name = map(lambda x: x.prop, pob)
        if len(prop_name)==0:
            if(unit_list[j+1] != ''):
                p = MolProp(prop=list_name[j+1], unit=unit_list[j+1])  #Entering the property name and its corresponding unit
                p.save()                                               #Saving the property name and unit to the database.

            else:
                p = MolProp(prop=list_name[j+1])  #Entering the property name with no unit
                p.save() #Saving the property name with no unit

#Input the MYSQL username and password
username= raw_input('MySQL Username:')
password= raw_input('MySQL Password:')
