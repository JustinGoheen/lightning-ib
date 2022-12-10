import dash
import dash_bootstrap_components as dbc
import lightning as L
from dash import html
from dash.dependencies import Input, Output

from lightning_ib.components.ui import Body, NavBar


class DashAgent(L.LightningWork):
    def run(self):
        """runs a Plotly Dash UI"""
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.layout = html.Div(
            [
                NavBar,
                html.Br(),
                Body,
            ]
        )

        @app.callback(
            [Output("preds-fig", "figure")],
            [Input("dropdown", "value")],
        )
        def update_figure(label_value):
            ...

        app.run_server(host=self.host, port=self.port)
