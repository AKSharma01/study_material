
from src.search.views.v1_0 import search as search_v1_0
from src.questions.views.v1_0 import questions_category as questions_category_v1_0

routes = [
	['/search/v1.0', search_v1_0],
	['/catalog/v1.0', questions_category_v1_0]
]
