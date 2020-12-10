import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib import cm
import math
import pandas as pd
import seaborn as sns

PRISM_DATE = datetime.datetime(2013, 6, 6)


def split_timeseries_figures(in_frames, names, split_at=PRISM_DATE, same_plot=True, **kwargs):
    """
    Takes the input data and creates a plot similar to figure 4a in the paper.
    :param dataframes: An iterable of 2 pandas data frames with the dates (dtype=PeriodIndex) as index and views as only column
    :param names: Names for the incoming data frames (neede for the legend)
    :param split_at: The date at which the data shall be split
    :param same_plot: If set false, a subplot will be created for each dataframe in in_frames. If true, they will be plotted on the same axis.
    :return: Plots the figure
    """

    # Default values that can be changed
    title = kwargs.get('title', '')
    figsize = kwargs.get('figsize', [18, 6])
    keyword = kwargs.get('keyword', 'views')
    sharey = kwargs.get('sharey', True)
    show_legend = kwargs.get('legend', True) and same_plot

    # Make sure we can iterate over the input argument to get a constant behavior, even if there is only 1df given.
    if isinstance(in_frames, pd.DataFrame):
        in_frames = [in_frames]
    if isinstance(names, str):
        names = [names]
    assert len(names) == len(in_frames), "{} dataframes but {} names specified. This should be equal".format(
        len(in_frames), len(names))
    nr_subplots = len(in_frames)
    same_plot = True if nr_subplots == 1 else same_plot  # Remove useless specification of 'separate plots' if there is only 1 df

    dfs_to_plot = []
    for in_frame in in_frames:
        # Prepare the dataframe for seaborn (https://stackoverflow.com/questions/52112979/having-xticks-to-display-months-in-a-seaborn-regplot-with-pandas)
        # Seaborn has issues handling datetimes, so for the computation they are transformed to integers before transforming them back for the labelling later on.
        # Matplotlib provides the necessary functionality.
        dataframe = in_frame.copy()
        dataframe.index = dataframe.index.to_timestamp()
        dataframe['date_ordinal'] = mdates.date2num(dataframe.index)
        dfs_to_plot.append(dataframe)

    # Some color definition for plotting and the legend
    if 'colors' in kwargs:
        colors = kwargs['colors']
    else:
        colors = {}
        cmap = cm.get_cmap(kwargs.get('cmap', 'Set1'))
        cmap_colors = cmap.colors
        for i, name in enumerate(names):
            colors[name] = cmap_colors[i % len(cmap_colors)]
    colors['Prism Disclosure, 6/6/2013'] = 'red'

    # Starting to build the actual plot
    if same_plot:
        fig, ax = plt.subplots(figsize=figsize)
        show_every_nth_month = 1  # There is enough space for every month to be displayed
    else:
        COLS = math.ceil(math.sqrt(nr_subplots))
        ROWS = math.ceil(nr_subplots / COLS)
        fig, axs = plt.subplots(ncols=COLS, nrows=ROWS, sharex=True, sharey=sharey, figsize=figsize)
        show_every_nth_month = COLS  # It gets tight if we display every month

    for i, dataframe in enumerate(dfs_to_plot):
        # First some axes unpacking. Numpy has an ugly feature of changing the depth of the list storing the axes, so lets unpack them
        if not same_plot:
            if ROWS == 1:
                ROW = 1
                COL = i
                ax = axs[COL]
            else:
                COL = i % COLS
                ROW = i // COLS
                ax = axs[ROW][COL]
        before = dataframe.loc[dataframe.index < split_at]
        after = dataframe.loc[dataframe.index >= split_at]
        sns.regplot(x='date_ordinal', y=keyword, data=before, ax=ax, color=colors[names[i]],
                    scatter_kws={'color': colors[names[i]], 's': 30},
                    line_kws={'color': colors[names[i]]})
        sns.regplot(x='date_ordinal', y=keyword, data=after, ax=ax, color=colors[names[i]],
                    scatter_kws={'color': colors[names[i]], 's': 30},
                    line_kws={'color': colors[names[i]]})
        ax.set(xlabel='', ylabel='')  # Per default, we do not really want a label on every subplot
        if not show_legend:
            ax.set_title(names[i])  # Some minimum information should be there

        # Tune the visuals
        ax.set_xlim(dataframe['date_ordinal'].min() - 15, dataframe['date_ordinal'].max() + 15)  # 15 days offset
        ax.vlines(mdates.date2num(split_at), 0, 1, color=colors['Prism Disclosure, 6/6/2013'],
                  transform=ax.get_xaxis_transform(), label=split_at)
        if not same_plot and COL == 0:
            ax.set_ylim(dataframe[keyword].min() * 0.9,
                        dataframe[keyword].max() * 1.1)  # Assumes there are no negative values
            ax.set_ylabel(keyword)
        if not same_plot and ROW + 1 == ROWS:
            # As mentioned above, the date was transformed to integers for the sake of plotting it using seaborn.
            # Now, they have to be transformed back to have nice x-Axis labels that are human-readable
            loc = mdates.MonthLocator(interval=show_every_nth_month)
            ax.xaxis.set_major_locator(loc)
            ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

    # Formatting and Optics
    fig.patch.set_facecolor('lightgrey')
    fig.suptitle(title)

    # Axis settings
    if same_plot:
        ax.set_xlabel('Month / Year')
        ax.set_ylabel(keyword)
        # As mentioned above, the date was transformed to integers for the sake of plotting it using seaborn.
        # Now, they have to be transformed back to have nice x-Axis labels that are human-readable
        loc = mdates.MonthLocator(interval=show_every_nth_month)
        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

    fig.autofmt_xdate(rotation=60)

    if show_legend:
        # Add a custom legend
        legend_patches = []
        for entry, c in colors.items():
            legend_patches.append(mpatches.Patch(color=c, label=entry))
        #  legend_patches.append(mpatches.Patch(color='lightgrey', label='95% Confidence Interval'))
        font = FontProperties()
        font.set_size('large')
        plt.legend(handles=legend_patches, title='Legend', bbox_to_anchor=(0, 0), loc='lower left', prop=font,
                   ncol=math.ceil(math.sqrt(nr_subplots)), fancybox=True, shadow=True)