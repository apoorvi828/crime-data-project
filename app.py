from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('CrimesOnWomenData.csv')

# Helper functions to generate charts
def get_growth_rate_data():
    crimes = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    growth_rate = df.groupby('Year')[crimes].sum().pct_change() * 100
    traces = [go.Scatter(x=growth_rate.index, y=growth_rate[crime], mode='lines+markers', name=crime) for crime in crimes]
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_total_cases_data():
    crimes = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    total_cases = df.groupby('Year')[crimes].sum()
    traces = [go.Bar(x=total_cases.index, y=total_cases[crime], name=crime) for crime in crimes]
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_average_cases_by_state():
    # Group the data by 'State' and calculate the mean for the specified columns
    avg_cases_by_state = df.groupby('State')[['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']].mean()

    # Create histograms for each crime category with adjusted width
    traces = []
    for crime in avg_cases_by_state.columns:
        trace = go.Histogram(
            x=avg_cases_by_state[crime],
            name=crime,
            marker=dict(
                line=dict(
                    width=0.5  # Adjust the width here
                )
            )
        )
        traces.append(trace)

    # Convert the charts to JSON format
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_rape_cases_data():
    avg_rape_cases = df.groupby('Year')['Rape'].mean()
    trace = go.Scatter(x=avg_rape_cases.index, y=avg_rape_cases.values, mode='lines+markers', name='Average Rape Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_DD_cases_data():
    avg_DD_cases = df.groupby('Year')['DD'].mean()
    trace = go.Scatter(x=avg_DD_cases.index, y=avg_DD_cases.values, mode='lines+markers', name='Average DD Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_AoW_cases_data():
    avg_AoW_cases = df.groupby('Year')['AoW'].mean()
    trace = go.Scatter(x=avg_AoW_cases.index, y=avg_AoW_cases.values, mode='lines+markers', name='Average Aow Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_AoM_cases_data():
    avg_AoM_cases = df.groupby('Year')['AoM'].mean()
    trace = go.Scatter(x=avg_AoM_cases.index, y=avg_AoM_cases.values, mode='lines+markers', name='Average AoM Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_DV_cases_data():
    avg_DV_cases = df.groupby('Year')['DV'].mean()
    trace = go.Scatter(x=avg_DV_cases.index, y=avg_DV_cases.values, mode='lines+markers', name='Average DV Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_WT_cases_data():
    avg_WT_cases = df.groupby('Year')['WT'].mean()
    trace = go.Scatter(x=avg_WT_cases.index, y=avg_WT_cases.values, mode='lines+markers', name='Average WT Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_highest_rape_cases_data():
    highest_rape_cases = df.groupby('Year')['Rape'].max()
    trace = go.Bar(x=highest_rape_cases.index, y=highest_rape_cases.values, name='Highest Rape Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_lowest_rape_cases_data():
    lowest_rape_cases = df.groupby('Year')['Rape'].min()
    trace = go.Bar(x=lowest_rape_cases.index, y=lowest_rape_cases.values, name='Lowest Rape Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_highest_DD_cases_data():
    highest_DD_cases = df.groupby('Year')['DD'].max()
    trace = go.Bar(x=highest_DD_cases.index, y=highest_DD_cases.values, name='Highest DD Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_lowest_DD_cases_data():
    lowest_DD_cases = df.groupby('Year')['DD'].min()
    trace = go.Bar(x=lowest_DD_cases.index, y=lowest_DD_cases.values, name='Lowest DD Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)


def get_highest_lowest_other_crimes_data():
    crimes = ['K&A','DD', 'AoW', 'AoM', 'DV', 'WT']
    highest_lowest_other = df.groupby('Year').agg({crime: ['min', 'max'] for crime in crimes})
    
    traces = []
    for crime in crimes:
        traces.append(go.Scatter(x=highest_lowest_other.index, y=highest_lowest_other[crime]['max'], mode='lines+markers', name=f'Highest {crime}'))
        traces.append(go.Scatter(x=highest_lowest_other.index, y=highest_lowest_other[crime]['min'], mode='lines+markers', name=f'Lowest {crime}'))
    
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

# Route for Home Page
@app.route('/')
def home():
    growth_rate_data = get_growth_rate_data()
    total_cases_data = get_total_cases_data()
    return render_template('index.html', growth_rate_data=growth_rate_data, total_cases_data=total_cases_data)

@app.route('/overview')
def overview():
    growth_rate_data = get_growth_rate_data()
    total_cases_data = get_total_cases_data()
    return render_template('overview.html', growth_rate_data=growth_rate_data, total_cases_data=total_cases_data)

# Route for Crime Distribution Page
@app.route('/crime-distribution')
def crime_distribution():
    average_cases_data = get_average_cases_by_state()
    return render_template('crime_distribution.html', average_cases_data=average_cases_data)

# Route for Crime Categories Page
@app.route('/crime-categories')
def crime_categories():
    rape_cases_data = get_rape_cases_data()
    DD_cases_data = get_DD_cases_data()
    AoW_cases_data = get_AoW_cases_data()
    AoM_cases_data = get_AoM_cases_data()
    DV_cases_data = get_DV_cases_data()
    WT_cases_data = get_WT_cases_data()
    return render_template('crime_categories.html', rape_cases_data=rape_cases_data, DD_cases_data=DD_cases_data, AoW_cases_data=AoW_cases_data,  AoM_cases_data=AoM_cases_data,  DV_cases_data=DV_cases_data,  WT_cases_data=WT_cases_data)

# Route for Yearly Comparison Page
@app.route('/yearly-comparison')
def yearly_comparison():
    highest_rape_cases_data = get_highest_rape_cases_data()
    lowest_rape_cases_data = get_lowest_rape_cases_data()
    highest_DD_cases_data = get_highest_DD_cases_data()
    lowest_DD_cases_data = get_lowest_DD_cases_data()
    highest_lowest_other_crimes_data = get_highest_lowest_other_crimes_data()
    return render_template('yearly_comparison.html', highest_rape_cases_data=highest_rape_cases_data,
                           lowest_rape_cases_data=lowest_rape_cases_data,
                           highest_DD_cases_data=highest_DD_cases_data,
                           lowest_DD_cases_data=lowest_DD_cases_data,
                           highest_lowest_other_crimes_data=highest_lowest_other_crimes_data)

if __name__ == '__main__':
    app.run(debug=True)
