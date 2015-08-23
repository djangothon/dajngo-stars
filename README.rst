=====
Django Stars
=====

Stars is a simple generic Django app to store user ratings for either e-commerce websites, blog articles, review sites etc.


Quick start
-----------

1. Add "stars" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'stars',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'', include('stars.urls')),

3. Run `python manage.py migrate` to create the stars models.

4. Include stars.js script in pages where you'd like to show ratings and get ratings from users.

5. You can show ratings by adding following line to your template at desired position
    <div id="show-rating-{{post.get_content_type.id}}-{{post.id}}" class="star-show-rating" ajax="{% url 'show_rating' post.get_content_type.id post.id %}" target="show-rating-{{post.get_content_type.id}}-{{post.id}}" loader="false"></div>

where post is the object for which you're showing the rating.

6. Similarly, you can get ratings from users by adding following line. It adds a rating form where users can submit their rating.
    <div id="get-rating-{{post.get_content_type.id}}-{{post.id}}" class="star-get-rating" ajax="{% url 'get_rating' post.get_content_type.id post.id 1 %}" target="get-rating-{{post.get_content_type.id}}-{{post.id}}" loader="false"></div>

where post is the object for which you're gettng the rating from user.
