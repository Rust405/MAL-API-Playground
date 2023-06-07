import os
import requests
import urllib

base_url = 'https://api.myanimelist.net/v2/'
client_id = '95d31dfcde4bee587d28ab0b1f0aaaf8'
auth = {'X-MAL-CLIENT-ID': client_id}

def menu():
    os.system('cls')

    title = 'MAL API Playground'

    print(title)
    print('-'*len(title))

    print()
    print('(1) Search anime by name')
    print('(2) Top 10 anime')
    print('(3) Search manga by name')
    print('(4) Top 10 manga')

    print('(x) Exit')

    choice = input('\nOption: ')

    match choice:
        case '1':
            searchByName('anime')
        case '2':
           topAnimeMenu()
        case '3':
            searchByName('manga')
        case '4':
           topMangaMenu()
        case 'x':
            print()
            os.system('pause')
            os.system('cls')
            os.system('exit')
        case _:
           menu()

def topAnimeMenu():
    os.system('cls')

    title = 'Top 10 Anime'

    print(title)
    print('-'*len(title))

    print('(1) Airing')
    print('(2) Upcoming')
    print('(3) Popular')
    print('(4) All Time')
    print('(5) Movies')
    print('(x) Main Menu')

    choice = input('\nOption: ')

    match choice:
        case '1':
            getTop('airing','anime', 'Airing Anime')
        case '2': 
            getTop('upcoming', 'anime','Upcoming Anime')
        case '3': 
            getTop('bypopularity', 'anime','Anime by Popularity')
        case '4':
            getTop('all', 'anime','Anime Of All Time')
        case '5':
            getTop('movie','anime', 'Anime Movies')
        case 'x':
            menu()
        case _:
           topAnimeMenu()

def topMangaMenu():
    os.system('cls')

    title = 'Top 10 Manga'

    print(title)
    print('-'*len(title))
    print('(1) Manga')
    print('(2) Doujinshi')
    print('(3) One-shots')
    print('(4) Popular')
    print('(5) All Time')
    print('(x) Main Menu')

    choice = input('\nOption: ')

    match choice:
        case '1':
            getTop('manga', 'manga', 'Manga')
        case '2': 
            getTop('doujin','manga', 'Doujinshi')
        case '3': 
            getTop('oneshots','manga', 'One-shots')
        case '4':
            getTop('bypopularity','manga', 'Manga by Popularity')
        case '5':
            getTop('all','manga','Manga Of All Time')
        case 'x':
            menu()
        case _:
           topAnimeMenu()

def searchByName(option):
    os.system('cls')

    searchValue = input('Search '+ option +' by name: ')

    param = urllib.parse.urlencode({'q': searchValue , 'limit' : '6'})

    searchResponse = requests.get(base_url + option + '?'+ param, headers = auth )

    search_data = searchResponse.json().get('data')

    if len(search_data )==0:
        print('\nNot Found!')
    else:
        id = str(search_data[0]['node']['id'])

        detailResponse = getDetails(id, option)

        print('\nSearch Result:')

        displayDetails(detailResponse.json(),option)

        del search_data[0]

        print('\nAlternative Results:')

        for idx, entry in enumerate(search_data):
            print('\t' + str(idx + 1) + '. ' + entry['node']['title'])

    fineSelect = ''

    print()
    while (fineSelect.isdigit() == True and (int(fineSelect) > len(search_data) or int(fineSelect) < 1)) or (fineSelect.isdigit() == False and (fineSelect != 'y' and fineSelect != 'n')):
        fineSelect = input('Select to view (1-' + str(len(search_data)) + ') or \'y\' to search again or \'n\' to return to main menu: ')

    match fineSelect:
        case 'y':
            searchByName(option)
        case 'n':
            menu()
        case _:
            os.system('cls')

            print('Selected ' + option + ': ' + search_data[(int(fineSelect)-1)]['node']['title'])
            
            detailResponse = getDetails(str(search_data[(int(fineSelect)-1)]['node']['id']), option)
            displayDetails(detailResponse.json(),option)

            searchAgain = ''

            while searchAgain != 'y' and searchAgain != 'n':
                searchAgain = input('\nSearch again (y/n): ')

            match searchAgain:
                case 'y':
                    searchByName(option)
                case 'n':
                    menu()


