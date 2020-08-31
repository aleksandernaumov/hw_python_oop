import datetime as dt

class Record:
    def __init__(self, amount, comment, date=None):
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:             
            self.date = dt.datetime.now().date()
        self.amount = float(amount)
        self.comment = comment          
        
class Calculator:    
    def __init__(self, limit):
        self.limit=limit
        self.records = []                  

    def add_record(self, record):
        self.records.append(record)               

    def summ_records(self, dates):
        summ = 0        
        for date in dates:            
            for record in self.records:
                if date == record.date:
                    summ += record.amount               
        return summ

    def get_today_stats(self):
        current_day=dt.datetime.today().date()
        return self.summ_records([current_day])

    def get_week_stats(self):          
        week_days = []
        for one_date in range(0, 6):
            current_day = dt.datetime.today()
            period = dt.timedelta(days=one_date)
            week_day = current_day - period
            week_days.append(week_day.date())
        return self.summ_records(week_days)

class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    EURO_RATE = 88.74
    USD_RATE = 74.64
    
    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': 'руб',
            'eur': 'Euro',
            'usd': 'USD',
        }
        cash_balance = self.limit - self.get_today_stats()
        if currency == 'eur':
            cash_balance = round(cash_balance/self.EURO_RATE, 2)
        elif currency == 'usd':
            cash_balance = round(cash_balance/self.USD_RATE, 2)
        if cash_balance > 0:                
            return (f'На сегодня осталось {cash_balance} {currencies[currency]}')
        elif cash_balance < 0:
            cash_dept = -cash_balance
            return (f'Денег нет, держись: твой долг - {cash_dept} {currencies[currency]}')
        else:
            return (f'Денег нет, держись')

class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
    
    def get_calories_remained(self):
        calories_balance = int(self.limit - self.get_today_stats())
        if calories_balance > 0:                
            return (f'Сегодня можно съесть что-нибудь ещё, '
            'но с общей калорийностью не более '
            f'{calories_balance} кКал')      
        else:
            return (f'Хватит есть!')
                

cash_calculator = CashCalculator(1000)
calories_calculator = CaloriesCalculator(2000)
cash_calculator.add_record(Record(amount=145, date="08.03.2019", comment="Безудержный шопинг"))
cash_calculator.add_record(Record(amount=1645, date="28.08.2020", comment="Сумасшедший шопинг"))
cash_calculator.add_record(Record(amount=45, comment="Дешёвая колбаса"))
cash_calculator.add_record(Record(amount=3000, date="27.08.2020", comment="Любимый сыр"))
calories_calculator.add_record(Record(amount=200, comment="Съел корюшку"))
calories_calculator.add_record(Record(amount=500, date="25.08.2020", comment="Съел колюшку"))
calories_calculator.add_record(Record(amount=20, comment="Съел колючку"))

print('Калькулятор денег')
print('Сегодня потрачено рублей:')
print(cash_calculator.get_today_stats())
print('За 7 дней потрачено рублей:')
print(cash_calculator.get_week_stats())
print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_cash_remained('eur'))
print(cash_calculator.get_today_cash_remained('usd'))
print()
print('----------------------')
print()
print('Калькулятор калорий')
print('Сегодня съедено калорий:')
print(calories_calculator.get_today_stats())
print('За 7 дней съедено калорий:')
print(calories_calculator.get_week_stats())
print(calories_calculator.get_calories_remained())
