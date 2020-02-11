from tps import *
def exec_cases(fm,fmclass):
    if 'casename' in fm.__dict__.keys():
        case1_ = fm.case1
        case2_ = fm.case2
        pdict_ = fm.__dict__
        twocases(fmclass,pdict_,case1_,case2_,fm.casename)
        filename_ = "{a}/{b}.pdf".format(a=fm.directory,b=fm.casename)
        plt.savefig(filename_,dpi=400,bbox_inches='tight',pad_inches=0)   
