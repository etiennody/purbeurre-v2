"""Filter the results from Product database model
"""
from django.views.generic import ListView

from .models import Product


class SearchResultsView(ListView):
    """Limit the search results page to filter the results outputted based upon a search query

    Args:
        ListView (generic class-based views): render some list of objects

    Returns:
        list: return the list of items for search results view
    """

    model = Product
    template_name = "product/search_results.html"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(name__icontains=query).order_by("name")
        return object_list
