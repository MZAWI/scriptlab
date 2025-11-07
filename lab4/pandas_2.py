# ============================================================
# 🔹 Analiza logów systemowych (logi.csv) przy użyciu biblioteki pandas
# ============================================================

import pandas as pd

# Wczytanie danych z pliku CSV
# parse_dates automatycznie konwertuje kolumnę timestamp na typ datetime
# Format pliku CSV:
# timestamp,IP,Użytkownik,Status
# 2025-09-28 10:12:34,192.168.0.1,root,FAILED

df = pd.read_csv("logi.csv", parse_dates=['timestamp'])

# Podstawowe informacje o danych
print("\n--- 🔍 Podgląd pierwszych wierszy ---")
print(df.head())  # pokazuje pierwsze 5 wierszy

print("\n--- ℹ️ Informacje o strukturze DataFrame ---")
print(df.info())  # nazwy kolumn, typy danych, liczba niepustych wartości

print("\n--- 📊 Statystyki opisowe ---")
print(df.describe(include='all'))  # statystyki dla wszystkich kolumn (również tekstowych)

# ============================================================
# 🔸 Typ danych Series — pojedyncza kolumna
# ============================================================
print("\nKolumna 'Status' to obiekt typu:", type(df['Status']))

# Możemy np. policzyć liczbę wystąpień poszczególnych statusów:
print("\n--- Liczba wystąpień statusów ---")
print(df['Status'].value_counts())

# ============================================================
# 🔸 Filtrowanie danych
# ============================================================
# Wybieramy tylko wiersze, gdzie Status == 'FAILED'
failed = df[df['Status'] == 'FAILED']

print("\n--- Wiersze z błędami logowania ---")
print(failed)

# ============================================================
# 🔸 Wybór kolumn
# ============================================================
print("\n--- Kolumny 'Użytkownik' i 'Status' ---")
print(df[['Użytkownik', 'Status']].head()) # pierwsze 5 wierszy wybranych kolumn

# ============================================================
# 🔸 Unikalne wartości i ich liczność
# ============================================================
print("\nUnikalni użytkownicy:", df['Użytkownik'].unique())
print("\nLiczba logowań per użytkownik:")
print(df['Użytkownik'].value_counts())

# ============================================================
# 🔸 Grupowanie i agregacja danych
# ============================================================

# 🔹 Liczba błędów (FAILED) na użytkownika
failed_per_user = df[df['Status'] == 'FAILED'].groupby('Użytkownik').size()
print("\n--- Liczba błędów na użytkownika ---")
print(failed_per_user)

# 🔹 Liczba wszystkich prób i błędów per użytkownik (z .agg)
stats = (
    df.groupby('Użytkownik')
        # .agg powoduje utworzenie nowych kolumn z wynikami agregacji
      .agg(
          # wszystkie_proby to liczba wszystkich wierszy (prób) per użytkownik
          # 'count' to funkcja zliczająca w pandas
          wszystkie_proby=('Status', 'count'),
          # błędy to liczba wierszy, gdzie Status == 'FAILED' per użytkownik
          bledy=('Status', lambda x: (x == 'FAILED').sum())
      )
)
# Dodanie kolumny z procentem błędów
stats['% błędów'] = (stats['bledy'] / stats['wszystkie_proby'] * 100).round(1)

print("\n--- Statystyki błędów per użytkownik ---")
print(stats)

# ============================================================
# 🔸 Sortowanie wyników
# ============================================================
print("\n--- Sortowanie użytkowników według liczby błędów ---")
# ascending=False dla sortowania malejącego
print(stats.sort_values(by='bledy', ascending=False))

# ============================================================
# 🔸 Operacje na czasie (timestamp)
# ============================================================

# Tworzymy nowe kolumny: data, godzina
df['Data'] = df['timestamp'].dt.date
df['Godzina'] = df['timestamp'].dt.hour

print("\n--- Nowe kolumny z datą i godziną ---")
print(df[['timestamp', 'Data', 'Godzina']].head())

# 🔹 Liczba błędów w czasie (np. per godzina)
failed_per_hour = (
    df[df['Status'] == 'FAILED']
    .groupby('Godzina')
    .size()
)

print("\n--- Liczba błędów w zależności od godziny ---")
print(failed_per_hour)

# ============================================================
# 🔸 Czyszczenie danych i brakujące wartości
# ============================================================
print("\n--- Liczba braków danych przed czyszczeniem ---")
print(df.isna().sum())

# Usuwamy wiersze z brakami (jeśli by wystąpiły)
df_clean = df.dropna()
print("\nLiczba wierszy po czyszczeniu:", len(df_clean))

# ============================================================
# 🔸 Grupowanie po adresie IP (np. analiza podejrzanych IP)
# ============================================================
# Statystyki błędów per adres IP, ip_stats to nowy DataFrame o kolumnach: próby, błędy
# i wierszach zawierających unikalne adresy IP z ilością prób i błędów
ip_stats = (
    df.groupby('IP')
      .agg(
          proby=('Status', 'count'),
          bledy=('Status', lambda x: (x == 'FAILED').sum())
      )
)
# Dodanie kolumny z procentem błędów
ip_stats['% błędów'] = (ip_stats['bledy'] / ip_stats['proby'] * 100).round(1)

print("\n--- Statystyki błędów per adres IP ---")
print(ip_stats.sort_values(by='bledy', ascending=False))

# ============================================================
# 🔸 Eksport wyników do pliku CSV
# ============================================================
stats.to_csv("statystyki_uzytkownikow.csv", encoding="utf-8")
ip_stats.to_csv("statystyki_ip.csv", encoding="utf-8")
print("\n✅ Wyniki zapisano do plików: 'statystyki_uzytkownikow.csv' i 'statystyki_ip.csv'")

# ============================================================
# 🔸 Wizualizacja danych
# ============================================================
try:
    import matplotlib.pyplot as plt

    # Wykres liczby błędów na użytkownika
    stats['bledy'].plot(kind='bar', title='Liczba błędów logowania na użytkownika')
    plt.xlabel('Użytkownik')
    plt.ylabel('Liczba błędów')
    plt.tight_layout()
    plt.show()

    # Wykres liczby błędów per godzina
    failed_per_hour.plot(kind='line', marker='o', title='Liczba błędów logowania wg godziny')
    plt.xlabel('Godzina')
    plt.ylabel('Liczba błędów')
    plt.tight_layout()
    plt.show()

except ImportError:
    print("\n(Matplotlib nie zainstalowany — pomijam wykresy)")
