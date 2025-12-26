import traitlets as tl

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self._bind_model_to_view()
        self._bind_view_events()
        
    def _on_calculate(self, _):
        # Get values from model traits which are bound to view
        a = self.model.a
        b = self.model.b
        c = self.model.c
        self.model.calculate(a, b, c)
        
    def _on_reset(self, _):
        self.model.reset()
        
    def _on_status_change(self, change):
        new_status = change['new']
        # Update status widget if it exists in view
        if hasattr(self.view, 'widgets_dict') and 'status_output' in self.view.widgets_dict:
            self.view.widgets_dict['status_output'].value = f"<b>Status:</b> {new_status}"
            
    def _on_result_change(self, change):
        # We can observe x1 or x2, or just update when status changes to Completed
        # But let's override the base method to handle specific logic
        pass

    def _bind_model_to_view(self):
        """
        Link Model traits to View widgets.
        """
        # Check if view is YAMLView-like (has widgets_dict)
        if hasattr(self.view, 'widgets_dict'):
            for key, widget in self.view.widgets_dict.items():
                if hasattr(self.model, key):
                    if hasattr(widget, 'value'):
                        tl.link((self.model, key), (widget, 'value'))
        else:
            tl.link((self.model, 'input_a'), (self.view.input_a_widget, 'value'))
            tl.link((self.model, 'input_b'), (self.view.input_b_widget, 'value'))
            
            self.model.observe(self._on_status_change, names='calculation_status')
            self.model.observe(self._on_result_change, names='result')

        self.model.observe(self._update_result_display, names=['x1', 'x2'])

    def _bind_view_events(self):
        """
        Bind button click events from View to Controller methods.
        """
        if hasattr(self.view, 'widgets_dict') and hasattr(self.view, 'events_dict'):
            for key, event_name in self.view.events_dict.items():
                widget = self.view.widgets_dict.get(key)
                if widget and hasattr(widget, 'on_click'):
                    if event_name == 'calculate':
                        widget.on_click(self._on_calculate)
                    elif event_name == 'reset':
                        widget.on_click(self._on_reset)

    def _update_result_display(self, change):
        if hasattr(self.view, 'widgets_dict') and 'result_output' in self.view.widgets_dict:
            if self.model.x1 is not None and self.model.x2 is not None:
                self.view.widgets_dict['result_output'].value = f"<b>Result:</b> x1 = {self.model.x1:.4f}, x2 = {self.model.x2:.4f}"
            else:
                self.view.widgets_dict['result_output'].value = "<b>Result:</b> No valid solution"
