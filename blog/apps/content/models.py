from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from taggit.models import TaggedItemBase
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from django.utils.translation import ugettext_lazy as _
from wagtail.snippets.models import register_snippet

# from blog import settings


class ContentIndexPage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['content.ContentPage']
    max_count_per_parent = 1
    show_in_menus_default = True

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
        all_posts = self.get_children().live().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 25)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            content_pages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            content_pages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            content_pages = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context['content_pages'] = content_pages
        context['posts'] = content_pages
        return context

    class Meta:
        verbose_name = _('Content index page')


class ContentPage(Page):
    parent_page_types = ['content.ContentIndexPage']
    subpage_types = []

    body = RichTextField(verbose_name=_('Body'), help_text=_('Content body'),)
    content_datetime = models.DateTimeField(null=True, verbose_name=_('Content datetime'),
                                            help_text=_('Content datetime'))

    direction = ParentalKey('ContentDirection', null=True, on_delete=models.SET_NULL,
                            verbose_name=_('Direction'), help_text=_('Content direction'))

    type = ParentalKey('ContentType', null=True, on_delete=models.SET_NULL, verbose_name=_('Type'),
                       help_text=_('Content type'))

    importance = ParentalKey('ContentImportance', null=True, on_delete=models.SET_NULL,
                             verbose_name=_('Importance'), help_text=_('Content importance'))

    tags = ClusterTaggableManager(through='ContentPageTag', blank=True)

    categories = ParentalManyToManyField('ContentCategory', blank=True, verbose_name=_('Categories'),
                                         help_text=_('Content categories'))

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('tags'),
        index.RelatedFields('direction', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('type', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('importance', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('importance', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('categories', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('type', [
            index.SearchField('name'),
        ]),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('content_datetime'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading=_('Content information'), help_text=_('Content base information')),
        MultiFieldPanel([
            FieldPanel('direction'),
            FieldPanel('type'),
            FieldPanel('importance'),
        ], heading=_('Content advance information'), help_text=_('Content advance information')),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images", help_text=_('Content images')),
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


@register_snippet
class ContentCategory(models.Model):
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


@register_snippet
class ContentDirection(ClusterableModel):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Content directions')
        verbose_name = _('Content direction')
        ordering = ['name']
        default_permissions = ()


@register_snippet
class ContentImportance(ClusterableModel):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Content importances')
        verbose_name = _('Content importance')
        ordering = ['name']
        default_permissions = ()


@register_snippet
class ContentType(ClusterableModel):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Content types')
        verbose_name = _('Content type')
        ordering = ['name']
        default_permissions = ()
