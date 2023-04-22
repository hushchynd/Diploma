from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DeleteView

from admin_panel import forms as my_forms
from admin_panel.tasks import send_email
from kino_app.views import is_ajax
from user import forms as user_forms
from django.forms import inlineformset_factory, modelformset_factory
# Create your views here.
from admin_panel.models import *
from datetime import date, timedelta


@login_required
@staff_member_required
def example(request):
    return render(request, 'admin_panel/example.html')


@login_required
@staff_member_required
def statistic(request):
    data = {'users_count': Account.objects.count()}
    return render(request, 'admin_panel/statistic.html', context=data)


@login_required
@staff_member_required
def clients(request):
    data = {'users': Account.objects.all()}
    return render(request, 'admin_panel/clients.html', context=data)


@login_required
@staff_member_required
def update_client(request, id):
    client = Account.objects.get(id=id)
    if request.method == 'POST':
        client_form = user_forms.AdminUserForm(request.POST, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect('clients')
        else:
            data = {'client_form': client_form, 'client_id': id}
            return render(request, 'admin_panel/update_client.html', context=data)
    client_form = user_forms.AdminUserForm(instance=client, )
    data = {'client_form': client_form, 'client_id': id}
    return render(request, 'admin_panel/update_client.html', context=data)


@login_required
@staff_member_required
def delete_client(request, id):
    return render(request, 'admin_panel/clients.html', )


@login_required
@staff_member_required
def films(request):
    start_date = date.today()
    released_films = Film.objects.filter(released__lte=start_date)
    unreleased_films = Film.objects.filter(released__gte=start_date)
    data = {
        'films': {
            'released_films': released_films,
            'unreleased_films': unreleased_films,
        },
        'title': 'Фильмы'
    }
    if request.method == 'POST':
        filmImgForm = my_forms.FilmImgForm(request.POST, request.FILES)
        film_form = my_forms.FilmForm(request.POST, request.FILES)
        seo_block = my_forms.SeoBlockForm(request.POST)

        if seo_block.is_valid() and film_form.is_valid() and filmImgForm.is_valid():
            seo_obj = seo_block.save()
            film_obj = film_form.save()
            film_obj.seo_block_id = seo_obj.id
            film_obj.save()
            for file in request.FILES.getlist('img'):
                FilmImg.objects.create(img=file, film_id=film_obj.id)

        else:
            data = {
                'seo_form': seo_block,
                'form': film_form,
                'filmImg_form': filmImgForm,
            }
            return render(request, 'admin_panel/film_form.html', context=data)

    return render(request, 'admin_panel/films2.html', context=data)


@login_required
@staff_member_required
def cinemas(request):
    if request.method == "POST":
        hall_form = my_forms.HallForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        hall_gallery_form = my_forms.HallImgForm(request.POST, request.FILES)
        if seo_form.is_valid() and hall_form.is_valid() and hall_gallery_form.is_valid():
            seo_obj = seo_form.save()
            hall_obj = hall_form.save()
            hall_obj.seo_block_id = seo_obj.id
            hall_obj.cinema_id = 1
            hall_obj.save()
            for file in request.FILES.getlist('img'):
                if file:
                    HallImg.objects.create(img=file, hall_id=hall_obj.id)
        else:
            data = {'hall_form': hall_form, 'hallImgs_form': hall_gallery_form, 'seo_form': seo_form}
            return render(request, 'admin_panel/hall_form.html', context=data)

    cinemas = Cinema.objects.all()
    data = {'cinemas': cinemas}
    return render(request, 'admin_panel/cinemas.html', context=data)


@login_required
@staff_member_required
def choose_client(request):
    users = Account.objects.all()
    data = {
        'users': users
    }
    return render(request, 'admin_panel/choose_client.html', context=data)


@login_required
@staff_member_required
def mailing(request):
    clients_filter = request.GET.getlist('clients_filter')
    if clients_filter:
        users = Account.objects.filter(id__in=clients_filter)
    else:
        users = Account.objects.all()

    if request.method == 'POST':
        templates_filter = request.POST.getlist('templates_filter')
        if templates_filter:
            obj = TemplateHtml.objects.get(id__in=templates_filter)
        else:
            form = my_forms.TemplateHtmlForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save()
            else:
                templates_html = TemplateHtml.objects.all()[:5]
                data = {
                    'file_form': form,
                    'templates_html': templates_html,
                }
                return render(request, 'admin_panel/mailing.html', context=data)

        with open(f'media/{obj.template_html}', 'r') as file:
            html_content = file.read()
        to = []
        for i in users:
            to.append(i.email)

        task = send_email.delay(html_content, to)

    templates_html = TemplateHtml.objects.all()[:5]
    file_form = my_forms.TemplateHtmlForm()
    data = {
        'file_form': file_form,
        'templates_html': templates_html,
    }
    return render(request, 'admin_panel/mailing.html', context=data)


@login_required
@staff_member_required
def deleteHtmlTemplate(request, id):
    templates_html = TemplateHtml.objects.get(id=id)
    templates_html.delete()
    return redirect('mailing')


@login_required
@staff_member_required
def stocks(request):
    if request.method == "POST":
        stock_form = my_forms.StockForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        gallery_stock_form = my_forms.StockImgForm(request.POST, request.FILES)
        if seo_form.is_valid() and stock_form.is_valid() and gallery_stock_form.is_valid():
            seo_obj = seo_form.save()
            stock_obj = stock_form.save()
            stock_obj.seo_block_id = seo_obj.id
            stock_obj.save()
            for file in request.FILES.getlist('img'):
                if file:
                    StockImg.objects.create(img=file, stock_id=stock_obj.id)
        else:
            data = {'stock_form': stock_form, 'stockImgs_form': gallery_stock_form, 'seo_form': seo_form}
            return render(request, 'admin_panel/stock_form.html', context=data)

    stocks = Stock.objects.all()
    data = {'stocks': stocks}
    return render(request, 'admin_panel/stocks2.html', context=data)


@login_required
@staff_member_required
def get_stock_form(request):
    stockImgs_form = my_forms.StockImgForm()
    stock_form = my_forms.StockForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'stock_form': stock_form, 'stockImgs_form': stockImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/stock_form.html', context=data)


@login_required
@staff_member_required
def update_stock(request, id):
    stock = Stock.objects.get(id=id)
    if request.method == 'POST':
        stock_form = my_forms.StockForm(request.POST, request.FILES, instance=stock)
        seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if stock_form.is_valid() and seo_form.is_valid():
            stock_form.save()
            seo_form.save()
            return redirect('stocks_table')
        else:

            data = {'stock_form': stock_form, 'stock_id': stock.id, 'seo_form': seo_form}
            return render(request, 'admin_panel/stock_update2.html', context=data)

    stock_form = my_forms.StockForm(instance=stock)
    seo_obj = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'stock_form': stock_form, 'stock_id': stock.id, 'seo_form': seo_form}
    return render(request, 'admin_panel/stock_update2.html', context=data)


