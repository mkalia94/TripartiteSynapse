from set_up import *

smallECS = ['smallECS_path1.mat','smallECS_path2.mat','smallECS_phys0.mat','smallECS_phys1.mat',
              'smallECS_phys2.mat','smallECS_phys3.mat','smallECS_phys4.mat','smallECS_phys5.mat' ]
largeECS = ['largeECS_path0.mat','largeECS_path11.mat','largeECS_path12.mat','largeECS_path2.mat',
              'largeECS_phys1.mat','largeECS_phys2.mat']
PScale2_largeECS = ['PScale2_largeECS_path1.mat','PScale2_largeECS_path2.mat','PScale2_largeECS_phys2.mat',
                     'PScale2_largeECS_phys1.mat']
PScale2_smallECS = ['PScale2_smallECS_path1.mat','PScale2_smallECS_phys2.mat',
                     'PScale2_smallECS_phys1.mat']
heights = [0.5]
widths = [1,1]
wspace_ = 0.8
hspace_ = 0.6
figsizex_ = sum(widths)+(len(widths)+1)*wspace_
figsizey_ = sum(heights)+(len(heights)+1)*hspace_
fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                          height_ratios=heights)
fig.subplots_adjust(wspace=wspace_)
fig.subplots_adjust(hspace=hspace_)


