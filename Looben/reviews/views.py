from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ReviewOfUniversity
from .forms import ReviewForm

from accounts.models import Users, Schools
from accounts import contribution_calculation


@login_required
def create_review_of_university(request):
    create_review_form = ReviewForm(request.POST or None)
    if create_review_form.is_valid():
        create_review_form.instance.user = request.user
        create_review_form.save()
        messages.success(request, 'レビューを作成しました')
        # Start -Schoolsの星評価にこのレビューの評価を反映させる-
        target_university = Schools.objects.get(id=create_review_form.cleaned_data.get('university').id)
        review_list_for_target_university = ReviewOfUniversity.objects.filter(university=target_university).all()
        # get the value of total added rating
        total_added_rating_value = int(create_review_form.cleaned_data.get('star'))
        number_of_review = len(review_list_for_target_university) + 1
        for review in review_list_for_target_university:
            total_added_rating_value += int(review.star)
        target_university.star_rating = total_added_rating_value / number_of_review
        target_university.save()
        # End
        contribution_calculation.for_creating_review(user=request.user)
        return redirect('accounts:research_university')
    return render(
        request, 'reviews/create_review_of_university.html', context={
            'create_review_form': create_review_form
        }
    )
    
    
class ReviewListOfUniversities(DetailView):
    model = Schools
    template_name = 'reviews/review_list_of_universities.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.object
        context['reviews'] = ReviewOfUniversity.objects.filter(university=school)
        return context
    

