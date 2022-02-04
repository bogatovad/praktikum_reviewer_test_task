import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            # лучше dt.date.today()
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0

        # переменная-счетчик цикла не должна перекрывать имя класса Record
        # например, можно так: for record in self.records
        for Record in self.records:
            # лучше вынести определение даты: date_today = dt.datetime.now().date() выше
            # чтобы не пересчитывать одно и тоже выражение на каждой итерации цикла
            if Record.date == dt.datetime.now().date():

                # можно короче: today_stats += record.amount ( где имя record выбрано с учетом замечания выше )
                # также можно сократить код до 1 строчки использую метод sum() и передав ему список
                # с данными, см. https://www.python.org/dev/peps/pep-0289/
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0

        # вместо dt.datetime.now().date() лучше использовать dt.date.today(),
        # выглядит компактнее, результат тот же
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # такое условие можно записать короче, нарпимер так
                # week_ago <= record.date <= today
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                # тут можно собрать все данные в список а потом вернуть sum()
                # https://www.python.org/dev/peps/pep-0289/
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # имя переменной x ни о чем не говорит
        # по имени переменной должно быть понятно зачем она нужна в коде
        x = self.limit - self.get_today_stats()

        # тут компактнее было бы использование тернарного оператора
        # https://www.geeksforgeeks.org/ternary-operator-in-python/
        if x > 0:
            # лучше не использовать бэк-слэш, а использовать круглые скобки для переноса
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # тут скобки не нужны: return 'Хватит есть!'
            return('Хватит есть!')


class CashCalculator(Calculator):
    # float можно задать проще 60.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()

        # 1) эти блоки лучше вынести в отдельный метод convert_remaind(self, currency),
        # который по заданному currency вернет сконвертированный остаток
        # 2) что если нам передали неизвестную валюту?
        # можно завести словарик с валютами и проверять переданное значение по нему
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'

        # эти блоки лучше вынести в отдельный метод, который по cash_remained
        # вернет ответ
        if cash_remained > 0:
            # Все операции(логические, арифметические, округление и т.п.) должны выполняться вне f-строки,
            # в f-строке только подстановка определенной переменной.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # c нулем можно сравнивать короче: elif not cash_remained:...
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # тут нету смысла писать elif потому что 2 случая уже обработаны
        # когда остаток > 0 и == 0, значит сюда попадет все остальное
        # и можно просто вернуть строку
        elif cash_remained < 0:
            # лучше придерижваться единого стиля через f-строки
            # тут E128 по PEP8
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
