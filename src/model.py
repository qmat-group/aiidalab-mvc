import traitlets as tl
from aiida import orm, engine
import time
import threading

class Model(tl.HasTraits):
    """
    Model class: Manages data and business logic.
    """
    # Input parameters
    input_a = tl.Float(default_value=0.0)
    input_b = tl.Float(default_value=0.0)
    
    # Calculation settings
    code_label = tl.Unicode('your_code@computer')
    tot_num_mpiprocs = tl.Int(1)
    
    # Results and Status
    result = tl.Float(allow_none=True, default_value=None)
    calculation_status = tl.Unicode("Ready")
    calculation_node = tl.Any(allow_none=True, default_value=None)
    result_data = tl.Dict(allow_none=True, default_value=None)

    def __init__(self):
        super().__init__()
        # Load code if needed, or do it lazily in calculate
        # try:
        #     self.code = orm.load_code(self.code_label)
        # except:
        #     self.calculation_status = f"Error: Code '{self.code_label}' not found."
        pass

    def calculate(self, input_a, input_b):
        """
        Submit the calculation.
        """
        try:
            self.calculation_status = "Preparing..."
            
            # 1. Create Builder
            # code = orm.load_code(self.code_label)
            # builder = code.get_builder()
            
            # 2. Set Inputs
            # builder.a = orm.Float(self.input_a)
            # builder.b = orm.Float(self.input_b)
            
            # 3. Set Metadata
            # builder.metadata.options.resources = {
            #     'tot_num_mpiprocs': self.tot_num_mpiprocs,
            # }
            
            # 4. Submit
            self.calculation_status = "Submitting..."
            # self.calculation_node = engine.submit(builder)
            
            # SIMULATION FOR TEMPLATE
            time.sleep(1)
            self.calculation_status = f"Running (Simulated PK: 12345)"
            
            # 5. Start Monitoring Thread
            monitor_thread = threading.Thread(target=self._monitor_calculation)
            monitor_thread.daemon = True
            monitor_thread.start()
            
        except Exception as e:
            self.calculation_status = f"Error: {str(e)}"
            self.result = None

    def _monitor_calculation(self):
        """
        Monitor the calculation status in a background thread.
        """
        # In a real app, you would loop until the node is finished
        # while True:
        #     if self.calculation_node.is_finished:
        #         break
        #     time.sleep(5)
        
        # SIMULATION
        for i in range(5):
            time.sleep(1)
            # Update status if needed
        
        self.calculation_status = "Completed successfully"
        self._process_results()

    def _process_results(self):
        """
        Process results after calculation finishes.
        """
        try:
            # Real logic:
            # outputs = self.calculation_node.outputs
            # self.result = outputs.result_x.value
            
            # SIMULATION
            self.result = self.input_a + self.input_b
            self.result_data = {'sum': self.result}
            
        except Exception as e:
            self.calculation_status = f"Result processing error: {str(e)}"

    def reset(self):
        """
        Reset model state.
        """
        self.input_a = 0.0
        self.input_b = 0.0
        self.result = None
        self.calculation_status = "Ready"
        self.calculation_node = None
        self.result_data = None
