
from PIL import Image

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

"""
load data
"""

# Sa_output.txt 파일 읽기
with open('Sa_0.txt', 'r') as sa_file:
    sa = sa_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
sa_float = np.array([list(map(float, line.split())) for line in sa])


# g_eig.txt 파일 읽기
with open('g_0.txt', 'r') as g_file:
    g_eig = g_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
g_eig_float = np.array([list(map(float, line.split())) for line in g_eig])

# coef.txt 파일 읽기
with open('coef_0.txt', 'r') as coef_file:
    coef = coef_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
coef_float = np.array([list(map(float, line.split())) for line in coef])

# CR0098.txt 파일 읽기 (target spectrum)
with open('Sa_asce.txt', 'r') as cr_file:
    asce = cr_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
sa_asce = np.array([list(map(float, line.split())) for line in asce])

ngm = len(g_eig_float.transpose())

"""
define functions
"""

def save_gif_PIL(outfile, files, fps=5, loop=0):
    "Helper function for saving GIFs"
    imgs = [Image.open(file) for file in files]
    imgs[0].save(fp=outfile, format='GIF', append_images=imgs[1:], save_all=True, duration=int(1000/fps), loop=loop)
    

def rs_generate(Tn,t,dt,p):
    gamma, beta = 1/2, 1/4;
    mass, zeta = 1, 0.05;
    phat = np.zeros(len(p));
    disp = np.zeros(len(p));
    vel = np.zeros(len(p));
    acc = np.zeros(len(p));
    Sa_test = np.zeros(len(Tn));
    
    for jj in range(len(Tn)):
        c = 2 * zeta * mass * (2 * np.pi / Tn[jj])
        k = (2 * np.pi / Tn[jj]) ** 2

        acc[0] = p[0];
        delt = dt;
        a1 = mass / (beta * delt ** 2) + gamma * c / (beta * delt)
        a2 = mass / (beta * delt) + (gamma / beta - 1) * c
        a3 = (1 / 2 / beta - 1) * mass + delt * (gamma / 2 / beta - 1) * c
        khat = k + a1

        for kk in range(len(p) - 1):
            phat[kk + 1] = p[kk + 1] + a1 * disp[kk] + a2 * vel[kk] + a3 * acc[kk]
            disp[kk + 1] = phat[kk + 1] / khat
            vel[kk + 1] = gamma * (disp[kk + 1] - disp[kk]) / (beta * delt) + \
                          (1 - gamma / beta) * vel[kk] + delt * (1 - gamma / 2 / beta) * acc[kk]
            acc[kk + 1] = ((disp[kk + 1] - disp[kk]) / (beta * delt ** 2) - vel[kk] / (beta * delt) - \
                          (1 / 2 / beta - 1) * acc[kk])

        Sa_test[jj] = max(abs(disp)) * (2 * np.pi / Tn[jj]) ** 2
            
    return Sa_test
    

class FCN(nn.Module):
    "Defines a connected network"
    
    def __init__(self, N_INPUT, N_OUTPUT, N_HIDDEN, N_LAYERS):
        super().__init__()
        activation = nn.ReLU
        self.fcs = nn.Sequential(*[
                        nn.Linear(N_INPUT, N_HIDDEN),
                        activation()])
        self.fch = nn.Sequential(*[
                        nn.Sequential(*[
                            nn.Linear(N_HIDDEN, N_HIDDEN),
                            activation()]) for _ in range(N_LAYERS-1)])
        self.fce = nn.Linear(N_HIDDEN, N_OUTPUT)
        
    def forward(self, x):
        x = self.fcs(x)
        x = self.fch(x)
        x = self.fce(x)
        return x

"""
generate training data
"""

dt = 0.01;
t=np.arange(0, (len(g_eig_float[:,0]))/100, step=dt)


x_data = torch.Tensor(sa_float.transpose()); # pseudo response spectrum of real-recorded gms
y_data = torch.Tensor(coef_float.transpose()); # coefficients from SVD


## target spectrum
Tn = sa_asce[:,0];
sat = sa_asce[:,1]

