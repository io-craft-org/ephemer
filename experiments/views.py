from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from . import forms, models


# Create your views here.
def experiment_list(request):
    experiments = models.Experiment.objects.all()
    return render(
        request,
        template_name="experiments/experiment_list.html",
        context={"experiments": experiments},
    )


def experiment_detail(request, experiment_id):
    experiment = models.Experiment.objects.get(pk=experiment_id)
    return render(
        request,
        template_name="experiments/experiment_detail.html",
        context={"experiment": experiment},
    )


def experiment_create(request):
    if request.method == "POST":
        form = forms.ExperimentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("experiments-experiment-list"))
    else:
        form = forms.ExperimentForm()

    return render(
        request,
        template_name="experiments/experiment_create.html",
        context={"form": form},
    )


class ExperimentList(TemplateView):
    template_name = "experiments/experiment_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experiments"] = models.Experiment.objects.all()

        return context


class ExperimentList2(ListView):
    template_name = "experiments/experiment_list.html"
    queryset = models.Experiment.objects.all()
    context_object_name = "experiments"


class ExperimentCreate(CreateView):
    model = models.Experiment
    fields = ["title"]
    template_name = "experiments/experiment_create.html"


class ExperimentDetail(DetailView):
    model = models.Experiment
    template_name = "experiments/experiment_detail.html"
    context_object_name = "experiment"
    pk_url_kwarg = "experiment_id"
