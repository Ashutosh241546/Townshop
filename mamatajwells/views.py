from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Jewellery

@login_required
def jwells_home(request):
    featured = Jewellery.objects.all()[:5]
    return render(request, 'main.html', {'featured': featured})
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


