from teacher_data_processing.make_json.school_data import school


def update(kind: str, school_name: str, period=None):
    school.update(kind=kind, school_name=school_name, period=period)
