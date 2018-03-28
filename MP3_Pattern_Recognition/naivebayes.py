def compute_likelihoods(images_by_class, laplace):
    likelihoods = np.empty((0,1024))

    for k in range(len(images_by_class)):
        curImages = images_by_class[k]
        num_class_images = curImages.shape[1]

        curLikelihoods = []

        for i in range(curImages.shape[0]):
            num_observations = np.sum(curImages[i,:])

            likelihood = (num_observations + laplace) / (num_class_images + (2*laplace))

            curLikelihoods.append(likelihood)

        curLikelihoods = np.asarray(curLikelihoods)

        likelihoods = np.vstack((likelihoods, curLikelihoods))

    likelihoods = likelihoods.T

    return likelihoods

def compute_priors(training_data, images_by_class):
    pass