@login_required
@staff_member_required
def delete_stock(request, id):
    stock = Stock.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=stock.seo_block.id)
    seo_block.delete()
    stock.delete()

    return redirect('stocks_table')


@login_required
@staff_member_required
def news(request):
    if request.method == "POST":
        news_form = my_forms.NewsForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        gallery_news_form = my_forms.NewsImgForm(request.POST, request.FILES)
        if seo_form.is_valid() and news_form.is_valid() and gallery_news_form.is_valid():
            seo_obj = seo_form.save()
            news_obj = news_form.save()
            news_obj.seo_block_id = seo_obj.id
            news_obj.save()
            for file in request.FILES.getlist('img'):
                if file:
                    NewsImg.objects.create(img=file, news_id=news_obj.id)
        else:
            data = {'news_form': news_form, 'newsImgs_form': gallery_news_form, 'seo_form': seo_form}
            return render(request, 'admin_panel/news_form.html', context=data)

    news_list = News.objects.all()
    data = {'news_list': news_list}
    return render(request, 'admin_panel/news2.html', context=data)


@login_required
@staff_member_required
def get_news_form(request):
    newsImgs_form = my_forms.NewsImgForm()
    news_form = my_forms.NewsForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'news_form': news_form, 'newsImgs_form': newsImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/news_form.html', context=data)


