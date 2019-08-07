from fm_class import *
from scipy.optimize import root
import matplotlib.pyplot as plt


# Note that the full model does not satisfy a Gibbs-Donnan equilibrium. This is due to the equations for 
# glutamate, that prevent such an equilibrium to exist.
# Thus, we only consider the 

## Free parameters
NaCi0 = 13
KCi0 = 145
ClCi0 = 7
CaCi0 = 0.1*1e-3 # Assumption based on Oschmann model
GluCi0 = 3 # From 'Maintaining the presynaptic glutamate...Marx, Billups...2015'
NaCe0 = 152
KCe0 = 3
ClCe0 = 135
CaCc0 = 1.8 # Oschmann
GluCc0 = 1*1e-4 # Attwell Barbour Szatkowski... Non vesicular release...'93 (Neuron) 
NaCg0 = 13
KCg0 = 80
ClCg0 = 35
CaCg0 = 0.05*1e-3 # From 'Plasmalemmal so/ca exchanger...Reyes et al...2012'
GluCg0 = 2 # Empirical assumption
Wi0 = 2
Wg0 = 1.7
VolPreSyn = 1*1e-3
VolPAP = 1*1e-3 # Empirical
Volc = 1*1e-3 # Empirical

alphae0 = 0.2
 
initvals_temp = [NaCi0,KCi0,ClCi0,CaCi0,GluCi0,NaCe0,KCe0,ClCe0,CaCc0,GluCc0,NaCg0,KCg0,\
ClCg0,CaCg0,GluCg0,Wi0,Wg0,VolPreSyn,VolPAP,Volc]
testparams = [blockerScaleAst, blockerScaleNeuron, \
pumpScaleAst, pumpScaleNeuron, \
nkccScale, kirScale,gltScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,alphae0,choicee,astroblock]
sm = smclass(initvals_temp,testparams,1)
 

## APPROX GIBBS DONNAN
def approxGD(input):
    NaCi = input[0]
    KCi = input[1]
    ClCi = input[2]
    NaCg = input[3]
    KCg = input[4]
    ClCg = input[5]
    Wi = input[6]
    Wg = input[7]
    
    NNa = NaCi*Wi
    NK = KCi*Wi
    NCl = ClCi*Wi
    NNag = NaCg*Wg
    NKg = KCg*Wg
    NClg = ClCg*Wg
    
    NNae = sm.CNa - NNa - NNag
    NKe = sm.CK - NK - NKg
    NCle = sm.CCl - NCl - NClg
    We = sm.Wtot - Wi - Wg
    NaCe = NNae/We
    KCe = NKe/We
    ClCe = NCle/We

    
    # Voltages
    V=sm.F/sm.C*(NNa+NK-NCl-sm.NAi)
    Vg = sm.F/sm.Cg*(NNag + NKg + sm.NBg - sm.NAg -NClg)
    
    equations = [NaCi*KCe - KCi*NaCe,\
                 NaCi*ClCi - ClCe*NaCe,\
                 NaCg*KCe - KCg*NaCe,\
                 KCg*ClCg - ClCe*KCe,\
                 NaCi+KCi+ClCi+sm.NAi/Wi - (NaCe + KCe + ClCe + sm.NAe/We + sm.NBe/We),\
                 NaCe + KCe + ClCe + sm.NAe/We + sm.NBe/We - (NaCg + KCg + ClCg + sm.NAg/Wg + sm.NBg/Wg),\
                 (NaCi*Wi+KCi*Wi-ClCi*Wi-sm.NAi),\
                 (NaCg*Wg+KCg*Wg-ClCg*Wg + sm.NBg - sm.NAg)]
    return equations

approx_initvals = array([10,80,70,10,80,80,3,3])
initvals1 = approx_initvals  + random.normal(approx_initvals,0.2)
sol = root(approxGD,initvals1)
initvals = sol.x


