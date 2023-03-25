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
@click.option('--data-file-path', required=True)
@click.option('--topk', is_flag=True, default=False)
@click.option('--sampling', is_flag=True, default=False)
@click.option('--num-ops', default = 100)
def main(num_trials, log_file_path, data_file_path, topk, sampling, num_ops):
    global logger, log_file

    click.echo(f"Beginning benchmark for {log_file_path} with params: topk={topk} sampling={sampling}")

    lux.config.topk = 200
    # lux.config.early_pruning = False
    # lux.config.sampling = sampling

    log_file = open(log_file_path, "a")

    # moved inside the loop due to repeated deletes
    df = pd.read_csv(data_file_path) # "./data/500k.csv"

    df_copy = df.sample(n=min(num_ops * 2, len(df)), ignore_index=True)


    for _ in tqdm(range(int(num_trials))):

        df = pd.read_csv(data_file_path) # "./data/500k.csv"

        first_rec = df.recommendation

        start = time.perf_counter()

        # ===== begin all ops here =====
        
        for i in range(num_ops):
            df.delete_row(i)

        for i in range(num_ops):
            df.add_row(df_copy.iloc[i])

        # ===== end all ops =====

        second_rec = df.recommendation #compute non-incremental scores

        end = time.perf_counter()

        log_file.write(f"{str(end - start)} \n")

        df.expire_metadata()
        df.expire_recs()

    log_file.flush()
    log_file.close()




if __name__ == "__main__":
    main()
