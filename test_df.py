from pathlib import Path
import pandas as pd
from shiny import ui, render, App

df = pd.read_csv(Path(__file__).parent / "salmon.csv")

app_ui = ui.page_fluid(
    ui.output_table("salmon_species"),
)

def server(input, output, session):
    @output
    @render.table
    def salmon_species():
        return df

app = App(app_ui, server)
