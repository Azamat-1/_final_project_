import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from etl import get_data

# Настройка ширины страницы (в процентах)
PAGE_WIDTH = 68

# Функция для генерации CSS стилей
def generate_css(page_width):
    return f'''
        body {{
            width: {page_width}%;
            margin: 0 auto;
            font-family: Arial;
        }}
        .dash-graph {{
            width: 100%;
        }}
    '''

# Загрузка данных
df = get_data()

# Проверка наличия данных
if df.empty:
    raise ValueError("DataFrame is empty. Please check your data source.")

# Проверка наличия столбца 'Occupation'
if 'Occupation' not in df.columns:
    raise KeyError("Столбец 'Occupation' не найден в данных")

# Преобразование 'Credit_History_Age' в числовой формат
def convert_credit_history_age(value):
    if isinstance(value, str):
        parts = value.split()
        if len(parts) >= 2:
            return float(parts[0])
    return pd.to_numeric(value, errors='coerce')

df['Credit_History_Age'] = df['Credit_History_Age'].apply(convert_credit_history_age)

# Фильтрация данных для исключения экстремальных значений и возрастной группы
df = df[df['Annual_Income'] <= 1e6]
df = df[(df['Age'] >= 14) & (df['Age'] <= 100)]
df = df[df['Num_Bank_Accounts'] <= 10]
df = df[df['Num_Credit_Card'] <= 10]
df = df[df['Credit_History_Age'] <= 60]  # Предполагаем, что кредитная история не может быть больше 60 лет

# Убедимся, что все используемые столбцы имеют числовой тип данных
numeric_columns = [
    'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card', 
    'Interest_Rate', 'Num_Credit_Inquiries', 'Credit_History_Age', 'Outstanding_Debt'
]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Создание приложения Dash
app = dash.Dash(__name__)

# Добавление CSS стилей
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            {generate_css(PAGE_WIDTH)}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# Макет дашборда
app.layout = html.Div([
    html.H1("Дашборд клиентов", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Выберите профессию:"),
        dcc.Dropdown(
            id='occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None
        ),
    ], style={'margin': '10px 0'}),
    
    html.Div([
        html.Label("Выберите диапазон возраста:"),
        dcc.RangeSlider(
            id='age-slider',
            min=df['Age'].min(),
            max=df['Age'].max(),
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(int(df['Age'].min()), int(df['Age'].max())+1, 10)}
        ),
    ], style={'margin': '20px 0'}),
    
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Годовой доход', value='tab-1'),
        dcc.Tab(label='Возраст', value='tab-2'),
        dcc.Tab(label='Количество банковских счетов', value='tab-3'),
        dcc.Tab(label='Количество кредитных карт', value='tab-4'),
        dcc.Tab(label='Процентная ставка', value='tab-5'),
        dcc.Tab(label='Количество кредитных запросов', value='tab-6'),
        dcc.Tab(label='Кредитная история', value='tab-7'),
        dcc.Tab(label='Задолженность', value='tab-8'),
        dcc.Tab(label='Параллельные координаты', value='tab-9')
    ]),
    
    html.Div(id='tabs-content'),
    
    html.Div(id='debug-info', style={'margin': '20px 0'})
])

# Функция обратного вызова для обновления содержимого вкладок
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs-example', 'value'),
     Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def render_content(tab, selected_occupation, age_range):
    filtered_df = df[(df['Occupation'] == selected_occupation) & 
                     (df['Age'] >= age_range[0]) & 
                     (df['Age'] <= age_range[1])]
    
    if filtered_df.empty:
        return html.Div("Нет данных для выбранных параметров")
    
    if tab == 'tab-1':
        fig = px.histogram(filtered_df, x='Annual_Income', title='Годовой доход')
    elif tab == 'tab-2':
        fig = px.histogram(filtered_df, x='Age', title='Возраст')
    elif tab == 'tab-3':
        fig = px.histogram(filtered_df, x='Num_Bank_Accounts', title='Количество банковских счетов')
    elif tab == 'tab-4':
        fig = px.histogram(filtered_df, x='Num_Credit_Card', title='Количество кредитных карт')
    elif tab == 'tab-5':
        fig = px.histogram(filtered_df[filtered_df['Interest_Rate'] <= 50], x='Interest_Rate', title='Процентная ставка')
    elif tab == 'tab-6':
        fig = px.histogram(filtered_df[filtered_df['Num_Credit_Inquiries'] <= 20], x='Num_Credit_Inquiries', title='Количество кредитных запросов')
    elif tab == 'tab-7':
        fig = px.histogram(filtered_df, x='Credit_History_Age', title='Распределение кредитной истории',
                           labels={'Credit_History_Age': 'Длительность кредитной истории (лет)'})
    elif tab == 'tab-8':
        fig = px.histogram(filtered_df, x='Outstanding_Debt', title='Задолженность')
    elif tab == 'tab-9':
        fig = px.parallel_coordinates(filtered_df, dimensions=numeric_columns, title='Параллельные координаты')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )
    
    return dcc.Graph(figure=fig)

# Добавление отладочной информации
@app.callback(
    Output('debug-info', 'children'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_debug_info(selected_occupation, age_range):
    filtered_df = df[(df['Occupation'] == selected_occupation) & 
                     (df['Age'] >= age_range[0]) & 
                     (df['Age'] <= age_range[1])]
    return f"Количество записей после фильтрации: {len(filtered_df)}"

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)