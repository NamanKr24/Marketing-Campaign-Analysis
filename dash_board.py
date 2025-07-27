import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import data_loader

df = data_loader.load_bank_data('bank_data.csv')
if df is not None:
    df['y_numeric'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f9f9f9',
        'padding': '40px'
    },
    children=[
        html.H1(
            '📊 Bank Marketing Campaign Analysis',
            style={
                'textAlign': 'center',
                'color': '#222',
                'marginBottom': '10px'
            }
        ),

        html.Hr(style={'border': '1px solid #ccc'}),

        html.Div(
            'Explore customer demographics and campaign outcomes.',
            style={
                'textAlign': 'center',
                'color': '#555',
                'fontSize': '16px',
                'marginBottom': '40px'
            }
        ),

        html.Div([
            html.Label('Select a Category to Analyze:', style={
                'fontWeight': '600',
                'fontSize': '16px',
                'marginBottom': '10px',
                'display': 'block',
                'textAlign': 'center'
            }),
            dcc.Dropdown(
                id='category-dropdown',
                options=[
                    {'label': 'Job Role', 'value': 'job'},
                    {'label': 'Marital Status', 'value': 'marital'},
                    {'label': 'Education Level', 'value': 'education'},
                    {'label': 'Contact Method', 'value': 'contact'},
                    {'label': 'Previous Outcome', 'value': 'poutcome'}
                ],
                value='job',
                clearable=False,
                style={
                    'width': '300px',
                    'margin': '0 auto'
                }
            )
        ], style={'marginBottom': '40px'}),

        html.Div([
            html.Div(
                dcc.Graph(id='pie-chart'),
                style={'width': '48%', 'paddingRight': '1%'}
            ),
            html.Div(
                dcc.Graph(id='bar-chart'),
                style={'width': '48%', 'paddingLeft': '1%'}
            )
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center'
        })
    ]
)

@app.callback(
    [Output('pie-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('category-dropdown', 'value')]
)

def update_graphs(selected_category):
    
    pie_fig = px.pie(
        df, 
        names=selected_category, 
        title=f'Client Distribution by {selected_category.capitalize()}',
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    # pie_fig.update_traces(
    #     textinfo='percent+label',
    #     textfont_size=12,
    #     pull=0.02,
    #     marker=dict(line=dict(color='white', width=1))
    # )
    
    pie_fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        showlegend=True,
        legend_title_text=selected_category.capitalize(),
        legend=dict(
            orientation="v",
            x=1.05,
            y=0.95,
            font=dict(size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    pie_fig.show()
    
    rate_df = df.groupby(selected_category)['y_numeric'].mean().reset_index()
    rate_df['subscription_rate_%'] = rate_df['y_numeric'] * 100

    bar_fig = px.bar(
        rate_df, 
        x=selected_category, 
        y='subscription_rate_%', 
        title=f'Subscription Rate by {selected_category.capitalize()}',
        # text=rate_df['subscription_rate_%'].apply(lambda x: f'{x:.1f}%'),
        color='subscription_rate_%',
        color_continuous_scale='viridis'
    )
    
    bar_fig.update_traces(
        textposition='outside',
        marker_line_color='black',
        marker_line_width=0.5
    )
    
    bar_fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        yaxis_title="Subscription Rate (%)",
        xaxis_title=selected_category.capitalize(),
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickangle=45
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        font=dict(size=12),
        coloraxis_showscale=False
    )
    
    bar_fig.show()

    return pie_fig, bar_fig

if __name__ == '__main__':
    app.run(debug=True)