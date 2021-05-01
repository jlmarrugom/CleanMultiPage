import dash_core_components as dcc
import dash_html_components as html
import base64
import callbacks

#####################
# Nav bar
def get_navbar(p = 'gen'):

    navbar_gen = html.Div([

        html.Div([], className = 'two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'General Overview'),
                href='/general_overview'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Pacientes'),
                href='/apps/pacientes'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Animales'),
                href='/apps/animales'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Aire'),
                href='/apps/aire'
                )
        ],
        className='two columns'),

        html.Div([], className = 'two columns')

    ],
    className = 'row',style = {'textAlign' : 'center'}
    )

    navbar_page2 = html.Div([

        html.Div([], className = 'two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'General Overview'),
                href='/general_overview'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Pacientes'),
                href='/apps/pacientes'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Animales'),
                href='/apps/animales'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Aire'),
                href='/apps/aire'
                )
        ],
        className='two columns'),

        html.Div([], className = 'two columns')

    ],
    className = 'row',style = {'textAlign' : 'center'}
    )
    navbar_page3 = html.Div([

        html.Div([], className = 'two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'General Overview'),
                href='/general_overview'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Pacientes'),
                href='/apps/pacientes'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Animales'),
                href='/apps/animales'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Aire'),
                href='/apps/aire'
                )
        ],
        className='two columns'),

        html.Div([], className = 'two columns')

    ],
    className = 'row',style = {'textAlign' : 'center'}
    )
    navbar_page4 = html.Div([

        html.Div([], className = 'two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'General Overview'),
                href='/general_overview'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Pacientes'),
                href='/apps/pacientes'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Animales'),
                href='/apps/animales'
                )
        ],
        className='two columns'),

        html.Div([
            dcc.Link(
                html.H6(children = 'Aire'),
                href='/apps/aire'
                )
        ],
        className='two columns'),

        html.Div([], className = 'two columns')

    ],
    className = 'row',style = {'textAlign' : 'center'}
    )

    if p == 'gen':
        return navbar_gen
    elif p == 'page2':
        return navbar_page2
    elif p== 'page3':
        return navbar_page3
    else:
        return navbar_page4


layout0 = html.Div([
        get_navbar('gen'),
        html.Div([
            html.H1(children='ControlBox'),
            html.P('Sistema de información para la caracterización, identificación, información, y previsión de riesgo de contagio por covid-19.'),
            html.Div(children='''
                En este es el Dashboard puede encontrar
                toda la información relacionada al proyecto
                ControlBox
            '''),
           
        ], className='row'),
        html.Div([
            html.H3(children='Analisis de Edad'),

            html.P('Prueba:'),
            dcc.Dropdown(
                id='barras_edad',
                value='PCR',
                options=[{'value':x, 'label':x}
                        for x in ['PCR','Serologia']],
                clearable=False   
            ),
            dcc.Graph(
                id='bar_chart',
                config={
                'displayModeBar': False
            }
            ),  
        ], className='row')

],style = {'width':'auto','margin': '25px 50px'})

layout1 = html.Div([
    get_navbar('page2'),
    html.Div([
        
        html.H3(children='Síntomas'),
        html.P('Prueba:'),
            dcc.Dropdown(
                id='prueba_radial',
                value='Serologia',
                options=[{'value':x, 'label':x}
                        for x in ['PCR','Serologia']],
                clearable=False   
            ),
        dcc.Graph(
            id='radial_plot',
            config={
            'displayModeBar': False
            })
    ],className='eight columns'),
        html.Div([
            html.H3(children='Mapa de Pruebas'),
            html.P('Prueba:'),
            dcc.Dropdown(
                id='prueba',
                value='Serologia',
                options=[{'value':x, 'label':x}
                        for x in ['PCR','Serologia']],
                clearable=False   
            ),
            html.Iframe(id='map',#graficamos el mapa como un Iframe
            srcDoc=open('assets/prueba_por_municipios.html','r').read(),width='90%',height='400')
                ],className = 'four columns'),
        ], className = 'row',style = {'width':'auto','margin': '25px 50px'})

layout2 = html.Div([
    get_navbar('page3'),
    html.H3(children='Animales'),

            html.Div(children='''
                Murcielagos
            '''),
            html.P('Variable:'),
            dcc.Dropdown(
                id='variables',
                value='Lugar',
                options=[{'value':x, 'label':x}
                        for x in ['Fecha de  toma de muestra','Lugar','Urb/Rural','Especie','Sexo']], #df_mur.columns[2:8]]
                clearable=False   
            ),
            dcc.Graph(
                id='donut_chart',
                config={
                'displayModeBar': False
                }
                #figure=fig3
            ),  
        ], className='row',style = {'width':'auto','margin': '25px 50px'})
