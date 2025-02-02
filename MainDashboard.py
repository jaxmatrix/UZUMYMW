import numpy as np
import pandas as pd
import panel as pn

# Plotting Imports 
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10, Category20, Viridis256, Inferno256

from datetime import datetime, timedelta
import datetime as dt

from Dataset.MarketDatasets import df_sales
from Dataset.DataGen import df_claims, df_ehr, df_registry, df_rwe, df_tcga
from Dataset.Prevelance import df_epi

# Types and Categories 
from Dataset.MarketDatasets import CANCER_TYPES
from Dataset.MarketDatasets import DRUGS_BY_STAGE
from Dataset.MarketDatasets import COMPETITORS
from Dataset.Prevelance import US_REGIONS
from Dataset.Prevelance import US_STATES
from Dataset.DataGen import THERAPY_SEGMENT_BY_STAGE
from Dataset.DataGen import GENE_LIST

pn.extension()

# -----------------------------------------------------------------------------
# Create a synthetic DataFrame
# -----------------------------------------------------------------------------

# Date range
dates = pd.date_range(start="2014-01-01", periods=180, freq="M")
COLORS = [
    '#8AB1D2', '#FD9F5F', '#E47D78', '#9E7EDE', '#5DAEFF',
    '#447EAE', '#EF6303', '#CA3028', '#6131C1', '#0079F2',
]

# Some categories and sub-groups
categories = ["Alpha", "Beta", "Gamma"]
groups = ["Group 1", "Group 2", "Group 3"]

df = pd.DataFrame({
    "date": np.random.choice(dates, 500),
    "category": np.random.choice(categories, 500),
    "group": np.random.choice(groups, 500),
    "value": np.random.randn(500).cumsum()  # random walk for demonstration
})

# Ensure DataFrame is sorted by date for clarity
df = df.sort_values("date").reset_index(drop=True)

# -----------------------------------------------------------------------------
# Define widgets
# -----------------------------------------------------------------------------
date_slider = pn.widgets.DateRangeSlider(
    name="Date Range",
    start=df_epi['year'].min(),
    end=df_epi['year'].max(),
    value=(df_epi['year'].min(), df_epi['year'].max()),
    step=1
)

multi_cancer_type = pn.widgets.MultiSelect(
    name="Cancer Types",
    options=list(df_epi["cancer_type"].unique()),
    value=list(df_epi["cancer_type"].unique()),
    size=5
)

cancer_stages = [1, 2, 3, 4]

multi_cancer_stage = pn.widgets.MultiSelect(
    name="Cancer Stage",
    options=cancer_stages,
    value=cancer_stages,
    size=4
)

therapy_list = [THERAPY_SEGMENT_BY_STAGE[key] for key in THERAPY_SEGMENT_BY_STAGE.keys()]

line_of_therapy = pn.widgets.CheckBoxGroup(
    name='Line of Therapy', options=therapy_list, value=therapy_list
)

biomarkers_expression = pn.widgets.CheckBoxGroup(
    name='Gene of Interest', options=GENE_LIST, value=GENE_LIST
)

# Forecast Input Fields 
forecast_horizon = pn.widgets.IntInput(name='Forecast Horizon (months)', value=5, step=1, start=1, end=100)
future_market_forecast = pn.widgets.IntInput(name='Future Market Forecast', value=5, step=1, start=1, end=12)
base_market_share = pn.widgets.FloatInput(name='FloatInput', value=5., step=1e-1, start=0, end=1000)
target_market_share = pn.widgets.FloatInput(name='FloatInput', value=5., step=1e-1, start=0, end=1000)
gross_to_net_discount = pn.widgets.FloatInput(name='FloatInput', value=5., step=1e-1, start=0, end=1000)
base_demand = pn.widgets.IntInput(name='Future Market Forecast', value=5, step=1, start=1, end=12)
our_product_market_entry = pn.widgets.DateSlider(name='Date Slider', start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
our_product_market_decline = pn.widgets.DateSlider(name='Date Slider', start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))

forecast_input_list = [
    forecast_horizon,
    future_market_forecast,
    base_market_share,
    target_market_share,
    gross_to_net_discount,
    base_demand,
    our_product_market_entry,
    our_product_market_decline
]
# Model Simulation Fields 

patient_flow_simulation_time = pn.widgets.IntInput(name='Future Market Forecast', value=5, step=1, start=1, end=12)
simulation_cycles = pn.widgets.IntInput(name='Future Market Forecast', value=5, step=1, start=1, end=12)

# Action Button 
simulate_button = pn.widgets.Button(name='Simulate', button_type='primary')

# def handle_click(clicks):
#     return f'You have clicked me {clicks} times'

# pn.Column(
#     button,
#     pn.bind(handle_click, button.param.clicks),
# )



# -----------------------------------------------------------------------------
# Helper function to filter DataFrame based on widget values
# -----------------------------------------------------------------------------
def filter_epi_data(df, date_range, cancer_types, cancer_stages):
    """Return a filtered DataFrame based on date range and selected categories/groups."""
    start_date, end_date = date_range
    mask = (
        (df["year"] >= pd.to_datetime(start_date)) &
        (df["year"] <= pd.to_datetime(end_date)) &
        (df["cancer_type"].isin(cancer_types)) &
        (df["cancer_stage"].isin(cancer_stages))
    )
    print("MASK----------WORKING------#########")
    return df[mask]

