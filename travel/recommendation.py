from .models import Destination, Activity, TravelStyle, StyleParameter, UserTravelStyle


def recommend_destinations(user):
    user_style = UserTravelStyle.objects.filter(user=user).first()
    if not user_style:
        return []

    weights = {}
    for style in user_style.travel_style.all():
        for param in style.parameters.all():
            weights[param.key] = weights.get(param.key, 0) + param.weight

    destinations = Destination.objects.all()
    scored = []

    for dest in destinations:
        score = (
            weights.get('nature', 0) * dest.proximate_nature +
            weights.get('thrill', 0) * dest.thrill_activities +
            weights.get('cultural', 0) * dest.cultural_sites +
            weights.get('budget', 0) * (1 / dest.average_cost  if dest.average_cost > 0 else 0) +
            weights.get('relax', 0) * dest.spa_facilities
        )
        reason = "".join([
            f"طبیعت بالا. " if dest.proximity_nature > 0.7 else "",
            f"فعالیت‌های هیجانی. " if dest.thrill_activities > 0.7 else "",
            f"هزینه مناسب. " if dest.average_cost < 0.5 else "",
            f"فرهنگی غنی. " if dest.cultural_sites > 0.7 else "",
            f"امکانات ریلکسی بالا. " if dest.spa_facilities > 0.7 else ""
        ])
        dest.score = round(score, 3)
        dest.reason = reason.strip() or "پیشنهاد عمومی بر اساس علاقه‌مندی شما"
        scored.append((dest, score))

        return [dest for dest, score in scored[:10]]
