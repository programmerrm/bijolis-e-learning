from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.utils import GENERATE_SLUG
from accounts.services.user_id import GENERATE_USER_ID

User = get_user_model()

# === PRE SAVE: Generate user_id and slug ===
@receiver(pre_save, sender=User)
def populate_user_fields(sender, instance, **kwargs):
    # Auto-generate user_id if not present
    if not instance.user_id:
        instance.user_id = GENERATE_USER_ID(instance.role)
    
    # Auto-generate or update slug if username changed
    if not instance.slug:
        instance.slug = GENERATE_SLUG(instance.username)
    elif instance.pk:
        # Check if username has changed
        original = User.objects.filter(pk=instance.pk).only("username").first()
        if original and instance.username != original.username:
            instance.slug = GENERATE_SLUG(instance.username)

# === POST DELETE: Delete user image from storage ===
@receiver(post_delete, sender=User)
def delete_user_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
