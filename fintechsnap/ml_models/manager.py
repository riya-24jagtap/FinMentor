USE_SVM = True
USE_HMM = False
USE_CRF = False

def run_models(user_data):
    results = {}

    if USE_SVM:
        from ml_models.svm.predict import predict_svm
        results["health"] = predict_svm(user_data)

    if USE_HMM:
        from ml_models.hmm.predict import predict_hmm
        results["trend"] = predict_hmm(user_data)

    if USE_CRF:
        from ml_models.crf.predict import predict_crf
        results["context"] = predict_crf(user_data)

    return results
