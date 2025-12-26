import traitlets as tl
from aiida import orm, engine
from aiida import load_profile
load_profile()

class Model(tl.HasTraits):
    a = tl.Float()
    b = tl.Float()
    c = tl.Float()
    x1 = tl.Float(allow_none= True)
    x2 = tl.Float(allow_none= True)
    
    def __init__(self):
        # Cấu hình thông tin builder
        code = orm.load_code('quad_demo@pias_demo')
        self.builder = code.get_builder()
        metadata = {
            'options':{
                'resources':{
                    'tot_num_mpiprocs':1,
                    'parallel_env':'smp',
                },
                'withmpi':True,
            },
            'label':'quad_demo',
            'description': 'quad demo for IMMAD course',
        }
        self.builder.metadata = metadata
        
    def calculate(self, a, b, c):
        self.builder.a = orm.Float(a)
        self.builder.b = orm.Float(b)
        self.builder.c = orm.Float(c)
        result = engine.submit(self.builder, wait=True, wait_interval=15)
        text = result.outputs.quad.get_content()
        if text.strip() == 'Error' or text.strip() == 'None':
            self.x1 = None
            self.x2 = None
        else:
            splitted_text = text.split(',')
            self.x1 = float(splitted_text[0])
            self.x2 = float(splitted_text[1])

    def update(self): 
        pass
    def reset(self): 
        pass
