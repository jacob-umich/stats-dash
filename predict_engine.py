import pickle
import dash
import numpy as np

with open('model.pkl','rb') as f:
    model = pickle.load(f)


@dash.callback(
    dash.Output(component_id="ml_predict",component_property="children"),
    dash.Input(component_id='ml_ob',component_property="value"),
    dash.Input(component_id='ml_smoke',component_property="value"),
    dash.Input(component_id='ml_sleep',component_property="value")
)
def predict(obesity,sleep,smoke):
    x = np.array([[obesity,smoke,sleep]])
    y =  model.predict(x)
    print(y)
    return f"{y[0]}"
