import traitlets as tl
from aiida import orm, engine
from aiida import load_profile
load_profile()

class Model(tl.HasTraits):
    a = tl.Float()
    b = tl.Float()
    c = tl.Float()
    x1 = tl.Float(allow_none=True)
    x2 = tl.Float(allow_none=True)
    
    def __init__(self):
        # Cấu hình thông tin builder
        code = orm.load_code('quad-1.0@pias')
        self.builder = code.get_builder()
        metadata = {
            'options':{
                'resources':{
                    'tot_num_mpiprocs':1,
                    'parallel_env':'smp',
                },
                'withmpi':False,
            },
            'label':'quad_demo',
            'description': 'quad demo',
        }
        self.builder.metadata = metadata
        
    def calculate(self, a, b, c):
        self.builder.a = orm.Float(a)
        self.builder.b = orm.Float(b)
        self.builder.c = orm.Float(c)
        result = engine.submit(self.builder, wait=True, wait_interval=15)
        self.x1 = self.x2 = None 
        if 'x1' in result.outputs:
            self.x1 = result.outputs.x1.value
        if 'x2' in result.outputs:
            self.x2 = result.outputs.x2.value

    def update(self): 
        pass
    def reset(self): 
        pass
