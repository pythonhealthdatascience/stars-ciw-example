# CIW Model Application created with Shiny for Python (Core syntax, not Express)
from shiny import (App, ui, render, reactive, Inputs, Outputs, Session)
from shinywidgets import output_widget, render_widget
import shinyswatch
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from faicons import icon_svg

# Import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

MODELDESCRIPTION = """
This app is based on a 
[ciw example](https://health-data-science-or.github.io/simpy-streamlit-tutorial/content/03_streamlit/13_ciw_backend.html) 
that simulates a simple call centre model.

In this model:

1. Patients ring the urgent care call centre and wait for an operator.
2. A given proportion of patients will then require callback from a nurse.

The simulation allows you to alter the number of call operators and nurses on
duty.

You can then view the subsequent impact on caller wait times and staff
utilisation (i.e. the proportion of time that operators or nurses spent on
call, whilst on duty).
"""

ABOUT = """## About

This work is produced using entirely free and open-source software in python.

> This model is independent research supported by the National Institute for Health Research 
Applied Research Collaboration South West Peninsula. 
The views expressed in this publication are those of the author(s) and not necessarily 
those of the National Institute for Health Research or the Department of Health and Social Care."""


SIMSOFTWARE = """## Modelling and Simulation Software

The model is written in python3 and `ciw`. The simulation libary `ciw` is a network based DES package.

> Detailed documentation for `ciw` and additional models can be found here: https://ciw.readthedocs.io

"""

DOCS_LINK = """## Model Documentation
Live documentation including STRESS-DES reporting for the model and 
is available at: https://pythonhealthdatascience.github.io/stars-ciw-examplar"""

app_ui = ui.page_fluid(

    # Page header
    ui.row(
        # Logo
        ui.column(
            # Column width (required by function but we override with style)
            6,
            # Logo
            ui.tags.div(
                ui.tags.img(
                    src="stars_logo.png", height="100px"),
            ),
            # Ensure that the column always takes up 110px
            style="flex: 0 0 110px; max-width: 110px;",
        ),
        # Heading and introduction
        ui.column(
            # Column width (required by function but we override with style)
            6,
            # Title
            ui.h1(
                "Ciw Urgent Care Call Centre Model", style="margin-top: 10px;"),
            # Introductory paragraph
            ui.markdown(MODELDESCRIPTION),
            # Button to navigate to GitHub code
            ui.input_action_button(
                id="github_btn",
                label="View code on GitHub" ,  
                icon=icon_svg("github")
            ),
            ui.tags.script("""
                document.getElementById('github_btn').onclick = function() {
                    window.open('https://github.com/pythonhealthdatascience/stars-ciw-example/', '_blank');
                };
            """),
            # Button to view model documentation
            ui.input_action_button(
                id="docs_btn",
                label="View model documentation" ,  
                icon=icon_svg("book")
            ),
            ui.tags.script("""
                document.getElementById('docs_btn').onclick = function() {
                    window.open('https://pythonhealthdatascience.github.io/stars-ciw-example/', '_blank');
                };
            """),
            # Resize width to fill space, alongside the fixed logo column
            style="flex: 1; min-width: 0;",
        ),
    ),

    # Blank space
    ui.div().add_style("height:20px;"),

    # Sidebar and main panel
    ui.navset_tab(
        # Panel for the simulation page
        ui.nav_panel("Interactive simulation", 
            ui.layout_sidebar(
                # Sidebar content
                ui.sidebar(
                    
                    # Number of call operators
                    ui.tooltip(
                        ui.input_slider(id="n_operators",
                                        label="Call operators",
                                        min=1,
                                        max=40,
                                        value=13,
                                        ticks=False),
                        "Number of call operators on duty"
                    ),

                    # Number of nurses on duty
                    ui.tooltip(
                        ui.input_slider(id="n_nurses",
                                        label="Nurse practitioners",
                                        min=1,
                                        max=20,
                                        value=9,
                                        ticks=False),
                        "Number of nurses on duty"
                    ),

                    # Chance of nurse callback
                    ui.tooltip(
                        ui.input_slider(id="chance_callback",
                                        label="Probability of nurse callback",
                                        min=0.0,
                                        max=1.0,
                                        value=0.4,
                                        ticks=False),
                        """The probability of nurse callback: 0 means never,
                        0.5 means 50% of the time, and 1 means always"""
                    ),

                    # Number of replications
                    ui.tooltip(
                        # We set a minimum which applies to the arrow clicked,
                        # but user can still override minimum by typing
                        ui.input_numeric(id="n_reps",
                                        label="Replications",
                                        value=5,
                                        min=1),
                        "How many times to run the model (minimum 1)"
                    ),

                    # run simulation model button
                    ui.input_action_button(id="run_sim",
                                           label="Run Simulation",
                                           class_="btn-primary"),
                ),
                # Main panel content
                ui.output_data_frame("result_table"),
                output_widget("histogram"),
            ),
        ),
        # Panel for the about page
        ui.nav_panel("About", 
               ui.markdown(ABOUT),
               ui.markdown(SIMSOFTWARE),
               ui.markdown(DOCS_LINK)),
    ),
    theme = shinyswatch.theme.journal()
)

