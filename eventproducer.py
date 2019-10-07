
import datetime
import random

from datetime import datetime
from datetime import timedelta

class EventProducer:
    _iso_date_format = "%Y-%m-%d"

    def _cast_iso_format_string_to_date(self, date_str):
        return datetime.strptime(date_str, self._iso_date_format).date()

    def __init__(self, config):
        self._average_purchase_hour = config["average_purchase_hour"]
        self._stdev_purchase_hour = config["stdev_purchase_hour"]
        self._average_price = config["average_price"]
        self._stdev_price = config["stdev_price"]
        self._product_categ_count = config["product_categ_count"]
        self._product_in_categ_count = config["product_in_categ_count"]

        min_date_str = config["min_purchase_iso_format_date"]
        min_date = self._cast_iso_format_string_to_date(min_date_str)
        self._min_purchase_date = min_date

        max_date_str = config["max_purchase_iso_format_date"]
        max_date = self._cast_iso_format_string_to_date(max_date_str)
        self._days_delta = (max_date - min_date).days


    def produce(self):
        result = dict()
        purchase_tm = self._random_purchase_date_str() + " " + self._random_normal_purchase_time_str()
        result["purchase_date"] = purchase_tm
        result["price"] = self._random_normal_price()
        result["ip"] = self._random_ip_address_str()

        prod = self._random_product_info()
        result["product_name"] = "product_{:04d}_{:04d}".format(prod[0], prod[1])
        result["product_category"] = "categ_{:04d}".format(prod[0])

        return result

    def _random_normal_price(self):
        return max(0.01, round(random.gauss(self._average_price, self._stdev_price), 2))
        
    def _random_purchase_date_str(self):
        dt = self._random_purchase_date()
        return dt.strftime(self._iso_date_format)

    def _random_product_info(self):
        categ_num = random.randint(1, self._product_categ_count)
        prod_id = random.randint(1, self._product_in_categ_count)
        return (categ_num, prod_id)

    def _random_purchase_date(self):
        random_offset = random.randrange(self._days_delta)
        return self._min_purchase_date + timedelta(random_offset)
    
    def _random_normal_purchase_time_str(self):
        hour_gauss_val = random.gauss(self._average_purchase_hour, self._stdev_purchase_hour)
        hour_val = min(23, max(int(hour_gauss_val), 0))
        minute_val = random.randint(0, 59)
        sec_val = random.randint(0, 59)
        return "{:02d}:{:02d}:{:02d}".format(hour_val, minute_val, sec_val)
    
    def _random_ip_address_str(self):
        block1 = random.randrange(1, 254)
        while (block1 == 10):
            block1 = random.randrange(1, 254)

        block2 = random.randrange(1, 254)
        while (block1 == 172 and block2 >= 16 and block2 <= 31) or (block1 == 192 and block2 == 168):
            block2 = random.randrange(1, 254)
        
        block3 = random.randrange(1, 254)
        block4 = random.randrange(1, 254)
        ip = ("{}.{}.{}.{}".format(block1, block2, block3, block4))
        return ip
        