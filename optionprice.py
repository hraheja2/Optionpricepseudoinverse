import yfinance as yf 
import numpy as np
import matplotlib.pyplot as plt 
import numpy.linalg as la 
from scipy.linalg import lu
from scipy.interpolate import interp1d
stc=input("Enter TICKR (In caps)")
data =yf.download(stc,start="2026-01-01", end ="2027-07-01")
#print(data)
#print(data['Close'].to_numpy(),"values")
close_prices=(np.zeros(len(data['Close'].to_numpy())))
open_prices=(np.zeros(len(data[['Close']].to_numpy())))
#print(close_prices.shape,"shape")
close_prices[:]=data['Close'].to_numpy()[:,0]
open_prices[:]=data['Open'].to_numpy()[:,0]
returns=np.zeros(len(close_prices))
for i in range(len(returns)):
	returns[i]=np.log(close_prices[i]/open_prices[i])
#print(returns,"returns")
#print(close_prices)
mean=0
for i in range(len(data['Close'].to_numpy())):
	mean+=returns[i]
mean=mean/len(data['Close'].to_numpy())
#print(mean,'mean')
variance=0
for i in range(len(data['Close'].to_numpy())):
	variance+= (returns[i]-mean)**2
variance=variance/((len(data['Close'].to_numpy()))-1)
#print(variance,'variance')
volatility=np.sqrt(variance*252)
#print(volatility,'volatliity')
r=0.045
max_price=1.2*close_prices[-1]
#print(max_price,'max_price')
total_exercise_time=1/48
time_step=4
price_step=4
time_dif=(total_exercise_time/(time_step))
price_dif=(max_price)/price_step
v_i=0
vi2=0
vi1=0
vt2=np.zeros((time_step,price_step))
vt3=np.zeros((time_step,price_step))
print(yf.Ticker(stc).options[0],"expiration")
K=yf.Ticker(stc).option_chain(yf.Ticker(stc).options[0]).calls['strike'][0]
print(K,'K')
v_i=0
vi1=max(price_dif-K,0)
vi2=max((2*price_dif)-K,0)
vt2[:,-1]=max_price-K
#for i in range(0,time_step-1):
	#vt2[-1,i]=max((i*price_dif)-K,0)
#print(vt2,'initial')
#print(vt2,'vt2')
x=np.linspace(0,total_exercise_time,time_step)
y=np.linspace(0,max_price,price_step)
for j in range(0,price_step-2):
	#for i in range(0,time_step-2):
	a=(0.5*r*(j+1)*time_dif)-(0.5*(volatility**2)*((j+1)**2)*time_dif)
	b=1+((volatility**2)*((j+1)**2)*time_dif)+(r*time_dif)
	c=(-0.5*r*(j+1)*time_dif)-(0.5*(volatility**2)*((j+1)**2)*time_dif)
	d=vt2[:-1,price_step-j-1]
	e=np.zeros((time_step-1,price_step))
	print(a,b,c,'abc')
	e[0,0]=a
	e[0,1]=b
	e[0,2]=c
	for l in range(1,price_step-1):
		e[l,l-1]=a
		e[l,l]=b
		e[l,l+1]=c
	#print(e[0,1],e[1,1])
	f=np.transpose(e)
	#print(f,'f')
	u=np.matmul(f,e)
	#print(u,'u')
	#for q in range(0,price_step-1):
		#print(u[q,:],"u", q)
	#print(u,'u')
	z=np.linalg.det(u)
	#print(z,'z')
	g=np.linalg.inv(u)
	h=np.matmul(np.matmul(g,f),d)
	vt2[:,price_step-j-2]=h
		#print(a,'a')
		#print(b,'b')
		#print(c,'c')
		#if j!=0:
		#vt2[time_step-i-3,price_step-1-j]=max(vt2[time_step-i-3,price_step-1-j],max((price_step-1-j)*price_dif-K,0))
		#vt2[time_step-i-2,price_step-1-j]=max(vt2[time_step-i-2,price_step-1-j],max((price_step-1-j)*price_dif-K,0))
		#vt2[time_step-i-1,price_step-1-j]=max(vt2[time_step-i-1,price_step-1-j],max((price_step-1-j)*price_dif-K,0))
		#vt2[time_step-i-2,price_step-j-2]=(a*vt2[time_step-i-3,price_step-1-j])+(b*vt2[time_step-i-2,price_step-1-j])+(c*vt2[time_step-i-1,price_step-1-j])
	for i in range(0,time_step-1):
		vt2[i,price_step-j-2]=max(vt2[i,price_step-j-2],max((price_step-j-2)*price_dif-K,0))
	vt2[-1,price_step-j-2]=max(((price_step-j-2)*price_dif)-K,0)
		#print(vt2[time_step-i-2,time_step-j-2],'option value')
		#print(i, " time",j," Stock price")
		#if j==0:
			#vt2[i,j]=max(vt2[i,j],max(j*price_dif-K,0))
			#vt2[i+1,j]=max(vt2[i+1,j],max((j+1)*price_dif-K,0))
			#vt2[i+2,j]=max(vt2[i+2,j],max((j+2)*price_dif-K,0))
			#vt2[i+1,j+1]=(a*vt2[0,j])+(b*vt2[0,j+1])+(c*vt2[0,j+2])
#for i in range(0,time_step-1):
	#vt2[i,0]=max(vt2[i,0],max((i)*price_dif-K,0))
#print(vt2[18,:],"previous option price")
#print(vt2[17,:],"17th option price")
#print(vt2[:,-1],"option price max sp")
#print(vt2,'vt2')
#print(a,b,c,"abc")
fig = plt.figure(figsize=(8, 6))
ax=fig.add_subplot(111, projection='3d')
surface=ax.plot_surface(x,y,vt2,cmap='viridis',edgecolor='none')
fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10, label='Z Value')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('3D Surface Plot')
#print(max_price)
# 5. Show the plot
plt.show()
#print(np.argwhere(x>=10*time_dif)[0],np.argwhere(y>=(25)*price_dif)[0])
print(y[np.argwhere(y>=(price_step/2)*price_dif)[0]+1],'spot price')
interpolator=interp1d(y,vt2[np.argwhere(x>=(time_step/2)*time_dif)[0],:],kind='cubic')
spotprice=yf.Ticker(stc).fast_info.last_price
Current_price=max(interpolator(spotprice),max(spotprice-K,0))
print(spotprice,'current price')
#print(vt2[np.argwhere(x>=(time_step/2)*time_dif)[0],np.argwhere(y>=(price_step/2)*price_dif)[0]+1],"current option price")
print(Current_price,'current option price')