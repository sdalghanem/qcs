from django.shortcuts import render
from .models import *
# Create your views here.
def get_dept_score_by_secID(id):
    respons = Term_responsible.objects.get(section_id = id)
    term = Term_score.objects.get(term_id = respons.term_id)
    print(term)
    return term

def add_term(request , id):
    pass