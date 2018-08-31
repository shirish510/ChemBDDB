from __future__ import unicode_literals

# import django_filters
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.fields import BooleanField

# Create your models here.
class MolGraph(models.Model):
#   doi_str = models.CharField("DOI string", max_length=128, unique=True)
    compound_str = models.CharField("Compound Name", db_index=True, max_length=256, blank=True)
    SMILES_str = models.CharField("SMILES string", db_index=True, max_length=256, blank=True)
    verification = models.BooleanField("flag that tells us if the data is verified", default=True)

    #add canonical SMILES

    def __str__(self):
        return self.SMILES_str


class Publication(models.Model):
    publ_str = models.CharField("canonical string of the publication reference", max_length=2048, blank=True)
    
    
class MolProp(models.Model):
    prop = models.CharField("Keyword for property", db_index=True, max_length = 32, default='00000')
    unit = models.CharField( "keyword for unit", db_index=True, max_length=32,default=' ')

#class Unit(models.Model):
#    prop_name = models.ForeignKey(MolProp)
#    unit_str = models.CharField("unit" , max_length = 256, blank= True)
#    primary_unit = models.BooleanField("to be used as primary unit while displaying property value", default=False)

class Method(models.Model):
    method = models.CharField( "Keyword for method", db_index=True, max_length = 32, default='00000')
    comment = models.CharField( "details for the method", db_index=True, max_length=256, blank=True)

class Data(models.Model):
    mol_graph = models.ForeignKey(MolGraph)
    publication = models.ForeignKey(Publication, null=True)
    met=models.ForeignKey(Method, null = True)
    property = models.ForeignKey(MolProp, null=True)
    #unit=models.ForeignKey(Unit,null=True)
    #later add original or referenced
    value = models.FloatField(db_index=True, null=True, blank = True)
    
    credit=models.CharField( "username", max_length=256, default="The Hachmann Group")
    def __str__(self):
        # return (str(self.mol_graph)) + '.data'
        return str("%.2f" % self.value)
    class Meta:
        index_together=[['mol_graph','property','value']]
    

    
#class Candidate(models.Model):
#   molecule_str = models.CharField("Molecule name",max_length=256,blank=False)
#    smiles_str = models.CharField("SMILES str", max_length=256,blank=False)
#    property_str = models.CharField("Encoded Property String", max_length=4096, blank=True)
#    user = models.CharField("Username", max_length=256, blank=False)
   
# class Bookkeeping(models.Model):
#     mol_info = models.ForeignKey('MolGraph')
#     mol_prop = models.ForeignKey('MolProp')
#     entry_date = models.DateField(auto_now_add=True, null=True, blank=True)

#class Contributor(models.Model):
#    firstname_str = models.CharField("First name" , max_length = 256)
#    lastname_str = models.CharField("Last name" , max_length = 256)
#    affiliation_str = models.CharField("Name of School" , max_length = 512, blank= True)
#    email = models.EmailField("email id", max_length = 108, blank = True)
