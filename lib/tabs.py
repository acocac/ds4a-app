# import dash related libraries
import dash_core_components as dcc

# import local libraries
from lib import content


def build_tabs():
    return dcc.Tabs(id='tabs-header', value='tab-1', parent_className='custom-tabs', className='custom-tabs-container',
                    children=[
                        dcc.Tab(value='tab-1', label='Characterization', className='custom-tab',
                                selected_className='custom-tab--selected', children=content.build_characterization()
                                ),
                        dcc.Tab(value='tab-2', label='Crime Network', className='custom-tab',
                                selected_className='custom-tab--selected', children=content.build_network()
                                ),
                        dcc.Tab(value='tab-3', label='Prediction', className='custom-tab',
                                selected_className='custom-tab--selected', children=content.build_prediction()
                                )
                    ])