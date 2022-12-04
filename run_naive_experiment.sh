# ======= Naive Lux workloads, no optimizations =======

# # no optimizations, 50k
python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/mqo_stats_combined_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk

# # no optimizations, 250k
python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/mqo_stats_combined_250k.txt" --data-file-path "./data/250k.csv" --topk

# # no optimizations, 500k
python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/mqo_stats_combined_500k.txt" --data-file-path "./data/500k.csv" --topk

# # no optimizations, 1m
python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/mqo_stats_combined_1m.txt" --data-file-path "./data/1m.csv" --topk

# # no optimizations, 5m
python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/mqo_stats_combined_5m.txt" --data-file-path "./data/5m.csv" --topk

