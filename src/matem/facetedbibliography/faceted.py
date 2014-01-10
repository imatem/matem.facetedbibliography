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
#	self.renderer =  self._getRenderer(self.context)

	#*******************************************************************************************
	print "ini get pub"
#	pub = self.renderer.render(self.context['publicaciones'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	pub= self.context['file2'].getFile().getBlob()
	print "fin get pub"
	print "start build tax principal"
	self.interface_principal = interface.interface(self.researchers_file, pub)    
	print "end build tax principal"
	print "start build tax aux principal"
	self.interface_principal_aux = interface.interface(self.researchers_file, pub)    
	print "end build tax aux principal"
	pub=''
	#*******************************************************************************************
	print "ini get cit"
#	self.cit =self.renderer.render(self.context['citas'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	self.cit= self.context['file1'].getFile().getBlob()
	print "end get cit"
	print "start build tax cit"
        self.interface_citation = interface.interface(self.researchers_file , self.cit)
	print "end build tax cit"
	print "start build tax aux cit"
        self.interface_citation_aux = interface.interface(self.researchers_file , self.cit)
	print "start end tax aux cit"
	#*******************************************************************************************
	print "ini get ref"
#	self.ref = self.renderer.render(self.context['referencias'], output_encoding=self.output_encoding, msdos_eol_style=self.eol_style)
	self.ref= self.context['file3'].getFile().getBlob()
	print "fin get ref"
	print "start build tax ref"
        self.interface_reference = interface.interface(self.researchers_file, self.ref)
	print "end build tax ref"
	print "start build tax aux ref"
        self.interface_reference_aux = interface.interface(self.researchers_file, self.ref)
	print "end build tax aux ref"
	#*******************************************************************************************

	self.interface_principal.ini_listas()
        self.list_c = self.interface_principal.list_citation #ids
        self.list_r = self.interface_principal.list_reference #ids
	self.list_princ= Set([])
	self.list_cit= Set([])
	self.list_ref= Set([])

        self.interface_citation.tree.poda_arbol(self.list_c)
        self.interface_reference.tree.poda_arbol(self.list_r)

        self.interface_citation_aux.tree.poda_arbol(self.list_c)
        self.interface_reference_aux.tree.poda_arbol(self.list_r)

	self.tree_citation = self.interface_citation.tree.G
	self.tree_reference = self.interface_reference.tree.G
        self.interface_citation.ini_listas()
        self.interface_reference.ini_listas()
	#*******************************************************************************************

    	self.submitted_faceta = self.request.form.get('faceta', False)
    	self.submitted_publication = self.request.form.get('publication', False)
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

	
    def listas_a(self, lista_mix):
        for item in lista_mix:
                if not "+" in item:
                        self.list_input.add(item) 
                elif "+c" in item:
                        string = item.replace("+c",'')
                        self.list_input_citation.add(string)                       
                elif "+r" in item:
                        string = item.replace("+r",'')
                        self.list_input_reference.add(string)
    def publication_select(self,list_pub):
        for item in list_pub:
                if   "+p" in item:
                        string = item.replace("+p",'')
                        self.list_princ.add(string)                       
                elif "+x" in item:
                        string = item.replace("+x",'')
                        self.list_cit.add(string)                       
                elif "+y" in item:
                        string = item.replace("+y",'')
                        self.list_ref.add(string)
        
    def calcula_princ(self,list_input):
	
	self.list_input = list_input
	self.interface_principal.get_list_objects(self.list_input)
	if not self.interface_principal.compare(self.list_c, self.interface_principal.list_citation)  :
	       
               	self.list_c = self.interface_principal.list_citation
	       	self.interface_citation.tree.G = self.tree_citation
               	self.interface_citation.tree.poda_arbol(self.list_c)
               	self.interface_citation.ini_listas()
        if not self.interface_principal.compare(self.list_r, self.interface_principal.list_reference) :
               	self.list_r = self.interface_principal.list_reference
	       	self.interface_reference.tree.G = self.tree_reference
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
    	self.submitted_publication =self.request.form.get('publication','')
	
    def __call__(self):


        self.list_input = Set([])
        self.list_input_citation = Set([])
        self.list_input_reference  = Set([])
    	list_fac = self.request.form.get('faceta','')
    	list_pub = self.request.form.get('publication','')
