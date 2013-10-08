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
        bib_file = os.path.join(curpath, "archivo.bib")
	self.textfile1 = os.path.join(curpath, "list_input.txt")
	####conflictos consultando al mismo tiempo en diferentes sesiones, es importante
	####incluir los checkboxes y esperar que esos se reflejen unicamente en la
	####sesion actual

        list_empty = Set([])
        self.interface_principal = interface.interface(list_empty, self.researchers_file , bib_file)
        self.interface_principal.ini_listas()

        self.list_c = self.interface_principal.list_citation #objetos
        self.list_r = self.interface_principal.list_reference #objetos


        self.interface_citation = interface.interface(self.list_c, self.researchers_file, bib_file)
        self.interface_reference = interface.interface(self.list_r, self.researchers_file, bib_file)
        self.interface_citation.ini_listas()
        self.interface_reference.ini_listas()
	self.submitted_faceta = self.request.form.get('faceta', False)
	self.submitted_citation = self.request.form.get('citation', False)
	self.submitted_reference = self.request.form.get('reference', False)
	self.list_input = Set([])
	#self.list_input = self.interface_principal.add_list_input(list_empty, self.textfile1)
	self.list_input_citation = Set([])
	self.list_input_reference  = Set([])
	#self.calcula_princ(self.list_input)
	###al calcular con la entrada list_input (by lectura de archivos) se actualiza
	### en el caso de los checkboxes habria que ver si los checked envian solicitudes
	### que no creo,
	### lo importante es ver si se conserva lo list_input dado los checked
	### y cuando se recargue la pagina las facetas sean consistentes con los checked
	###pues asi sabremos que los list_input se conservan, (tengo mis dudas)
	##seria bueno ver si hay una funcion JS que me permita checar los cheked y hacer un submit 
	## de aquellos checked, refresh aqui __init__ como con calcula y poner las cosas en orden

    def calcula_princ(self,list_input):
	    
	self.list_input = list_input
	self.interface_principal.get_list_objects(self.list_input)
	

        if self.list_c != self.interface_principal.list_citation:
                    self.list_c = self.interface_principal.list_citation
                    self.interface_citation.tree.building_tree(self.list_c,self.researchers_file)
                    self.list_input_citation.clear()
                    self.interface_citation.ini_listas()
                    self.interface_citation.get_list_objects(self.list_input_citation)

        if self.list_r != self.interface_principal.list_reference:
                    self.list_r = self.interface_principal.list_reference
                    self.interface_reference.tree.building_tree(self.list_r,self.researchers_file)
                    self.list_input_reference.clear()
                    self.interface_reference.ini_listas()
                    self.interface_reference.get_list_objects(self.list_input_reference)  	     	   

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
        # make sure we had a proper form submit, not just GET request
	

	if  self.submitted_faceta:
	    #self.list_input = self.interface_principal.add_list_input(self.request.form.get('faceta',''), self.textfile1)   
	    focus = self.request.form.get('faceta','')
	    string = ''.join(focus)
	    self.list_input.add(string)
	    self.interface_principal.list_input.add(string)
	    print string, self.list_input, self.interface_principal.list_input
	    #los cambios en la navfac afectan a las citas y referencias por eso no se actualizan sus check
	    self.calcula_princ(self.list_input)
	    self.request.form.update()
	    return self.template()

	if  self.submitted_citation:
	    self.calcula_princ(self.list_input)
	    self.calcula_reference(self.list_input_reference)
	    self.list_input_citation = self.list_input_citation.union(self.request.form.get('citation',''))
	    self.calcula_citation(self.list_input_citation)
	    self.request.form.update()
	    return self.template()


	if  self.submitted_reference:
	    self.calcula_princ(self.list_input)
	    self.calcula_citation(self.list_input_citation)
	    self.list_input_reference=self.list_input_reference.union(self.request.form.get('reference',''))
	    self.calcula_reference(self.list_input_reference)
	    self.request.form.update()
	    return self.template()
        
 	    
	

        return self.template()
        # send_button = form.get('form.button.Send', None) is not None
    def indice_h(self):
	return self.interface_principal.indice_h()
    def indice_i10(self):
	return self.interface_principal.indice_i10() 

    def list_input(self):
	return sorted(self.list_input)

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
##########################################################################
    def list_input_citation(self):
	return sorted(self.list_input_citation)

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
###########################################################################
    def list_input_reference(self):
	return sorted(self.list_input_reference)

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
