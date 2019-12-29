from flask_mongoengine.wtf import model_form
from models import Artwork, Translation
from wtforms import FileField


ArtworkForm = model_form(Artwork)
TranslationForm = model_form(Translation)


class UploadForm(TranslationForm):
    photo_upload = FileField("jpg, png, or gif", validators=[])
    file_upload = FileField("place all code in a single .pde file")
