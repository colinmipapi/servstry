from django.shortcuts import render

from companies.forms import WaitListForm


def wait_list(request):
    submit = False
    if request.method == 'POST':
        form = WaitListForm(request.POST)
        if form.is_valid():
            form.save()
            submit = True
    else:
        form = WaitListForm()

    return render(request, 'wait_list_landing.html', {
        'form': form,
        'submit': submit,
    })
