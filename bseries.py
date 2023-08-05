"""
Wageningen B-Series Open Water Curves
"""

import numpy as np
import matplotlib.pyplot as plt


def thrust_torque_coefficients(J, PoD):
    """
    Computes the value of the thrust coefficient KT and 
    torque coefficient KQ as a function of advance ratio J 
    and reduced pitch P/D from polynomials.
    """
    with open('coeffs.dat','r') as f_coefs:
        f_coefs.readline()
        a = f_coefs.readlines()
        Kt = 0
        Kq = 0
        for line in a:
            l = line.split(' ')
            Kq += float(l[0])*J**float(l[1])*PoD**float(l[2])*EAR**float(l[3])*Z**float(l[4])
            Kt += float(l[5])*J**float(l[6])*PoD**float(l[7])*EAR**float(l[8])*Z**float(l[9])
    return Kt, Kq


def corr_reynolds(J, PoD):
    """
    Computes a correction on thrust and torque coefficients
    if the Reynolds number is greater than 2 000 000.
    """
    delta_kt = 0.000353485 \
    -0.00333758*EAR*J**2 \
    -0.00478125*EAR*PoD*J \
    +0.000257792*(np.log(Re)-0.301)**2*EAR*J**2 \
    +0.0000643192*(np.log(Re)-0.301)*PoD**6*J**2 \
    -0.0000110636*(np.log(Re)-0.301)**2*PoD**6*J**2 \
    -0.0000276305*(np.log(Re)-0.301)**2*Z*EAR*J**2 \
    +0.00009545*(np.log(Re)-0.301)*Z*EAR*PoD*J \
    +0.0000032049*(np.log(Re)-0.301)*Z**2*EAR*PoD**3*J
    delta_kq = -0.000591412 \
    +0.00696898*PoD \
    -0.0000666654*Z*PoD**6 \
    +0.0160818*EAR**2 \
    -0.000938091*(np.log(Re)-0.301)*PoD \
    -0.00059593*(np.log(Re)-0.301)*PoD**2 \
    +0.0000782099*(np.log(Re)-0.301)**2*PoD**2 \
    +0.0000052199*(np.log(Re)-0.301)*Z*EAR*J**2 \
    -0.00000088528*(np.log(Re)-0.301)**2*Z*EAR*PoD*J \
    +0.0000230171*(np.log(Re)-0.301)*Z*PoD**6 \
    -0.00000184341*(np.log(Re)-0.301)**2*Z*PoD**6 \
    -0.00400252*(np.log(Re)-0.301)*EAR**2 \
    +0.000220915*(np.log(Re)-0.301)**2*EAR**2
    return delta_kt,delta_kq


def eta(J, Kt, Kq):
    """
    Computes the efficiency of the propeller.
    """
    return J * Kt / (2 * np.pi * Kq)


if __name__ == '__main__':
    PoD_min = float(input('P/D min =' + '\n'))
    PoD_max = float(input('P/D max =' + '\n'))
    PoDs = np.arange(PoD_min, PoD_max, 0.1)
    print(f"Curves will be computed using a P/D step of 0.1, hence {len(PoDs)} curves\n")
    EAR = float(input('Ae/A0 =' + '\n'))
    Z = float(input('Z =' + '\n'))
    Re = float(input('Re =' + '\n'))
    J = np.linspace(0, 5, 1000)
    colors = ['r','g','b','c','m','y','k','violet','purple','fuchsia']
    for i in range(len(PoDs)):
        Kt = thrust_torque_coefficients(J, PoDs[i])[0]
        Kq = thrust_torque_coefficients(J, PoDs[i])[1]
        if Re > 2e6:
            Kt = Kt + corr_reynolds(J, PoDs[i])[0]
            Kq = Kq + corr_reynolds(J, PoDs[i])[1]
        eta0 = eta(J,Kt,Kq)
        for k in range(len(Kt)):
            if Kt[k] < 0:
                q = k
                break
        plt.plot(J[:q], Kt[:q], label='P/D={0}'.format(round(PoDs[i],2)), linestyle='solid', color=colors[i])
        plt.plot(J[:q], 5*Kq[:q], linestyle='dotted', color=colors[i])
        plt.plot(J[:q], eta0[:q], linestyle='dashed', color=colors[i])
        plt.text(J[list(eta0).index(max(eta0))]-0.1, max(eta0)+0.05, 'P/D='+str(PoDs[i]))
    plt.xlabel('Advance parameter $J$')
    plt.ylabel('$K_T$ (solid), $5K_Q$ (dotted), $\eta_0$ (dashed)')
    plt.legend()
    plt.title('Open-water curves for B-series $A_E/A_0=$' + str(EAR)+', $Z=$' + str(int(Z)) +' at Re = ' +str(Re))
    plt.show()