#	print list_fac
#	print list_pub	
    	self.listas_a(list_fac)
	self.publication_select(list_pub)
	print 'Objs Publication: ', self.list_princ, self.list_cit, self.list_ref
	print '\nFacetas select: ', self.list_input, self.list_input_citation, self.list_input_reference
    	if  self.submitted_faceta or  self.submitted_publication:
	    self.select_publications()
    
            if self.list_input.__len__()>0 and self.list_input_citation.__len__()<=0 and self.list_input_reference.__len__()<=0:
		    print "princ 100"
		    self.calcula_princ(self.list_input)

	    if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()>0:
		    print "cit ref 011"
		    self.calcula_citation(self.list_input_citation)

		    list_ref_princ= self.interface_citation.list_reference

		    self.calcula_reference(self.list_input_reference)
		    list_cit_princ= self.interface_reference.list_citation

		    list_result=Set(list_ref_princ).intersection(Set(list_cit_princ))

		    self.interface_principal.tree.poda_arbol(sorted(list_result))
		    self.interface_principal.get_list_objects(self.list_input)
		    self.calcula_reference(self.list_input_reference)
		    self.calcula_citation(self.list_input_citation)
	
	    if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()<=0:
		    print "cit 010"
                    self.calcula_citation(self.list_input_citation)

	       	    list_ref_princ= self.interface_citation.list_reference
		    self.interface_principal.tree.poda_arbol(list_ref_princ)
               	    self.interface_principal.ini_listas()

               	    self.list_r = self.interface_principal.list_reference
	            self.interface_reference.tree.G = self.tree_reference
               	    self.interface_reference.tree.poda_arbol(self.list_r)
               	    self.interface_reference.ini_listas()

            if  self.list_input.__len__()<=0 and self.list_input_citation.__len__()<=0 and self.list_input_reference.__len__()>0:
                    print "ref 001"
                    self.calcula_reference(self.list_input_reference)
	       	    list_cit_princ= self.interface_reference.list_citation

		    self.interface_principal.tree.poda_arbol(list_cit_princ)
               	    self.interface_principal.ini_listas()

               	    self.list_c = self.interface_principal.list_citation
	            self.interface_citation.tree.G = self.tree_citation
               	    self.interface_citation.tree.poda_arbol(self.list_c)
               	    self.interface_citation.ini_listas()

	    if  self.list_input.__len__()>0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()<=0:
  	 
		    print "princ cit 110" 
        	    self.interface_principal.get_list_objects(self.list_input)

                    self.calcula_citation(self.list_input_citation)

	       	    list_ref_princ= self.interface_citation.list_reference
	       	    list_cit = self.interface_principal.list_citation
	
		    list_result_princ=Set(self.interface_principal.list_objs).intersection(Set(list_ref_princ))
		    list_result_cit =Set(self.interface_citation.list_objs).intersection(Set(list_cit))

		    self.interface_principal.list_objs=sorted(list_result_princ)
		    self.interface_principal.related_concepts()

		    self.interface_citation.list_objs=sorted(list_result_cit)
		    self.interface_citation.related_concepts()
		    
	            self.list_r = self.interface_principal.list_reference #ids
	            self.interface_reference.tree.poda_arbol(self.list_r)
               	    self.interface_reference.ini_listas()

	    if  self.list_input.__len__()>0 and self.list_input_citation.__len__()<=0 and self.list_input_reference.__len__()>0:
		    print "princ ref 101" 
 
                    self.interface_principal.get_list_objects(self.list_input)

                    self.calcula_reference(self.list_input_reference)

                    list_cit_princ= self.interface_reference.list_citation
                    list_ref = self.interface_principal.list_reference

                    list_result_princ=Set(self.interface_principal.list_objs).intersection(Set(list_cit_princ))
                    list_result_ref =Set(self.interface_reference.list_objs).intersection(Set(list_ref))

                    self.interface_principal.list_objs=sorted(list_result_princ)
		    self.interface_principal.related_concepts()
                    self.interface_reference.list_objs=sorted(list_result_ref)
		    self.interface_reference.related_concepts()

                    self.list_c = self.interface_principal.list_citation #ids

                    self.interface_citation.tree.poda_arbol(self.list_c)
                    self.interface_citation.ini_listas()

	    if  self.list_input.__len__()>0 and self.list_input_citation.__len__()>0 and self.list_input_reference.__len__()>0:
		    print "all 111" 
                    self.interface_principal.get_list_objects(self.list_input)
                    self.calcula_citation(self.list_input_citation)

                    list_ref_princ= self.interface_citation.list_reference

                    self.calcula_reference(self.list_input_reference)

                    list_cit_princ= self.interface_reference.list_citation

		    list_objs=self.interface_principal.list_objs

                    list_result=Set(list_ref_princ).intersection(Set(list_cit_princ)).intersection(list_objs)

		    self.interface_principal.tree.poda_arbol(sorted(list_result))
                    self.calcula_princ(self.list_input)
                    self.calcula_reference(self.list_input_reference)
                    self.calcula_citation(self.list_input_citation)
	print "ini update template"
	self.request.form.update()
	print "end up/start return template"
 	return self.template()

    def select_publications(self):
