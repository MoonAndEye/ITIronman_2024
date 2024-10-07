from wagtail.blocks import (
    CharBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
)

from wagtail.images.blocks import ImageChooserBlock
from base.blocks import BaseStreamBlock


# add CardBlock:
# 加上 卡片型 block
class CardBlock(StructBlock):
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"])
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"


# add FeaturedPostsBlock:
# 加上 特色文章 block
class FeaturedPostsBlock(StructBlock):
    heading = CharBlock()
    text = RichTextBlock(features=["bold", "italic", "link"], required=False)
    posts = ListBlock(PageChooserBlock(page_type="blog.BlogPage"))

    class Meta:
        icon = "folder-open-inverse"
        template = "portfolio/blocks/featured_posts_block.html"


class PortfolioStreamBlock(BaseStreamBlock):
    # delete the pass statement
    # 請把之前的 pass 刪除掉

    card = CardBlock(group="Sections")
    featured_posts = FeaturedPostsBlock(group="Sections")
