posindex = {"SongName": 0 , "ArtistName": 1, "Genre": 2,"Length": 3} #const,store length in seconds


def data(library):
    with open(library,"r") as d:
        values = d.readline()
        musicdata = [value.strip().split(",") for value in values] #format of the txt would be song,artist,genre,length ,.split by , gives 4 seperate values from one line
    return musicdata


def sort(musicdata, posname, reverse=False):
    return sorted(musicdata,key=lambda x: int(x[posindex[posname]]) if posname == "Length" else x[posindex[posname]],reverse=reverse) 
#sorts according to the posindex provided,since length has to be an int,has to sort differently,reverse = reverse allows both asc and desc in one func instead of 2

def search(musicdata, posname, usersearchreq):
    return [x for x in musicdata if x[posindex[posname]] == usersearchreq]
#prints out data only if matching posindex with inputted index 


def songoutput(y):
    for x in y:
        SongName,ArtistName,Genre,Length = x
        print()#format insert here

#format of file has to be 3d array?
file = "musicdata.txt"
data1 = data(file)
#songoutput(sortasc/sortdesc(data1,type))
#2 seperate func for asc/desc data types?

#convert second into minutes
def displayedtime(sortinglist):
    len = int(sortinglist[3])
    return len//60,len%60
#floor div for minutes,modulus for seconds

timelimit = int(input("Enter time in minutes"))
timelimit = timelimit * 60 #need to add check in case of not int?


playlist = []
def playlisttime(musicdata,timelimit):
    total = 0
    for song in musicdata:
        length = int(song[posindex["Length"]])
        if total + length < timelimit:
            playlist.append(song)
            total = total + length#use += instead?? idk
    return playlist #just set a timielimit as userinput


def genresort(musicdata):
    genre_stored = []
    for song in musicdata:
        genre = song[posindex["Genre"]]
        length = int(song[posindex["Length"]])
        if genre not in genre_stored:
            genre_stored[genre] = []
        genre_stored[genre].append(length) #can remove this part if genre data is not left blank initially, just set some predetermined ones and remove this?

    for genre, lengths in genre_stored.items(): #.item() to give a pair of values of genre and length [('genre',''),('length','')]
        average_len = sum(lengths) / len(lengths)
        mins, secs = average_len // 60, int(average_len % 60)
        print()#placeholder
