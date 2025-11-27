import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    csvfile = "app_log.csv"

    df = pd.read_csv(csvfile, parse_dates=["timestamp"]).set_index("timestamp")
    login_requests = (df["endpoint"] == "/login").sum()
    # print(df["endpoint"] == "/login")
    print(f"login requests: {login_requests}")

    login_requests_per_user = df[df["endpoint"] == "/login"].groupby("user").size()
    print(f"\nRequests per user: \n{login_requests_per_user}")

    errors_per_user = (
        df[df["status_code"] != 200].groupby("user").size().to_frame("errors")
    )
    print(f"\nErrors per user:\n{errors_per_user}\n")

    pivtable = pd.pivot_table(
        df,
        index="user",
        columns="status_code",
        values="endpoint",
        aggfunc="count",
        fill_value=0,
    )
    print(pivtable)

    print(errors_per_user.sort_values(by="errors", ascending=False))
    errors_per_user.plot(kind="bar")
    # plt.show()
    traffic_per_hour = df.resample('1min').size().sort_values(ascending=False).head(7)
    print(traffic_per_hour)
