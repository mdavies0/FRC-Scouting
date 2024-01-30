import tbapy
import pyperclip

event = input("Enter the event key: ")

def getEventMatchTeams(key):
    tba = tbapy.TBA('KiFI9IObf1xbtTKuLzSu6clL006qHK1Lh5Xy65i1zSDutDcvsYJWwliU1svWKVzX')
    matches = tba.event_matches(key, simple=True)
    # set matches to be only keys of red and blue alliances
    alliances = []
    for match in matches:
        if match['comp_level'] == 'qm':
            alliances.append({'match_num': match['match_number'], 'red': match['alliances']['red']['team_keys'], 'blue': match['alliances']['blue']['team_keys']})

            #trim 'frc' from team keys
            alliances[-1]['red'][0] = alliances[-1]['red'][0][3:]
            alliances[-1]['red'][1] = alliances[-1]['red'][1][3:]
            alliances[-1]['red'][2] = alliances[-1]['red'][2][3:]
            alliances[-1]['blue'][0] = alliances[-1]['blue'][0][3:]
            alliances[-1]['blue'][1] = alliances[-1]['blue'][1][3:]
            alliances[-1]['blue'][2] = alliances[-1]['blue'][2][3:]
        
    alliances.sort(key=lambda x: x['match_num'])
    
    #delete match_num key
    for match in alliances:
        del match['match_num']
    
    return alliances

teams = getEventMatchTeams(event)
print("\n" + str(teams))
pyperclip.copy(str(teams))
input("\n\033[1m\033[92mCopied to clipboard!\033[0m\n\nPress any key to continue.")