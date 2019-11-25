from set_up import *

smallECS = ['smallECS_path1.mat','smallECS_path2.mat','smallECS_phys0.mat','smallECS_phys1.mat',
              'smallECS_phys2.mat','smallECS_phys3.mat','smallECS_phys4.mat','smallECS_phys5.mat' ]
largeECS = ['largeECS_path0.mat','largeECS_path11.mat','largeECS_path12.mat','largeECS_path2.mat'
              'largeECS_phys1.mat','largeECS_phys2.mat']
PScale2_largeECS = ['PScale2_largeECS_path1.mat','PScale2_largeECS_path2.mat','PScale2_largeECS_phys2.mat',
                     'PScale2_largeECS_phys1.mat']
PScale2_smallECS = ['PScale2_smallECS_path1.mat','PScale2_smallECS_phys2.mat',
                     'PScale2_smallECS_phys1.mat']
heights = [2]
widths = [2,2]
wspace_ = 0.8
hspace_ = 0.6
figsizex_ = sum(widths)+(len(widths)+1)*wspace_
figsizey_ = sum(heights)+(len(heights)+1)*hspace_
fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                          height_ratios=heights)
fig.subplots_adjust(wspace=wspace_)
fig.subplots_adjust(hspace=hspace_)


ax1 = fig.add_subplot(spec[specx,specy])
ax1.xaxis.set_tick_params(labelsize=8)
ax1.yaxis.set_tick_params(labelsize=8)
ax1.set_title('sdfdsf', fontdict={'fontsize': 8, 'fontweight': 'medium'})
ax1.set_ylabel('sdf', fontdict={'fontsize': 6, 'fontweight': 'medium'})

for name_ in smallECS:
    if 'path' in name_:
        xtemp = x['x']
        x_ = xtemp[0:19]
        x_ = append(x_,-65)
        x_ = append(x_,xtemp[19:22])
        Vm = fm.model(0,x_,'Vi')
        
