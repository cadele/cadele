#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ampOpInversor.py
#  
#  Copyright 2015 Roberto Tavares <roberto.tavares.filho@gmail.com>
#  
#  Versão: 0.1, em 11/11/2015
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
#  entrada= Avco    ganho de tensão
#           Rin     resistencia de entrada mínima
#           RL      resistencia de carga
# ---------Dados do ampOp ----------------------------------------
#			Vio  tensão de offset de entrada
#           dVio variacao da tensão de offset de entrada com temperatura
#           Iio  corrente de offset do operacional
#           dIo  variação de corrente de offset
#           Rid  resistencia de entrada diferencial
#           Avo  ganho de tensão em malha aberta
#           fop  frequencia do primeiro polo do op amp
#           Ro   resistencia de saída do amplificador
#           Vn   tensão de ruído equivalente na entrada do ampop
#           In   corrente de ruído na entrada do ampop
# --------------Sensibilidade dos resistores em relação a temperatura --------
#           dRi  varicao da resistenca Ri com a temperatura (ppm /grau centigrado)
#           dRf  variação da resitencia Rf com a temperatura (ppm/ graus centigrados)
# --------------------faixa de temperatura de uso do circuito ----------------------
#           tmin      temperatura minima graus centigrados
#           tmax      temperatura máxima em graus centigrados


import valoresPadroes
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
TXT_AVCOO = wx.NewId()    
TXT_RIN = wx.NewId()
TXT_RL = wx.NewId() 
TXT_VIO = wx.NewId()  
TXT_DVIO = wx.NewId()
TXT_IIO = wx.NewId()
TXT_DIIO = wx.NewId()
TXT_RID =  wx.NewId()
TXT_AVO = wx.NewId()
TXT_FOP = wx.NewId()
TXT_RO = wx.NewId()
TXT_VN = wx.NewId()
TXT_IN = wx.NewId()
TXT_DRI = wx.NewId()
TXT_DRF = wx.NewId()
TXT_TMIN = wx.NewId()
TXT_TMAX = wx.NewId()





