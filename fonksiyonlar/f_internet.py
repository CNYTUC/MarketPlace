import requests  # requests kütüphanesini eklemeyi unutmayın

def kontrol() -> bool:
    try:
        response = requests.get(
            "https://httpbin.org",
            timeout=10
        )
        return response.status_code == 200

    except requests.RequestException:
        return False