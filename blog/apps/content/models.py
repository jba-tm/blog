from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField


from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class ContentIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['content.ContentPage']
    max_count_per_parent = 1
    show_in_menus_default = True
    _all_entries = None
    _paginate = None

    # def get_context(self, request, *args, **kwargs):
    #     # Update context to include only published posts, ordered by reverse-chron
    #     context = super().get_context(request)
    #     content_pages = self.get_children().live().order_by('-first_published_at')
    #     context['content_pages'] = content_pages
    #     return context

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        self._all_entries = self.get_children().live().order_by('-first_published_at')

        self.paginate(request)
        # self._filter_tag(request)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context['content_pages'] = self._all_entries
        # context['posts'] = self._all_entries
        return context

    def paginate(self, request):
        # Paginate all posts by 2 per page
        paginator = Paginator(self._all_entries, 25)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            self._paginate = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            self._paginate = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            self._paginate = paginator.page(paginator.num_pages)

    class Meta:
        verbose_name = _('Content index page')


class ContentPage(Page):
    parent_page_types = ['content.ContentIndexPage']
    subpage_types = []

    body = RichTextField(verbose_name=_('Body'), help_text=_('Content body'), )

    category = ParentalKey('ContentCategory', null=True, on_delete=models.SET_NULL,
                           verbose_name=_('Category'), help_text=_('Content category'))

    tags = ClusterTaggableManager(through='ContentPageTag', blank=True)

    # categories = ParentalManyToManyField('ContentCategory', blank=True, verbose_name=_('Categories'),
    #                                      help_text=_('Content categories'))

    search_fields = Page.search_fields + [
        index.SearchField('body', partial_match=True),
        index.SearchField('tags', partial_match=True),
        index.RelatedFields('category', [
            index.SearchField('name', partial_match=True),
        ]),

        # index.RelatedFields('categories', [
        #     index.SearchField('name'),
        # ]),

    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            # FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('category'),
        ], heading=_('Content information'), help_text=_('Content base information')),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images", help_text=_('Content images')),
    ]

    api_fields = [
        APIField('last_published_at'),
        APIField('body'),
        APIField('category'),
        APIField('tags'),
        APIField('gallery_images'),
    ]

    class Meta:
        verbose_name_plural = _('Content pages')
        verbose_name = _('Content page')
        permissions = (
            ('import_content', _('Can import content')),
        )


class ContentPageTag(TaggedItemBase):
    content_object = ParentalKey(
        ContentPage,
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = _('Content page tags')
        verbose_name = _('Content page tag')


class ContentTagIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count_per_parent = 1

    def get_context(self, request, *args, **kwargs):
        # Filter by tag
        tag = request.GET.get('tag')
        content_pages = ContentPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['content_pages'] = content_pages
        return context

    class Meta:
        verbose_name = _('Content tag index page')


class ContentPageGalleryImage(Orderable):
    page = ParentalKey(ContentPage, null=True, blank=True, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.PROTECT, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

    api_fields = [
        APIField('page'),
        APIField('image'),
        APIField('caption'),
    ]


@register_snippet
class ContentCategory(ClusterableModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Content categories')
        verbose_name = _('Content category')
        ordering = ['name']
        default_permissions = ()
