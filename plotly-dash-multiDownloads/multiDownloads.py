#%% see requirements.txt for library versions
import base64
import io
import os
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=False,
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)
server = app.server


def parseContents(contents, filename):
    _, content_string = contents.split(",")  # content_type

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return "There was an error processing this file."

    return df


#%% main app layout
app.layout = html.Div(
    [
        html.H3(
            children="Mutliple Download Example",
            style={
                "text-align": "center",
                "font-family": "Arial Black",
                "color": "#ee283c",
            },
        ),
        html.Hr(),
        # upload
        html.Div(
            className="row",
            children=[
                dcc.Upload(
                    id="upload-techSheets",
                    className="three columns",
                    children=html.Div(
                        [
                            "Upload ",
                            html.B(
                                "Multiple TechSheet",
                                style={
                                    "text-align": "center",
                                    "font-size": 14,
                                    "font-family": "Arial Black",
                                    "color": "#ee283c",
                                },
                            ),
                            " Data",
                        ],
                        style={
                            "text-transform": "uppercase",
                            "font-size": 14,
                        },
                    ),
                    style={
                        "width": "300px",
                        "height": "38px",
                        "lineHeight": "38px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                        "display": "inline-block",
                        "verticalAlign": "center",
                    },
                    multiple=True,
                ),
                html.Button(
                    id="confirm-download",
                    children="download all",
                    style={
                        "margin": "10px",
                        "width": "300px",
                        "text-align": "center",
                        "font-size": 14,
                        "font-family": "Arial Black",
                    },
                ),
            ],
        ),
        Download(id="download-df"),
        dcc.Interval(
            id="interval-component",
            interval=1 * 1000,  # in milliseconds
            n_intervals=0,
            max_intervals=0,
            disabled=False,
        ),
    ],
    style={"display": "inline-block"},
)


@app.callback(
    [
        Output("interval-component", "max_intervals"),
        Output("download-df", "data"),
    ],
    [
        Input("confirm-download", "n_clicks"),
        Input("interval-component", "n_intervals"),
        Input("upload-techSheets", "filename"),
        Input("upload-techSheets", "contents"),
    ],
)
def update_uploads(
    n_clicks,
    n_intervals,
    techSheetFilename,
    techSheetContents,
):
    if n_clicks is not None:
        if techSheetFilename is not None and n_intervals < len(techSheetFilename):

            df = [
                parseContents(c, n)
                for c, n in zip(techSheetContents, techSheetFilename)
            ]
            df = df[n_intervals]
            df_name = techSheetFilename[n_intervals]

            """
            Do something cool with df
            """

            print(n_intervals, df_name)

            return [
                len(techSheetFilename),
                send_data_frame(
                    df.to_csv,
                    filename=df_name,
                ),
            ]
        else:
            return [0, None]
    else:
        return [0, None]


if __name__ == "__main__":
    app.run_server()
