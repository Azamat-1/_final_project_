import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from etl import get_data

# Загрузка данных
df = get_data()

# Проверка наличия данных
if df.empty:
    raise ValueError("DataFrame is empty. Please check your data source.")

# Проверка наличия столбца 'Occupation'
if 'Occupation' not in df.columns:
    raise KeyError("Столбец 'Occupation' не найден в данных")

# Фильтрация данных для исключения экстремальных значений и возрастной группы
df = df[df['Annual_Income'] <= 1e6]
df = df[(df['Age'] >= 14) & (df['Age'] <= 100)]
df = df[df['Num_Bank_Accounts'] <= 10]
df = df[df['Num_Credit_Card'] <= 10]

# Убедимся, что все используемые столбцы имеют числовой тип данных
numeric_columns = [
    'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card', 
    'Interest_Rate', 'Num_Credit_Inquiries', 'Outstanding_Debt'
]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Преобразование 'Credit_History_Age' в числовой формат
if df['Credit_History_Age'].dtype == 'object':
    df['Credit_History_Age'] = df['Credit_History_Age'].apply(lambda x: float(x.split()[0]) if isinstance(x, str) else x)
df['Credit_History_Age'] = pd.to_numeric(df['Credit_History_Age'], errors='coerce')

# Создание приложения Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Стиль для контейнеров с шириной 50%
container_style = {
    'width': '50%',
    'margin': '0 auto',
    'padding': '10px'
}

# Макет дашборда
app.layout = html.Div([
    html.H1("Дашборд клиентов", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.Label("Выберите профессию:"),
            dcc.Dropdown(
                id='occupation-dropdown',
                options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
                value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None
            ),
        ], style=container_style),
        
        html.Div([
            html.Label("Выберите диапазон возраста:"),
            dcc.RangeSlider(
                id='age-slider',
                min=df['Age'].min(),
                max=df['Age'].max(),
                value=[df['Age'].min(), df['Age'].max()],
                marks={i: str(i) for i in range(int(df['Age'].min()), int(df['Age'].max())+1, 5)}
            ),
        ], style=container_style),
    ]),
    
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Годовой доход', value='tab-1'),
        dcc.Tab(label='Возраст', value='tab-2'),
        dcc.Tab(label='Количество банковских счетов', value='tab-3'),
        dcc.Tab(label='Количество кредитных карт', value='tab-4'),
        dcc.Tab(label='Процентная ставка', value='tab-5'),
        dcc.Tab(label='Количество кредитных запросов', value='tab-6'),
        dcc.Tab(label='Кредитная история', value='tab-7'),
        dcc.Tab(label='Задолженность', value='tab-8'),
        dcc.Tab(label='Средние значения параметров', value='tab-9')
    ], style=container_style),
    
    html.Div(id='tabs-content', style=container_style),
    
    html.Div([
        html.Label("Выберите параметры для полярной диаграммы:"),
        dcc.Dropdown(
            id='radar-parameters',
            options=[{'label': col, 'value': col} for col in numeric_columns + ['Credit_History_Age']],
            value=numeric_columns + ['Credit_History_Age'],
            multi=True
        ),
        dcc.Graph(id='radar-chart')
    ], id='radar-chart-container', style=dict(container_style, **{'display': 'none'})),
    
    html.Div(id='debug-info', style=container_style)
])

@app.callback(
    [Output('tabs-content', 'children'),
     Output('radar-chart-container', 'style')],
    [Input('tabs-example', 'value'),
     Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def render_content(tab, selected_occupation, age_range):
    filtered_df = df[(df['Occupation'] == selected_occupation) & 
                     (df['Age'] >= age_range[0]) & 
                     (df['Age'] <= age_range[1])]
    
    if filtered_df.empty:
        return html.Div("Нет данных для выбранных параметров"), {'display': 'none'}
    
    if tab == 'tab-9':
        return html.Div(), dict(container_style, **{'display': 'block'})
    
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
        filtered_df = filtered_df[filtered_df['Credit_History_Age'] <= 100]
        bins = np.linspace(0, filtered_df['Credit_History_Age'].max(), 20)
        fig = px.histogram(filtered_df, x='Credit_History_Age', nbins=20,
                           title='Распределение кредитной истории',
                           labels={'Credit_History_Age': 'Длительность кредитной истории (лет)',
                                   'count': 'Количество клиентов'},
                           color_discrete_sequence=['skyblue'])
        fig.update_layout(
            xaxis_title="Длительность кредитной истории (лет)",
            yaxis_title="Количество клиентов",
            bargap=0.1
        )
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5)
    elif tab == 'tab-8':
        fig = px.histogram(filtered_df, x='Outstanding_Debt', title='Задолженность')

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )
    return dcc.Graph(figure=fig), {'display': 'none'}

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('radar-parameters', 'value'),
     Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_radar_chart(selected_parameters, selected_occupation, age_range):
    filtered_df = df[(df['Occupation'] == selected_occupation) & 
                     (df['Age'] >= age_range[0]) & 
                     (df['Age'] <= age_range[1])]
    
    radar_fig = go.Figure()

    if not filtered_df.empty and selected_parameters:
        # Нормализация данных
        normalized_df = filtered_df[selected_parameters].copy()
        for col in selected_parameters:
            normalized_df[col] = (filtered_df[col] - filtered_df[col].min()) / (filtered_df[col].max() - filtered_df[col].min())
        
        avg_values = normalized_df.mean()
        
        radar_fig.add_trace(go.Scatterpolar(
            r=avg_values.values,
            theta=selected_parameters,
            fill='toself',
            line=dict(color='royalblue', width=2),
            text=[f"{v:.2f}" for v in avg_values.values],  # Добавляем текстовые метки
            textposition="middle center",  # Располагаем метки в центре каждого сегмента
            textfont=dict(size=10, color="black"),  # Настройки шрифта для меток
            mode='lines+markers+text'  # Добавляем режим отображения текста
        ))

    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],  # Фиксированный диапазон для нормализованных данных
                showticklabels=True,  # Показываем метки значений
                tickformat=".2f",  # Формат отображения чисел
                gridcolor='lightgrey',
                linewidth=1
            ),
            angularaxis=dict(
                linewidth=1,
                gridcolor='lightgrey'
            ),
            bgcolor='white'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='black', size=12),
        showlegend=False,
        title="Средние нормализованные значения параметров",
        title_font=dict(size=20)
    )

    # Добавляем подписи значений вне диаграммы
    for i, param in enumerate(selected_parameters):
        angle = (i / len(selected_parameters)) * 2 * np.pi
        x = 1.3 * np.cos(angle)
        y = 1.3 * np.sin(angle)
        
        original_value = filtered_df[param].mean()
        radar_fig.add_annotation(
            x=x, y=y,
            text=f"{param}<br>{original_value:.2f}",
            showarrow=False,
            font=dict(size=10),
            align='center'
        )

    return radar_fig

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