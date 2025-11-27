import pandas as pd

# 1. read CSV
log_a = pd.read_csv("server_A.csv", parse_dates=["timestamp"])
log_b = pd.read_csv("server_B.csv", parse_dates=["timestamp"])
log_a['source'] = 'A'
log_b['source'] = 'B'

# 2. find common IPs
common_ip = set(log_a["IP"]) & set(log_b["IP"])
log_a_comm = log_a[log_a["IP"].isin(common_ip)].sort_values("timestamp")
log_b_comm = log_b[log_b["IP"].isin(common_ip)].sort_values("timestamp")

# print(common_ip, "\n")  

# 3. join common IP logs
merged = pd.merge_asof(
    log_a_comm,  # must be sorted
    log_b_comm,
    by="IP",
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("5s"),  # on timestamp +- 5s
)

# print(merged, "\n")

both_failed = merged[
    (merged["action"] == "LOGIN_FAIL") & (merged["event"] == "LoginFailed")
]

# 4. both servers failed request from the same IP
print(both_failed[["timestamp", "IP", "action"]], "\n")

# 5. error statistics by IP
err_count = both_failed["IP"].value_counts() # sorts by default
print(err_count, "\n")

# 6. Most correlations
print(err_count.head(2), "\n")

# 7. usernames from both systems same IP
print(both_failed[["IP", "user", "username"]])
