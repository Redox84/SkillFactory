from django_filters import FilterSet
from .models import *


class PostFilters(FilterSet):

    class Meta:
        model = Respon
        fields = [
            'postR',
        ]

    def __init__(self, *args, **kwargs):
        super(PostFilters, self).__init__(*args, **kwargs)
        self.filters['postR'].queryset = Post.objects.filter(author_id=kwargs['request'])
