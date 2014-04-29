import publication
import networkx as nx

import re
import unicodedata
from sets import Set
#import matplotlib.pyplot as plt
#import sys




class arbol:

    def __init__(self):
	self.G=nx.DiGraph()
	self.G.clear()
	self.ini_listas()
	
    def ini_listas(self):
	self.list_author = Set([])
	self.list_collaborators = Set([])
	self.list_years = Set([])
	self.list_journals = Set ([])
	self.list_types = Set ([])
	self.list_publisher = Set ([])
	self.list_citation = Set([])
	self.list_reference = Set([])
	
	self.list_objects = Set([])
#	 self.list_valid_authors = Set([])
	
	self.object_tmp = publication.publication()

    def remove_accents(self,data):
	return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

	
    def leer_autores(self, filenameAuthors):
#	 researchers_file = open (filenameAuthors,"r+")
	researchers_file = filenameAuthors
	researchers_file= researchers_file.open()

	for line in researchers_file:
		if '\n' in line and line.__len__>1:
		    string = line.replace('\n','')
		    string = string.title()
		    string = string.strip()
		    self.list_author.add(string)
	researchers_file.close()
	
    def leer(self, filenameBib):
#	 input_file=open(filenameBib,"r+")
	input_file = filenameBib 
	input_file = input_file.open()

