from django.shortcuts import render, redirect
from .models import Post, Like, Comment
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse



@login_required
def post_comment_create__and_list_view(request):
	qs = Post.objects.all()
	profile = Profile.objects.get(user=request.user)
	p_form = PostModelForm()
	c_form = CommentModelForm()
	post_added = False

	if 'submit_p_form' in request.POST:
		p_form = PostModelForm(request.POST, request.FILES)
		if p_form.is_valid():
			instance = p_form.save(commit=False)
			instance.author = profile
			instance.save()
			p_form = PostModelForm()
			post_added = True

	if 'submit_c_form' in request.POST:
		c_form = CommentModelForm(request.POST)	
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.user = profile
			instance.post = Post.objects.get(id=request.POST.get('post_id'))
			instance.save()
			c_form = CommentModelForm()

	context = {
	'qs':qs,
	'profile':profile,
	'p_form':p_form,
	'c_form':c_form,
	'post_added':post_added,
	}

	return render(request, 'post.html', context)



@login_required
def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)
		else:
			post_obj.liked.add(profile)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

			post_obj.save()
			like.save()

		data = {
		'value': like.value,
		'likes': post_obj.liked.all().count()
		}

		#return JsonResponse(data, safe=False)

	return redirect('posts:post')



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'confirm_del.html'
    success_url = reverse_lazy('posts:post')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author.user:
            return True
        return False



class PostUpdateView(LoginRequiredMixin, UpdateView):
	form_class = PostModelForm
	model = Post
	template_name = 'update.html'
	success_url = reverse_lazy('posts:post')

	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None, 'You need to be an author for update this post')
			return super().form_invalid(form)