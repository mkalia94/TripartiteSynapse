from tps import *

def plottwoaxes(fm,t,y,y1name,y2name,title1,title2):
    fig, ax1 = plt.subplots()
    plt.rc('text', usetex=True)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=20)
    plt.locator_params(axis='y', nbins = 6)
    plt.locator_params(axis='x', nbins=3)
    if 'excite' in fm.__dict__.keys():
        val = fm.excite
        plt.axvspan(val[0], val[1], color='red',
                    alpha=0.5, lw=0, label='Neuron excited')
    for plotname in y1name:
        y1 = fm.model(array(t),y,plotname)
        ax1 .set_xlabel('time (in min)')
        if plotname[-1] == 'i':
            ax1.plot(t, y1,color='tab:blue', label="Neuron")
            ax1.set_ylabel(title1, color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')
        elif plotname[-1] == 'e':
            ax1.plot(t, y1, color='forestgreen', label="ECS")
            ax1.set_ylabel(title1, color='forestgreen')
            ax1.tick_params(axis='y', labelcolor='forestgreen')
        elif plotname[-1] == 'g':
            ax1.plot(t, y1, color='orange', label="Ast.")
            ax1.set_ylabel(title1, color='orange')
            ax1.tick_params(axis='y', labelcolor='orange')
        elif plotname[-1] == 'c':
            ax1.plot(t, y1, color='forestgreen', label="Cleft")
            ax1.set_ylabel(title1, color='forestgreen')
            ax1.tick_params(axis='y', labelcolor='forestgreen')
        else:
            ax1.plot(t,y1,color='black')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    #color = 'tab:blue'
    for plotname in y2name:
        y2 = fm.model(array(t),y,plotname)
        ax2 .set_xlabel('time (in min)')
        if plotname[-1] == 'i':
            ax2.plot(t, y2, label="Neuron")
            ax2.set_ylabel(title2, color='blue')
            ax2.tick_params(axis='y', labelcolor='blue')
        elif plotname[-1] == 'e':
            ax2.plot(t, y2, color='forestgreen', label="ECS")
            ax2.set_ylabel(title2, color='forestgreen')
            ax2.tick_params(axis='y', labelcolor='forestgreen')
        elif plotname[-1] == 'g':
            ax2.plot(t, y2, color='orange', label="Ast.")
            ax2.set_ylabel(title2, color='orange')
            ax2.tick_params(axis='y', labelcolor='orange')
        elif plotname[-1] == 'c':
            ax2.plot(t, y2, color='forestgreen', label="Cleft")
            ax2.set_ylabel(title2, color='forestgreen')
            ax2.tick_params(axis='y', labelcolor='forestgreen')
        else:
            ax2.plot(t,y2)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
