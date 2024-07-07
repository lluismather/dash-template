import dash
from dash import dcc, html

footer = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Built by the Labour Party",
                            className="text-sm text-white",
                        ),
                        html.P(
                            "Powered by Dash",
                            className="text-sm text-white",
                        ),
                    ],
                    className="flex flex-col sm:flex-row sm:justify-between sm:items-center",
                ),
            ],
            className="w-full flex flex-col sm:flex-row sm:justify-between sm:items-center",
        ),
    ],
    className="bg-black p-4 mt-auto",
)


def layout():

    heading = [
        html.Div(
            [
                html.A(
                    [
                        html.Img(
                            src=dash.get_asset_url("dash-white.svg"),
                            className="w-full h-auto sm:h-10 sm:w-auto",
                        ),
                    ],
                    href="/",
                ),
                html.Div(
                    [
                        html.A(
                            "Log out",
                            href="/logout",
                            className="hover-underline text-white mr-4",
                        ),
                    ],
                    style={"float": "right"},
                ),
            ],
            className="w-full flex flex-col sm:flex-row sm:justify-between sm:!items-center",
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
