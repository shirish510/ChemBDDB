from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemdb.settings")
from sets import Set
import django
django.setup()
from django.contrib.sessions.models import Session
import pickle
sys.path.insert(0, "/user/m27/pkg/openbabel/2.3.2/lib")
import openbabel
import pybel

from chembddb.models import MolGraph, Publication, MolProp, Data, Method

from chembddb.forms import *
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import numpy as np
import subprocess

# from StdSuites.Type_Names_Suite import null

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return HttpResponseRedirect('/chembddb/register/success/')
    else:
        form = RegistrationForm()  # until the submit button is not pressed, the first if loop will not be entered.

    return render(request, 'registration/register.html', {'form': form})

def login(request):
        username = request.POST['username'],
        password = request.POST['password'],
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,
                      '/chembddb/register/success/')
        else:
            return render(request, 'registration/login.html')



def register_success(request):
    print "Here in Successful registration\n"
    return render(request,
                  'registration/success.html',
                  )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/chembddb/')

def reviewRequest(request):
    check = MolGraph.objects.filter(
        verification=False)  # check - gets all the objects that are to be reviewed by the admin.

    info = []
    name_list = []
    cids = map(lambda x: x.id, check)  # returns the id's of check
    count = 0
    # if request.method == 'GET':
    x = 0
    for c in cids:
        count += 1
        name = MolGraph.objects.get(pk=c).compound_str
        temp = name
        temp = temp + ";" + MolGraph.objects.get(pk=c).SMILES_str
        dataset = Data.objects.filter(mol_graph_id=c)
        for val in dataset:
            p = MolProp.objects.get(pk=val.property_id)
            temp = temp + ";" + str(p.prop)
            data = " "
            if (val.value != 0.0):
                data = str(val.value) + " " + p.unit
                temp = temp + ";" + data
                try:
                    m = Method.objects.get(pk=val.met_id).method
                    temp = temp + ";" + m
                except ObjectDoesNotExist:
                    m = " "
                temp = temp + ";" + val.credit

        info.append(temp)
        name_list.append(name)

        if "approve_" + name in request.POST:
            ob = MolGraph.objects.get(pk=c)
            ob.verification = True
            ob.save()
            return HttpResponseRedirect('/chembddb/reviewrequest')
        elif "reject_" + name in request.POST:
            MolGraph.objects.get(id=c).delete()
            return HttpResponseRedirect('/chembddb/reviewrequest')
            # Do something

    lis = zip(info, name_list)

    return render(request, 'chembddb/reviewpage.html', {'lis': lis})

