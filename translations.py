current_language = "PL"

translations = {
    "PL": {
        "title": "Geo",
        "new": "Nowy obiekt",
        "load": "Wczytaj",
        "options": "Opcje",
        "info": "Informacje",
        "exit": "Wyjdź",
        "language": "Język",
        "theme": "Motyw",
        "size": "Rozmiar okna",
        "back": "Wróć",
        "main_title": "Aplikacja Geometryczna",
        "prompt": "Wybierz:",
        "intersection": "1. Przecięcie dwóch odcinków",
        "convex": "2. Otoczka wypukła",
        "calculate": "Oblicz",
        "save": "Zapisz",
        "coords_prompt_2": "Podaj współrzędne punktów:",
        "coords_prompt_4": "Podaj współrzędne 4 punktów:",
        "info_text": (
            "Projekt aplikacji geometrycznej składającej się z dwóch modułów:\n\n"
            "1. Przecięcie dwóch odcinków – określa, czy odcinki przecinają się "
            "i zwraca punkt przecięcia lub odcinek przecięcia, jeśli się pokrywają.\n\n"
            "2. Otoczka wypukła – wyznacza otoczkę wypukłą zbioru punktów "
            "i określa jej typ: punkt, odcinek, trójkąt lub czworokąt.\n\n"
        ),
        "info_title": "Informacje o projekcie",
        "plot_title": "Kliknij, aby zaznaczyć punkty",
        "save_success": "Punkty zapisano do pliku:",
        "save_error": "Nie udało się zapisać punktów:",
        "saved": "Zapisano",
        "error": "Błąd",
        "no_data_saved": "Brak zapisanych danych.",
        "delete": "Usuń",
        "error_info": "Nieprawidłowy format pliku.",
        "delete_confirm": "Czy na pewno usunąć:\n{filename}?",
        "result": "Wynik",
        "no_intersection": "Odcinki nie przecinają się.",
        "intersect_at": "Odcinki przecinają się w punkcie: ({x:.2f}, {y:.2f})",
        "overlap": "Odcinki nakładają się na odcinku od {a} do {b}",
        "intersect_but_error": "Odcinki przecinają się ale nie udało się znaleźć punktu przecięcia."
    },
    "EN": {
        "title": "Geo",
        "new": "New object",
        "load": "Load",
        "options": "Options",
        "info": "Info",
        "exit": "Exit",
        "language": "Language",
        "theme": "Theme",
        "size": "Window size",
        "back": "Back",
        "main_title": "Geometry App",
        "prompt": "Choose:",
        "intersection": "1. Line segment intersection",
        "convex": "2. Convex hull",
        "calculate": "Calculate",
        "save": "Save",
        "coords_prompt_2": "Enter coordinates:",
        "coords_prompt_4": "Enter coordinates of 4 points:",
        "info_text": (
            "A geometry application project consisting of two modules:\n\n"
            "1. Segment intersection – determines whether two line segments intersect "
            "and returns the point of intersection or the overlapping segment if they are collinear.\n\n"
            "2. Convex hull – computes the convex hull of a set of points "
            "and identifies its type: point, segment, triangle, or quadrilateral.\n\n"
        ),
        "info_title": "Project Info",
        "plot_title": "Click to mark points",
        "save_success": "Points saved to file:",
        "save_error": "Failed to save points:",
        "saved": "Saved",
        "error": "Error",
        "no_data_saved": "No data saved.",
        "delete": "Delete",
        "error_info": "Incorrect file format.",
        "delete_confirm": "Are you sure you want to delete:\n{filename}?",
        "result": "Result",
        "no_intersection": "Segments do not intersect.",
        "intersect_at": "Segments intersect at point: ({x:.2f}, {y:.2f})",
        "overlap": "Segments overlap from {a} to {b}",
        "intersect_but_error": "Segments intersect but intersection point could not be found."
    }
}

def tr(key):
    return translations.get(current_language, {}).get(key, key)

def set_language_global(lang):
    global current_language
    current_language = lang
