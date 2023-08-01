from shiny import App, ui, render, reactive
import asyncio

# import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

import pandas as pd
import numpy as np

n_operators = 13
n_nurses = 9

# app_ui = ui.page_fixed(
#     ui.h2("Ciw Urgent Care Call Centre Model"),
#     ui.markdown("""
#         This app is based on a [ciw example][0] that simulates a simple call centre model.
#         [0]: https://health-data-science-or.github.io/simpy-streamlit-tutorial/content/03_streamlit/13_ciw_backend.html
#     """),
#     ui.layout_sidebar(
#         ui.panel_sidebar(
#             # number of call operators
#             ui.input_slider("n_operators", "Call operators", 1, 40, 13, sep=5),
#             ui.output_text_verbatim("set_n_operators"),

#             # nurses on duty
#             ui.input_slider("n_nurses", "Nurse practitioners", 1, 20, 9),
#             ui.output_text_verbatim("txt"),

#             # chance of nurse call back
#             ui.input_slider("chance_callback", "Probability of nurse callback", 0.0, 1.0, 0.4),
#             ui.output_text_verbatim("txt"),

#             # Number of replications
#             ui.input_numeric("n_reps", "Replications", value=5),
#         ),
#         ui.panel_main(
#             ui.input_action_button("run_sim", "Run Simulation", class_="btn-primary"),
#             ui.output_text_verbatim("result", placeholder=True),
#         )
#     )
# )

app_ui = ui.page_fluid(
    # number of call operators
    ui.input_slider("n_operators", "Call operators", 1, 40, 13, sep=5),
    ui.output_text_verbatim("set_n_operators"),

    # nurses on duty
    ui.input_slider("n_nurses", "Nurse practitioners", 1, 20, 9),
    ui.output_text_verbatim("txt"),

    ui.input_action_button("run_sim", "Run Simulation", class_="btn-primary"),
    ui.output_text_verbatim("result")

)

def server(input, output, session):

    @output
    @render.table
    @reactive.event(input.run_sim)
    async def result():
        #await asyncio.sleep(2)
        with reactive.isolate():
            exp = Experiment()
            results = multiple_replications(exp)
            print(results)
            return results

app = App(app_ui, server)