class entradaInversorAmpOp(wx.Dialog):
	"""
	Implementa a tela de entrada de parametros de projeto do inversor com amp op
	"""
	def __init__(self):
			
		wx.Dialog.__init__(self, None, -1, _('Inverter Amplifier Specifications'),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer10 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer11 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer12 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer13 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer14 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer15 = wx.BoxSizer(wx.HORIZONTAL);
								
		self.staticTxtTitulo= wx.StaticText(self, -1, _("Input Data"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer1.Add(self.staticTxtTitulo, flag= wx.ALIGN_CENTER_HORIZONTAL)        #insere os conteudos dos sizer horizontais		

		self.static1= wx.StaticText(self, -1, "Avco:")  #objeto texto statico 
		self.static1.SetToolTipString(_("Circuito closed gain"))
		self.static1.SetForegroundColour(wx.BLUE)
		self.avcoTxt = wx.TextCtrl(self, TXT_AVCOO,'100',size=(40,20), style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static1,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.avcoTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static2= wx.StaticText(self, -1, "Ri min:")  #objeto texto statico 
		self.static2.SetToolTipString(_("Minimum input resistence, ohms"))
		self.static2.SetForegroundColour(wx.BLUE)
		self.riminTxt = wx.TextCtrl(self, TXT_RIN,'1000',size=(60,20), style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static2,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.riminTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static3= wx.StaticText(self, -1, "RL:")  #objeto texto statico 
		self.static3.SetToolTipString(_("Minimum Load resistence, ohms"))
		self.static3.SetForegroundColour(wx.BLUE)
		self.rlTxt = wx.TextCtrl(self, TXT_RL,'2000',size=(60,20), style=wx.TE_CENTRE)  
		self.sizer10.Add(self.static3,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer10.Add(self.rlTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static4= wx.StaticText(self, -1, "Vio:")  #objeto texto statico 
		#self.static4.SetToolTipString(_("Input offset voltage (millivolts volts)"))
		#self.vioTxt = wx.TextCtrl(self, TXT_VIO,'0.8',size=(40,20), style=wx.TE_CENTRE)  
		#self.sizer11.Add(self.static4,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer11.Add(self.vioTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static5= wx.StaticText(self, -1, "Delta Vio:")  #objeto texto statico 
		#self.static5.SetToolTipString(_("Output change due input offset change (microvolts/centigrades degrees)"))
		#self.dvioTxt = wx.TextCtrl(self, TXT_DVIO,'15',size=(40,20), style=wx.TE_CENTRE)  
		#self.sizer11.Add(self.static5,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer11.Add(self.dvioTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static6= wx.StaticText(self, -1, "Iio:")  #objeto texto statico 
		#self.static6.SetToolTipString(_("Input offset currente (nA)"))
		#self.iioTxt = wx.TextCtrl(self, TXT_IIO,'3',size=(40,20), style=wx.TE_CENTRE)  
		#self.sizer11.Add(self.static6,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer11.Add(self.iioTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static7= wx.StaticText(self, -1, "Delta Iio:")  #objeto texto statico 
		#self.static7.SetToolTipString(_("Output change due input current offset change (nA/centigrades degrees)"))
		#self.diioTxt = wx.TextCtrl(self, TXT_DIIO,'0.5',size=(40,20), style=wx.TE_CENTRE)  
		#self.sizer11.Add(self.static7,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer11.Add(self.diioTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		self.static8= wx.StaticText(self, -1, "Rid:")  #objeto texto statico 
		self.static8.SetToolTipString(_("Differential input resistence (Megaohms)"))
		self.ridTxt = wx.TextCtrl(self, TXT_RID,'6',size=(40,20), style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static8,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.ridTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.static9= wx.StaticText(self, -1, "Avo:")  #objeto texto statico 
		self.static9.SetToolTipString(_("Operational amplifier open loop gain"))
		self.avoTxt = wx.TextCtrl(self, TXT_AVO,'50000',size=(80,20), style=wx.TE_CENTRE)  
		self.sizer11.Add(self.static9,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer11.Add(self.avoTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		self.static10= wx.StaticText(self, -1, "fop:")  #objeto texto statico 
		self.static10.SetToolTipString(_("First pole frequency of amp op(hz)"))
		self.fopTxt = wx.TextCtrl(self, TXT_FOP,'8',size=(40,20), style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static10,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.fopTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		self.static11= wx.StaticText(self, -1, "Ro:")  #objeto texto statico 
		self.static11.SetToolTipString(_("Output resistence of amp op(ohms)"))
		self.roTxt = wx.TextCtrl(self, TXT_RO,'70',size=(40,20), style=wx.TE_CENTRE)  
		self.sizer12.Add(self.static11,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		self.sizer12.Add(self.roTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static12= wx.StaticText(self, -1, "Vn:")  #objeto texto statico 
		#self.static12.SetToolTipString(_("Equivalente input noise voltage (fentoV 2 / Hz)"))
		#self.vnTxt = wx.TextCtrl(self, TXT_VN,'5',size=(40,20), style=wx.TE_CENTRE)  
		#self.sizer12.Add(self.static12,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer12.Add(self.vnTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static13= wx.StaticText(self, -1, "In:")  #objeto texto statico 
		#self.static13.SetToolTipString(_("Equivalente input noise current  (atto I 2 / Hz)"))
		#self.inTxt = wx.TextCtrl(self, TXT_IN,'0.00005',size=(80,20), style=wx.TE_CENTRE)  
		#self.sizer12.Add(self.static13,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer12.Add(self.inTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		#self.static14= wx.StaticText(self, -1, "Delta Ri:")  #objeto texto statico 
		#self.static14.SetToolTipString(_("Change in circuit input resistence in ppm/degree centigrade)"))
		#self.static14.SetForegroundColour(wx.RED)
		#self.driTxt = wx.TextCtrl(self, TXT_DRI,'100',size=(80,20), style=wx.TE_CENTRE)  
		#self.sizer13.Add(self.static14,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer13.Add(self.driTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	


		#self.static15= wx.StaticText(self, -1, "Delta Rf:")  #objeto texto statico 
		#self.static15.SetToolTipString(_("Change in circuit feedback  resistence in ppm/degree centigrade)"))
		#self.static15.SetForegroundColour(wx.RED)
		#self.drfTxt = wx.TextCtrl(self, TXT_DRF,'100',size=(80,20), style=wx.TE_CENTRE)  
		#self.sizer13.Add(self.static15,flag= wx.RIGHT , border = 2)        #insere os conteudos dos sizer horizontais
		#self.sizer13.Add(self.drfTxt,flag= wx.RIGHT , border = 10)        #insere os conteudos dos sizer horizontais	

		self.rb1 = wx.RadioButton(self, -1, _('Resistors 1% tol'),  style=wx.RB_GROUP)
		self.rb2 = wx.RadioButton(self, -1, _('Resistors 5% tol') )

		self.sizer14.Add(self.rb1,flag= wx.RIGHT , border = 10)
		self.sizer14.Add(self.rb2,flag= wx.RIGHT , border = 10)

		self.okButton= wx.Button(self, wx.ID_OK, "OK")	#objeto botao OK
		self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancela")	#objeto botao cancela
		self.sizer15.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		self.sizer15.Add(self.cancelButton,flag= wx.EXPAND | wx.ALL, border = 5)


		self.sizer1.Add(self.sizer10,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer1.Add(self.sizer11,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL, border = 10) 
		self.sizer1.Add(self.sizer12,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer1.Add(self.sizer13,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer1.Add(self.sizer14,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)		
		self.sizer1.Add(self.sizer15,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)

		self.SetSizer(self.sizer1)    
		self.Fit()


		
	
	def GetAvcoTxt(self):
		return self.avcoTxt.GetValue()
	
	def GetRidTxt(self):
		return self.ridTxt.GetValue()
	
	def GetRoTxt(self):
		return self.roTxt.GetValue()
	
	def GetRiminTxt(self):
		return self.riminTxt.GetValue()
	
	def GetFopTxt(self):
		return self.fopTxt.GetValue()
	
	def GetAvoTxt(self):
		return self.avoTxt.GetValue()
	
	#def GetVnTxt(self):
	#	return self.vnTxt.GetValue()
	
	#def GetInTxt(self):
	#	return self.inTxt.GetValue()
	
	def GetRLTxt(self):
		return self.rlTxt.GetValue()
		
	def GetTol(self):
		if self.rb1.GetValue == True:
			return 1
		else:
			return 5	





class saidaAmpOpInverter(wx.Dialog):

	def __init__(self,Ri,Rf,RL,Rp,fcp,tr):
			
		wx.Dialog.__init__(self, None, -1, _('Circuito values'),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
				
		self.sizer10 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer11 = wx.BoxSizer(wx.VERTICAL);
		self.sizer12 = wx.BoxSizer(wx.VERTICAL);
		self.sizer13 = wx.BoxSizer(wx.VERTICAL);
				
		self.sizer15 = wx.BoxSizer(wx.VERTICAL);	
		self.staticTxtTitulo= wx.StaticText(self, -1, _("AmpOp inverter design output data"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer1.Add(self.staticTxtTitulo, flag= wx.ALIGN_CENTER_HORIZONTAL)        

			
		self.texto= "RI= " + str(Ri) + " ohms"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Circuit input resistor"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= "RF= " + str(Rf) + " ohms"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Circuit feedback resistor"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= "RL= " + str(RL) + " ohms"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Circuit load resistence"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

		self.texto= "RP= " + str(Rp) + " ohms"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Circuit offset resistor"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)  


		#self.texto= "Minimum  Avco= " + str(Avco_min)
		#self.static1= wx.StaticText(self, -1, self.texto)   
		#self.static1.SetToolTipString(_("Minimum gain due to resistor tolerance"))
		#self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        
		
		#self.texto= "Maximum  Avco= " + str(Avco_max)
		#Self.static1= wx.StaticText(self, -1, self.texto)   
		#self.static1.SetToolTipString(_("Maximum gain due to resistor tolerance"))
		#self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        
					

		self.texto= "fcp= " + str(fcp) + " Hz"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Small signal bandwidth"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)     


		self.texto= "tr= " + str(tr) + " microseconds"
		self.static1= wx.StaticText(self, -1, self.texto)   
		self.static1.SetToolTipString(_("Small signal risetime"))
		self.sizer11.Add(self.static1,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)   

		
		self.okButton= wx.Button(self, wx.ID_OK, _("CLOSE"))	#objeto botao OK
		self.sizer15.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		
			
		#insere a figura com o esquema associado
		self.img1 = wx.Image("ampOpInversor.png", wx.BITMAP_TYPE_ANY)
		self.bitmap1 = wx.StaticBitmap(self, -1, wx.BitmapFromImage(self.img1))
		self.sizer12.Add(self.bitmap1,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
		
		self.static13= wx.StaticText(self, -1, _("For theorical explanation, please visit http://www.cadernodelaboratorio.com.br"))  #objeto texto statico 
		self.sizer13.Add(self.static13,flag= wx.RIGHT , border = 2) 
		#montagem da estrutura de sizers
		
		self.sizer10.Add(self.sizer11,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer10.Add(self.sizer12,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
				
		self.sizer1.Add(self.sizer10,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)
		self.sizer1.Add(self.sizer13,flag= wx.ALL| wx.ALIGN_CENTER_HORIZONTAL , border = 10)        

			
		self.sizer1.Add(self.sizer15,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)  
		
		
			
				
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()





class ampOpInverterAmplifierDesign():
		
	
	def __init__(self):
	
		self.dialogo =  entradaInversorAmpOp()      #cria um dialogo de solicitacao de parametros de entrada
		
		self.result = self.dialogo.ShowModal() 

				
		if self.result == wx.ID_OK:  
			self.result2= self.calculaCircuito()
			self.tol= self.dialogo.GetTol()
			self.RiStd= valoresPadroes.retornaValorResistor(self.Ri,self.tol,0)
			self.RfStd= valoresPadroes.retornaValorResistor(self.Rf,self.tol,0)
			self.RpStd= valoresPadroes.retornaValorResistor(self.Rp,self.tol,0)
			self.dialogo2= saidaAmpOpInverter(self.RiStd,self.RfStd,self.RL,self.RpStd,self.fcp, self.tr*1000000)
			self.result3= self.dialogo2.ShowModal()	
				
		self.dialogo2.Destroy()		
		self.dialogo.Destroy()
								
				
		
		
	def calculaCircuito(self):
		self.avco = -float(self.dialogo.GetAvcoTxt())
		self.Rid= 1000000.0 * float(self.dialogo.GetRidTxt())
		self.Ro= float(self.dialogo.GetRoTxt())
		self.Rimin= float(self.dialogo.GetRiminTxt())
		self.fop= float(self.dialogo.GetFopTxt())
		self.avo= float(self.dialogo.GetAvoTxt())
		#self.vn = float(self.dialogo.GetVnTxt())
		#self.inoise = float(self.dialogo.GetInTxt())
		self.RL= float(self.dialogo.GetRLTxt())
		
		#calculo do valor otimo de Rf
		self.beta= 1.0 / (1.0 -self.avco)
		#calcula o valor de Rf otimo
		self.Rf= sqrt((self.Rid * self.Ro)/(2*self.beta))
	    #calcula o valor de ri
		self.Ri= - self.Rf/self.avco
	    
		while  self.Ri< self.Rimin:
			self.Rf = 1.1 * self.Rf
			self.Ri = -self.Rf / self.avco
		
		#calculo de Rp	
		self.Rp= (self.Ri * self.Rf)/(self.Ri + self.Rf) 
	    
	    #calculo da banda de passagem 
		self.fcp= self.fop * self.avo * self.Ri/self.Rf
	    
	    #calculo de tr
		self.tr = 0.35 * self.Rf/(self.fop*self.avo*self.Ri)
	    
	    
		
		return True


	
