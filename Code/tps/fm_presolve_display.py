from tps import *
def presolve_display(fm):
    if 'excite' in fm.__dict__.keys():
        disp('Exciting neuron with constant {0:.2f}pA current for {1:.2f}s every {2:.2f}s...'.format(fm.excite[2],fm.excite[3],fm.excite[3]/60/(1-fm.excite[4])))
    if 'astblock' in fm.__dict__.keys():
        disp('Astrocyte gradients blocked between the t={0:.2f} and t={1:.2f} ...'.format(fm.astblock[0],fm.astblock[1]))

    if 'block' in fm.__dict__.keys():
        for keys in fm.block:
            disp('Channel/transporter {0} blocked from t={1:.2f} to t={2:.2f} ...'.format(keys,fm.block[keys][0],fm.block[keys][1]))

    if fm.nogates:
        disp('HH gates set to steady state...')

    if fm.nosynapse:
        disp('Only somatic gradients evaluated! ...')
