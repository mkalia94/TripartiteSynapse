from tps import *

def plottwoaxes(fm,t,y,y1name,y2name,title,fig,ax1):
    title1 = title
    title2 = title
    tnew = arange(fm.t0, fm.tfinal, 1e-2)
    tnew = tile(tnew, (2, 1))
    blockerExp = fm.model(array(t),y,'blockerExp')
    tstart_ = 0
    tend_ = 0
    tstartfine_ = 0
    tendfine_ = 0
    # fm.tstart = fm.tstart - fm.t0
    # fm.tend = fm.tend - fm.t0

    if type(y1name).__name__ == 'dict':
        if "scale" in y1name:
            ax1scale = y1name["scale"]
        else:
            ax1scale=False            
        if "scale" in y2name:
            ax2scale = y2name["scale"]
        else:
            ax2scale=False
        y1name = y1name["plot"]
        y2name = y2name["plot"]
    else:
        ax1scale = False
        ax2scale = False
    if ax1scale:
        ax1.set_ylim(ax1scale[0],ax1scale[1])
    if 'breakaxis' not in fm.__dict__.keys():
        ax1.set_xlim(fm.t0, fm.tfinal)
    for i in range(shape(t)[0]):
        if abs(blockerExp[i]-fm.perc_gray)>1e-2:
            if tstart_ == 0:
                tstart_ = t[i]
            else:
                tend_ = 1
                if abs(blockerExp[i]-fm.perc)<1e-2:
                    if tstartfine_ ==0:
                        tstartfine_ = t[i]
                    else:
                        tendfine_ = 1
                else:
                    if tendfine_ == 1:
                        tendfine_ = t[i]
        else:
            if tend_ == 1:
                tend_ = t[i]
    if tend_ == 1:
        tend_ = fm.tfinal
    ax1.xaxis.set_tick_params(labelsize=6)
    ax1.yaxis.set_tick_params(labelsize=6)
    tx1 = ax1.yaxis.get_offset_text()
    tx1.set_fontsize(2)
    ax1.axvspan(fm.tstart_old,fm.tend_old,color='gray',alpha=0.5)    
    if 'astblock' in fm.__dict__.keys():
        val = fm.astblock
        ax1.axvspan(val[0], val[1], color='red',
                    alpha=0.2, lw=0, label='Astrocyte blocked')
    if 'block' in fm.__dict__.keys():
        dict_ = fm.block
        for key in dict_:
            val = dict_[key]
            ax1.axvspan(val[0], val[1], color='forestgreen',
                    alpha=0.2, lw=0)
    minploty1 = 1e6    
    for plotname in y1name:
        y1 = fm.model(array(t),y,plotname)
        #if max(y1)-min(y1)<1.5:
            #ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.2e'))
        if min(y1)<minploty1:
            minploty1 = min(y1)
        #ax1 .set_xlabel('time (in min)')
        if plotname[-1] == 'i':
            ax1.plot(array(t), y1,color='tab:blue', label="Neuron")
            #ax1.set_ylabel(title1, color='blue')
            #ax1.tick_params(axis='y', labelcolor='blue')
        elif plotname[-1] == 'e':
            ax1.plot(array(t), y1, color='forestgreen', label="ECS")
            #ax1.set_ylabel(title1, color='forestgreen')
            #ax1.tick_params(axis='y', labelcolor='forestgreen')
        elif plotname[-1] == 'g':
            ax1.plot(array(t), y1, color='orange', label="Ast.")
            #ax1.set_ylabel(title1, color='orange')
            #ax1.tick_params(axis='y', labelcolor='orange')
        elif plotname[-1] == 'c':
            ax1.plot(array(t), y1, color='forestgreen', label="Cleft")
            #ax1.set_ylabel(title1, color='forestgreen')
            #ax1.tick_params(axis='y', labelcolor='forestgreen')
        else:
            ax1.plot(array(t),y1,color='black',lw=0.5)
        ax1.set_title(title, fontdict={'fontsize': 8, 'fontweight': 'medium'})
        ax1.set_ylabel('', fontdict={'fontsize': 6, 'fontweight': 'medium'})
    ax1.ticklabel_format(axis='y',style='scientific',useOffset=True,scilimits=(-2.5,2.5),useMathText=True)
    ax1.ticklabel_format(axis='x',style='scientific',useOffset=True,scilimits=(-3,3),useMathText=True)
    fm.labeloffset(ax1,"y")    
        #ax1.title.set_text(title,fontsize=6)
    if y2name != []:
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        if ax2scale:
            ax2.set_ylim(ax2scale[0],ax2scale[1])
        ax2.set_xlim(fm.t0, fm.tfinal)
        ax2.xaxis.set_tick_params(labelsize=6)
        ax2.yaxis.set_tick_params(labelsize=6)
        tx2 = ax2.yaxis.get_offset_text()
        tx2.set_fontsize(8)
        
        #color = 'tab:blue'
        for plotname in y2name:
            y2 = fm.model(array(t)-fm.t0,y,plotname)
            #if max(y2)-min(y2)<1.5:
                #ax2.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.5e'))
                #ax2.ticklabel_format(useOffset=True)
            #ax2 .set_xlabel('time (in min)')
            if plotname[-1] == 'i':
                ax2.plot(array(t)-fm.t0, y2, label="Neuron")
                #ax2.set_ylabel(title2, color='blue')
                ax2.tick_params(axis='y', labelcolor='blue')
            elif plotname[-1] == 'e':
                ax2.plot(array(t)-fm.t0, y2, color='forestgreen', label="ECS")
                #ax2.set_ylabel(title2, color='forestgreen')
                ax2.tick_params(axis='y', labelcolor='forestgreen')
            elif plotname[-1] == 'g':
                ax2.plot(array(t)-fm.t0, y2, color='orange', label="Ast.")
                #ax2.set_ylabel(title2, color='orange')
                ax2.tick_params(axis='y', labelcolor='orange')
            elif plotname[-1] == 'c':
                ax2.plot(array(t)-fm.t0, y2, color='forestgreen', label="Cleft")
                #ax2.set_ylabel(title2, color='forestgreen')
                ax2.tick_params(axis='y', labelcolor='forestgreen')
            else:
                ax2.plot(array(t)-fm.t0,y2,color='black',lw=0.5)
        ax2.set_ylabel('', fontdict={'fontsize': 6, 'fontweight': 'medium'})
        ax2.ticklabel_format(axis='y',style='scientific',useOffset=True,scilimits=(-2.5,2.5),useMathText=True)
        ax2.ticklabel_format(axis='x',style='scientific',useOffset=True,scilimits=(-3,3),useMathText=True)
        fm.labeloffset(ax2,"y")
    #if minploty1<0:
    #    ax1.plot([tstartfine_,tendfine_],[minploty1*1.05,minploty1*1.05],color='black')
    #else:
    #    ax1.plot([tstartfine_,tendfine_],[minploty1*0.95,minploty1*0.95],color='black')            
