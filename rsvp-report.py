import csv
import numpy as np


ageTots = [0, 0, 0]
totAll = 0
linecount = 0


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
                fixedNameWords.append(word[0].upper() + word[1:].lower())
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

def processRsvpList(rsvpList):
    global linecount, totAll, ageTots
    for rsvp in sorted(rsvpList, key=byLast):    
        linecount += 1
        for n in range(3):
            ageTots[n] += rsvp.counts[n]
            totAll += rsvp.counts[n]
        # print(f'{name:35} {email:35} {C}')
        fullName = f'{rsvp.nameFirst} {rsvp.nameLast}'
        print(f'{fullName:35} {rsvp.counts}')

def printRsvpSummary(linecount, ageTots, intro=''):
    numInvites = 54
    rsvpPct = linecount * 100 / numInvites
    print(f'{intro}{linecount} RSVPs from {numInvites} invites ({rsvpPct:.0f}%) totalling {ageTots} = {sum(ageTots)} all ages')

    
# counts of each age group as an array
filenames = ['normal.csv', 'nokids.csv']

posRsvps = []
negRsvps = []
for filename in filenames:
    # print(f'\nprocessing {filename}...')
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            name = line['Name']
            email = line['Email Address']
            if email == 'kennethdeneau@gmail.com':
                name = 'Kenneth Jr. Deneau'
            if name == 'Totals':
                continue
            # now fixups not necessary because can edit rsvp response
            knownFixups = {
                'Jumhoor Rashid' : [1, 0, 0],
                'Kristin Davey'  : [1, 2, 0],
                'Philip Deneau'  : [1, 0, 0],
                'Cheryl Young'   : [2, 0, 0],
                }
            if False and name in knownFixups.keys():
                C = knownFixups[name]
            else:
                # normal parsing
                C = getCounts(line)

            rec = RsvpRec(name, C)
            if C == [0, 0, 0]:
                negRsvps.append(rec)
            else:
                posRsvps.append(rec)

rsvpTypes = [
    [posRsvps, 'Positive'],
    [negRsvps, 'Negative'],
    ]

for (rsvpList, str) in rsvpTypes:
    print(f'\nRSVPs {str}')
    print('--------------')
    processRsvpList(rsvpList)
    
printRsvpSummary(linecount, ageTots)

expectedYes = [
    RsvpRec('Alex Carson', [1, 0, 0]),
    RsvpRec('Sarah Horton', [2, 0, 0]),
    RsvpRec('Lali Cheema',  [1, 0, 0]),
    ]

print(f'\nExpected or Verbal Yes but No RSVP Yet')
print('---------------------------')
processRsvpList(expectedYes)
if False:
    printRsvpSummary(linecount, ageTots)

expectedNoNames = [
    'Jaiah Rashid',
    'Chris Deneau', 
    'Sikander and Darcy Rashid',
    'Nadir and Marguerite Rashid',
    'Robia Rashid and Mike Oppenhuizen',
    'Eli and Arooj Simmons',
    'Tashfeen and Fiona Rashid',
    'Pastor Martin and Teresa Danner',
    ]

expectedNo = []
for name in expectedNoNames:
    expectedNo.append(RsvpRec(name, [0, 0, 0]))
                      
print(f'\nExpected Or Verbal No but No RSVP Yet')
print('---------------------------')
processRsvpList(expectedNo)
printRsvpSummary(linecount, ageTots, 'Including all Expected, ')
        