def GD(input):
    NaCi = input[0]
    KCi = input[1]
    ClCi = input[2]
    NaCg = input[3]
    KCg = input[4]
    ClCg = input[5]
    Wi = input[6]
    Wg = input[7]
    
    NNa = NaCi*Wi
    NK = KCi*Wi
    NCl = ClCi*Wi
    NNag = NaCg*Wg
    NKg = KCg*Wg
    NClg = ClCg*Wg
    
    NNae = sm.CNa - NNa - NNag
    NKe = sm.CK - NK - NKg
    NCle = sm.CCl - NCl - NClg
    We = sm.Wtot - Wi - Wg
    NaCe = NNae/We
    KCe = NKe/We
    ClCe = NCle/We

    
    # Voltages
    V=sm.F/sm.C*(NNa+NK-NCl-sm.NAi)
    Vg = sm.F/sm.Cg*(NNag + NKg + sm.NBg - sm.NAg -NClg)
    
    equations = [NaCi*KCe - KCi*NaCe,\
                 NaCi*ClCi - ClCe*NaCe,\
                 NaCg*KCe - KCg*NaCe,\
                 KCg*ClCg - ClCe*KCe,\
                 NaCi*Wi*We+KCi*Wi*We+ClCi*Wi*We+sm.NAi*We - (NaCe*We*Wi + KCe*We*Wi + ClCe*We*Wi + sm.NAe*Wi + sm.NBe*Wi),\
                 NaCe*Wg*We + KCe*Wg*We + ClCe*Wg*We + sm.NAe*Wg + sm.NBe*Wg - (NaCg*Wg*We + KCg*Wg*We + ClCg*Wg*We + sm.NAg*We + sm.NBg*We),\
                 KCe - KCi*exp(sm.F**2/sm.C/sm.R/sm.T*(NaCi*Wi+KCi*Wi-ClCi*Wi-sm.NAi)),\
                 NaCe - NaCg*exp(sm.F**2/sm.Cg/sm.R/sm.T*(NaCg*Wg+KCg*Wg-ClCg*Wg + sm.NBg - sm.NAg)),]
    return equations

sol2 = root(GD,initvals)
succ = sol2.success


if succ == True:
    disp(sol2)
else:
    disp('Unsolved')

