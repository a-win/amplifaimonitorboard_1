import pyodbc
import pandas as pd
import numpy as np
import datetime as dt
import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Output, Input


external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app = dash_app.server

dash_app.layout = html.Div(
    html.Div([
        html.Div(
            [html.Div(
                [html.H4('AmplifAI DataBase Metrics | amplifai20SQLSvcDB |', style={'float': 'left', 'margin-left': '10px','margin-top':'2px'}),
                 html.H6('DTU Consumption Percentage Level',style={'float': 'left', 'margin-left': '20px', 'margin-top':'3px'})], className='row')
            ]),
        html.Div(
            [html.Div(
                [html.Thead('Metric Aggregation Type',style = {'float': 'left', 'margin': 'auto'}),
                dcc.RadioItems(['Min','Max','Avg'],value='Avg',id='range-bands',
                               labelStyle={'display': 'inline-block','margin-left':'10px','marginTop': '1px'},
                               style = {'float': 'left', 'margin': 'auto'})]
                ,className = 'row')
            ]),
        dcc.Interval(id='interval-component',interval=3*1000,n_intervals=0),
        dcc.Graph(id='live-update-graph',config={'displayModeBar':False}, animate=False),
        html.Div(
            [html.Div(
                [html.H6('Application refresh rate (seconds):', style={'float': 'left', 'margin': 'auto'}),
                 html.Thead('please set slider to required setting',style={'float': 'left', 'margin-left': '10px', 'margin-top':'3px'})], className='row')
            ]),
        dcc.Slider(5,60,1, value=5,
                   marks={5:'5',10:'10',15:'15',20:'20',25:'25',30:'30',35:'35',40:'40',45:'45',50:'50',55:'55',60:'60'},
                   id='interval-refresh',tooltip={"placement":"bottom","always_visible":True})
    ]))

@dash_app.callback(
    Output(component_id='interval-component', component_property='interval'),
    Input('interval-refresh', 'value'))  # refresh interval

def update_refresh_rate(value):
    return [value * 1000]

@dash_app.callback(
    Output('live-update-graph','figure'),       #Graph component outputs
    Input('interval-component','n_intervals'),  #refresh interval variable
    Input('range-bands','value'))
# #
#
def live_update_graph(interval,value):
    server = 'amplifai20sqldbserver.database.windows.net'
    database = 'amplifai20SQLSvcDB'
    username = 'amplifaiadmin'
    password = 'Ampl1f@1'
    driver = '{ODBC Driver 17 for SQL Server}'
    dtu = []
    utc = []

    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as connector:
        with connector.cursor() as cursor:
            cursor.execute(
                "SELECT end_time,avg_cpu_percent,avg_data_io_percent,avg_log_write_percent FROM sys.dm_db_resource_stats;")
            row = cursor.fetchall()
            for i in range(len(row)):
                utc.append(row[i][0])
                dtu.append(row[i][1])

            data_tuples = list(zip(utc, dtu))
            df = pd.DataFrame(data_tuples, columns=['UTC', 'DTUs%'])
            df['CST'] = df['UTC'].dt.tz_localize('utc').dt.tz_convert('US/Central')
            df['CST'] = df['CST'] + dt.timedelta(minutes=1)
            df.index = df['CST']
            if value=='Avg':
                agg_1m = df.groupby(pd.Grouper(freq='1min')).aggregate(np.mean)
                agg_1m_final = agg_1m.drop(labels='UTC', axis=1)

                ymax = agg_1m_final['DTUs%'].max() * 1.2

                fig = go.Figure(
                    go.Scatter(x=agg_1m_final['CST'], y=agg_1m_final['DTUs%'], line=dict(color='rgb(0,100,80)'),
                               mode='lines'))
                fig.update_layout({'height': 480, 'hovermode': "x unified", 'yaxis_range': (0, ymax)},
                                  template='presentation')
                fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                return fig

            if value=='Min':
                agg_1m = df.groupby(pd.Grouper(freq='1min')).aggregate(np.min)
                agg_1m_final = agg_1m.drop(labels='UTC', axis=1)

                ymax = float(agg_1m_final['DTUs%'].max()) * 1.2

                fig = go.Figure(
                    go.Scatter(x=agg_1m_final['CST'], y=agg_1m_final['DTUs%'], line=dict(color='rgb(0,100,80)'),
                               mode='lines'))
                fig.update_layout({'height': 480, 'hovermode': "x unified", 'yaxis_range': (0, ymax)},
                                  template='presentation')
                fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                return fig

            if value=='Max':
                agg_1m = df.groupby(pd.Grouper(freq='1min')).aggregate(np.max)
                agg_1m_final = agg_1m.drop(labels='UTC', axis=1)

                ymax = float(agg_1m_final['DTUs%'].max()) * 1.2

                fig = go.Figure(
                    go.Scatter(x=agg_1m_final['CST'], y=agg_1m_final['DTUs%'], line=dict(color='rgb(0,100,80)'),
                               mode='lines'))
                fig.update_layout({'height': 480, 'hovermode': "x unified", 'yaxis_range': (0, ymax)},
                                  template='presentation')
                fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightPink')
                return fig


if __name__ == '__main__':
    dash_app.run_server(debug=False)
