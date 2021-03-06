##Wageningen B-Series Open Water Curves
import numpy as np
import matplotlib.pyplot as plt
import matplotlib2tikz as pltt

PoD_min = float(input('P/D min =' + '\n'))
PoD_max = float(input('P/D max =' + '\n'))
print('Curves will be computed using a P/D step of 0.1, hence ' + str((PoD_max-PoD_min)/0.1) + ' curves' + '\n')
EAR = float(input('Ae/A0 =' + '\n'))
Z = float(input('Z =' + '\n'))
Re = float(input('Re =' + '\n'))
PoDs = np.arange(PoD_min, PoD_max, 0.1)

def KtKq(J,PoD):
    f = open('coeffs.dat','r')
    f.readline()
    a = f.readlines()
    Kt = 0
    Kq = 0
    for line in a:
        l = line.split(' ')
        Kq += float(l[0])*J**float(l[1])*PoD**float(l[2])*EAR**float(l[3])*Z**float(l[4])
        Kt += float(l[5])*J**float(l[6])*PoD**float(l[7])*EAR**float(l[8])*Z**float(l[9])
    f.close()
    return(Kt,Kq)
    
def corr_Re(J,PoD):
    deltaKt = 0.000353485
    -0.00333758*EAR*J**2
    -0.00478125*EAR*PoD*J
    +0.000257792*(np.log(Re)-0.301)**2*EAR*J**2
    +0.0000643192*(np.log(Re)-0.301)*PoD**6*J**2
    -0.0000110636*(np.log(Re)-0.301)**2*PoD**6*J**2
    -0.0000276305*(np.log(Re)-0.301)**2*Z*EAR*J**2
    +0.00009545*(np.log(Re)-0.301)*Z*EAR*PoD*J
    +0.0000032049*(np.log(Re)-0.301)*Z**2*EAR*PoD**3*J
    deltaKq = -0.000561412
    +0.00696898*PoD
    -0.0000666654*Z*PoD**6
    +0.0160818*EAR**2
    -0.000938091*(np.log(Re)-0.301)*PoD
    -0.00059593*(np.log(Re)-0.301)*PoD**2
    +0.0000782099*(np.log(Re)-0.301)**2*PoD**2
    +0.0000052199*(np.log(Re)-0.301)*Z*EAR*J**2
    -0.00000088528*(np.log(Re)-0.301)**2*Z*EAR*PoD*J
    +0.0000230171*(np.log(Re)-0.301)*Z*PoD**6
    -0.00000184341*(np.log(Re)-0.301)**2*Z*PoD**6
    -0.00400252*(np.log(Re)-0.301)*EAR**2
    +0.000220915*(np.log(Re)-0.301)**2*EAR**2
    return(deltaKt,deltaKq)
    
def eta(J,Kt,Kq):
        return(J*Kt/(2*np.pi*Kq))
        
J = np.linspace(0,5,1000)
    
colors=['r','g','b','c','m','y','k','violet','purple','fuchsia']

for i in range(len(PoDs)):
    Kt = KtKq(J,PoDs[i])[0]
    Kq = KtKq(J,PoDs[i])[1]
    eta0 = eta(J,Kt,Kq)
    if Re > 2000000:
        Kt = Kt+corr_Re(J)[0]
        Kq = Kq+corr_Re(J)[1]
    for k in range(len(Kt)):
        if Kt[k] < 0:
            q = k
            break
    plt.plot(J[:q],Kt[:q],label='P/D={0}'.format(round(PoDs[i],2)),linestyle='solid',color=colors[i])
    plt.plot(J[:q],5*Kq[:q],linestyle='dotted',color=colors[i])
    plt.plot(J[:q],eta0[:q],linestyle='dashed',color=colors[i])
    plt.text(J[list(eta0).index(max(eta0))]-0.1, max(eta0)+0.05, 'P/D='+str(PoDs[i]))
plt.xlabel('Advance parameter $J$')
plt.ylabel('$K_T$ (solid), $5K_Q$ (dotted), $\eta_0$ (dashed)')
plt.legend()
plt.title('Open-water curves for B-series $A_E/A_0=$' + str(EAR)+', $Z=$' + str(int(Z)) +' at Re = ' +str(Re))
plt.show()
