#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#           
#  Copyright 2015 tavares <tavares@tavares-Dev>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
#

import sys
import os
import wx
import socket  
from subprocess import call
import math
import cmath
import time
import traceback
from math import pi, sin, cos, log, sqrt, atan2

#imports para internacionalizacao
import gettext
import __builtin__
__builtin__.__dict__['_'] = wx.GetTranslation


#imports para execução de projetos
import transistorAmp
import valoresPadroes
import ampOpDesign
import ampOpInversor
import ampOpNaoInversor


class aboutDlg(wx.Dialog):

	def __init__(self):
			
		wx.Dialog.__init__(self, None, -1, _('About Cadele'),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer10 = wx.BoxSizer(wx.VERTICAL);
		self.sizer11 = wx.BoxSizer(wx.VERTICAL);
		self.sizer12 = wx.BoxSizer(wx.VERTICAL);
		self.sizer13 = wx.BoxSizer(wx.VERTICAL);
		self.sizer14 = wx.BoxSizer(wx.VERTICAL);
		self.sizer15 = wx.BoxSizer(wx.VERTICAL);	

		self.staticTxtTitulo= wx.StaticText(self, -1, _("About Cadele"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer1.Add(self.staticTxtTitulo, flag= wx.ALIGN_CENTER_HORIZONTAL)        
		
		
		
		self.texto= _("Version: 15.09 dev- date: 2015/09/10")
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= _("Implement low gain ( < 10) transistor amplifier design")
		self.static2= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static2,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        
 
 		self.texto= _("Version: 15.11 dev- date: 2015/11/15")
		self.static3= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static3,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= _("Implement OpAmp inverter amplifier design")
		self.static4= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static4,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)  
    

		self.texto= _("Version: 15.11a dev- date: 2015/11/25")
		self.static3= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static3,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= _("Implement OpAmp non inverter amplifier design")
		self.static4= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static4,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)  
					
		self.texto= _("Author: Roberto Tavares")
		self.static5= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static5,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)   
		

		self.texto= _("For detailed information or author contact:www.cadernodelaboratorio.com.br")
		self.static6= wx.StaticText(self, -1, self.texto)   
		self.sizer10.Add(self.static6,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)     


		
		
		self.okButton= wx.Button(self, wx.ID_OK, _("CLOSE"))	#objeto botao OK
		self.sizer11.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		
		
		
		
		#montagem da estrutura de sizers
		self.sizer1.Add(self.sizer10,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer1.Add(self.sizer11,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
				
				
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()



						
class MyFrame(wx.Frame):
	def __init__(self):
				
		wx.Frame.__init__(self, None, -1, "CADELE 15.11a dev", size=(600, 200))
				
		"""
		tradução das mensagens
		"""
		
		self.mylocale = wx.Locale()
		self.mylocale.AddCatalogLookupPathPrefix('.')
		self.mylocale.AddCatalog('pt_BR')
		
		
		
		"""
		implementação dos menus
		"""
		
		menuBar = wx.MenuBar()      #cria uma barra de menus
		
		fileMenu = wx.Menu()            #cria um novo menu, chamado de fileMenu
		mnuSair = fileMenu.Append(-1, _("Exit"), _("Close program"))  #cria o item de menu que irá provocar a saída do programa
		
		self.Bind(wx.EVT_MENU, self.OnExit, mnuSair)    #associa  evento que será gerado ao se clicar sobre o menu SAIR ao método OnExit
		
	
		helpMenu = wx.Menu()            #cria menu help
		mnuAbout = helpMenu.Append(-1, _("About"), _("Basic info about program"))  #cria o item de menu que irá provocar a saída do programa	
		self.Bind(wx.EVT_MENU, self.OnAbout, mnuAbout)    #associa  evento que será gerado ao se clicar sobre o menu SAIR ao método OnExit	
	
	
		
		menuBar.Append(fileMenu, _("File"))   #adiciona o menu fileMenu na barra de menus
		menuBar.Append(helpMenu, _("Help"))   #adiciona o menu helpMenu na barra de menus
		self.SetMenuBar(menuBar)     #associa a barra de menus ao frame  MyFrame
		
		
		
		"""
		impĺementação do painel principal
		"""
		self.panel= wx.Panel(self)
		bSizer1 = wx.BoxSizer( wx.VERTICAL )   # o painel principal será composto de um sizer vertical com tres elementos
		
		#staticTextTitulo é um texto statico que contem o titulo
		self.panel.staticTextTitulo = wx.StaticText( self.panel, wx.ID_ANY, "Cadele 15.11a", wx.DefaultPosition, wx.DefaultSize,0 )

		self.panel.staticTextTitulo.SetFont( wx.Font( 16, 74, 90, 92, False, "Sans" ) )
		bSizer1.Add(self.panel.staticTextTitulo, 0, wx.ALIGN_CENTER | wx.ALL, 1 )
		
		#no sizer 2 inserimos botoes para projetos diversos
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL)   # o painel principal será composto de um sizer vertical com tres elementos
		
		#inserimos os botoes que chamam os diferentes scripts de projeto
		#criamos o botão de proejto amplificadores transistorizados e o adicionamos ao sizer 2
		self.panel.btnAmplificadoresT = wx.Button( self.panel, wx.ID_ANY, _("BJT Amplifiers design"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.panel.btnAmplificadoresT, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		
		self.panel.btnAmplificadorOperacional = wx.Button( self.panel, wx.ID_ANY, _("Amp Op Design"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.panel.btnAmplificadorOperacional, 0, wx.ALIGN_CENTER | wx.ALL, 10 ) 

				
		
		#inserimos o sizer bSizer2 no sizer vertical principal, com flag ajustado para centralizar 
		bSizer1.Add( bSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL)
		#associamos o sizer principal ao painel
		self.panel.SetSizer (bSizer1)
		self.panel.Layout() #traçamos a interface
		
		
		# Associamos os botões aos processos corrrespodentes
		self.panel.btnAmplificadoresT.Bind( wx.EVT_BUTTON, self.OnSelAmplifier)
		self.panel.btnAmplificadorOperacional.Bind( wx.EVT_BUTTON, self.OnSelAmplificadorOperacional)

	def OnAbout(self,event):
		self.aboutDlg = aboutDlg()      #cria um dialogo de solicitacao de IP
		result = self.aboutDlg.ShowModal() 		
		self.aboutDlg.Destroy()
		
	def OnExit(self, event):   #ao se clicar sobre o menu mnuSair, ese método é chamado e fecha o programa
		self.Close()




	def OnSelAmplificadorOperacional(self,event):
		
		self.dialogo = ampOpDesign.SelAmpOpDesign()      #cria um dialogo de solicitacao de IP
		
		self.result = self.dialogo.ShowModal() 

				
		if self.result == wx.ID_OK:  
			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_INVERSOR:
				 ampOpInversor.ampOpInverterAmplifierDesign()
				 
				
			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_NAO_INVERSOR:
				ampOpNaoInversor.ampOpNoInverterAmplifierDesign()				
				
			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_DE_CORRENTE:
				print _("current to be implemented")	
			
			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_DE_TRANSCONDUTANCIA:
				print _("transcondutance to be implemented")	

			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_INVERSOR_AC:
				print _("ac inverter to be implemented")				
			
			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_SENSIVEL__CARGA:
				print _("charge to be implemented")	

			if self.dialogo.GetSelection() == ampOpDesign.BTN_AMPLIFICADOR_SOMADOR:
				print _("adder to be implemented")	


			
		self.dialogo.Destroy()




	def OnSelAmplifier(self,event):
		
		self.dialogo = transistorAmp.SelAmplifiersDesign()      #cria um dialogo de solicitacao de IP
		
		self.result = self.dialogo.ShowModal() 
				
		if self.result == wx.ID_OK:  
			if self.dialogo.GetSelection() == transistorAmp.BTN_AMPLIFIER_TR_G_1_10:
				self.dialogo1 = transistorAmp.entradaAmplificadorTransistorizado()
				self.result1= self.dialogo1.ShowModal()
				
				if self.result1 == wx.ID_OK:	
					self.Vg=        float(self.dialogo1.GetVg())
					self.rlTxt=     float(self.dialogo1.GetRL())
					self.ecmTxt = 	float(self.dialogo1.GetEcmax())
					self.tmaxTxt=   float(self.dialogo1.GetTmax())
					self.sTxt=      float(self.dialogo1.GetS())
					self.betaTxt=   float(self.dialogo1.GetBeta())
					self.dicTxt=    float(self.dialogo1.GetDeltaIc())
					self.e0ppTxt=   float(self.dialogo1.GetE0pp())
					self.cirTxt=    float(self.dialogo1.GetCir())
					self.vccTxt=    float(self.dialogo1.GetVcc())
					self.fminTxt=   float(self.dialogo1.GetFmin())
					self.icmaxTxt=  float(self.dialogo1.GetIcmax())
				
					self.design= transistorAmp.TransistorAmpDesign(self.Vg,self.rlTxt,self.ecmTxt,self.tmaxTxt,self.sTxt,self.dicTxt,self.e0ppTxt,self.betaTxt,self.vccTxt,self.fminTxt,self.icmaxTxt,False)
					
					
					self.result= self.design.calculaCircuito()
					if self.result == True:
						
						self.Re=  int(valoresPadroes.retornaValorResistor(self.design.GetRe(),5,0))
						self.Rl=  int(valoresPadroes.retornaValorResistor(self.design.GetRl(),5,0))
						self.Rb1= int(valoresPadroes.retornaValorResistor(self.design.GetRb1(),5,0)) 
						self.Rb2= int(valoresPadroes.retornaValorResistor(self.design.GetRb2(),5,0)) 
						self.Cin= int(valoresPadroes.retornaValorEletrolitico(self.design.GetCcin()*1000000.0,2))
						self.Cout= int( valoresPadroes.retornaValorEletrolitico(self.design.GetCco()*1000000.0,2))
						self.Ic= self.design.GetQic()
						self.Zin= self.design.GetZin()
						self.finalMsg= self.design.GetFinalMsg()
						
						self.dialogo2 = transistorAmp.saidaAmplificadorTransistorizado(self.Re,self.Rl,self.Rb1,self.Rb2,self.Cin,self.Cout,self.Ic,self.Zin,self.finalMsg,True)
						
						self.result2 = self.dialogo2.ShowModal() 
						
						self.dialogo2.Destroy() 
						
					else:
						self.finalMsg= self.design.GetFinalMsg()
						
						self.dialogo2 = transistorAmp.saidaAmplificadorTransistorizado(0,0,0,0,0,0,0,0,self.finalMsg,False)
						
						self.result2 = self.dialogo2.ShowModal() 
						self.dialogo2.Destroy()
				
				self.dialogo1.Destroy()
					
				
			if self.dialogo.GetSelection() == transistorAmp.BTN_AMPLIFIER_TR_G_10_50:
				print "pressionado 2"				

			if self.dialogo.GetSelection() == transistorAmp.BTN_AMPLIFIER_TR_G_50_100:
				print "pressionado 3"		

			
		self.dialogo.Destroy()

		






if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = MyFrame()
	frame.Show(True)
	app.MainLoop()



