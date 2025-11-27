import pandas as pd

# 1-2. Read files
linux = pd.read_csv("linux_log.csv", parse_dates=["timestamp"])
windows = pd.read_csv("windows_log.csv", parse_dates=["timestamp"])
web = pd.read_csv("web_log.csv", parse_dates=["timestamp"])

# common ips
common_ip = set(linux["IP"]) & set(windows["IP"]) & set(web["IP"])
print(common_ip, "\n")

merged_linwin = pd.merge_asof(
    linux.sort_values("timestamp"),
    windows.sort_values("timestamp"),
    by="IP",
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("10s"),
)

merged = pd.merge_asof(
    merged_linwin.sort_values("timestamp"),
    web.sort_values("timestamp"),
    by="IP",
    on="timestamp",
    direction="nearest",
    tolerance=pd.Timedelta("10s"),
)
print(merged)

# Błędy w więcej niż jednym systemie
err_lin = merged["status"] == "FAILED"
err_win = merged["event"] == "LoginFailed"
err_web = merged["status_code"] != "200"
# errors = err_lin + err_win + err_web > 1
errors = err_lin.astype(int) + err_win.astype(int) + err_web.astype(int)

both_failed = merged[errors > 1]
print(both_failed)

