from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Jewellery,Category,SubCategory

@login_required
# def jwells_home(request):
#     featured = Jewellery.objects.all()[:5]
#     return render(request, 'main.html', {'featured': featured})
def jwells_home(request):

    # Only Mamata Jwells categories
    categories = Category.objects.filter(type="jwells")

    # Read filter values
    selected_category = request.GET.get("category")
    selected_subcategory = request.GET.get("subcategory")

    # Load subcategories
    if selected_category:
        subcategories = SubCategory.objects.filter(category_id=selected_category)
    else:
        subcategories = SubCategory.objects.filter(category__type="jwells")

    # Featured = only 5 items (same as your old code)
    featured = Jewellery.objects.all()

    # Apply filters
    if selected_category:
        featured = featured.filter(category_id=selected_category)

    if selected_subcategory:
        featured = featured.filter(subcategory_id=selected_subcategory)

    # Limit to 5 items (your original code logic)
    featured = featured[:5]

    return render(request, "main.html", {
        "categories": categories,
        "subcategories": subcategories,
        "featured": featured,
    })

@login_required
def jewellery_list(request):
    q = request.GET.get('q')
    if q:
        items = Jewellery.objects.filter(name__icontains=q)
    else:
        items = Jewellery.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'items': items, 'query': q})

@login_required
def jewellery_detail(request, pk):
    # Get the current item
    item = get_object_or_404(Jewellery, pk=pk)
    
    # Get all other items to show in "You may also like"
    featured = Jewellery.objects.exclude(id=pk)
    
    return render(request, 'detail.html', {
        'item': item,
        'featured': featured
    })