# -----------------------------------------------------------------------------
# Define Bokeh chart update functions
# -----------------------------------------------------------------------------
@pn.depends(
    date_slider.param.value,
    multi_cancer_type.param.value,
    multi_cancer_stage.param.value
)
def prevelance_tab(date_range, selected_categories, selected_groups):
    """
    Tab 1: A line chart showing sum of 'value' by date.
    """
    filtered = filter_epi_data(df_epi, date_range, selected_categories, selected_groups)

    # Aggregate by date
    agg = filtered.groupby(["year", "cancer_type"])['prevalence_count'].sum().reset_index()

    print("Filtered Data  ############################")
    print(agg)

    # Create a Bokeh figure
    p = figure(
        width=700, height=400, 
        x_axis_type="datetime", 
        title="Tab 1: Yearly Prevelance data for cancer"
    )

    cancer_types = list(agg['cancer_type'].unique())
    num_cancer_types = len(cancer_types)
    print(num_cancer_types, cancer_types)
    palette = COLORS


    for i,cancer_type in enumerate(cancer_types) :
        source = ColumnDataSource(agg[agg["cancer_type"] == cancer_type])
        line = p.line("year", "prevalence_count", legend_label=cancer_type, source=source, line_width=2, color=palette[i])


    # p.circle("date", "value", source=source, size=6, color="navy")
    p.xaxis.axis_label = "Year"
    p.yaxis.axis_label = "Prevalence Count"

    return p


@pn.depends(
    date_slider.param.value,
    multi_cancer_type.param.value,
    multi_cancer_stage.param.value
)
def incidence_tab(date_range, selected_categories, selected_groups):
    """
    Tab 1: A line chart showing sum of 'value' by date.
    """
    filtered = filter_epi_data(df_epi, date_range, selected_categories, selected_groups)

    # Aggregate by date
    agg = filtered.groupby(["year", "cancer_type"])['incidence_count'].sum().reset_index()

    print("Filtered Data  ############################")
    print(agg)

    # Create a Bokeh figure
    p = figure(
        width=700, height=400, 
        x_axis_type="datetime", 
        title="Tab 2: Yearly Incidence data for cancer"
    )

    cancer_types = list(agg['cancer_type'].unique())
    num_cancer_types = len(cancer_types)
    print(num_cancer_types, cancer_types)
    palette = COLORS


    for i,cancer_type in enumerate(cancer_types) :
        source = ColumnDataSource(agg[agg["cancer_type"] == cancer_type])
        line = p.line("year", "incidence_count", legend_label=cancer_type, source=source, line_width=2, color=palette[i])


    # p.circle("date", "value", source=source, size=6, color="navy")
    p.xaxis.axis_label = "Year"
    p.yaxis.axis_label = "Incidence Count"

    return p



def calculate_parameters(df):
    # Calculate Total Population

    # Incidence Rate 

    # Prevalence Rate 

    # Diagnosis Rate

    # Treeatment Rate 

    # Biomarker Prevelance Rate

    # Chemo Experience Rate 

    # Transition Matrix Values 
        ## Patient Flow Transition ( line of therapy )
        ## Patient Flow Transition ( Health State Transition )
        ## Disease Stage Transition 
    
    pass 

def calculate_scenario(df):
    # Calculate Market Projection for [best case, average case, worst case]

    pass

def calculate_health_economic_model(df):
    # Cost per State


    # Utility Per State 

    # ICER Benchmark
    pass 

def calculate_competitor_info(df):
    # For Every Competitor 
        ## Start Month 
        ## End Month
    
    # Our Product Stats
        ## Our Product Start 
        ## Our Product End 

    pass

def patient_segmentation(df):
    pass 

@pn.depends(
    date_slider.param.value,
    multi_cancer_type.param.value,
    multi_cancer_stage.param.value
)
def updateData(one, two, three):
    print("Updating DataFrame Test ####################################")
    print(one,two,three)

    calculated_display = pn.Column(
        "First : **FIRST**",
        "First : **FIRST**",
        "First : **FIRST**",
        "First : **FIRST**",
    )

    calculated_display2 = pn.Column(
        "First : **FIRST**",
        "First : **FIRST**",
        "First : **FIRST**",
        "First : **FIRST**",
    )

    return pn.Row(calculated_display, calculated_display2)

market_simulation_input_grid = pn.GridBox(*forecast_input_list, ncols=4)
market_simulation_tab = pn.Column(
    simulate_button,
    market_simulation_input_grid
)



epi_plots = pn.Row(
    prevelance_tab, incidence_tab
)

epi_tab = pn.Column(
    updateData,
    epi_plots,
)

main_layout = pn.Tabs(
    ("Epi Data", epi_tab),
    ("Market Simulation", market_simulation_tab),
)
# -----------------------------------------------------------------------------
# Layout: sidebar (widgets) + main (tabs)
# -----------------------------------------------------------------------------
# Clinical Data Filters
clinical_filters = pn.WidgetBox(
    "<b>Clinical Filters</b>",
    "Line of therapies",
    line_of_therapy,
    "Gene Expression",
    biomarkers_expression,
    width=359
)

# General Filters 
filters = pn.WidgetBox(
    "<br/><b>Filters</b>",
    date_slider,
    multi_cancer_stage,
    multi_cancer_type,
    width=359,
)


# Using a Template for a cleaner look, but you can also just use a row/column layout.
dashboard = pn.template.MaterialTemplate(
    title="Market Forecasting Dashboard",
    sidebar=[clinical_filters, "  " ,filters],
    main=[ main_layout],
)

# Serve or display the dashboard
dashboard.servable()
