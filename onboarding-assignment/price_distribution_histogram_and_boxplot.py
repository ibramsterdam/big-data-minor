import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlalchemy
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

engine = sqlalchemy.create_engine('sqlite:///amazon_reviews.sqlite3')
products_df = pd.read_sql_table('products', engine)

def remove_outliers(df, variable):
    Q1 = df[variable].quantile(0.25)
    Q3 = df[variable].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[variable] >= lower_bound) & (df[variable] <= upper_bound)]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Amazon Product Data Analysis"),
    html.Label("Select Variable for X-Axis"),
    dcc.Dropdown(
        id='x-axis-variable',
        options=[
            {'label': 'Price', 'value': 'price'},
            {'label': 'Sales Rank', 'value': 'sales_rank'}
        ],
        value='price'
    ),
    dcc.Dropdown(
        id='plot-type',
        options=[
            {'label': 'Histogram (Without Outliers)', 'value': 'histogram_without_outliers'},
            {'label': 'Box Plot (With Outliers)', 'value': 'boxplot_with_outliers'}
        ],
        value='histogram_without_outliers'
    ),
    dcc.Graph(id='plot')
])

@app.callback(
    Output('plot', 'figure'),
    Input('x-axis-variable', 'value'),
    Input('plot-type', 'value')
)
def update_plot(selected_variable, plot_type):
    if plot_type == 'histogram_without_outliers':
        products_df_filtered = remove_outliers(products_df, selected_variable)
        fig = px.histogram(
            products_df_filtered,
            x=selected_variable,
            title=f'{selected_variable.capitalize()} Distribution (Without Outliers)',
            labels={'value': selected_variable, 'count': 'Frequency'},
            nbins=50
        )
    elif plot_type == 'boxplot_with_outliers':
        fig = px.box(
            products_df,
            y=selected_variable,
            title=f'{selected_variable.capitalize()} Box Plot (With Outliers)',
            labels={'value': selected_variable}
        )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)