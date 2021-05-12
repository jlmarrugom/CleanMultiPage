import dash
#external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
#Uso mi propio CSS para poderlo editar
#external_stylesheets=external_stylesheets
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

