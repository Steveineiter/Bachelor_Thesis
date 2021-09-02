# Idee:
# 1. get K random hashtags
# 2. calculate levenshtein disctances to those centroids
# 3. cluster it up
# 4. calculate the best new centroid in cluster (which hashtag has the smallest total number of levenshtein distances) # TODO Ponder if necessary
# 5. Repeat 2-5 until the centroid stays the same or MAX_ITERATIONS is reached
# 6. Return clusters aka personas