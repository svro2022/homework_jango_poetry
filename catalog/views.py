from django.shortcuts import render
from catalog.models import Category, Product, Blog, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from catalog.forms import ProductForm, VersionForm
from django.forms import inlineformset_factory

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from catalog.cache_services import categories_cache

'''ФОРМА CATALOG'''

# FBV подход
# @login_required # скрывает контент от неавторизованных пользователей
# def index(request):
# '''контроллер главной страницы'''
# context = {
# 'object_list': Product.objects.all(),
# 'title': 'Онлайн магазин',
# 'title_text': 'Добро пожаловать! Выбираем нужную Вам категорию товаров.'
# }
# return render(request, 'catalog/index.html', context)


'''CBV подход'''

class MainListView(LoginRequiredMixin, ListView):
    '''Контролер главной страницы. Отображает все товары без категорий'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Product
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Онлайн магазин',
        'title_text': 'Добро пожаловать! Выбираем нужный товар.'
    }

    def get_queryset(self):
        '''Доступ для группы модераторов'''
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)

        return queryset


# FBV подход
# @login_required # скрывает контент от неавторизованных пользователей
# def categories(request):
# '''контроллер страницы всех категорий'''
# context = {
#   'object_list': Category.objects.all(),
#  'title': 'Онлайн магазин',
#   'title_text': 'Добро пожаловать! Выбираем нужную Вам категорию товаров.'

# }
# return render(request, 'catalog/categories.html', context)


'''CBV подход'''

class CategoriesListView(LoginRequiredMixin, ListView):
    '''Контроллер страницы Категории'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Category
    template_name = 'catalog/categories.html'
    extra_context = {
        'title': 'Онлайн магазин',
        'title_text': 'Добро пожаловать! Выбираем нужную Вам категорию товаров.'
    }


# FBV подход
# @login_required # скрывает контент от неавторизованных пользователей
# def category_products(request, pk):
# '''контроллер страницы всех товаров с категориями'''
# category_item = Category.objects.get(pk=pk)
# context = {
#    'object_list': Product.objects.filter(category_id=pk),
#    'title': f'Товары из {category_item.name}',
#    'title_text': 'Добро пожаловать! Выбираем нужный Вам товар.'

# }
# return render(request, 'catalog/products.html', context)


'''CBV подход'''

class CategoryProductsListView(LoginRequiredMixin, ListView):
    '''Контроллер страницы товаров в конкретной Категории'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Product
    template_name = 'catalog/products.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'Товары из {category_item.name}'
        context_data['title_text'] = f'Добро пожаловать! Выбираем нужный Вам товар.'

        return context_data



class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    '''CREATE - создается продукт (использование форм)'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    '''PermissionRequiredMixin - доступ для изменения контента, обязательное указание permission_required'''
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''кеш'''
        context_data = super().get_context_data(**kwargs)
        categories = categories_cache()
        context_data['categories'] = categories
        return context_data




# FBV подход
# @login_required # скрывает контент от неавторизованных пользователей
# def products(request):
# '''контроллер страницы всех товаров без категорий'''
# products_list = Product.objects.all()
# context = {
#    'object_list': products_list
# }
# return render(request, "catalog/products_all.html", context)



'''CBV подход'''

class ProductsListView(LoginRequiredMixin, ListView):
    '''READ - Контролер страницы Товары. Отображает все товары без категорий'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Product
    template_name = 'catalog/products_all.html'
    extra_context = {
        'title': 'Онлайн магазин',
        'title_text': 'Добро пожаловать! Ознакомьтесь с товарами.'
    }

    def get_context_data(self, object_list=None, **kwargs):
        '''кеш'''
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        categories = categories_cache()
        context_data['categories'] = categories

        return context_data


# FBV подход
# @login_required # скрывает контент от неавторизованных пользователей
# def product_detailed(request, pk):
# '''контроллер страницы одного товара'''
# category_item = Product.objects.get(pk=pk)
# context = {
#    'object_list': Product.objects.filter(pk=pk),
#    'title': f'Товар - {category_item.name}',
#    'title_text': 'Добро пожаловать! Выбираем нужный Вам товар.',
#    'name_card': category_item.name,
#    'price': category_item.price,
#    'description': category_item.description,
#    'data_added': category_item.data_create,
#    'data_edit': category_item.data_edit

# }
# return render(request, "catalog/product_detail.html", context)


'''CBV подход'''

class ProductDetailView(LoginRequiredMixin, DetailView):
    '''READ - Контроллер страницы одного товара'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''

    model = Product
    template_name = 'catalog/product_detail.html'
    extra_context = {
        'title': 'Онлайн магазин',
        'title_text': 'Добро пожаловать! Ознакомьтесь с товаром.'
    }

    def get_context_data(self, object_list=None, **kwargs):
        '''Кеширование списка категорий'''
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        categories = categories_cache()
        context_data['categories'] = categories

        return context_data


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    ''' UPDATE - обновление продукта (использование форм)'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    '''PermissionRequiredMixin - доступ для изменения контента, обязательное указание permission_required'''
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('Изменять может только владелец продукта')
        return self.object

    def get_success_url(self):
        return reverse('catalog:product_detailed', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        '''Формирование формсета'''
        context_data = super().get_context_data(**kwargs)

        '''кеш'''
        categories = categories_cache()
        context_data['categories'] = categories

        version_formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = version_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = version_formset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)



class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    '''DELETE - удаление продукта'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    '''PermissionRequiredMixin - доступ для изменения контента, обязательное указание permission_required'''
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'

    def get_context_data(self, object_list=None, **kwargs):
        '''кеш'''
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        categories = categories_cache()
        context_data['categories'] = categories

        return context_data



'''ФОРМА BLOG'''

class BlogCreateView(LoginRequiredMixin, CreateView):
    '''CREATE - создается запись'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    model = Blog
    fields = ('title', 'slug', 'body', 'preview', 'data_create', 'is_published', 'views_count',)
    success_url = reverse_lazy('catalog:blog_index')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    '''READ - чтение списка записей'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Blog
    template_name = 'catalog/blog_index.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    '''READ - чтение одной записи'''
    '''LoginRequiredMixin - скрывает контент от неавторизованных пользователей'''
    model = Blog
    success_url = reverse_lazy('catalog:blog_detail')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    '''UPDATE - обновление записи'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    model = Blog
    fields = ('title', 'slug', 'body', 'preview', 'data_create', 'is_published', 'views_count',)
    success_url = reverse_lazy('catalog:blog_index')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
            self.kwargs['slug'] = new_mat.slug

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    '''DELETE - удаление записи'''
    '''LoginRequiredMixin - скрывают контент от неавторизованных пользователей'''
    model = Blog
    success_url = reverse_lazy('catalog:blog_index')