#**********************************************************************************************************
	    list_princ= self.list_princ
	    list_cit =  self.list_cit 
	    list_ref =  self.list_ref
	    if(self.list_princ.__len__()>0):

			self.list_princ=Set(self.interface_principal.list_objs).intersection(Set(self.list_princ))
			if self.list_cit.__len__()>0:
				self.list_cit=Set(self.interface_citation.list_objs).intersection(Set(self.list_cit))
				self.interface_citation.list_objs=sorted(self.list_cit)
				self.interface_citation.related_concepts()

				if self.list_ref.__len__()>0:
					print "111"
					self.list_ref=Set(self.interface_reference.list_objs).intersection(Set(self.list_ref))
					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

					self.list_princ=Set(self.interface_reference.list_citation).intersection(Set(self.interface_citation.list_reference).intersection(Set(self.list_princ)))

					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_cit=Set(self.list_cit).intersection(Set(self.interface_principal.list_citation))
					self.list_ref=Set(self.list_ref).intersection(Set(self.interface_principal.list_reference))

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
				else:
					print "110"
					self.list_princ=Set(self.interface_citation.list_reference).intersection(Set(self.list_princ))
					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_cit=Set(self.list_cit).intersection(Set(self.interface_principal.list_citation))
					self.list_ref = self.interface_principal.list_reference

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
			else:
				if self.list_ref.__len__()>0:
					print "101"
					self.list_ref=Set(self.interface_reference.list_objs).intersection(Set(self.list_ref))
					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

					self.list_princ=Set(self.interface_reference.list_citation).intersection(Set(self.list_princ))
					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_cit = self.interface_principal.list_citation

					self.list_ref=Set(self.list_ref).intersection(Set(self.interface_principal.list_reference))
					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
				else:
					print "100"

					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_ref = self.interface_principal.list_reference
					self.list_cit = self.interface_principal.list_citation

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()
				
				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
	    else:
	    #***********************************************************************************
			self.list_princ=self.interface_principal.list_objs
			if self.list_cit.__len__()>0:
				self.list_cit=Set(self.interface_citation.list_objs).intersection(Set(self.list_cit))
				self.interface_citation.list_objs=sorted(self.list_cit)
				self.interface_citation.related_concepts()

				if self.list_ref.__len__()>0:
					print "011"
					self.list_ref=Set(self.interface_reference.list_objs).intersection(Set(self.list_ref))
					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

					self.list_princ=Set(self.interface_reference.list_citation).intersection(Set(self.interface_citation.list_reference).intersection(Set(self.list_princ)))

					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_cit=Set(self.list_cit).intersection(Set(self.interface_principal.list_citation))
					self.list_ref=Set(self.list_ref).intersection(Set(self.interface_principal.list_reference))

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
				else:
					print "010"
					self.list_princ=Set(self.interface_citation.list_reference).intersection(Set(self.list_princ))
					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()

					self.list_cit=Set(self.list_cit).intersection(Set(self.interface_principal.list_citation))
					self.list_ref = self.interface_principal.list_reference

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
			else:
				if self.list_ref.__len__()>0:
					print "001"
					self.list_ref=Set(self.interface_reference.list_objs).intersection(Set(self.list_ref))
					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

					self.list_princ=Set(self.interface_reference.list_citation).intersection(Set(self.list_princ))
					self.interface_principal.list_objs=sorted(self.list_princ)
					self.interface_principal.related_concepts()


					self.list_cit = self.interface_principal.list_citation
					self.list_ref=Set(self.list_ref).intersection(Set(self.interface_principal.list_reference))

					self.interface_citation.list_objs=sorted(self.list_cit)
					self.interface_citation.related_concepts()

					self.interface_reference.list_objs=sorted(self.list_ref)
					self.interface_reference.related_concepts()

				        self.interface_principal.tree.poda_arbol(self.list_princ)
	    				self.interface_principal.ini_listas()
	    				self.interface_citation.tree.poda_arbol(self.list_cit)
	    				self.interface_citation.ini_listas()
	    				self.interface_reference.tree.poda_arbol(self.list_ref)
	    				self.interface_reference.ini_listas()
	    self.list_princ= list_princ
	    self.list_cit =  list_cit 
	    self.list_ref =  list_ref
