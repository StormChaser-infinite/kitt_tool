import re

check_list = ["create view", "create function", "create procedure"]

def _read_sql_file(filename: str):
    """Read the uploaded SQL file,"""
    try:
        with open(filename,  encoding='utf-8') as f:
            lines = f.readlines()
            return lines
    except: 
        try:
            with open(filename,  encoding='utf-16') as f:
                lines = f.readlines() 
                return lines
        except Exception as e:
            print(f"The input file {filename} cannot open!")


def _split_sql_input(filename: str, output_path: str):
    """Split the uploaded SQL file, if it contains more than one SP/Functions/Views then the SQL script will be split into individual txt file"""
    try:
        sql_lines = _read_sql_file(filename)
        counts = 0
        for i in sql_lines:
            if i.lower().strip().startswith(check_list[0]) or i.lower().strip().startswith(check_list[1]) or i.lower().strip().startswith(check_list[2]):
                counts = counts + 1

        if counts == 0:
            print(f"The file {filename} couldnot find any Stored Procedures, functions or views!" )
        elif counts == 1: 
            print(f'There is only one SP/Function/View in the SQL script, no need to split the file!')
            _export_txt_file(sql_lines, output_path)  
        else:
            print(f'There are {counts} SPs/Functions/Views in the SLQ Script!')
            indexes = [index for index in range(len(sql_lines)) if sql_lines[index].lower() == 'SET ANSI_NULLS ON\n'.lower()]
            if indexes == 0:
                print(f"The file contains SP/Functions/Views, but the sytax might be incorrect!")
            else:
                count_output = 0
                for i in range(0, len(indexes)):
                    if i < len(indexes) - 1:
                        sql = sql_lines[indexes[i]-2:indexes[i+1]-2]
                        _export_txt_file(sql, output_path)
                        count_output = count_output + 1
                    else:
                        sql = sql_lines[indexes[i]-2:-1]
                        _export_txt_file(sql, output_path)
                        count_output = count_output + 1
                print(f"There are {count_output} SPs/Functions/Views which were exported into txt files!")
    except Exception as e:
        print(f'The SQL scripts did not split successfully because {e}.')
                         
def _export_txt_file(sql_section: list, output_folder: str):
    """Exported the split SQL script into txt files """
    try:
        for s in sql_section:
            if s.lower().strip().startswith(check_list[0]) or s.lower().strip().startswith(check_list[1]) or s.lower().strip().startswith(check_list[2]):
                end_index = [e for e, n in enumerate(list(s)) if n == ']'][1]
                file_name = re.sub("[\W_]+"," ", ' '.join([t.lower() for t in s[0:end_index].strip().split(" ")])).replace(" ", "_")
                
        output_file = output_folder + file_name + '.txt'
        with open(output_file, 'w') as fp:
            for item in sql_section:
                fp.write(item)
            fp.close() 
    except Exception as e:
        print(f'The name cannot be found for the SP/Function/View! Because {e}')


def main():
    output_path = 'C:\\Users\\lilisun1\\kiwibank\\SQLs\\'
    input_file = r"C:\Users\lilisun1\kiwibank\LiquidityDB_procs_views_functions.sql"
    _split_sql_input(input_file,output_path )



main()


    