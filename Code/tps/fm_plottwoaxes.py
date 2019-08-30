from tps import *

def plottwoaxes(fm,t,y,y1name,y2name,color1,color2):
    y1 = fm.model(array(t),y,y1name)
    y2 = fm.model(array(t),y,y2name)

    fig, ax1 = plt.subplots()

    plt.rc('text', usetex=True)
    plt.rc('font', size=20)
    plt.rc('axes', titlesize=20)

    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=3)

    #color = 'forestgreen'
    ax1.set_xlabel('time (in min)')
    ax1.set_ylabel(y1name, color=color1)
    ax1.plot(array(t),y1 , color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    #color = 'tab:blue'
    ax2.set_ylabel(y2name, color=color2)  # we already handled the x-label with ax1
    ax2.plot(array(t), y2, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
