# ======= Naive Lux workloads, no optimizations =======

# # no optimizations, 50k
python3 granular_mqo_workload.py --num-trials 10 --log-file-path "./experiment_logs/granular_mqo_50k.txt" --data-file-path "./data/AB_NYC_2019.csv" --topk

# # no optimizations, 250k
python3 granular_mqo_workload.py --num-trials 10 --log-file-path "./experiment_logs/granular_mqo_250k.txt" --data-file-path "./data/250k.csv" --topk

# # no optimizations, 500k
python3 granular_mqo_workload.py --num-trials 10 --log-file-path "./experiment_logs/granular_mqo_500k.txt" --data-file-path "./data/500k.csv" --topk

# # no optimizations, 10
python3 granular_mqo_workload.py --num-trials 10 --log-file-path "./experiment_logs/granular_mqo_1m.txt" --data-file-path "./data/1m.csv" --topk

# # no optimizations, 5m
python3 granular_mqo_workload.py --num-trials 10 --log-file-path "./experiment_logs/granular_mqo_5m.txt" --data-file-path "./data/5m.csv" --topk
