#%% see requirements.txt for library versions
import base64
import io
import os
import re
from datetime import datetime
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
            df = pd.read_excel(io.BytesIO(decoded), engine="openpyxl")
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
                    n_clicks=None,
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
        # upload and download up to 5 files, you may set the upper limit to any number
        # you want, ideally more than what you need. It should not affect the performance
        # significantly
        html.Div([Download(id=f"download-df-{i}") for i in range(5)]),
    ],
    style={"display": "inline-block"},
)


@app.callback(
    [Output(f"download-df-{i}", "data") for i in range(5)],
    Input("confirm-download", "n_clicks"),
    [
        State("upload-techSheets", "filename"),
        State("upload-techSheets", "contents"),
    ],
)
def update_uploads(
    n_clicks,
    techSheetFilename,
    techSheetContents,
):
    if n_clicks is not None:
        if techSheetFilename is not None:

            list_of_df = [
                parseContents(c, n)
                for c, n in zip(techSheetContents, techSheetFilename)
            ]

            """
            Do something cool with df
            """

            outputDF = [
                send_data_frame(
                    df.to_csv,
                    filename=df_name,
                )
                for df, df_name in zip(list_of_df, techSheetFilename)
            ] + [None for i in range(5 - len(techSheetFilename))]

            return outputDF
        else:
            return [None for i in range(5)]
    else:
        return [None for i in range(5)]


if __name__ == "__main__":
    app.run_server()
