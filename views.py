from django.views import generic
from .models import Post, Comment
from .forms import CommentForm,Add_Form, UserForm
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

def ordering_get_for_activ_posts(order_key):
    queryset = Post.objects.filter(status=1).order_by(order_key)
    return queryset


class PostList(generic.ListView):
    queryset = ordering_get_for_activ_posts('-created_on')
    template_name = 'blog/card.html'


    def get_context_data(self, **kwargs):

        context = super(PostList, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['last_post'] = self.queryset[0]
        # print(self.request.user.is_authenticated)
        return context

# @login_required(login_url='/accounts/login/')
class UserPanel(generic.TemplateView):
    template_name = 'blog/userpanel.html'
    # login_url = 'login/'
    # redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super(UserPanel, self).get_context_data(**kwargs)
        context['form'] = Add_Form

        return context
    def post(self,**kwargs ):
        print(self.request.POST)



# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#partsipamn
# t
# def get_(self, ):
#     print('dsds')
def log_in(request):
    print(request.user)
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)

    return HttpResponseRedirect('/blog')


def unauth(request):
    logout(request)
    print('HUI')
    return HttpResponseRedirect('../blog')

def reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['mail']
        user = User.objects.create_user(username=username, password=password, email=email)
        if user :
            login(request, user)
        return HttpResponseRedirect('/blog')
    else:
        return HttpResponseRedirect('/blog/error-reg')

def detail_view(request, slug):
    template_name = 'blog/post_detail.html'
    # print(request.POST)
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).filter(active=True)
    queryset = ordering_get_for_activ_posts('-created_on')

    if request.user.is_authenticated:

        if request.method == 'POST':

            comment_form = CommentForm(data=request.POST)
            # print(dir(comment_form))
            # print(comment_form.errors)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author_id=request.user
                new_comment.save()
                return HttpResponseRedirect('.')

    comment_form = CommentForm()

    context = {'post': post,
               'form': comment_form,
               'comments': comments,
               'last_post': queryset[0],
                'count_comm': len(comments)
               }
    return render(request, template_name, context)
