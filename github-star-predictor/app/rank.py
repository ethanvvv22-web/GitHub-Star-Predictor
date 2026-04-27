from .model.load_model import predict_stars

def rank_repositories(repos):
	ranked = []
	for repo in repos:
		prediction = predict_stars(repo)
		ranked.append({'repo': repo, 'predicted_stars': prediction})

	## Sort by prediction
	ranked_sorted = sorted(ranked, key=lambda x: x['predicted_stars'], reverse=True)
	return ranked_sorted


