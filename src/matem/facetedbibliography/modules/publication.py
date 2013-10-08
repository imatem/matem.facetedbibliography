'''
Created on 02/08/2013

@author: Alejandra
'''
from sets import Set

class publication:

    def __init__(self):
        
               
        self.idp    = ""
        self.title  = ""
        self.publisher= ""
        
        self.year   = ""
        self.type   = ""
        self.journal= ""
        self.author = Set([])
        self.citation = Set([])
        self.reference = Set([])