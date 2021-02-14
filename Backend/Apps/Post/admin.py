from django.contrib import admin

from Apps.Post.models import TagUser, Post, PostPhoto


class TagUserAdmin(admin.TabularInline):
    model = TagUser
    fields = ('user', 'post')
    fk_name = 'post'


class PostAdmin(admin.ModelAdmin):
    inlines = (TagUserAdmin,)


admin.site.register(Post, PostAdmin)
admin.site.register(PostPhoto)
