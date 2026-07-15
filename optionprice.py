import yfinance as yf 
import numpy as np
import matplotlib.pyplot as plt 
import numpy.linalg as la 
from scipy.linalg import lu
from scipy.interpolate import interp1d
import tkinter as tk
import pandas as pd 
import pyautogui
root=tk.Tk()
stc=tk.StringVar()
ep=tk.IntVar()
aed=tk.IntVar()
total_exercise_time=tk.DoubleVar()
spotprice=tk.IntVar()
vol=tk.IntVar()
root.title("Call Option Price Calculator")
tk.Label(root,text="TICKR").pack()
tk.Label(root,text="Time to exercise(In DAYS from 1st July)").pack()
tk.Label(root,text="Strike Price").pack()
tk.Label(root,text="Period of exercise").pack()
tk.Label(root,text="Expected price").pack()
tk.Label(root,text="Volatility(Daily)").pack()
entry1=tk.Entry(root,textvariable=stc)
entry1.pack()
entry2=tk.Entry(root,textvariable=total_exercise_time)
entry3=tk.Entry(root,textvariable=ep)
entry4=tk.Entry(root,textvariable=aed)
entry2.pack()
entry3.pack()
entry4.pack()
entry5=tk.Entry(root,textvariable=spotprice)
entry5.pack()
entry6=tk.Entry(root,textvariable=vol)
entry6.pack()
def option_price_calculator(stc,ep,aed,total_exercise_time,vol,spotprice):
	volatility=vol
	r=0.045
	max_price=2*spotprice
	tet= float(total_exercise_time)
	time_step=100
	price_step=100
	time_dif=(int(tet)/(time_step-1))
	price_dif=(max_price)/(price_step-1)
	v_i=0
	vi2=0
	vi1=0
	vt2=np.zeros((time_step,price_step))
	vt3=np.zeros((time_step,price_step))
	K=float(ep)
	v_i=0
	vi1=max(price_dif-K,0)
	vi2=max((2*price_dif)-K,0)
	vt2[:,-1]=max_price-K
	x=np.linspace(0,float(total_exercise_time),int(time_step))
	y=np.linspace(0,max_price,price_step)
	for j in range(0,price_step-2):
		a=(0.5*r*(price_step-j-1)*time_dif)-(0.5*(volatility**2)*((price_step-j-1)**2)*time_dif)
		b=1+((volatility**2)*((price_step-j-1)**2)*time_dif)#+(r*time_dif)
		c=(-0.5*r*(price_step-j-1)*time_dif)-(0.5*(volatility**2)*((j+1)**2)*time_dif)
		d=vt2[:-1,price_step-j-1]
		e=np.zeros((time_step-1,price_step))
		e[0,0]=a/(1-r*(time_dif))
		e[0,1]=b/(1-r*(time_dif))
		e[0,2]=c/(1-r*(time_dif))
		for l in range(1,price_step-1):
			e[l,l-1]=a/(1-r*(time_dif))
			e[l,l]=b/(1-r*(time_dif))
			e[l,l+1]=c/(1-r*(time_dif))
		g=la.pinv(e)
		f=np.transpose(e)
	
		h=np.matmul(g,d)
		vt2[:,price_step-j-2]=h
		for i in range(0,time_step-1):
			vt2[i,price_step-j-2]=max(vt2[i,price_step-j-2],max((price_step-j-2)*price_dif-K,0))
		vt2[-1,price_step-j-2]=max(((price_step-j-2)*price_dif)-K,0)
	def lagrange(x1,y1,stockprice):
		u=1
		stockprice=float(stockprice)
		for y2 in range(0,len(x1)):
			if stockprice!=x1[y2]:
				u*=(stockprice-x1[y2])
			else:
				u*=1
		def l3(x1,index):
			w=1
			for m in range(0,len(x1)):
				if m!=index:
					w*=1/(x1[index]-x1[m])
				else:
					w*=1
			return w 
		z1=0
		for l2 in range(0,len(x1)):
			if stockprice!=x1[l2]:
				z1+=y1[l2]*l3(x1,l2)*(1/(stockprice-x1[l2]))
			else: 
				z1+=0
		return z1*u

	Current_price=lagrange(y,vt2[int(aed)-1,:], spotprice)
	return Current_price
option_price1=tk.IntVar()
text1=tk.StringVar()
output_label2 = tk.Label(root, textvariable=option_price1, font=("Arial", 14))
output_label2.pack(pady=10)
output_label4 = tk.Label(root, textvariable=text1, font=("Arial", 14))
output_label4.pack(pady=10)
def submit_data():
	stc=entry1.get()
	ep=entry3.get()
	aed=entry4.get()
	spotprice=entry5.get()
	total_exercise_time=entry2.get()
	vol=float(entry6.get())
	option_price1.set((option_price_calculator(stc,ep,aed,total_exercise_time,vol,float(spotprice))))
	text1.set("Option Price")
button = tk.Button(root, text="Check Option Price", width=30, command=submit_data).pack()
root.mainloop()