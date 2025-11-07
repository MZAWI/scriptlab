# lista słowników z danymi użytkowników
users = [
    {"nazwisko": "Nowak", "wiek": 25},
    {"nazwisko": "Kowalski", "wiek": 21},
    {"nazwisko": "Wiśniewski", "wiek": 19}
]

# max zwraca największą wartość z podanego iterowalnego obiektu
print(max(u["wiek"] for u in users)) # -> 25 (tylko liczba wieku)

# dzięki key=lambda u: u["wiek"] zwracany jest cały słownik osoby najstarszej
# lambda tworzy małą, jednorazową funkcję bez nazwy, której używamy tam, 
# gdzie chcemy szybko określić sposób przetwarzania, wybierania lub porównywania danych.
najstarszy = max(users, key=lambda u: u["wiek"])
# bez użycia funkcji lambda:
# def get_wiek(u):
#     return u["wiek"]
# najstarszy = max(users, key=get_wiek)

print(najstarszy) # {'nazwisko': 'Nowak', 'wiek': 25}

# wyznaczenie średniego wieku oraz suma wieku
suma_wieku = sum(u["wiek"] for u in users)
sredni_wiek = suma_wieku / len(users)
print(f"Średni wiek: {sredni_wiek}") # -> Średni wiek: 21.666666666666668

# lub z formatowaniem
print(f"Średni wiek: {sredni_wiek:.2f}") # -> Średni wiek: 21.67
print(f"Suma wieku: {suma_wieku}") # -> Suma wieku: 65
# sortowanie owoców zapisanych w krotce
owoce = ("banan", "jabłko", "gruszka", "kiwi")
posortowane_owoce = sorted(owoce)
for i, owoc in enumerate(posortowane_owoce, start=1):
    print(f"{i}. {owoc}")

# 1. banan
# 2. gruszka
# 3. jabłko
# 4. kiwi
