from shiny import App, ui, render, reactive, Inputs, Outputs, Session
import shinyswatch

# import the wrapper objects for model interaction.
from ciw_model import Experiment, multiple_replications

app_ui = ui.page_fixed(
    shinyswatch.theme.minty(),
    ui.h2("Ciw Urgent Care Call Centre Model"),
    ui.markdown("""
        This app is based on a [ciw example][0] that simulates a simple call centre model.
        [0]:https://health-data-science-or.github.io/simpy-streamlit-tutorial/content/03_streamlit/13_ciw_backend.html
    """),
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
        ),
        ui.panel_main(
            ui.output_data_frame("result_table")
        )
    )
)

def server(input: Inputs, output: Outputs, session: Session):

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
        summary = replications.describe().round(2)
        # resetting index because cannot figure out how to show index
        return summary.reset_index() 

    @output
    @render.data_frame
    @reactive.event(input.run_sim)
    def result_table():
        '''
        Reactive event to when the run simulation button
        is clicked.
        '''
        #await asyncio.sleep(2)
        #with reactive.isolate():
        return summary_results(run_simulation())

app = App(app_ui, server)