'''
Created on 27/08/2013

@author: Alejandra
'''
import arbol
import sys
import re
from sets import Set

class interface(object):
    '''
    classdocs
    '''
    def __init__(self,filenameAuthors,filenameBib):
	self.tree = arbol.arbol()
	
	self.tree.construir_arbol(filenameAuthors,filenameBib)
	#objetos resultantes
	self.list_objs = Set([])  #lista de puros identificadores
	# los objetos de cada concepto -- la extension de los conceptos seleccionados
	self.list_ext_author  = Set([])
	self.list_ext_journal = Set([])
	self.list_ext_type = Set([])
	self.list_ext_year = Set([])
	self.list_ext_collaborator = Set([])
	# los conceptos validos
	
	self.list_val_author = Set([])
	self.list_val_journal = Set([])
	self.list_val_type = Set([])
	self.list_val_year = Set([])
	self.list_val_collaborator = Set([])
	
	#lista de conceptos
	self.list_author = Set([])
	self.list_journal = Set([])
	self.list_type = Set([])
	self.list_year = Set([])
	self.list_collaborator = Set([])
	
	self.list_input =Set([])
	
	self.list_reference = Set([]) #lista de objetos referencia de todos las publicaciones validas
	self.list_citation = Set([]) #lista de objetos citas de todas las publicaciones validas
	
    def ini_listas(self):
	
		
	self.list_ext_author = self.tree.extension("author")
	self.list_objs = self.list_ext_author
	
	self.list_ext_collaborator = self.tree.extension("collaborator")
	self.list_objs = self.list_objs.union(self.list_ext_collaborator)
	
	self.list_ext_type = self.tree.extension("type")
	self.list_objs = self.list_objs.union(self.list_ext_type)
	
#	list_aux=[]
#	for item in self.tree.G.predecessors("year"):#extension("year")
#		list_aux.append(item)
#	 self.list_ext_year=list_aux 
	self.list_ext_year = self.tree.extension("year")
	
	self.list_objs = self.list_objs.union(self.list_ext_year)
	
	self.list_ext_journal = self.tree.extension("journal")
	self.list_objs = self.list_objs.union(self.list_ext_journal)
	
	self.list_val_author = self.tree.valido("author", self.list_ext_author)
	self.list_val_collaborator = self.tree.valido("collaborator", self.list_ext_collaborator)
	self.list_val_type = self.tree.valido("type", self.list_ext_type)
	self.list_val_year = self.tree.valido("year", self.list_ext_year)
	self.list_val_journal = self.tree.valido("journal", self.list_ext_journal)

	self.list_author = self.list_val_author
	self.list_type = self.list_val_type
	self.list_year = self.list_val_year
	self.list_journal = self.list_val_journal
	self.list_collaborator = self.list_val_collaborator
	    
	
	list_c = Set([])
	list_r = Set([])
	for item in self.list_objs:
	    obj = self.tree.G.node[item]['data']
	    list_c = list_c.union(obj.citation)  #union de listas
	    list_r = list_r.union(obj.reference)
	self.list_citation = list_c
	self.list_reference = list_r	    
	
    def get_list_objects(self,list_input):
	
	if list_input.__len__()>0:
	    self.calculo_concepto_author(list_input)
	    self.calculo_concepto_journal(list_input)
	    self.calculo_concepto_type(list_input)
	    self.calculo_concepto_year(list_input)
	    self.calculo_concepto_collaborator(list_input)
	    
	    for item in list_input:
		if item in self.list_year:
		    self.list_objs = self.list_objs.intersection(self.list_ext_year)
		 
		elif item in self.list_type:
		    self.list_objs = self.list_objs.intersection(self.list_ext_type)
		
		elif item in self.list_author:
		    self.list_objs = self.list_objs.intersection(self.list_ext_author)
		    
		elif item in self.list_collaborator:
		    self.list_objs = self.list_objs.intersection(self.list_ext_collaborator)

		elif item in self.list_journal:
		    self.list_objs = self.list_objs.intersection(self.list_ext_journal)
	    self.related_concepts()
	else:
	    self.ini_listas()
    def related_concepts(self):		   
	self.list_val_author = sorted(self.tree.valido("author", self.list_objs))
	self.list_val_type = sorted(self.tree.valido("type", self.list_objs))
	self.list_val_journal = sorted(self.tree.valido("journal", self.list_objs))
	self.list_val_year = sorted(self.tree.valido("year", self.list_objs))
	self.list_val_collaborator = sorted(self.tree.valido("collaborator", self.list_objs))
	list_c = Set([])
	list_r = Set([])
	for item in self.list_objs:
		obj = self.tree.G.node[item]['data']
		list_c = list_c.union(obj.citation)  #union de listas
		list_r = list_r.union(obj.reference)
	    
	    #de la lista de objetos obtengo las citas y referencias que son IDs
	self.list_citation = list_c #self.tree.get_objects_list(list_c) #obtengo los objetos con los IDs pasados
	self.list_reference = list_r #self.tree.get_objects_list(list_r)
	    

    def calculo_concepto_author(self,list_input):
	if list_input.intersection(self.list_author).__len__()>0:
	    list_aux = Set([])
	    for item in list_input:
		if item in self.list_author:
		    list_aux = self.tree.extension(item).union(list_aux)
		
	    self.list_ext_author = list_aux
	    self.list_objs = self.list_ext_author
	    
    def calculo_concepto_collaborator(self,list_input):
	if list_input.intersection(self.list_collaborator).__len__()>0:
	    list_aux = Set([])
	    for item in list_input:
		if item in self.list_collaborator:
		    list_aux = self.tree.extension(item).union(list_aux)
		
	    self.list_ext_collaborator = list_aux
	    self.list_objs = self.list_ext_collaborator
	    
    def calculo_concepto_year(self,list_input):
	if list_input.intersection(self.list_year).__len__()>0:
	    list_aux = Set([])
	    for item in list_input:
		if item in self.list_year:
		    list_aux = self.tree.extension(item).union(list_aux)
	
	    self.list_ext_year = list_aux
	    self.list_objs = self.list_ext_year
    def calculo_concepto_type(self,list_input):
	if list_input.intersection(self.list_type).__len__()>0:
	    list_aux = Set([])
	    for item in list_input:
		if item in self.list_type:
		    list_aux = self.tree.extension(item).union(list_aux)
	
	    self.list_ext_type = list_aux
	    self.list_objs = self.list_ext_type
	
    def calculo_concepto_journal(self,list_input):
	if list_input.intersection(self.list_journal).__len__()>0:
	    list_aux = Set([])
	    for item in list_input:
		if item in self.list_journal:
		    list_aux = self.tree.extension(item).union(list_aux)
	
	    self.list_ext_journal = list_aux
	    self.list_objs = self.list_ext_journal
	    
    def print_list_objs(self):
	for item in self.list_objs:
	    obj = self.tree.G.node[item]['data']
	    print obj.idp, obj.type, obj.title,'\n', obj.author, obj.journal, obj.publisher, obj.year
	    print "list citation ",sorted(obj.citation)
	    print "list reference ",sorted(obj.reference), '\n\n'
	    
	print "\n"
	
    def return_list_objs(self):
	list_string_obj = Set([])
	for item in self.list_objs:
	  if self.tree.G.has_node(item): 
	    obj = self.tree.G.node[item]['data']

	    if obj.type=='':
		type_='--'
	    else:
		type_=obj.type

	    if obj.year=='':
		year_='--'
	    else:
		year_=obj.year

	    if obj.journal=='':
		journal_='--'
	    else:
		journal_=obj.journal

	    if obj.publisher=='':
		publisher_='--'
	    else:
		publisher_=obj.publisher

	    if obj.author.__len__()==0:
		author_='--'
	    else:
		author_=', '.join(obj.author)

	    if obj.title=='':
		title_='--'
	    else:
		title_=obj.title
		
	    cad1 = obj.idp  +'%%' + title_+ '%%'+ type_ +'%%' 
	    cad2 = author_  +'%%'      
	    cad3 = journal_ +'%%' +  year_  +'%%'
	    cad4 = ','.join(obj.citation)
	    cad5= ','.join(obj.reference)
	    if cad4.__len__()>0:
		cadx= cad4  +'%%'
	    else:
		cadx = '%%'
	    if cad5.__len__()>0:
		cady= cad5 +''
	    else:
		cady = ''
	    
	    string = cad1 + cad2 + cad3 + cadx + cady
	    list_string_obj.add(string)

	b=[]
	for item in list_string_obj:
		l=item.split('%%')
		b.append(l)
	c=sorted(b, key=lambda x: x[1])
	d=[]
	for item in c:
		string='%%'.join(item)
		d.append(string)
