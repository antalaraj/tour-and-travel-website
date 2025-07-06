def calculate_price(destination_id, number_of_people):
    # Example logic: Fetch destination price and multiply by number of people
    from .models import Destination  # Import here to avoid circular imports
    destination = Destination.objects.get(id=destination_id)
    return destination.price_per_person * number_of_people
