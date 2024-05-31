from django.contrib import admin, messages
from django.db.models import Q
from django.utils.safestring import mark_safe

from .models import Man, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус мужчины'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Женат'),
            ('single', 'Холост'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(wife__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(wife__isnull=True)


@admin.register(Man)
class ManAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'photo', 'post_photo', 'slug', 'cat', 'wife', 'tags')
    readonly_fields = ('slug', 'post_photo')
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['is_published', MarriedFilter, 'cat__name']
    save_on_top = True

    @admin.display(description="Фотография", ordering='content')
    def post_photo(self, man: Man):
        if man.photo:
            return mark_safe(f"<img src='{man.photo.url}' width=50>")
        return f"Без фото"

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Man.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description='Снять публикации с выбранных записей')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Man.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']
