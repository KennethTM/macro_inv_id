import pickle
from os import path

dictionaries_path = path.abspath(path.join(path.dirname(__file__), "models", 'dictionaries.pickle'))

with open(dictionaries_path, 'rb') as src:
    dictionaries = pickle.load(src)

kgGroup6 = dictionaries.get("kgGroup6")
kgGroup4 = dictionaries.get("kgGroup4")
kgGroup2 = dictionaries.get("kgGroup2")
kgGroup1 = dictionaries.get("kgGroup1")
caenidaeKG2 = dictionaries.get("caenidaeKG2")
gammarusKG2 = dictionaries.get("gammarusKG2")
KG5oligochaeta = dictionaries.get("KG5oligochaeta")
KG5 = dictionaries.get("KG5")
simuliidaeKG2 = dictionaries.get("simuliidaeKG2")
setOfPositiveGrp = dictionaries.get("setOfPositiveGrp")
setOfNegativeGrp = dictionaries.get("setOfNegativeGrp")
listOfTrichoptera = dictionaries.get("listOfTrichoptera")

def calcDiversityScore(sample):
    
    # convert the list to distinct values
    distSample = list(set(sample))
    
    posGrpTaken = {}

    negGrpTaken = {}
    
    score = 0
    
    if sample.count('oligochaeta') >= 100:
        score -= 1
    
    # run through the sample
    for s in distSample:
        
        posFamilyName = setOfPositiveGrp.get(s)
        print('POS: we found ' + str(s) + ' in our sample and the family is ' + str(posFamilyName))
        
        negFamilyName = setOfNegativeGrp.get(s)
        print('NEG: we found ' + str(s) + ' in our sample and the family is ' + str(negFamilyName))
        
        # if it exists in the positive family list
        if posFamilyName is not None:
            print('Found familyname from the positive list')
            
            posTaken = posGrpTaken.get(posFamilyName)
            print('Check to see if this has already been found ' + str(posTaken))

            #If we have not seen it before
            if posTaken is None:
                print('We add to the plus score and we set the familyname as taken')
                score += 1
                posGrpTaken[posFamilyName] = s
            elif posTaken is not None:
                print('this has already been found!')
            print("\n\n")
        
        # if it exists in the negative family list
        elif negFamilyName is not None:
            print('Found familyname from the negative list')
            
            negTaken = negGrpTaken.get(negFamilyName)
            print('Check to see if this has already been found ' + str(negTaken))

            #If we have not seen it before
            if negTaken is None:
                print('We subtract to the score and we set the familyname as taken')
                score -= 1
                negGrpTaken[negFamilyName] = s
            elif negTaken is not None:
                print('this has already been found!')
            print("\n\n")
    
    return score

#Nøglegruppe 1 færdig
def keygroup1(sample, score):
    
    fixedList = []
    for s in sample:
        fixedList.append(kgGroup1.get(s))
    
    keygroup1 = ['brachyptera', 'capnia', 'leuctra', 'isogenus', 'isoperla', 'isoptena', 'perlodes', 'protonemura', 'siphonoperla', 'ephemera', 'limnius', 'glossosomatidae', 'sericostomatidae']
    
    sumOfGrp1 = 0
    
    for kg in keygroup1:
        if fixedList.count(kg) >= 2:
            sumOfGrp1 += 1

    if sumOfGrp1 >= 2:
        if score <= -2:
            return 0
        elif score >= -1 and score <= 3:
            return 5
        elif score >= 4 and score <= 9:
            return 6
        elif score >= 10:
            return 7
    elif sumOfGrp1 == 1:
        if score <= -2:
            return 0
        elif score >= -1 and score <= 3:
            return 4
        elif score >= 4 and score <= 9:
            return 5
        elif score >= 10:
            return 6
        
    return 0

#Nøglegruppe 2 færdig
def keygroup2(sample, score):
    
    if sample.count('asellus') >= 5 or sample.count('asellus aquaticus') >= 5:
        return 0
    elif sample.count('chironomus') >= 5:
        return 0
    
    fixedList = []
    for s in sample:
        fixedList.append(kgGroup2.get(s))
    
    keygroup2 = ['amphinemura', 'taeniopteryx', 'ametropodidae', 'ephemerellidae,', 'heptageniidae', 'leptophlebiidae', 'siphlonuridae', 'elmis', 'elodes', 'rhyacophilidae', 'goeridae', 'ancylus'] 
    
    for kg in keygroup2:
        if fixedList.count(kg) >= 2:
            if score <= -2:
                return 4
            elif score >= -1 and score <= 3:
                return 4
            elif score >= 4 and score <= 9:
                return 5
            elif score >= 10:
                return 5
   
    return 0

#Nøglegruppe 3 mangler trichoptera
def keygroup3(sample, score):

    if sample.count('chironomus') >= 5:
        return 0

    enter = False
    
    fixedListGammarus = []
    for s in sample:
        fixedListGammarus.append(gammarusKG2.get(s))
    
    if fixedListGammarus.count('gammarus') >= 10:
        enter = True
    
    fixedListCaenidae = []
    for s in sample:
        fixedListCaenidae.append(caenidaeKG2.get(s))
    
    if fixedListCaenidae.count('caenidae') >= 2:
        enter = True
    
    keygroupTrichoptera = ['beraeidae', 'brachycentridae', 'ecnomidae', 'hydropsychidae', 'hydroptilidae', 
                           'lepidostomatidae', 'leptoceridae', 'limnephilidae', 'molannidae', 'odontoceridae',
                            'philopotamidae', 'phryganeidae', 'polycentropodidae', 'psychomyiidae', 'ptilocolepidae']
    
    fixedListTrichoptera = []
    for s in sample:
        fixedListTrichoptera.append(listOfTrichoptera.get(s))
    
    for trichoptera in keygroupTrichoptera:
        if fixedListTrichoptera.count(trichoptera) >= 5:
            enter = True
            break
    
    if enter:
        if score <= -2:
            return 3
        elif score >= -1 and score <= 3:
            return 4
        elif score >= 4 and score <= 9:
            return 4
        elif score >= 10:
            return 4
   
    return 0

