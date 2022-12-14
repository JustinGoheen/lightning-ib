# Copyright Justin R. Goheen.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import torch
from dash import dash_table, dcc, html
from pytorch_lightning.utilities.model_summary import ModelSummary

from lightning_ib.core.module import LitModel

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


def metrics_collection(y_true, y_predict):
    pass


def create_figure(image, title_text):
    fig = px.imshow(image.view(28, 28))
    fig.update_layout(
        title=dict(
            text=title_text,
            font_family="Ucityweb, sans-serif",
            font=dict(size=24),
            y=0.05,
            yanchor="bottom",
            x=0.5,
        ),
        height=300,
    )
    return fig


def make_model_layer_table(model_summary: list):
    model_layers = model_summary[:-4]
    model_layers = [i for i in model_layers if not all(j == "-" for j in i)]
    model_layers = [i.split("|") for i in model_layers]
    model_layers = [[j.strip() for j in i] for i in model_layers]
    model_layers[0][0] = "Layer"
    header = model_layers[0]
    body = model_layers[1:]
    table = pd.DataFrame(body, columns=header)
    table = dash_table.DataTable(
        data=table.to_dict("records"),
        columns=[{"name": i, "id": i} for i in table.columns],
        style_cell={
            "textAlign": "left",
            "font-family": "FreightSans, Helvetica Neue, Helvetica, Arial, sans-serif",
        },
        style_as_list_view=True,
        style_table={
            "overflow-x": "auto",
        },
        style_header={"border": "0px solid black"},
    )
    return table


def make_model_param_text(model_summary: list):
    model_params = model_summary[-4:]
    model_params = [i.split("  ") for i in model_params]
    model_params = [[i[0]] + [i[-1]] for i in model_params]
    model_params = [[j.strip() for j in i] for i in model_params]
    model_params = [i[::-1] for i in model_params]
    model_params[-1][0] = "Est. params size (MB)"
    model_params = ["".join([i[0], ": ", i[-1]]) for i in model_params]
    return model_params


def make_model_summary(model_summary: ModelSummary):
    model_summary = model_summary.__str__().split("\n")
    model_layers = make_model_layer_table(model_summary)
    model_params = make_model_param_text(model_summary)
    return model_layers, model_params


def find_index(dataset, label=0, label_idx=1):
    for i in range(len(dataset)):
        if dataset[i][label_idx] == label:
            return i


# DATA


# model summary
chkptdir = os.path.join("models", "checkpoints")
available_checkpoints = os.listdir(chkptdir)
available_checkpoints.remove("README.md")
latest_checkpoint = available_checkpoints[0]
chkpt_fname = os.path.join("models", "checkpoints", "model.ckpt")
model = LitModel.load_from_checkpoint(chkpt_fname)
summary = ModelSummary(model)
model_layers, model_params = make_model_summary(summary)

# APP LAYOUT
NavBar = dbc.NavbarSimple(
    brand="Lightning IB",
    color="#792ee5",
    dark=True,
    fluid=True,
    className="app-title",
)

ModelCard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H1("Model Card", id="model_card", className="card-title"),
                html.Br(),
                html.H3("Layers", className="card-title"),
                model_layers,
                html.Br(),
                html.H3("Parameters", className="card-title"),
                html.P(
                    f"{model_params[0]}",
                    id="model_info_1",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[1]}",
                    id="model_info_2",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[2]}",
                    id="model_info_3",
                    className="model-card-text",
                ),
                html.P(
                    f"{model_params[3]}",
                    id="model_info_4",
                    className="model-card-text",
                ),
            ]
        ),
    ],
    className="model-card-container",
)

SideBar = dbc.Col(
    [
        ModelCard,
    ],
    width=3,
)

Predictions = dcc.Graph(
    id="preds-fig",
    figure=create_figure(..., "Decoded"),
    config={
        "responsive": True,
        "displayModeBar": True,
        "displaylogo": False,
    },
)

Metrics = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4("Metric 1", className="card-title"),
                        html.P("0.xx", id="metric_1_text", className="metric-card-text"),
                    ],
                    id="metric_1_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4("Metric 2", className="card-title"),
                        html.P("0.xx", id="metric_2_text", className="metric-card-text"),
                    ],
                    id="metric_2_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4("Metric 3", className="card-title"),
                        html.P("0.xx", id="metric_3_text", className="metric-card-text"),
                    ],
                    id="metric_3_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        html.H4("Metric 4", className="card-title"),
                        html.P("0.xx", id="metric_4_text", className="metric-card-text"),
                    ],
                    id="metric_4_card",
                    className="metric-container",
                )
            ],
            width=3,
        ),
    ],
    id="metrics",
    justify="center",
)

Graphs = dbc.Row(
    Predictions,
    justify="center",
    align="middle",
    className="graph-row",
)

MainArea = dbc.Col([Metrics, html.Br(), Graphs])

Body = dbc.Container([dbc.Row([SideBar, MainArea])], fluid=True)

# PASS LAYOUT TO DASH
app.layout = html.Div(
    [
        NavBar,
        html.Br(),
        Body,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
