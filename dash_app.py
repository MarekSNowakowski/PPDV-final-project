import dash
import numpy as np
import plotly.graph_objects as go

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from storage import get_storage

global patient_id


def draw_plot():
    if 2 in get_storage():
        patient_data = get_storage()[patient_id]
        timestamps = np.array(patient_data["timestamps"])
        values = np.array(patient_data["values"])
        anomalies = np.array(patient_data["anomalies"])
    else:
        timestamps = np.array([0])
        values = np.array([[0, 0, 0, 0, 0, 0]])
        anomalies = np.array([False, False, False, False, False, False])
    fig = go.Figure([
        go.Scatter(x=timestamps, y=values[:, 0], line=dict(color='darkblue', width=3), name='L0'),
        go.Scatter(x=timestamps, y=values[:, 1], line=dict(color='blue', width=3), name='L1'),
        go.Scatter(x=timestamps, y=values[:, 2], line=dict(color='lightblue', width=3), name='L2'),
        go.Scatter(x=timestamps, y=values[:, 3], line=dict(color='darkgreen', width=3), name='R0'),
        go.Scatter(x=timestamps, y=values[:, 4], line=dict(color='green', width=3), name='R1'),
        go.Scatter(x=timestamps, y=values[:, 5], line=dict(color='lime', width=3), name='R2'),
    ])
    return fig


app = dash.Dash()

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    html.H1(id='H1', children=f'Python programming and data visualisation final project - Marek Nowakowski',
            style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),

    html.Div(id='content', children=[
        html.Div(id='main-graph', children=[])
    ])
])


def create_layout(_patient_id):
    global patient_id
    patient_id = _patient_id
    return html.Div(id='main-graph', children=[
        dcc.Dropdown(
            id='patient-dropdown',
            options=[
                {'label': 'Patient 1', 'value': 1},
                {'label': 'Patient 2', 'value': 2},
                {'label': 'Patient 3', 'value': 3},
                {'label': 'Patient 4', 'value': 4},
                {'label': 'Patient 5', 'value': 5}
            ],
            value=patient_id
        ),
        dcc.Graph(id='the_plot', figure=draw_plot()),
        dcc.Interval(id='interval', interval=1000, n_intervals=0)
    ])


@app.callback(Output('content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if len(pathname) == 10 and pathname[0:9] == '/patient/' and int(pathname[9]) in range(1, 6):
        return create_layout(int(pathname[9]))
    else:
        return create_layout(1)


@app.callback(Output(component_id='the_plot', component_property='figure'),
              [Input(component_id='interval', component_property='n_intervals')])
def graph_update(n_intervals):
    return draw_plot()


@app.callback(Output(component_id='url', component_property='pathname'),
              [Input(component_id='patient-dropdown', component_property='value')])
def dropdown_update(value):
    return f'/patient/{value}'
