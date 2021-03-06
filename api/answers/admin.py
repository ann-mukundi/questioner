from django.contrib import admin
from answers.models import Answer, AnswerVote
# Register your models here.


class AnswerAdmin(admin.ModelAdmin):
    """
    Customizing the Answer panel
    """
    list_display = ["id", "body", "question",
                    "date_created_on", "date_updated_on"]


admin.site.register(AnswerVote)
admin.site.register(Answer, AnswerAdmin)