def submitRequest(request):
    err_list = []
    prop_list = MolProp.objects.all()
    prop_strings = []
    context = []
    if request.method == 'POST':
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location='/projects/academic/hachmann/shirish/python/mysite/chembddb/media')
            filename = fs.save(myfile.name, myfile)
            # print myfile.name
            uploaded_file_url = fs.url(filename)
            subprocess.Popen(['python','/projects/academic/hachmann/shirish/python/mysite/chembddb/feeder.py', filename])
            # execfile("bulktry.py")
            return render(request, 'chembddb/requestpage.html', {'uploaded_file_url': uploaded_file_url})
        elif (request.POST['molecule_string'] and request.POST['smiles_string']):
            mol_str = request.POST['molecule_string']
            smiles_str = request.POST['smiles_string']
            property_str = ""
            cand = MolGraph(compound_str=mol_str, SMILES_str=smiles_str, verification=False)
            cand.save()
            c = MolGraph.objects.filter(SMILES_str=smiles_str)
            cid = map(lambda x: x.id, c)
            pn = map(lambda x: x.prop, prop_list)
            pid = map(lambda x: x.id, prop_list)
            pdic = dict(zip(pn, pid))
            for prop in prop_list:
                val = request.POST[prop.prop + "_val"]
                unit = request.POST[prop.prop + "_unit"]
                pub = request.POST[prop.prop + "_pub"]
                met = request.POST[prop.prop + "_met"]
                cm = request.POST[prop.prop + "_metcom"]
                if (val):
                    if (pub):
                        p = Publication(publ_str=pub)
                        p.save()
                        p1 = Publication.objects.filter(publ_str=pub)
                        p1id = map(lambda x: x.id, p1)
                        if (met):
                            m = Method(method=met, comment=cm)
                            m.save()
                            m1 = Method.objects.filter(method=met)
                            mid = map(lambda x: x.id, m1)
                            n = Data(mol_graph_id=cid[0], publication_id=p1id[0], met_id=mid[0], property_id=pdic[prop.prop],
                                 value=float(val), credit=request.user.username)
                        else:
                            n = Data(mol_graph_id=cid[0], publication_id=p1id[0], property_id=pdic[prop.prop],
                                     value=float(val), credit=request.user.username)
                        n.save()
                    else:
                        p = Publication(publ_str=" ")
                        p.save()
                        p1 = Publication.objects.filter(publ_str=" ")
                        p1id = map(lambda x: x.id, p1)
                        n = Data(mol_graph_id=cid[0], property_id=pdic[prop.prop], value=float(val),
                                 credit=request.user.username)
                        n.save()
            return HttpResponseRedirect('/chembddb/')
        else:
            if (not request.POST['molecule_string']):
                err_list.append("Please provide a name to the molecule")
            if (not request.POST['smiles_string']):
                err_list.append("Please provide SMILES string for the molecule")

    return render(request, 'chembddb/requestpage.html', {'property_list': prop_list, 'error_list': err_list})

