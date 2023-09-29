CREATE TABLE ilmoweb_user(
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    username TEXT,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    last_login DATE,
    is_superuser BOOL,
    is_staff BOOL,
    is_active BOOL,
    date_joined DATE);

CREATE TABLE ilmoweb_courses(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    labs_amount INTEGER,
    is_visible BOOL);

CREATE TABLE ilmoweb_labs(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    max_students INTEGER,
    is_visible TEXT,
    course_id INTEGER);

CREATE TABLE ilmoweb_labgroups(
    id SERIAL PRIMARY KEY,
    date DATE,
    start_time TIME,
    end_time TIME,
    place TEXT,
    status INTEGER,
    lab_id INTEGER);