##	list_entrada = filenameBib.split('\n')
##	  for line in list_entrada:
	for line in input_file:
	    text=repr(line.decode('unicode-escape'))
	    text= text.encode("utf-8")
	    objeto = self.object_tmp
	    if '@'  in line:
		try:
		    
		    type_pub = re.search('@(.+?){',line).group(1)
		    key_pub = re.search('{(.+?),',line).group(1)
		    type_pub = type_pub.strip()
		    type_pub = type_pub.title()
		    key_pub = key_pub.strip()

		    self.list_types.add(type_pub)
    
		    self.list_objects.add(objeto)
			
		    self.object_tmp = publication.publication()
			
		    self.object_tmp.idp = key_pub
			
		    self.object_tmp.type = type_pub			   
			
		except AttributeError:
		    type_pub = ''
		    key_pub =  ''
	    
	    elif 'author' in line:
		try:
		    collaborators_pub = re.search('{(.+$)',line).group(1)
		    collaborators_pub = collaborators_pub[:-1]			  
		    #collaborators_list = self.obtenerListaAutores(collaborators_pub)
		    collaborators_list = collaborators_pub.split(" and ")
		    for item in collaborators_list:
			string = item.replace('}','')
			string = string.replace(',','')
			string = string.replace('{','')
			string = string.replace('\\','')
			string = string.replace('~','')
			string = string.replace('+','')
			string = string.replace("'",'')
			string = string.strip()
			string = string.title()
			self.list_collaborators.add(string)
			objeto.author.add(string)
			
			
		except AttributeError:
		    collaborators_pub = ''
	    
	    elif 'title' in line and not 'booktitle ' in line:
		try:
		    title_pub = re.search('{(.+?)}',line).group(1)
		    title_pub = title_pub.strip()
		    objeto.title = title_pub
		except AttributeError:
		    title_pub = ''
	    elif 'journal' in line:
		try:
		    journal_pub = re.search('{(.+?)}',line).group(1)
		    journal_pub = journal_pub.strip()
		    self.list_journals.add(journal_pub)
		    objeto.journal = journal_pub
		except AttributeError:
		    journal_pub=''
		    
	    elif 'publisher' in line:
		try:
		    publisher_pub = re.search('{(.+?)}',line).group(1)
		    publisher_pub = publisher_pub.strip()
		    self.list_publisher.add(publisher_pub)
		    objeto.publisher = publisher_pub
		except AttributeError:
		    publisher_pub = ''
		    
	    elif 'year' in line:
		try:
		    year_pub = re.search('{(.+?)}',line).group(1)
		    year_pub = year_pub.strip()
		    self.list_years.add(year_pub)
		    objeto.year = year_pub
		except AttributeError:
		    year_pub =''

	    elif 'citedby' in line or 'reference' in line:
		line=line.replace("{a}",'a')
		line=line.replace("{e}",'e')
		line=line.replace("{i}",'i')
		line=line.replace("{o}",'o')
		line=line.replace("{u}",'u')
		line=line.replace("{",'')
		line=line.replace("}",'')
		line=line.replace("\\'",'')
		line=line.replace("\\v",'')
		line=line.replace("~",'')
		if 'citedby' in line:
		    citation_str = re.search("citedby(.+?)\)",line).group(1)
		    citation_list = citation_str.split(',')
		    for item in citation_list:
			string = item.strip()
			string = string.replace('=','')
			string = string.replace('}','')
			string = string.replace('{','')
			string = string.replace('\\','')
			string = string.replace('(','')
			string = string.replace(')','')
			#string = ''.join(e for e in string if e.isalnum())
			if string.__len__()>0:
				self.list_citation.add(string)
				objeto.citation.add(string)
		if 'reference' in line:
		    reference_str = re.search('reference(.+?)\)',line).group(1)
		    reference_list = reference_str.split(',')
		    for item in reference_list:
			string = item.strip()
			string = string.replace('=','')
			string = string.replace('}','')
			string = string.replace('{','')
			string = string.replace('\\','')
			string = string.replace('(','')
			#string = string.replace(')','')
			string = ''.join(e for e in string if e.isalnum())

			if string.__len__()>0:
				self.list_reference.add(string)
				objeto.reference.add(string)

		
	    elif line.strip().__len__()>0:
		    self.list_objects.add(objeto)
	input_file.close()
    
       
    '''
    Construir el arbol mediante la lectura de un bibtex
    
    '''
    
    def construir_arbol(self,filenameAuthors,filenameBib):
	
	self.__init__()
	
	self.leer_autores(filenameAuthors)
	
	self.G.add_node("publication",leaf='0')

	self.G.add_node("type",leaf='0')
	self.G.add_node("author",leaf='0')
	self.G.add_node("journal",leaf='0')
	self.G.add_node("year",leaf='0')
	self.G.add_node("collaborator",leaf='0')
    
    
	self.G.add_edge("type","publication")
	self.G.add_edge("author","publication")
	self.G.add_edge("journal","publication")
	self.G.add_edge("year","publication")
	self.G.add_edge("collaborator","publication")
    
	self.leer(filenameBib)	  
    
	self.list_years = sorted(self.list_years)
	self.list_author = sorted (self.list_author)
	self.list_journals = sorted (self.list_journals)
	self.list_collaborators = sorted(self.list_collaborators)
		
	for item in self.list_collaborators:
	    if item in self.list_author:
		if item!='':
		    self.G.add_node(item,leaf='0')
		    self.G.add_edge(item,"author")
	    else:
		if item!='':
		    self.G.add_node(item,leaf='0')
		    self.G.add_edge(item,"collaborator")
	#print self.G.nodes(data=False)
		
	for item in self.list_types:	
	    if item != '':
		self.G.add_node(item,leaf='0')
		self.G.add_edge(item,"type")
    
    
	for item in self.list_years:
	    if item != '':
		self.G.add_node(item,leaf='0')
		self.G.add_edge(item,"year")
		
	for item in self.list_journals:
	    if item != '':
		self.G.add_node(item,leaf='0')
		self.G.add_edge(item,"journal")
		
	
	for item in self.list_objects:
	    if item.idp!='':
		
		self.G.add_node(item.idp, data = item, leaf='1') #creo el objeto
				
		for elem in item.author:
		    if self.G.has_node(elem):
			self.G.add_edge(item.idp, elem)    
		    
		if item.year in self.list_years:
		    self.G.add_edge(item.idp, item.year)
		if item.type in self.list_types:
		    self.G.add_edge(item.idp, item.type)
		if item.journal in self.list_journals:
		    self.G.add_edge(item.idp, item.journal)
	
    '''
    
    Metodo auxiliar recursivo
    Es auxiliar al metodo 'extension'
    '''
    def deep_extension(self,focus,list_objects):
	
	if self.G.__contains__(focus):
	    
	    if self.G.predecessors(focus)==[]:
		
		list_objects.add(focus)
	    else:
		for item in self.G.predecessors(focus):
		    self.deep_extension(item,list_objects)
    ## A diferencia de deep_extension, la lista resultante es regresada, no en los argumentos
    # eso se hizo para la recursividad en deep_extension    
    def extension(self,focus):
	    list_a = Set([])
	    list_resultante = Set([])
	    if self.G.has_node(focus):
		self.deep_extension(focus, list_resultante)
		lista = (n for n,d in self.G.nodes_iter(data=True) if d['leaf']=='1' and n in list_resultante)
		
		for item in lista:
		    list_a.add(item)
	    return list_a
	   
    
    def valido(self, concept, list_objs):
	list_concepts = set ([])
	if self.G.has_node(concept):
	    for item in self.G.predecessors(concept):
		if self.extension(item).intersection(list_objs).__len__()>0 and self.G.node[item]['leaf']=='0':
		    list_concepts.add(item)
	    return list_concepts
		    
    def poda_arbol(self,listIds):
	list_iter_pub = (n for n,d in self.G.nodes_iter(data=True) if d['leaf']=='1' )
	list_ids_pub = Set([])
	
	for item in list_iter_pub:
	    list_ids_pub.add(item)
	#Los nodos del arbol que no estan en la lista: remove
	for item in list_ids_pub:
	    if item not in listIds:
		self.G.remove_node(item)		
	
	#los conceptos que no tienen hijos: remove
	for item in self.list_author:	    
	    if self.G.has_node(item):
		if self.extension(item).__len__()<=0:
		    self.G.remove_node(item)
	for item in self.list_collaborators:	   
	    if self.G.has_node(item):
		if self.extension(item).__len__()<=0:
		    self.G.remove_node(item)
	for item in self.list_years:	   
	    if self.G.has_node(item):
		if self.extension(item).__len__()<=0:
		    self.G.remove_node(item)
	for item in self.list_types:	   
	    if self.G.has_node(item):
		if self.extension(item).__len__()<=0:
		    self.G.remove_node(item)
	for item in self.list_journals:       
	    if self.G.has_node(item):
		if self.extension(item).__len__()<=0:
		    self.G.remove_node(item)
	self.ini_listas()
