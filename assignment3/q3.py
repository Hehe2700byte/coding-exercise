import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def read_population_data(filename: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Reads population CSV data, extracts specific mid-year columns,
    and returns a cleaned DataFrame along with a list of available years.
    """
    df = pd.read_csv(filename, nrows=6, usecols=[2, 4, 6, 8])
    years = df.loc[3]
    column_headings = ['Sex', 'Age'] + list(years)
    df = pd.read_csv(filename, skiprows=[0, 1, 2, 3, 4, 5, 93], nrows=172,
                     usecols=[0, 1, 2, 4, 6, 8])  # Use mid-year columns only
    df.columns = column_headings
    return df, list(years)


def transform_data(pdf: pd.DataFrame, year: str, k: int = 5) -> pd.DataFrame:
    """
    Processes raw population data into a combined format for plotting, grouping
    ages by 'k' rows and splitting values into 'Male' and 'Female' columns.
    """
    # Helper functions
    def filter_by_sex(df: pd.DataFrame, sex: str) -> pd.DataFrame:
        return df.loc[df['Sex'] == sex]

    def select_age_year(df: pd.DataFrame) -> pd.DataFrame:
        return df.loc[:, ['Age', year]]

    def group_by_age(df: pd.DataFrame) -> pd.DataFrame:
        def concat_first_last(group: pd.Series) -> str:
            if len(group) == 1:
                return group.iloc[0]
            return group.iloc[[0, -1]].str.cat(sep='-')
        grouped = df.groupby(df.index // k)  # group by every k rows
        return grouped.agg({'Age': concat_first_last, year: "sum"})

    def rename_year(df: pd.DataFrame, sex: str) -> pd.DataFrame:
        return df.rename(columns={year: sex})
    
    def process_gender(sex: str):
        df = filter_by_sex(pdf, sex)
        df = select_age_year(df)
        df = df.reset_index(drop = True)
        df = group_by_age(df)
        return rename_year(df, sex)
    
    grouped_male, grouped_female = list(map(process_gender, ['Male', 'Female']))
    grouped_female = grouped_female.drop(columns=['Age'])
    return pd.concat([grouped_male, grouped_female], axis=1)

def population_pyramid(pdf: pd.DataFrame, city: str, year: str, k: int = 5,
                       w: int = 6, h: int = 4) -> Figure:
    """
    Creates a Matplotlib Figure showing a population pyramid, using horizontal
    bars to compare male and female demographics for a specific year.
    """
    df = transform_data(pdf, year, k)
    fig, ax = plt.subplots(figsize = (w, h))
    ax.barh(df['Age'], df['Female'], color = '#ee7a87', label = 'Female')
    ax.barh(df['Age'], df['Male'], left = -df['Male'], color = '#4682b4', label = 'Male')
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f'{int(abs(x)/1000)}K')
    )

    ax.set_title(f"{city} Population Pyramid for Year {year}")
    ax.set_xlabel("population")
    ax.set_ylabel("age")
    ax.legend()

    fig.tight_layout()
    return fig

# Sample client
if __name__ == "__main__":
    try:
        hkpdf, years = read_population_data("q3_data.csv")
        print("Raw data:", hkpdf, "List of years:", years, sep="\n")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    # Plot the default population pyramid for each year
    for year in years:
        pop_fig = population_pyramid(hkpdf, "Hong Kong", year, w=7, h=5)
        pop_fig.savefig(f"hk_{year}_pyramid_k5.png")

    # Plot using other intervals for the age groups
    year = '2025'
    for k in [10, 15, 20]:
        print(f"Year {year} Demographics Grouped by {k} Years:")
        print(transform_data(hkpdf, year, k))
        pop_fig = population_pyramid(hkpdf, "Hong Kong", year, k=k)
        pop_fig.savefig(f"hk_{year}_pyramid_k{k}.png")
