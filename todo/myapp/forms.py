from django import forms

class create_task_form(forms.Form):
    task=forms.CharField(label="task",max_length=100)
    member_id=forms.IntegerField(label="member_id")
    due_date=forms.DateField(label="due_date")