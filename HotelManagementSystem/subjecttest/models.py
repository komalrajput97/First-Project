# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Subject(models.Model):
    """
    Models for storing subjects
    """

    subject_name = models.CharField(max_length=60)

    def __str__(self):
        return self.subject_name


class Standard_Subject(models.Model):
    """
    Model for storing standards and subjects in that standard
    """

    standard = models.PositiveIntegerField(
        choices=[(c, c) for c in range(1, 13)])
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return str(self.standard)

    @classmethod
    def get_standard_list(cls):
        return [c for c in range(1, 13)]


class Question(models.Model):
    """
    Model for storing questions of each subject
    """

    question = models.TextField()
    option1 = models.CharField(max_length=60)
    option2 = models.CharField(max_length=60)
    option3 = models.CharField(max_length=60)
    option4 = models.CharField(max_length=60)
    answer = models.CharField(max_length=60)
    std_id = models.ForeignKey(Standard_Subject, on_delete=models.CASCADE)
    sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return str("Std:{},Sub:{}").format(self.std_id.standard,self.sub_id.subject_name)