import ipywidgets as ipw
import traitlets as tl
import yaml
import os

class View(ipw.VBox):
    """
    View class: Handles UI layout and user interaction.
    """
    def __init__(self, **kwargs):
        # 1. Input Widgets
        self.input_a_widget = ipw.FloatText(
            value=0.0,
            description="Input A:",
            style={'description_width': 'initial'}
        )
        self.input_b_widget = ipw.FloatText(
            value=0.0,
            description="Input B:",
            style={'description_width': 'initial'}
        )
        
        # 2. Control Widgets
        self.calculate_button = ipw.Button(
            description="Run Calculation",
            button_style="primary", # 'success', 'info', 'warning', 'danger' or ''
            icon="play"
        )
        
        self.reset_button = ipw.Button(
            description="Reset",
            button_style="warning",
            icon="refresh"
        )
        
        self.progress_bar = ipw.IntProgress(
            value=0,
            min=0,
            max=100,
            description='Progress:',
            bar_style='info', # 'success', 'info', 'warning', 'danger'
            orientation='horizontal'
        )

        # 3. Output Widgets
        self.status_output = ipw.HTML(value="<b>Status:</b> Ready")
        self.result_output = ipw.HTML(value="<b>Result:</b> No calculation performed yet")

        # 4. Layout
        input_box = ipw.VBox([
            ipw.HTML("<h3>Parameters</h3>"),
            self.input_a_widget, 
            self.input_b_widget
        ])
        
        control_box = ipw.VBox([
            ipw.HTML("<h3>Controls</h3>"),
            ipw.HBox([self.calculate_button, self.reset_button]),
            self.progress_bar
        ])
        
        result_box = ipw.VBox([
            ipw.HTML("<h3>Results</h3>"),
            self.status_output,
            self.result_output
        ])
        
        # Combine all boxes
        main_layout = ipw.HBox([
            ipw.VBox([input_box, control_box]),
            result_box
        ])
        
        super().__init__(children=[
            ipw.HTML("<h2>My AiiDA App</h2>"),
            main_layout
        ], **kwargs)


class YAMLView(ipw.VBox):
    """
    YAMLView class: Handles UI layout from YAML file.
    """
    def __init__(self, yaml_file, **kwargs):
        self.widgets_dict = {} # Key -> Widget
        self.events_dict = {}  # Key -> Event Name
        
        if not os.path.exists(yaml_file):
            raise FileNotFoundError(f"YAML file not found: {yaml_file}")
            
        with open(yaml_file, 'r') as f:
            self.layout_def = yaml.safe_load(f)
            
        children = self._build_widgets(self.layout_def.get('children', []))
        
        super().__init__(children=children, **kwargs)

    def _build_widgets(self, widget_defs):
        widgets = []
        for w_def in widget_defs:
            w_type = w_def.get('type')
            w_key = w_def.get('key')
            w_event = w_def.get('event')
            w_children = w_def.get('children', [])
            
            # Extract kwargs for widget initialization
            kwargs = {k: v for k, v in w_def.items() if k not in ['type', 'key', 'event', 'children']}
            
            # Create widget instance
            if hasattr(ipw, w_type):
                widget_cls = getattr(ipw, w_type)
                
                # Recursively build children if container
                if w_children:
                    kwargs['children'] = self._build_widgets(w_children)
                    
                widget = widget_cls(**kwargs)
                
                # Register widget if key is provided
                if w_key:
                    self.widgets_dict[w_key] = widget
                    
                # Register event if provided
                if w_event:
                    self.events_dict[w_key] = w_event
                
                widgets.append(widget)
            else:
                print(f"Warning: Widget type '{w_type}' not found in ipywidgets.")
                
        return widgets
