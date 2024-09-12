import re, urllib, sys
import urllib.parse

class NOSJ_Parser():
    def __init__(self, data) -> None:
        self.data = data.strip() #whitespace is allowed before and after so get rid of it in case 

    def parse(self, data=None):
        if not data:
            data = self.data
        if self._is_map(data):
            return self._parse_map(data)
        elif self._is_num(data):
            return self._parse_num(data)
        elif self._is_simple_string(data):
            return self._parse_simple_string(data)
        elif self._is_complex_string(data):
            return self._parse_complex_string(data)
        #if not an expected type
        else:
            self._throw_error(f"Invalid NOSJ data format: {' '.join(data.splitlines())} did not match any known types.")
    
    def print_parsed_data(self, data=None):
        if type(data) == dict:
            print("begin-map", file=sys.stdout)
            for key, value in data.items():
                if type(value) == dict:
                    print(f"{key} -- map -- ", file=sys.stdout)
                    self.print_parsed_data(value)
                else:
                    print(f"{key} -- {self._get_type(value)} -- {value}", file=sys.stdout)
            print("end-map", file=sys.stdout)
        else:
            print(f"{data} -- {self._get_type(data)} -- {data}", file=sys.stdout)
        
    def _throw_error(self, message):
        print(f"ERROR -- {message}", file=sys.stderr)
        sys.exit(66)

    def _get_type(self, data):
        if type(data) == int:
            return "num"
        elif type(data) == dict:
            return "map"
        elif type(data) == str:
            return "string"
        else:
            self._throw_error("Invalid data type")            

    def _parse_map(self, data):
        data = data[2:-2]
        map = {}
        pairs = self._split_pairs(data)
        for pair in pairs:
            key, value = pair.split(':', 1)
            key = self._parse_map_key(key)
            value = self.parse(value)
            map[key] = value
        return map

    def _parse_num(self, data):
        value = int(data, 2)
        if data[0] == '1':
            value -= (1 << len(data))
        return value
    
    def _parse_map_key(self, data):
        if not re.match(r'^[a-z]+$', data):
            self._throw_error(f"Invalid map key: '{data}'")
        else:
            return data
        
    def _parse_simple_string(self, data):
        return data[:-1]
    
    def _parse_complex_string(self, data):
        if "%20" in data or "%09" in data or "%0a" in data:
            self._throw_error("Invalid complex string value. Whitespace characters are not allowed.")
        return urllib.parse.unquote(data)
    
    def _is_num(self, data):
        return re.match(r'^[01]+$', data) is not None
    
    def _is_map(self, data):
        return data.startswith("(<") and data.endswith(">)")
    
    def _is_simple_string(self, data):
        return data.endswith('s') and re.match(r'^[^s]*s$', data) is not None
    
    def _is_complex_string(self, data):
        return '%' in data and re.match(r'^[A-Za-z0-9%]+$', data) is not None
    
    def _split_pairs(self, data):
        # Split key-value pairs in a map, taking nested maps into account
        pairs = []
        depth = 0
        current_pair = []
        for char in data:
            if char == '(' and data[data.index(char)+1] == '<':
                depth += 1
            elif char == ')' and data[data.index(char)-1] == '>':
                depth -= 1

            if char == ',' and depth == 0:
                pairs.append(''.join(current_pair))
                current_pair = []
            else:
                current_pair.append(char)

        pairs.append(''.join(current_pair))
        return pairs

