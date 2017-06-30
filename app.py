import os

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas
import flask

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('app', server=server)
app.title = 'WCBU 2017 Statistics'

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

players = pandas.read_csv('players.csv')

team_options = [
    {'label': team, 'value': team} for team in
    list(players['TeamName'].unique())
]
division_options = [
    {'label': division, 'value': division} for division in
    list(players['Division'].unique())
]


app.layout = html.Div([
    html.H1('Player Statistics'),
    dcc.Dropdown(
        id='divisions-dropdown',
        options=division_options,
        value='Mixed'
    ),
    dcc.Dropdown(
        id='teams-dropdown',
        options=team_options,
        value='India'
    ),
    dcc.Graph(id='my-graph')
], className="container")

app.css.append_css({
    'external_url': (
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8bc4d40ae11324931d832b02dc91183025b50f6a/dash-hello-world.css'
    )
})


@app.callback(Output('my-graph', 'figure'),
              [Input('divisions-dropdown', 'value'), Input('teams-dropdown', 'value')])
def update_graph(division, team):
    title = "Player Statistics - {} - {}".format(team, division)
    team_players = players[(players.TeamName == team) & (players.Division == division)]
    fig = {"data": [
        {
            "values": team_players.Goals,
            "labels": team_players.FirstName,
            "domain": {"x": [0, 0.48]},
            "name": "Goals",
            "textposition":"inside",
            "hoverinfo":"label+value+name",
            "hole": .4,
            "type": "pie",
            "textinfo": "value",
        },
        {
            "values": team_players.Assists,
            "labels": team_players.FirstName,
            "domain": {"x": [0.52, 1]},
            "name": "Assists",
            "hoverinfo":"label+value+name+percent",
            "textposition":"inside",
            "hole": .4,
            "type": "pie",
            "textinfo": "value",
        }
    ],
           "layout": {
               "title": title,
               "annotations": [
                   {
                       "font": {
                           "size": 20
                       },
                       "showarrow": False,
                       "text": "Goals",
                       "x": 0.22,
                       "y": 0.5
                   },
                   {
                       "font": {
                           "size": 20
                       },
                       "showarrow": False,
                       "text": "Assists",
                       "x": 0.785,
                       "y": 0.5
                   }
               ]
        }
    }
    return fig

if __name__ == '__main__':
    app.run_server()
