def orientation(p, q, r):
    # Zwraca 0 jeśli współliniowe, 1 jeśli zgodnie z ruchem zegara, 2 przeciwnie
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2

def convex_hull(points):
    # Usuwa duplikaty
    points = list(set(points))
    if len(points) == 1:
        return points
    if len(points) == 2:
        return sorted(points)

    # Sortuj po x, potem y
    points.sort()

    # Dolna otoczka
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) != 2:
            lower.pop()
        lower.append(p)

    # Górna otoczka
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) != 2:
            upper.pop()
        upper.append(p)

    # Połącz bez powtarzania końców
    return lower[:-1] + upper[:-1]

def compute_convex_hull(coords):
    points = [(coords[i], coords[i+1]) for i in range(0, len(coords), 2)]
    hull = convex_hull(points)

    if len(set(points)) == 1:
        return f"Otoczka wypukła to punkt: {points[0]}"
    elif len(hull) == 2:
        return f"Otoczka wypukła to odcinek od {hull[0]} do {hull[1]}"
    elif len(hull) == 3:
        return f"Otoczka wypukła to trójkąt z wierzchołkami: {hull}"
    elif len(hull) == 4:
        return f"Otoczka wypukła to czworokąt z wierzchołkami: {hull}"
    else:
        return f"Nieoczekiwana liczba wierzchołków: {len(hull)}"
