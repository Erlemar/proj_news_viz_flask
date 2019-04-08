import pandas as pd
import json
import altair as alt
import pickle


class DataManager(object):

    def __init__(self):
        self.data = pd.read_csv('src/rubrics.csv')
        with open('src/topics_dict.json', 'r') as f:
            self.topics_dict = json.load(f)
        with open('src/rubrics_dict.json', 'r') as f:
            self.rubrics_dict = json.load(f)

    def get_initial_data(self):
        plot_df = self.data.loc[self.data['Rubric'] == 'bivs-SSR']
        chart = self.make_ridge_chart(plot_df)


        return {'rubrics_dict': self.rubrics_dict,
                'topics_dict': self.topics_dict,
                'chart': chart.to_json()}

    def change_plot(self, request):

        plot_type = request.values['plot_type']
        rubric = request.values['rubric']
        topics = request.form.getlist('topics[]')

        plot_df = self.data.loc[self.data['Rubric'] == rubric]

        if 'All' in topics:
            pass
        else:
            plot_df = plot_df.loc[plot_df['Topic'].isin(topics)]

        if plot_type == 'ridge':
            chart = self.make_ridge_chart(plot_df)

        elif plot_type == 'bump':
            chart = self.make_bump_chart(plot_df)

        with open(f'src/{rubric}.pickle', 'rb') as f:
            rubric_topics = pickle.load(f)
        # rubric_topics = pd.DataFrame(rubric_topics)

        if 'All' in topics:
            rubric_topics = {k: list(v) for k, v in rubric_topics.items()}
        else:
            rubric_topics = {k: list(v) for k, v in rubric_topics.items() if k in topics}

        return {'chart': chart.to_json()}


    def make_bump_chart(self, data):
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