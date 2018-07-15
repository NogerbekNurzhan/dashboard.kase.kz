# -*- coding: utf-8 -*-


from .models import Video
from .forms import VideoForm
from django.views.generic import TemplateView
from django.views.generic.edit import(
	FormView,
	CreateView,
	UpdateView,
	DeleteView,
)
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.context_processors import PermWrapper
from django.contrib.auth.mixins import PermissionRequiredMixin


# Video List View
class VideoListView(TemplateView):
    template_name = "video/video_content.html"
    permission_required = ('video.view_video')

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context


# Video Sorting View
class VideoSortingView(CsrfExemptMixin, JsonRequestResponseMixin, FormView):
    def post(self, request, *args, **kwargs):
        print self.request_json.items()
        for pk, idx in self.request_json.items():
            Video.objects.filter(pk=pk).update(idx=idx)
        return self.render_json_response({'saved': 'ok'})


# Video Create View
class VideoCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'video/create_video.html'
    form_class = VideoForm
    permission_required = ('video.add_video')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        context = {'video_create_form': VideoForm()}
        data['html_form'] = render_to_string('video/create_video.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        data = dict()
        # Перед созданием новой записи проверяем есть ли видео
        if Video.objects.all().exists():
            data['video_exist'] = True
        else:
            data['video_exist'] = False
        # Сохраняем новую запись
        new_video = form.save(commit=False)
        new_video.save()
        # Будет использовано лишь один раз в начале, когда еще нет списка видео
        data['html_videos'] = render_to_string(
            'video/videos.html',
            {
                'videos': Video.objects.all(),
                'perms': PermWrapper(self.request.user),
            }
        )
        # Будет использоваться когда есть список видео
        data['html_video'] = render_to_string(
            'video/video.html',
            {
                'video': new_video,
                'perms': PermWrapper(self.request.user),
            }
        )
        data['video_id'] = new_video.id
        data['form_is_valid'] = True
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Video Edit View
class VideoEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'video/edit_video.html'
    form_class = VideoForm
    model = Video
    permission_required = ('video.change_video')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        data = dict()
        video = Video.objects.get(pk=self.kwargs['pk'])
        video_edit_form = VideoForm(instance=video)
        context = {'video': video, 'video_edit_form': video_edit_form}
        data['html_form'] = render_to_string('video/edit_video.html', context, request=request)
        return JsonResponse(data)

    def form_valid(self, form):
        new_video = form.save(commit=False)
        new_video.save()
        data = dict()
        data['form_is_valid'] = True
        data['html_video'] = render_to_string(
            'video/video.html',
            {
                'video': new_video,
                'perms': PermWrapper(self.request.user),
            }
        )
        data['video_id'] = new_video.id
        return JsonResponse(data)

    def form_invalid(self, form):
        data = dict()
        data['form_is_valid'] = False
        data['form_errors'] = form.errors
        return JsonResponse(data)


# Video Delete View
class VideoDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('video.delete_video')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs['pk'])
        data = dict()
        context = {'video': video}
        data['html_form'] = render_to_string('video/delete_video.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs['pk'])
        data = dict()
        data['video_id'] = video.id
        video.delete()
        # После удаление записи проверяем есть ли видео
        if Video.objects.all().exists():
            data['video_exist'] = True
        else:
            data['video_exist'] = False
            data['html_videos'] = render_to_string(
                'video/videos.html',
                {
                    'videos': Video.objects.all(),
                    'perms': PermWrapper(self.request.user),
                }
            )
        data['form_is_valid'] = True
        return JsonResponse(data)