def index(request):
    prop_list = MolProp.objects.all()
    mol_objects = []
    mol_objects_smi = []
    data_prop_search = []
    mol_graph_id_set = Set()
    mol_graph_list = []
    query_text = []
    prop_names = map(lambda x: x.prop, prop_list)
    prop_id = map(lambda x: x.id, prop_list)
    context = {}
    key = 'my_mol_prob'
    if('queried_text' in request.POST.keys() and request.POST['queried_text']):  # check if queried_text is entered at all and also check if the entered text is not empty
        query_text = request.POST['queried_text']
        if request.POST['verified'] == "1":
            # POST is a dictionary which can be accessed through its key
            # print("queried_text {}".format(query_text))

            mol_objects_smi = MolGraph.objects.get(SMILES_str__exact=query_text,verification=True)  # matches exactly
            # mol_objects_str = MolGraph.objects.get(compound_str__icontains=query_text,verification=True)  # case insensitive, matches substring
        else:
            mol_objects_smi = MolGraph.objects.get(SMILES_str__exact=query_text)  # matches exactly
            # mol_objects_str = MolGraph.objects.get(compound_str__icontains=query_text)  # case insensitive, matches substring
        mol_objects = Data.objects.filter(mol_graph_id=mol_objects_smi.id)
    elif (request.method == 'POST'):
        print "Its inside this loop"
        # request.session.modified = True
        prop_from = []
        prop_to = []
        # prop_unit = map(lambda x: x.unit, prop_list)
        context['propname'] = []
        context['from_field'] = []
        context['to_field'] = []
        for prop in prop_names:
            prop_from = ""  # the value entered in MIN text area by user
            prop_to = ""  # the value entered in MAX text area by user
            if (prop in request.POST.keys()):
                prop_from_text_field = prop + "_from_val"
                prop_to_text_field = prop + "_to_val"
                # for u in unit_list:
                # if (u.unit_str in request.POST.keys()):
                prop_unit_name = prop + "_unit"
                # This is to modify the unit of Bohr3 to C2m2J-1
                if (prop_unit_name in request.POST.keys() and request.POST[prop_unit_name] == "coulomb"):
                    prop_from = float(request.POST[prop_from_text_field])
                    prop_from = float(prop_from/(1.3305))
                    prop_to = float(request.POST[prop_to_text_field])
                    prop_to = float(prop_to/(1.3305))
                    # prop_from_text_field = prop_from_text_field/(1.3305*1e-9)
                    # prop_to_text_field = prop_to_text_field/(1.3305*1e-9)

                # This is to modify the unit of Bohr3 to cm3
                elif (prop_unit_name in request.POST.keys() and request.POST[prop_unit_name] == "cubiccm"):
                    prop_from = float(request.POST[prop_from_text_field])
                    prop_from = float((prop_from)/(0.148))
                    prop_to = float(request.POST[prop_to_text_field])
                    prop_to = float((prop_to)/(0.148))

                # This is to modify the unit for Hartree into Calories:
                elif (prop_unit_name in request.POST.keys() and request.POST[prop_unit_name] =="g/cm3"):
                    prop_from = float(request.POST[prop_from_text_field])
                    prop_to = float(request.POST[prop_to_text_field])
                    prop_from = float(prop_from/0.001)
                    prop_to = float(prop_to/0.001)

                # This is to modify the unit for Hartree into eV
                # elif (prop_unit_name in request.POST.keys() and request.POST[prop_unit_name] =="electrovolt"):
                #     prop_from = float(request.POST[prop_from_text_field])
                #     prop_to = float(request.POST[prop_to_text_field])
                #     prop_from = float(prop_from/27.2114)
                #     prop_to = float(prop_to/27.2114)

                else:
                    if (prop_from_text_field in request.POST.keys() and request.POST[prop_from_text_field]):
                        prop_from = request.POST[prop_from_text_field]
                    if (prop_to_text_field in request.POST.keys() and request.POST[prop_to_text_field]):
                        prop_to = request.POST[prop_to_text_field]

                    if (prop_from or prop_to):
                        data_prop_search = Data.objects.filter(property_id=request.POST[prop])
                        if (prop_to):
                            data_prop_search = data_prop_search.filter(value__lte=prop_to)
                        if (prop_from):
                            data_prop_search = data_prop_search.filter(value__gte=prop_from)
                    mol_id_set = Set(map(lambda x: x.mol_graph_id, data_prop_search))

                    if (len(mol_graph_id_set) > 0):
                        mol_graph_id_set = mol_graph_id_set.intersection(mol_id_set)  # When new set is added to the existing set this command helps to add only new set of data.
                    else:
                        mol_graph_id_set = mol_id_set

            context['from_field'].append(prop_from)
            context['to_field'].append(prop_to)
            mol_graph_list = mol_graph_id_set

        # mol_data = MolGraph.objects.filter(id__in=mol_graph_list)
        request.session[key] = pickle.dumps(mol_graph_list)
        mol_objects1 = pickle.loads(request.session[key])
        mol_objects_smiles = Data.objects.all()
        mol_objects = mol_objects_smiles.filter(mol_graph_id__in=mol_objects1, property_id__in=prop_id).select_related('mol_graph').defer('met', 'publication', 'credit')

           # Now get mol_graph_id of every exp data retrieved and store it in a set to avoid duplication
        '''for mol_graph_id in mol_graph_id_set:
            mol_objects.append(MolGraph.objects.get(pk=mol_graph_id))'''
            # the variables stored in context can be used in html files

        query_text = request.GET.get('queried_text')

    elif ('page' in request.GET.keys()):  # For other pages when a property is advanced searched
        mol_objects1 = pickle.loads(request.session[key])
        mol_objects_smiles = Data.objects.all()
        mol_objects = mol_objects_smiles.filter(mol_graph_id__in=mol_objects1, property_id__in=prop_id).select_related('mol_graph').defer('met', 'publication', 'credit')

    elif ('page' not in request.GET.keys()):  # For homepage
        request.session.modified = True
        key = 'my_mol_prob'
        mol_graph_list = []
        context ={'request':request, 'query_text':query_text, 'property_list':prop_list}
        return render(request, 'chembddb/index.html', context)

    #For plotting of graph between two properties.


    page = request.GET.get('page')
    paginator = Paginator(mol_objects, 80)
    try:
        compounds = paginator.page(page)
    except PageNotAnInteger:
        compounds = paginator.page(1)
    except EmptyPage:
        compounds = paginator.page(paginator.num_pages)

    # Here the values from mol_objects is extracted to get only polymer property values.
    mol_obj = mol_objects.values_list('value', flat=True)
    paginator = Paginator(mol_obj, 80)
    try:
        compound2 = paginator.page(page)
    except PageNotAnInteger:
        compound2 = paginator.page(1)
    except EmptyPage:
        compound2 = paginator.page(paginator.num_pages)


    context['compound_list'] = mol_objects
    context['comp'] = compound2
    # context['compound_count'] = compounds.count()
    context['property_list'] = prop_list
    context['pcount'] = prop_list.count()
    context['query_text'] = query_text
    context['compounds'] = compounds
    context['request'] = request

    #context['unit_list']=unit_list
    # context = {'compound_list': compound_list_query, 'property_list': prop_list, 'query_text': query_text,}

    return render(request, 'chembddb/index.html', context)