def server(input: Inputs, output: Outputs, session: Session):

    # reactive value for replication results.
    replication_results = reactive.Value()

    def run_simulation():
        '''
        Run the simulation model

        Returns:
        --------
        pd.DataFrame
            Pandas Dataframe containing replications by performance
            measures
        '''
        # create the experiment
        user_experiment = Experiment(n_operators=input.n_operators(),
                                     n_nurses=input.n_nurses(),
                                     chance_callback=input.chance_callback())
        
        # run multiple replications
        results = multiple_replications(user_experiment, n_reps=input.n_reps())

        return results

    def summary_results(replications):
        '''
        Convert the replication results into a summary table
        
        Returns:
        -------
        pd.DataFrame
        '''
        summary = replications.describe().round(2).T

        # Resetting index because cannot figure out how to show index
        summary = summary.reset_index() 
        summary = summary.rename(columns={'index': 'metric'})

        # Renaming columns
        metrics = {
            '01_mean_waiting_time': 'Time waiting for operator (mins)',
            '02_operator_util': 'Operator utilisation (%)',
            '03_mean_nurse_waiting_time': 'Time waiting for nurse (mins)',
            '04_nurse_util': 'Nurse utilisation (%)'
        }
        summary['metric'] = summary['metric'].map(metrics)

        # Drop count, as that is implicit from chosen number of replications
        summary = summary.drop('count', axis=1)

        return summary
    
    def create_user_filtered_hist(results):
        '''
        Create a plotly histogram that includes a drop down list that allows a user
        to select which KPI is displayed as a histogram
        
        Params:
        -------
        results: pd.Dataframe
            rows = replications, cols = KPIs
            
        Returns:
        -------
        plotly.figure
        
        Sources:
        ------
        The code in this function was partly adapted from two sources:
        1. https://stackoverflow.com/questions/59406167/plotly-how-to-filter-a-pandas-dataframe-using-a-dropdown-menu
        
        Thanks and credit to `vestland` the author of the reponse.
        
        2. https://plotly.com/python/dropdowns/
        '''
        # create a figure
        fig = go.Figure()

        # set up a trace
        fig.add_trace(go.Histogram(x=results[results.columns[0]]))

        buttons = []

        # create list of drop down items - KPIs
        # the params in the code would need to vary depending on the type of chart.
        # The histogram will show the first KPI by default
        for col in results.columns:
            buttons.append(dict(method='restyle',
                                label=col,
                                visible=True,
                                args=[{'x':[results[col]],
                                    'type':'histogram'}, [0]],
                                )
                        )

        # create update menu and parameters
        updatemenu = []
        your_menu = dict()
        updatemenu.append(your_menu)

        updatemenu[0]['buttons'] = buttons
        updatemenu[0]['direction'] = 'down'
        updatemenu[0]['showactive'] = True
        updatemenu[0]['x'] = 0.25
        updatemenu[0]['y'] = 1.1
        updatemenu[0]['xanchor'] = 'right'
        updatemenu[0]['yanchor'] = 'bottom'
             
        # add dropdown menus to the figure
        fig.update_layout(showlegend=False, 
                        updatemenus=updatemenu)
        
        # add label for selecting performance measure
        fig.update_layout(
        annotations=[
            dict(text="Performance measure", x=0, xref="paper", y=1.25, 
                yref="paper", align="left", showarrow=False)
        ])
        return fig

    @render.data_frame
    def result_table():
        '''
        Reactive event to when the run simulation button
        is clicked.
        '''
        return summary_results(replication_results())
    
    @render_widget
    def histogram():
        '''
        Updates the interactive histogram

        Returns:
        -------
        plotly.figure
        '''
        return create_user_filtered_hist(replication_results())

    @reactive.Effect
    @reactive.event(input.run_sim)
    async def _():
        '''
        Runs simulation model when button is clicked.
        This is a reactive effect. Once replication_results
        is set it invalidates results_table and histogram.  
        These are rerun by Shiny
        '''
        # set to empty - forces shiny to dim output widgets
        # helps with the feeling of waiting for simulation to complete
        replication_results.set([])
        ui.notification_show("Simulation running. Please wait", type='warning')
        replication_results.set(run_simulation())
        ui.notification_show("Simulation complete.", type='message')

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, static_assets=www_dir)