# normal neural network
def plot_result(Tn,x,x_data,y_data,yh,xp=None):
    "Pretty plot training results"
    plt.figure(figsize=(8,4))
    plt.loglog(Tn,x, color="grey", linewidth=2, alpha=0.8, label="Exact solution")
    plt.loglog(Tn,0.9*x, color="grey", linewidth=1, alpha=0.8)
    plt.loglog(Tn,1.1*x, color="grey", linewidth=1, alpha=0.8)
    sa_try = rs_generate(Tn,t,dt,gm_try)
    plt.semilogx(Tn,sa_try,color='red',linewidth=0.5, label='NN matching')
    #plt.plot(Tn,yh, color="tab:blue", linewidth=4, alpha=0.8, label="Neural network prediction")


    l = plt.legend(loc=(1.01,0.34), frameon=False, fontsize="large")
    plt.setp(l.get_texts(), color="k")
    plt.xlim(0.01, 10)
    plt.ylim(0.01, 1)
    plt.text(1.065,0.7,"Training step: %i"%(i+1),fontsize="xx-large",color="k")
    #plt.axis("off")


# train standard neural network to fit training data

x = torch.Tensor(sat.transpose());

torch.manual_seed(2) # random seed 고정
model = FCN(len(sa_float),len(coef_float),10,2)
optimizer = torch.optim.Adam(model.parameters(),lr=5*1e-3)
files = []

max_epoch = 10000

loss_hist = np.zeros((max_epoch,1))
c_hist = np.zeros((max_epoch,ngm))

for i in range(10000):
    optimizer.zero_grad()
    yh = model(x_data)
    loss = torch.sqrt(torch.mean((yh-y_data)**2))# use mean squared error
    
    ytry = model(x).detach()
    ytry2 = np.array(ytry)
    
    loss_hist[i,:] = float(loss)
    c_hist[i,:] = ytry2.transpose()
        
    loss.backward()
    optimizer.step()
    
    # plot the result as training progresses
    if (i+1) % 200 == 0: 
        
        print(f"trial: {i+1}, loss= {float(loss):.4f}")
        
        yh = model(x).detach()
        
        c_try = np.array(yh);
        gm_try = g_eig_float@c_try
        
        plot_result(Tn,x,x_data,y_data,yh)
        
        file = "plots/nn_%.8i.png"%(i+1)
        plt.savefig(file, bbox_inches='tight', pad_inches=0.1, dpi=100, facecolor="white")
        files.append(file)
    
        if (i+1) % 200 == 0: plt.show()
        else: plt.close("all")
            
save_gif_PIL("nn.gif", files, fps=20, loop=0)

opt_point = np.argmin(loss_hist[:,-1]) - 1

opt_coefficient = c_hist[opt_point,:]

fit_gm = g_eig_float@opt_coefficient.transpose()

fit_rs = rs_generate(Tn,t,dt,fit_gm)

plt.figure()
plt.loglog(Tn,fit_rs)
plt.loglog(Tn,sa_asce[:,-1])
plt.loglog(Tn,0.9*sa_asce[:,-1])
plt.loglog(Tn,1.1*sa_asce[:,-1])
plt.show()

plt.figure(figsize=(8,3))
plt.plot(t,fit_gm,linewidth=0.5)
plt.xlabel('Time (s)')
plt.ylabel('Acc (g)')
plt.show()

pick = [int (i) for i in range(0,ngm)]

plt.figure(figsize=(8,3))
for i in range(0,ngm):
    if i==1:
        plt.scatter(pick,coef_float[:,i],s=10, color="grey", alpha=0.4,label='Real-recorded motions')
    else:
        plt.scatter(pick,coef_float[:,i],s=10, color="grey", alpha=0.4)
plt.scatter(pick,opt_coefficient, s=20, color='red',label='generated motion')
plt.xlim(0,80)
plt.ylim(-4, 4)
plt.xlabel('modes')
plt.ylabel('coefficient')
plt.legend()
plt.show()
