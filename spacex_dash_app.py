# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id = 'site-dropdown',
                                            options=[
                                                {'label':'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                            value='ALL',
                                            placeholder='Select a Launch Site',
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0', 100: '100', 1000: '1000', 5000: '5000', 7000: '7000'},
                                    value=[min_payload, max_payload],
                                    tooltip={
                                            "placement": "bottom",
                                            "always_visible": True,
                                            "style": {"color": "LightSteelBlue", "fontSize": "16px"}}
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                dcc.Graph(id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    custom_colors = ['red', 'green']
    # Filter the DataFrame based on the selected site
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(filtered_df, values='class', names='Launch Site',
                     title='Success Pie Chart for All Sites')
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        new_df = filtered_df['class'].value_counts().reset_index()
        new_df.columns = ['Outcome', 'count']
        fig = px.pie(new_df, values='count', names='Outcome',color = "Outcome", color_discrete_sequence=custom_colors,
                     title='Success Failure Pie Chart for Launch Site CCAFS LC-40')
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        new_df = filtered_df['class'].value_counts().reset_index()
        new_df.columns = ['Outcome', 'count']
        fig = px.pie(new_df, values='count', names='Outcome',color = "Outcome", color_discrete_sequence=custom_colors,
                     title='Success Failure Pie Chart for Launch Site CCAFS SLC-40')
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        new_df = filtered_df['class'].value_counts().reset_index()
        new_df.columns = ['Outcome', 'count']
        fig = px.pie(new_df, values='count', names='Outcome',color = "Outcome", color_discrete_sequence=custom_colors,
                     title='Success Failure Pie Chart for Launch Site KSC LC-39A')
    elif entered_site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        new_df = filtered_df['class'].value_counts().reset_index()
        new_df.columns = ['Outcome', 'count']
        fig = px.pie(new_df, values='count', names='Outcome',color = "Outcome", color_discrete_sequence=custom_colors,
                     title='Success Failure Pie Chart for Launch Site VAFB SLC-4E')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_plot(site_selection, payload_range):
    filtered_df = spacex_df
    if site_selection == 'ALL':
       plot = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        # Filter by the selected launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_selection]
        
        # Assuming payload_range is a tuple (min_payload, max_payload) from the slider
        min_payload, max_payload = payload_range
        filtered_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= min_payload) & 
                                (filtered_df["Payload Mass (kg)"] <= max_payload)]
        
        # Create scatter plot for filtered data
        plot = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return plot

# Run the app
if __name__ == '__main__':
    app.run_server()