#**********************************************************************************************************
       
        
    def indice_h(self):
        return self.interface_principal_aux.indice_h()
	
    def indice_i10(self):
        return self.interface_principal_aux.indice_i10() 

    def show_years(self):
	j=False
	list_ij =[]
	k=0
	list_a= sorted(self.interface_principal.list_year, reverse=True)
	for i in list_a:		
		if i in self.interface_principal.list_val_year:
			j=True
		else:
			j=False
		tupl = (i,j,k)
		list_ij.append(tupl)
		k=k+1
        return  list_ij

    def show_authors(self):
        j=False
        list_ij =[]
	k=0
	list_a= sorted(self.interface_principal.list_author)
        for i in list_a:
                if i in self.interface_principal.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_types(self):
        j=False
        list_ij = []
	k=0
	list_a=sorted(self.interface_principal.list_type)
        for i in list_a:
                if i in self.interface_principal.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_journals(self):
        j=False
        list_ij =[]
	k=0
	list_a=sorted(self.interface_principal.list_journal)
        for i in list_a:
                if i in self.interface_principal.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_collaborators(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_principal.list_collaborator)
        for i in list_a:
                if i in self.interface_principal.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij
	
    def show_pub(self):
	list_pub= self.interface_principal.return_list_objs()
	list_final=[]
	for item in  list_pub:
		list_a=item.split('%%')	
		list_b=list_a[6].split(',')
		list_c=list_a[7].split(',')
		list_2b=[]
		list_2c=[]
		for i in list_b:
			idc=i.strip()
			if idc.__len__()>0 and self.interface_citation_aux.tree.G.has_node(idc):
				obj=  self.interface_citation_aux.tree.G.node[idc]['data']
				str_b= idc +';;'+ obj.title
				list_2b.append(str_b)
				
		for i in list_c:
			idc=i.strip()
			if idc.__len__()>0 and self.interface_reference_aux.tree.G.has_node(idc):
				obj= self.interface_reference_aux.tree.G.node[idc]['data']
				str_c= idc +';;'+ obj.title
				list_2c.append(str_c)
	
#		print 'PRINC ', list_a[0], list_a[1], list_a[2], list_a[3], list_a[4], list_a[5]
		list_a[6]=',,'.join(list_2b)
		list_a[7]=',,'.join(list_2c)
		str_final='%%'.join(list_a)
		list_final.append(str_final)
	
	return list_final

    def show_num_pub(self):
	list_pub= self.interface_principal.return_list_objs()
	return  filter(None, list_pub).__len__()
	
    def show_list_princ(self):
	return sorted(self.list_princ)

    def show_list_input(self):
	return sorted(self.list_input)
	
    def get_url(self):
	return self.context.absolute_url_path()
	
    def get_url_ref(self):
	return self.context['referencias'].absolute_url_path()

    def get_url_cit(self):
	return self.context['citas'].absolute_url_path()

    def get_url_pub(self):
	return self.context['publicaciones'].absolute_url_path()

