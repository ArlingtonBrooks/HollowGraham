#Hollow Graham
#Personal Data Organizer

from os.path import expanduser
from os import replace
import json

home = expanduser("~")
objfile = home + "/.HollowGraham.obj"

def IsInt(test):
    try: 
        j = int(test)
        return True
    except ValueError: return False

def OpenFile(filename,mode):
    try: f = open(filename,mode)
    except:
        print("Could not open file.")
        return 0
    return f

def ParseCmd(cmd):
    print("Not yet implemented.")
    #Break command up into what ye want and execute relevant code;

def NewObject(obj,loc,tags = []):
    IDNum = 0
    f = OpenFile(objfile,"r") #Read whole file first.  Check for highest ID tag;
    Contents = f.read()
    f.close()
    Contents = Contents.splitlines()
    ContentsJSON = [] #List of all objects;
    for x in range(len(Contents)):
        print(Contents[x])
        ContentsJSON.append(json.loads(Contents[x]))

    #We now have contents loaded in JSON format;  We can work with this.
    #First: we must find the highest ID Number;
    for i in range(len(ContentsJSON)):
        if (ContentsJSON[i]['ID'] > IDNum):
            IDNum = int(ContentsJSON[i]['ID'])

    IDNum = IDNum + 1

    print("Not yet implemented.")
    print("TEST: open file " + objfile + " of type 'a'")
    for x in range(len(tags)):
        tags[x] = tags[x].lower()
    f = OpenFile(objfile,"a")
    if (f != 0):
        TheObject = {'name': obj.lower(), 'loc': loc.lower(), 'tags': tags, 'ID': IDNum} #ID number
        TheContent = json.dumps(TheObject)
        f.write(TheContent + "\n")
        f.close()
        return 1
    else:
        print("TEST: null file;")
        return 0
    #Append object to end of our objects file;
    #Add to end of our objects file for future reference.

def MoveObject(IDNum,newloc): #We should have some kind of ID for each entry...
    #print list of objects with tags if relevant, change location when selected;
    Ln = -1
    f = OpenFile(objfile,"r") #Read whole file first.  Check for highest ID tag;
    Contents = f.read()
    f.close()
    Contents = Contents.splitlines()
    ContentsJSON = [] #List of all objects;
    for x in range(len(Contents)):
        ContentsJSON.append(json.loads(Contents[x]))
        print(ContentsJSON[x]['ID'])
    
    #Find the IDNum we want to move:
    for x in range(len(ContentsJSON)):
        print(ContentsJSON[x]['ID'])
        if (int(ContentsJSON[x]['ID']) == int(IDNum)):
            Ln = x
            break;
    FileOutput = ""
    if (Ln >= 0):
        ContentsJSON[Ln]['loc'] = newloc.lower()
        #Write data;
        for x in range(len(ContentsJSON)):
            FileOutput += json.dumps(ContentsJSON[x]) + "\n"
        if (not OverwriteFile(objfile,FileOutput)):
            print("Sorry, Captain... I can't seem to save that information.")
        return True
    else:
        print("Sorry, Captain, I couldn't locate the object of ID " + str(IDNum))
        return False
    pass

def AppendTags(IDNum, tags):
    Ln = -1
    f = OpenFile(objfile,"r") #Read whole file first.  Check for highest ID tag;
    Contents = f.read()
    f.close()
    Contents = Contents.splitlines()
    NewTags = tags.lower().split(",")
    ContentsJSON = [] #List of all objects;
    for x in range(len(Contents)):
        ContentsJSON.append(json.loads(Contents[x]))
        print(ContentsJSON[x]['ID'])
    
    #Find the IDNum we want to move:
    for x in range(len(ContentsJSON)):
        print(ContentsJSON[x]['ID'])
        if (int(ContentsJSON[x]['ID']) == int(IDNum)):
            Ln = x
            break;

    for x in range(len(ContentsJSON[Ln]['tags'])):
        if ContentsJSON[Ln]['tags'][x] not in NewTags:
            NewTags.append(ContentsJSON[Ln]['tags'][x])

    FileOutput = ""
    if (Ln >= 0):
        ContentsJSON[Ln]['tags'] = NewTags
        print("New Tags: " + str(NewTags))
        #Write data;
        for x in range(len(ContentsJSON)):
            FileOutput += json.dumps(ContentsJSON[x]) + "\n"
        if (not OverwriteFile(objfile,FileOutput)):
            print("Sorry, Captain... I can't seem to save that information.")
        return True
    else:
        print("Sorry, Captain, I couldn't locate the object of ID " + str(IDNum))
        return False
    pass
   

