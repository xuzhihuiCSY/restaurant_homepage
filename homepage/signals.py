from django.core.files.storage import default_storage
from django.db.models import Q
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import DailyRecommendation, Event, RestaurantPhoto, RestaurantProfile


MODEL_FILE_FIELDS = {
    RestaurantProfile: [
        "logo",
        "hero_image",
        "reviews_background_image",
        "online_order_image_left",
        "online_order_image_right",
        "group_reservation_background_image",
    ],
    DailyRecommendation: ["image"],
    RestaurantPhoto: ["image"],
    Event: ["cover_image"],
}


def _file_name(instance, field_name):
    field_file = getattr(instance, field_name)
    return field_file.name if field_file else ""


def _instance_file_names(instance):
    return {
        name
        for field_name in MODEL_FILE_FIELDS[type(instance)]
        if (name := _file_name(instance, field_name))
    }


def _file_is_referenced(file_name):
    for model, field_names in MODEL_FILE_FIELDS.items():
        query = Q()
        for field_name in field_names:
            query |= Q(**{field_name: file_name})
        if query and model.objects.filter(query).exists():
            return True
    return False


def _delete_unreferenced_files(file_names):
    for file_name in file_names:
        if _file_is_referenced(file_name):
            continue
        default_storage.delete(file_name)


@receiver(pre_save, dispatch_uid="homepage_remember_replaced_files")
def remember_replaced_files(sender, instance, **kwargs):
    if sender not in MODEL_FILE_FIELDS or not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_files = _instance_file_names(old_instance)
    new_files = _instance_file_names(instance)
    instance._replaced_file_names = old_files - new_files


@receiver(post_save, dispatch_uid="homepage_delete_replaced_files")
def delete_replaced_files(sender, instance, **kwargs):
    if sender not in MODEL_FILE_FIELDS:
        return

    file_names = getattr(instance, "_replaced_file_names", set())
    if file_names:
        _delete_unreferenced_files(file_names)
        instance._replaced_file_names = set()


@receiver(post_delete, dispatch_uid="homepage_delete_instance_files")
def delete_instance_files(sender, instance, **kwargs):
    if sender not in MODEL_FILE_FIELDS:
        return

    _delete_unreferenced_files(_instance_file_names(instance))
