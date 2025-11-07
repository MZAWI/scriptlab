import pandas as pd
import matplotlib.pyplot as plt

# 1️⃣ Wczytanie danych z plików
linux = pd.read_csv("logi.csv", parse_dates=['timestamp'])
windows = pd.read_csv("windows_log.csv", parse_dates=['timestamp'])

# 2️⃣ Dodanie źródła danych
linux['source'] = 'Linux'
windows['source'] = 'Windows'

# 3️⃣ Podgląd danych
print("\n--- Linux logi ---")
print(linux.head())

print("\n--- Windows logi ---")
print(windows.head())

# 4️⃣ Szukanie wspólnych adresów IP
common_ips = set(linux['IP']).intersection(set(windows['IP']))
print("\nWspólne adresy IP:", common_ips)

# 5️⃣ Filtrowanie danych tylko dla wspólnych IP
linux_common = linux[linux['IP'].isin(common_ips)]
windows_common = windows[windows['IP'].isin(common_ips)]

# 6️⃣ Dopasowanie zdarzeń po czasie i adresie IP (±5 sekund)
merged = pd.merge_asof(
    linux_common.sort_values('timestamp'), # sort_values wymagane przez merge_asof
    windows_common.sort_values('timestamp'),
    on='timestamp', # kolumna po której łączymy
    by='IP', # dodatkowe kryterium łączenia, adres IP musi się zgadzać
    direction='nearest', # szukaj najbliższego dopasowania w obie strony; 'backward' lub 'forward' dla jednostronnego
    tolerance=pd.Timedelta('5s') # tolerancja czasowa 5 sekund
)

print("\n--- Skorelowane zdarzenia po IP i czasie ---")
print(merged[['timestamp', 'IP', 'Użytkownik', 'Status', 'User', 'Event']])

# 7️⃣ Szukanie przypadków, gdy oba systemy zgłosiły błąd logowania
both_failed = merged[
    (merged['Status'] == 'FAILED') &
    (merged['Event'] == 'LoginFailed')
]

print("\n--- Wspólne błędy logowania (Linux + Windows) ---")
print(both_failed[['timestamp', 'IP', 'Użytkownik', 'User']])

# 8️⃣ Statystyka błędów wg adresu IP
corr_by_ip = both_failed['IP'].value_counts()

print("\n--- Liczba wspólnych błędów per IP ---")
print(corr_by_ip)

# 9️⃣ Wizualizacja
corr_by_ip.plot(kind='bar', title='Wspólne błędy logowania (Linux + Windows)', color='tomato')
plt.xlabel('Adres IP')
plt.ylabel('Liczba korelacji błędów')
plt.tight_layout()
plt.show()
