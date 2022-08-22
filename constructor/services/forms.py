from django.http import QueryDict
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from constructor.models import Form, FormField, FormSubmission, FormFieldAnswer


def submit_form(data: QueryDict, form: Form):
    req_fields = form.fields.filter(required=True).values_list("id", flat=True)
    subm = FormSubmission.objects.create(form=form)
    answers = []

    for el_id, text in data.items():
        field = get_object_or_404(FormField, id=el_id)
        if field.max_length < len(text):
            subm.delete()
            raise ValidationError("text is too long")
        answers.append(el_id)
        FormFieldAnswer.objects.create(submission=subm, field=field, text=text)

    if not all(x in answers for x in req_fields):
        subm.delete()
        raise ValidationError("not all required fields are satisfied")

    return
