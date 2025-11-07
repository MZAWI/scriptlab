import pandas as pd

# Wczytanie logów z pliku CSV o formacie:
# timestamp,IP,Użytkownik,Status
# 2025-09-28 10:12:34,192.168.0.1,root,FAILED

# parse_dates konwertuje kolumnę timestamp na typ datetime
# df to DataFrame - struktura danych podobna do tabeli
df = pd.read_csv("logi.csv", parse_dates=["timestamp"])

# Podgląd danych
print("Podgląd danych logowania:")
print(df.head()) # pierwsze 5 wierszy

# 1. Zliczanie nieudanych logowań (FAILED) dla każdego użytkownika
# Filtrowanie wierszy z Status 'FAILED', grupowanie po 'Użytkownik' i zliczanie
# failed_per_user to Series - typ jednowymiarowa tablica z etykietami z biblioteki pandas
# indeks (etykiety) to nazwy użytkowników, wartości to liczba nieudanych logowań
failed_per_user = df[df['Status'] == 'FAILED'].groupby('Użytkownik').size()
print("\nNieudane logowania na użytkownika:")
print(failed_per_user)

# grouped_failed to DataFrameGroupBy - obiekt grupujący DataFrame
grouped_failed = df[df['Status'] == 'FAILED'].groupby('Użytkownik')
print("\nLista nieudanych logowań na użytkownika:")
for user, group in grouped_failed:
    print(f"Użytkownik: {user}")
    print (group)

# 2. Zliczanie prób logowania z każdego adresu IP
# logins_per_ip to Series
logins_per_ip = df.groupby('IP').size()
print("\nLiczba prób logowania z każdego IP:")
print(logins_per_ip)

# 3. Podsumowanie (ile razy użytkownik miał OK i FAILED)
# .unstack() zamienia Series na DataFrame aby mieć kolumny dla każdego statusu: OK i FAILED
# w wierszach są użytkownicy z liczbą zdarzeń dla każdego statusu
# w ten sposób uzyskujemy tabelę przestawną (pivot table)
summary_by_user = df.groupby(['Użytkownik', 'Status']).size().unstack(fill_value=0)
print("\nPodsumowanie zdarzeń (OK/FAILED) na użytkownika:")
print(summary_by_user)
# pivot_table można też stworzyć bezpośrednio:
# summary_by_user = df.pivot_table(index='Użytkownik', columns='Status', aggfunc='size', fill_value=0)
# print(summary_by_user)

# 4. Analiza w czasie – liczba zdarzeń w poszczególnych minutach
# set_index('timestamp') ustawia kolumnę timestamp jako indeks (oś czasu)
# resample('1min') grupuje dane w odstępach jednominutowych
events_over_time = df.set_index('timestamp').resample('1min').size()
print("\nLiczba zdarzeń w poszczególnych minutach:")
print(events_over_time)

# 5. Eksport podsumowania do CSV
summary_by_user.to_csv("summary_by_user.csv")
print("\nPodsumowanie zapisane w pliku 'summary_by_user.csv'")
