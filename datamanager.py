import pandas as pd
import json
import altair.vegalite.v3 as alt
import pickle


class DataManager(object):

    def __init__(self):
        self.data = pd.read_csv('src/rubrics.csv')
        with open('src/topics_dict.json', 'r') as f:
            self.topics_dict = json.load(f)
        with open('src/rubrics_dict.json', 'r') as f:
            self.rubrics_dict = json.load(f)
        with open('src/rubric_topic_words.json', 'r') as f:
            self.rubric_topic_words = json.load(f)

    def get_initial_data(self):
        plot_df = self.data.loc[self.data['Rubric'] == 'bivs-SSR']
        chart = self.make_cool_ridge_chart(plot_df, ['All'])

        rubric_topics = self.rubric_topic_words['bivs-SSR']
        topics_dict = {v: v for v in rubric_topics.keys()}

        return {'rubrics_dict': self.rubrics_dict,
                'topics_dict': topics_dict,
                'chart': chart.to_json(),
                'rubric_topics': rubric_topics}

    def change_plot(self, request):

        plot_type = request.values['plot_type']
        rubric = request.values['rubric']
        topics = request.form.getlist('topics[]')
        add_data_names = request.form.getlist('add_data[]')


        plot_df = self.data.loc[self.data['Rubric'] == rubric]
        if 'All' in topics or len(topics) == 0:
            pass
        else:
            plot_df = plot_df.loc[plot_df['Topic'].isin(topics)]

        if plot_type == 'ridge':
            chart = self.make_cool_ridge_chart(plot_df, add_data_names)

        elif plot_type == 'bump':
            chart = self.make_bump_chart(plot_df, add_data_names)

        # with open(f'src/{rubric}.pickle', 'rb') as f:
        #     rubric_topics = pickle.load(f)
        # rubric_topics = pd.DataFrame(rubric_topics)
        rubric_topics = self.rubric_topic_words[rubric]
        # print('rubric_topics', rubric_topics)
        print('topics', topics)
        topics_dict = {v: v for v in rubric_topics.keys()}
        if 'All' in topics or len(topics) == 0:
            rubric_topics = rubric_topics
        else:
            rubric_topics = {k: v for k, v in rubric_topics.items() if k in topics}
        # print(rubric_topics)

        return {'chart': chart.to_json(), 'rubric_topics': rubric_topics, 'topics_dict': topics_dict}


    def make_bump_chart_old(self, data):
        chart = alt.Chart(data).mark_line(point=True, interpolate='monotone').encode(
                x='year:O',
                y='rank:Q',
                color=alt.Color('Topic:N', sort='descending'),
                tooltip=['year:O', 'rank:Q', 'Topic:N', 'rate']
            ).properties(
                height=400,
                width=800
            ).interactive()
        return chart


    def make_bump_chart(self, data, add_data_names):
        data['year'] = pd.to_datetime(data['year'].astype(str) + '-01-01')
        brush = alt.selection(type='interval', encodings=['x'])
        a = alt.Chart(data).mark_line(point=True, interpolate='monotone').encode(
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


        b = alt.Chart(data).mark_area().encode(
            y='sum(rate):Q',
            x='year:T',
        ).properties(
            width=800,
            height=100
        ).add_selection(
            brush
        )

        if add_data_names != ['All']:
            add_charts = [self.make_add_data_chart(i, brush) for i in add_data_names]
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
        chart = alt.Chart(data).mark_line().encode(
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

    def make_ridge_chart(self, data):
        chart = alt.Chart(data).mark_area().encode(
                x='year:Q',
                y='rate:Q',
                color='Topic:N',
                tooltip=['Topic:N'],
                row=alt.Row('Topic:N')
            ).properties(
                height=30,
                width=600
            ).interactive()
        return chart

    def make_cool_ridge_chart(self, data, add_data_names):
        data['year'] = pd.to_datetime(data['year'].astype(str) + '-01-01')
        brush = alt.selection(type='interval', encodings=['x'])
        step = 18
        overlap = 4
        a = alt.Chart(data).mark_area(stroke='black', strokeWidth=0, fillOpacity=0.6).encode(
            x=alt.X('year:T'),
            y=alt.Y('rate:Q', scale=alt.Scale(range=[0, -overlap * (step + 1)]), axis=None),
            row=alt.Row('Topic:N', header=alt.Header(title=None, labelPadding=0, labelFontSize=0)),
            color='Topic:N'
        ).properties(
            width=800,
            height=step,
            bounds='flush',
        ).transform_filter(
            brush
        )
        b = alt.Chart(data).mark_area().encode(
            y='sum(rate):Q',
            x='year:T',
        ).properties(
            width=800,
            height=100
        ).add_selection(
            brush
        )

        if add_data_names != ['All']:
            add_charts = [self.make_add_data_chart(i, brush) for i in add_data_names]
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