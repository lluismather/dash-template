from dash import html
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
