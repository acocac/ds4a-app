#import data related libraries
import pandas as pd
import pickle

#import dash related libraries
import dash_core_components as dcc

# import viz related libraries
import plotly.graph_objs as go


loadModel = pickle.load(open("model/Model_dash.pickle", "rb"))


# Predictor Function
def pred_outputs(x):
    prediction = loadModel.predict(x)
    predictProba = loadModel.predict_proba(x)
    return prediction, predictProba


def get_pred(age, gender, sentence, study, education, work, intramuros, crimes, calificado, agravado, cluster1, cluster4, cluster5):
    data = pd.DataFrame({'edad': [age],
                         'sentencia': [sentence],
                         'actividades_estudio': [study],
                         'CLUSTER_4': [cluster4],
                         'actividades_trabajo': [work],
                         'calificado': [calificado],
                         'nivel_educativo': [education],
                         'estado_ingreso_Intramuros': [intramuros],
                         'cuenta_delitos': [crimes],
                         'agravado': [agravado],
                         'CLUSTER_5': [cluster5],
                         'CLUSTER_1': [cluster1],
                         'genero': [gender]}
                        )

    prediction, predictProba = pred_outputs(data)
    target = ''
    if (prediction[0] == 1):
        target = 'RECIDIVIST'
        prob = predictProba[:, 1]
    else:
        target = 'NON-RECIDIVIST'
        prob = predictProba[:, 0]

    return target, "{0:.0%}".format(float(prob))


#create VarImp plot
feature_important = loadModel.get_booster().get_score(importance_type='weight')
keys = list(feature_important.keys())
values = list(feature_important.values())

imp_fig = go.Figure(go.Bar(
        x=values,
        y=keys,
        marker=dict(
            color='#00b6cb'
        ),
        orientation='h',
    ))

imp_fig.update_layout(yaxis={'categoryorder': 'total ascending'})

imp_fig.update_layout(title=f'Variable Importance',
                  paper_bgcolor="#2c2f38",
                  plot_bgcolor='#2c2f38',
                  font=dict(color='#fefefe'),
                  xaxis_title='Importance',
                  yaxis_title='Variable'
                  )

imp_fig.update_traces(showlegend=False)


def plotImp():
    return dcc.Graph(figure=imp_fig, id='Bar1')