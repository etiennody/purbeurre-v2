"""Filter the results from Product database model
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from .models import CustomerProduct, Product


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
    """Limit the substitute results page to filter the results
    outputted based upon a substitute query

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
        self.id = self.kwargs["product_id"]
        self.product = Product.objects.get(pk=self.id)
        return self.product.substitutes()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.product.name
        context["image"] = self.product.image_url
        context["product"] = self.product
        return context


class ProductDetailsView(DetailView):
    """ProductDetailsView is designed to display product details data

    Args:
        DetailView (generic class-based views):  contain the object that the view is operating upon
    """

    model = Product
    template_name = "product/product_details.html"
    paginate_by = 6


@login_required
def save_view(request):
    """Function views to save the subsitute

    Args:
        request (object): an HttpRequest object

    Returns:
        redirect: Return an HttpResponseRedirect to the homepage URL
    """

    if request.method == "POST":
        product_id = request.POST["product_id"]
        substitute_id = request.POST["substitute_id"]
        page = request.POST["next"]
        _user = request.user
        if _user and product_id and substitute_id:
            obj, created = CustomerProduct.objects.get_or_create(
                customer=_user, product_id=product_id, substitute_id=substitute_id,
            )
            if created:
                messages.add_message(
                    request, messages.SUCCESS, "Le substitut a bien été sauvegardé !"
                )
            else:
                messages.add_message(
                    request, messages.INFO, "Le substitut est déja enregistré !"
                )
                return redirect(page)
    return redirect("favorites")


class FavoritesView(ListView, LoginRequiredMixin):
    """FavoritesView is designed to display favorite list data
    with a user authenticated

    Args:
        ListView (generic class-based views): render substitute list of objects
        LoginRequiredMixin (class): verify that the current user is authenticated
    """

    template_name = "product/favorites.html"
    paginate_by = 6

    def get_queryset(self):
        return CustomerProduct.objects.filter(customer=self.request.user.id).order_by(
            "product"
        )
