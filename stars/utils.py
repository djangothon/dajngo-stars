import collections

from django.contrib.contenttypes.models import ContentType

from .models import Stars, AggregateStars
from constants import MIN_RATING, MAX_RATING


def get_avg_rating(ctype_id, object_id):
    """Get average rating for an object
    """
    aggregate_stars = AggregateStars.objects.filter(
            content_type_id=ctype_id,
            object_id=object_id)

    if not aggregate_stars:
        avg_rating = 0.0
        score_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        return avg_rating, score_dist
    else:
        avg_rating = aggregate_stars[0].avg_rating
        score_dist = aggregate_stars[0].rating_dist
        return round(avg_rating, 1), score_dist


def calculate_stars(avg_rating):
    """
    Returns number of full_stars, half_stars and empty_stars
    for the given average rating.

    Average rating is rounded off according to the following
    function.
       [4.0 - 4.3) => 4.0
       [4.3 - 4.7) => 4.5
       [4.8 - 5.0) => 5.0

    """
    avg_rating *= 10
    avg_rating = int(avg_rating)
    full_star = avg_rating/10
    remainder = avg_rating%10
    half_star = 0

    if remainder >= 3 and remainder <= 7:
        half_star = 1
    if remainder >= 8:
        full_star += 1

    empty_star = MAX_RATING - full_star - half_star
    empty_star = int(empty_star)
    return [full_star, half_star, empty_star]


def update_aggregate_stars(content_type_id, object_id, rating):
    print "3"*40, MIN_RATING, MAX_RATING
    obj = AggregateStars.objects.filter(content_type_id=content_type_id,
        object_id=object_id)
    # If it's first rating make a new entry
    if not obj:
        num_of_user = 1
        rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        rating = int(rating)
        rating_dist[rating] = 1
        rating_dist = rating_dist
        aggr_stars = AggregateStars(content_type_id=content_type_id,
                                        object_id=object_id,
                                        avg_rating=rating,
                                        rating_dist=rating_dist,
                                        num_of_users=num_of_user)
        aggr_stars.save()
    else:
        obj = obj[0]
        avg_rating = obj.avg_rating
        num_of_users = obj.num_of_users
        rating = int(rating)
        rating_dist = obj.rating_dist
        # rating will be negative if user will clear his rating
        if rating < 0.0:
            print "clearing rating"
            obj.num_of_users = num_of_users-1
            if num_of_users == 1:
                new_avg_rating = 0.0
            else:
                new_total_rating = avg_rating*num_of_users+rating
                new_avg_rating = new_total_rating/(num_of_users-1)
            positive_rating = -1*rating
            rating_dist[positive_rating] -= 1
            print rating_dist, new_avg_rating
        else:
            print "Update Rating"
            obj.num_of_users = num_of_users+1
            new_total_rating = avg_rating*num_of_users+rating
            new_avg_rating = new_total_rating/(num_of_users+1)
            rating_dist[rating] += 1
            print rating_dist, new_avg_rating
        obj.rating_dist = rating_dist
        obj.avg_rating = new_avg_rating
        obj.save()


def get_percentages_for_stars_dist(star_dist):
    """Get percentage of how many users have submitted 1,2,3,4 or 5 star rating
    """
    percentage_fields = {
            "one_star_percentage": 1,
            "two_stars_percentage": 2,
            "three_stars_percentage": 3,
            "four_stars_percentage": 4,
            "five_stars_percentage": 5
    }

    StarsPercentageDist = collections.namedtuple('StarsPercentageDist', percentage_fields)
    percentages = {}
    total_votes = sum(star_dist.values())
    for field_name, no_of_stars in percentage_fields.iteritems():
        no_of_users = star_dist.get(no_of_stars)
        if total_votes:
            percentage = float(no_of_users)/(total_votes*100)
            percentages[field_name] = round(percentage,0)
        else:
            percentages[field_name] = 0

    return StarsPercentageDist(**percentages)
