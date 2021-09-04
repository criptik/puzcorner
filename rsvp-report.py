import csv
import numpy as np
import sys


ageTots = [0, 0, 0]
totAll = 0
linecount = 0
averyNames = []

# opening the file using "with" 
# statement
CHeads = ["Please indicate the number of attendees 13 and older",
          "Please indicate the number of attendees aged 6-12, if any",
          "Please indicate the number of attendees aged 5 or less, if any"
          ]
CHeadNoKids = "Please indicate the number of adult attendees"

# known fixups not necessary because can edit rsvp response
knownFixups = {
    'Jumhoor Rashid' : [1, 0, 0],
    'Kristin Davey'  : [1, 2, 0],
    'Philip Deneau'  : [1, 0, 0],
    'Cheryl Young'   : [2, 0, 0],
}

class RsvpRec:
    def __init__(self, name, counts, inviteName=None):
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
        self.inviteName = inviteName if inviteName is not None else f'using {name}'
        # generate attenders names
        self.attenders = []
        if sum(self.counts) > 0:
            iw = self.inviteName.split()
            if iw[0] == 'using':
                iw = iw[1:]
            if len(iw) >= 4 and iw[1].lower() == 'and':
                # format is "John and Mary Smith and xxx and yyy"
                self.addAttenderCond(iw[0], iw[3])
                self.addAttenderCond(iw[2], iw[3])
                n=4
                while n < len(iw):
                    if iw[n].lower() == 'and':
                        self.addAttenderCond(iw[n+1], iw[3])
                    n += 2    
            elif iw[1].lower() != 'and':
                # format is "Joe Smith and Mary Jones and xxx Jones and yyy Smith"
                self.addAttenderCond(iw[0], iw[1])
                if len(iw) >= 5 and iw[2].lower() == 'and':
                    self.addAttenderCond(iw[3], iw[4])
                    n=5
                    while n < len(iw):
                        if iw[n].lower() == 'and':
                            self.addAttenderCond(iw[n+1], iw[n+2])
                        n += 3    

    def addAttenderCond(self, first, second):
        if sum(self.counts) > len(self.attenders):
            self.attenders.append([first, second])
            
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
        if True:
            print(f'{fullName:35} {rsvp.counts}')
        else:
            print(f'{fullName:35} {rsvp.counts} --- {rsvp.inviteName}')
        for attender in rsvp.attenders:
            csNames = f'{attender[1]},{attender[0]}'
            # print(f' ATT: {csNames}')
            averyNames.append(csNames)
        if len(rsvp.attenders) != sum(rsvp.counts):
            print(f'ERROR: attenders list does not match counts')
            
def printRsvpSummary(linecount, ageTots, intro=''):
    numInvites = 54
    rsvpPct = linecount * 100 / numInvites
    print(f'{intro}{linecount} RSVPs from {numInvites} invites ({rsvpPct:.0f}%) totalling {ageTots} = {sum(ageTots)} all ages')


# the invite files that contain the fuller names related to email address
inviteFilenames = ['DinnerNames1.csv', 'DinnerNames1-nokids.csv']
inviteMap = {}
for filename in inviteFilenames:
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            inviteMap[line['Email']] = line['Name']

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
            if True:
                inviteName = inviteMap.get(email, f'{email} not Found in inviteMap, using {name}')
            if False and name in knownFixups.keys():
                C = knownFixups[name]
            else:
                # normal parsing
                C = getCounts(line)

            rec = RsvpRec(name, C, inviteName)
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
    RsvpRec('Sarah Horton', [1, 0, 0]),
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

def makeNonAttendee(name):
    return RsvpRec(name, [0, 0, 0])

expectedNoList = list(map(makeNonAttendee, expectedNoNames))
                      
print(f'\nExpected Or Verbal No but No RSVP Yet')
print('---------------------------')
processRsvpList(expectedNoList)
printRsvpSummary(linecount, ageTots, 'Including all Expected, ')


# finally generate the list of sorted names of actual attendees in csv format for Avery
averyOutFile = open('averyDinnerNames.csv', 'w')
print('LastName,FirstName', file=averyOutFile)
for attendee in sorted(averyNames):
    print(attendee, file=averyOutFile)




