from tps import *

widths = [1,1,1,1]
heights= [0.25,1,1,1,1,1,1]
wspace_ = 1.2
hspace_ = 0.6
figsizex_ = sum(widths)+(len(widths)+1)*wspace_
figsizey_ = sum(heights)+(len(heights)+1)*hspace_

#Case 1
paramdict['s'] = False
paramdict['m'] = False
paramdict['b'] = False
paramdict['nochargecons'] = False
paramdict['nogates'] = False
paramdict['tstart'] = 10
paramdict['tend'] = 13
paramdict['tfinal'] = 20
paramdict['perc'] = 0.4
paramdict['alphae0'] = 0.7
fm = fmclass(paramdict)
fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
               fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
            fm.Wi0, fm.Wg0]  
t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

paramdict['tend'] =  20
paramdict['tfinal'] = 30
fm2 = fmclass(paramdict)
fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
            fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
               fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
            fm2.Wi0, fm2.Wg0]
t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                          height_ratios=heights)
fig.subplots_adjust(wspace=wspace_)
fig.subplots_adjust(hspace=hspace_)
plotall(fm,t1,y1,fig,spec,1)
plotall(fm2,t2,y2,fig,spec,2)
plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
plt.savefig('Case1.pdf',dpi=400,bbox_inches='tight',pad_inches=0)
plt.clf()

# # Case 2
# paramdict['s'] = False
# paramdict['m'] = False
# paramdict['b'] = False
# paramdict['nochargecons'] = False
# paramdict['nogates'] = False
# paramdict['tstart'] = 200
# paramdict['tend'] = 500
# paramdict['tfinal'] = 3
# paramdict['excite'] = [1,2]
# paramdict['perc'] = 0.4
# paramdict['alphae0'] = 0.2

# fm = fmclass(paramdict)
# fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
#             fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
#                fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
#             fm.Wi0, fm.Wg0]  
# t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

# paramdict['astblock'] = [1,2] 
# fm2 = fmclass(paramdict)
# fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
#             fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
#                fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
#             fm2.Wi0, fm2.Wg0]
# t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

# fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
# spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
#                           height_ratios=heights)
# fig.subplots_adjust(wspace=wspace_)
# fig.subplots_adjust(hspace=hspace_)
# plotall(fm,t1,y1,fig,spec,1)
# plotall(fm2,t2,y2,fig,spec,2)
# plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
# plt.savefig('Case2.pdf',dpi=400,bbox_inches='tight',pad_inches=0)  


# # Case 3
# paramdict['s'] = False
# paramdict['m'] = False
# paramdict['b'] = False
# paramdict['nochargecons'] = False
# paramdict['nogates'] = False
# paramdict['tstart'] = 20
# paramdict['tend'] = 45
# paramdict['tfinal'] = 70
# paramdict['perc'] = 0.3
# paramdict['alphae0'] = 0.2

# fm = fmclass(paramdict)
# fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
#             fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
#                fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
#             fm.Wi0, fm.Wg0]  
# t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

# paramdict['alphae0'] = 0.98 
# fm2 = fmclass(paramdict)
# fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
#             fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
#                fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
#             fm2.Wi0, fm2.Wg0]
# t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

# fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
# spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
#                           height_ratios=heights)
# fig.subplots_adjust(wspace=wspace_)
# fig.subplots_adjust(hspace=hspace_)
# plotall(fm,t1,y1,fig,spec,1)
# plotall(fm2,t2,y2,fig,spec,2)
# plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
# plt.savefig('Case3.pdf',dpi=400,bbox_inches='tight',pad_inches=0)  

# # Case 4
# paramdict['s'] = False
# paramdict['m'] = False
# paramdict['b'] = False
# paramdict['nochargecons'] = False
# paramdict['nogates'] = False
# paramdict['tstart'] = 20
# paramdict['tend'] = 170
# paramdict['tfinal'] = 200
# paramdict['perc'] = 0.3
# paramdict['alphae0'] = 0.2
# #paramdict['pumpScaleNeuron'] = 
# #paramdict['pumpScaleAst'] = 2.2

# fm = fmclass(paramdict)
# fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
#             fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
#                fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
#             fm.Wi0, fm.Wg0]  
# t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

# paramdict['alphae0'] = 0.98

# fm2 = fmclass(paramdict)
# fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
#             fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
#                fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
#             fm2.Wi0, fm2.Wg0]
# t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

# fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
# spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
#                           height_ratios=heights)
# fig.subplots_adjust(wspace=wspace_)
# fig.subplots_adjust(hspace=hspace_)
# plotall(fm,t1,y1,fig,spec,1)
# plotall(fm2,t2,y2,fig,spec,2)
# plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
# plt.savefig('Case4.pdf',dpi=400,bbox_inches='tight',pad_inches=0)  

# # Case 5
# paramdict['s'] = False
# paramdict['m'] = False
# paramdict['b'] = False
# paramdict['nochargecons'] = False
# paramdict['nogates'] = False
# paramdict['tstart'] = 20
# paramdict['tend'] = 170
# paramdict['tfinal'] = 200
# paramdict['perc'] = 0.3
# paramdict['alphae0'] = 0.2
# paramdict['pumpScaleNeuron'] = 2.2
# paramdict['pumpScaleAst'] = 2.2

# fm = fmclass(paramdict)
# fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
#             fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
#                fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
#             fm.Wi0, fm.Wg0]  
# t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

# paramdict['alphae0'] = 0.98 
# fm2 = fmclass(paramdict)
# fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
#             fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
#                fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
#             fm2.Wi0, fm2.Wg0]
# t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

# fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
# spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
#                           height_ratios=heights)
# fig.subplots_adjust(wspace=wspace_)
# fig.subplots_adjust(hspace=hspace_)
# plotall(fm,t1,y1,fig,spec,1)
# plotall(fm2,t2,y2,fig,spec,2)
# plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
# plt.savefig('Case5.pdf',dpi=400,bbox_inches='tight',pad_inches=0)  

# # Case 6
# paramdict['s'] = False
# paramdict['m'] = False
# paramdict['b'] = False
# paramdict['nochargecons'] = False
# paramdict['nogates'] = False
# paramdict['tstart'] = 20
# paramdict['tend'] = 170
# paramdict['tfinal'] = 200
# paramdict['perc'] = 0.3
# paramdict['alphae0'] = 0.2
# paramdict['pumpScaleNeuron'] = 2.8
# paramdict['pumpScaleAst'] = 2.8

# fm = fmclass(paramdict)
# fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
#             fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
#                fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
#             fm.Wi0, fm.Wg0]  
# t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

# paramdict['alphae0'] = 0.98 
# fm2 = fmclass(paramdict)
# fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
#             fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
#                fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
#             fm2.Wi0, fm2.Wg0]
# t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

# fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
# spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
#                           height_ratios=heights)
# fig.subplots_adjust(wspace=wspace_)
# fig.subplots_adjust(hspace=hspace_)
# plotall(fm,t1,y1,fig,spec,1)
# plotall(fm2,t2,y2,fig,spec,2)
# plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
# plt.savefig('Case6.pdf',dpi=400,bbox_inches='tight',pad_inches=0)

# Case 7
paramdict['s'] = False
paramdict['m'] = False
paramdict['b'] = False
paramdict['nochargecons'] = False
paramdict['nogates'] = False
paramdict['tstart'] = 20
paramdict['tend'] = 170
paramdict['tfinal'] = 200
paramdict['perc'] = 0.3
paramdict['alphae0'] = 0.2
paramdict['pumpScaleNeuron'] = 3
paramdict['pumpScaleAst'] = 3

fm = fmclass(paramdict)
fm.initvals = [fm.NNai0, fm.NKi0, fm.NCli0, fm.m0, fm.h0, fm.n0, fm.NCai0,
            fm.NN0, fm.NR0, fm.NR10, fm.NR20, fm.NR30, fm.NI0,
               fm.ND0, fm.NNag0, fm.NKg0, fm.NClg0, fm.NCag0, fm.NGlug0, fm.Vi0,
            fm.Wi0, fm.Wg0]  
t1,y1 = solver(fm,fm.t0,fm.tfinal,fm.initvals)

paramdict['alphae0'] = 0.98 
fm2 = fmclass(paramdict)
fm2.initvals = [fm2.NNai0, fm2.NKi0, fm2.NCli0, fm2.m0, fm2.h0, fm2.n0, fm2.NCai0,
            fm2.NN0, fm2.NR0, fm2.NR10, fm2.NR20, fm2.NR30, fm2.NI0,
               fm2.ND0, fm2.NNag0, fm2.NKg0, fm2.NClg0, fm2.NCag0, fm2.NGlug0, fm2.Vi0,
            fm2.Wi0, fm2.Wg0]
t2,y2 = solver(fm2,fm2.t0,fm2.tfinal,fm2.initvals)

fig = plt.figure(constrained_layout=True,figsize=(figsizex_,figsizey_))
spec = fig.add_gridspec(ncols=len(widths), nrows=len(heights), width_ratios=widths,
                          height_ratios=heights)
fig.subplots_adjust(wspace=wspace_)
fig.subplots_adjust(hspace=hspace_)
plotall(fm,t1,y1,fig,spec,1)
plotall(fm2,t2,y2,fig,spec,2)
plt.plot([0.505, 0.505], [0.2, 0.9], color='black',lw=3,alpha = 0.2,transform=plt.gcf().transFigure, clip_on=False)
plt.savefig('Case7.pdf',dpi=400,bbox_inches='tight',pad_inches=0)  
