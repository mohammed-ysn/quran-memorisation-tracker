import quran_utils as qu


# TODO ensure revision ayah does not exceed the memorisation ayah (implement in qu.load_json)
# TODO create logbook.json if it does not exist
# TODO make next start memorisation ayah the previous end (to chain)
# TODO disambiguate var and key names

def main():
    filename = 'logbook.json'
    surahs_data = qu.load_json('quran_data.json')["surahs"]
    logbook = qu.load_json(filename)
    qu.print_ayah_range('revise', logbook, surahs_data)
    qu.print_ayah_range('memorise', logbook, surahs_data)
    to_update = input('Is the memorisation and revision complete? (y/n) ').strip().lower() == 'y'
    if to_update:
        qu.update_logbook("revise", logbook, surahs_data, filename)
        qu.update_logbook("memorise", logbook, surahs_data, filename)
        print('Logbook updated successfully')
    input('Press ENTER to exit...')


if __name__ == "__main__":
    main()
