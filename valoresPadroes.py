#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  resistorPadrao.py
#  
#  Copyright 2015 tavares <tavares@tavares-Inspiron-N5010>
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
#  Este programa identifica o valor padrão correspondente ao valor de entrada,
#segundo as séries E12, E24 e E92, para 10% 5% e 1% respectivamente
#
#  
#  valorOriginal- valor calculado em ohms
#  tolerancia   10, 5, 1 para 10, 5 1%
#  selecao  0-> retorna valor mais proximo   1-> retorna valor imediatamente inferior   2-> retorna valor imediatamente superior
#  v 1.0     17/02/2015


from numpy  import *

"""
17/02/2015 
Este script retorna o valor padrão corresponde as séries E12, E24 e E96, aplicadas a resistores
valorOriginal. Valor original em ohm
tolerancia: pode ser 10, 5 e 1 , correspondendo a 10%, 5% e 1% respectivamente
seleção: Se 0 -> retorna o valor mais próximo
         Se 1 -> retorna o valor imediatamente inferior
		 Se 2 -> retorna o valor imediatamente superior

10/09/2015
Acrescentado retorno de valores padrões de capacitores eletrolíticos

"""

def retornaValorResistor (valorOriginal,tolerancia,selecao):
		E12= array([1.0,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2])
		E24= array([1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1])
		E96= array([1.00,1.02,1.05,1.07,1.10,1.13,1.15,1.18,1.21,1.24,1.27,1.30,1.33,1.37,1.40,1.43,1.47,1.50,1.54,
		1,58,1.62,1.65,1.69,1.74,1.78,1.82,1.87,1.91,1.96,2.00,2.05,2.10,2.16,2.21,2.26,2.32,2.37,2.43,2.49,2.55,2.61,
		2.67,2.74,2.80,2.87,2.94,3.01,3.09,3.16,3.24,3.32,3.40,3.48,3.57,3.65,3.74,3.83,3.92,4.02,4.12,4.22,4.32,4.42,
		4.53,4.64,4.75,4.87,4.99,5.11,5.23,5.36,5.49,5.62,5.76,5.90,6.04,6.19,6.34,6.49,6.65,6,81,6.98,7.15,7.32,7.50,
		7.68,7.87,8.06,8.25,8.45,8.66,8.87,9.09]) 


		#escala o valor original para algo entre 1 e 10 		
		multiplicador = 1.0
		while valorOriginal > 10.0:
			valorOriginal= valorOriginal / 10.0
			multiplicador= multiplicador * 10.0
		
		if tolerancia == 10:
			indice= searchsorted(E12, valorOriginal)
			valorInferior= E12[indice-1]*multiplicador
			valorSuperior= E12[indice]*multiplicador	

		if tolerancia == 5:
			indice= searchsorted(E24, valorOriginal)
			valorInferior= E24[indice-1]*multiplicador
			valorSuperior= E24[indice]*multiplicador	
		
		if tolerancia == 1:
			indice= searchsorted(E96, valorOriginal)
			valorInferior= E96[indice-1]*multiplicador
			valorSuperior= E96[indice]*multiplicador			
			

		if (valorSuperior - valorOriginal) > (valorOriginal - valorInferior) :
			valorMaisProximo= valorInferior
		else:
			valorMaisProximo= valorSuperior

	
		if selecao == 0:
			return valorMaisProximo
			
		if selecao == 1:
			return valorInferior
			
		if selecao == 2:
			return valorSuperior
		
		
"""
Recebe o valor do  eletrolitico em microfarads 	e retorna o valor padrao mais proximo		

valorOriginal: valor do capacitor em microfarads
seleção: Se 0 -> retorna o valor mais próximo
         Se 1 -> retorna o valor imediatamente inferior
		 Se 2 -> retorna o valor imediatamente superior


"""

def retornaValorEletrolitico (valorOriginal,selecao):
		capArray= array([0.47,1, 2.2 , 3.3 ,4.7,10,22,33,47,100,220,330,470,1000,2200,3300,4700,10000,47000])
	
		indice= searchsorted(capArray, valorOriginal)
		
	
		valorInferior= capArray[indice-1]
		valorSuperior= capArray[indice]	
		
		if (valorSuperior - valorOriginal) > (valorOriginal - valorInferior) :
			valorMaisProximo= valorInferior
		else:
			valorMaisProximo= valorSuperior

		


		if selecao == 0:
			return valorMaisProximo
			
		if selecao == 1:
			return valorInferior
			
		if selecao == 2:
			return valorSuperior
			

