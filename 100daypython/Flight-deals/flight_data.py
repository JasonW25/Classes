class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = 0
        self.dep_city = ""
        self.dep_ap_iata = ""
        self.ar_city = ""
        self.ar_ap_iata = ""
        self.out_date = ""
        self.in_date = ""

    def set_price(self, price):
        self.price = price
    
    def set_dep_city(self, city):
        self.dep_city = city

    def set_dep_ap_iata(self, iata):
        self.dep_ap_iata = iata

    def set_ar_city(self, city):
        self.ar_city = city

    def set_ar_ap_iata(self, iata):
        self.ar_ap_iata = iata

    def set_out_date(self, date):
        self.out_date = date

    def set_in_date(self, date):
        self.in_date = date
