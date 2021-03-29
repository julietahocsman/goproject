
from goproject.neighbor import search_neighborhood
from goproject.download_data import download
from goproject.get_data import preproc
from sys import argv



def main():
    argc = len(argv)

    neighborhood = 'ciudad'

    if argc > 1:
        command = argv[1]
        if command == 'download':
            download('raw_data/API_gopa.json', 'raw_data/dataBackup.json')
        elif command == 'analyse':
            neighborhood = argv[2]
            coordinates = preproc('raw_data/dataBackup.json')
            search_neighborhood(neighborhood, coordinates)
        else:
            pass
    else:
        pass

if __name__ == '__main__':
    main()

