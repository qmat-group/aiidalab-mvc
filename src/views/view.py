import ipywidgets as ipw
import traitlets as tl
import yaml
import os

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
