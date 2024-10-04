import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout with graphs and a table for statistics
app.layout = html.Div([
    html.H1("Accelerometer Data Dashboard"),
    
    # Graphs for X, Y, and Z data
    dcc.Graph(id='live-graph-x'),
    dcc.Graph(id='live-graph-y'),
    dcc.Graph(id='live-graph-z'),
    
    # Interval for auto-update every second
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
    
    # Div to display statistics in a table format
    html.Div(id='statistics-summary', style={'padding': '20px', 'fontSize': 20}),
    
    # Div to show debug output for CSV reading
    html.Div(id='debug-output', style={'padding': '10px', 'fontSize': 15, 'color': 'red'})
])

# Function to create a pretty HTML table
def generate_statistics_table(x_mean, x_std, x_min, x_max, y_mean, y_std, y_min, y_max, z_mean, z_std, z_min, z_max):
    return html.Table([
        html.Thead(
            html.Tr([html.Th("Axis"), html.Th("Mean"), html.Th("Std Dev"), html.Th("Min"), html.Th("Max")])
        ),
        html.Tbody([
            html.Tr([html.Td("X-axis"), html.Td(f"{x_mean:.2f}"), html.Td(f"{x_std:.2f}"), html.Td(f"{x_min:.2f}"), html.Td(f"{x_max:.2f}")]),
            html.Tr([html.Td("Y-axis"), html.Td(f"{y_mean:.2f}"), html.Td(f"{y_std:.2f}"), html.Td(f"{y_min:.2f}"), html.Td(f"{y_max:.2f}")]),
            html.Tr([html.Td("Z-axis"), html.Td(f"{z_mean:.2f}"), html.Td(f"{z_std:.2f}"), html.Td(f"{z_min:.2f}"), html.Td(f"{z_max:.2f}")])
        ])
    ], style={'border': '1px solid black', 'width': '50%', 'margin': 'auto', 'textAlign': 'center'})

# Update the graphs dynamically whenever the interval component triggers
@app.callback([
    dash.Output('live-graph-x', 'figure'),
    dash.Output('live-graph-y', 'figure'),
    dash.Output('live-graph-z', 'figure'),
    dash.Output('statistics-summary', 'children'),  # Output for the statistics table
    dash.Output('debug-output', 'children')  # Debug output for checking CSV data
], 
[dash.Input('interval-component', 'n_intervals')])  # Trigger callback every interval
def update_graph(n_intervals):
    try:
        df = pd.read_csv("accelerometer_data.csv")
        if df.empty:
            return [
                {'data': [], 'layout': go.Layout(title='X-axis Data')},
                {'data': [], 'layout': go.Layout(title='Y-axis Data')},
                {'data': [], 'layout': go.Layout(title='Z-axis Data')},
                None,
                "CSV file is empty. No data to display."
            ]
        
        # Plot X, Y, Z graphs
        trace_x = go.Scatter(y=df['x'], mode='lines', name='X-axis')
        trace_y = go.Scatter(y=df['y'], mode='lines', name='Y-axis')
        trace_z = go.Scatter(y=df['z'], mode='lines', name='Z-axis')
        
        # Calculate statistics for X, Y, Z
        x_mean, x_std, x_min, x_max = df['x'].mean(), df['x'].std(), df['x'].min(), df['x'].max()
        y_mean, y_std, y_min, y_max = df['y'].mean(), df['y'].std(), df['y'].min(), df['y'].max()
        z_mean, z_std, z_min, z_max = df['z'].mean(), df['z'].std(), df['z'].min(), df['z'].max()

        # Create the statistics table
        stats_table = generate_statistics_table(x_mean, x_std, x_min, x_max, y_mean, y_std, y_min, y_max, z_mean, z_std, z_min, z_max)

        return [
            {'data': [trace_x], 'layout': go.Layout(title='X-axis Data')},
            {'data': [trace_y], 'layout': go.Layout(title='Y-axis Data')},
            {'data': [trace_z], 'layout': go.Layout(title='Z-axis Data')},
            stats_table,
            "Data loaded successfully."
        ]
    
    except FileNotFoundError:
        return [
            {'data': [], 'layout': go.Layout(title='X-axis Data')},
            {'data': [], 'layout': go.Layout(title='Y-axis Data')},
            {'data': [], 'layout': go.Layout(title='Z-axis Data')},
            None,
            "CSV file not found."
        ]
    except pd.errors.EmptyDataError:
        return [
            {'data': [], 'layout': go.Layout(title='X-axis Data')},
            {'data': [], 'layout': go.Layout(title='Y-axis Data')},
            {'data': [], 'layout': go.Layout(title='Z-axis Data')},
            None,
            "CSV file contains no data."
        ]
    except Exception as e:
        return [
            {'data': [], 'layout': go.Layout(title='X-axis Data')},
            {'data': [], 'layout': go.Layout(title='Y-axis Data')},
            {'data': [], 'layout': go.Layout(title='Z-axis Data')},
            None,
            f"An error occurred: {str(e)}"
        ]

if __name__ == '__main__':
    app.run_server(debug=True)
