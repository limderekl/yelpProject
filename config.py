data = {
    'user': 'Reduced_Yelp_Data/reduced_yelp_academic_dataset_user.json',
    'business': 'Reduced_Yelp_Data/restaurants.json',
    'review': 'Reduced_Yelp_Data/reduced_yelp_academic_dataset_review.json'
}

fields = {
    'user': ['user_id', 'name', 'fans', 'review_count', 'average_stars'],
    'business': ['business_id', 'review_count', 'name', 'stars', 'categories', 'price'],
    'review': ['review_id', 'user_id', 'business_id', 'stars']
}