#load tree image
image_filename = '/assets/tree.png'

layout3 = html.Div([
    get_navbar('page4'),
    html.H3(children='Aire'),

            html.Div(children='''
                Análisis
            '''),
            html.P('Los análisis referentes a calidad de aire.'),
        html.Div([
            html.Div([
                html.Div([
                html.Div([
                    html.P('Variable:'),
                    dcc.Dropdown(
                        id='columna',
                        value='MUNICIPIO',
                        options=[{'value':x, 'label':x}
                                for x in ['MUNICIPIO',                                                                                                                  
                                            'ZONA',  
                                            'UBICACION',                                                                              
                                            'TIPOBOM',                 
                                            'SEXO',                                 
                                            'VENTILACION_MECANICA_',                                                                            
                                            'PATOLOGIA_BASE',                                                           
                                            'V_NAT',
                                            'AIRE_ACOND',
                                            'VENTILADORES',
                                            'VEHICULOS',
                                            'POLVO']],
                        clearable=False   
                    )
                ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                html.Div([
                    html.P('Campaña:'),
                    dcc.Dropdown(
                        id='campaña',
                        value='1',
                        options=[{'value':x, 'label':x}
                                for x in ['1','2','Exteriores']],
                        clearable=False   
                    )
                ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                ],className='row'),
                dcc.Graph(
                    id='cat_chart',
                    config={
                    'displayModeBar': False
                    }),
                
            ], className='eight columns'),
            
            
        html.Div([
            
            html.H3('Resultados PCR Agrupados'),
            html.P("""
            Se puede observar que en la campaña 1 fue la única donde se encontraron resultados PCR Positivos. 
            """),
            html.P("""
            En las otras campañas no pueden apreciarse diferencias en los resultados de las pruebas ya que solo
            fueron registrados resultados Negativos.
            """)
        ],className='four columns',style = {'margin-top': '80px'}),
        ],className='row'),

        html.Div([
            html.Div([
                html.H3('Diagrama de Correlación'),
                html.P("""
                La matriz de correlación presenta las posibles relaciones entre variables,
                siendo -1 inversamente proporcional y 1 directamente proporcional. De esa forma, 
                se observa un comportamiento similar entre las 3 campañas.                
                """)
            ],className='eight columns'),
            html.Div([
                html.Div([
                    html.P('Campaña:'),
                    dcc.Dropdown(
                        id='campaña1',
                        value='1',
                        options=[{'value':x, 'label':x}
                                for x in ['1','2','Exteriores']],
                        clearable=False   
                    )
                ],className='row',style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),
                html.Div([
                html.Img(id='corr_plot',style={'height':'100%', 'width':'100%'})
                ],className='row'),
                ], className='four columns'),
            
        ],className='row'),
        
        html.Div([
            html.Div([
            
            html.Img(src=image_filename, style={'height':'100%', 'width':'100%'}),
            ],className='eight columns'),
                
            html.Div([
                html.H3('Árbol de Decisión'),
                html.P("""
                Para un mejor entendimiento de las variables, se generó un árbol de decisiones
                que muestra la serie de condiciones posibles que se deben presentar para obtener un resultado PCR positivo,
                en terminos de probabilidad. Es así como cada variable representada por un nodo es dividida en dos posibilidades,
                una flacha hacia a la izquiera si la desigualdad es verdadera y a la derecha en caso contrario. 
                """),
                html.P("""
                El valor de la probabilidad de que el resultado sea positivo, dadas las condiciones evaluadas, está dada en el 
                resultado de "value". Es así como para PM2 <= 9.2 y HCOH <= 1.51 la probabilidad de un resultado PCR positivo es 0%. 
                """),
                html.P("""
                Ahora, siguiendo las condiciones anteriores pero con HCOH > 1.51, CAUDAL > 4.6, AQI <= 15.5 y evaluando nuevamente 
                PM2 pero esta vez debe ser > 4.1, la probabilidad de un resultado PCR positivo es 100%.
                """)
            ],className='four columns'),
        ],className='row')

    ], className='row',style = {'width':'auto','margin': '25px 50px'})
