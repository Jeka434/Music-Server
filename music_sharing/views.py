from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from .models import AudioFile


audio_mime_types = [
    'audio/mpeg',
    'audio/ogg',
    'audio/wav',
]


def get_pretty_size(size) -> str:
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    while size / 1024 > 1 and unit_index < len(units):
        size /= 1024
        unit_index += 1
    return '{:.2f}'.format(size) + ' ' + units[unit_index]


def mime_type_check(file):
    return file.content_type in audio_mime_types


@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = AudioFile(file=request.FILES['file'])
            if mime_type_check(instance.file.file):
                instance.save()
                return HttpResponseRedirect("/")
            messages.add_message(request, messages.ERROR, 'Non-audio file detected.')
    template = loader.get_template('music_sharing/index.html')
    files = []
    for f in AudioFile.objects.all():
        files.append({
            'name': f.file.name,
            'size': get_pretty_size(f.file.size),
            'url': f.file.url,
            'content_type': f.content_type
        })
    context = {'files': files}
    return HttpResponse(template.render(context, request))
