# ======= Incremental Lux workloads =======

# 1/16 total incremental ops (1/32 deletes, 1/32 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_16.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 16

# 1/8 total incremental ops (1/16 deletes, 1/16 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_8.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 8

# 1/4 total incremental ops (1/8 deletes, 1/8 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_4.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 4

# 1/2 total incremental ops (1/4 deletes, 1/4 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_2.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 2

# 1/1 total incremental ops (1/2 deletes, 1/2 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_1.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 1

# 1/.75 total incremental ops (.67 deletes, .67 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_pt_75.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 0.75

# 1/.67 total incremental ops (.75 deletes, .75 row adds)
python3 incremental_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/incremental_pt_67.txt" --data-file-path "./data/crimedata.csv" --num-ops-frac 0.67

# baseline eval
python3 baseline_eval.py --num-trials 10 --log-file-path "./incr_experiment_logs/baseline.txt" --data-file-path ./data/crimedata.csv