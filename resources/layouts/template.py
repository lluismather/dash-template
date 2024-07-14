import dash
from dash import dcc, html
import datetime

footer = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.A(
                            "{} template by Mather Group Limited".format(
                                str(datetime.datetime.now().year)
                            ),
                            href="https://mathergroup.io",
                            target="_blank",
                            className="text-sm text-white",
                        ),
                        html.P(
                            "",
                            className="text-sm text-white",
                        ),
                    ],
                    className="flex flex-col sm:flex-row sm:justify-between sm:items-center",
                ),
            ],
            className="w-full flex flex-col sm:flex-row sm:justify-between sm:items-center",
        ),
    ],
    className="bg-gray-800 p-8 mt-auto",
)


def layout():

    heading = [
        html.Div(
            [
                html.A(
                    [
                        # html.Img(
                        #     src=dash.get_asset_url("dash-white.svg"),
                        #     className="w-full h-auto sm:h-10 sm:w-auto",
                        # ),
                        html.H1(
                            "Dashboard",
                            className="text-2xl font-semibold",
                        ),
                    ],
                    href="/",
                ),
                html.Div(
                    [
                        html.A(
                            "Log out",
                            href="/logout",
                            className="hover-underline mr-4",
                        ),
                    ],
                    style={"float": "right"},
                ),
            ],
            className="w-full flex flex-col sm:flex-row sm:justify-between sm:!items-center py-8 px-4 bg-teal-700 shadow-md border-b border-gray-300 text-white",
        ),
    ]

    return html.Div(
        [
            html.Div(
                [
                    dcc.Location(id="url", refresh=True),
                    html.Div(
                        [
                            html.Div(heading, className=""),
                            html.Div(
                                dash.page_container,
                                className="",
                            ),
                        ],
                        className="w-full flex flex-col",
                    ),
                ], 
                className="min-h-screen bg-gray-100 flex flex-col"
            ),
            footer,
        ],
    )
