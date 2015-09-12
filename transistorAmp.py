#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  transistorAmp.py
#  
#  Copyright 2015 Roberto Tavares <roberto.tavares.filho@gmail.com>
#  
#  Versão: 0.1, em 07/09/2015
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
#  entrada= vg  ganho de tensão
#           rlw resistencia de carga
#           Ecmax tensão máxima de coletor
#			tmax  temperatura máxima de operação
#           s     fator de estabilidade
#           dIc   delta corrente quiescente
#           Eo pp tensão pico a pico de saída


import argparse
import gettext
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


#criacao dos IDs identificadores dos objetos
BTN_AMPLIFIER_TR_G_1_10 = wx.NewId()    # amplificador transistorizado  ganho 1-10 
BTN_AMPLIFIER_TR_G_10_50 = wx.NewId()
BTN_AMPLIFIER_TR_G_50_100 = wx.NewId()
ID_VG  = wx.NewId()
ID_RL  = wx.NewId()
ID_ECMAX =  wx.NewId()
ID_TMAX =  wx.NewId()
ID_S =  wx.NewId()
ID_BETA =  wx.NewId()
ID_DIC =  wx.NewId()
ID_E0PP =  wx.NewId()
ID_CIR =  wx.NewId()		
ID_VCC =  wx.NewId()
ID_FMIN =  wx.NewId()
ID_ICMAX =  wx.NewId()



def retornaDeltaVbe(fQic):
	"""
	returns delta Vbe for a given quiescent current iQc em A, delta Vbe em V/grau centigrado
	"""
	retorno= 0.003
	if fQic < 0.1:
		retorno= 0.002
	if fQic < 0.01:
		retorno= 0.0025 
	if fQic < 0.001:
		retorno= 0.00275					
	if fQic < 0.0001:
		retorno= 0.003
	return retorno

