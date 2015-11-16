#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ampOpDesign.py
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
BTN_AMPLIFICADOR_INVERSOR = wx.NewId()     
BTN_AMPLIFICADOR_NAO_INVERSOR = wx.NewId()
BTN_AMPLIFICADOR_DE_CORRENTE = wx.NewId()
BTN_AMPLIFICADOR_DE_TRANSCONDUTANCIA = wx.NewId()
BTN_AMPLIFICADOR_INVERSOR_AC = wx.NewId()
BTN_AMPLIFICADOR_SENSIVEL__CARGA = wx.NewId()
BTN_AMPLIFICADOR_SOMADOR = wx.NewId()



class SelAmpOpDesign(wx.Dialog):
		
	def __init__(self):
			
		wx.Dialog.__init__(self, None, -1, _("Operational Amplifier Circuits Selection"),size=(300, 150)) #inicializacao do dialogo
		
		self.sizer1 = wx.BoxSizer(wx.VERTICAL)
		
		self.sizer10 = wx.BoxSizer(wx.HORIZONTAL);
		
		self.sizer11 = wx.StaticBoxSizer( wx.StaticBox( self, -1, "AMPLIFIERS" ), wx.VERTICAL );
		self.sizer111 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer112 = wx.BoxSizer(wx.HORIZONTAL);		
		self.sizer113 = wx.BoxSizer(wx.HORIZONTAL);		
		self.sizer11.Add(self.sizer111,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer11.Add(self.sizer112,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer11.Add(self.sizer113,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)		
		
		#self.sizer12 = wx.BoxSizer(wx.HORIZONTAL);
		self.sizer13 = wx.BoxSizer(wx.HORIZONTAL);
		
	
		self.staticTxtTitulo= wx.StaticText(self, -1, _("Select the circuit type"))  
		self.staticTxtTitulo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		self.sizer10.Add(self.staticTxtTitulo)        #insere os conteudos dos sizer horizontais
		
		
		self.rb1 = wx.RadioButton(self, BTN_AMPLIFICADOR_INVERSOR , _("Inverter amplifier") ,style=wx.RB_GROUP)
		self.rb2 = wx.RadioButton(self, BTN_AMPLIFICADOR_NAO_INVERSOR , _("Non inverter amplifier"))
		self.rb3 = wx.RadioButton(self, BTN_AMPLIFICADOR_DE_CORRENTE , _("Current amplifier"))
		self.rb4 = wx.RadioButton(self, BTN_AMPLIFICADOR_DE_TRANSCONDUTANCIA , _("Transcondutance amplifier"))		
		self.rb5 = wx.RadioButton(self, BTN_AMPLIFICADOR_INVERSOR_AC , _("AC inverter amplifier"))		
		self.rb6 = wx.RadioButton(self, BTN_AMPLIFICADOR_DE_CORRENTE , _("Current amplifier"))		
		self.rb7 = wx.RadioButton(self, BTN_AMPLIFICADOR_SENSIVEL__CARGA , _("Charge amplifier"))
		self.rb8 = wx.RadioButton(self, BTN_AMPLIFICADOR_SOMADOR , _("Summing amplifier"))				
		
		
		self.sizer111.Add(self.rb1,flag= wx.EXPAND | wx.ALL, border = 5)        #insere os conteudos dos sizer horizontais
		self.sizer111.Add(self.rb2,flag= wx.EXPAND | wx.ALL, border = 5) 
		self.sizer111.Add(self.rb3,flag= wx.EXPAND | wx.ALL, border = 5) 
		
		self.sizer112.Add(self.rb4,flag= wx.EXPAND | wx.ALL, border = 5)        #insere os conteudos dos sizer horizontais
		self.sizer112.Add(self.rb5,flag= wx.EXPAND | wx.ALL, border = 5) 
		self.sizer112.Add(self.rb6,flag= wx.EXPAND | wx.ALL, border = 5) 		

		self.sizer113.Add(self.rb7,flag= wx.EXPAND | wx.ALL, border = 5)        #insere os conteudos dos sizer horizontais
		self.sizer113.Add(self.rb8,flag= wx.EXPAND | wx.ALL, border = 5) 
		 		

		
		self.okButton= wx.Button(self, wx.ID_OK, "OK")                      #objeto botao OK
		self.cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel")        #objeto botao cancela
		self.sizer13.Add(self.okButton,flag= wx.EXPAND | wx.ALL, border = 5)
		self.sizer13.Add(self.cancelButton,flag= wx.EXPAND | wx.ALL, border = 5)
		
		
		self.sizer1.Add(self.sizer10,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)         #inserimos os sizers horizontais no vertical
		self.sizer1.Add(self.sizer11,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		#self.sizer1.Add(self.sizer12,flag= wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border = 10)
		self.sizer1.Add(self.sizer13,flag= wx.ALL |wx.ALIGN_CENTER_HORIZONTAL  ,border = 10)
		
		self.SetSizer(self.sizer1)    #insere o sizer de maior nivel na área ocupada pelo dialogo
		self.Fit()
		
	def GetSelection(self):
		if self.rb1.GetValue() == True:
			return 	BTN_AMPLIFICADOR_INVERSOR
		if self.rb2.GetValue() == True:
			return 	BTN_AMPLIFICADOR_NAO_INVERSOR
		if self.rb3.GetValue() == True:
			return 	BTN_AMPLIFICADOR_DE_CORRENTE
		if self.rb4.GetValue() == True:
			return 	BTN_AMPLIFICADOR_DE_TRANSCONDUTANCIA
		if self.rb5.GetValue() == True:
			return 	BTN_AMPLIFICADOR_INVERSOR_AC
		if self.rb6.GetValue() == True:
			return 	BTN_AMPLIFICADOR_DE_CORRENTE
		if self.rb7.GetValue() == True:
			return 	BTN_AMPLIFICADOR_SENSIVEL__CARGA
		if self.rb8.GetValue() == True:
			return 	BTN_AMPLIFICADOR_SOMADOR