@login_required
@staff_member_required
def update_news(request, id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        news_form = my_forms.NewsForm(request.POST, request.FILES, instance=news)
        seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if news_form.is_valid() and seo_form.is_valid():
            news_form.save()
            seo_form.save()
            return redirect('news_table')
        data = {'news_form': news_form, 'news_id': news.id, 'seo_form': seo_form}
        return render(request, 'admin_panel/news_update2.html', context=data)

    news_form = my_forms.NewsForm(instance=news)
    seo_obj = SeoBlock.objects.get(id=news.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'news_form': news_form, 'news_id': news.id, 'seo_form': seo_form}
    return render(request, 'admin_panel/news_update2.html', context=data)


@login_required
@staff_member_required
def delete_news(request, id):
    news = News.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=news.seo_block.id)
    seo_block.delete()
    news.delete()

    return redirect('news_table')


# def get_film_form(request):
#     filmImgForm = my_forms.FilmImgForm()
#
#     film_form = my_forms.FilmForm()
#     seo = my_forms.SeoBlockForm()
#     data = {'form': film_form, 'filmImg_form': filmImgForm, 'seo_form': seo}
#     return render(request, 'admin_panel/film_form.html', context=data)

@method_decorator([login_required, staff_member_required], name='dispatch')
class FilmForm(FormView):
    initial = {'name': 'Film name'}
    template_name = 'admin_panel/film_form.html'
    form_class = my_forms.FilmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo = my_forms.SeoBlockForm()
        context['seo_form'] = seo
        filmImgForm = my_forms.FilmImgForm()
        context['filmImg_form'] = filmImgForm
        return context

    def get_success_url(self):
        return redirect('films')


