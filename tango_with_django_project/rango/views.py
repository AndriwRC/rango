from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm


def index(request):
    # set up the context dictionary with our bold message
    context_dict = {"aboldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}

    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    # Place the list in our context_dict dictionary (with our aboldmessage!)
    # that will be passed to the template engine.
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list
    # Render the response and send it back

    return render(request, "rango/index.html", context=context_dict)


def about(request):
    return render(request, "rango/about.html")


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict["pages"] = pages
        # We also add teh category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict["category"] = None
        context_dict["pages"] = None

        # Go render the response and return it to the client.
    return render(request, "rango/category.html", context=context_dict)


def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == "POST":
        form = CategoryForm(request.POST)
        # Have we been provided with a valid fom?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect("/rango/")
        else:
            # The supplied from contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, "rango/add_category.html", {"form": form})
