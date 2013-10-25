# -*- coding: utf-8 -*-
from matem.facetedbibliography.modules import interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import os
from Products.Five import BrowserView
from sets import Set
from bibliograph.rendering.interfaces import IBibliographyRenderer
from zope import component
from Products.CMFCore.utils import getToolByName

class FacetedView(BrowserView):

    template = ViewPageTemplateFile('faceted_view.pt')

    def __init__(self,context,request):
    	self.context = context
    	self.request = request
        curpath = os.path.abspath(os.curdir)
        self.output_encoding = self.request.get('output_encoding', 'utf-8')
        self.eol_style = self.request.get('eol_style', 0)


	self.researchers_file = self.context['investigadores'].getFile().getBlob()
	self.renderer =  self._getRenderer(self.context)

    
	#*******************************************************************************************
	pub = self.renderer.render(self.context['publicaciones'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	#bib_file.write(pub)
	#bib_file.seek(0)
	self.interface_principal = interface.interface(self.researchers_file, pub)    
	pub=''
	#*******************************************************************************************
	#self.bib_file_cit = open('archivo1.bib','wb+')
	self.cit =self.renderer.render(self.context['citas'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	#self.bib_file_cit.write(cit)
	#self.bib_file_cit.seek(0)
        self.interface_citation = interface.interface(self.researchers_file , self.cit)
	#*******************************************************************************************
	#self.bib_file_ref = open('archivo2.bib','wb+')
	self.ref = self.renderer.render(self.context['referencias'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	#self.bib_file_ref.write(ref)
	#self.bib_file_ref.seek(0)
        self.interface_reference = interface.interface(self.researchers_file, self.ref)
	#*******************************************************************************************

	self.interface_principal.ini_listas()
        self.list_c = self.interface_principal.list_citation #objetos
        self.list_r = self.interface_principal.list_reference #objetos

        self.interface_citation.tree.poda_arbol(self.list_c)
        self.interface_reference.tree.poda_arbol(self.list_r)

	self.tree_citation = self.interface_citation.tree.G
	self.tree_reference = self.interface_reference.tree.G

        self.interface_citation.ini_listas()
        self.interface_reference.ini_listas()
        
        
	#*******************************************************************************************

    	self.submitted_faceta = self.request.form.get('faceta', False)
    	self.submitted_button = self.request.form.get('clear', False)
    	
	
    	self.list_input = Set([])
    	self.list_input_citation = Set([])
    	self.list_input_reference  = Set([])    

    def _getRenderer(self,context):
	# see Products/CMFBibliographyAT/browser/export.py
	#getAllUtilitiesRegisteredFor ( interface, context=None )
        utils = component.getAllUtilitiesRegisteredFor(IBibliographyRenderer,context)
        for renderer in utils:
            if renderer.available and renderer.enabled:
                    return renderer
        return None

	
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
        #print "get_list_objs"    
        if not self.interface_principal.compare(self.list_c, self.interface_principal.list_citation):
	       
               self.list_c = self.interface_principal.list_citation
	       #*******************************
               #self.interface_citation.tree.construir_arbol(self.researchers_file, self.cit)
	       self.interface_citation.tree.G = self.tree_citation
	       #*******************************
               self.interface_citation.tree.poda_arbol(self.list_c)
               self.interface_citation.ini_listas()
	       #print "const cit"
        if not self.interface_principal.compare(self.list_r, self.interface_principal.list_reference):
               self.list_r = self.interface_principal.list_reference
	       #*******************************
               #self.interface_reference.tree.construir_arbol(self.researchers_file, self.ref)
	       self.interface_reference.tree.G = self.tree_reference
	       #*******************************
               self.interface_reference.tree.poda_arbol(self.list_r)
               self.interface_reference.ini_listas()
	       #print "const ref"
    def calcula_citation(self, list_input_citation):
        
    	self.list_input_citation = list_input_citation
    	self.interface_citation.get_list_objects(self.list_input_citation)

    def calcula_reference(self,list_input_reference):
        
    	self.list_input_reference = list_input_reference 
    	self.interface_reference.get_list_objects(self.list_input_reference)

    def update(self):
	
    	self.submitted_faceta =self.request.form.get('faceta','')
	
    def __call__(self):

        self.list_input = Set([])
        self.list_input_citation = Set([])
        self.list_input_reference  = Set([])

    	if  self.submitted_faceta:
    	    list_a = self.request.form.get('faceta','')
    	    self.listas(list_a)


	    if self.list_input.__len__()>0:
		    #print "princ"
	    	    self.calcula_princ(self.list_input)
    		    self.calcula_citation(self.list_input_citation)
	    	    self.calcula_reference(self.list_input_reference)
    		    self.request.form.update()
	    	    return self.template()
    
    	    if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()>0:
		    #print "cit ref"
	    	    self.calcula_citation(self.list_input_citation)
    		    self.calcula_reference(self.list_input_reference)
	    	    self.request.form.update()
    		    return self.template()
    
            if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()<=0:
                    #print "cit"
                    self.calcula_citation(self.list_input_citation)
                    self.request.form.update()
                    return self.template()

    	    if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()<=0 and self.list_input_reference.__len__()>0:
	    	   #print "ref"
    	     	   self.calcula_reference(self.list_input_reference)
    	    	   self.request.form.update()
    	    	   return self.template()
 	return self.template()
       
        
    def indice_h(self):
        return self.interface_principal.indice_h()
	
    def indice_i10(self):
        return self.interface_principal.indice_i10() 

    def show_years(self):
	j=False
	list_ij =Set([])
	for i in self.interface_principal.list_year:		
		if i in self.interface_principal.list_val_year:
			j=True
		else:
			j=False
		tupl = (i,j)
		list_ij.add(tupl)
        return sorted(list_ij)

    def show_authors(self):
        j=False
        list_ij =Set([])
        for i in self.interface_principal.list_author:
                if i in self.interface_principal.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)

#	return sorted(self.interface_principal.list_author)

    def show_types(self):
        j=False
        list_ij =Set([])
        for i in self.interface_principal.list_type:
                if i in self.interface_principal.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)

#	return sorted(self.interface_principal.list_type)

    def show_journals(self):
        j=False
        list_ij =Set([])
        for i in self.interface_principal.list_journal:
                if i in self.interface_principal.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)

#	return sorted(self.interface_principal.list_journal)

    def show_collaborators(self):
        j=False
        list_ij =Set([])
        for i in self.interface_principal.list_collaborator:
                if i in self.interface_principal.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)

#	return sorted(self.interface_principal.list_collaborator)
	
    def show_pub(self):
	return sorted(self.interface_principal.return_list_objs())
	
    def show_list_input(self):
	return sorted(self.list_input)
	

#
##########################################################################

    def show_years_cit(self):
        j=False
        list_ij =Set([])
        for i in self.interface_citation.list_year:
                if i in self.interface_citation.list_val_year:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)

#        return sorted(self.interface_citation.list_year)

    def show_authors_cit(self):
        j=False
        list_ij =Set([])
        for i in self.interface_citation.list_author:
                if i in self.interface_citation.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_citation.list_author)

    def show_types_cit(self):
        j=False
        list_ij =Set([])
        for i in self.interface_citation.list_type:
                if i in self.interface_citation.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_citation.list_type)

    def show_journals_cit(self):
        j=False
        list_ij =Set([])
        for i in self.interface_citation.list_journal:
                if i in self.interface_citation.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_citation.list_journal)

    def show_collaborators_cit(self):
        j=False
        list_ij =Set([])
        for i in self.interface_citation.list_collaborator:
                if i in self.interface_citation.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_citation.list_collaborator)

    def show_pub_cit(self):
	return sorted(self.interface_citation.return_list_objs())

    def show_list_input_citation(self):
	return sorted(self.list_input_citation)


	
    ###########################################################################

    def show_years_ref(self):
        j=False
        list_ij =Set([])
        for i in self.interface_reference.list_year:
                if i in self.interface_reference.list_val_year:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#        return sorted(self.interface_reference.list_year)

    def show_authors_ref(self):
        j=False
        list_ij =Set([])
        for i in self.interface_reference.list_author:
                if i in self.interface_reference.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_reference.list_author)

    def show_types_ref(self):
        j=False
        list_ij =Set([])
        for i in self.interface_reference.list_type:
                if i in self.interface_reference.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_reference.list_type)

    def show_journals_ref(self):
        j=False
        list_ij =Set([])
        for i in self.interface_reference.list_journal:
                if i in self.interface_reference.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_reference.list_journal)

    def show_collaborators_ref(self):
        j=False
        list_ij =Set([])
        for i in self.interface_reference.list_collaborator:
                if i in self.interface_reference.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j)
                list_ij.add(tupl)
        return sorted(list_ij)
#	return sorted(self.interface_reference.list_collaborator)

    def show_pub_ref(self):
	return sorted(self.interface_reference.return_list_objs())

    def show_list_input_reference(self):
	return sorted(self.list_input_reference)
	

