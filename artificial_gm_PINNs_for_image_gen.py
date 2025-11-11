# PINNs based spectrum-matched earthquake motion generation
# proposed by Ju-Hyung Kim (jhkk@khu.ac.kr)

from PIL import Image

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

dataset = 0 # 0 = full set, 1~8 = subset

in_gm_name = "Sa_" + str(dataset) + ".txt"
in_g_eig_name = "g_" + str(dataset) + ".txt"
in_c_name = "coef_" + str(dataset) + ".txt"

# Sa_output.txt 파일 읽기
with open(in_gm_name, 'r') as sa_file:
    sa = sa_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
sa_float = np.array([list(map(float, line.split())) for line in sa])

# g_eig.txt 파일 읽기
with open(in_g_eig_name, 'r') as g_file:
    g_eig = g_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
g_eig_float = np.array([list(map(float, line.split())) for line in g_eig])


# coef.txt 파일 읽기
with open(in_c_name, 'r') as coef_file:
    coef = coef_file.readlines()

# 파일의 각 줄을 float 형식으로 변환하여 numpy 배열로 저장
coef_float = np.array([list(map(float, line.split())) for line in coef])

# Sa_asce.txt 파일 읽기 (target spectrum)
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
    phat = torch.zeros(len(p));
    disp = torch.zeros(len(p));
    vel = torch.zeros(len(p));
    acc = torch.zeros(len(p));
    Sa_test = torch.zeros(len(Tn));
    
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
            
        Sa_test[jj] = max(abs(disp.clone())) * (2 * np.pi / Tn[jj]) ** 2
        
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

dt = 0.01
t=np.arange(0, (len(g_eig_float[:,0]))/100, step=dt)

# interest period range only
int_period = range(0,111)

Tn = sa_asce[int_period,0]
## target spectrum
sat = sa_asce[int_period,1]

# training data
x_data = torch.Tensor(sa_float[int_period,:].transpose()) # pseudo response spectrum of real-recorded gms
y_data = torch.Tensor(coef_float.transpose()) # coefficients from SVD

def plot_result(Tn,x,x_data,y_data,yh,xp=None):
    "Pretty plot training results"
    plt.figure(figsize=(8,4))
    plt.loglog(Tn,x, color="grey", linewidth=2, alpha=0.8, label="Exact solution")
    plt.loglog(Tn,0.9*x, color="grey", linewidth=1, alpha=0.8)
    plt.loglog(Tn,1.1*x, color="grey", linewidth=1, alpha=0.8)
    plt.loglog(Tn,sa_pred,color='red',linewidth=0.5, label="PINNs matching")
    plt.scatter(Tn[samp], sa_pred[samp], s=60, color="tab:orange", alpha=0.4, label='Random points')
    l = plt.legend(loc=(1.01,0.34), frameon=False, fontsize="large")
    plt.setp(l.get_texts(), color="k")
    plt.xlim(0.01, 10)
    plt.ylim(0.01, 1)
    plt.text(1.065,0.7,"Training step: %i"%(i+1),fontsize="xx-large",color="k")
    #plt.axis("off")


# test data (target data)
x = torch.Tensor(sat)

torch.manual_seed(2) # fix random seed for reproducibility
model = FCN(len(sa_float[int_period,:]),len(coef_float),10,2)
optimizer = torch.optim.Adam(model.parameters(),lr=5*1e-2)
files = []

# pick: 14 periods between 0.2 s to 1.5 s
samp = np.array([0, 7, 13, 19, 21, 24, 26, 28, 30, 31, 32, 33, 34, 35]) + 37 # T=0.2:0.1:1.5

max_epoch = 40 # maximum iteration 

loss_hist = np.zeros((max_epoch,3))
c_hist = np.zeros((max_epoch,ngm))

