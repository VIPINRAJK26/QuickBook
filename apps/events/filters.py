from django.db.models import Q


class EventFilter:

    @staticmethod
    def filter_queryset(*, queryset, params):
        search = params.get("search")
        location = params.get("location")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(location__icontains=search)
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        return queryset