#	self.print_list_objs()
		
	return d


    

    def indice_h(self):
	tup_list = Set([]) 
	lista = (n for n,d in self.tree.G.nodes_iter(data=True) if d['leaf']=='1' )
	for item in lista:
	    obj = self.tree.G.node[item]['data']
	    num_citations = obj.citation.__len__()	
	    tupla = (num_citations, item)    
	    tup_list.add(tupla)
	indexh_list = sorted(tup_list, key=lambda x:x[0], reverse=True)
	i=1
	indice_h=0
	#indexh_list=[(5,'abc'),(4,'cedf'), (4,'gh'),(1,'aa')]
	for item in indexh_list:
	    if i <= item[0]:
		indice_h = i
	    else:
		break
	    i= i + 1
	#print indexh_list
	return indice_h

    def indice_i10(self):
	tup_list = Set([]) 
	lista = (n for n,d in self.tree.G.nodes_iter(data=True) if d['leaf']=='1' )
		    
	for item in lista:
	    obj = self.tree.G.node[item]['data']
	    num_citations = obj.citation.__len__()	
	    tupla = (num_citations, item)    
	    tup_list.add(tupla)
	index_list = sorted(tup_list, key=lambda x:x[0], reverse=True)
	
	i=1
	indice_i10 = 0
	#index_list=[(15,'abc'),(14,'cedf'), (10,'gh'),(3,'aa')]
	for item in index_list:
	    if	item[0]>=10:
		indice_i10 = i
	    else:
		break
	    i= i + 1
	#print index_list
	return indice_i10
    def compare(self,set1, set2):
	flag=False
	if set1.__len__() == set2.__len__():
	    for item in set1:
		if item in set2:
		    flag = True
		else:
		    return False
	    return flag
	else:
	    return False 
