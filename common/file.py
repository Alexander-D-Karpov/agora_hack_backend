import os


def file_path_mixing(instance, filename):
    if "Font" in instance.__class__.__name__:
        return os.path.join(f"uploads/{instance.user.username}/fonts/", filename)
    elif "Image" in instance.__class__.__name__:
        return os.path.join(f"uploads/{instance.user.username}/images/", filename)
    return os.path.join(f"uploads/{instance.user.username}/", filename)
