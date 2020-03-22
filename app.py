import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output,Input
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd

# load and prepare data
country_list = [{'label': 'globe', 'value': 'globe'},{'label': 'india', 'value': 'india'}]
df = pd.read_csv('./Data/covid19_1.csv')
#Get rid of row containing total of columns
df = df[df['Name of State / UT'] != 'Total number of confirmed cases in India']
states = df['Name of State / UT'].unique()

#preparing states list for dropdown filter
state_options = []
for state in states:
    state_options.append({'label':state, 'value': state})


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = 'My Title'

#Setup static chart
def setup_india_chart(dataframe):
    df = dataframe
    data = []
    for cat in df.columns[3:5]:
        print(cat)
        data.append(
            go.Bar(
                x=df['Name of State / UT'],
                y=df[cat],
                name=cat,
                textangle=45
            )
        )

    india_fig = {
        'data': data,
        'layout': go.Layout(
            xaxis={'type': '-', 'title': 'State'},
            yaxis={'title': 'Case Count'},
            barmode='stack',
            margin={'t': 35}
        )
    }

    return india_fig

india_chart = setup_india_chart(df)


app.layout = html.Div(
    [
        #html.Div(id="output-clientside"),
        html.Div([
            html.Div([
                html.Img(
                    src=app.get_asset_url("logo.png"),
                    id="plotly-image",
                    style={
                        "height": "60px",
                        "width": "auto",
                        "margin-bottom": "25px",
                    },
                )
            ],className="one-third column"),
            html.Div([
                html.Div(
                    [
                        html.H3(
                            "Corona pandemic",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "Covid - 19 Outbreak Visualization", style={"margin-top": "0px"}
                        ),
                    ]
                )
            ], className="one-half column",id="title",),
            html.Div([

            ], className="one-third column")
        ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"}
        ),#End of header
        html.Div([
            html.Div([
                html.P(
                    "Filter:",
                    className="control_label",
                ),
                html.Div([
                    dcc.Dropdown(id='state-picker',value="",options=state_options)
                ])
            ],className="pretty_container four columns",id="cross-filter-options"),
            html.Div([
                html.Div(
                    [
                        html.Div(
                            [html.P("Confirmed Cases(Local)"),html.H6(id="totalLocalCasesText")],
                            id="total-cases-local",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.P("Confirmed Cases(Foreign)"),html.H6(id="totalForeignCasesText")],
                            id="total-cases-foreign",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.P("Cured Cases"),html.H6(id="totalCuredCasesText")],
                            id="total-cured",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.P("Deaths"),html.H6(id="totalDeathCasesText")],
                            id="total-death",
                            className="mini_container",
                        ),
                    ],
                    id="info-container",
                    className="row container-display",
                )
            ],
                className="eight columns",
                id="right-column"
            )
        ],className="row flex-display"),#End of stat cards and filter
        html.Div([
            html.Div(
                [dcc.Graph(id="india_graph",figure=india_chart)],
                className="pretty_container seven columns",
            ),
            html.Div(
                [dcc.Graph(id="world_graph")],
                className="pretty_container five columns",
            )
        ],className="row flex-display")
    ],
        id="mainContainer",
        style={"display": "flex", "flex-direction": "column"}
)







@app.callback([Output('totalLocalCasesText','children'),
               Output('totalForeignCasesText','children'),
               Output('totalCuredCasesText','children'),
               Output('totalDeathCasesText','children')],
              [Input('state-picker','value')])
def update_stats(state_name):
    result = []
    if (state_name == None) or (state_name == '') :
        result.append(df['Total Confirmed cases (Indian National)'].apply(pd.to_numeric).sum())
        result.append(df['Total Confirmed cases ( Foreign National )'].apply(pd.to_numeric).sum())
        result.append(df['Cured/Discharged/Migrated'].apply(pd.to_numeric).sum())
        result.append(df['Death'].apply(pd.to_numeric).sum())
        print(result)
        return result
    else:
        print("value selected {}".format(state_name))
        result.append(df[df['Name of State / UT'] == state_name]['Total Confirmed cases (Indian National)'].apply(pd.to_numeric))
        result.append(df[df['Name of State / UT'] == state_name]['Total Confirmed cases ( Foreign National )'].apply(pd.to_numeric))
        result.append(df[df['Name of State / UT'] == state_name]['Cured/Discharged/Migrated'].apply(pd.to_numeric))
        result.append(df[df['Name of State / UT'] == state_name]['Death'].apply(pd.to_numeric))
        return result




if __name__ == '__main__':
    app.run_server()
    # df = pd.read_csv('./Data/covid19_1.csv')
    # print(df.columns)
    # #getting rid of total row from dataframe
    # df = df[df['Name of State / UT'] != 'Total number of confirmed cases in India']
    # print(df[['Name of State / UT','Total Confirmed cases (Indian National)','Total Confirmed cases ( Foreign National )']])
    #
    #
    # df = pd.read_csv