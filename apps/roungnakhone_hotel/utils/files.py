from django.core.exceptions import ValidationError
from django.core.files import File
from PIL import Image
from io import BytesIO

from dj_roungnakhone_hotel.settings.common import FILE_UPLOAD_MAX_MEMORY_SIZE

import os


def validate_image_extension(image):
    allowed_extensions = ['jpeg', 'jpg', 'png', 'gif']
    extension = image.name.split('.')[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError(
            "Invalid image format. Please upload a valid image file (JPG, JPEG, PNG, GIF)."
        )


# Calculate the maximum file size in bytes
# 2.5 MB (2.5 * 1024 * 1024 bytes)
def max_file_size_validator(value):
    max_size_byte = FILE_UPLOAD_MAX_MEMORY_SIZE
    max_size_mb = max_size_byte / (1024**2)

    # print('Greater or Not:', value.size > max_size_byte)
    # print('max_size_mb:', value.size / (1024**2))

    if value.size > max_size_byte:
        raise ValidationError(f'File size cannot exceed {max_size_mb} MB.')


def receptionist_storage(instance, filename):
    # Modify the file name as needed
    receptionist_id = instance.id
    if receptionist_id is None:
        # If the receptionist is new and doesn't have an ID yet, use a temporary identifier
        receptionist_id = "new"
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'receptionist_{receptionist_id}_profile.{ext}'  # Customize the new file name
    return os.path.join('receptionist_profiles/', new_filename)


def guest_storage(instance, filename):
    # Modify the file name as needed
    guest_id = instance.id
    if guest_id is None:
        # If the guest is new and doesn't have an ID yet, use a temporary identifier
        guest_id = "new"
    ext = filename.split('.')[-1]  # Get the file extension
    new_filename = f'guest_{guest_id}_profile.{ext}'  # Customize the new file name
    return os.path.join('guest_profiles/', new_filename)


def room_storage(instance, filename):
    room_id = instance.id
    if room_id is None:
        room_id = "new"
    ext = filename.split('.')[-1]
    new_filename = f'room_{room_id}_image.{ext}'
    return os.path.join('room_images/', new_filename)


def payment_storage(instance, filename):
    payment_id = instance.id
    if payment_id is None:
        payment_id = "new"
    ext = filename.split('.')[-1]
    new_filename = f'payment_slip_{payment_id}.{ext}'
    return os.path.join('payment_slips/', new_filename)


def compress_image(instance):
    # Compress the profile image when an instance is added or updated
    if hasattr(instance, 'profile_image') and instance.profile_image:
        try:
            with Image.open(instance.profile_image) as im:
                img_format = im.format

                # If image is JPEG, compress using JPEG format
                if img_format == 'JPEG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'JPEG', quality=70)
                    new_image = File(im_io, name=instance.profile_image.name)

                # If image is PNG, compress using PNG format
                elif img_format == 'PNG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'PNG', optimize=True)
                    new_image = File(im_io, name=instance.profile_image.name)

                # If image is neither JPEG nor PNG, raise an exception
                else:
                    raise Exception(f'Unsupported image format: {img_format}')

                # Assign the compressed image back to the instance's image attribute
                instance.profile_image = new_image
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            raise ValidationError(f'Error processing the image. {str(e)}')

    # Compress the room image when an instance is added or updated
    elif hasattr(instance, 'room_image') and instance.room_image:
        try:
            with Image.open(instance.room_image) as im:
                img_format = im.format

                # If image is JPEG, compress using JPEG format
                if img_format == 'JPEG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'JPEG', quality=70)
                    new_image = File(im_io, name=instance.room_image.name)

                # If image is PNG, compress using PNG format
                elif img_format == 'PNG':
                    im.thumbnail((400, 400))
                    im_io = BytesIO()
                    im.save(im_io, 'PNG', optimize=True)
                    new_image = File(im_io, name=instance.room_image.name)

                # If image is neither JPEG nor PNG, raise an exception
                else:
                    raise Exception(f'Unsupported image format: {img_format}')

                # Assign the compressed image back to the instance's image attribute
                instance.room_image = new_image
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            raise ValidationError(f'Error processing the image. {str(e)}')
