# ======= Naive Lux workloads, no optimizations =======

# # no optimizations, 50k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_50k.txt" --data-file-path "./data/AB_NYC_2019.csv"

# # no optimizations, 250k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_250k.txt" --data-file-path "./data/250k.csv"

# # no optimizations, 500k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_500k.txt" --data-file-path "./data/500k.csv"

# # no optimizations, 1m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_1m.txt" --data-file-path "./data/1m.csv"


# ======= Naive Lux workloads, sampling + prune (all current opt) =======

# # no optimizations, 50k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk --sampling

# # no optimizations, 250k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_250k.txt" --data-file-path "./data/250k.csv" --topk --sampling

# # no optimizations, 500k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_500k.txt" --data-file-path "./data/500k.csv" --topk --sampling

# # no optimizations, 1m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/naive_no_opt_1m.txt" --data-file-path "./data/1m.csv" --topk --sampling