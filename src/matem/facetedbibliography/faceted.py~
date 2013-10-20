# -*- coding: utf-8 -*-
from matem.facetedbibliography.modules import interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import os
from Products.Five import BrowserView
from sets import Set



class FacetedView(BrowserView):

    template = ViewPageTemplateFile('faceted_view.pt')

    def __init__(self,context,request):
    	self.context = context
    	self.request = request
        curpath = os.path.abspath(os.curdir)
        self.researchers_file = os.path.join(curpath, "researchers.txt")
        bib_file = os.path.join(curpath, "archivo0.bib")
        self.bib_file_cit = os.path.join(curpath, "archivo1.bib")
        self.bib_file_ref = os.path.join(curpath, "archivo2.bib")
        self.interface_principal = interface.interface(self.researchers_file,bib_file)
 
        
        self.interface_principal.ini_listas()
        
        self.list_c = self.interface_principal.list_citation #objetos
        self.list_r = self.interface_principal.list_reference #objetos
        
        self.interface_citation = interface.interface(self.researchers_file,self.bib_file_cit)
        self.interface_reference = interface.interface(self.researchers_file,self.bib_file_ref)
        self.interface_citation.tree.poda_arbol(self.list_c)
        self.interface_reference.tree.poda_arbol(self.list_r)
        self.interface_citation.ini_listas()
        self.interface_reference.ini_listas()
        

    	self.submitted_faceta = self.request.form.get('faceta', False)
    	self.submitted_citation = self.request.form.get('citation', False)
    	self.submitted_reference = self.request.form.get('reference', False)
    	self.submitted_button = self.request.form.get('clear', False)
    	
    	self.list_input = Set([])
    	self.list_input_citation = Set([])
    	self.list_input_reference  = Set([])    
	
    def listas(self, lista_mix):
        for item in lista_mix:
                
                if not "+" in item:
                        self.list_input.add(item) 
                elif "+c" in item:
                        string = item.replace("+c",'')
                        self.list_input_citation.add(string)                       
                elif "+r" in item:
                        string = item.replace("+r",'')
                        self.list_input_reference.add(string)
                  
        
    def calcula_princ(self,list_input):
	
	self.list_input = list_input
	self.interface_principal.get_list_objects(self.list_input)
            
        if not self.interface_principal.compare(self.list_c, self.interface_principal.list_citation):
                     
               self.list_c = self.interface_principal.list_citation
               self.interface_citation.tree.construir_arbol(self.researchers_file, self.bib_file_cit)
               self.interface_citation.tree.poda_arbol(self.list_c)
               self.interface_citation.ini_listas()

        if not self.interface_principal.compare(self.list_c, self.interface_principal.list_reference):
               self.list_r = self.interface_principal.list_reference
               self.interface_reference.tree.construir_arbol(self.researchers_file, self.bib_file_ref)
               self.interface_reference.tree.poda_arbol(self.list_r)
               self.interface_reference.ini_listas()

    def calcula_citation(self, list_input_citation):
        
    	self.list_input_citation = list_input_citation
    	self.interface_citation.get_list_objects(self.list_input_citation)

    def calcula_reference(self,list_input_reference):
        
    	self.list_input_reference = list_input_reference 
    	self.interface_reference.get_list_objects(self.list_input_reference)

    def update(self):
	
    	self.submitted_faceta =self.request.form.get('faceta','')
    	self.submitted_citation = self.form.get('citation','')
    	self.submitted_reference = self.form.get('reference','')
	
    def __call__(self):
    	if  self.submitted_faceta:
    	    list_a = self.request.form.get('faceta','')
    	    self.listas(list_a)
    	    self.calcula_princ(self.list_input)
    	    self.calcula_citation(self.list_input_citation)
    	    self.calcula_reference(self.list_input_reference)
    	    self.request.form.update()
    	    return self.template()
    
    	if  self.submitted_citation:
    	    list_a = self.request.form.get('citation','')
    	    self.listas(list_a)
    	    self.calcula_citation(self.list_input_citation)
    	    self.calcula_reference(self.list_input_reference)
    	    self.request.form.update()
    	    return self.template()
    
    
    	if  self.submitted_reference:
    	    list_a = self.request.form.get('reference','')    	    
    	    self.listas(list_a)
    	    self.calcula_reference(self.list_input_reference)
    	    self.request.form.update()
    	    return self.template()
 	return self.template()
       
        
    def indice_h(self):
        return self.interface_principal.indice_h()
	
    def indice_i10(self):
        return self.interface_principal.indice_i10() 

    def show_years(self):
        return sorted(self.interface_principal.list_year)

    def show_authors(self):
	return sorted(self.interface_principal.list_author)

    def show_types(self):
	return sorted(self.interface_principal.list_type)

    def show_journals(self):
	return sorted(self.interface_principal.list_journal)

    def show_collaborators(self):
	return sorted(self.interface_principal.list_collaborator)
	
    def show_pub(self):
	return sorted(self.interface_principal.return_list_objs())
	
    def show_list_input(self):
	return sorted(self.list_input)
	
    
#
##########################################################################

    def show_years_cit(self):
        return sorted(self.interface_citation.list_year)

    def show_authors_cit(self):
	return sorted(self.interface_citation.list_author)

    def show_types_cit(self):
	return sorted(self.interface_citation.list_type)

    def show_journals_cit(self):
	return sorted(self.interface_citation.list_journal)

    def show_collaborators_cit(self):
	return sorted(self.interface_citation.list_collaborator)

    def show_pub_cit(self):
	return sorted(self.interface_citation.return_list_objs())

    def show_empty_cit(self):
	return sorted(self.interface_citation.list_empty)

    ###########################################################################

    def show_years_ref(self):
        return sorted(self.interface_reference.list_year)

    def show_authors_ref(self):
	return sorted(self.interface_reference.list_author)

    def show_types_ref(self):
	return sorted(self.interface_reference.list_type)

    def show_journals_ref(self):
	return sorted(self.interface_reference.list_journal)

    def show_collaborators_ref(self):
	return sorted(self.interface_reference.list_collaborator)

    def show_pub_ref(self):
	return sorted(self.interface_reference.return_list_objs())

    def show_empty_ref(self):
	return sorted(self.interface_reference.list_empty)

