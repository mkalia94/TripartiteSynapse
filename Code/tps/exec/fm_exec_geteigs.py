from tps import *
from scipy.linalg import eigvals
def exec_geteigs(fm,y):
    if fm.geteigs:
        def temp_model(y):
            return fm.num_model(y,fm.perc)   
        jac = jacobian(temp_model)
        eigs = linalg.eigvals(jac(y))
        disp('Eigenvalues for Pmin={0:.2f}: {1}'.format(fm.perc,eigs))
