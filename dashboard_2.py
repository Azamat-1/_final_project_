import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from etl import get_data

df = get_data()

if df.empty:
    raise ValueError("DataFrame is empty. Please check your data source.")

if 'Occupation' not in df.columns:
    raise KeyError("Столбец 'Occupation' не найден в данных")

df = df[df['Annual_Income'] <= 1e6]
df = df[(df['Age'] > 0) & (df['Age'] <= 100)]
df = df[df['Num_Bank_Accounts'] <= 10]
df = df[df['Num_Credit_Card'] <= 10]

app = dash.Dash(__name__)

styles = {
    'body': {
        'backgroundColor': '#2c2c2c',
        'color': '#ffffff',
        'fontFamily': 'Arial, sans-serif, Roboto',
        'padding': '20px',
    },
    'container': {
        'maxWidth': '1200px',
        'fontFamily': 'Arial',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': '#2c2c2c',
        'color': '#ffffff'
    },
    'header': {
        'textAlign': 'center',
        'fontFamily': 'Arial',
        'padding': '10px 0',
        'color': '#ffffff'
    },
    'section': {
        'fontFamily': 'Arial',
        'padding': '10px 0'
    },
    'label': {
        'display': 'block',
        'fontFamily': 'Arial',
        'margin': '10px 0 5px 0',
        'color': '#ffffff'
    
    },
    'dropdown': {
        'fontFamily': 'Arial',
        'color': '#000000'
    }
}

# Добавление стиля для body
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body style="background-color: #2c2c2c; color: #ffffff;">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Макет дашборда
app.layout = html.Div(style=styles['container'], children=[
    html.H1("Дашборд клиентов", style=styles['header']),
    
    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (доход):", style=styles['label']),
        dcc.Dropdown(
            id='income-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (доход):", style=styles['label']),
        dcc.RangeSlider(
            id='income-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='income-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (возраст):", style=styles['label']),
        dcc.Dropdown(
            id='age-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (возраст):", style=styles['label']),
        dcc.RangeSlider(
            id='age-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='age-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (банковские счета):", style=styles['label']),
        dcc.Dropdown(
            id='bank-accounts-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (банковские счета):", style=styles['label']),
        dcc.RangeSlider(
            id='bank-accounts-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='bank-accounts-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (кредитные карты):", style=styles['label']),
        dcc.Dropdown(
            id='credit-cards-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (кредитные карты):", style=styles['label']),
        dcc.RangeSlider(
            id='credit-cards-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='credit-cards-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (задолженность):", style=styles['label']),
        dcc.Dropdown(
            id='debt-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (задолженность):", style=styles['label']),
        dcc.RangeSlider(
            id='debt-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='debt-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (коэффициент использования кредита):", style=styles['label']),
        dcc.Dropdown(
            id='credit-utilization-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
            value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (коэффициент использования кредита):", style=styles['label']),
        dcc.RangeSlider(
            id='credit-utilization-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='credit-utilization-graph')
    ]),

    html.Div(style=styles['section'], children=[
        html.Label("Выберите профессию (ежемесячные инвестиции):", style=styles['label']),
        dcc.Dropdown(
            id='investment-occupation-dropdown',
            options=[{'label': occ, 'value': occ} for occ in df['Occupation'].unique()],
                        value=df['Occupation'].unique()[0] if not df['Occupation'].empty else None,
            style=styles['dropdown']
        ),
        html.Label("Выберите диапазон возраста (ежемесячные инвестиции):", style=styles['label']),
        dcc.RangeSlider(
            id='investment-age-slider',
            min=0,
            max=100,
            value=[df['Age'].min(), df['Age'].max()],
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True},
            included=False,
            updatemode='drag'
        ),
        dcc.Graph(id='investment-graph')
    ])
])

# Обработчики для обновления графиков
@app.callback(
    Output('income-graph', 'figure'),
    [Input('income-occupation-dropdown', 'value'),
     Input('income-age-slider', 'value')]
)
def update_income_graph(selected_occupation, age_range):
    print(f'Updating income graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for income graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Annual_Income', title='Распределение годового дохода', color_discrete_sequence=['darkorange'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('age-graph', 'figure'),
    [Input('age-occupation-dropdown', 'value'),
     Input('age-age-slider', 'value')]
)
def update_age_graph(selected_occupation, age_range):
    print(f'Updating age graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for age graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Age', title='Распределение возраста', color_discrete_sequence=['#636efa'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('bank-accounts-graph', 'figure'),
    [Input('bank-accounts-occupation-dropdown', 'value'),
     Input('bank-accounts-age-slider', 'value')]
)
def update_bank_accounts_graph(selected_occupation, age_range):
    print(f'Updating bank accounts graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for bank accounts graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Num_Bank_Accounts', title='Распределение количества банковских счетов', color_discrete_sequence=['darkorange'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('credit-cards-graph', 'figure'),
    [Input('credit-cards-occupation-dropdown', 'value'),
     Input('credit-cards-age-slider', 'value')]
)
def update_credit_cards_graph(selected_occupation, age_range):
    print(f'Updating credit cards graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for credit cards graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Num_Credit_Card', title='Распределение количества кредитных карт', color_discrete_sequence=['#636efa'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('debt-graph', 'figure'),
    [Input('debt-occupation-dropdown', 'value'),
     Input('debt-age-slider', 'value')]
)
def update_debt_graph(selected_occupation, age_range):
    print(f'Updating debt graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for debt graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Outstanding_Debt', title='Распределение задолженности', color_discrete_sequence=['darkorange'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('credit-utilization-graph', 'figure'),
    [Input('credit-utilization-occupation-dropdown', 'value'),
     Input('credit-utilization-age-slider', 'value')]
)
def update_credit_utilization_graph(selected_occupation, age_range):
    print(f'Updating credit utilization graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for credit utilization graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Credit_Utilization_Ratio', title='Распределение коэффициента использования кредита', color_discrete_sequence=['#636efa'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

@app.callback(
    Output('investment-graph', 'figure'),
    [Input('investment-occupation-dropdown', 'value'),
     Input('investment-age-slider', 'value')]
)
def update_investment_graph(selected_occupation, age_range):
    print(f'Updating investment graph with: Occupation={selected_occupation}, Age Range={age_range}')
    if selected_occupation is None:
        return px.histogram(title='Нет данных')
    
    filtered_df = df[(df['Occupation'] == selected_occupation) &
                     (df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    print(f'Filtered DataFrame for investment graph:\n{filtered_df.head()}')
    
    if filtered_df.empty:
        return px.histogram(title='Нет данных')
    
    fig = px.histogram(filtered_df, x='Amount_invested_monthly', title='Распределение ежемесячных инвестиций', color_discrete_sequence=['darkorange'])
    fig.update_layout(
        plot_bgcolor='#2c2c2c',
        paper_bgcolor='#2c2c2c',
        font=dict(
            size=14,
            color='#ffffff'
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
