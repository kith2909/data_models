import pandas as pd
import seaborn as sns
import matplotlib as mpl
import plotly.graph_objects as go


class data_start():

    def __init__(self):
            df_fert = pd.read_csv('/home/kith/Spiced/bergamot-encoder-student-code/weekly_milestones/week_01/data/gapminder_total_fertility.csv', index_col=0)
            df_life = pd.read_excel('/home/kith/Spiced/bergamot-encoder-student-code/weekly_milestones/week_01/data/gapminder_lifeexpectancy.xlsx', index_col=0)
            df_pop = pd.read_csv('/home/kith/Spiced/bergamot-encoder-student-code/weekly_milestones/week_01/data/population.csv', index_col=0)

            df = {
                 'fert': df_fert,
                 'life': df_life,
                 'pop': df_pop
            }
            for item in df:
                print(df[item].shape)
                print(df[item].columns)

st = data_start()