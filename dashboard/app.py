import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load the CSV data
df = pd.read_csv(r"C:\Users\Asus\Desktop\i\react-crypto-app-master\react-crypto-app-master\spacex-power-prediction-datat-science-\dashboard\web-cleaned-data.csv")

# Determine max and min payload values
max_payload = df["Payloadmass"].max()
min_payload = df["Payloadmass"].min()

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app with enhanced CSS and dark background
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "font-size": "40px", 
                "textAlign": "center", 
                "color": "#FFFFFF",
                "padding": "20px 0"
            },
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCSFS SLC-40", "value": "CCSFS SLC-40"},
                {"label": "VSFB SLC-4E", "value": "VSFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
            ],
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
            style={
                "width": "80%",
                "margin": "auto",
                "padding": "10px",
                "font-size": "20px",
                "text-align-last": "center",
                "color": "#000000"
            },
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (kg):", style={"color": "#FFFFFF", "font-size": "20px", "text-align": "center"}),
        html.Div(
            dcc.RangeSlider(
                id="payload-slider",
                min=0,
                max=18000,
                step=1000,
                value=[min_payload, max_payload],
                marks={i: f'{i} kg' for i in range(0, 18001, 4000)},
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            style={
                "padding": "20px",
                "margin": "auto",
                "width": "80%",
            }
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ],
    style={
        "backgroundColor": "#2c3e50",
        "padding": "20px",
        "font-family": "Arial"
    }
)

# Callback for updating pie chart based on selected launch site
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(launch_site):
    if launch_site == "ALL":
        fig = px.pie(
            df, names="Boosterlanding", title="Landing status for all Launch sites"
        )
    else:
        df_launch_site = df[df["Launchsite"] == launch_site]
        fig = px.pie(
            df_launch_site,
            names="Boosterlanding",
            title=f"Landing status for site {launch_site}",
        )
    fig.update_layout(paper_bgcolor="#2c3e50", font_color="white")
    return fig

# Callback for updating scatter plot based on selected launch site and payload range
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_scatter_chart(launch_site, payload):
    df_payload = df[df["Payloadmass"].between(payload[0], payload[1])]
    if launch_site == "ALL":
        fig = px.scatter(
            df_payload,
            x="Payloadmass",
            y="Boosterlanding",
            color="BoosterVersion",
            title="Landing status count on payload mass for all sites",
        )
    else:
        df_payload_launchsite = df_payload[df_payload["Launchsite"] == launch_site]
        fig = px.scatter(
            df_payload_launchsite,
            x="Payloadmass",
            y="Boosterlanding",
            color="BoosterVersion",
            title=f"Landing status count on payload mass for site {launch_site}",
        )
    fig.update_layout(paper_bgcolor="#2c3e50", font_color="white")
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
