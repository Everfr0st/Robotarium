def get_semester_name(semester):
    switcher = {
        1: 'Primer semestre',
        2: 'Segundo semestre',
        3: 'Tercer semestre',
        4: 'Cuarto semestre',
        5: 'Quinto semestre',
        6: 'Sexto semestre',
        7: 'Séptimo semestre',
        8: 'Octavo semestre',
        9: 'Noveno semestre',
        10: 'Décimo semestre',
        11: 'Pensionado/a',
    }
    return switcher.get(semester, "Pensinado/a")
