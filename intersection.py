from translations import tr

"""
Moduł do sprawdzania przecięcia dwóch odcinków w przestrzeni 2D.

Wykorzystany algorytm:
-------------------------
Algorytm opiera się na klasycznym podejściu geometrycznym, które wykorzystuje orientację trzech punktów,
iloczyn wektorowy oraz sprawdzenie warunku przecięcia na podstawie wzajemnych orientacji końców odcinków.

Krok po kroku:
--------------
1. **Orientacja trzech punktów (funkcja `orientation`)**
   - Dla każdego trójkąta punktów (p, q, r) obliczany jest znak pola trójkąta, co pozwala określić,
     czy punkty są współliniowe, czy tworzą skręt w lewo (CCW), czy w prawo (CW).
   - Zwracane są wartości:
     - 0: współliniowe
     - 1: zgodnie z ruchem wskazówek zegara (CW)
     - 2: przeciwnie do ruchu wskazówek zegara (CCW)

2. **Sprawdzenie przecięcia odcinków (funkcja `segments_intersect`)**
   - Wykorzystuje orientację czterech trójek punktów, aby określić przecięcie:
     - Przypadek ogólny: jeśli końce jednego odcinka leżą po przeciwnych stronach drugiego (i odwrotnie), to odcinki się przecinają.
     - Przypadki szczególne: sprawdzane są sytuacje, gdy punkty są współliniowe i mogą leżeć na odcinkach.

3. **Obliczanie punktu przecięcia (funkcja `intersection_point`)**
   - Dla przecinających się prostych, które nie są równoległe, obliczany jest punkt przecięcia za pomocą wzorów na podstawie równań prostych.
   - W przypadku odcinków równoległych (denominator ≈ 0), zwracane jest `None`.

4. **Funkcja `check_intersection` (funkcja główna)**
   - Przyjmuje współrzędne dwóch odcinków.
   - Sprawdza, czy odcinki się przecinają.
   - Zwraca komunikat:
     - brak przecięcia,
     - przecięcie w konkretnym punkcie,
     - informacja o nałożeniu się (gdy są współliniowe i nakładają się częściowo lub całkowicie),
     - wszystkie punkty są identyczne,
     - podano punkty, nie odcinki.
"""

def orientation(p, q, r):
    """
    Zwraca orientację trzech punktów (p, q, r):
    - 0: punkty są współliniowe,
    - 1: układ zgodny z ruchem wskazówek zegara,
    - 2: układ przeciwny do ruchu wskazówek zegara.
    
    Używa iloczynu wektorowego do określenia znaku kąta między wektorami pq i qr.
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    """
    Sprawdza, czy punkt q leży na odcinku pr (gdy wszystkie 3 punkty są współliniowe).
    """
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

def segments_intersect(p1, q1, p2, q2):
    """
    Sprawdza, czy odcinki p1q1 i p2q2 przecinają się.
    Uwzględnia zarówno przypadek ogólny, jak i przypadki szczególne (współliniowość).
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Przypadek ogólny: różne orientacje
    if o1 != o2 and o3 != o4:
        return True

    # Przypadki szczególne: punkty współliniowe i leżące na odcinkach
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

def intersection_point(p1, p2, p3, p4):
    """
    Oblicza punkt przecięcia dwóch odcinków (p1p2 i p3p4),
    rozwiązując układ równań parametrycznych prostych.
    
    Zwraca punkt przecięcia jako (x, y) lub None, jeśli odcinki są równoległe.
    """
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # Wyznacznik (mianownik) układu równań
    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(denom) < 1e-9:
        return None  # odcinki są równoległe lub pokrywają się

    # Wzory na punkt przecięcia (x, y)
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
    return (px, py)

def check_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    Sprawdza przecięcie dwóch odcinków zadanych współrzędnymi:
    (x1, y1)-(x2, y2) i (x3, y3)-(x4, y4).
    
    Zwraca komunikat tekstowy:
    - brak przecięcia,
    - przecięcie w punkcie,
    - nałożenie się odcinków,
    - wszystkie punkty są identyczne,
    - podano punkty, nie odcinki.
    """
    p1, q1 = (x1, y1), (x2, y2)
    p2, q2 = (x3, y3), (x4, y4)

    # Sprawdzenie, czy oba odcinki są punktami
    if p1 == q1 and p2 == q2:
        if p1 == p2:
            return (tr("all_same_point").format(x=x1, y=y1), (x1, y1))
        else:
            return (tr("pairs_same_point"), None)

    if not segments_intersect(p1, q1, p2, q2):
        return (tr("no_intersection"), None)

    # Sprawdzenie czy są współliniowe i nachodzą na siebie
    if orientation(p1, q1, p2) == 0 and orientation(p1, q1, q2) == 0:
        points = sorted([p1, q1, p2, q2])
        a, b = points[1], points[2]
        if a == b:
            return (tr("intersect_at").format(x=a[0], y=a[1]), a)
        else:
            return (tr("overlap").format(a=a, b=b), (a, b))

    # Punkt przecięcia w przypadku zwykłego przecięcia
    pt = intersection_point(p1, q1, p2, q2)
    if pt:
        return (tr("intersect_at").format(x=pt[0], y=pt[1]), pt)
    else:
        return (tr("intersect_but_error"), None)