def getTop(ranking_type , option , title):
    os.system('cls')

    param = urllib.parse.urlencode({'ranking_type': ranking_type , 'limit' : '10'})

    getResponse = requests.get(base_url + option + '/ranking?' + param, headers = auth)

    res = getResponse.json().get('data')

    print('Top 10 ' + title + ':\n')

    for idx, entry in enumerate(res):
        print(str(idx + 1) + '. ' + entry['node']['title'])
        
    print()

    select = input('Select to view (1-10) or \'x\' to return to top 10 menu: ')

    while (select.isdigit() == True and (int(select) > 10 or int(select) < 1)) or (select.isdigit() == False and select != 'x'):
        select = input('Select to view (1-10) or \'x\' to return to top 10 menu: ')

    if select == 'x':
        if option == 'anime':
            topAnimeMenu()
        elif option == 'manga':
            topMangaMenu()
    else:       
        os.system('cls')
        detailResponse = getDetails(str(res[(int(select)-1)]['node']['id']), option)
        displayDetails(detailResponse.json(), option)

        print()
        os.system('pause')
        menu()

def getDetails(id, option) :
    fields  = 'title,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_scoring_users,media_type,status,genres,'
    animeFields = 'num_episodes,start_season,broadcast,source,average_episode_duration,rating,studios'
    mangaFields = 'num_volumes,num_chapters,serialization,authors{first_name,last_name}'

    detail_url = base_url + option + '/' + id + '?fields=' + fields +  (animeFields if option == 'anime' else mangaFields)
    return requests.get(detail_url, headers = auth)

def displayDetails(details, option):
    print('\n' +  details['title']  + ' (' + details['alternative_titles']['ja'] + ')')

    print()
    print('Score     : ' + ('?' if details.get('mean') is  None else str(details['mean']) + ' according to ' + str(details['num_scoring_users']) + ' users'))
    print('Rank      : #' + ('?'  if details.get('rank') is None else str(details['rank'])))
    print('Popularity: #' + str(details['popularity']))
    print('\nSynopsis  :\n' + ('?' if details.get('synopsis') is None else details['synopsis']))

    print()
    if option == 'anime':
        print('Media Type: ' + ('?' if details.get('media_type') is None else details['media_type'].upper()))
        print('Episodes  : ' + str(details['num_episodes']))
        print('Status    : ' + details['status'].replace('_', ' ').title())
        print('Aired     : ' + ('?' if details.get('start_date') is None else details['start_date']) + ' to ' +  ('?' if details.get('end_date') is None else details['end_date']))
        print('Premiered : ' + ('?' if details.get('start_season') is None else details['start_season']['season'].title() + ' ' + str(details['start_season']['year'])))
        print('Broadcast : ' + ('?' if details.get('broadcast') is None else (details['broadcast']['day_of_the_week'] + 's').title() + ' at ' + details['broadcast']['start_time'] + ' (JST)'))
        print('Studios   : ' + ', '.join([studio['name'] for studio in details['studios']]))
        print('Source    : ' + details['source'].replace('_', ' ').title())
        print('Genres    : ' + ', '.join([genre['name'] for genre in details['genres']]))
        print('Duration  : ' + str(int((details['average_episode_duration'] / 60 ))) + '  min. per ep.')
        print('Rating    : ' + ('?' if details.get('rating') is None else details['rating'].replace('_', ' ').title()) )
    elif option == 'manga': 
        print('Media Type   : ' + ('?' if details.get('media_type') is None else details['media_type'].upper()))
        print('Volumes      : ' + str(details['num_volumes']))
        print('Chapters     : ' + str(details['num_chapters']))
        print('Status       : ' + details['status'].replace('_', ' ').title())
        print('Published    : ' + ('?' if details.get('start_date') is None else details['start_date']) + ' to ' +  ('?' if details.get('end_date') is None else details['end_date']))
        print('Genres       : ' + ', '.join([genre['name'] for genre in details['genres']]))
        print('Serialization: ' + ', '.join([serialization['node']['name'] for serialization in details['serialization']]))
        print('Authors      : ' + concatAuthors(details['authors']))

def concatAuthors(authors):
    fullNames = []
    
    for author in authors:
        fullNames.append(author['node']['last_name'] + ( ' ' + author['node']['first_name'] if author['node']['first_name'] != '' else ''))

    return ', '.join(fullNames)

menu()