#TODO: Implement ID system; have this return an ID so that we can simply search it out from other functions;
#FIXME: Should always return IDNum;
def FindObject(name = "",tags = []):
    f = OpenFile(objfile,"r")
    Contents = f.read()
    f.close()
    print(Contents)
    Contents = Contents.splitlines()
    ContentsJSON = [] #List of all objects;
    CandidateList = [] #Possible matches;
    #Convert from JSON to dictionary
    for x in range(len(Contents)):
        print(Contents[x])
        ContentsJSON.append(json.loads(Contents[x]))

    print("TEST")
    print(ContentsJSON)

    #We now have file contents by line;  Now we must search line-by-line;
    if (len(name) != 0):
        for x in range(len(ContentsJSON)):
            if (name.lower() in ContentsJSON[x]['name'].lower()):
                print("TEST Candidate found!")
                print(ContentsJSON[x])
                if (len(tags) != 0):
                    print("TEST tagsweep") #FIXME: This runs even with null tags;
                    for y in range(len(tags)):
                        if tags[y] in ContentsJSON[x]['tags'] or len(tags[y]) == 0:
                            CandidateList.append(ContentsJSON[x])
                            break;
                else:
                    print("TEST NoTagSweep;Append;")
                    CandidateList.append(ContentsJSON[x])
                #Add to list;
        
    else:
        #get list by name;
        if (len(tags) != 0):
            for x in range(len(ContentsJSON)):
                for y in range(len(tags)):
                    if tags[y].lower() in ContentsJSON[x]['tags']:
                        CandidateList.append(ContentsJSON[x])
    print(CandidateList) #if list is more than one, ask for specificity.
    if (len(CandidateList) == 0):
        if (len(name) > 0):
            print("I wasn't able to find " + name + ", captain.")
        else:
            print("I wasn't able to find anything like that, captain.")
        return 0
    elif (len(CandidateList) == 1):
        print("I found a match for what you were searching for.  According to my records:")
        print(CandidateList[0]['name'] + " is located " + CandidateList[0]['loc'] + " and matches the following tag descriptions: " + str(CandidateList[0]['tags']))
        resp = "\0"
        while (resp.lower() != "y" and resp.lower() != "n"):
            resp = input("Is this the item you were searching for? (y/n): ")
        if (resp.lower() == "y"):
            return CandidateList[0]['ID']
        else:
            print("I'm sorry I couldn't find what you were looking for, captain.")
            return 0
    else:
        print("I found a few matches for what you were searching for.  Here is what my records suggest: ")
        for x in range(len(CandidateList)):
            print(str(x) + ") " + CandidateList[x]['name'] + " is located " + CandidateList[x]['loc'] + " and matches the following tag descriptions: " + str(CandidateList[x]['tags']))
        resp = "\0"
        IsValid = False
        while (not IsValid):
            resp = input("Which candidate are you looking for? ")
            if (IsInt(resp)):
                if (int(resp) >= 1 and int(resp) <= len(CandidateList)):
                    IsValid = True
            if (not IsValid):
                print("Sorry, captain, you need to give me a number to work with.")
        print("I hope that I was of assistance, captain.")
        return CandidateList[resp]['ID']
        
    print("I hope that I was of assistance, captain.")
    return 0
    #Locate either object of name 'name' and/or with tags 'tags'

def DeleteObject(IDNum):
    Ln = -1
    f = OpenFile(objfile,"r") #Read whole file first.  Check for highest ID tag;
    Contents = f.read()
    f.close()
    Contents = Contents.splitlines()
    ContentsJSON = [] #List of all objects;
    for x in range(len(Contents)):
        ContentsJSON.append(json.loads(Contents[x]))
        print(ContentsJSON[x]['ID'])
    
    #Find the IDNum we want to move:
    for x in range(len(ContentsJSON)):
        print(ContentsJSON[x]['ID'])
        if (int(ContentsJSON[x]['ID']) == int(IDNum)):
            Ln = x
            break;
    if (Ln >= 0):
        ContentsJSON.pop(Ln)
 
    FileOutput = ""
    for x in range(len(ContentsJSON)):
        FileOutput += json.dumps(ContentsJSON[x]) + "\n"
    if (not OverwriteFile(objfile,FileOutput)):
        print("Sorry, Captain... I can't seem to save that information.")
    return True
    pass