@login_required
@staff_member_required
def cinema_card(request, name):
    cinema = Cinema.objects.get(name=name)
    if request.method == 'POST':
        cinema_form = my_forms.CinemaForm(request.POST, request.FILES, instance=cinema)
        seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if cinema_form.is_valid() and seo_form.is_valid():
            cinema_form.save()
            seo_form.save()
            return redirect('admin_cinemas')
        else:
            halls = Hall.objects.filter(cinema_id=cinema.id)

            data = {'form': cinema_form, 'cinema_name': cinema.name, 'seo_form': seo_form, 'halls': halls}
            return render(request, 'admin_panel/cinema_update.html', context=data)

    seo_obj = SeoBlock.objects.get(id=cinema.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    halls = Hall.objects.filter(cinema_id=cinema.id)
    cinema_form = my_forms.CinemaForm(instance=cinema)
    data = {'form': cinema_form, 'cinema_name': cinema.name, 'seo_form': seo_form, 'halls': halls}
    return render(request, 'admin_panel/cinema_update.html', context=data)


@login_required
@staff_member_required
def get_hall_form(request):
    hallImgs_form = my_forms.HallImgForm()
    hall_form = my_forms.HallForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'hall_form': hall_form, 'hallImgs_form': hallImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/hall_form.html', context=data)


@login_required
@staff_member_required
def banners_sliders(request):
    TopCarouselFormset = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormset(queryset=TopCarousel.objects.all(), prefix='top_carousel')

    BottomCarouselFormset = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormset(queryset=BottomCarousel.objects.all(), prefix='bottom_carousel')

    interval = my_forms.FormInterval()

    back_img_form = my_forms.BackImgForm()
    data = {

        'top_carousel_formset': top_carousel_formset,
        'bottom_carousel_formset': bottom_carousel_formset,
        'back_img_form': back_img_form,
        'interval': interval,
    }
    return render(request, 'admin_panel/banners_sliders2.html', context=data)


@login_required
@staff_member_required
def top_carousel(request):
    TopCarouselFormSet = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormSet(request.POST, request.FILES, prefix='top_carousel')

    BottomCarouselFormset = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormset(queryset=BottomCarousel.objects.all(), prefix='bottom_carousel')

    interval = my_forms.FormInterval(request.POST)

    back_img_form = my_forms.BackImgForm()
    if top_carousel_formset.is_valid() and interval.is_valid():
        TopCarousel.interval = interval.cleaned_data['interval']
        top_carousel_formset.save()
    else:
        data = {
            'top_carousel_formset': top_carousel_formset,
            'bottom_carousel_formset': bottom_carousel_formset,
            'back_img_form': back_img_form,
            'interval': interval,
        }
        return render(request, 'admin_panel/banners_sliders2.html', context=data)

    return redirect('banners_sliders')


@login_required
@staff_member_required
def bottom_carousel(request):
    BottomCarouselFormSet = modelformset_factory(BottomCarousel, form=my_forms.BottomCarouselForm, extra=0,
                                                 can_delete=True)
    bottom_carousel_formset = BottomCarouselFormSet(request.POST, request.FILES, prefix='bottom_carousel')

    TopCarouselFormset = modelformset_factory(TopCarousel, form=my_forms.TopCarouselForm, extra=0, can_delete=True)
    top_carousel_formset = TopCarouselFormset(queryset=TopCarousel.objects.all(), prefix='top_carousel')

    interval = my_forms.FormInterval(request.POST)
    back_img_form = my_forms.BackImgForm()

    if bottom_carousel_formset.is_valid() and interval.is_valid():
        BottomCarousel.interval = interval.cleaned_data['interval']
        bottom_carousel_formset.save()

    else:
        data = {
            'top_carousel_formset': top_carousel_formset,
            'bottom_carousel_formset': bottom_carousel_formset,
            'back_img_form': back_img_form,
            'interval': interval,
        }
        return render(request, 'admin_panel/banners_sliders2.html', context=data)

    return redirect('banners_sliders')


@login_required
@staff_member_required
def back_img(request):
    back_img_form = my_forms.BackImgForm(request.POST, request.FILES)
    if back_img_form.is_valid():
        BackImg.objects.all().delete()
        back_img_form.save()

    return redirect('banners_sliders')


@login_required
@staff_member_required
def pages(request):
    if request.method == "POST":
        page_form = my_forms.PageForm(request.POST, request.FILES)
        seo_form = my_forms.SeoBlockForm(request.POST)
        pageImgForm = my_forms.PageImgForm(request.POST, request.FILES)

        if seo_form.is_valid() and page_form.is_valid() and pageImgForm.is_valid():
            seo_obj = seo_form.save()
            page_obj = page_form.save()
            page_obj.seo_block_id = seo_obj.id
            page_obj.save()
            for file in request.FILES.getlist('img'):
                if file:
                    PageImg.objects.create(img=file, page_id=page_obj.id)
        else:
            data = {'page_form': page_form, 'pageImgs_form': pageImgForm, 'seo_form': seo_form}
            return render(request, 'admin_panel/page_form.html', context=data)

    page_list = Page.objects.order_by('creation_date')
    data = {'page_list': page_list}
    return render(request, 'admin_panel/pages2.html', context=data)


@login_required
@staff_member_required
def get_page_form(request):
    pageImgs_form = my_forms.PageImgForm()
    page_form = my_forms.PageForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'page_form': page_form, 'pageImgs_form': pageImgs_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/page_form.html', context=data)


@login_required
@staff_member_required
def update_page(request, id):
    menuFormset = modelformset_factory(can_delete=True, model=CafeBarMenu, form=my_forms.CafeBarMenuForm, extra=0)

    page = Page.objects.get(id=id)

    if request.method == 'POST':
        if page.name == 'Кафе-Бар':
            menu_formset = menuFormset(request.POST)
            page_form = my_forms.PageUpdateForm(request.POST, request.FILES, instance=page)
            seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
            seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
            if menu_formset.is_valid() and page_form.is_valid() and seo_form.is_valid():
                menu_formset.save()
                page_form.save()
                seo_form.save()
                return redirect('pages')
            else:
                data = {
                    'page_form': page_form,
                    'page_id': page.id,
                    'seo_form': seo_form,
                    'menu_formset': menu_formset,
                    'labels': my_forms.CafeBarMenuForm
                        }
                return render(request, 'admin_panel/update_cafe-bar.html', context=data)

        page_form = my_forms.PageUpdateForm(request.POST, request.FILES, instance=page)
        seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if page_form.is_valid() and seo_form.is_valid():
            page_form.save()
            seo_form.save()
            return redirect('pages')
        else:
            data = {'page_form': page_form, 'page_id': page.id, 'seo_form': seo_form}
            return render(request, 'admin_panel/page_update2.html', context=data)

    page_form = my_forms.PageUpdateForm(instance=page)
    seo_obj = SeoBlock.objects.get(id=page.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)

    data = {'page_form': page_form, 'page_id': page.id, 'seo_form': seo_form}
    if page.name == 'Кафе-Бар':
        menu_formset = menuFormset(queryset=CafeBarMenu.objects.all())
        data['menu_formset'] = menu_formset
        data['labels'] = my_forms.CafeBarMenuForm
        return render(request, 'admin_panel/update_cafe-bar.html', context=data)
    return render(request, 'admin_panel/page_update2.html', context=data)


@login_required
@staff_member_required
def delete_page(request, id):
    page = Page.objects.get(id=id)
    seo_block = SeoBlock.objects.get(id=page.seo_block.id)
    seo_block.delete()
    page.delete()

    return redirect('pages')


@login_required
@staff_member_required
def update_film(request, name):
    film = Film.objects.get(name=name)
    if request.method == 'POST':

        film_form = my_forms.FilmForm(request.POST, request.FILES, instance=film)
        seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if film_form.is_valid() and seo_form.is_valid():
            film_form.save()
            seo_form.save()
            return redirect('films')
        else:
            data = {'form': film_form, 'film_name': film.name, 'seo_form': seo_form}
            return render(request, 'admin_panel/film_update.html', context=data)

    film_form = my_forms.FilmForm(instance=film)
    film_form.fields['banner'].src = film.banner
    seo_obj = SeoBlock.objects.get(id=film.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'form': film_form, 'film_name': film.name, 'seo_form': seo_form}
    return render(request, 'admin_panel/film_update.html', context=data)


@login_required
@staff_member_required
def update_hall(request, number):
    hall = Hall.objects.get(number=number)
    if request.method == 'POST':

        hall_form = my_forms.HallForm(request.POST, request.FILES, instance=hall)
        seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if hall_form.is_valid() and seo_form.is_valid():
            hall_form.save()
            seo_form.save()
            return redirect('admin_cinemas')
        else:
            data = {'hall_form': hall_form, 'hall_number': hall.number, 'seo_form': seo_form}
            return render(request, 'admin_panel/hall_update2.html', context=data)

    hall_form = my_forms.HallForm(instance=hall)
    seo_obj = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'hall_form': hall_form, 'hall_number': hall.number, 'seo_form': seo_form}
    return render(request, 'admin_panel/hall_update2.html', context=data)


