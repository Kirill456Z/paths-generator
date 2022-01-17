import overpy
import pickle


class ApiBuffer:
    dump_file: str = "last_q.dmp"

    def make_query(self, query: str) -> overpy.Result:
        api = overpy.Overpass()
        res = api.query(query)
        with open(self.dump_file, 'wb') as file:
            pickle.dump(res, file)
        return res

    def get_last_query(self) -> overpy.Result:
        try:
            with open(self.dump_file, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            raise BufferError("No query found, make a query first!")
