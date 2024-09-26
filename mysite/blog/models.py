from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField

# New imports added for ClusterTaggableManager, TaggedItemBase
# 要將 ClusterTaggableManager, TaggedItemBase 加進來
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtail.api import APIField
from django.utils import timezone


# 加上 BlogPageTag 系統
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage", related_name="tagged_items", on_delete=models.CASCADE)


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    content_panels = Page.content_panels + [FieldPanel("intro")]


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField("blog.Author", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    feed_image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, related_name="+")
    private_field = models.CharField(max_length=255, default="Default private value")

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                FieldPanel("tags"),
            ],
            heading="Blog information",
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("published_date"),
        FieldPanel("feed_image"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]

    api_fields = [
        APIField("published_date"),
        APIField("body"),
        APIField("feed_image"),
        APIField("authors"),  # 這將在 API 回應中嵌套相關的 BlogPageAuthor 物件
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(blank=True, max_length=250)
    private_field = models.CharField(max_length=255, default="Default private value")

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)

    api_fields = [
        APIField("name"),
    ]

    author_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("author_image"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


class BlogTagIndexPage(Page):
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context
