import lux
import pandas as pd
import click
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

LUX_DEFAULT_TOP_K = 15


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

    log_file = open(log_file_path, "a")
    df = pd.read_csv(data_file_path) # "./data/500k.csv"

    for _ in tqdm(range(int(num_trials))):

        start = time.perf_counter()
        first_rec = df.recommendation

        df.expire_metadata()
        df.expire_recs()

        second_rec = df.recommendation

        end = time.perf_counter()

        log_file.write(f"{str(end - start)} \n")

        df.expire_metadata()
        df.expire_recs()

    log_file.flush()
    log_file.close()




if __name__ == "__main__":
    main()