class saidaAmplificadorTransistorizado(wx.Dialog):

	"""
	Implementa a tela com os valores calculados do amplificador transistorizado
	"""
	def __init__(self,Re,Rl,Rb1,Rb2,Cin,Cout,Icq,Zin,statusMsg,status):
			
		wx.Dialog.__init__(self, None, -1, _('Amplifier values'),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer30 = wx.BoxSizer(wx.HORIZONTAL);
		
		self.sizer20 = wx.BoxSizer(wx.VERTICAL);
		self.sizer21 = wx.BoxSizer(wx.VERTICAL);
		
		self.sizer10 = wx.BoxSizer(wx.VERTICAL);
		self.sizer11 = wx.BoxSizer(wx.VERTICAL);
		self.sizer12 = wx.BoxSizer(wx.VERTICAL);
		self.sizer13 = wx.BoxSizer(wx.VERTICAL);
		self.sizer14 = wx.BoxSizer(wx.VERTICAL);
		self.sizer15 = wx.BoxSizer(wx.VERTICAL);	

		self.staticTxtTitulo= wx.StaticText(self, -1, _("Amplifier design output data"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer1.Add(self.staticTxtTitulo, flag= wx.ALIGN_CENTER_HORIZONTAL)        
		
		if status == True:
			self.texto= "Re= " + str(Re) + " ohms"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Emiter resistor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

			self.texto= "RL= " + str(Rl) + " ohms"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Colector  resistor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

			self.texto= "Rb1= " + str(Rb1) + " ohms"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Upper base resistor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        
					

			self.texto= "Rb2= " + str(Rb2) + " ohms"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Lower base resistor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)     


			self.texto= "Cin= " + str(Cin) + " microfarads"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Input capacitor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)   


			self.texto= "Cout= " + str(Cout) + " microfarads"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Output capacitor"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)   
			

			self.texto= "Zin= " + str(int(Zin)) + " ohms"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Input impedance"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10) 


			self.texto= "Icq= " + str(int(Icq * 1000)) + " miliamperes"
			self.static1= wx.StaticText(self, -1, self.texto)   
			self.static1.SetToolTipString(_("Quiescente current"))
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10) 

		else:
			self.static1= wx.StaticText(self, -1, statusMsg)   
			self.static1.SetForegroundColour((255,0,0)) # set text color
			self.sizer10.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)      
			self.static2= wx.StaticText(self, -1, _("Please change values and try again")) 
			self.static2.SetForegroundColour((255,0,0)) # set text color  
			self.sizer10.Add(self.static2,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)   



		self.okButton= wx.Button(self, wx.ID_OK, _("CLOSE"))	#objeto botao OK
		self.sizer15.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		
		
		#insere a figura com o esquema associado
		self.img1 = wx.Image("amp1.png", wx.BITMAP_TYPE_ANY)
		self.bitmap1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.img1))
		self.sizer21.Add(self.bitmap1,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
		
		
		#montagem da estrutura de sizers
		self.sizer30.Add(self.sizer20,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer30.Add(self.sizer21,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
		
		self.sizer1.Add(self.sizer30,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer1.Add(self.sizer15,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
		
		
		self.sizer20.Add(self.sizer14,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer20.Add(self.sizer13,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer20.Add(self.sizer12,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)		
		self.sizer20.Add(self.sizer10,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)         #inserimos os sizers horizontais no vertical
		self.sizer20.Add(self.sizer11,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10) 


		
				
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()



class entradaAmplificadorTransistorizado(wx.Dialog):
	"""
	Implementa a tela de entrada de parametros de projeto do amplificador transistorizado
	"""
	def __init__(self):
			
		wx.Dialog.__init__(self, None, -1, _('Amplifier Specifications'),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer10 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer11 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer12 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer13 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer14 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer15 = wx.BoxSizer(wx.HORIZONTAL);
								
		self.staticTxtTitulo= wx.StaticText(self, -1, _("Amplifier input data"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer1.Add(self.staticTxtTitulo, flag= wx.ALIGN_CENTER_HORIZONTAL)        #insere os conteudos dos sizer horizontais		
        
		self.static1= wx.StaticText(self, -1, "Vg:")  #objeto texto statico 
		self.static1.SetToolTipString(_("Amplifier gain"))
		self.vgTxt = wx.TextCtrl(self, ID_VG,'5',size=(40,20), style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static1,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.vgTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais		
		
		
		self.static2= wx.StaticText(self, -1, "RLW:")  #objeto texto statico 
		self.static2.SetToolTipString(_("Load resistence in ohms"))
		self.rlTxt = wx.TextCtrl(self, ID_RL,'10000',size=(60,20),style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static2,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.rlTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	
		

		self.static3= wx.StaticText(self, -1, "Ecmax:")  #objeto texto statico
		self.static3.SetToolTipString(_("Maximum colector voltage in volts")) 
		self.ecmTxt = wx.TextCtrl(self, ID_ECMAX,'30',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static3,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.ecmTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static4= wx.StaticText(self, -1, "Tmax:")  #objeto texto statico 
		self.static4.SetToolTipString(_("Maximum junction temperature, in celsius degrees"))
		self.tmaxTxt = wx.TextCtrl(self, ID_TMAX,'70',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static4,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.tmaxTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		self.static5= wx.StaticText(self, -1, "S:")  #objeto texto statico 
		self.static5.SetToolTipString(_("Stabilty factor, 1-10, 10 for ac coupled circuits, 2 dor DC coupled"))
		self.sTxt = wx.TextCtrl(self, ID_S,'10',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static5,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.sTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static6= wx.StaticText(self, -1, "Beta:")  #objeto texto statico 
		self.static6.SetToolTipString(_("Transistor beta parameter"))
		self.betaTxt = wx.TextCtrl(self, ID_BETA,'100',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static6,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.betaTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

				
		self.static7= wx.StaticText(self, -1, "Delta Ic:")  #objeto texto statico 
		self.static7.SetToolTipString(_("Allowable Ic current variation (%)"))
		self.dicTxt = wx.TextCtrl(self, ID_DIC,'10',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static7,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.dicTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static8= wx.StaticText(self, -1, "Eopp:")  #objeto texto statico 
		self.static8.SetToolTipString(_("Peak to peak output voltage (%)"))
		self.e0ppTxt = wx.TextCtrl(self, ID_E0PP,'2',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static8,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.e0ppTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

  

		self.static9= wx.StaticText(self, -1, "Cir:")  #objeto texto statico 
		self.static9.SetToolTipString(_("Circuit topology (1,2,or 3"))
		self.cirTxt = wx.TextCtrl(self, ID_CIR,'1',size=(30,20),style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static9,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.cirTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais  
  
  
		self.static10= wx.StaticText(self, -1, "Vcc:")  #objeto texto statico 
		self.static10.SetToolTipString(_("Battery voltage (volts)"))
		self.vccTxt = wx.TextCtrl(self, ID_VCC,'12',size=(40,20),style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static10,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.vccTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais  
    
		self.static11= wx.StaticText(self, -1, "Fmin:")  #objeto texto statico 
		self.static11.SetToolTipString(_("Minimux operational frequency (Hz)"))
		self.fminTxt = wx.TextCtrl(self, ID_FMIN,'20',size=(60,20),style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static11,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.fminTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais  
		  
		self.static12= wx.StaticText(self, -1, "Icmax:")  #objeto texto statico 
		self.static12.SetToolTipString(_("Maximum colector current (A)"))
		self.icmaxTxt = wx.TextCtrl(self, ID_ICMAX,'0.5',size=(60,20),style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static12,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.icmaxTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais   
  
  
 		self.static13= wx.StaticText(self, -1, _("For theorical explanation, please visit http://www.cadernodelaboratorio.com.br"))  #objeto texto statico 
		self.sizer14.Add(self.static13,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais 
  
  
        
		self.okButton= wx.Button(self, wx.ID_OK, "OK")	#objeto botao OK
		self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancela")	#objeto botao cancela
		self.sizer15.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		self.sizer15.Add(self.cancelButton,flag= wx.EXPAND | wx.ALL, border = 5)

		self.sizer1.Add(self.sizer13,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer1.Add(self.sizer10,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)         #inserimos os sizers horizontais no vertical
		self.sizer1.Add(self.sizer11,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL, border = 10) 
		self.sizer1.Add(self.sizer12,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer1.Add(self.sizer14,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer1.Add(self.sizer15,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
				
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()
		
	def GetVg(self):
		return self.vgTxt.GetValue()
	def GetRL(self):
		return self.rlTxt.GetValue()
	def GetEcmax(self):
		return self.ecmTxt.GetValue()
	def GetTmax(self):
		return self.tmaxTxt.GetValue()
	def GetS(self):
		return self.sTxt.GetValue()
	def GetBeta(self):
		return self.betaTxt.GetValue()
	def GetDeltaIc(self):
		return self.dicTxt.GetValue()
	def GetE0pp(self):
		return self.e0ppTxt.GetValue()
	def GetCir(self):
		return self.cirTxt.GetValue()
	def GetVcc(self):
		return self.vccTxt.GetValue()
	def GetFmin(self):
		return self.fminTxt.GetValue()
	def GetIcmax(self):
		return self.icmaxTxt.GetValue()





class SelAmplifiersDesign(wx.Dialog):
	"""
	Implementa o dialgo de seleçã da topologia do amplificador transistorizado
	"""
	def __init__(self):
			
		wx.Dialog.__init__(self, None, -1, _("Amplifier Design Selection"),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer10 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer11 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer12 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer13 = wx.BoxSizer(wx.HORIZONTAL);
		
		self.staticTxtTitulo= wx.StaticText(self, -1, _("Select the amplifier type"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer10.Add(self.staticTxtTitulo)        #insere os conteudos dos sizer horizontais
		

		self.rb1 = wx.RadioButton(self, BTN_AMPLIFIER_TR_G_1_10 , _("Circuit  gain 1-10") ,style=wx.RB_GROUP)
		#self.rb2 = wx.RadioButton(self, BTN_AMPLIFIER_TR_G_10_50 , _("Circuit gain 10-50"))
		#self.rb3 = wx.RadioButton(self, BTN_AMPLIFIER_TR_G_50_400 , _("Circuit max possible gain"))
		
		self.sizer11.Add(self.rb1,flag= wx.EXPAND | wx.ALL, border = 5)        #insere os conteudos dos sizer horizontais
		#self.sizer11.Add(self.rb2,flag= wx.EXPAND | wx.ALL, border = 5) 
		#self.sizer11.Add(self.rb3,flag= wx.EXPAND | wx.ALL, border = 5) 
		
		
		
		self.okButton= wx.Button(self, wx.ID_OK, "OK")                      #objeto botao OK
		self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancela")        #objeto botao cancela
		self.sizer13.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		self.sizer13.Add(self.cancelButton,flag= wx.EXPAND | wx.ALL, border = 5)
		
		
		self.sizer1.Add(self.sizer10,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)         #inserimos os sizers horizontais no vertical
		self.sizer1.Add(self.sizer11,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer1.Add(self.sizer12,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer1.Add(self.sizer13,flag= wx.ALL |wx.ALIGN_CENTER_HORIZONTAL  ,border = 10)
		
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()
		
	def GetSelection(self):
		if self.rb1.GetValue() == True:
			return 	BTN_AMPLIFIER_TR_G_1_10
		#if self.rb2.GetValue() == True:
		#	return 	BTN_AMPLIFIER_TR_G_10_50
		#if self.rb3.GetValue() == True:
		#	return 	BTN_AMPLIFIER_TR_G_50_100



	

class TransistorAmpDesign():
	"""
	calcula os valores de um amplificador transistorizado ganho 1-10
	"""
	def __init__(self,fVg,fRlw,fEcmax,fTmax,fS,fDic,fE0pp,fBeta,fVcc,fMin,fIcmax,debugMode):
		
		self.fVg= fVg
		self.fRlw= fRlw
		self.fEcmax= fEcmax
		self.fTmax= fTmax
		self.fS= fS
		self.fDic= fDic
		self.fE0pp=fE0pp
		self.fBeta=fBeta
		self.fVcc= fVcc
		self.fMin= fMin
		self.fIcmax= fIcmax
		
		self.condicaoValida= True
		self.valorIcOK= False
		
		self.debugMode= debugMode
		
		self.finalMsg= _("Circuit calculated correctly")
		
		if self.debugMode == True:
			print "Vg=", self.fVg
			print "Rl=",self.fRlw
			print "Ecmax=",self.fEcmax
			print "Tmax=",self.fTmax
			print "S=",self.fS
			print "Dic=",self.fDic
			print "E0pp=",self.fE0pp
			print "Beta=",self.fBeta
			print "Vcc=",self.fVcc
			print "Fmin=",self.fMin
			print "Icmax=",self.fIcmax
		
		
	def calculaCircuito(self):
		"""
		retorna  booleano indicando se a topologia pode ser calculada(True/False)
		os valores dos componentes podem ser obtidos atrevés dos métodos correspondentes
		"""
		
		self.fQic= 0.0005	#corrente quiescente inicial em amperes
		
		#calcula a minima Icq em funcao dos valores de Re e Rlac
		
		while self.condicaoValida == True:
			
			self.fEres= (retornaDeltaVbe(self.fQic)*(self.fTmax-20)*100)/self.fDic
			self.fRes= self.fEres/self.fQic
	
			self.fRlac= self.fVg * self.fRes
			
			if self.fRlw <= self.fRlac:
				self.fQic = 1.2 * self.fQic #aumentamos a Icq para atender aos valores de RLac e Re necessarios para o ganho especificado
				if self.fQic > self.fIcmax/2:
					self.condicaoValida= False	
					self.finalMsg=  _("Design impossible: Try increase RLw")	
		
			else:
				break
				
		
		#calcula a minima Icq para resultar em Rl positivo
		
		while self.condicaoValida == True:
			self.fEres= (retornaDeltaVbe(self.fQic)*(self.fTmax-20)*100)/self.fDic
			self.fRes= self.fEres/self.fQic
	
			self.fRlac= self.fVg * self.fRes
			self.fRl= (self.fRlw * self.fRlac)/(self.fRlw-self.fRlac)
			
			if self.fRl < 0:
				self.fQic = 1.2 * self.fQic
				if self.fQic > self.fIcmax/2:
					self.condicaoValida= False	
					self.finalMsg= _("Design impossible: Try increase RLw or lower Vg")	
		
			else:
				break
				
				
		#calcula o minIcq para garantir a VCE desejada				
		
		
		while self.condicaoValida== True:
			if self.debugMode == True:
				print self.fQic
		
			self.fEres= (retornaDeltaVbe(self.fQic)*(self.fTmax-20)*100)/self.fDic
			self.fRes= self.fEres/self.fQic
			self.fRlac= self.fVg * self.fRes
			self.fRl= (self.fRlw * self.fRlac)/(self.fRlw-self.fRlac)
		
			self.fErl= self.fQic * self.fRl
			self.fEq= 1 + self.fE0pp
		
			self.fEs= self.fEq + self.fErl + self.fEres
			self.fFolgaVcc= self.fVcc- self.fEs

			if self.fFolgaVcc < 1.0:
				self.fQic= self.fQic * 1.1
				if self.fQic > self.fIcmax/2:
					self.condicaoValida= False
					self.finalMsg=  _("Design impossible: Try increase Vcc")
					
									
			else:
				self.valorIcOK= True
				self.fEq = self.fEq + self.fFolgaVcc
				break
				
		if self.condicaoValida==True:
			self.fRb2= self.fS * self.fRes
			self.fBetaRes= self.fBeta * self.fRes
			self.fRint= (self.fRb2 * self.fBetaRes)/(self.fRb2+self.fBetaRes)
			self.fErb1= self.fEq + self.fErl - 0.6 
			self.fRb1= (self.fErb1 * self.fRint)/(self.fEres +0.6)
			self.fiZin= 1.0/self.fRb1 + 1.0/self.fRb2 + 1.0/(self.fBeta * self.fRes) 
			self.fZin= 1.0/self.fiZin
			self.fCcin= 1.0/(2 * 3.14 * self.fMin * self.fZin/10.0)
			self.fCco= 1.0 /(2 * 3.14 * self.fMin * self.fRlw/10.0)
			
		return self.condicaoValida


	def GetRe(self):
		return self.fRes
		 
	def GetRl(self):
		return self.fRl

	def GetRb1(self):
		return self.fRb1

	def GetRb2(self):
		return self.fRb2
		
	def GetCcin(self):
		return self.fCcin		

	def GetCco(self):
		return self.fCco	

	def GetQic(self):
		return self.fQic
		
	def GetZin(self):
		return self.fZin	
		
	def GetEres(self):
		return self.fEres		
			
	def GetFinalMsg(self):
		return self.finalMsg
