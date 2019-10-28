import pandas as pd
import json
import altair.vegalite.v3 as alt
import pickle


class DataManager(object):
    """
    Class for getting and managing data for flask app.
    Also creates altair visualizations.

    """

    def __init__(self):
        """
        Load all the data.

        """
        self.data = pd.read_csv('src/rubrics.csv')
        self.add_data_names = ['All']
        self.plot_type = 'ridge'
        with open('src/topics_dict.json', 'r') as f:
            self.topics_dict = json.load(f)
        with open('src/rubrics_dict.json', 'r') as f:
            self.rubrics_dict = json.load(f)
        with open('src/rubric_topic_words.json', 'r') as f:
            self.rubric_topic_words = json.load(f)

    def get_initial_data(self):
        """
        For making default visualization and showing data.
        Rubric was chosen at random.
        Rubrics_dict - dictionary with mapping of technical rubric names and
        names for showing on site.
        Topics_dict - dictionary with topics and their words (from topic modelling).
        Rubric_topics - topics of the current rubric.

        :return:
        """
        plot_df = self.data.loc[self.data['Rubric'] == 'bivs-SSR']
        self.plot_df = plot_df
        self.rubric_df = plot_df.copy()
        chart = self.make_plot()

        rubric_topics = self.rubric_topic_words['bivs-SSR']
        self.rubric_topics = rubric_topics
        topics_dict = {v: v for v in rubric_topics.keys()}

        return {'rubrics_dict': self.rubrics_dict,
                'topics_dict': topics_dict,
                'chart': chart.to_json(),
                'rubric_topics': rubric_topics}

    def make_plot(self):

        if self.plot_type == 'ridge':
            chart = self.make_ridge_chart()

        elif self.plot_type == 'bump':
            chart = self.make_bump_chart()

        return chart

    def change_plot_type(self, request):
        """
        Change only plot type.

        :param request:
        :return:
        """

        plot_type = request.values['plot_type']
        self.plot_type = plot_type

        chart = self.make_plot()

        return {'chart': chart.to_json()}

    def change_plot_add(self, request):
        """
        Add additional data to the plot.

        :param request:
        :return:
        """

        add_data_names = request.form.getlist('add_data[]')
        self.add_data_names = add_data_names

        chart = self.make_plot()

        return {'chart': chart.to_json()}

    def change_plot_topic(self, request):
        """
        Change plot and table based on the selected topics.

        :param request:
        :return:
        """

        topics = request.form.getlist('topics[]')

        if 'All' in topics or len(topics) == 0:
            self.plot_df = self.rubric_df.copy()
        else:
            self.plot_df = self.rubric_df.loc[self.rubric_df['Topic'].isin(topics)]

        rubric_topics = {k: v for k, v in self.rubric_topics.items() if k in topics}

        chart = self.make_plot()


        return {'chart': chart.to_json(), 'rubric_topics': rubric_topics}

    def change_plot_rubric(self, request):
        """
        Change plot and table based on the selected rubric.

        :param request:
        :return:
        """

        rubric = request.values['rubric']
        topics = request.form.getlist('topics[]')
        self.plot_df = self.data.loc[self.data['Rubric'] == rubric]
        self.rubric_df = self.plot_df.copy()

        rubric_topics = self.rubric_topic_words[rubric]
        self.rubric_topics = rubric_topics

        topics_dict = {v: v for v in rubric_topics.keys()}

        chart = self.make_plot()


        return {'chart': chart.to_json(), 'rubric_topics': rubric_topics, 'topics_dict': topics_dict}


    def make_bump_chart(self):
        self.plot_df['year'] = pd.to_datetime(self.plot_df['year'].astype(str) + '-01-01')
        brush = alt.selection(type='interval', encodings=['x'])
        a = alt.Chart(self.plot_df)\
            .mark_line(point=True, interpolate='monotone').encode(
                x='year:T',
                y='rank:Q',
                color=alt.Color('Topic:N', sort='descending'),
                tooltip=['year:T', 'rank:Q', 'Topic:N', 'rate']
            ).properties(
                height=400,
                width=800
            ).transform_filter(
                brush
            ).interactive()


        b = alt.Chart(self.plot_df).mark_area().encode(
            y='sum(rate):Q',
            x='year:T',
        ).properties(
            width=800,
            height=100
        ).add_selection(
            brush
        )

        if self.add_data_names != ['All']:
            add_charts = [self.make_add_data_chart(i, brush) for i in self.add_data_names]
            chart = alt.vconcat(
                a, *add_charts, b, padding=0, spacing=0
            ).configure_view(
                stroke=None
            ).configure_axis(
                grid=False
            )
            return chart
        else:
            chart = alt.vconcat(
                a, b, padding=0, spacing=0
            ).configure_view(
                stroke=None
            ).configure_axis(
                grid=False
            )
            return chart

    def make_add_data_chart(self, data_name, brush):

        data = pd.read_csv(f'src/add_data_cleaned/{data_name}.csv', encoding='utf-8')
        col_name = data.columns[-1]
        chart = alt.Chart(data).mark_line(interpolate='monotone').encode(
            y=f'{col_name}:Q',
            x='year:T',
        ).properties(
            width=800,
            height=100,
			title=f'График {col_name}'
        ).transform_filter(
            brush
        )

        return chart

    def make_ridge_chart(self):
        self.plot_df['year'] = pd.to_datetime(self.plot_df['year'].astype(str) + '-01-01')
        brush = alt.selection_interval(encodings=['x'])
        step = 18
        overlap = 7
        # Topic selection
        selection = alt.selection_multi(fields=['Topic'])

        # смена цвета на выборе темы -- всё что не выделили делается серым
        color = alt.condition(selection,
                              alt.Color('Topic:N', legend=None,
                            scale=alt.Scale(scheme="rainbow")),
                             alt.value('lightgray'))

        a = alt.hconcat(alt.Chart(self.plot_df).mark_area(
                fillOpacity=0.6, interpolate='monotone').encode(
            x=alt.X('year:T'),
            y=alt.Y('rate:Q', scale=alt.Scale(range=[0, -overlap * (step + 1)]), axis=None),
            row=alt.Row('Topic:N', header=alt.Header(title=None,
                labelPadding=0, labelFontSize=0)),
            color=color
        ).add_selection(selection).properties(
            width=800,
            height=step,
            bounds='flush',
        ).transform_filter(
            brush
        ),
        alt.Chart(self.plot_df, height=500).mark_point().encode(
        y=alt.Y('Topic:N', axis=alt.Axis(orient='right')),
            color=color).add_selection(selection))

        b = alt.Chart(self.plot_df).mark_area(interpolate='monotone').encode(
            y='sum(rate):Q',
            x='year:T',
        ).properties(
            width=800,
            height=100
        ).add_selection(
            brush
        )

        if self.add_data_names != ['All']:
            add_charts = [self.make_add_data_chart(i, brush) for i in self.add_data_names]
            chart = alt.vconcat(
                a, *add_charts, b, padding=0, spacing=0
            ).configure_view(
                stroke=None
            ).configure_axis(
                grid=False
            )
            return chart
        else:
            chart = alt.vconcat(
                a, b, padding=0, spacing=0
            ).configure_view(
                stroke=None
            ).configure_axis(
                grid=False
            )
            return chart
