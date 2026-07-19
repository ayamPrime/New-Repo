from django.db import models

class LegalDocument(models.Model):
    DOC_CHOICES = [
        ('terms', 'Terms of Service'),
        ('privacy', 'Privacy Policy'),
        ('escrow_refund', 'Escrow and Refund Policy'),
        ('lister_onboarding', 'Lister Onboarding Agreement'),
    ]
    doc_type = models.CharField(max_length=30, choices=DOC_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # terms, privacy, escrow-refund, lister-onboarding
    version = models.CharField(max_length=20, default='1.0')
    content = models.TextField(help_text="Paste plain text. Leave a blank line between paragraphs.")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (v{self.version})"