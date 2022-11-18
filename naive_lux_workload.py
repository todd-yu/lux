import lux
import pandas as pd
import click
import time

lux.config.topk = False
lux.config.sampling = False


@click.command()
@click.option('--num-trials')
@click.option('--log-file-path')
@click.option('--data-file-path')
def main(num_trials, log_file_path, data_file_path):
    log_file = open(log_file_path, "a")

    for _ in range(int(num_trials)):

        df = pd.read_csv(data_file_path) # "./data/500k.csv"
        start = time.perf_counter()
        first_rec = df.recommendation

        df.expire_metadata()
        df.expire_recs()

        second_rec = df.recommendation

        end = time.perf_counter()

        log_file.write(f"{str(end - start)} \n")

    log_file.flush()
    log_file.close()




if __name__ == "__main__":
    main()
