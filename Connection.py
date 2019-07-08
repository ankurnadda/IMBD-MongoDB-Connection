from pymongo import MongoClient
client = MongoClient()
db = client.moviesproject
print("********************MENU***********************")
print("1.Find average rating of each movie")
print("2.Find similar users")
print("3.Find number of movies in each genre")
print("4.Find user defined tags associated with a movie")
print("5.Find the number of movies a user has rated")
print("6.Find the genre associated with a movie")
choice = int(input("Choose an option:"))


def avgRating():
    result = db.ratings.aggregate([
        {
            "$group": {"_id": "$MovieID", "Avg": {"$avg": "$Rating"}}
        },
        {
            "$sort": {"Avg": 1}
        }
    ])
    for line in result:
        print("Movie ID:", line["_id"], "|", "Avg Rating:", line["Avg"])


def similarUser(user):
    array = list()
    array2 = list()
    result = db.ratings.find(
        {"UserID": user},
        {"_id": 0, "MovieID": 1})
    for record in result:
        array.append(record['MovieID'])
    finalResult = db.ratings.find(
        {"MovieID": {"$in": array}},
        {"_id": 0, "UserID": 1})
    for rec in finalResult:
        array2.append(rec['UserID'])
    ans = set(array2)
    print("User similar to ", user, "are as below:")
    for l in ans:
        print(l)


def noMoviesinGenre():
    genreName = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
                 "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]
    print("Genre", "|", "Count")
    print("-------------------")
    for line in genreName:
        count = db.movies.count({"Genres": {"$regex": line}})
        print(line, "|", count)


def tagsinMovie(movieid):
    result = db.tags.find(
        {"MovieID": movieid},
        {"_id": 0, "Tag": 1}
    )
    finalResult = list()
    print("The", movieid, "is associated with the following tags")
    for record in result:
        finalResult.append(record["Tag"])
    finalResult = set(finalResult)
    print(finalResult)


def noofMoviesUserRated(userid):
    result = db.ratings.find(
        {"UserID": userid},
    ).count()
    print("The number of movies rated by ", userid, "are", result)


def movieGenre(movieid):
    result = db.movies.find(
        {"MovieID": movieid},
        {"_id": 0, "MovieID": 0}
    )
    for record in result:
        print("The movie", record["Title"], "is associated with the following genres:", record["Genres"])

if choice == 1:
    avgRating()
elif choice == 2:
    similarUser(int(input("Enter a User ID:")))
elif choice == 3:
    noMoviesinGenre()
elif choice == 4:
    tagsinMovie(int(input("Enter a movie id:")))
elif choice == 5:
    noofMoviesUserRated(int(input("Enter a user id:")))
elif choice == 6:
    movieGenre(int(input("Enter a movie id:")))
else:
    print("Invalid Choice.Exiting program.Run again")