# class DetailView(generic.DetailView):
#     model = MolGraph
#     template_name = 'chembddb/detail.html'

def mol_detail(request, mol_graph_id):
    dataset = Data.objects.filter(mol_graph_id=mol_graph_id)
    prop_list = []
    val_list = []
    credit_list = []
    ver_list = []
    pub_list = []
    met_list = []
    info_list = []
    info = " "
    unit_list = []
    for val in dataset:
        p = MolProp.objects.get(pk=val.property_id)

        data = " "
        if (val.value != 0.0):
            data = str("%.2f" % val.value)
            prop_list.append(p.prop)
            if val.met_id:
                m = Method.objects.get(pk=val.met_id)
                met_list.append(m.method)
            else:
                met_list.append("")
            if MolGraph.objects.get(pk=mol_graph_id).verification == True:
                ver_list.append("Verified")
            else:
                ver_list.append("Not Verified")
            credit_list.append(val.credit)
            # if(p.unit_set.count()): # check if this property has unit
            # data = data + " " + p.unit
            data = data + " "
            val_list.append(data)
            # val_list.append(data)

        else:
            data = str("%.2f" % val.value)
            prop_list.append(p.prop)
            if val.met_id:
                m = Method.objects.get(pk=val.met_id)
                met_list.append(m.method)
            else:
                met_list.append("")
            if MolGraph.objects.get(pk=mol_graph_id).verification == True:
                ver_list.append("Verified")
            else:
                ver_list.append("Not Verified")
            credit_list.append(val.credit)
            # if(p.unit_set.count()): # check if this property has unit
            # data = data + " " + p.unit
            data = data + " "
            val_list.append(data)
            # val_list.append(data)


        # pub1=Publication.objects.get(pk = val.publication_id)
        pub_list.append(" ")

        smiles_str = str(MolGraph.objects.get(pk=mol_graph_id).SMILES_str)
        # obConversion = openbabel.OBConversion()
        # obConversion.SetInFormat("smi")
        # mol = openbabel.OBMol()
        # obConversion.ReadString(mol, smiles_str)
        '''Creating an XYZ file from SMILES String using Openbabel and Pybel function. This XYZ is used for 3D visualization of polymer molecule structure'''
        mol = pybel.readstring("smi", smiles_str)
        mol.make3D(forcefield="mmff94", steps= 100)
        mol.write("xyz", "./chembddb/static/xyz/mol.xyz", overwrite = True)

        smiles_string = str(MolGraph.objects.get(pk=mol_graph_id).SMILES_str)
        # mol = pybel.readstring("smi", smiles_str)
        info = str(mol.molwt)
        info_list.append(info)
        info = str(mol.formula)
        info_list.append(mol.formula)
        info = str(mol.OBMol.NumAtoms())
        info_list.append(mol.OBMol.NumAtoms())
        info = str(mol.OBMol.NumBonds())
        info_list.append(info)

    context = {'smiles_str': smiles_string,
               'detail_list': zip(prop_list, val_list, pub_list, met_list, ver_list, credit_list),'mol_id': mol_graph_id, 'info_list': info_list,}
    return render(request, 'chembddb/detail.html', context)
