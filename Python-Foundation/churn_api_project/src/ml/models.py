from sklearn.ensemble import RandomForestClassifier


class BaseModel:
    def __init__(self, **kwargs):
        # Encapsulation: The raw sklearn model is hidden behind a protected variable
        self._model = None
        self.hyperparams = kwargs

    def train(self, X, y):
        raise NotImplementedError("Subclasses must implement this method")

    def predict(self, X):
        return self._model.predict(X)


# Inheritance: Child class specifically for Random Forest
class ChurnRandomForest(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Default params with **kwargs override capability
        params = {"n_estimators": 100, "random_state": 42}
        params.update(self.hyperparams)
        self._model = RandomForestClassifier(**params)

    def train(self, X, y):
        self._model.fit(X, y)
