from django.views import generic
from django.shortcuts import render, get_object_or_404
from .models import Gallery, GalleryImage
from .forms import CommentForm


class GalleryList(generic.ListView):
    queryset = Gallery.objects.order_by('-created_on')
    template_name = 'gallery/gallery_list.html'
    paginate_by = 10


def gallery_detail(request, slug):
    template_name = 'gallery/gallery_detail.html'
    gallery = get_object_or_404(Gallery, slug=slug)
    photos = gallery.images.all()
    comments = gallery.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.gallery = gallery
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'gallery': gallery,
        'photos': photos,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })
