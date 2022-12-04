# ======= Naive Lux workloads, no optimizations =======

# # no optimizations, 50k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_50k.txt" --data-file-path "./data/AB_NYC_2019.csv"

# # no optimizations, 250k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_250k.txt" --data-file-path "./data/250k.csv"

# # no optimizations, 500k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_500k.txt" --data-file-path "./data/500k.csv"

# # no optimizations, 1m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_1m.txt" --data-file-path "./data/1m.csv"

# # no optimizations, 5m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_5m.txt" --data-file-path "./data/5m.csv"


# ======= Naive Lux workloads, sampling + prune (all current opt) =======

# all optimizations, 50k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_all_opt_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk --sampling

# all optimizations, 250k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_all_opt_250k.txt" --data-file-path "./data/250k.csv" --topk --sampling

# all optimizations, 500k
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_all_opt_500k.txt" --data-file-path "./data/500k.csv" --topk --sampling

# all optimizations, 1m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_all_opt_1m.txt" --data-file-path "./data/1m.csv" --topk --sampling

# all optimizations, 5m
python3 naive_lux_workload.py --num-trials 30 --log-file-path "./experiment_logs/mqo_all_opt_5m.txt" --data-file-path "./data/5m.csv" --topk --sampling
