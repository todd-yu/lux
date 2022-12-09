# ======= Naive Lux workloads, no optimizations =======

# # no optimizations, 50k
python3 naive_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs_v2/base_naive_topk50_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk

# # no optimizations, 250k
python3 naive_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs_v2/base_naive_topk50_250k.txt" --data-file-path "./data/250k.csv" --topk

# # no optimizations, 500k
python3 naive_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs_v2/base_naive_topk50_500k.txt" --data-file-path "./data/500k.csv" --topk

# # no optimizations, 1m
python3 naive_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs_v2/base_naive_topk50_1m.txt" --data-file-path "./data/1m.csv" --topk

# # no optimizations, 5m
python3 naive_lux_workload.py --num-trials 10 --log-file-path "./experiment_logs_v2/base_naive_topk50_5m.txt" --data-file-path "./data/5m.csv" --topk


# ======= Naive Lux workloads, all optimizations =======

# # no optimizations, 50k
# python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/base_incremental_v2_all_opt_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk --sampling

# # # no optimizations, 250k
# python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/base_incremental_v2_all_opt_250k.txt" --data-file-path "./data/250k.csv" --topk --sampling

# # # no optimizations, 500k
# python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/base_incremental_v2_all_opt_500k.txt" --data-file-path "./data/500k.csv" --topk --sampling

# # # no optimizations, 1m
# python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/base_incremental_v2_all_opt_1m.txt" --data-file-path "./data/1m.csv" --topk --sampling

# # # no optimizations, 5m
# python3 raw_vis_combined_workload.py --num-trials 10 --log-file-path "./experiment_logs/base_incremental_v2_all_opt_5m.txt" --data-file-path "./data/5m.csv" --topk --sampling