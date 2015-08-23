import collections

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts  import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from .models import Stars, AggregateStars
from decorators import ajax_view
from utils import calculate_stars, update_aggregate_stars, get_avg_rating
from utils import get_percentages_for_stars_dist

AJAX_OK = 'OK'
AJAX_ERROR = 'ERROR'


def show_rating(request, ctype_id, object_id):
    """Show average rating of an object
    # stars[0]=> fullstar
    # stars[1]=> halfstar
    # stars[2]=> emptystar
    # Perncentage of each type of rating {1,2,3,4,5}
    """

    template = 'stars/show_rating.html'
    # Get avg_rating of the object and rating distribution
    avg_rating, star_dist = get_avg_rating(ctype_id, object_id)
    stars = calculate_stars(avg_rating)
    # Check if there is no any rating for the object or not
    no_rating = 0
    if stars[2] == 5:
        no_rating = 1

    ctx = {
            "full_stars": range(stars[0]),
            "half_stars": range(stars[1]),
            "empty_stars": range(stars[2]),
            # if no rating is there
            "no_rating": no_rating,
            "avg_rating": avg_rating,
            # StarsPercentageDist
            "stars_percentage_dist": get_percentages_for_stars_dist(star_dist)
    }
    ctx = RequestContext(request, ctx)
    return render_to_response(template, ctx)


def get_rating(request, ctype_id, object_id, decoration=1):
    ctx = {}
    template = 'stars/get_rating.html'
    # Check if user already has submitted the rating
    if request.user.is_authenticated():
        stars = Stars.objects.filter(user=request.user,
            content_type_id=ctype_id, object_id=object_id)

        if stars and stars[0].rating > 0.0:
            template = 'stars/show_user_rating.html'
            stars_count = calculate_stars(stars[0].rating)
            ctx.update({
                'full_stars': range(stars_count[0]),
                'half_stars': range(stars_count[1]),
                'empty_stars': range(stars_count[2]),
                'user_rating': stars[0].rating,
                # Show 'Saved' text only after submitting new rating
                "show_check": 0,
            })

    ctx.update({
        'ctype_id': ctype_id,
        'object_id': object_id,
        'decoration': int(decoration),
    })
    ctx = RequestContext(request, ctx)
    return render_to_response(template, ctx)


@ajax_view()
def submit_user_rating(request, ctype_id, object_id, decoration=1):
    """
    Save the rating submitted by user
    """
    template = 'stars/show_user_rating.html'
    rating_id = 'rating-%s-%s' % (ctype_id, object_id)
    rating = request.POST.get(rating_id, 1.0)
    rating = float(rating)
    # Check if user has already submitted rating
    user = User.objects.all()[0]
    stars = Stars.objects.filter(user=user,
        content_type_id=ctype_id, object_id=object_id)

    # If not, create new object Else update existing rating
    if not stars:
        star = Stars(user=user, content_type_id=ctype_id,
            object_id=object_id, rating=rating)
        star.save()
    else:
        star = stars[0]
        star.rating = rating
        star.save()

    # Update AggragateStars model
    update_aggregate_stars(ctype_id, object_id, rating)

    stars_count = calculate_stars(rating)
    ctx = {
        'ctype_id': ctype_id,
        'object_id': object_id,
        'full_stars': range(stars_count[0]),
        'half_stars': range(stars_count[1]),
        'empty_stars': range(stars_count[2]),
        'user_rating': rating,
        'show_check': 1,
        'decoration': int(decoration),
    }
    ctx = RequestContext(request, ctx)
    html = render_to_string(template, ctx)
    response = {
        'status': AJAX_OK,
        'data' : html
    }
    return response


@ajax_view()
def clear_user_rating(request, ctype_id, object_id, decoration=1):
    """
    Clear previous rating by the user and render get-rating page
    for new rating
    """
    # Update rating by the user for object_id to zero.
    user = User.objects.all()[0]
    stars = Stars.objects.get(user=user, content_type_id=ctype_id,
                              object_id=object_id)
    previous_rating = stars.rating
    stars.rating = 0.0
    stars.save()
    print "+="*80, previous_rating

    # If user didn't clere his rating
    if previous_rating != 0.0:
        # Update AggragateStars model
        update_aggregate_stars(ctype_id, object_id, -1*previous_rating)
    template = 'stars/get_rating.html'
    ctx = {
        'ctype_id': ctype_id,
        'object_id': object_id,
        'decoration': int(decoration),
    }
    ctx = RequestContext(request, ctx)
    html = render_to_string(template, ctx)
    response = {
        'status': AJAX_OK,
        'data' : html
    }
    return response
