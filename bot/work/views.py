import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignupForm, ChatLinkFormSet, SessionStep1Form, SessionStep2Form
from django.contrib.auth import logout
from .models import Groups, TelegramSession


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/register/login/')
    else:
        form = SignupForm()

    return render(request, 'work/signup.html', {'form': form})


def logout_v(request):
    logout(request)
    return redirect('/')


def add_chats(request):
    if request.method == 'POST':
        formset = ChatLinkFormSet(request.POST, prefix='chats')
        if formset.is_valid():
            links = [form.cleaned_data['link']
                     for form in formset
                     if form.cleaned_data.get('link')]

            group, created = Groups.objects.get_or_create(
                user=request.user,
                defaults={'chats': []}
            )

            added = group.add_chats(links)

            if added > 0:
                return redirect('/')
            else:
                for form in formset:
                    if form.cleaned_data.get('link') in group.get_chats():
                        form.add_error('link', 'Эта ссылка уже была добавлена ранее')
    else:
        formset = ChatLinkFormSet(prefix='chats')

    return render(request, 'work/add.html', {
        'formset': formset,
        'title': 'Добавление чатов'
    })


@login_required
def create_session(request):
    if hasattr(request.user, 'session'):
        session = request.user.session_us
        if not session.is_step1_completed:
            return handle_step1(request, session)
        else:
            return handle_step2(request, session)

    return handle_step1(request)


def handle_step1(request, session=None):

    if request.method == 'POST':
        form = SessionStep1Form(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.is_step1_completed = True
            session.save()
            return redirect('work:handle_step2', session_id=session.id)
    else:
        form = SessionStep1Form(instance=session)

    return render(request, 'work/session_step1.html', {'form': form})


def handle_step2(request, session_id):

    try:
        session = Session.objects.get(id=session_id, user=request.user)
    except Session.DoesNotExist:
        return redirect('work:create_session')

    if request.method == 'POST':
        form = SessionStep2Form(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Все данные успешно сохранены')
            return redirect('/')
    else:
        form = SessionStep2Form(instance=session)

    return render(request, 'work/session_step2.html', {'form': form})