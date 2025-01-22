import pandas as pd
from typing import Dict, Any

class MarketSizeAnalysis:
    def __init__(self):
        # Инициализация базовых параметров по сегментам
        self.segments = {
            'enterprise': {
                'monthly_price': 5000,
                'companies_count': 1000,
                'adoption_rate': 0.3,
                'service_share': 0.4,
                'implementation_cost': 10000
            },
            'medium': {
                'monthly_price': 2000,
                'companies_count': 25000,
                'adoption_rate': 0.25,
                'service_share': 0.3,
                'implementation_cost': 5000
            },
            'small': {
                'monthly_price': 500,
                'companies_count': 150000,
                'adoption_rate': 0.15,
                'service_share': 0.2,
                'implementation_cost': 2000
            }
        }
        
        # Коэффициенты для расчетов
        self.coefficients = {
            'tech_ready_rate': 0.7,
            'market_share_2025': 0.05,
            'retention_rate': 0.9,
            'quarterly_growth': 1.5
        }

    def calculate_market_size(self) -> Dict[str, Any]:
        """
        Расчет размера рынка по сегментам и общий
        """
        results = {
            'by_segment': {},
            'total': 0
        }
        
        for segment, data in self.segments.items():
            # Расчет годовой выручки от подписки
            subscription_revenue = (
                data['companies_count'] * 
                data['monthly_price'] * 
                12
            )
            
            # Расчет выручки от услуг внедрения
            implementation_revenue = (
                data['companies_count'] * 
                data['implementation_cost'] * 
                data['adoption_rate']
            )
            
            # Расчет выручки от дополнительных услуг
            service_revenue = (
                subscription_revenue * 
                data['service_share']
            )
            
            segment_total = (
                subscription_revenue + 
                implementation_revenue + 
                service_revenue
            ) / 1_000_000  # конвертация в млн EUR
            
            results['by_segment'][segment] = segment_total
            results['total'] += segment_total
            
        return results

    def generate_input_table(self) -> pd.DataFrame:
        """
        Создание таблицы входных параметров
        """
        data = {
            'Название': [],
            'Сокращение': [],
            'Единица измерения': [],
            'Значение': [],
            'Источник данных': []
        }
        
        # Добавление параметров по сегментам
        for segment in ['enterprise', 'medium', 'small']:
            prefix = segment.capitalize()
            data['Название'].extend([
                f'{prefix} - Месячная стоимость',
                f'{prefix} - Количество компаний',
                f'{prefix} - Уровень адаптации',
                f'{prefix} - Доля сервисных услуг',
                f'{prefix} - Стоимость внедрения'
            ])
            
            data['Сокращение'].extend([
                f'P_{segment}',
                f'N_{segment}',
                f'AR_{segment}',
                f'SS_{segment}',
                f'IC_{segment}'
            ])
            
            data['Единица измерения'].extend([
                'EUR/мес',
                'компании',
                '%',
                '%',
                'EUR'
            ])
            
            segment_data = self.segments[segment]
            data['Значение'].extend([
                segment_data['monthly_price'],
                segment_data['companies_count'],
                segment_data['adoption_rate'] * 100,
                segment_data['service_share'] * 100,
                segment_data['implementation_cost']
            ])
            
            data['Источник данных'].extend([
                'Анализ конкурентов',
                'Исследование рынка',
                'Отраслевая статистика',
                'Экспертная оценка',
                'Анализ затрат'
            ])

        return pd.DataFrame(data)

    def generate_calculations_table(self) -> pd.DataFrame:
        """
        Создание таблицы расчетных показателей
        """
        market_size = self.calculate_market_size()
        
        data = {
            'Название': [
                'TAM - Общий объем рынка',
                'TAM - Enterprise сегмент',
                'TAM - Medium сегмент',
                'TAM - Small сегмент',
                'SAM - Доступный рынок',
                'SOM - Достижимый рынок 2025',
                'Выручка Q2 2025',
                'Выручка Q3 2025',
                'Выручка Q4 2025',
                'Выручка Q1 2026'
            ],
            'Сокращение': [
                'TAM_total',
                'TAM_ent',
                'TAM_med',
                'TAM_small',
                'SAM',
                'SOM',
                'REV_Q2_25',
                'REV_Q3_25',
                'REV_Q4_25',
                'REV_Q1_26'
            ],
            'Единица измерения': ['млн EUR'] * 10,
            'Значение': [
                round(market_size['total'], 2),
                round(market_size['by_segment']['enterprise'], 2),
                round(market_size['by_segment']['medium'], 2),
                round(market_size['by_segment']['small'], 2),
                round(market_size['total'] * self.coefficients['tech_ready_rate'], 2),
                round(market_size['total'] * self.coefficients['tech_ready_rate'] * 
                      self.coefficients['market_share_2025'], 2),
                # Квартальные показатели
                round(market_size['total'] * self.coefficients['tech_ready_rate'] * 
                      self.coefficients['market_share_2025'] * 0.2, 2),
                round(market_size['total'] * self.coefficients['tech_ready_rate'] * 
                      self.coefficients['market_share_2025'] * 0.2 * 1.5, 2),
                round(market_size['total'] * self.coefficients['tech_ready_rate'] * 
                      self.coefficients['market_share_2025'] * 0.2 * 1.5 * 1.5, 2),
                round(market_size['total'] * self.coefficients['tech_ready_rate'] * 
                      self.coefficients['market_share_2025'] * 0.2 * 1.5 * 1.5 * 1.5, 2)
            ],
            'Формула': [
                'Σ(TAM по сегментам)',
                'N_ent × P_ent × 12 + Implementation + Services',
                'N_med × P_med × 12 + Implementation + Services',
                'N_small × P_small × 12 + Implementation + Services',
                'TAM × Tech Ready Rate',
                'SAM × Market Share 2025',
                'SOM × 0.2',
                'Q2_2025 × 1.5',
                'Q3_2025 × 1.5',
                'Q4_2025 × 1.5'
            ]
        }
        
        return pd.DataFrame(data)

    def export_to_csv(self):
        """
        Экспорт таблиц в CSV файлы
        """
        input_table = self.generate_input_table()
        calc_table = self.generate_calculations_table()
        
        input_table.to_csv('market_size_inputs.csv', index=False, encoding='utf-8-sig')
        calc_table.to_csv('market_size_calculations.csv', index=False, encoding='utf-8-sig')
        
        print("Файлы сохранены:")
        print("- market_size_inputs.csv")
        print("- market_size_calculations.csv")

if __name__ == "__main__":
    analysis = MarketSizeAnalysis()
    analysis.export_to_csv() 