#Nøglegruppe 4 manger trichoptera
def keygroup4(sample, score):

    enter = 0
    
    fixedListGammarus = []
    for s in sample:
        fixedListGammarus.append(gammarusKG2.get(s))
    
    if fixedListGammarus.count('gammarus') >= 10:
        enter += 1
    
    keygroupTrichoptera = ['beraeidae', 'brachycentridae', 'ecnomidae', 'hydropsychidae', 'hydroptilidae', 
                           'lepidostomatidae', 'leptoceridae', 'limnephilidae', 'molannidae', 'odontoceridae',
                            'philopotamidae', 'phryganeidae', 'polycentropodidae', 'psychomyiidae', 'ptilocolepidae']

    fixedListTrichoptera = []
    for s in sample:
        fixedListTrichoptera.append(listOfTrichoptera.get(s))
    
    for trichoptera in keygroupTrichoptera:
        if fixedListTrichoptera.count(trichoptera) >= 2:
            enter += 1
    
    fixedListKG4 = []
    for s in sample:
        fixedListKG4.append(kgGroup4.get(s))
    
    for kg4 in fixedListKG4:
        if sample.count(kg4) >= 2:
            enter += 1        
    
    if enter >= 2:
        if score <= -2:
            return 3
        elif score >= -1 and score <= 3:
            return 3
        elif score >= 4 and score <= 9:
            return 4
        elif score >= 10:
            return 0
        
    if enter == 1:
        if score <= -2:
            return 2
        elif score >= -1 and score <= 3:
            return 3
        elif score >= 4 and score <= 9:
            return 3
        elif score >= 10:
            return 0
        
    return 0

#Nøglegruppe 5 færdig
def keygroup5(sample, score):

    if sample.count('eristalis') >= 2:
        return 0
    
    keygroup5 = ['gammarus', 'baetidae']
    
    enter = 0

    #KG5
    fixedListKG5 = []
    for s in sample:
        fixedListKG5.append(KG5.get(s))
    
    for kg in keygroup5:
        if fixedListKG5.count(kg) >= 2:
            enter += 1
    
    fixedListKG5simuliidae = []
    for s in sample:
        fixedListKG5simuliidae.append(simuliidaeKG2.get(s))
    
    if fixedListKG5.count('simuliidae') >= 25:
        enter += 1
    
    fixedListKG5oligochaeta = []
    for s in sample:
        fixedListKG5oligochaeta.append(KG5oligochaeta.get(s))
    
    if fixedListKG5oligochaeta.count('oligochaeta') >= 100 or enter == 1:
        if score <= -2:
            return 2
        elif score >= -1 and score <= 3:
            return 2
        elif score >= 4 and score <= 9:
            return 3
        elif score >= 10:
            return 0
    elif enter >= 2:
        if score <= -2:
            return 2
        elif score >= -1 and score <= 3:
            return 3
        elif score >= 4 and score <= 9:
            return 3
        elif score >= 10:
            return 0
    return 0

#Nøglegruppe 6 færdig
def keygroup6(sample, score):
    keygroup6 = ['tubificidae', 'psychoidae', 'chironomidae', 'eristalis']  
    
    fixedListKGGroup6 = []
    for s in sample:
        fixedListKGGroup6.append(kgGroup6.get(s))
    
    for kg in keygroup6:
        if fixedListKGGroup6.count(kg) >= 2:
            if score <= -2:
                return 1
            elif score >= -1 and score <= 3:
                return 1
            elif score >= 4 and score <= 9:
                return 0
            elif score >= 10:
                return 0
    return 0

#Nøglegruppe 7 færdig
def keygroup7(score):
    if score <= -2:
        return 1
    return 0

def DVFI(sample):
    diversityScore = calcDiversityScore(sample)
    print('Diversitetsgrupper: ' + str(diversityScore))
    
    kgRes1 = keygroup1(sample, diversityScore)
    print('Nøglegruppe 1: ' + str(kgRes1))
    if kgRes1 != 0:
        return kgRes1, 1, diversityScore

    kgRes2 = keygroup2(sample, diversityScore)
    print('Nøglegruppe 2: ' + str(kgRes2))
    if kgRes2 != 0:
        return kgRes2, 2, diversityScore

    kgRes3 = keygroup3(sample, diversityScore)
    print('Nøglegruppe 3: ' + str(kgRes3))
    if kgRes3 != 0:
        return kgRes3, 3, diversityScore
    
    kgRes4 = keygroup4(sample, diversityScore)
    print('Nøglegruppe 4: ' + str(kgRes4))
    if kgRes4 != 0:
        return kgRes4, 4, diversityScore

    kgRes5 = keygroup5(sample, diversityScore)
    print('Nøglegruppe 5: ' + str(kgRes5))
    if kgRes5 != 0:
        return kgRes5, 5, diversityScore

    kgRes6 = keygroup6(sample, diversityScore)
    print('Nøglegruppe 6: ' + str(kgRes6))
    if kgRes6 != 0:
        return kgRes6, 6, diversityScore

    kgRes7 = keygroup7(diversityScore)
    print('Nøglegruppe 7: ' + str(kgRes7))
    if kgRes7 != 0:
        return kgRes7, 7, diversityScore
    elif kgRes7 == 0:
        return "-", 7, diversityScore
