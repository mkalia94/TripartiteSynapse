from tps import *
from gooey import Gooey,GooeyParser 

@Gooey(dump_build_config=True, program_name="Tripartite Synapse v1.0")
def main():
    desc = "Tripartite Synapse: v1.0"
    arg = GooeyParser(description=desc)
    subs = arg.add_subparsers(help='Simulation options', dest='command')
    ed = subs.add_parser('EnergyDeprivation',help='Energy deprivation')
    
    ed.add_argument('--ECS',default=0.2,type=float,help="Initial extracellular volume fraction")
    ed.add_argument('--tfinal',default=100,type=float,help="Simulation duration (in min.)")
    ed.add_argument('--tstart',default=20,type=float,help="Onset of energy deprivation (in min.)")
    ed.add_argument('--tend',default=30,type=float,help="Offset of energy deprivation (in min.)")
    ed.add_argument('--EnergyAvailable',default=0.5,type=float,help="Minimum available energy during ED (fraction)")
    ed.add_argument('--solve', action='store_true')
    ed.add_argument('--nogates', action='store_true',help="Set gates to steady state?")
    ed.add_argument('--savenumpy', action='store_true',help="Save data?")
    #arg.add_argument('--savematlab', action='store_true')
    ed.add_argument('--Plot', action='store_true',help="Plot?")

    ex = subs.add_parser('Excitation',help='Excitation')
    
    ex.add_argument('--ECS',default=0.2,type=float,help="Initial extracellular volume fraction")
    ex.add_argument('--tfinal',default=100,type=float,help="Simulation duration (in min.)")
    ex.add_argument('--StartExcitation',default=1,type=float,help="Onset of excitation (in min.)")
    ex.add_argument('--EndExcitation',default=15,type=float,help="Offset of excitation (in min.)")
    ex.add_argument('--Current',default=20,type=float,help="Injected current (in pA)")
    ex.add_argument('--Wavelength',default=20,type=float,help="Pulse wavelength(in min.)")
    ex.add_argument('--Duty',default=0.95,type=float,help="Duty of injected pulse (fraction)")
    ex.add_argument('--BlockAstrocyte',default=0.5,action='store_true',help="Block astrocyte gradients too?")
    ex.add_argument('--nogates', action='store_true',help="Set gates to steady state?")
    ex.add_argument('--solve', action='store_true')
    ex.add_argument('--savenumpy', action='store_true',help="Save data?")
    # arg.add_argument('--savematlab', action='store_true')
    ex.add_argument('--Plot', action='store_true',help="Plot?")

    
    # arg.add_argument('--plot', type=json.loads)
    # arg.add_argument('--block', type=json.loads)
    # arg.add_argument('--excite', nargs=5, type=float)
    # arg.add_argument('--astblock', nargs=2, type=float)
    # arg.add_argument('--nogates', action='store_true')
    # arg.add_argument('--nochargecons', action='store_true')
    # arg.add_argument('--saveloc', type=str)
    # arg.add_argument('--readdata', type=str)
    # arg.add_argument('--case1', type=json.loads)
    # arg.add_argument('--case2', type=json.loads)
    # arg.add_argument('--casename',type=str)
    # arg.add_argument('--geteigs',action='store_true')
    # arg.add_argument('--savematlabpar',action='store_true')

    args = arg.parse_args()

    if 'EnergyAvailable' in args.__dict__.keys():
        args.perc = args.EnergyAvailable

    args.alphae0 = args.ECS
    args.plotall = args.Plot
    

    args.__dict__['savematlab'] = False
    if 'StartExcitation' in args.__dict__.keys():
        args.__dict__['excite'] = [args.__dict__['StartExcitation'],args.__dict__['EndExcitation'],args.__dict__['Current'],args.__dict__['Wavelength'],args.__dict__['Duty']]
        if args.BlockAstrocyte:
            args.__dict__['astblock'] = [args.__dict__['StartExcitation'],args.__dict__['EndExcitation']]
            
    args.__dict__['nochargecons'] = False
    args.__dict__['geteigs'] = False
    args.__dict__['savematlabpar'] = False
    args.__dict__['nosynapse'] = False	
    
    for key in args.__dict__:
        if args.__dict__[key] is not None:
            paramdict[key] = args.__dict__[key]

    if 'saveloc' in paramdict.keys():
        disp('------{a}------'.format(a=paramdict['saveloc']))
    else:
        disp('------Test------')

    fm = fmclass(paramdict)
    negcheck_init(fm)
    exec_cases(fm,fmclass)
    t,y = exec_solve(fm)

main()
