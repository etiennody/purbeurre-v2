"""Filter the results from Product database model
"""
from django.views.generic import ListView, DetailView

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
        """Retrieving specific objects with iconatains filter

        Returns:
            list: objects by products name 
        """
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(name__icontains=query).order_by("name")
        return object_list


class SubstituteResultsView(ListView):
    """Limit the substitute results page to filter the results outputted based upon a substitute query

    Args:
        ListView (generic class-based views): render some list of objects

    Returns:
        list: return the list of items for substitutes results view
    """

    model = Product
    template_name = "product/substitute_results.html"
    paginate_by = 6

    def get_queryset(self):
        """Retrieving specific objects with category name and lte filters
        without the product id itself order by nutriscore and energy

        Returns:
            list: objects by complex query
        """
        self._id = self.kwargs["product_id"]
        self.product = Product.objects.get(pk=self._id)
        return (
            Product.objects.filter(categories__name=self.product.categories.first())
            .filter(nutrition_grade__lte=self.product.nutrition_grade)
            .exclude(id=self._id)
            .order_by("nutrition_grade", "energy_100g")
            .distinct("nutrition_grade", "energy_100g")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.product.name
        context["image"] = self.product.image_url
        return context


class ProductDetailsView(DetailView):
    """ProductDetailsView is designed to display product details data

    Args:
        DetailView (generic class-based views):  contain the object that the view is operating upon
    """

    model = Product
    template_name = "product/product_details.html"
    paginate_by = 6
