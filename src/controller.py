import traitlets as tl
import ipywidgets as ipw

class Controller:
    """
    Controller class: Links Model and View.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self._bind_model_to_view()
        self._bind_view_events()

    def _bind_model_to_view(self):
        """
        Link Model traits to View widgets.
        """
        # Check if view is YAMLView-like (has widgets_dict)
        if hasattr(self.view, 'widgets_dict'):
            for key, widget in self.view.widgets_dict.items():
                if hasattr(self.model, key):
                    # Determine trait type to decide binding logic if needed
                    # For now, assume 'value' property for widgets
                    if hasattr(widget, 'value'):
                        tl.link((self.model, key), (widget, 'value'))
        else:
            # Fallback to hardcoded binding for legacy View
            # Two-way binding for inputs
            tl.link((self.model, 'input_a'), (self.view.input_a_widget, 'value'))
            tl.link((self.model, 'input_b'), (self.view.input_b_widget, 'value'))
            
            # Observe model changes to update view
            self.model.observe(self._on_status_change, names='calculation_status')
            self.model.observe(self._on_result_change, names='result')

    def _bind_view_events(self):
        """
        Bind View events to Controller actions.
        """
        if hasattr(self.view, 'events_dict'):
            for key, event_name in self.view.events_dict.items():
                widget = self.view.widgets_dict.get(key)
                if widget:
                    # Look for handler method in controller
                    handler_name = f"_on_{event_name}"
                    if hasattr(self, handler_name):
                        handler = getattr(self, handler_name)
                        # Bind based on widget type (Button click vs others)
                        if isinstance(widget, ipw.Button):
                            widget.on_click(handler)
                        # Add other event types here if needed
        else:
            # Legacy binding
            self.view.calculate_button.on_click(self._on_calculate_clicked)
            self.view.reset_button.on_click(self._on_reset_clicked)

    def _on_calculate_clicked(self, _):
        """
        Handle calculate button click.
        """
        # Disable button to prevent double click
        self.view.calculate_button.disabled = True
        input_a = self.model.input_a
        input_b = self.model.input_b
        self.model.calculate(input_a, input_b)

    def _on_reset_clicked(self, _):
        """
        Handle reset button click.
        """
        self.model.reset()

    def _on_status_change(self, change):
        """
        Update status display when model status changes.
        """
        new_status = change['new']
        self.view.status_output.value = f"<b>Status:</b> {new_status}"
        
        # Update UI state based on status
        if "Running" in new_status or "Submitting" in new_status:
            self.view.progress_bar.bar_style = 'info'
            self.view.progress_bar.value = 50 # Indeterminate or partial
            self.view.calculate_button.disabled = True
        elif "Completed" in new_status:
            self.view.progress_bar.bar_style = 'success'
            self.view.progress_bar.value = 100
            self.view.calculate_button.disabled = False
        elif "Error" in new_status:
            self.view.progress_bar.bar_style = 'danger'
            self.view.calculate_button.disabled = False
        elif "Ready" in new_status:
            self.view.progress_bar.bar_style = 'info'
            self.view.progress_bar.value = 0
            self.view.calculate_button.disabled = False

    def _on_result_change(self, change):
        """
        Update result display when model result changes.
        """
        new_result = change['new']
        if new_result is not None:
            self.view.result_output.value = f"<b>Result:</b> {new_result}"
        else:
            self.view.result_output.value = "<b>Result:</b> No calculation performed yet"
