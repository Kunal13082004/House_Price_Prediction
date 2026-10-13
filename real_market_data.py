import requests
import json


NHB_URL = (
    "https://residex.nhbonline.org.in/"
    "DashboardBY2024/Get_NHBResiCersai_PriceTrend"
)

NHB_REFERER = (
    "https://residex.nhbonline.org.in/"
    "DashboardBY2024/DashboardBY2024"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
    "Referer": NHB_REFERER,
}


def get_nhb_data(city_id=1, lookup="HFC", price_method_id=2):

    payload = {
        "reporttype": "CITY",
        "lookup": str(lookup),
        "cityid": str(city_id),
        "pincode": "0",
        "wardid": "0",
        "pricemtdid": str(price_method_id),
        "locid": "0",
        "chkbefore1718": "false",
    }

    try:

        response = requests.post(
            NHB_URL,
            headers=HEADERS,
            data=payload,
            timeout=20
        )

        if response.status_code != 200:
            return {
                "success": False,
                "message": f"NHB HTTP error: {response.status_code}",
                "data": None
            }

        result = response.json()

        if result.get("status") != "Success":
            return {
                "success": False,
                "message": result.get(
                    "message",
                    "NHB data unavailable"
                ),
                "data": None
            }

        raw_data = result.get("data")

        if not raw_data:
            return {
                "success": False,
                "message": "NHB returned empty data",
                "data": None
            }

        # Convert NHB JSON string into Python data
        try:
            parsed_data = json.loads(raw_data)
        except (json.JSONDecodeError, TypeError):
            parsed_data = raw_data

        return {
            "success": True,
            "message": "NHB data fetched successfully",
            "data": parsed_data
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": "NHB request timed out",
            "data": None
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "message": f"NHB connection error: {e}",
            "data": None
        }

    except ValueError:

        return {
            "success": False,
            "message": "NHB returned an invalid JSON response",
            "data": None
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Unexpected NHB error: {e}",
            "data": None
        }


if __name__ == "__main__":

    print("Testing NHB RESIDEX connection...")
    print()

    result = get_nhb_data(
        city_id=1,
        lookup="HFC",
        price_method_id=2
    )

    print("Success:", result["success"])
    print("Message:", result["message"])

    if result["success"]:
        print()
        print("NHB DATA:")
        print(result["data"])