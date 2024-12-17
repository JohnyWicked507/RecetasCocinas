import requests

SWAPI_BASE_URL = "https://swapi.dev/api/"


def get_all_data(endpoint):
    data = []
    url = f"{SWAPI_BASE_URL}{endpoint}/"
    while url:
        response = requests.get(url).json()
        data.extend(response["results"])
        url = response["next"]
    return data


def planets_with_arid_climate():
    planets = get_all_data("planets")
    arid_planets = [planet for planet in planets if "arid" in planet["climate"].lower()]
    movie_count = set()
    for planet in arid_planets:
        for film in planet["films"]:
            movie_count.add(film)
    return len(movie_count)


def count_wookies():
    species = get_all_data("species")
    wookiee_count = 0
    for species_item in species:
        if "Wookie" in species_item["name"]:
            wookiee_count += 1
            # Get all characters that are Wookies
            characters = get_all_data("people")
            for character in characters:
                if species_item["url"] in character["species"]:
                    wookiee_count += 1
    return wookiee_count


def smallest_starship_in_first_movie():
    films = get_all_data("films")
    first_movie = films[0]
    starships = get_all_data("starships")
    smallest_starship = None
    for starship in starships:
        if first_movie["url"] in starship["films"]:
            if smallest_starship is None or int(starship["length"]) < int(
                smallest_starship["length"]
            ):
                smallest_starship = starship
    return smallest_starship["name"] if smallest_starship else None


if __name__ == "__main__":
    print(
        f"Planets with an arid climate appear in {planets_with_arid_climate()} films."
    )
    print(f"Total number of Wookiees in the saga: {count_wookies()}")
    print(
        f"The smallest starship in the first movie is: {smallest_starship_in_first_movie()}"
    )
