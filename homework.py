import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:             
            self.date = dt.date.today()
        self.amount = amount
        self.comment = comment          
        
class Calculator:    
    def __init__(self, limit):
        self.limit=limit
        self.records = []
        self.current_day=dt.date.today()             

    def add_record(self, record):
        self.records.append(record)               

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if self.current_day == record.date:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self): 
        week_stats = 0       
        week_ago = self.current_day - dt.timedelta(weeks=1)
        for record in self.records:
            if self.current_day >= record.date >= week_ago:
                week_stats += record.amount
        return week_stats
    
    def balance_stats(self):
        balance = self.limit - self.get_today_stats()
        return balance

class CashCalculator(Calculator):
    RUB_RATE = 1
    EURO_RATE = 88.74
    USD_RATE = 74.64
    
    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': [self.RUB_RATE, 'руб'],
            'eur': [self.EURO_RATE, 'Euro'],
            'usd': [self.USD_RATE, 'USD']
        }

        if self.balance_stats() == 0:
            return ('Денег нет, держись')
        elif self.balance_stats() < 0:
            cash_balance = round(self.balance_stats()/
                           currencies[currency][0], 2) 
            cash_dept = abs(cash_balance)
            return ('Денег нет, держись: твой долг - '
                    f'{cash_dept} {currencies[currency][1]}')
        else:
            cash_balance = round(self.balance_stats()/
                           currencies[currency][0], 2)               
            return ('На сегодня осталось '
                    f'{cash_balance} {currencies[currency][1]}')        
  
class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_balance = self.balance_stats()

        if calories_balance > 0:                
            return ('Сегодня можно съесть что-нибудь ещё, '
                   'но с общей калорийностью не более '
                    f'{calories_balance} кКал')
        else:
            return ('Хватит есть!')
                
if __name__ == "__main__":    
    cash_calculator = CashCalculator(10)
    calories_calculator = CaloriesCalculator(2000)
    cash_calculator.add_record(Record(amount=145,date="08.03.2019",
                                      comment="Безудержный шопинг"))
    cash_calculator.add_record(Record(amount=1645, date="28.08.2020",
                                      comment="Сумасшедший шопинг"))
    cash_calculator.add_record(Record(amount=45,
                                      comment="Дешёвая колбаса"))
    cash_calculator.add_record(Record(amount=3000, date="27.08.2020",
                                      comment="Любимый сыр"))
    calories_calculator.add_record(Record(amount=200,
                                      comment="Съел корюшку"))
    calories_calculator.add_record(Record(amount=500,
                                      date="25.08.2020",
                                      comment="Съел колюшку"))
    calories_calculator.add_record(Record(amount=20,
                                      comment="Съел колючку"))
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