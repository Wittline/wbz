from typing_extensions import Self


class SqlEngine:

    def __init__(self, query):

        self.columns = None
        self.conditions = None
        self.partition_column = None
        self.q = query
        self.__query_parser()

    def __get_filters(self):
        pass

        
    
    def __query_parser(self):

        self.columns =  self.q['SELECT'].split(',')
        self.conditions = self.__get_filters(self.q['WHERE'])
        self.partition_column = self.q['PARTITIONS']


    def run_query(self, csvfile):

        
        return partitions 

        c = 
        
                   



