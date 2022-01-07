import dash
import numpy as np
import plotly.graph_objects as go

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from storage import get_storage


def draw_plot():
    if 2 in get_storage():
        patient_data = get_storage()[2]
        timestamps = np.array(patient_data["timestamps"])
        values = np.array(patient_data["values"])
    else:
        timestamps = np.array([0])
        values = np.array([[0, 0, 0, 0, 0, 0]])
    fig = go.Figure([
        go.Scatter(x=timestamps, y=values[:, 0], line=dict(color='firebrick', width=4), name='L0'),
        go.Scatter(x=timestamps, y=values[:, 1], line=dict(color='blue', width=4), name='L1'),
        go.Scatter(x=timestamps, y=values[:, 2], line=dict(color='green', width=4), name='L2'),
        go.Scatter(x=timestamps, y=values[:, 3], line=dict(color='violet', width=4), name='R0'),
        go.Scatter(x=timestamps, y=values[:, 4], line=dict(color='black', width=4), name='R1'),
        go.Scatter(x=timestamps, y=values[:, 5], line=dict(color='pink', width=4), name='R2'),
    ])
    return fig


app = dash.Dash()


def create_layout():
    app.layout = html.Div(id='parent', children=[
        html.H1(id='H1', children='Title',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        dcc.Graph(id='the_plot', figure=draw_plot()),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])


@app.callback(Output(component_id='the_plot', component_property='figure'),
              [Input(component_id='interval', component_property='n_intervals')])
def graph_update(n_intervals):
    return draw_plot()
