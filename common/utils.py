from django.utils.text import slugify


def generate_slug(text):
    """
    Generate a URL-friendly slug.
    """
    return slugify(text)