@login_required
@staff_member_required
def delete_hall(request, number):
    hall = Hall.objects.get(number=number)
    seo_block = SeoBlock.objects.get(id=hall.seo_block.id)
    seo_block.delete()
    hall.delete()

    return redirect('admin_cinemas')


@login_required
@staff_member_required
def update_main_page(request):

    main_page_obj = MainPage.objects.first()

    if request.method == 'POST':

        main_page_form = my_forms.MainPageForm(request.POST, instance=main_page_obj)
        seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
        seo_form = my_forms.SeoBlockForm(request.POST, instance=seo_obj)
        if main_page_form.is_valid() and seo_form.is_valid():
            seo_form.save()
            main_page_form.save()
            return redirect('pages')
        else:
            data = {'main_page_form': main_page_form, 'seo_form': seo_form}
            return render(request, 'admin_panel/main_page.html', context=data)

    main_page_form = my_forms.MainPageForm(instance=main_page_obj)
    seo_obj = SeoBlock.objects.get(id=main_page_obj.seo_block.id)
    seo_form = my_forms.SeoBlockForm(instance=seo_obj)
    data = {'main_page_form': main_page_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/main_page.html', context=data)


@login_required
@staff_member_required
def update_contacts(request):
    contactFormset = modelformset_factory(can_delete=True, model=Contact, form=my_forms.ContactForm, extra=0)
    if request.method == 'POST':
        contacts_formset = contactFormset(request.POST, request.FILES)
        if contacts_formset.is_valid():
            contacts_formset.save()
            redirect("pages")
        else:
            data = {'contacts_formset': contacts_formset}
            return render(request, 'admin_panel/update_contacts.html', context=data)
    contacts_formset = contactFormset(queryset=Contact.objects.all())
    data = {'contacts_formset': contacts_formset}
    return render(request, 'admin_panel/update_contacts.html', context=data)


@login_required
@staff_member_required
def seances(request):
    template = '../templates/admin_panel/seances.html'
    seances = Seance.objects.all()
    if is_ajax(request):
        template = '../templates/admin_panel/seances_items.html'
        date_filter = request.GET.get('period')
        halls_filter = request.GET.getlist('halls_filter')
        films_filter = request.GET.getlist('films_filter')
        techs_filter = request.GET.getlist('techs_filter')
        if date_filter:
            seances = seances.filter(date=date_filter)
        if halls_filter:
            seances = seances.filter(hall__number__in=halls_filter)
        if films_filter:
            seances = seances.filter(film_id__in=films_filter)
        if techs_filter:
            seances = seances.filter(tech_type__name__in=techs_filter)

    result = []
    for film_seance in seances.distinct('film_id'):
        film_seances = seances.filter(film_id=film_seance.film_id)
        date_film = []

        for date_seance in film_seances.distinct('date'):
            date_seances = film_seances.filter(date=date_seance.date)
            hall_film = []

            for hall_seance in date_seances.distinct('hall'):
                hall_seances = date_seances.filter(hall=hall_seance.hall)
                tech_film = []

                for tech_seance in hall_seances.distinct('tech_type'):
                    tech_seances = hall_seances.filter(tech_type=tech_seance.tech_type)
                    tech_film.append((tech_seance.tech_type.name, tech_seances))

                hall_film.append((hall_seance.hall, tech_film))

            date_film.append((date_seance.date, hall_film))
        result.append((film_seance.film, date_film))

    film_list = []
    today_date = date.today()
    for film in Film.objects.filter(released__lt=today_date).order_by('name'):
        film_list.append(('unchecked', film))
    tech_list = []
    for tech in TechnologyType.objects.order_by('name'):
        tech_list.append(('unchecked', tech))

    hall_list = []
    for hall in Hall.objects.order_by('number'):
        hall_list.append(('unchecked', hall))

    data = {
        "result": result,
        'hall_list': hall_list,
        'film_list': film_list,
        "tech_list": tech_list,
    }
    return render(request, template, context=data)


@login_required
@staff_member_required
def get_seance_form(request):
    if request.method == 'POST':
        seance_form = my_forms.SeanceForm(request.POST)
        if seance_form.is_valid():
            seance_form.save()
            return redirect('seances')
        else:
            data = {'seance_form': seance_form, }
            return render(request, 'admin_panel/seance_form.html', context=data)

    seance_form = my_forms.SeanceForm()
    seo_form = my_forms.SeoBlockForm()

    data = {'seance_form': seance_form, 'seo_form': seo_form}
    return render(request, 'admin_panel/seance_form.html', context=data)


@login_required
@staff_member_required
def delete_seance(request, id):
    tickets = Ticket.objects.filter(seance_id=id)
    for ticket in tickets:
        ticket.delete()
    Seance.objects.get(id=id).delete()
    return redirect('seances')