for i in range(max_epoch):
    
    print('iter =', i+1)
      
    optimizer.zero_grad(set_to_none = True)
    yh = model(x_data)
    loss1 = torch.mean((yh-y_data)**2)# use mean squared error
    
    ytry = model(x)
    
    gm_tmp = torch.Tensor(g_eig_float)@ytry
    
    # data format
    Tn = torch.Tensor(Tn)
    t = torch.Tensor(t)

    sa_tmp = rs_generate(Tn[samp],t,dt,gm_tmp)
    
    # in-place operations error should be fixed
    
    loss2 = 100 * torch.mean(torch.Tensor((torch.Tensor(sat[samp])-sa_tmp)**2))
    
    loss = loss1 + loss2
    loss.backward()
    optimizer.step()

    # save data (eigen motion coefficients and loss function)
    c_hist[i,:] = np.array(model(x).detach()).transpose()
    loss_hist[i,:] = [float(loss1), float(loss2), float(loss)]
    
    # plot the result as training progresses
    if (i+1) % 2 == 0: 
        
        print(f"trial: {i+1}, loss1= {float(loss1):.4f}, loss2= {float(loss2):.4f}, loss= {float(loss):.4f}")
        
        yh = model(x).detach()
        gm_pred = torch.Tensor(g_eig_float)@yh
        sa_pred=rs_generate(Tn,t,dt,gm_pred)
        plot_result(Tn,x,x_data,y_data,yh)
        
        file = "plots/pinns0_%.8i.png"%(i+1)
        plt.savefig(file, bbox_inches='tight', pad_inches=0.1, dpi=100, facecolor="white")
        files.append(file)
    
        if (i+1) % 2 == 0: plt.show()
        else: plt.close("all")
            
save_gif_PIL("pinns0.gif", files, fps=6, loop=0)

opt_point = np.argmin(loss_hist[:i,-1]) - 1

opt_coefficient = c_hist[opt_point,:]

fit_gm = g_eig_float@opt_coefficient.transpose()

# selected tn (to plot pseudo RS)

fit_rs = rs_generate(Tn,t,dt,fit_gm)

plt.figure()
plt.loglog(Tn,sat,color='black')
plt.loglog(Tn,0.9*sat,color='black')
plt.loglog(Tn,1.1*sat,color='black')
plt.loglog(Tn,fit_rs,color='red')
plt.ylim(0.01, 1)
plt.xlim(0.01, 10)
plt.show()

plt.figure()
plt.semilogx(Tn,sat,color='black')
plt.semilogx(Tn,0.9*sat,color='black')
plt.semilogx(Tn,1.1*sat,color='black')
plt.semilogx(Tn,fit_rs,color='red')
plt.ylim(0, 1)
plt.xlim(0.01, 10)
plt.show()

plt.figure(figsize=(8,3))
plt.plot(t,fit_gm,linewidth=0.5)
plt.xlim(0, 80)
# plt.ylim(-0.3,0.3)
plt.xlabel('Time (s)')
plt.ylabel('Acc (g)')
plt.show()


# number of motions (from 0)
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

abs_u = np.max(abs(g_eig_float), axis=0)

outt=abs_u*abs(opt_coefficient)
# outt = abs(opt_coefficient)

# sort coefficient in descending orderto identify the number of governing motions
outt_cum = np.cumsum(np.sort(outt)[::-1])

plt.figure()
plt.plot(abs(outt))

plt.figure()
plt.plot(abs(outt_cum)/outt_cum[-1])

# save data
out_gm_name = "output\out_gm_" + str(dataset) + ".txt"
out_c_name = "output\out_c_" + str(dataset) + ".txt"
out_sa_name = "output\out_sa_" + str(dataset) + ".txt"

out_c_hist_name = "output\out_c_hist_" + str(dataset) + ".txt"
out_loss_name = "output\out_loss_" + str(dataset) + ".txt"

np.savetxt(out_gm_name,fit_gm)
np.savetxt(out_c_name,opt_coefficient)
np.savetxt(out_sa_name,fit_rs)

np.savetxt(out_c_hist_name,c_hist)
np.savetxt(out_loss_name,loss_hist)