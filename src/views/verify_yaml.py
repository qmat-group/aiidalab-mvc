import sys
import os
import unittest.mock as mock

# Mock ipywidgets, traitlets, and aiida since they might not be installed in the agent environment
sys.modules['ipywidgets'] = mock.MagicMock()
sys.modules['traitlets'] = mock.MagicMock()
sys.modules['aiida'] = mock.MagicMock()
import ipywidgets as ipw
import traitlets as tl

# Define mock classes that are used in the view
class MockWidget:
    def __init__(self, **kwargs):
        self.value = kwargs.get('value')
        self.description = kwargs.get('description')
        self.children = kwargs.get('children', [])
        self.on_click_handler = None
        
    def on_click(self, handler):
        self.on_click_handler = handler

ipw.VBox = MockWidget
ipw.HBox = MockWidget
ipw.FloatText = MockWidget
ipw.Button = MockWidget
ipw.HTML = MockWidget
ipw.IntProgress = MockWidget

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from view import YAMLView

def test_yaml_loading():
    print("Testing YAML loading...")
    try:
        view = YAMLView('yaml_elements/view.yaml')
        print("YAML loaded successfully.")
        
        # Verify widgets exist
        expected_keys = ['a', 'b', 'c', 'calculate_btn', 'reset_btn', 'status_output', 'result_output']
        for key in expected_keys:
            if key in view.widgets_dict:
                print(f"Widget '{key}' found.")
            else:
                print(f"ERROR: Widget '{key}' not found!")
                return False
                
        # Verify events exist
        expected_events = {'calculate_btn': 'calculate', 'reset_btn': 'reset'}
        for key, event in expected_events.items():
            if view.events_dict.get(key) == event:
                print(f"Event for '{key}' matches: {event}")
            else:
                print(f"ERROR: Event for '{key}' mismatch!")
                return False
                
        print("Verification PASSED!")
        return True
    except Exception as e:
        print(f"Verification FAILED with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_yaml_loading():
        sys.exit(0)
    else:
        sys.exit(1)
