print(__doc__)

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


##############################################################################
# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
#X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
#print X
#print labels_true
#X = StandardScaler().fit_transform(X)
f = open('input_data', 'r')
fn = f.readlines()
f.close()
X = [[] for i in range(10)]
for i in range(10):
	X[i] = [float(x) for x in fn[i].strip().split()]

X = np.array(X)
X_scaled = StandardScaler().fit_transform(X)
#############################################################################
# Compute DBSCAN
#db = DBSCAN(eps=0.3, min_samples=3, metric='precomputed' algorithm='auto', leaf_size30, p=None,random_state=None).fit(X)
db = DBSCAN(eps=0.3, min_samples=5, metric='precomputed').fit(X_scaled)
core_samples = db.core_sample_indices_
labels = db.labels_

print("core samples are:")
print(core_samples)
print("labels are:")
print(labels)

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"% metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(X, labels))
##############################################################################
# Plot result
import pylab as pl
# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
	if k == -1:
	# Black used for noise.
		col = 'k'
		markersize = 6
	class_members = [index[0] for index in np.argwhere(labels == k)]
	cluster_core_samples = [index for index in core_samples if labels[index] == k]
	for index in class_members:
		x = X[index]
		if index in core_samples and k != -1:
			markersize = 14
		else:
		    markersize = 6
        pl.plot(x[0], x[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=markersize)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()