def OverwriteFile(filename,content): #Safe method for file overwrite;  Returns true if successful or false if there is an error;
    cont = False
    ftmpbase = filename + ".tmp"
    ftmpadd = ""
    cycle = 0
    while (not cont):
        cycle += 1
        try: f = open(ftmpbase + ftmpadd,"x")
        except FileExistsError:
            ftmpadd = str(cycle)
            cont = True;
        except:
            return False
    try: 
        f.write(content)
    except: 
        f.close()
        return False
    try: 
        replace(filename + ".tmp", filename)
    except NotImplementedError:
        f.close()
        f = open(filename,"w")
        try: f.write(content)
        except:
            f.close()
            return False
    f.close()
    return True

def PrintOptionList():
    print("1) Take A Memo (audio or text note)") #TODO
    print("2) Define an object location") #Complete;
    print("3) Find an object") #Complete
    print("4) Add tags to an object") #Complete;
    print("5) Move an object to a new location") #Complete;
    print("6) Delete an object from existence") #Complete;
    print("7) Name an object (or attempt to by description)") #TODO
    print("8) Attempt to parse a natural text command (EXPERIMENTAL)") #TODO
    print("0) Exit") #Complete

def main():
    MainLoop = True
    while (MainLoop):
        print("Select an option:")
        PrintOptionList()
        try: opt = int(input("\tSelect an option: "))
        except: continue
        if (opt == 0):
            MainLoop = False
        elif (opt == 1):
            print("Sorry, I can't do that yet, captain.")
        elif (opt == 2):
            ObjName = input("What is this object called? ")
            ObjLoc = input("Where is this object located? ")
            ObjTags = input("Enter some helpful tags separated by commas: ")
            if (len(ObjName) == 0):
                print("Sorry captain, I can't store a location of something that doesn't have a name.")
                continue
            elif (len(ObjLoc) == 0):
                print("Sorry captain, I can't store a location that doesn't exist.")
                continue
            elif (len(ObjTags) == 0):
                print("This object doesn't have any helpful tags, captain.  I'll still store it, but feel free to modify it later.")
            ObjTagsList = ObjTags.split(",")
            #TODO: run a findobject to see if it exists already.  Also create a unique ID;
            NewObject(ObjName,ObjLoc,ObjTagsList)
        elif (opt == 3):
            print("Sorry, I can't do that yet.")
            naime = input("Do you know the object's name? ")
            if (naime.lower() == "no" or len(naime) == 0):
                naime = ""
                desc = input("Well then... what descriptions can you offer? ")
            else:
                desc = input("What descriptions can you offer? ")
                
            tags = desc.split(",")
            FindObject(naime,tags)
        elif (opt == 4): #ADD TAGS
            print("Sorry, I can't do that yet.")
            naime = input("Do you know the object's name? ")
            if (naime.lower() == "no" or len(naime) == 0):
                naime = ""
                desc = input("Well then... what descriptions can you offer? ")
            else:
                desc = input("What descriptions can you offer? ")
            tags = desc.split(",")
            IDNum = FindObject(naime,tags)
            NewTags = input("What new tags do you wish to add? ")
            AppendTags(IDNum,NewTags)
            
        elif (opt == 5): #MOVE LOCATION
            print("Sorry, I can't do that yet.")
            naime = input("Do you know the object's name? ")
            if (naime.lower() == "no" or len(naime) == 0):
                naime = ""
                desc = input("Well then... what descriptions can you offer? ")
            else:
                desc = input("What descriptions can you offer? ")
            tags = desc.split(",")
            IDNum = FindObject(naime,tags)
            if (IDNum >= 0):
                NewLoc = input("What is the new location of this object? ")
                MoveObject(IDNum,NewLoc)
        elif (opt == 6): #DELETE OBJECT
            print("Sorry, I can't do that yet.")
            naime = input("Do you know the object's name? ")
            if (naime.lower() == "no" or len(naime) == 0):
                naime = ""
                desc = input("Well then... what descriptions can you offer? ")
            else:
                desc = input("What descriptions can you offer? ")
            tags = desc.split(",")
            IDNum = FindObject(naime,tags)
            if (IDNum >= 0):
                DeleteObject(IDNum)
        elif (opt == 7): #GUESS NAME FROM TAGS AND (use score???)
            print("Sorry, I can't do that yet.")
        elif (opt == 8): #Attempt to parse natural text command;
            print("Sorry, I can't do that yet.")
        else:
            print("I don't know what you're asking me to do =(>.<)=/\"")

main()
print("Have a nice day, captain =(^.^)=")
exit(0)
