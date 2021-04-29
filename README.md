# my-top-10-movies
Flask app that lists our top 10 films of all time

This full-stack app is written using Flask and is linked to an SQLite database. Thanks to "the Movies DB API", we are able to get information
about movies like the poster image, their title, the year of their release and their synopsis.

For our front-end, Flask/Bootstrap, Flask/WTForms and Jinja templating were used.
The server runs on Flask and the database is built on SQLite.

In our server we create a Model called "Movie" for the our database, two Flask forms and routes.

These routes are:

1. Home route
2. Edit route
3. Add route
4. Delete route
5. Find route

The home route once reached will read the movies from the database and order them by rating (we set the rating via another route).
After that, the movies will be sent to be rendered in the "index.html" file. There, the movies are rendered as cards which can be flipped by
moving the cursor on them. The user can see more info about the movie and can update or delete the card.

![image](https://user-images.githubusercontent.com/55893421/116587931-f1f24e80-a8e8-11eb-8815-ddb021cb9cca.png)

![image](https://user-images.githubusercontent.com/55893421/116587948-f9195c80-a8e8-11eb-8b7b-f2a8789b74e7.png)


The edit route (reached via the update button) leads to a form (Flask form). This form has two fields, one for the movie rating and one
for our review of the movie. Once we click submit, the data of the form is sent to the server via a POST request, extracted and used to
update the Movie entry in our database with the corresponding id (the current Movie database id is passed as a query parameter).

![image](https://user-images.githubusercontent.com/55893421/116588057-151cfe00-a8e9-11eb-8124-8dcaf6f55327.png)

The add route can be reached by the "Add" button at the bottom of the home page. It leads to another Flask Form with only one field asking for
the name of the movie. 

![image](https://user-images.githubusercontent.com/55893421/116590503-d8063b00-a8eb-11eb-83fb-faa9eb8e8b61.png)


Once a name (aka the movie title) is entered and submitted, we use it to make a GET request to the Movies DB API and we
send the results to be rendered on the "select.html" file. This file will render on screen all movie titles similar to the one the user submitted
as links:

![image](https://user-images.githubusercontent.com/55893421/116590662-07b54300-a8ec-11eb-8899-e37ad47f9869.png)

The user can click on the appropriate link, which will lead to the find route.

The find route will try to find the movie selected by the user in the Movies DB API via a GET request. Relevant information will be extracted from
the response and used to create a new entry in the database. The user is then redirected to the edit route, where he will be able to add a new rating
and review for that movie.

A delete route also exist in the case the user wants to remove a movie from this list. The movie id is sent to the server as a query parameter  and using
that id to delete the Movie enrty with that corresponding id.