#
##########################################################################
    def show_list_cit(self):
	return sorted(self.list_cit)

    def show_years_cit(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_citation.list_year, reverse=True)
        for i in list_a:
                if i in self.interface_citation.list_val_year:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_authors_cit(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_citation.list_author)
        for i in list_a:
                if i in self.interface_citation.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_types_cit(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_citation.list_type)
        for i in list_a:
                if i in self.interface_citation.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_journals_cit(self):
        j=False
	k=0
        list_ij =[]
	list_a= sorted(self.interface_citation.list_journal)
        for i in list_a:
                if i in self.interface_citation.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_collaborators_cit(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_citation.list_collaborator)
        for i in list_a:
                if i in self.interface_citation.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_pub_cit(self):
        list_pub= self.interface_citation.return_list_objs()
        list_final=[]
        for item in  list_pub:
                list_a=item.split('%%')
                list_c=list_a[7].split(',')#ref
                list_2c=[]
		#print list_c
                for i in list_c:
                        idc=i.strip()
                        if idc.__len__()>0 and self.interface_principal_aux.tree.G.has_node(idc):
                                obj= self.interface_principal_aux.tree.G.node[idc]['data']
                                str_c= idc +';;'+ obj.title
				
                                list_2c.append(str_c)
		#print list_2c
#		print 'CIT: ', list_a[0], list_a[1], list_a[2], list_a[3], list_a[4], list_a[5]
                list_a[7]=',,'.join(list_2c)
                str_final='%%'.join(list_a)
                list_final.append(str_final)
        return list_final

    def show_list_input_citation(self):
	return sorted(self.list_input_citation)

    def show_num_cit(self):
	list_pub= self.interface_citation.return_list_objs()
	return [x for x in list_pub if x].__len__()

	
    ###########################################################################
    def show_list_ref(self):
	return sorted(self.list_ref)

    def show_years_ref(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_reference.list_year, reverse=True)
        for i in list_a:
                if i in self.interface_reference.list_val_year:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_authors_ref(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_reference.list_author)
        for i in list_a:
                if i in self.interface_reference.list_val_author:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_types_ref(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_reference.list_type)
        for i in list_a:
                if i in self.interface_reference.list_val_type:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_journals_ref(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_reference.list_journal)
        for i in list_a:
                if i in self.interface_reference.list_val_journal:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_collaborators_ref(self):
        j=False
	k=0
        list_ij =[]
	list_a=sorted(self.interface_reference.list_collaborator)
        for i in list_a:
                if i in self.interface_reference.list_val_collaborator:
                        j=True
                else:
                        j=False
                tupl = (i,j,k)
                list_ij.append(tupl)
		k=k+1
        return list_ij

    def show_pub_ref(self):
        list_pub= self.interface_reference.return_list_objs()
        list_final=[]
        for item in  list_pub:
                list_a=item.split('%%')
                list_b=list_a[6].split(',')#cit
                list_2b=[]
                for i in list_b:
                        idc=i.strip()
                        if idc.__len__()>0 and self.interface_principal_aux.tree.G.has_node(idc):
                                obj=  self.interface_principal_aux.tree.G.node[idc]['data']
                                str_b= idc +';;'+ obj.title
                                list_2b.append(str_b)
                list_a[6]=',,'.join(list_2b)
                str_final='%%'.join(list_a)
                list_final.append(str_final)
#		print 'REF: ',list_a[0], list_a[1], list_a[2], list_a[3], list_a[4], list_a[5]
        return list_final

    def show_list_input_reference(self):
	return sorted(self.list_input_reference)
	
    def show_num_ref(self):
	list_pub= self.interface_reference.return_list_objs()
	return [x for x in list_pub if x].__len__()

