import pandas as pd
import numpy as np

class UnitEconomicsCalculator:
    def __init__(self):
        # Инициализация базовых параметров
        self.products = [
            'SupplyChain Blockchain Core Platform',
            'SupplyChain Analytics Suite',
            'SupplyChain Technical Support & Consulting',
            'SupplyChain Enterprise Solutions'
        ]
        
        self.segments = ['Small', 'Medium', 'Enterprise']
        
        # Структура для хранения входных данных
        self.input_data = {
            'aov': {
                'Small': [500, 200, 100, None],
                'Medium': [2000, 800, 400, None],
                'Enterprise': [5000, 2000, 1000, 8000]
            },
            'distribution': {
                'Small': [0.50, 0.40, 0.45, 0.00],
                'Medium': [0.35, 0.40, 0.35, 0.00],
                'Enterprise': [0.15, 0.20, 0.20, 1.00]
            },
            'cogs': {
                'Small': [100, 70, 25, None],
                'Medium': [500, 130, 100, None],
                'Enterprise': [1000, 500, 250, 1600]
            },
            'lifetime': {
                'Small': [24, 24, 24, None],
                'Medium': [36, 36, 36, None],
                'Enterprise': [48, 48, 48, 48]
            },
            'cac': {
                'Small': [2500, 1500, 300, None],
                'Medium': [7500, 4500, 1000, None],
                'Enterprise': [20000, 12000, 2000, 30000]
            },
            'setup': {
                'Small': [500, 200, 100, None],
                'Medium': [2000, 800, 400, None],
                'Enterprise': [5000, 2000, 1000, 10000]
            },
            'churn': {
                'Small': [0.06, 0.06, 0.06, 0.00],
                'Medium': [0.04, 0.04, 0.04, 0.00],
                'Enterprise': [0.03, 0.03, 0.03, 0.03]
            }
        }
        
        self.opex = {
            'Разработка': 15000,
            'DevOps': 5000,
            'Тестирование': 3000,
            'Маркетинг': 2000,
            'Продажи': 6000,
            'Администрирование': 4000
        }
        
        self.growth_plan = {
            'year1_clients': [50, 75, 100, 5],
            'monthly_new_clients': {
                'months1_3': [2, 3, 5, 1],
                'months4_6': [3, 5, 8, 2],
                'months7_12': [4, 7, 10, 2]
            }
        }

    def calculate_weighted_metrics(self):
        """Расчет взвешенных метрик для каждого продукта"""
        results = []
        
        for prod_idx, product in enumerate(self.products):
            # Расчет WAO
            wao = sum(self.input_data['aov'][segment][prod_idx] * 
                     self.input_data['distribution'][segment][prod_idx]
                     for segment in self.segments
                     if self.input_data['aov'][segment][prod_idx] is not None)
            
            # Аналогичные расчеты для других метрик
            wcogs = sum(self.input_data['cogs'][segment][prod_idx] * 
                       self.input_data['distribution'][segment][prod_idx]
                       for segment in self.segments
                       if self.input_data['cogs'][segment][prod_idx] is not None)
            
            wcac = sum(self.input_data['cac'][segment][prod_idx] * 
                      self.input_data['distribution'][segment][prod_idx]
                      for segment in self.segments
                      if self.input_data['cac'][segment][prod_idx] is not None)
            
            wsetup = sum(self.input_data['setup'][segment][prod_idx] * 
                        self.input_data['distribution'][segment][prod_idx]
                        for segment in self.segments
                        if self.input_data['setup'][segment][prod_idx] is not None)
            
            avg_life = sum(self.input_data['lifetime'][segment][prod_idx] * 
                          self.input_data['distribution'][segment][prod_idx]
                          for segment in self.segments
                          if self.input_data['lifetime'][segment][prod_idx] is not None)
            
            wchurn = sum(self.input_data['churn'][segment][prod_idx] * 
                        self.input_data['distribution'][segment][prod_idx]
                        for segment in self.segments
                        if self.input_data['churn'][segment][prod_idx] is not None)
            
            # Расчет производных метрик
            gm = (wao - wcogs) / wao if wao > 0 else 0
            ltr = wao * avg_life
            ltc = wcac + wsetup + (wcogs * avg_life)
            ltv = ltr - ltc
            ltv_cac = ltv / wcac if wcac > 0 else 0
            margin = (wao - wcogs - (wcac + wsetup) / avg_life) / wao if wao > 0 else 0
            cm = wao * margin
            cac_payback = (wcac + wsetup) / (wao - wcogs) if (wao - wcogs) > 0 else 0
            time_to_profit = cac_payback + 1
            
            # NPV calculation
            r = 0.0167  # monthly rate (20% annual)
            cf = cm
            npv = -wcac - wsetup
            for t in range(1, int(avg_life) + 1):
                npv += cf / (1 + r) ** t
            
            # MRR and other growth metrics
            mrr = wao * self.growth_plan['year1_clients'][prod_idx]
            expansion = 0.10  # 10% expansion rate
            nrr = (1 + expansion - wchurn) * 100
            cae = wao / (self.opex['Маркетинг'] / sum(self.growth_plan['year1_clients']))
            
            results.append({
                'product': product,
                'wao': wao,
                'wcogs': wcogs,
                'wcac': wcac,
                'wsetup': wsetup,
                'avg_life': avg_life,
                'wchurn': wchurn,
                'gm': gm,
                'ltr': ltr,
                'ltc': ltc,
                'ltv': ltv,
                'ltv_cac': ltv_cac,
                'margin': margin,
                'cm': cm,
                'cac_payback': cac_payback,
                'time_to_profit': time_to_profit,
                'npv': npv,
                'mrr': mrr,
                'nrr': nrr,
                'cae': cae
            })
        
        return results

    def generate_input_table(self) -> pd.DataFrame:
        """Создание таблицы входных данных"""
        rows = []
        
        # Добавление AOV
        for segment in self.segments:
            for prod_idx, product in enumerate(self.products):
                if self.input_data['aov'][segment][prod_idx] is not None:
                    rows.append({
                        'Метрика': f'AOV {segment}',
                        'Обозначение': f'AOV_{segment[0]}',
                        'Unit': 'eur',
                        'Продукт': product,
                        'Значение': self.input_data['aov'][segment][prod_idx]
                    })
        
        # Добавление Distribution
        for segment in self.segments:
            for prod_idx, product in enumerate(self.products):
                rows.append({
                    'Метрика': f'Distribution {segment}',
                    'Обозначение': f'Dist_{segment[0]}',
                    'Unit': '%',
                    'Продукт': product,
                    'Значение': self.input_data['distribution'][segment][prod_idx] * 100
                })
        
        # Добавление остальных метрик
        metrics = {
            'cogs': ('COGS', 'eur'),
            'lifetime': ('Lifetime', 'month'),
            'cac': ('CAC', 'eur'),
            'setup': ('Setup', 'eur'),
            'churn': ('Churn', '%')
        }
        
        for metric, (name, unit) in metrics.items():
            for segment in self.segments:
                for prod_idx, product in enumerate(self.products):
                    if self.input_data[metric][segment][prod_idx] is not None:
                        value = self.input_data[metric][segment][prod_idx]
                        if metric == 'churn':
                            value *= 100
                        rows.append({
                            'Метрика': f'{name} {segment}',
                            'Обозначение': f'{name}_{segment[0]}',
                            'Unit': unit,
                            'Продукт': product,
                            'Значение': value
                        })
        
        # Добавление OPEX
        for opex_name, value in self.opex.items():
            rows.append({
                'Метрика': f'OPEX {opex_name}',
                'Обозначение': 'OPEX',
                'Unit': 'eur',
                'Продукт': 'All',
                'Значение': value
            })
        
        return pd.DataFrame(rows)

    def generate_calculated_metrics_table(self) -> pd.DataFrame:
        """Создание таблицы расчетных показателей"""
        results = self.calculate_weighted_metrics()
        
        # Преобразование списка словарей в DataFrame
        df = pd.DataFrame(results)
        
        # Переименование колонок
        column_mapping = {
            'product': 'Продукт',
            'wao': 'Средний чек (WAO)',
            'wcogs': 'Средний COGS',
            'wcac': 'Customer Acquisition Cost (CAC)',
            'wsetup': 'Средние затраты на внедрение',
            'avg_life': 'Средний срок жизни',
            'wchurn': 'Средний месячный Churn',
            'gm': 'Gross Margin',
            'ltr': 'Выручка за жизненный цикл',
            'ltc': 'Затраты за жизненный цикл',
            'ltv': 'Customer Lifetime Value',
            'ltv_cac': 'LTV/CAC Ratio',
            'margin': 'Маржинальность (%)',
            'cm': 'Contribution Margin',
            'cac_payback': 'CAC Payback Period',
            'time_to_profit': 'Time to Profit',
            'npv': 'NPV на клиента',
            'mrr': 'Monthly Recurring Revenue',
            'nrr': 'Net Revenue Retention',
            'cae': 'Customer Acquisition Efficiency'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Форматирование числовых значений
        format_rules = {
            'Средний чек (WAO)': '€{:.0f}',
            'Средний COGS': '€{:.0f}',
            'Customer Acquisition Cost (CAC)': '€{:.0f}',
            'Средние затраты на внедрение': '€{:.0f}',
            'Средний срок жизни': '{:.0f}',
            'Средний месячный Churn': '{:.1%}',
            'Gross Margin': '{:.1%}',
            'Выручка за жизненный цикл': '€{:.0f}',
            'Затраты за жизненный цикл': '€{:.0f}',
            'Customer Lifetime Value': '€{:.0f}',
            'LTV/CAC Ratio': '{:.1f}',
            'Маржинальность (%)': '{:.1%}',
            'Contribution Margin': '€{:.0f}',
            'CAC Payback Period': '{:.1f}',
            'Time to Profit': '{:.1f}',
            'NPV на клиента': '€{:.0f}',
            'Monthly Recurring Revenue': '€{:.0f}',
            'Net Revenue Retention': '{:.1%}',
            'Customer Acquisition Efficiency': '{:.2f}'
        }
        
        for column, format_str in format_rules.items():
            if column in df.columns:
                df[column] = df[column].apply(lambda x: format_str.format(x))
        
        return df

    def export_to_csv(self):
        """Экспорт результатов в CSV файлы"""
        self.generate_input_table().to_csv('input_data.csv', index=False)
        self.generate_calculated_metrics_table().to_csv('calculated_metrics.csv', index=False)

# Использование
if __name__ == "__main__":
    calculator = UnitEconomicsCalculator()
    calculator.export_to_csv()
    print("Анализ юнит-экономики сохранен в файлы input_data.csv и calculated_metrics.csv")