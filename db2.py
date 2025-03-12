import sqlite3
from datetime import datetime
import os
import json


def insert_subjects(class_name , subject_name, lesson_name):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    query = "INSERT INTO subjects (class,subject_name, lesson_name) VALUES (?,?, ?)"
    cur.execute(query, (class_name, subject_name, lesson_name))
    conn.commit()
    conn.close()


def init_subjects():
    # Load data from the JSON file
    with open('subjects.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Iterate through the JSON data and insert into the database
    for class_name, subjects in data.items():
        for subject_name, lessons in subjects.items():
            for lesson in lessons:
                # print(class_name,subject_name,lesson)
                insert_subjects(class_name,subject_name, lesson)
    print("Subjects inserted successfully!")


init_subjects()