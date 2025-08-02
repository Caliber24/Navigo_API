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
      weights.get('budget', 0) * (1 / dest.average_cost if dest.average_cost > 0 else 0) + 
      weights.get('relax', 0) * dest.spa_facilities
    )
    
    scored.append((dest, score))
    scored.sort(reverse=True, key=lambda x: x[1])
    
    return [dest for dest, score in scored[:10]]