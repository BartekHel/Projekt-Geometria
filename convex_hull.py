from translations import tr

# Funkcja oblicza otoczkę wypukłą zbioru punktów na płaszczyźnie
# przy użyciu algorytmu Andrew's Monotone Chain – jednego z wariantów algorytmu Grahama.
#
# Działanie:
# - Dla mniej niż 3 unikalnych punktów zwraca odpowiedni komunikat (punkt / odcinek).
# - Dla 3 lub więcej punktów konstruuje otoczkę wypukłą:
#   * sortuje punkty rosnąco według x i y,
#   * buduje dolną i górną część otoczki,
#   * łączy je w finalną otoczkę (usuwając powtórzenia).
#
# Zwraca:
# - tekstowy opis typu otoczki wypukłej (punkt, odcinek, trójkąt, czworokąt, wielokąt z n wierzchołkami)
# - listę nazwanych punktów w kolejności pojawienia się na otoczce: P1 (x, y), P2 (x, y), ...

def compute_convex_hull(points):
    # 1. Usunięcie duplikatów i przygotowanie
    unique_points = list(set(points))  # unikamy wielokrotnego wpisania tego samego punktu
    n = len(unique_points)

    # 2. Obsługa przypadków brzegowych (mniej niż 3 punkty)
    if n == 0:
        return tr("no_points"), []
    elif n == 1:
        x, y = unique_points[0]
        return f"{tr('convex_is_point')}\n{tr('convex_vertices')}:\nP1 ({x}, {y})", [(x, y)]
    elif n == 2:
        (x1, y1), (x2, y2) = unique_points
        return f"{tr('convex_is_segment')}\n{tr('convex_vertices')}:\nP1 ({x1}, {y1})\nP2 ({x2}, {y2})", [(x1, y1), (x2, y2)]

    # 3. Dodanie indeksów do punktów (potrzebne do etykietowania np. P1, P2)
    indexed_points = [(x, y, i + 1) for i, (x, y) in enumerate(points)]

    # 4. Sortowanie punktów najpierw po x, potem po y
    indexed_points.sort()

    # 5. Funkcja pomocnicza – oblicza iloczyn wektorowy dla trzech punktów
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - \
               (a[1] - o[1]) * (b[0] - o[0])

    # 6. Budowanie dolnej części otoczki (z lewej do prawej)
    lower = []
    for p in indexed_points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # 7. Budowanie górnej części otoczki (z prawej do lewej)
    upper = []
    for p in reversed(indexed_points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # 8. Połączenie dolnej i górnej części, bez duplikatów końcowych punktów
    hull = lower[:-1] + upper[:-1]

    # 9. Ustalenie typu otoczki wypukłej na podstawie liczby unikalnych punktów
    num_vertices = len(set((x, y) for x, y, _ in hull))
    if num_vertices == 3:
        shape_type = tr("convex_is_triangle")
    elif num_vertices == 4:
        shape_type = tr("convex_is_quadrilateral")
    else:
        shape_type = tr("convex_is_polygon").format(n=num_vertices)

    # 10. Przygotowanie wyniku tekstowego do wyświetlenia w GUI
    result_lines = [shape_type]
    result_lines.append(f"{tr('convex_vertices')}:")
    for x, y, index in hull:
        result_lines.append(f"P{index} ({x}, {y})")

    hull_coords = [(x, y) for x, y, _ in hull]
    return "\n".join(result_lines), hull_coords
