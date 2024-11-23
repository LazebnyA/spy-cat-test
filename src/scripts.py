import requests

def get_valid_breeds():
    """
    Fetches and returns a list of valid cat breed names from the Cat API.

    Returns:
        list: A list of strings containing breed names.
    """
    url = "https://api.thecatapi.com/v1/breeds"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        breeds = response.json()
        return [breed['name'] for breed in breeds]
    except requests.RequestException as e:
        print(f"An error occurred while fetching breed data: {e}")
        return []

VALID_BREEDS = get_valid_breeds()

if __name__ == "__main__":
    valid_breeds = get_valid_breeds()
    print(f"Valid Cat Breeds:\n{valid_breeds}")
