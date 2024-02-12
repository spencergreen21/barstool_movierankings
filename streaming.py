import pandas as pd
import requests
import os

url = "https://streaming-availability.p.rapidapi.com/search/title"

# Read movie titles from the file
movies_list = []
with open("movie_list.txt", "r") as file:
    for movie in file:
        movies_list.append(movie.strip())

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame(columns=["Title", "Genre1", "Genre2", "Subscription_Service1", "Subscription_Service2", "Subscription_Service3"])

# API parameters
params = {
    "country": "us",
    "show_type": "movie",
    "output_language": "en"
}

headers = {
    "X-RapidAPI-Key": os.environ.get("X-RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
}

for movie_title in movies_list:
    params["title"] = movie_title

    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Print API response for debugging
    print("API Response for", movie_title, ":", data)

    # Extract genre information from the response
    if data.get("result"):
        genres = data["result"][0].get("genres", [])
        genre1 = genres[0]["name"] if genres else None
        genre2 = genres[1]["name"] if len(genres) > 1 else None
        print("Genres for", movie_title, ":", genre1, genre2)

        # Extract subscription streaming platforms
        subscription_services = []
        for streaming_info in data["result"][0]["streamingInfo"]["us"]:
            if streaming_info.get("streamingType") == "subscription":
                subscription_services.append(streaming_info["service"])
        print("Subscription services for", movie_title, ":", subscription_services)

        # Take up to three subscription services
        subscription_services = subscription_services[:3]

        # Append movie title, genre information, and subscription services to the DataFrame
        result_df = result_df.append({
            "Title": movie_title,
            "Genre1": genre1,
            "Genre2": genre2,
            "Subscription_Service1": subscription_services[0] if len(subscription_services) > 0 else None,
            "Subscription_Service2": subscription_services[1] if len(subscription_services) > 1 else None,
            "Subscription_Service3": subscription_services[2] if len(subscription_services) > 2 else None
        }, ignore_index=True)

print(result_df)









