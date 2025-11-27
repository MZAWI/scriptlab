if __name__ == "__main__":
    top: int = 3
    test_results: dict = {}
    sum: int = 0
    avg: float = 0
    passed: int = 0

    while True:
        user_in: str = input("[Imię] [Ocena]: ").strip()
        if user_in.lower() == "koniec":
            break
        try:
            stud, mark = user_in.split()
            mark = int(mark)
            if mark < 0 or mark > 100:
                raise ValueError("zakres oceny [0-100]")
        except ValueError as e:
            print(f"Nieprawidłowe dane wejściowe: {e}")
            continue
        test_results[stud] = mark
    count: int = len(test_results)

    if count < 5:
        exit("Minium 5 osób")

    print(f"Top {top} studentów:")
    for stud, mark in sorted(
        test_results.items(), key=lambda item: item[1], reverse=True
    ):
        if top > 0:
            print(f"{stud}: {mark}")
            top -= 1
        if mark >= 50:
            passed += 1
        sum += mark

    print(f"Zdało: {passed}")
    print(f"Średni wynik: {sum/count}")

    for stud, mark in test_results.items():
        if mark < 50:
            grade = 2.0
        else:
            grade = 3.0 + ((mark - 50) // 10) * 0.5
        print(f"{stud} {min(grade, 5.0)}")
