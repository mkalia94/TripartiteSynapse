dict_ = fm.plot
ctr = 0
size_ = dict_['size']
# Comment all lines till for loop to remove single file plotting
len_ = fm.plot.__len__()-1
if len_>1:
widths = list(ones(size_[0],'int'))
else:
widths = [1]
heights= list(ones(size_[1],'int'))
wspace_ = 0.8
if len(heights) == 1:
hspace_ = 0
else:
hspace_ = 0.8
figsizex_ = sum(widths)+(len(widths)+1)*wspace_
figsizey_ = sum(heights)+(len(heights))*hspace_
fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
height_ratios=heights)
fig.subplots_adjust(wspace=wspace_)
fig.subplots_adjust(hspace=hspace_)

specx = int(ctr/size_[0])
specy = ctr - int(ctr/size_[0])
ax = fig.add_subplot(spec[specx,specy])
if 'breakaxis' in fm.__dict__.keys():
    vals_ = fm.breakaxis 
    ax = brokenaxes(xlims=((vals_[0],vals_[1]),(vals_[2],vals_[3])),subplot_spec = spec[specx,specy])
else:
    ax = fig.add_subplot(spec[specx,specy])
    ax1_ = []
    ax2_ = []
for vals in plotdict["plot"]:
    if 'ax1' in vals:
        ax1_.append(vals)
    elif 'ax2' in vals:
        ax2_.append(vals)
if len(ax1_) == 0:
    plottwoaxes(fm,t,y,plotdict["plot"],[],keys,fig,ax)
else:
    if "ax1scale" in plotdict:
        ax1  = {"plot":ax1_,"scale":plotdict["ax1scale"]}
    else:
        ax1  = {"plot":ax1_}
    if "ax2scale" in plotdict:
        ax2  = {"plot":ax2_,"scale":plotdict["ax2scale"]}
    else:
        ax2  = {"plot":ax2_}    

    plottwoaxes(fm,t,y,ax1,ax2,keys,fig,ax)
if ctr == (len_-1) or ctr == (len_-2):
    ax.set_xlabel('time (min.)', fontdict={'fontsize': 8, 'fontweight': 'medium'})
    #fig.tight_layout()
    #plotfilename = '{a}/{b}.pdf'.format(a=directory,b=keys)
    #plt.savefig(plotfilename, format='pdf', bbox_inches='tight')
    ctr = ctr + 1
