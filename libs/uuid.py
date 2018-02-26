# coding=utf-8

import uuid
import random

CHOICE_CODE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def create_uuid(name=""):
    """create uuid"""
    return str(uuid.uuid4())


def create_student_uid(name=""):
    """创建学生UID"""
    s = "S"
    for i in range(6):
        s += random.choice(CHOICE_CODE)
    return s


def create_teacher_uid(name=""):
    """创建学生UID"""
    s = "T"
    for i in range(6):
        s += random.choice(CHOICE_CODE)
    return s