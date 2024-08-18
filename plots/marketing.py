import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import update_hover_layout
from constants import MONTHS


def event_seq_pie(data):
    fig = px.pie(data, names='Event Sequence', values='AOV',
                 labels="percent+label", hole=0.3,
                 color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072", "#f9f7f3",
                                          "teal", "silver", "#f2cc8f", "#81b29a"],
                 title='Average Order Value (AOV) by Event Sequence')
    fig = update_hover_layout(fig)
    fig.update_layout(legend_title="Event Sequence", height=500)
    return fig


def event_seq_funnel(data):
    total_visitors = len(data)
    event_sequence_steps = [1, 2, 3, 4, 5, 6, 7]
    conversion_rates = []
    previous_count = total_visitors
    for step in event_sequence_steps:
        current_count = len(data[data['Event Sequence'] == step])
        conversion_rate = (current_count / previous_count) * 100
        conversion_rates.append(conversion_rate)
        previous_count = current_count
    fig = go.Figure(go.Funnel(
        y=event_sequence_steps,
        x=conversion_rates,
        textinfo="value+percent initial",
        marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver", "#f2cc8f", "#81b29a"]},
    ))
    fig.update_layout(title="Event Sequence Conversion Funnel",
                      xaxis_title="Conversion Rate (%)",
                      yaxis_title="Event Sequence Step",
                      showlegend=False, height=500)
    return fig


def channel_funnel(df1, df2):
    total_spend = df1.groupby('Channel')['Media Spend'].sum()
    total_conversions = df2[df2['Is Target'] == 1].groupby('Channel')['Is Target'].count()
    percent_spend = (total_spend / total_spend.sum()) * 100
    percent_conversion = (total_conversions / total_conversions.sum()) * 100

    funnel_data = pd.DataFrame({'Channel': total_spend.index, 'Percent Spend': percent_spend,
                                'Percent Conversion': percent_conversion})
    funnel_data = funnel_data.sort_values(by='Percent Spend', ascending=False)
    fig = px.funnel(funnel_data, x='Percent Spend', y='Channel',
                    title=' Spend and Conversion by Channel', )
    fig.update_traces(textinfo='percent total')
    fig.update_traces(marker=dict(color='#006d77'))
    return fig


def channels_performance(data):
    channel_conversion_rates = data[data['Is Target'] == 1].groupby(
        'Channel'
    )['Is Target'].count()
    top_channel = channel_conversion_rates.idxmax()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=channel_conversion_rates.index, y=channel_conversion_rates))
    highlight_color = ['#264653' if channel == top_channel else '#2a9d8f' for channel in channel_conversion_rates.index]
    fig.update_layout(title="Channel Performance",
                      xaxis_title="Channel",
                      yaxis_title="Conversion Count",
                      showlegend=False,
                      xaxis_tickangle=-45,
                      bargap=0.1,
                      xaxis={'categoryorder': 'total descending'},
                      )
    fig.update_traces(marker=dict(color=highlight_color))
    fig = update_hover_layout(fig)
    return fig


def aov_by_channels(data):
    fig = px.pie(data, names='Channel', values='AOV',
                 labels="percent+label", hole=0.3,
                 color_discrete_sequence=["#0fa3b1", "#b5e2fa", "#eddea4", "#f7a072",
                                          "teal", "silver", "#f2cc8f", "#81b29a"],
                 title='Average Order Value (AOV) by Channel')
    fig = update_hover_layout(fig)
    return fig
