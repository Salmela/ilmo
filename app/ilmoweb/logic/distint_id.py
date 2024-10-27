"""Module for app logic."""

def sort(data):
    """
        sorts distinct data items into lists
    """
    reports = []
    lab_groups = []
    course_labs = []
    courses = []
    id_1 = []
    id_2 = []
    id_3 = []

    for report in data:
        reports.append(report)

    for report in reports:
        if report.lab_group.id not in id_1:
            lab_groups.append(report.lab_group)

        id_1.append(report.lab_group.id)

    for lab_group in lab_groups:
        if lab_group.lab.id not in id_2:
            course_labs.append(lab_group.lab)

        id_2.append(lab_group.lab.id)

    for lab in course_labs:
        if lab.course.id not in id_3:
            courses.append(lab.course)

        id_3.append(lab.course.id)

    return reports, lab_groups, course_labs, courses

def sort_limited(data):
    """
        sorts distinct data items into lists
    """
    reports = []
    lab_groups = []
    course_labs = []
    courses = []

    for report in data:
        reports.append(report)

    for report in reports:
        lab_groups.append(report.lab_group)

    for lab_group in lab_groups:
        course_labs.append(lab_group.lab)

    for lab in course_labs:
        courses.append(lab.course)

    return reports, lab_groups, course_labs, courses