ax1 = fig.add_subplot(spec[0,0])
ax1.xaxis.set_tick_params(labelsize=8)
ax1.yaxis.set_tick_params(labelsize=8)
ax1.set_title(r'$\alpha_e=20$% (Small ECS)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax1.set_ylabel('Relative volume increase (%)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax1.set_xlabel(r'Available energy ($P_{\rm min}$, %)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax1.set_xlim(0,150)             
ax1.set_ylim(90,150)


for name_ in smallECS:
    data_ = sio.loadmat('BifFiles/{a}'.format(a=name_))
    xtemp = data_['x']
    eigs = data_['f']
    limpoints = [0,0]
    hopfpoints = [0,0]
    stable_data = [0,0]
    unstable_data= [0,0]
    ctr_old = 0
    for i in range(shape(xtemp)[1]):
        x_ = xtemp[0:19,i]
        x_ = append(x_,-65)
        x_ = append(x_,xtemp[19:21,i])
        p_ = xtemp[-1,i]*100
        Voli = fm.model(0,x_,'Voli')
        ctr_new = 0
        if i!=0:
            eig_ = eigs[:,i]
            for j in range(len(eig_)):
                if real(eig_[j])>0:
                    ctr_new = ctr_new + 1
            if ctr_new-ctr_old == 1:
                limpoints = vstack((limpoints,[Voli,p_]))
            elif ctr_new - ctr_old ==2:
                hopfpoints  = vstack((hopfpoints,[Voli,p_]))
            elif ctr_new - ctr_old == 0:
                if ctr_new == 0:
                    stable_data = vstack((stable_data,[Voli,p_]))
                else:
                    unstable_data = vstack((unstable_data,[Voli,p_]))
            ctr_old = ctr_new        
        else:
            if ctr_new == 0:
                stable_data = vstack((stable_data,[Voli,p_]))
            else:
                unstable_data = vstack((unstable_data,[Voli,p_]))
            ctr_temp = 0
            eig_ = eigs[:,0]
            for j in range(len(eig_)):
                if real(eig_[j])>0:
                    ctr_temp = ctr_temp + 1
            ctr_old = ctr_temp
        #stable_data = sort(stabledata,1)
        #unstable_data = sort(unstable_data,1)
    if 'phys' in name_:
        if len(shape(stable_data))!=1:
            ax1.plot(stable_data[1:,1],stable_data[1:,0],color='tab:blue')
        if len(shape(unstable_data))!=1:    
            ax1.plot(unstable_data[1:,1],unstable_data[1:,0],'--',color='tab:blue',)
    else:
        if len(shape(stable_data))!=1:
            ax1.plot(stable_data[1:,1],stable_data[1:,0],color='tab:red')
        if len(shape(unstable_data))!=1:    
            ax1.plot(unstable_data[1:,1],unstable_data[1:,0],'--',color='tab:red')
    if len(shape(limpoints))!=1:
        ax1.scatter(limpoints[1:,1],limpoints[1:,0],marker="*",color='black')
    if len(shape(hopfpoints))!=1:
        ax1.scatter(hopfpoints[1:,1],hopfpoints[1:,0],marker="v",color='black')

t1 = load('BifFiles/BaselineSmallECS/tfile1.npy')
y1 = load('BifFiles/BaselineSmallECS/yfile1.npy')
fm.tend=21.5
fm.perc = 0.4
Voli1 = fm.model(t1,y1,'Voli')
blockExp1 = fm.model(t1,y1,'blockerExp')*100
t2 = load('BifFiles/BaselineSmallECS/tfile2.npy')
y2 = load('BifFiles/BaselineSmallECS/yfile2.npy')
fm.tend=27
fm.perc= 0.4
blockExp2 = fm.model(t2,y2,'blockerExp')*100
Voli2 = fm.model(t2,y2,'Voli')

ax1.plot(blockExp2,Voli2,color='black',alpha=0.6,linewidth=2)
ax1.plot(blockExp1,Voli1,color='tab:green',linewidth=2)
arrow_dist = range(int(len(blockExp1)/6),len(blockExp1)-1,int(len(blockExp1)/6))
for val in arrow_dist:
    ax1.arrow(blockExp1[val],Voli1[val],blockExp1[val+1]-blockExp1[val],Voli1[val+1]-Voli1[val])
arrow_dist = range(int(len(blockExp2)/6),len(blockExp2)-1,int(len(blockExp2)/6))
for val in arrow_dist:
    ax1.arrow(blockExp2[val],Voli2[val],blockExp2[val+1]-blockExp2[val],Voli2[val+1]-Voli2[val])
        
ax2 = fig.add_subplot(spec[0,1])
ax2.xaxis.set_tick_params(labelsize=8)
ax2.yaxis.set_tick_params(labelsize=8)
ax2.set_title(r'$\alpha_e=98$% (Large ECS)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax2.set_ylabel('Relative volume increase (%)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax2.set_xlabel(r'Available energy ($P_{\rm min}$, %)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax2.set_xlim(0,150)
ax2.set_ylim(90,150)


for name_ in largeECS:
    data_ = sio.loadmat('BifFiles/{a}'.format(a=name_))
    xtemp = data_['x']
    eigs = data_['f']
    limpoints = [0,0]
    hopfpoints = [0,0]
    stable_data = [0,0]
    unstable_data= [0,0]
    ctr_old = 0
    for i in range(shape(xtemp)[1]):
        x_ = xtemp[0:19,i]
        x_ = append(x_,-65)
        x_ = append(x_,xtemp[19:21,i])
        p_ = xtemp[-1,i]*100
        Voli = fm.model(0,x_,'Voli')
        ctr_new = 0
        if i!=0:
            eig_ = eigs[:,i]
            for j in range(len(eig_)):
                if real(eig_[j])>0:
                    ctr_new = ctr_new + 1
            if ctr_new-ctr_old == 1:
                limpoints = vstack((limpoints,[Voli,p_]))
            elif ctr_new - ctr_old ==2:
                hopfpoints  = vstack((hopfpoints,[Voli,p_]))
            elif ctr_new - ctr_old == 0:
                if ctr_new == 0:
                    stable_data = vstack((stable_data,[Voli,p_]))
                else:
                    unstable_data = vstack((unstable_data,[Voli,p_]))
            ctr_old = ctr_new        
        else:
            if ctr_new == 0:
                stable_data = vstack((stable_data,[Voli,p_]))
            else:
                unstable_data = vstack((unstable_data,[Voli,p_]))
            ctr_temp = 0
            eig_ = eigs[:,0]
            for j in range(len(eig_)):
                if real(eig_[j])>0:
                    ctr_temp = ctr_temp + 1
            ctr_old = ctr_temp
        #stable_data = sort(stabledata,1)
        #unstable_data = sort(unstable_data,1)
    if 'phys' in name_:
        if len(shape(stable_data))!=1:
            ax2.plot(stable_data[1:,1],stable_data[1:,0],color='tab:blue',lw=2)
        if len(shape(unstable_data))!=1:    
            ax2.plot(unstable_data[1:,1],unstable_data[1:,0],'--',color='tab:blue',lw=2)
    else:
        if len(shape(stable_data))!=1:
            ax2.plot(stable_data[1:,1],stable_data[1:,0],color='tab:red',lw=2)
        if len(shape(unstable_data))!=1:    
            ax2.plot(unstable_data[1:,1],unstable_data[1:,0],'--',color='tab:red',lw=2)
    if len(shape(limpoints))!=1:
        ax2.scatter(limpoints[1:,1],limpoints[1:,0],marker="*",color='black')
    if len(shape(hopfpoints))!=1:
        ax2.scatter(hopfpoints[1:,1],hopfpoints[1:,0],marker="v",color = 'black')

def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = [xdata.mean(),ydata.mean()]
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position[0])+np.absolute(ydata-position[1]))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate('',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="->", color=color),
        size=size
    )

        
t1 = load('BifFiles/BaselineLargeECS/tfile1.npy')
y1 = load('BifFiles/BaselineLargeECS/yfile1.npy')
fm.tend=23
fm.perc = 0.4
Voli1 = fm.model(t1,y1,'Voli')
blockExp1 = fm.model(t1,y1,'blockerExp')*100
t2 = load('BifFiles/BaselineLargeECS/tfile2.npy')
y2 = load('BifFiles/BaselineLargeECS/yfile2.npy')
fm.tend=30
fm.perc= 0.4
blockExp2 = fm.model(t2,y2,'blockerExp')*100
Voli2 = fm.model(t2,y2,'Voli')
plt1=ax2.plot(blockExp2,Voli2,color='black',alpha=0.6,linewidth=2)[0]
plt2 = ax2.plot(blockExp1,Voli1,color='tab:green',alpha=0.6,linewidth=2)[0]
add_arrow(plt1,position = [40,105],size=7)
add_arrow(plt1,position = [80,100],size=7)
add_arrow(plt1,position = [80,120],size=7)
add_arrow(plt1,position = [100,120],size=7)
plt.savefig('BifFiles/Bif.pdf', format='pdf',bbox_inches='tight',pad_inches=0)
