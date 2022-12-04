import lux
import pandas as pd
import click
import time
from tqdm import tqdm
import warnings
from lux.vis.VisList import VisList
from lux.vis.Vis import Vis
from lux.executor.PandasExecutor import set_log_file
warnings.filterwarnings("ignore")

LUX_DEFAULT_TOP_K = 15

def numeric_type(col, df):
    dt = df.dtypes[col]
    return dt == "int64" or dt == "float64"

class Spec:
    def __init__(self, *args):
        self.attrs = list(args)
    
def gen_viz(specs, df):
    vizs = []
    for spec in specs:
        vizs.append(Vis(spec.attrs, None))
    return VisList(vizs, df)

def gen_all_geo_specs(df):
    # TODO: Support country cols
    assert "state" in df
    specs = []
    for col in df.columns:
        if col == "state" or not numeric_type(col, df):
            continue
        specs.append(Spec("state", col))
    return specs

def gen_all_bar_specs(df):
    specs = []
    x_cols = []
    y_cols = []
    for col in df.columns:
        # TODO: Ignore country cols
        if df.dtypes[col] == "object" and col != "state":
            x_cols.append(col)
        elif numeric_type(col, df):
            y_cols.append(col)
    for x in x_cols:
        for y in y_cols:
            specs.append(Spec(x, y))
    return specs

def gen_all_2d_count_specs(df):
    # Heatmaps with counts
    specs = []
    x_cols = []
    y_cols = []
    for col in df.columns:
        # TODO: Ignore country cols
        if numeric_type(col, df):
            x_cols.append(col)
            y_cols.append(col)
    for x in x_cols:
        for y in y_cols:
            if x != y:
                specs.append(Spec(x, y))
    return specs

def gen_all_1d_count_specs(df):
    # Bar graphs with count
    specs = []
    x_cols = []
    for col in df.columns:
      if df.dtypes[col] == "object":
        x_cols.append(col)
    for x in x_cols:
        specs.append(Spec(x))
    return specs

def gen_all_histogram_specs(df):
    # Heatmaps with counts
    specs = []
    x_cols = []
    for col in df.columns:
        if numeric_type(col, df):
            x_cols.append(col)
    for x in x_cols:
        specs.append(Spec(x))
    return specs

@click.command()
@click.option('--num-trials', required=True)
@click.option('--log-file-path', required=True)
@click.option('--data-file-path', required=True)
@click.option('--data-file-path', required=True)
@click.option('--topk', is_flag=True, default=False)
@click.option('--sampling', is_flag=True, default=False)
def main(num_trials, log_file_path, data_file_path, topk, sampling):

    click.echo(f"Beginning benchmark for {log_file_path} with params: topk={topk} sampling={sampling}")

    lux.config.topk = LUX_DEFAULT_TOP_K if topk else False
    lux.config.sampling = sampling
    lux.config.early_pruning = False

    log_file = open(log_file_path, "a")
    set_log_file(log_file)

    for _ in tqdm(range(int(num_trials))):

        # moved inside the loop due to repeated deletes
        df = pd.read_csv(data_file_path) # "./data/500k.csv"

        log_file.write(f"Heatmap: ")
        gen_viz(gen_all_2d_count_specs(df), df)

        log_file.write(f"Bar+Geo: ")
        gen_viz(gen_all_bar_specs(df) + gen_all_geo_specs(df), df)

        df.expire_metadata()
        df.expire_recs()

    log_file.flush()
    log_file.close()




if __name__ == "__main__":
    main()