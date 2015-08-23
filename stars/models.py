from django.db import models
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from fields import SerializedDataField
from constants import MIN_RATING, MAX_RATING

class Stars(models.Model):
    """
    A generic model for storing rating out of MAX_RATING for any other model
    """
    # User who submits rating/stars
    user = models.ForeignKey(User)

    rating = models.FloatField(db_index=True)
    # User comment/review
    comment = models.CharField(max_length=100, blank=True, null=True)

    # Generic content types
    content_type = models.ForeignKey(ContentType, db_index=True)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = 'User Rating'
        verbose_name_plural = 'User Ratings'
        unique_together = ('content_type', 'object_id', 'user')


class AggregateStars(models.Model):
    """
    Generic model for storing average rating of objects
    """
    avg_rating = models.FloatField(db_index=True, default=0.0)

    # Number of users who have submitted the rating
    num_of_users = models.PositiveIntegerField(default=0, db_index=True)
    # Rating distribution in form of dictionary
    # Shows the count of users who submitted 'x' rating
    rating_dist = SerializedDataField()

    last_update = models.DateTimeField(auto_now=True)

    # Generic content types.
    content_type = models.ForeignKey(ContentType, db_index=True)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = 'Aggregate Rating'
        verbose_name_plural = 'Aggregate Ratings'
        unique_together = ('content_type', 'object_id')
