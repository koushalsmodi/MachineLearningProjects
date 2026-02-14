


def calculate_nights(travel_dates):
    if len(travel_dates) < 2:
        nights = 1
    else:
        nights = len(travel_dates) - 1

    return nights