import matplotlib.pyplot as plt
from lofo import LOFOImportance, Dataset, plot_importance
from sklearn.model_selection import KFold

class ImportanceAgent:
    def __init__(self, model, dataset, scoring):
        self.model = model
        self.dataset = dataset
        self.scoring = scoring
    
    def __make_dataset(self):   
        dataset = Dataset(df=self.dataset, target='produtividade', features=[col for col in self.dataset.columns if col != 'produtividade'])
        return dataset
        
    def get_lofo_importance(self):
        cv = KFold(n_splits=4, shuffle=False, random_state=None)
        lofo_imp = LOFOImportance(dataset=self.__make_dataset(), cv= cv, scoring=self.scoring, model = self.model)
        return lofo_imp.get_importance()
    
    def plot_importance(self):
        plot_importance(self.get_lofo_importance())
        plt.savefig('saves/lofo_importance.png')

    def remove_negative_importance(self):
        importance_df = self.get_lofo_importance()
        return importance_df[importance_df.importance_mean > 0]