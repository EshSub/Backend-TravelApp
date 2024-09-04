from django.contrib import admin
from cms.models import Profile, EmailConfirmation, Place, Activity, PlaceActivity, Type, Tag, District, Province, Image
from messaging.models import Message, Conversation
class ListAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        fields = model._meta.fields
        first_field = "id"
        if first_field in fields:
            self.list_display = [f.name for f in fields].insert(
                0, fields.pop(fields.index(first_field))
            )
        else:
            self.list_display = [f.name for f in fields]

        # self.list_filter = [f.name for f in fields if type(f) in filter_field_types]
        # self.search_fields = [f.name for f in fields if type(f) in search_field_types]

        # if "user" in self.list_display:
        #     self.search_fields.append("user__username")
        # if "group" in self.list_display:
        #     self.list_filter.append("group__name")
        super(ListAdmin, self).__init__(model, admin_site)

# Register your models here.
admin.site.register(Profile, ListAdmin)
admin.site.register(EmailConfirmation, ListAdmin)
admin.site.register(Place, ListAdmin)
admin.site.register(Activity, ListAdmin)
admin.site.register(PlaceActivity, ListAdmin)
admin.site.register(Type, ListAdmin)
admin.site.register(Tag, ListAdmin)
admin.site.register(District, ListAdmin)
admin.site.register(Province, ListAdmin)
admin.site.register(Message,ListAdmin)
admin.site.register(Conversation,ListAdmin)
admin.site.register(Image,ListAdmin)

