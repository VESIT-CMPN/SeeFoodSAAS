import json
import os
import shutil
import socket

import subprocess
from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from recognition.forms import ImageUploadForm

context = {}


def home(request):
    return HttpResponse("SeeFood Homepage!")


# TODO: Try using ResultsView commented below instead
def results(request):
    context['hostname'] = socket.gethostname()
    return render(request, 'recognition/results.html', context)


# Gives error : django.core.exceptions.ImproperlyConfigured: ResultsView is missing a QuerySet.
# Define ResultsView.model, ResultsView.queryset, or override ResultsView.get_queryset().
#
# class ResultsView(generic.ListView):
#     template_name = 'recognition/results.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['json_arr '] = json_arr
#         context['filename'] = filename


class UploadView(generic.FormView):
    template_name = 'recognition/details.html'
    form_class = ImageUploadForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print("form_invlaid() called!")
        return self.form_valid(form)

    def form_invalid(self, form):
        print("form_invlaid() called!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        upload_context = super().get_context_data(**kwargs)
        upload_context['container_id'] = socket.gethostname()
        return upload_context


def process(request):
    uploaded_file = request.FILES['image_file']

    location = 'media/' + str(uploaded_file.name).split('.')[0]
    print("location: ", location)
    if Path(location).exists():
        shutil.rmtree(location)

    fs = FileSystemStorage(location=location)
    filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(filename)
    print("Image saved at: ", uploaded_file_url)

    print("Processing image...")
    current_path = os.getcwd()
    output = subprocess.run(['flow', '--pbLoad', '../darkflow/built_graph/Adam/tiny-yolo-coco-4c.pb',
                             '--metaLoad', '../darkflow/built_graph/Adam/tiny-yolo-coco-4c.meta',
                             '--imgdir', location, '--json'])

    if output.returncode == 0:
        json_path = os.path.join(current_path, location, 'out')
        json_filename = str(filename).split('.')[0] + '.json'
        json_arr = json.load(open(os.path.join(json_path, json_filename)))
    else:
        return render(request, 'recognition/details.html', {'error_message': 'Error processing the image...'})

    global context
    context = {'json_arr': json_arr, 'filename': filename}
    return HttpResponseRedirect(reverse('recognition:results'))
