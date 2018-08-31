import pandas as pd
import numpy as np
import os
# import pybel
# import openbabel
import django
import sys
# parentdir = os.path.dirname("/projects/academic/hachmann/shirish/python/mysite/chembddb")
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
# sys.path.insert(0,parentdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from chembddb.models import MolGraph, Publication, MolProp, Data, Method
# from chembddb.input import
'''To read the uploaded chemical dataset from the .csv file and analyze it. The dataset is parsed and inserted 
into the MySQL database named 'chemdb_pol'. This is done with the help of pandas whose function  
read_csv() is used to parse the data in the .csv file by splitting it into dataframes. If dataframe
is not a number (NaN) then its replace by '' using dataframe.replace() from Numpy.'''

filename = sys.argv[1]
print filename
df1=pd.read_csv('./chembddb/media/'+str(filename), index_col=0)
df = df1.replace(np.nan,'', regex=True)


# df2 = pd.read_csv('pol_RI_val.csv')
# df3 = list(df2.columns.values)

# for i in range(len(df3)):
# 	print df3[i]+''


pol=df['Polarizability'].tolist()
smiles=df['Mol_Smiles'].tolist()
# En=df['Energy'].tolist()
refind=df['RI'].tolist()
refind2=df['RI_LL'].tolist()
den = df['Density'].tolist()

#For Testing if uploaded file is parsed properly
# print pol[0]
# print pol[1]
# print den[0]
# print den[1]

n1=[]
n=[]
#entering molgraph details
mg = MolGraph.objects.all()
mg_id = map(lambda x: x.id, mg)
#if len(mg) == 0:
for i in range(len(df)):
        try:
                n.append(MolGraph(compound_str='',SMILES_str=smiles[i]))
        except ValueError:
                n.append(MolGraph(compound_str='',SMILES_str=''))
MolGraph.objects.bulk_create(n,batch_size=1000)



#entering property names
#To make sure that property names arent repeated in property table
mp = MolProp.objects.all()
mp_id = map(lambda x: x.id, mp)
if len(mp) == 0:
	pob = MolProp.objects.all() 
	prop_name = map(lambda x: x.prop, pob)
	if len(prop_name)==0:
		p=MolProp(prop="Polarizability",unit="Bohr")
		p.save()
		p=MolProp(prop="Density",unit="kg/m3")
		p.save()
		p=MolProp(prop="RI")
		p.save()
		p=MolProp(prop="RI(2)")
		p.save()


#entering method names
me = Method.objects.all()
me_id = map(lambda x: x.id, me)
if len(me) == 0:
	m = Method(method="MD")
	m.save()
	m = Method(method="DFT")
	m.save()
	m = Method(method="LL")
	m.save()
	m= Method(method="VDW")
	m.save()


#entering data
d = Data.objects.all()
# dl = MolGraph.objects.latest('id')
#data_value = map(lambda y: y.id, d)
#print len(d)


if len(d) == 0:
	# For Polarizability using DFT
	x = 0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[1], property_id=mp_id[0], value=float(pol[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[1], property_id=mp_id[0], value=0))

	# For density using M.D.
	x = 0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[0], property_id=mp_id[1], value=float(den[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[0], property_id=mp_id[1], value=0))

	# For refractive index calculated using Lorentz Lorentz Equation where Kp is constant
	x = 0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[2], property_id=mp_id[2], value=float(refind[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[2], property_id=mp_id[2], value=0))
	# Data.objects.bulk_create(n1,batch_size=1000)

	# For refractive index using Lorentz Lorentz equation where Kp=0.75
	x = 0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[2], property_id=mp_id[3], value=float(refind2[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=x+1, met_id=me_id[2], property_id=mp_id[3], value=0))

	#Data.objects.bulk_create(n1, batch_size=100000)  # Adds all the file data into the database of 'chemdb_den'

else:
	dl = Data.objects.latest('id')
	dlast = dl.mol_graph_id
	# dl_id = map(lambda x: x.id, dl)
	#print dl.mol_graph_id
	print len(df)
	print dl.mol_graph_id
	x=0

	print MolGraph.objects.filter(id = dl.mol_graph_id+x+1)
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id= (dl.mol_graph_id+x+1), met_id=me_id[1],property_id=mp_id[0],value=float(pol[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[1],property_id=mp_id[0],value=0))

	# For density using M.D.
	x=0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[0],property_id=mp_id[1],value=float(den[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[0],property_id=mp_id[1],value=0))

	# For refractive index calculated using M.D.
	x=0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[0],property_id=mp_id[2],value=float(refind[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[0],property_id=mp_id[2],value=0))
	# Data.objects.bulk_create(n1,batch_size=1000)

	# For refractive index using Lorentz Lorentz equation
	x = 0
	for x in range(len(df)):
		try:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[2], property_id=mp_id[3], value=float(refind2[x])))
		except ValueError:
			n1.append(Data(mol_graph_id=(dl.mol_graph_id+x+1), met_id=me_id[2], property_id=mp_id[3], value=0))

Data.objects.bulk_create(n1, batch_size=10000)  #Adds all the file data into the database of 'chemdb_den'





