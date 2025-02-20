class CFPB:
    """This class helps you initialise perform operations on a Python class object called CFPB"""
    def __init__(self, base_url = None, name=None, creationTimeStamp=None,  modifiedTimeStamp=None, createdBy=None, modifiedBy=None, start_date=None, end_date=None, has_narrative=None, dataframes=[], profiles=[]) -> None:
        
        import datetime

        # Initialisation of attributes
        self.base_url = None
        self.name = None
        self.creationTimeStamp = None
        self.modifiedTimeStamp = None
        self.createdBy = None
        self.modifiedBy = None
        self.start_date = datetime.datetime.now()
        self.end_date = datetime.datetime.now()
        self.has_narrative = None
        self.dataframes = []
        self.profiles = []

        # Assign attributes based on what's passed

        self.base_url = base_url if base_url else "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
        self.name = name if name else self.name
        self.creationTimeStamp = creationTimeStamp if creationTimeStamp else datetime.datetime.now()
        self.modifiedTimeStamp = modifiedTimeStamp if modifiedTimeStamp else datetime.datetime.now()
        self.createdBy = createdBy if createdBy else self.createdBy
        self.modifiedBy = modifiedBy if modifiedBy else self.modifiedBy
        self.start_date = datetime.datetime.now() if start_date else self.start_date
        self.end_date = datetime.datetime.now() if end_date else self.end_date
        self.has_narrative = has_narrative if has_narrative else self.has_narrative
        self.dataframes = dataframes if dataframes else self.dataframes
        self.profiles = profiles if profiles else self.profiles

    def create_request_url(self,base_url, start_date, end_date, has_narrative):
        """This function creates a request URL based on the parameters passed"""
        request_url = base_url + "?format=json&date_received_min=" + start_date + "&date_received_max=" + end_date + "&has_narrative=" + has_narrative
        return request_url

    def get_data(self,request_url):
        """This function gets data from the request URL"""
        import requests
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            return response.status_code, {"error": "An error occurred while fetching data", "status_code": response.status_code, "reason": response.reason}
        
    def convert_data_to_dataframe(self,data):
        """This function converts data to a pandas dataframe"""
        import pandas as pd
        return pd.DataFrame(data)       
    
    def cluster(self):
        """This function clusters data based on the parameters passed"""
        pass
     
    def load(self, start_date=None, end_date=None, has_narrative=None):
        """This function loads data based on the parameters passed"""
        import datetime
        self.start_date = min(self.start_date, datetime.datetime.strptime(start_date, "%Y-%m-%d")) if start_date else self.start_date
        self.end_date = max(self.end_date, datetime.datetime.strptime(end_date, "%Y-%m-%d")) if end_date else self.end_date
        self.has_narrative = has_narrative if has_narrative else self.has_narrative
        request_url = self.create_request_url(self.base_url, start_date, end_date, has_narrative)
        status_code, data = self.get_data(request_url)
        print(status_code)
        if status_code == 200:
            dataframe = self.convert_data_to_dataframe([ob["_source"]for ob in data])
            self.dataframes.append(dataframe)
            print(f"Data frame of {len(data)} rows and {len(dataframe.columns)} columns loaded")
        else:
            print(data)

    def describe(self, dataframe_indicator=0):
        """This function returns a dataframe profile"""
        profile = self.dataframes[dataframe_indicator].describe().T
        profile["column_name"]=profile.index
        profile["id"]=list(range(0,len(profile.index)))
        profile.set_index("id", inplace=True)
        print(profile)
        self.profiles[dataframe_indicator]=profile
        pass
