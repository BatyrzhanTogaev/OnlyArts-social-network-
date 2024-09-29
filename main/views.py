from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import ArtWork
from django.contrib.auth.decorators import login_required
from .forms import ArtWorkForm, CommentForm
from django.core.paginator import Paginator


class ArtWorkListView(ListView):
    model = ArtWork
    template_name = 'home.html'  # Шаблон для отображения работ
    context_object_name = 'artworks'
    paginate_by = 3  # Пагинация: 3 работ на страницу

    def get_queryset(self):
        queryset = ArtWork.objects.all()
        sort = self.request.GET.get('sort')
        if sort == 'likes':
            queryset = queryset.order_by('-likes')
        else:
            queryset = queryset.order_by('-created_at')
        return queryset


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        form = ArtWorkForm(request.POST, request.FILES)  # Не забудьте передать request.FILES
        if form.is_valid():
            artwork = form.save(commit=False)  # Не сохраняйте еще в базе данных
            artwork.author = request.user  # Установите автора
            artwork.save()  # Теперь сохраните объект, и created_at будет автоматически установлен
            return redirect('')  # Перенаправьте на нужную страницу
    else:
        form = ArtWorkForm()
    return render(request, 'upload_artwork.html', {'form': form})


class ArtWorkDetailView(DetailView):
    model = ArtWork
    template_name = 'artwork_detail.html'
    pk_url_kwarg = 'artwork_id'  # Указываем, что мы используем artwork_id вместо pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.object
        comments = artwork.comments.all().order_by('-created_at')

        # Пагинация комментариев
        paginator = Paginator(comments, 10)  # 10 комментариев на страницу
        page_number = self.request.GET.get('page')
        page_comments = paginator.get_page(page_number)

        context['comments'] = page_comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        artwork = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.artwork = artwork
            comment.author = request.user
            comment.save()
            return redirect('artwork_detail', artwork_id=artwork.id)  # Перенаправляем обратно на страницу работы

        return self.get(request, *args, **kwargs)