# 
# NaCi = tf.get_variable("NaCi",initializer=tf.constant(100.0))
# KCi = tf.get_variable("KCi",initializer=tf.constant(200.0))
# ClCi = tf.get_variable("ClCi",initializer=tf.constant(100.0))
# NaCg = tf.get_variable("NaCg",initializer=tf.constant(200.0))
# KCg = tf.get_variable("KCg",initializer=tf.constant(100.0))
# ClCg = tf.get_variable("ClCg",initializer=tf.constant(200.0))
# Wi = tf.get_variable("Wi",initializer=tf.constant(2.0))
# Wg = tf.get_variable("Wg",initializer=tf.constant(3.0))
# 
# 
# def computeGibbsDonnan(input):
#     NNae = sm.CNa - NaCi*Wi - NaCg*Wg
#     NKe = sm.CK - KCi*Wi - KCg*Wg
#     NCle = sm.CCl - ClCi*Wi -ClCg*Wg
#     We = sm.Wtot - Wi - Wg 
#     NaCe = NNae/We
#     KCe = NKe/We
#     ClCe = NCle/We
# 
#     
#     equations = [NaCi*KCe - KCi*NaCe,\
#                  KCi*ClCi - ClCe*KCe,\
#                  sm.R*sm.T/sm.F*tf.log(NaCe/NaCi) - sm.F/sm.C*(NaCi*Wi+KCi*Wi-ClCi*Wi-sm.NAi),\
#                  NaCg*KCe - KCg*NaCe,\
#                  KCg*ClCg - ClCe*KCe,\
#                  sm.R*sm.T/sm.F*tf.log(NaCe/NaCg) - sm.F/sm.C*(NaCg*Wg+KCg*Wg-ClCg*Wg + sm.NBg - sm.NAg),\
#                  NaCi+KCi+ClCi+sm.NAi/Wi - (NaCe + KCe + ClCe + sm.NAe/We),\
#                  NaCe + KCe + ClCe + sm.NAe/We - (NaCg + KCg + ClCg + sm.NAg/Wg + sm.NBg/Wg)]
#                  
#     return equations             
# 
# 
# X = tf.placeholder("float",[8,None])
# Y = tf.placeholder("float",[8])
# logits = computeGibbsDonnan(X)
# 
# numits = 5000
# loss_op = tf.reduce_mean(tf.losses.mean_squared_error(logits,Y))  
# global_step = tf.Variable(0, trainable=False)
# learning_rate = tf.train.exponential_decay(0.01, global_step,
#                                            10, 0.96, staircase=True)
# optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
# train_op = optimizer.minimize(loss_op,global_step = global_step)
# init = tf.global_variables_initializer()
# sess = tf.InteractiveSession()
# sess.run(init)
# 
# ecs = arange(0.1,0.9,0.05)
# glia = arange(0.9,1.1,0.05)
# gdratio = zeros((size(ecs),size(glia)))
# 
# 
# 
# 
# for i in range(size(ecs)):
#     for j in range(size(glia)):
#         ecsratio = ecs[i]
#         gliaratio = glia[j]
#         Wi0 = 2.0
#         Wg0 = gliaratio*Wi0
#         We0 = ecsratio/(1-ecsratio)*Wi0 + ecsratio/(1-ecsratio)*Wg0 
#         sm.Wtot = Wi0 + Wg0 + We0
#         NaCi0 = 13.0
#         KCi0 = 145.0
#         ClCi0 = 7.0
#         NaCg0 = 13.0
#         KCg0 = 80.0
#         ClCg0 = 35.0
#         NNai0 = NaCi0*Wi0
#         NKi0 = KCi0*Wi0
#         NCli0 = ClCi0*Wi0
#         NNag0 = NaCg0*Wg0
#         NKg0 = KCg0*Wg0
#         NClg0 = ClCg0*Wg0
#         initvals = [NNai0,NKi0,NCli0,NNag0,NKg0,NClg0,Wi0,Wg0]
#         testparams = [blockerScaleAst, blockerScaleNeuron, \
#     pumpScaleAst, pumpScaleNeuron, \
#     nkccScale, kirScale, nka_na,nka_k,beta1, beta2, perc, tstart, tend,nkccblock_after,kirblock_after,ecsratio]
#         paramfile.parameters(sm,testparams,initvals)
#         initvals = 1*ones((8,1))
#         # initvals = [100,100,100,100,100,100,2,2]
#         # for k in range(numits):
#         #     xin = initvals
#         #     xout = zeros(8)
#         #     inputdict = {X: xin, Y: xout}
#         #     sess.run(train_op, feed_dict=inputdict)
#         #     loss = sess.run(loss_op, feed_dict=inputdict)
#         #     print('({0:2d},{1:2d}): \t iteration:{2:2d} \t loss:{3:.2f}'.format(i,j,k,loss))
#         #     if loss<1e-4:
#         #         gdratio[i,j] = Wi.eval()/Wg.eval()
#         #         break
#         #     
#         # 
#         succ = False
#         ctr = 0
#         while succ == False & ctr<11:
#             initvals1 = initvals + random.normal(initvals,0.1)
#             sol = root(approxGD,initvals1)
#             succ = sol.success
#             if min(sol.x)<0:
#                 succ = False
#             ctr = ctr + 1
#         if succ == True & (max(sol.x)<1000):
#             sol1 = sol.x
#             gdratio[i,j] = sol1[6]/sol1[7]
#             print('%d,%d done'.format([i]))
#         else:
#             print('fsolve didn\'t compute accurately')
#                 
# plt.imshow(gdratio)
# plt.show()