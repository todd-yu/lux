# ======= incremental_optimized workloads, no existing optimizations =======

# incremental_optim, 50k
python3 optimized_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs/incremental_mqo_naive_workload_50k.txt" --data-file-path "./data/AB_NYC_2019.csv"

# incremental_optim, 250k
python3 optimized_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs/incremental_mqo_naive_workload_250k.txt" --data-file-path "./data/250k.csv"

# incremental_optim, 500k
python3 optimized_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs/incremental_mqo_naive_workload_500k.txt" --data-file-path "./data/500k.csv"

# incremental_optim, 1m
python3 optimized_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs/incremental_mqo_naive_workload_1m.txt" --data-file-path "./data/1m.csv"

# incremental_optim, 5m
python3 optimized_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs/incremental_mqo_naive_workload_5m.txt" --data-file-path "./data/5m.csv"
