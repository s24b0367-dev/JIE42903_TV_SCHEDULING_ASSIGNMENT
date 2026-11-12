import pandas as pd
import streamlit as st
from ga import load_ratings, genetic_algorithm

st.set_page_config(page_title='TV Scheduling | Genetic Algorithm', page_icon='📺', layout='wide')
st.title('📺 TV Scheduling Using a Genetic Algorithm')
st.caption('JIE42903 Evolutionary Computing • 18 hourly slots • Program repeats permitted')
st.info('Assignment ambiguity: mutation default is written as 0.2, but the required range is 0.01–0.05. This app uses 0.02 within the stated range. Confirm with your lecturer.')

hours, ratings = load_ratings('program_ratings_modified.csv')
with st.expander('Modified ratings dataset and assumptions'):
    st.write('Three illustrative assumptions were applied: higher morning news demand, higher evening soccer demand, and higher late-night boxing demand. All other ratings are unchanged.')
    st.dataframe(pd.DataFrame(ratings, index=[f'{h:02d}:00' for h in hours]).T, use_container_width=True)

st.sidebar.header('Algorithm settings')
generations = st.sidebar.number_input('Generations', min_value=10, max_value=1000, value=100, step=10)
population_size = st.sidebar.number_input('Population size', min_value=10, max_value=500, value=50, step=10)
seed = st.sidebar.number_input('Random seed (shared across trials)', min_value=0, value=42)
st.sidebar.caption('For a fair comparison, all trials use the same dataset, population, generations and random seed.')

st.subheader('Trial parameters')
def trial_controls(label, co, mut):
    with st.container(border=True):
        st.markdown(f'**{label}**')
        c1, c2 = st.columns(2)
        crossover = c1.slider('CO_R (crossover rate)', min_value=0.0, max_value=0.95, value=co, step=0.05, key=f'{label}_co')
        mutation = c2.slider('MUT_R (mutation rate)', min_value=0.01, max_value=0.05, value=mut, step=0.01, key=f'{label}_mut')
    return crossover, mutation

configs = [trial_controls('Trial 1', 0.40, 0.01),
           trial_controls('Trial 2', 0.80, 0.02),
           trial_controls('Trial 3', 0.95, 0.05)]

if st.button('Run all three trials', type='primary', use_container_width=True):
    summaries = []
    curves = {}
    for i, (co, mut) in enumerate(configs, start=1):
        schedule, score, history = genetic_algorithm(
            ratings, crossover_rate=co, mutation_rate=mut,
            generations=int(generations), population_size=int(population_size), seed=int(seed))
        summaries.append({'Trial': f'Trial {i}', 'CO_R': co, 'MUT_R': mut, 'Total fitness': round(score, 4)})
        curves[f'Trial {i}'] = history
        with st.expander(f'Trial {i}: CO_R={co:.2f}, MUT_R={mut:.2f} • Fitness={score:.3f}', expanded=i == 1):
            table = pd.DataFrame({'Time slot': [f'{h:02d}:00–{h+1:02d}:00' for h in hours],
                                  'Scheduled program': schedule,
                                  'Expected rating': [ratings[p][j] for j, p in enumerate(schedule)]})
            st.dataframe(table, use_container_width=True, hide_index=True)
            st.download_button(f'Download Trial {i} schedule', table.to_csv(index=False),
                               file_name=f'trial_{i}_schedule.csv', mime='text/csv', key=f'dl{i}')
    st.subheader('Comparison of three trials')
    summary = pd.DataFrame(summaries)
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.bar_chart(summary.set_index('Trial')['Total fitness'])
    st.subheader('Best fitness by generation')
    st.line_chart(pd.DataFrame(curves).rename_axis('Generation'))
    winner = summary.loc[summary['Total fitness'].idxmax()]
    st.success(f"Highest fitness in these runs: {winner['Trial']} (CO_R={winner['CO_R']:.2f}, MUT_R={winner['MUT_R']:.2f}, fitness={winner['Total fitness']:.3f}).")
    st.caption('A single run per configuration does not establish statistical superiority. Repeat using multiple random seeds for stronger conclusions.')
    st.download_button('Download trial comparison', summary.to_csv(index=False), 'trial_comparison.csv', 'text/csv')
else:
    st.write('Choose the trial parameters above, then click **Run all three trials**.')
