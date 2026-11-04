# BlocketAPI

[![PyPI version](https://img.shields.io/pypi/v/blocket_api)](https://pypi.org/project/blocket_api/) [![License](https://img.shields.io/badge/license-WTFPL-green)](https://github.com/dunderrrrrr/blocket_api/blob/main/LICENSE) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![PyPI - Downloads](https://static.pepy.tech/personalized-badge/blocket-api?period=monthly&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=RED&left_text=downloads%2Fmonth)

BlocketAPI allows users to search [blocket.se](https://blocket.se/) for ads.

> Blocket is one of Sweden's largest online marketplaces. It was founded in 1996 and allows users to buy and sell a wide range of items, including cars, real estate, jobs, services, and second-hand goods. The platform is known for its extensive reach ~~and user-friendly interface~~, making it a popular choice for Swedes looking to purchase or sell items quickly and efficiently.

## 🧑‍💻️ Install

Install BlocketAPI via PyPI...

```sh
pip install blocket-api # using pip
uv add blocket-api # using uv
```

## 📜 Docs 

The full documentation can be found at [blocket-api.se](https://blocket-api.se/).

## 💁‍♀️ Usage

```py
from blocket_api import (
    BlocketAPI,
    Category,
    CarColor,
    CarFuel,
    CarModel,
    CarSortOrder,
    CarTransmission,
    CarWheelDrive,
    Location,
)

api = BlocketAPI()

# search all of blocket
api.search(
    "Tamagotchi",
    sort_order=SortOrder.PRICE_ASC,
    locations=[Location.STOCKHOLM, Location.UPPSALA],
    category=Category.FRITID_HOBBY_OCH_UNDERHALLNING,
)

# search for cars
api.search_car(
    "Audi", # query is optional
    sort_order=CarSortOrder.MILEAGE_ASC,
    models=[CarModel.AUDI],
    colors=[CarColor.GULD],
    price_from=10000,
    price_to=50000,
    transmissions=[CarTransmission.MANUAL],
    fuels=[CarFuel.DIESEL],
    wheel_drive=[CarWheelDrive.RWD],
    locations=[Location.STOCKHOLM],
    horsepower_from=200,
    horsepower_to=300,
    org_id=1337, # dealer or store id
)

# search for boats
from blocket_api import BoatType

api.search_boat(
    "Mercury", # query is optional
    types=[BoatType.DAYCRUISER],
    locations=[Location.STOCKHOLM],
    length_from=10,
    length_to=15,    
    price_from=20000,
    price_to=90000,
    org_id=1337, # dealer or store id
)

# search for motorcycles
from blocket_api import McType, McModel

api.search_mc(
    "TC 150", # query is optional
    types=[McType.SPORT],
    locations=[Location.STOCKHOLM],
    models=[McModel.DUCATI],
    price_from=20000,
    price_to=90000,
    engine_volume_from=100,
    engine_volume_to=200,
    org_id=1337, # dealer or store id
)


# get ad details
from blocket_api import CarAd, RecommerceAd, BoatAd, McAd

api.get_ad(RecommerceAd(12345678))
api.get_ad(CarAd(12345678))
api.get_ad(BoatAd(12345678))
api.get_ad(McAd(12345678))
```

### Async support

```py
import asyncio
from blocket_api import AsyncBlocketAPI

async def main():
    async with AsyncBlocketAPI() as api:
        results = await api.search("iPhone 15")

asyncio.run(main())
```

## 📝 Notes

- REST API: https://blocket-api.se
- Webhooks: https://webhooks.blocket-api.se
- Source repo: https://github.com/dunderrrrrr/blocket_api
- PyPI: https://pypi.org/project/blocket-api/
- Email: hello@blocket-api.se


## Skadeklar extension: moped and scooter search (work in progress)

This fork adds `BlocketAPI.search_moped()`, `AsyncBlocketAPI.search_moped()`,
`MopedType` (EU class I: `type=6`, class II: `type=8`) and `MopedAd`.
Moped cars are intentionally excluded; motorcycle scooters still use `search_mc()`.

**Not production ready yet:** The public Blocket page
<https://www.blocket.se/mobility/search/mc/scooter> confirms the class filters
but its dedicated JSON endpoint identifier has not been verified. The library
therefore **does not guess an endpoint or silently fall back to motorcycle
search**. Until an endpoint has been validated against real moped listings,
calling `search_moped()` without explicit configuration raises a descriptive
exception. This feature must not be marked as connected in Skadeklar Portal.

After verifying the real Blocket network request, set the endpoint only on
the backend (environment variable `BLOCKET_MOPED_SEARCH_URL`) or pass it in
the constructor. No Blocket API key is required for the unofficial public
search interface.

```python
from blocket_api import BlocketAPI, McModel, MopedType

api = BlocketAPI()  # reads server-side BLOCKET_MOPED_SEARCH_URL
results = api.search_moped(
    "Speedfight", models=[McModel.PEUGEOT],
    types=[MopedType.EU_KLASS_I],
    price_to=30000,
)
```

This fork is for Skadeklar's authorized internal workflows. Upstream
response shape, type filtering and results for specific models need live
verification before enabling the portal integration. No public relay,
proxy or new database is required by this Python library.
