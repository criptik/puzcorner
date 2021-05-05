import csv
import numpy as np

  
# opening the file using "with" 
# statement
CHeads = ["Please indicate the number of attendees 13 and older",
          "Please indicate the number of attendees aged 6-12, if any",
          "Please indicate the number of attendees aged 5 or less, if any"
          ]
CHeadNoKids = "Please indicate the number of adult attendees"

class RsvpRec:
    def __init__(self, name, counts):
        self.counts = counts
        nameWords = name.split(' ')
        fixedNameWords = []
        for word in nameWords:
            if len(word) > 1:
                fixedNameWords.append(word[0] + word[1:].lower())
            else:
                fixedNameWords.append(word)
                
        self.nameFirst = ' '.join(fixedNameWords[:-1])
        self.nameLast = fixedNameWords[-1]
    
def lineCol(line, head):
    txt = line.get(head, '0')
    return int(txt) if txt.isnumeric() else 0

def getCounts(line):
    C = []
    heads = CHeads
    if CHeadNoKids in line.keys():
        heads[0] = CHeadNoKids
    for head in heads:
        C.append(lineCol(line,head))
    return C
    
def byLast(rsvp):
    return f'{rsvp.nameLast}, {rsvp.nameFirst}'

# counts of each age group as an array
filenames = ['normal.csv', 'nokids.csv']

linecount = 0
allRsvps = []
for filename in filenames:
    # print(f'\nprocessing {filename}...')
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            name = line['Name']
            email = line['Email Address']
            if name == 'Totals':
                continue
            linecount += 1
            # do the known fixups
            if name == 'Jumhoor Rashid':
                C = [1, 0, 0]
            elif name == 'Kristin Davey':
                C = [1, 2, 0]
            else:
                # normal parsing
                C = getCounts(line)

            allRsvps.append(RsvpRec(name, C))

ageTots = [0, 0, 0]
totAll = 0

for rsvp in sorted(allRsvps, key=byLast):    
    for n in range(3):
        ageTots[n] += rsvp.counts[n]
        totAll += rsvp.counts[n]
    # print(f'{name:35} {email:35} {C}')
    fullName = f'{rsvp.nameFirst} {rsvp.nameLast}'
    print(f'{fullName:35} {rsvp.counts}')

numInvites = 53
rsvpPct = linecount * 100 / numInvites
print(f'{linecount} RSVPs from {numInvites} invites ({rsvpPct:.1f}%) totalling {ageTots} = {totAll} all ages')
    
        
