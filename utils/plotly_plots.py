import datetime
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import seaborn as sns
import statsmodels.formula.api as smf

def analyse_and_plot(dataset='wikipedia', lang=None, ignore_months=range(54, 61), split=None, layout=None, seperate_y=False, start_at=None, end_at=None, outliers=None):
    
    # Read both csv files
    if dataset == 'wikipedia':
        df_terrorism = pd.read_csv(f'data/wikipedia/terrorism_views.csv')
        df_domestic = pd.read_csv(f'data/wikipedia/domestic_views.csv')
        yax = 'views'
    elif dataset in ['google', 'google-trends']:
        df_terrorism = pd.read_csv(f'data/google-trends/terrorism_en.csv')
        df_domestic = pd.read_csv(f'data/google-trends/domestic_en.csv')
        yax = 'max_ratio'
    else:
        raise ValueError("Unknown dataset")
    
    # Group them
    df = pd.concat([df_terrorism, df_domestic])
    
    # Create a mapping from article name to study group
    group = {}
    for article in df_terrorism.article.unique():
        group[article] = 'terrorism'
    for article in df_domestic.article.unique():
        group[article] = 'domestic'
    
    if lang is not None:
        # Keep only articles in this language
        df = df.loc[df.language == lang]
    
    if outliers is not None:
        if lang is None:
            for language, out_list in outliers.items():
                for out in out_list:
                    df = df.drop(df.loc[(df.language == language) & (df.article == out)].index)
        else:
            if lang in outliers:
                for out in outliers[lang]:
                    df = df.drop(df.loc[df.article == out].index)
    
    if start_at is not None:
        df = df.loc[pd.to_datetime(df.date) >= start_at]
    if end_at is not None:
        df = df.loc[pd.to_datetime(df.date) <= end_at]
    
    # We extract the month, year, time (number of months elapsed since the beginning of the period)
    df['month'] = pd.DatetimeIndex(df.date).month
    df['year'] = pd.DatetimeIndex(df.date).year
    df['time'] = (df.year - df.year.min()) * 12 + df.month
    if split is None:
        split = (2013 - df.year.min()) * 12 + 7 - df.loc[df.year == df.year.min()].month.min()
    
    # Get the total number of views for each article for each month
    monthly_views = df.groupby(['article', 'time'])[yax].sum().reset_index()\
                                  .pivot_table(index='article', columns='time', values=yax)
    
    # Retrieve the monthly pageviews for each article group
    terrorism_views = monthly_views.loc[monthly_views.index.map(lambda art: group[art] == 'terrorism')]
    domestic_views = monthly_views.loc[monthly_views.index.map(lambda art: group[art] == 'domestic')]
    
    # DataFrame to apply the ITS analysis to
    its = pd.DataFrame()

    # Monthly number of views aggregated over all terrorism articles
    its['t_views'] = terrorism_views.sum()
    # Monthly number of views aggregated over all terrorism articles
    its['d_views'] = domestic_views.sum()

    # Indicator of whether the NSA revelations have already happened
    its['NSA'] = (its.index.to_series() >= split).astype(int)
    # We just do this to be able to use the column 'month' in the regression
    its['month'] = its.index
    its = its.drop(index=split)
    
    ignore_months = [m for m in ignore_months if m<= max(its['month'])]
    
    # Fitting the ITS regressions
    terrorism_regr = smf.ols(formula='t_views ~ month * NSA', data=its.drop(index=ignore_months)).fit()
    domestic_regr = smf.ols(formula='d_views ~ month * NSA', data=its.drop(index=ignore_months)).fit()
    
    # Retrieve the ITS predictions and confidence intervals
    its['t_pred'] = terrorism_regr.predict(its)
    its[['t_low', 't_high']] = terrorism_regr.get_prediction(its).summary_frame(alpha=0.05).iloc[:, 2:4].values
    its['d_pred'] = domestic_regr.predict(its)
    its[['d_low', 'd_high']] = domestic_regr.get_prediction(its).summary_frame(alpha=0.05).iloc[:, 2:4].values    
    
    ## Plotting
    if seperate_y:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    else:
        fig = go.Figure()
    hovertemplate = '<b>Views</b>: %{y:.2f}' + '<br>Month: %{x}<br>'

    # Plot the regression confidence intervals
    x = its.loc[:split-1, 't_pred'].index
    fig.add_trace(go.Scatter(x=x.append(x[::-1]), y=its.loc[:split-1, 't_high'].append(its.loc[:split-1, 't_low'][::-1]),
                             fill='toself', fillcolor='rgba(64,144,248,0.15)', mode='none',
                             name='95% Confidence Interval for the Terrorism Trend'))
    x = its.loc[split:, 't_pred'].index
    fig.add_trace(go.Scatter(x=x.append(x[::-1]), y=its.loc[split+1:, 't_high'].append(its.loc[split:, 't_low'][::-1]),
                             fill='toself', fillcolor='rgba(64,144,248,0.15)', mode='none',
                             name='95% Confidence Interval for the Terrorism Trend', showlegend=False))
    x = its.loc[:split-1, 'd_pred'].index
    dom_fill_before = go.Scatter(x=x.append(x[::-1]), y=its.loc[:split-1, 'd_high'].append(its.loc[:split-1, 'd_low'][::-1]), 
                                 fill='toself', fillcolor='rgba(255,130,0,0.15)', mode='none',
                                 name='95% Confidence Interval for the Comparator Trend')
    x = its.loc[split:, 'd_pred'].index
    dom_fill_after = go.Scatter(x=x.append(x[::-1]), y=its.loc[split+1:, 'd_high'].append(its.loc[split:, 'd_low'][::-1]), 
                                fill='toself', fillcolor='rgba(255,130,0,0.15)', mode='none', 
                                name='95% Confidence Interval for the Comparator Trend', showlegend=False)
    if seperate_y:
        fig.add_trace(dom_fill_before, secondary_y=True)
        fig.add_trace(dom_fill_after, secondary_y=True)
    else:
        fig.add_trace(dom_fill_before)
        fig.add_trace(dom_fill_after)
        
        
    # Plot the terror regression line before and after the June 2013 revelations (June 2013 excluded)
    fig.add_trace(go.Scatter(x=its.loc[:split-1, 't_pred'].index, y=its.loc[:split-1, 't_pred'], mode='lines',
                             name='Trend before NSA revelations', line={'color': 'black'}))
    fig.add_trace(go.Scatter(x=its.loc[split:, 't_pred'].index, y=its.loc[split+1:, 't_pred'], mode='lines',
                             name='Trend after NSA revelations', line={'color': 'black', 'dash': 'dash'}))

    # Plot the domestic regression line before and after the June 2013 revelations (June 2013 excluded)
    dom_reg_before = go.Scatter(x=its.loc[:split-1, 'd_pred'].index, y=its.loc[:split-1, 'd_pred'], mode='lines',
                                name='Trend before NSA revelations', line={'color': 'black'}, showlegend=False)
    dom_reg_after = go.Scatter(x=its.loc[split:, 'd_pred'].index, y=its.loc[split+1:, 'd_pred'], mode='lines',
                               name='Trend after NSA revelations', line={'color': 'black', 'dash': 'dash'}, showlegend=False)
    if seperate_y:
        fig.add_trace(dom_reg_before, secondary_y=True)
        fig.add_trace(dom_reg_after, secondary_y=True)
    else:
        fig.add_trace(dom_reg_before)
        fig.add_trace(dom_reg_after)
        
    # Plot the actual monthly pageviews as dots
    fig.add_trace(go.Scatter(x=its['t_views'].drop(index=ignore_months).index, y=its['t_views'].drop(index=ignore_months),
                             mode='markers', name='Terrorism article ' + yax, marker_color='rgba(64,144,248,1)', marker_size=8,
                             hovertemplate=hovertemplate))
    fig.add_trace(go.Scatter(x=its['t_views'].loc[ignore_months].index, y=its['t_views'].loc[ignore_months],
                             mode='markers', name='Ignored terrorism article ' + yax, marker_color='rgba(64,144,248,1)', marker_size=8,
                             marker_symbol='x', hovertemplate=hovertemplate))

    dom_scatter = go.Scatter(x=its['d_views'].drop(index=ignore_months).index, y=its['d_views'].drop(index=ignore_months),
                             mode='markers', name='Domestic article ' + yax, marker_color='rgba(255,130,0,1)', marker_size=8,
                             hovertemplate=hovertemplate)
    dom_ignore = go.Scatter(x=its['d_views'].loc[ignore_months].index, y=its['d_views'].loc[ignore_months],
                             mode='markers', name='Ignored domestic article ' + yax, marker_color='rgba(255,130,0,0.6)', marker_size=8,
                             marker_symbol='x', hovertemplate=hovertemplate)
    if seperate_y:
        fig.add_trace(dom_scatter, secondary_y=True)
        fig.add_trace(dom_ignore, secondary_y=True)
    else:
        fig.add_trace(dom_scatter)
        fig.add_trace(dom_ignore)
        
    # Show the moment of the NSA revelations
    # fig.add_shape(type="line", yref='paper', x0=split, y0=0, x1=split, y1=1, line=dict(color="Red",width=2, dash='dash'), name='PRISM revelation')
    y0 = min(min(its['t_views'].values), min(its['d_views'].values))
    y1 = max(max(its['t_views'].values), max(its['d_views'].values))
    fig.add_trace(go.Scatter(x=[split, split], y=[y0,y1], mode="lines", name="PRISM revelation", line=dict(color="Red",width=3.5, dash='dash')))

    # Set layout, title, axis labels, x ticks
    lang = f'[{lang}] ' if lang is not None else ''
    title = lang + 'Terrorism study group vs Domestic security comparator group, {}'.format(dataset)
    fig.update_layout(title=title,
                      legend=dict(yanchor="top", y=-0.2, xanchor="left", x=0, orientation='h', bgcolor='rgba(180,180,180,0.9)',bordercolor="Black", borderwidth=2))
    fig.update_xaxes(range=[0, its.month.max() + 1], nticks=40, ticks="inside", showgrid=False, showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    if seperate_y:
        fig.update_yaxes(nticks=10, ticks="inside", showline=True, linewidth=2, linecolor='rgba(64,144,248,1)', secondary_y=False)
        fig.update_yaxes(nticks=10, ticks="inside", showline=True, linewidth=2, linecolor='rgba(255,130,0,1)', secondary_y=True)
    else:
        fig.update_yaxes(nticks=10, ticks="inside", showline=True, linewidth=2, linecolor='black', mirror=True)
        
    
    if layout is not None:
        fig.update_layout(layout)
        if seperate_y:
            text = layout.get('yaxis_title', '')
            fig.update_yaxes(title_text=text + ', <b>Terrorism</b>', secondary_y=False)
            fig.update_yaxes(title_text=text + ', <b>Domestic</b>', secondary_y=True)
    
    return (terrorism_regr, domestic_regr), fig
    
def four_panel_pageviews_plot(data, ignore=None):
    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, shared_yaxes=True, horizontal_spacing = 0.02, vertical_spacing = 0.03)
    
    articles = data.article.unique()
    n = data.shape[0]
    data_rows = len(articles)
    m = data_rows // 4
    
    if ignore is None:
        ignore = []
    
    for i, art in enumerate(articles):
        if art in ignore:
            continue
        subplot_nr = 1 + i // m
        row = 1 if (subplot_nr <= 2) else 2
        col = 1 if (subplot_nr in [1, 3]) else 2
        art_data = data.loc[data.article == art]
        scatter = go.Scatter(x=art_data.time, y=art_data.views, name=art)
        fig.add_trace(scatter, row=row, col=col)
    
    fig.update_layout(margin={'l': 20, 'r': 20, 'b': 10, 't': 10})
    fig.show('png', width=1000, height=700)
    
    
def four_panel_google_plot(data, ignore=None):
    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, shared_yaxes=True, horizontal_spacing = 0.02, vertical_spacing = 0.03)
    
    articles = data.article.unique()
    n = data.shape[0]
    data_rows = len(articles)
    m = data_rows // 4
    
    if ignore is None:
        ignore = []
    
    for i, art in enumerate(articles):
        if art in ignore:
            continue
        subplot_nr = 1 + i // m
        row = 1 if (subplot_nr <= 2) else 2
        col = 1 if (subplot_nr in [1, 3]) else 2
        art_data = data.loc[data.article == art]
        scatter = go.Scatter(x=list(range(len(art_data))), y=art_data.max_ratio, name=art)
        fig.add_trace(scatter, row=row, col=col)
    
    fig.update_layout(margin={'l': 20, 'r': 20, 'b': 10, 't': 10}, width=2000, height=1200)
    fig.show('png', width=1000, height=700)

