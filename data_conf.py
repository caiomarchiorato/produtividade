import pandas as pd
from utils.query_execution import create_dataframe_from_query 

class DataChecker:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def read_data(self):
        try:
            
            self.data = create_dataframe_from_query(self.filepath)
            print("Dados lidos com sucesso.")
        except Exception as e:
            print(f"Erro ao ler os dados: {e}")

    def validate_data(self):
        if self.data is None:
            print("Dados não carregados.")
            return
        # self.check_missing_values()
        self.check_data_types()

    def check_missing_values(self):
        missing_values = self.data.isnull().sum()
        if missing_values.any():
            print("Valores ausentes encontrados:")
            print(missing_values)
        else:
            print("Nenhum valor ausente encontrado.")

    def check_data_types(self):
        data_types = self.data.info()
        print("Tipos de dados das colunas:")
        print(data_types)

    # def clean_data(self):
    #     if self.data is None:
    #         print("Dados não carregados.")
    #         return
    #     self.data.fillna(method='ffill', inplace=True)
    #     print("Dados limpos com sucesso.")

    def generate_report(self):
        if self.data is None:
            print("Dados não carregados.")
            return
        report = {
            "missing_values": self.data.isnull().sum().to_dict(),
            "data_types": self.data.dtypes.to_dict()
        }
        return report

    def print_report(self, report):
        if not report:
            print("Relatório vazio.")
            return
        print(50*"-")
        print("Relatório de Valores ausentes por coluna:")
        for column, missing in report["missing_values"].items():
            if missing == 0:
                pass
            else:
                print(f"{column}: {missing} Valores ausentes")

    def min_max_report(self):
        for column in self.data.columns:
            if self.data[column].dtype == 'int64' or self.data[column].dtype == 'float64':
                min_value = self.data[column].min()
                max_value = self.data[column].max()
                print(f"## Coluna --> {column}")
                print(f"(-) Valor Mínimo: {min_value}")
                print(f"(+) Valor Máximo: {max_value}")

def main():
    filepath = "data/queries/23_05_2024.sql"
    checker = DataChecker(filepath)
    
    checker.read_data()
    checker.validate_data()
    print(50*"-")
    checker.min_max_report()
    report = checker.generate_report()
    checker.print_report(report)
    
    print(50*"-")
    print("Relatório de Resultados:")
    print(report)

if __name__ == "__main__":
    main()
