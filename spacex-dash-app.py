# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Dropdown for selecting launch site
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    dcc.Graph(id='success-pie-chart')
])

# Callback to update pie chart based on selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            title='Total Successful Launches by Site',
            values='class'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Launch Outcomes for site {selected_site}'
        )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)