from datetime import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from .models import Article

admin.site.register([Article, ])


class CurrentLoggedInUsersFilter(SimpleListFilter):
    title = 'Currently Logged In'
    parameter_name = 'is_logged_in'

    def lookups(self, request, model_admin):
        options = [
            {'id': 0, 'text': 'OFFLINE'},
            {'id': 1, 'text': 'ONLINE'},
        ]
        return [(opt.get('id'), opt.get('text')) for opt in options]

    def queryset(self, request, queryset):
        # Query all non-expired sessions
        sessions = Session.objects.filter(expire_date__gte=datetime.now())
        uid_list = []

        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

        if self.value() == '1':
            return queryset.filter(id__in=uid_list)
        elif self.value() == '0':
            return queryset.exclude(id__in=uid_list)
        return queryset


class UserAdmin(admin.ModelAdmin):
    list_filter = (CurrentLoggedInUsersFilter,)

    class Meta:
        model = User


admin.site.unregister([User, ])
admin.site.register(User, UserAdmin)
