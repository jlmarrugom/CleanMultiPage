from dash.dependencies import Input, Output

from app import app
import numpy as np
import pandas as pd
import folium

# import plotly.express as px
import plotly.graph_objects as go
######################################################
#Funciones
######################################################
#Here are all the functions used in the app

def pre_processing(df,nombre):
    """
    Recibe un DataFrame y lo entrega 
    listo para la aplicación.
    nombre: pcr, sero, anim, mur, air
    """
    if nombre=='pcr':
        df['RESULTADO PCR'] = df['RESULTADO PCR'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan,
                                                                'NO LLEGO MUESTRA ':np.nan}).astype(float)
        df['EDAD'] = df['EDAD'].replace({'NO REGISTRA':np.nan}).astype(float).astype('Int16')
        df['MUNICIPIO'] = df['MUNICIPIO'].astype(object).replace({1:'Lorica',
                                                                    2:'Planeta Rica',
                                                                    3:'Tierralta',
                                                                    4:'Sahagun',
                                                                    5:'Montelibano',
                                                                    6:'Montería'})                                           
        df['NOMBRE'] = df['PRIMER NOMBRE']+df['SEGUNDO NOMBRE']+df['PRIMER APELLIDO']+df['SEGUNDO APELLIDO']
    elif nombre=='sero':
        df['MUNICIPIO'] = df['MUNICIPIO'].astype(object).replace({1:'Lorica',
                                                                    2:'Planeta Rica',
                                                                    3:'Tierralta',
                                                                    4:'Sahagun',
                                                                    5:'Montelibano',
                                                                    6:'Montería'}) 
        df['RESULTADO SEROLOGIA'] = df['RESULTADO SEROLOGIA'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan,
                                                                'NO LLEGO MUESTRA ':np.nan}).astype(float)
        df['NOMBRE'] = df['PRIMER NOMBRE']+df['SEGUNDO NOMBRE']+df['PRIMER APELLIDO']+df['SEGUNDO APELLIDO']

    elif nombre=='mur':
        df['Coordenadas'] = df['lat'].astype(str) + ', '+df['lon'].astype(str)
        df['MUNICIPIO'] = df['Lugar']
        df['FECHA'] = pd.to_datetime(df['Fecha de  toma de muestra'],format='%Y-%m-%d')

    elif (nombre=='air1')|(nombre=='air2')|(nombre=='airE'):
        df.columns=df.columns.str.upper()
        df.columns=df.columns.str.replace(' ','_')
        df.columns=df.columns.str.replace('/','_')
        df.columns=df.columns.str.replace('  ','_')
        df.columns=df.columns.str.replace('UBICACI�N_','UBICACION')

        df['FECHA'] = pd.to_datetime(df['FECHA_'],format='%d/%m/%Y')
        df['PCR'] = df['PCR'].replace({'negativo ':0,
                                        'negativo':0,
                                        'positivo':1,
                                       'positivo ':1})

        df[['V_NAT']]=df[['V_NAT']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
        df[['AIRE_ACOND']]=df[['AIRE_ACOND']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
        df[['VENTILADORES']]=df[['VENTILADORES']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
        df[['VEHICULOS']]=df[['VEHICULOS']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
        df[['POLVO']]=df[['POLVO']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
        df[['POLVO']]=df[['POLVO']].replace({'si ':1,
                                             'si':1,
                                             'no':0,
                                             'no ':0})
            
        df=df.replace('nan',np.NaN)
    else:
        df['RESULTADO PCR'] = df['RESULTADO PCR'].replace({'2':0,
                                                                'POSITIVO':1,
                                                                'NEGATIVO':0,
                                                                'Pendiente':np.nan,
                                                                'NO LLEGO MUESTRA ':np.nan}).astype(float)
        df = df.replace('NR',np.nan)
        df['MESES'] = df['MESES'].astype(float).astype('Int16')
        df['EDAD'] = df['EDAD MESES (1= (0-12); 2= (13-36); 3= (37-72); 4= (73-108); 5= (>109); 0= NI']
        df['SEXO'] = df['SEXO'].replace({'H ':'H',
                                        'M ':'M'})
    return df

def module_selection(data,module,prueba):
  """
  Selector de modulo de los datos. Entrega DataFrame.
  1. Info Básica.
  2. Actitudes con enfermos o asintomáticos con COVID-19
  3. Prácticas sobre COVID-19.
  4. Percepción sobre la pandemia.				
  5. Situación laboral y social.				
  6. Conocimiento sobre COVID-19.				
  """
  if prueba=='Serologia':

        if module=='Info Básica':
            return data.loc[:,'COD':'EN CASO DE HABER TOMADO MEDICAMENTOS CUÁLES TOMÓ?']
        elif module=='Actitudes':
            return data.loc[:,'ALGUIEN EN LA FAMILIA O USTED A SIDO REPORTADO COMO ENFERMO DE COVID-19?':'USAN MASCARILLAS O CARETAS DENTRO DE LA VIVIENDA']
        elif module=='Prácticas':
            return data.loc[:,'DURANTE LA PANDEMIA ME HE QUEDADO EN CASA':'OTRO CUAL?']
        elif module=='Percepción':
            return data.loc[:,'YO CREO QUE?':'ME HABRIA AISLADO VOLUNTARIAMENTE']
        elif module=='Situación':
            return data.loc[:,'PERDÍ MI TRABAJO':'1 CAMBIÉ TENGO MÁS INGRESOS']
        elif module=='Conocimiento':
            return data.loc[:,'¿LA COVID -19 ES?':'DISTANCIAMIENTO SOCIAL']
        else:
            return data.loc[:,'CÓDIGO':]
  else:
        if module=='Info Básica':
            return data.loc[:,:'DIARREA']
        elif module=='Actitudes':
            return data.loc[:,'LA PERSONA CON COVID ESTUVO AISLADA DE LOS DEMAS?':'USAN MASCARILLAS O CARETAS DENTRO DE LA VIVIENDA']
        elif module=='Prácticas':
            return data.loc[:,'DURANTE LA PANDEMIA ME HE QUEDADO EN CASA':'OTRO CUAL?']
        elif module=='Percepción':
            return data.loc[:,'YO CREO QUE?':'ME HABRIA AISLADO VOLUNTARIAMENTE']
        elif module=='Situación':
            return data.loc[:,'PERDÍ MI TRABAJO':'HE CAMBIADO DE ACTIVIDAD LABORAL?']
        elif module=='Conocimiento':
            return data.loc[:,'¿LA COVID -19 ES?':'DISTANCIAMIENTO SOCIAL']
        else:
            return data.loc[:,'COD':]

    
def apilado(datos,target,agrupacion, title, y_title, barmode='stack',porcentaje=False):
    """
    Esta función recibe un set de datos DataFrame, 
    el tipo de Prueba PCR o Serologia, y la variable 
    sobre la que se desean agrupar los datos.
    Retorna un grafico de barras apilado.
    """
    #mapear los datos a numero
    # datos[agrupacion]=datos[agrupacion].astype(int)
    datos[target] = datos[target].replace({'POSITIVO':1,
                                            'NEGATIVO':0})
    #print(datos[prueba].value_counts())
    #agrupación
    total = datos[[target,agrupacion]].groupby(agrupacion).count()
    positivos = datos[[target,agrupacion]].loc[datos[target]==1].groupby(agrupacion).count()
    negativos = datos[[target,agrupacion]].loc[datos[target]==0].groupby(agrupacion).count()

    if porcentaje: #Las columnas deben tener el mismo nombre
        positivos = 100*positivos/total
        negativos = 100*negativos/total

    positivos.rename(columns={target:'Positivos'},inplace=True)
    negativos.rename(columns={target:'Negativos'},inplace=True)

    
    tabla = pd.concat([positivos, negativos],axis = 1)

    #Creación de la figura
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x = tabla.index,
        y = tabla['Positivos'],
        name='Positivos',
        marker_color='rgb(26, 118, 255)'
    ))
    fig.add_trace(go.Bar(
        x = tabla.index,
        y = tabla['Negativos'],
        name='Negativos',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.update_layout(
    title=title,
    xaxis_tickfont_size=14,
    yaxis=dict(
        title=y_title,
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        # x=0,
        # y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ))

    fig.update_layout(barmode=barmode)
    return fig

def auto_apilado(datos,target,agrupacion, title, y_title='Conteo (Individuos)', barmode='stack',porcentaje=False):
    """
    Esta función recibe un set de datos DataFrame, 
    una variable target, y la variable 
    sobre la que se desean agrupar los datos (eje X).
    Retorna un grafico de barras apilado.
    """
    #mapear los datos a numero
    # datos[agrupacion]=datos[agrupacion].astype(int)

    # datos[target] = datos[target].replace({'POSITIVO':1,
    #                                         'NEGATIVO':0})
    
    #print(datos[prueba].value_counts())
    #agrupación
    
    total = datos[[target,agrupacion]].groupby(agrupacion).count()
    tabla = pd.DataFrame([])
    fig = go.Figure()
    #Creamos una traza 
    for value in datos[target].unique():
        trace = datos[[target,agrupacion]].loc[datos[target]==value].groupby(agrupacion).count()
    
        if porcentaje: #Las columnas deben tener el mismo nombre
            trace = 100*trace/total
            y_title ='Porcentaje (Individuos)'
            
        trace.rename(columns={target:str(value)},inplace=True)

        tabla = pd.concat([tabla, trace],axis = 1)

        #Creación de la figura
        
        fig.add_trace(go.Bar(
            x = tabla.index,
            y = tabla[str(value)],
            name=str(value),
            # marker_color='rgb(26, 118, 255)'
        ))
  
    fig.update_layout(
    title=title,
    xaxis_tickfont_size=14,
    yaxis=dict(
        title=y_title,
        titlefont_size=16,
        tickfont_size=14,
    ),
    )

    fig.update_layout(barmode=barmode)
    return fig
                                
def donut_plot(bats,bw):
    """
    bw: string con nombre de la columna.
    Recibe un Dataframe y la columna bw,
    agrupa los datos respecto a bw, hace el conteo
    y grafica una donut.
    """
    bats = bats[['Conteo',bw]].groupby(bw).sum().sort_values(by='Conteo',ascending=False)

    labels = bats.index
    values = bats['Conteo']

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=.5
        )]
    )
    fig.update_layout(
        title={
            'text': "Conteo por "+str(bw),
            'y':0.95,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    return fig

def radial_plot(df,prueba):
    """
    Recibe un dataframe con datos de los síntomas de los pacientes
    y grafica un gráfico radial donde cada linea correspone al 
    promedio de sintomas por cada municipio.

    prueba: pcr, sero.
    """
    if prueba=='sero':
        data = module_selection(df,'Info Básica','Serologia').copy(deep=True) #Info básica
        #data = df.copy(deep=True)
        data.loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'] = data.loc[:,'HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES':'DIARREA'].replace({2:0,3:np.nan}) #Cambio según la convención 0: No, 1 Sí
        #Seleccionamos sólo personas con síntomas:
        data = data.loc[data['HA ESTADO ENFERMO A HA TENIDO SÍNTOMAS LOS ÚLTIMOS TRES MESES']!=0].dropna() #los nan bajan el promedio
        #La siguiente parte da problemas sin el filtro de Info basica:
        data = data.groupby('MUNICIPIO').mean() #Agrupamos el promedio de cada síntoma por municipio
        #Radial plot
        data = data.loc[:,'FIEBRE Ó ESCALOFRIOS':'DIARREA']
    else:
        data = df.copy(deep=True)
        data.loc[:,'FIEBRE Ó ESCALOFRIOS':'DIARREA'] = data.loc[:,'FIEBRE Ó ESCALOFRIOS':'DIARREA'].replace({2:0,3:np.nan}) #Cambio según la convención 0: No, 1 Sí
        #Seleccionamos sólo personas con síntomas:
        data = data.loc[data['RESULTADO PCR']!=0].dropna() #los nan bajan el promedio
        data = data.groupby('MUNICIPIO').mean() #Agrupamos el promedio de cada síntoma por municipio
        #Radial plot
        data = data.loc[:,'FIEBRE Ó ESCALOFRIOS':'DIARREA']

    # data = data.reset_index()


    categories = ['FIEBRE Ó ESCALOFRIOS','TOS','DIFICULTAD PARA RESPIRAR','FATIGA','DOLORES MUSCULARES Y CORPORALES',
                'DOLOR DE CABEZA','PERDIDAD DEL OLFATO O DEL GUSTO','DOLOR DE GARGANTA',
                'CONGESTION DE LA NARIZ','NÁUSEAS O VÓMITOS','DIARREA']

    fig = go.Figure()
    for i in range(len(data)):

        fig.add_trace(go.Scatterpolar(
            r=data.iloc[i],
            theta=categories,
            name=str(data.index[i])
        ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )

    fig.update_layout(
        title={
            'text': "Sintomas por Municipio",
            'y':0.95,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'}

    )
    return fig


def mun_to_coord(full_ser):
    """
    Recibe un Dataframe con municipios,
     añade sus coordenadas
    y regresa un Dataframe.
    """
    full_ser['lat']=0
    full_ser['lon']=0

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Montería'] = 8.7558921
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Montería'] = -75.887029

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Lorica'] = 9.2394583
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Lorica'] = -75.8139786

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = 8.4076739 
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Planeta Rica'] = -75.5840456 

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Tierralta'] = 8.1717342
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Tierralta'] = -76.059376

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Sahagun'] = 8.9472964
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Sahagun'] = -75.4434972

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Montelibano'] = 7.9800534
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Montelibano'] = -75.4167198

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='Cereté'] = 8.8852282
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='Cereté'] = -75.7922421

    full_ser['lat'].loc[full_ser['MUNICIPIO']=='San Antero'] = 9.373016
    full_ser['lon'].loc[full_ser['MUNICIPIO']=='San Antero'] = -75.7595056

    return full_ser

def table_prueba(pat_df,prueba):
    """
    Genera la tabla necesaria para el mapa
    Prueba: string Tipo de prueba, Serologia o PCR, son sets de datos distintos
    Entrega una tabla agrupada por municipio con conteo de pruebas y
    No de Positivos
    """
    df = pat_df.copy(deep=True)
    df = df[['lat','lon','MUNICIPIO']].groupby('MUNICIPIO').max()

    if prueba=='PCR':

        df = df.merge(pat_df[['RESULTADO PCR','MUNICIPIO']].loc[pat_df['RESULTADO PCR']==1].groupby(['MUNICIPIO']).count() ,how='outer',on='MUNICIPIO')
        df = df.merge(pat_df[['RESULTADO PCR','MUNICIPIO']].groupby(['MUNICIPIO']).count() ,how='inner',on='MUNICIPIO')

        df = df.rename(columns={'RESULTADO PCR_x':'POSITIVOS PCR',
                                'RESULTADO PCR_y':'No DE PRUEBAS PCR'})
        df = df.reset_index()
    else:
        df = df.merge(pat_df[['RESULTADO SEROLOGIA','MUNICIPIO']].loc[pat_df['RESULTADO SEROLOGIA']==1].groupby(['MUNICIPIO']).count() ,how='outer',on='MUNICIPIO')
        df = df.merge(pat_df[['RESULTADO SEROLOGIA','MUNICIPIO']].groupby(['MUNICIPIO']).count() ,how='inner',on='MUNICIPIO')

        df['VULNERABILIDAD (%)'] = round(100*(1-(df['RESULTADO SEROLOGIA_x']/df['RESULTADO SEROLOGIA_y'])))
        df = df.rename(columns={'RESULTADO SEROLOGIA_x':'POSITIVOS SEROLOGIA',
                                'RESULTADO SEROLOGIA_y':'No DE PRUEBAS SEROLOGIA'})
        df = df.reset_index()
    return df

def mapping_df(full_ser,prueba,an=False):
    """
    Recibe un Dataframe con Coordenadas y lo grafica
    en un mapa. retorna un html para usar con Iframe.

    Prueba es el tipo de prueba, Serologia o PCR
    an: Booleano para verificar si corresponde a animales
    """
    df = table_prueba(full_ser, prueba)
    #Mapa:

    folium_hmap = folium.Figure(width=500, height=500)
    m = folium.Map(location=[8.3344713,-75.6666238],
                            width='100%',
                            height='100%',
                            zoom_start=8,#Por defecto es 10
                            tiles="OpenStreetMap" #OpenSteetMap ,Stamen Toner(Terrain, Watercolor)
                            ).add_to(folium_hmap)

    data = df
    if prueba=='Serologia':
        for i in range(0,len(data)):
            html = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> Serología: </p>
                    <p>Positivas: {data.iloc[i]['POSITIVOS SEROLOGIA']}</p>
                    <p> Total: {data.iloc[i]['No DE PRUEBAS SEROLOGIA']}</p>
                    """
            iframe = folium.IFrame(html=html,width=130, height=160)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup,
                radius=float(data.iloc[i]['No DE PRUEBAS SEROLOGIA'])*100,
                color='lightgray',
                fill=True,
                fill_color='gray'
            ).add_to(m)

        for i in range(0,len(data)):
            html = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> Serología: </p>
                    <p>Positivas: {data.iloc[i]['POSITIVOS SEROLOGIA']}</p>
                    <p> Total: {data.iloc[i]['No DE PRUEBAS SEROLOGIA']}</p>
                    """
            iframe = folium.IFrame(html=html,width=130, height=160)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup,
                radius=float(data.iloc[i]['POSITIVOS SEROLOGIA'])*100,
                color='cadetblue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

    else:
        for i in range(0,len(data)):
            html = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> PCR: </p>
                    <p>Positivas: {data.iloc[i]['POSITIVOS PCR']}</p>
                    <p> Total: {data.iloc[i]['No DE PRUEBAS PCR']}</p>
                    """
            iframe = folium.IFrame(html=html,width=130, height=160)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup,
                radius=float(data.iloc[i]['No DE PRUEBAS PCR'])*100,
                color='lightgray',
                fill=True,
                fill_color='lightgray'
            ).add_to(m)
        for i in range(0,len(data)): #redundante
            html = f"""
                    <head>
                        <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/dZVMbK.css">
                    <head>
                    <h6> {data.iloc[i]['MUNICIPIO']}</h6>
                    <p> PCR: </p>
                    <p>Positivas: {data.iloc[i]['POSITIVOS PCR']}</p>
                    <p> Total: {data.iloc[i]['No DE PRUEBAS PCR']}</p>
                    """
            iframe = folium.IFrame(html=html,width=130, height=160)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Circle(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=popup,
                radius=float(data.iloc[i]['POSITIVOS PCR'])*100,
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(m)
    if an ==True:
        folium_hmap.save('assets/prueba_por_municipios_Animal.html')
    else:
        folium_hmap.save('assets/prueba_por_municipios.html')

    return folium_hmap

def tabla(data1,data2,columna1,columna2,union='MUNICIPIO'):
    """
    Recibe 2 sets de datos, 2 columnas (String) y la columna
    que las une, y entrega una tabla agrupada por la unión.
    data1,data2: df de los datos a unir
    columna1,columna2: str columnas de interes
    union: str columna donde hacer la unión.
    """#Escoger entre más común, media, máximo y promedio
    df1 = data1[[columna1,union]].groupby(union).agg(lambda x:x.value_counts().index[0])
    df2 = data2[[columna2,union]].groupby(union).agg(lambda x:x.value_counts().index[0])
    df = df1.join(df2,on=df2.index)
    df = df.reset_index()
    #print(df.head()) #Porque no funciona con la misma columna?
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns)
                    # fill_color='paleturquoise',
                    # align='left'
                    ),
        cells=dict(values=[df[union], df[columna1], df[columna2]]
                # fill_color='lavender',
                # align='left'
                ))
    ])
    fig.update_layout(
        title={
            'text': "Valor más común de "+str(columna1)+" y "+str(columna2)+" por Municipio",
            'y':0.95,
            'x':0.45,
            'xanchor': 'center',
            'yanchor': 'top'}
    )

    return fig

def line_chart(datos,target,agrupacion,title='',y_title='',porcentaje=False):
    """
    Esta función recibe un set de datos DataFrame, 
    una variable target, y la variable de la fecha
    sobre la que se desean agrupar los datos (eje X).
    Retorna un grafico de barras apilado.
    """
    #agrupación
    
    total = datos[[target,agrupacion]].groupby(agrupacion).count()
    tabla = pd.DataFrame([])
    fig = go.Figure()
    #Creamos una traza 
    for value in datos[target].unique():
        trace = datos[[target,agrupacion]].loc[datos[target]==value].groupby(agrupacion).count()
    
        if porcentaje: #Las columnas deben tener el mismo nombre
            trace = 100*trace/total
            y_title ='Porcentaje (Individuos)'
            
        trace.rename(columns={target:str(value)},inplace=True)

        tabla = pd.concat([tabla, trace],axis = 1)
        tabla = tabla.sort_values(by='FECHA')
        tabla = tabla.fillna(0)
        #Creación de la figura
        print(tabla)
        fig.add_trace(go.Scatter(
            x = tabla.index,
            y = tabla[str(value)],
            mode='lines',
            name=str(value),
            # marker_color='rgb(26, 118, 255)'
        ))
  
    fig.update_layout(
    title=title,
    xaxis_tickfont_size=14,
    yaxis=dict(
        title=y_title,
        titlefont_size=16,
        tickfont_size=14,
    ),
    )

    return fig

def select(dataName):
    df =df_pcr
    if dataName=='Pacientes':
        df = df_ser
    elif dataName=='Animales Domésticos':
        df = df_ani
    elif dataName =='Calidad del Aire':
        df = df_air1
    else:
        df=df_mur
    return df

def opciones(datos,column1='Cod',to_drop=''):
    df = select(datos)
    try:
        df = df.drop(to_drop,axis=1)
    except:
        pass
    if column1!='Cod':
        df=df.drop(column1,axis=1)
   
    return [{'value':x, 'label':x[0]+x[1:].lower()} for x in df.columns]



#####################################################
# Importar los datos
#####################################################

df_ser = pd.read_csv('data/BDcomunitarioSeroprevalencia.csv')
df_pcr = pd.read_csv('data/pat_df2021GATEWAY.csv')
df_ani = pd.read_csv('data/animales_domesticos.csv')
df_mur = pd.read_csv('data/BasedeDatosMurcielagosCórdoba_Dic2020.csv')
df_air1= pd.read_csv('data/bdmp_primera.csv',delimiter=';')
df_air2= pd.read_csv('data/bdmp_segunda.csv',delimiter=';')
df_airE= pd.read_csv('data/bdmp_exteriores.csv',delimiter=';')

df_ser = pre_processing(df_ser,'sero')
df_pcr = pre_processing(df_pcr,'pcr')
df_ani = pre_processing(df_ani,'ani')
df_mur = pre_processing(df_mur,'mur')
df_air1= pre_processing(df_air1,'air1')
df_air2= pre_processing(df_air2,'air2')
df_airE= pre_processing(df_airE,'airE')


#####################################################
# layout callbacks 
#####################################################

#Grafico apilado
@app.callback(
    Output('bar_chart','figure'),
    Input('barras_edad','value'),
    Input('column','value'),#El orden en que se definen en el callback afecta a la función
    Input('porcentaje0','value')
)
def generate_bar(barras_edad,column,porcentaje0):
    if porcentaje0=='Sí':
        porcentaje0=True
    else:
        porcentaje0=False

    if barras_edad=='PCR':
        fig1 = auto_apilado(df_pcr,'RESULTADO PCR',str(column), 'Resultados de la Prueba PCR por '+str(column),porcentaje=porcentaje0)
    else:
        fig1 = auto_apilado(df_ser,'RESULTADO SEROLOGIA',str(column),  'Resultados de la Prueba Serologia por '+str(column),porcentaje=porcentaje0)

    return fig1

#Grafico radial
@app.callback(
    Output('radial_plot','figure'),
    [Input('prueba_radial','value')]
)
def generate_radial(prueba_radial):
    if prueba_radial=='PCR':
        fig2 = radial_plot(df_pcr,'pcr')
    else:
        fig2 = radial_plot(df_ser,'sero')

    return fig2

#Actividad para actualizar gráficos dependiendo de la opción
@app.callback(
    Output('map','srcDoc'),
    [Input('prueba','value')]
)
def generate_map(prueba):
    if prueba=='Serologia':
        mapping_df(mun_to_coord(df_ser),prueba)
    else:
        mapping_df(mun_to_coord(df_pcr),prueba)
    return open('assets/prueba_por_municipios.html','r').read()

#Donut chart:
@app.callback(
    Output('donut_chart','figure'),
    [Input('variables','value')]
)
def generate_donut(variables):
    fig3 = donut_plot(df_mur,str(variables))
    return fig3

#Categories chart:
@app.callback(
    Output('cat_chart','figure'),
    Input('columna','value'),
    Input('campaña','value')
)
def generate_airbar(columna,campaña):
    df = df_air1
    if campaña =='1':
        df = df_air1
    elif campaña=='2':
        df = df_air2
    else:
        df = df_airE
    
    fig4 = apilado(df,'PCR',str(columna), '', 'Conteo')

    return fig4

#Categories chart:
@app.callback(
    Output('corr_plot','src'),
    Input('campaña1','value')
)
def generate_corrplot(campaña1):
    if campaña1 =='1':
        path = '/assets/coor1.png'
    elif campaña1 =='2':
        path = '/assets/corr2.png'
    else:
        path = '/assets/corrE.jpg'

    return path

#options FUNCIONAAA!!! :D
@app.callback(
    Output('column','options'),
    Input('barras_edad','value'),
    Input('module','value')
)
def desplegar_opciones(barras_edad,module):
    df =df_pcr
    if barras_edad=='PCR':
        df = df_pcr
        df = module_selection(df,module,'PCR')

    else:
        df = df_ser
        df = module_selection(df,module,'Serologia')

    return [{'value':x, 'label':x[0]+x[1:].lower()} for x in df.columns]
    
@app.callback(
    Output('animalbar_chart','figure'),
    Input('columnA','value')
)
def generate_animalbar(columnA):
    df = df_ani
       
    fig5 = apilado(df,'RESULTADO PCR',str(columnA), '', 'Conteo')

    return fig5

##############################################################
#------------------PlayGround--------------------------------#
##############################################################

@app.callback(
    Output('column1','options'),
    Input('datos1','value'),
)
def desplegar_opciones1(datos):
    return opciones(datos)

@app.callback(
    Output('column2','options'),
    Input('datos1','value'),
    Input('column1','value')
)
def desplegar_opciones2(datos,column1):
    return opciones(datos,column1)

@app.callback(
    Output('play_bar','figure'),
    Input('datos1','value'),
    Input('column1','value'),
    Input('column2','value'),#El orden en que se definen en el callback afecta a la función
)
def generate_play_bar(datos1,column1,column2):
    """

    """
    df = select(datos1)

    fig6 = auto_apilado(df,str(column1),str(column2), str(column1)+' agrupado por '+str(column2))
    
    return fig6

@app.callback(
    Output('columna1','options'),
    Input('data1','value')
)
def desplegar_opciones3(data1):
    return opciones(data1,to_drop='MUNICIPIO')

@app.callback(
    Output('columna2','options'),
    Input('data2','value')
)
def desplegar_opciones4(data2):
    return opciones(data2,to_drop='MUNICIPIO')

@app.callback(
    Output('play_table','figure'),
    Input('data1','value'),
    Input('data2','value'),
    Input('columna1','value'),
    Input('columna2','value')
)
def generate_table(datos1,datos2,columna1,columna2):
    df1 = select(datos1)
    df2 = select(datos2)
    
    return tabla(df1,df2,columna1,columna2)

@app.callback(
    Output('graph','figure'),
    Input('chart_type','value'),
)
def graph_returner(chart_type):
    """
    Returns the different chart types defined on top.
    """
    if chart_type=='bar':
        return auto_apilado(df_ser,'RESULTADO SEROLOGIA','EDAD',  'Resultados de la Prueba Serologia por '+'EDAD',porcentaje=False)
    elif chart_type=='donut':
        return donut_plot(df_mur,'Lugar')
    elif chart_type=='map':
        mapping_df(mun_to_coord(df_ser),'Serologia')
        return open('assets/prueba_por_municipios.html','r').read() #returns a srcDoc for Iframe to read
    elif chart_type=='corrplot':
        path = '/assets/coor1.png'
        return path #returns a path for html.img to read
    elif chart_type=='radial':
        return radial_plot(df_ser,'sero')
    elif chart_type=='table':
        return tabla(df_ser,df_air1,'AREA DEL MUNICIPIO','HOSPITAL')
    elif chart_type=='playbar': 
        return auto_apilado(df_ani,'ESPECIE','SEXO', ('Especie'+' agrupado por '+'Lugar'))
    elif chart_type=='line':
        return line_chart(df_air1,'ZONA','FECHA',title='Conteo de Zona por Fechas',y_title='Conteo (Número)')
#la diferencia con Bar es que este no es centrado en las pruebas 
# #Los comentarios luego de los ":" afectan el codigo
    
