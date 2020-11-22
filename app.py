# Dash Web Applications

from datetime import date

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px  

from settings import DB_FILE
from etl.db_operations import create_connection

from analytics.analytics_functions import get_chart_data

# Location of SQLite database file
dbfile = DB_FILE

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H1("Electricity Hourly Prices",
        style = { 
            'textAlign': 'center',
            'margin': '20px'
        }
    ),
    
    html.Div([
                html.Label(children = "Select Date Range: ",
                    style = {
                        'textAlign': 'left',
                        'margin-right': '20px'
                        }
                ),
        
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    display_format='YYYY-MM-DD',
                    min_date_allowed=date(2018, 1, 1),
                    max_date_allowed=date(2020, 9, 30),
                    initial_visible_month=date(2020, 9, 1),
                    start_date = date(2020, 9, 1),
                    end_date=date(2020, 9, 30)
                ),   
            ],
            
            style = {
                'margin-top': '10px',
                'margin-bottom': '10px',
                'font-weight': 'bold'
            }
        ),
        
    
        dcc.Graph(id='graph-electricity-prices', figure={})
    
    
    ],
    style = {
        'margin':'0',
        'font-family': 'Arial Narrow'
    }
)

@app.callback(
    dash.dependencies.Output('graph-electricity-prices', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):

    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        
    # Connect to SQLite DB and get chart data
    conn = create_connection(DB_FILE)
    data = get_chart_data(conn, start_date_object, end_date_object)
    t = []
    prices = []
    regions = []
    
    for row in data:
        # Time
        t.append(row[0])
        # Region
        if row[1] == 'DK1':
            regions.append('DK')
        elif row[1] == 'SE1':
            regions.append('SE')
        else:
            regions.append(row[1])
        # Price
        prices.append(row[2])
    
    # Chart Settings 
    figure = px.line(
        x=t,
        y=prices,
        line_group = regions,
        color = regions,
        labels = {
            'x':'Date',
            'y':'Price, EUR/MWh',
            'color':'Regions'
            },
        template='plotly_dark',
        title = "Electricity Prices, EUR/MWh"
    )
    figure.update_layout(
        font_family="Courier New"
    )
    
    # Close DB connection
    conn.close()
    
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    