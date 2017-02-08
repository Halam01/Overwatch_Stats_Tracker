'''
Created on Aug 11, 2016

@author: Hanna
'''
import plotly.plotly as py
import plotly.graph_objs as go

py.sign_in('halam', 'o2ktki0dy8')
# import plotly.tools as tls
# tls.set_credentials_file(username='halam', api_key='o2ktki0dy8')

fig = {
          "data": [
            {
              "values": wins_values,
              "labels": wins_maps,
              "domain": {"x": [0, .48]},
              "name": "Wins",
              "hoverinfo":"label+percent+name",
              "hole": .4,
              "type": "pie"
            },     
            {
              "values": losses_values,
              "labels": losses_maps,
              "text":"Losses",
              "textposition":"inside",
              "domain": {"x": [.52, 1]},
              "name": "Losses",
              "hoverinfo":"label+percent+name",
              "hole": .4,
              "type": "pie"
            }],
          "layout": {
                "title":("Wins and Losses for {}").format(hero),
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "GHG",
                        "x": 0.20,
                        "y": 0.5
                    },
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "CO2",
                        "x": 0.8,
                        "y": 0.5
                    }
                ]
            }
        }
        py.iplot(fig)