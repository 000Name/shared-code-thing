class Musiclibrary:
    posindex = {"SongName": 0, "ArtistName": 1, "Genre": 2, "Length": 3}  #constant stored, length is stored in seconds

    def __init__(self, file): #allows easier object creation, file is usable within the 
        self.file = file
        self.musicdata = self.load_data() #originally within the loaddata function,changed to here so code doesnt have to call load data everytime 

    def load_data(self):
        with open(self.file, "r") as d:  # fixed from self.filepath to self.file
            values = d.readlines()
            data = [value.strip().split(",") for value in values] 
            for row in data:
                row[self.posindex["Length"]] = row[self.posindex["Length"]]  # keep as str in memory
            return data
            #format of the txt would be song,artist,genre,length ,.split by , gives 4 seperate values from one line

    def sort(self, posname, reverse = False):
        return sorted(self.musicdata,key=lambda x: int(x[self.posindex[posname]])if posname == "Length" else x[self.posindex[posname]],reverse=reverse)
#sorts according to the posindex provided,since length has to be an int,has to sort differently,
#reverse = reverse allows both asc and desc in one func instead of 2
    def search(self, posname, usersearchreq):
        return [x for x in self.musicdata if x[self.posindex[posname]] == usersearchreq]
#prints out data only if matching posindex with inputted index 
#x refers to each item, and only return value that corresponds with the user search
    def songoutput(self, songs):
        for song in songs:
            SongName, ArtistName, Genre, Length = song
            mins, secs = self.displayedtime(song)
            print()#placeholder , consider using f string and format specified 02d

    def displayedtime(self, song):
        length = int(song[self.posindex["Length"]])
        return length // 60, length % 60 #floor div for min,modulus for second

    def playlisttime(self, timelimitminutes: int):
        timelimit = timelimitminutes * 60 #user dont need to enter in seconds,prefer whole numbers,easier to do if used html,css 
        total = 0
        playlist = [] #possibly change this to a append to txt, so easier data manipulation , could add a function to clear playlist if its a text file
        for song in self.musicdata:
            length = int(song[self.posindex["Length"]])
            if total + length <= timelimit:
                playlist.append(song)
                total += length #same as total = total + length
        return playlist

    def playlist_by_genre(self, genre):
        return [song for song in self.musicdata if song[self.posindex["Genre"]].lower() == genre.lower()] #adds all songs of a genre to a list

    def save_artist_songs(self, artistname, outputfile):
        songs = [song for song in self.musicdata if song[self.posindex["ArtistName"]].lower() == artistname.lower()] #same principle as genre,
        with open(outputfile, "w") as f:
            for song in songs:
                # force output order: SongName, ArtistName, Genre, Length
                line = [song[self.posindex["SongName"]], song[self.posindex["ArtistName"]], song[self.posindex["Genre"]], song[self.posindex["Length"]]]
                #data is in the same format as the musicdata.txt 
                f.write(",".join(line) + "\n")
                #.join is used to take the seperated items and stored as str in the textfile
        return songs

    def genresort(self):
        genre_stored = {}
        for song in self.musicdata:
            genre = song[self.posindex["Genre"]]
            length = int(song[self.posindex["Length"]])
            if genre not in genre_stored:
                genre_stored[genre] = []
            genre_stored[genre].append(length) #can remove this part if genre data is not left blank initially, just set some predetermined ones and remove this?

        for genre, lengths in genre_stored.items():  #.item() to give a pair of values of genre and length [('genre',''),('length','')]
            average_len = sum(lengths) / len(lengths)
            mins, secs = average_len // 60, int(average_len % 60)
            print()#placeholder
file = "musicdata.txt"
