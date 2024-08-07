# dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from etl import get_data

# Загрузка данных
df = get_data()

# Проверка наличия данных
if df.empty:
    raise ValueError("DataFrame is empty. Please check your data source.")

# Проверка наличия столбца 'Occupation'
if 'Occupation' not in df.columns:
    raise KeyError("Столбец 'Occupation' не найден в данных")

# Фильтрация данных для исключения экстремальных значений
df = df[df['Annual_Income'] <= 1e6]
df = df[(df['Age'] > 0) & (df['Age'] <= 100)]
df = df[df['Num_Bank_Accounts'] <= 10]
df = df[df['Num_Credit_Card'] <= 10]

# Создание приложения Dash
app = dash.Dash(__name__)

# Макет дашборда
app.layout = html.Div([
    html.H1("Дашборд клиентов"),
    
    html.Div([
        html.Label("Выберите профессию:"),
        dcc.Dropdown(
            id='occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        html.Label("Выберите диапазон возраста:"),
        dcc.RangeSlider(
            id='age-slider',
            min=df['Age'].min(),
            max=df['Age'].max(),
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(df['Age'].min(), df['Age'].max()+1, 5)}
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Годовой доход:"),
        dcc.Graph(id='income-graph')
    ]),
    
    html.Div([
        html.Label("Возраст:"),
        dcc.Graph(id='age-graph')
    ]),

    html.Div([
        html.Label("Количество банковских счетов:"),
        dcc.Graph(id='bank-accounts-graph')
    ]),

    html.Div([
        html.Label("Количество кредитных карт:"),
        dcc.Graph(id='credit-cards-graph')
    ]),

    html.Div([
        html.Label("Задолженность:"),
        dcc.Graph(id='debt-graph')
    ]),

    html.Div([
        html.Label("Коэффициент использования кредита:"),
        dcc.Graph(id='credit-utilization-graph')
    ]),

    html.Div([
        html.Label("Ежемесячные инвестиции:"),
        dcc.Graph(id='investment-graph')
    ])
])

# Обработчик для обновления графика дохода
@app.callback(
    Output('income-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_income_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Annual_Income', title='Распределение годового дохода')
    return fig

# Обработчик для обновления графика возраста
@app.callback(
    Output('age-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_age_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Age', title='Распределение возраста')
    return fig

# Обработчик для обновления графика числа банковских счетов
@app.callback(
    Output('bank-accounts-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_bank_accounts_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Num_Bank_Accounts', title='Распределение количества банковских счетов')
    return fig

# Обработчик для обновления графика числа кредитных карт
@app.callback(
    Output('credit-cards-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_credit_cards_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Num_Credit_Card', title='Распределение количества кредитных карт')
    return fig

# Обработчик для обновления графика задолженности
@app.callback(
    Output('debt-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_debt_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Outstanding_Debt', title='Распределение задолженности')
    return fig

# Обработчик для обновления графика коэффициента использования кредита
@app.callback(
    Output('credit-utilization-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_credit_utilization_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Credit_Utilization_Ratio', title='Распределение коэффициента использования кредита')
    return fig

# Обработчик для обновления графика суммы ежемесячных инвестиций
@app.callback(
    Output('investment-graph', 'figure'),
    [Input('occupation-dropdown', 'value'),
     Input('age-slider', 'value')]
)
def update_investment_graph(selected_occupation, age_range):
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    fig = px.histogram(filtered_df, x='Amount_invested_monthly', title='Распределение ежемесячных инвестиций')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
