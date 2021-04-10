from tps import *
def set_saveloc(fm):
    if 'saveloc' in fm.__dict__.keys():
        directory = 'SimDataImages/{a}'.format(a=fm.saveloc)
        if not os.path.exists(directory):
            os.makedirs(directory)
    elif 'readdata' in fm.__dict__.keys():
        directory = 'SimDataImages/{a}'.format(a=fm.readdata)
    else:
        directory = 'SimDataImages/{a}'.format(a='Test')
        if not os.path.exists(directory):
            os.makedirs(directory)
    fm.directory = directory
