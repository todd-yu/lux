import lux
import pandas as pd
import click
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

LUX_DEFAULT_TOP_K = 15
logger = False

@click.command()
@click.option('--num-trials', required=True)
@click.option('--log-file-path', required=True)
@click.option('--data-file-path', required=True)
@click.option('--topk', is_flag=True, default=False)
@click.option('--sampling', is_flag=True, default=False)
def main(num_trials, log_file_path, data_file_path, topk, sampling):
    global logger, log_file

    click.echo(f"Beginning benchmark for {log_file_path} with params: topk={topk} sampling={sampling}")

    # lux.config.topk = LUX_DEFAULT_TOP_K if topk else False
    lux.config.early_pruning = False
    lux.config.topk = False
    lux.config.sampling = False

    log_file = open(log_file_path, "a")

    # moved inside the loop due to repeated deletes
    df = pd.read_csv(data_file_path) # "./data/500k.csv"


    for _ in tqdm(range(int(num_trials))):


        rec = df.recommendation #compute all recs

        start, end = lux.core.frame.start, lux.core.frame.end

        log_file.write(f"{str(end - start)} \n") # custom profiling for interestingness scores

        df.expire_metadata()
        df.expire_recs()

    log_file.flush()
    log_file.close()




if __name__ == "__main__":
    main()
