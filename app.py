from shiny import (App, ui, render, reactive, Inputs, Outputs, Session)
from shinywidgets import output_widget, render_widget
import shinyswatch
import plotly.graph_objects as go
import pandas as pd

# import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

app_ui = ui.page_fluid(
    shinyswatch.theme.journal(),
    ui.h1("Ciw Urgent Care Call Centre Model"),
    ui.markdown("""
        This app is based on a 
        [ciw example](https://health-data-science-or.github.io/simpy-streamlit-tutorial/content/03_streamlit/13_ciw_backend.html) 
        that simulates a simple call centre model.
    """),
    ui.navset_tab(
        ui.nav("Interactive simulation", 


            ui.layout_sidebar(
                ui.panel_sidebar(
                    # number of call operators
                    ui.input_slider("n_operators", "Call operators", 1, 40, 13, sep=5),
                
                    # nurses on duty
                    ui.input_slider("n_nurses", "Nurse practitioners", 1, 20, 9),
                    
                    # chance of nurse call back
                    ui.input_slider("chance_callback", "Probability of nurse callback", 0.0, 1.0, 0.4),

                    # Number of replications
                    ui.input_numeric("n_reps", "Replications", value=5),

                    # run simulation model button
                    ui.input_action_button("run_sim", "Run Simulation", class_="btn-primary"),

                    width=2
                ),
                ui.panel_main(

                    ui.row(
                        ui.column(5, ui.output_data_frame("result_table"),),
                        ui.column(7, output_widget("histogram")),
                    ),

                )
            )

        ),
        ui.nav("About", "tab b content"),
    )
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
        # resetting index because cannot figure out how to show index
        summary = summary.reset_index() 
        summary = summary.rename(columns={'index': 'metric'})
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

    @output
    @render.data_frame
    def result_table():
        '''
        Reactive event to when the run simulation button
        is clicked.
        '''
        return summary_results(replication_results())
    
    @output
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

        
app = App(app_ui, server)