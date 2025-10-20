import os 

class UserAccount:
    loginindex = {"Username": 0, "Password": 1}  # index for username and password
    posindex = {"BirthDate": 0, "FavouriteArtist": 1, "FavouriteGenre": 2}  # index for user data

    def __init__(self, filename="user_account.txt"):
        self.filename = filename
        self.userdata = ["", "", ""]  # only birthdate, fav artist, fav genre now
        self.userlogin = ["", ""]  # username, password

    def createaccount(self):
        print("Account creation")
        self.userlogin[self.loginindex["Username"]] = input("Enter username: ").strip()
        self.userlogin[self.loginindex["Password"]] = input("Enter password: ").strip()
        self.userdata[self.posindex["BirthDate"]] = input("Enter your birth date: ").strip()
        self.userdata[self.posindex["FavouriteArtist"]] = input("Enter your favourite artist: ").strip()
        self.userdata[self.posindex["FavouriteGenre"]] = input("Enter your favourite genre: ").strip()
        self.savetofile()

    def savetofile(self):
        # store username,password followed by userdata in one line
        with open(self.filename, "a") as f:
            f.write(",".join(self.userlogin + self.userdata) + "\n")
        # join concentrates the differet inputs , allowing it all to be stored in one single line

    def login(self):
        print("Login")
        username = input("Username: ").strip() #.strip removes any unnecessary spaces
        password = input("Password: ").strip()

        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    #parts refer to the individual components of the array
                    if parts[self.loginindex["Username"]] == username and parts[self.loginindex["Password"]] == password:
                        print("Login successful")
                        self.userlogin = [parts[self.loginindex["Username"]], parts[self.loginindex["Password"]]]
                        self.userdata = [parts[2], parts[3], parts[4]]
                        return True
        except FileNotFoundError:
            print("No accounts found")
            return False

        print("Invalid detail")
        return False

    def editfav(self):
        print("Edit data")
        print("1.Change favourite artist \n 2. Change favourite genre \n 3. Exit")
        choice = input("Enter your choice: ").strip()
        match choice:
            case "1":
                self.userdata[self.posindex["FavouriteArtist"]] = input("Enter new favourite artist: ")
            case "2":
                self.userdata[self.posindex["FavouriteGenre"]] = input("Enter new favourite genre: ")
            case "3":
                return
            case _:
                print("Invalid")
                return self.editfav()

        # Rewrite the updated data to the file
        self.updateuser()
        print("updated")

    def updateuser(self):
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return

        updated_lines = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 5 and parts[self.loginindex["Username"]] == self.userlogin[self.loginindex["Username"]]:
                line = ",".join(self.userlogin + self.userdata) + "\n"
            updated_lines.append(line)

        with open(self.filename, "w") as f:
            f.writelines(updated_lines)

    def displayinfo(self):
        print(" User info ")
        print("Username:", self.userlogin[self.loginindex["Username"]])
        for key, index in self.posindex.items():
            print(key + ":", self.userdata[index])


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
        match posname:
            case "Length":
                return sorted(self.musicdata,key=lambda x: int(x[self.posindex["Length"]]),reverse=reverse)
            case _:
                return sorted(self.musicdata,key=lambda x: x[self.posindex[posname]],reverse=reverse)
#sorted according to the posindex provided,since length has to be an int,has to sort differently,
#reverse = reverse allows both asc and desc in one func instead of 2
#uses match case (just alternative way of doing if else statements)
    def search(self, posname, usersearchreq):
        return [x for x in self.musicdata if x[self.posindex[posname]] == usersearchreq]
#prints out data only if matching posindex with inputted index 
#x refers to each item, and only return value that corresponds with the user search

    def songoutput(self, songs):
        print("View \n1. By song title \n 2. By artist \n 3. By genre")
        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                sorted_songs = self.sort("SongName")
            case "2":
                sorted_songs = self.sort("ArtistName")
            case "3":
                sorted_songs = self.sort("Genre")
            case _:
                print("Invalid choice.")
                return

        print("List")
        for song in sorted_songs:
            SongName, ArtistName, Genre, Length = song
            mins, secs = self.displayedtime(song)
            print(f"Song: {SongName} \n Artist: {ArtistName} \n Genre: {Genre} \n Length: {mins:02d}:{secs:02d}")

    def displayedtime(self, song):
        length = int(song[self.posindex["Length"]])
        return length // 60, length % 60 #floor div for min,modulus for second

    def manageplaylist(self):
        print(" Menu \n 1. Create playlist \n 2. View playlist \n 3. Exit")
        choice = input("Enter choice: ").strip()

        match choice:
            case "1":
                playlist_name = input("Enter playlist name: ").strip()
                genre = input("Enter genre to include: ").strip()
                songs = self.playlist_by_genre(genre)
                if len(songs) > 0:
                    self.create_playlist(playlist_name, songs)
            case "2":
                playlist_name = input("Enter playlist name to view: ").strip()
                self.view_playlist(playlist_name)
            case "3":
                os.system("clear")
                return
            case _:
                print("Invalid choice")
                return self.manageplaylist()

    def create_playlist(self, playlist_name, songs):
        if len(songs) == 0:
            print("Playlist must contain one song miniumim")
            return
        with open(f"{playlist_name}.txt", "w") as f:
            for song in songs:
                SongName = song[self.posindex["SongName"]]
                ArtistName = song[self.posindex["ArtistName"]]
                Genre = song[self.posindex["Genre"]]  # added genre
                Length = song[self.posindex["Length"]]
                f.write(f"{SongName},{ArtistName},{Genre},{Length}\n")  # added genre in line
        print(f"Playlist '{playlist_name}' saved")

    def view_playlist(self, playlist_name):
        try:
            with open(f"{playlist_name}.txt", "r") as f:
                lines = f.readlines()
                print(f"Viewing Playlist: {playlist_name}")
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) == 4:  # updated to 4 to include genre
                        print(f"Song: {parts[0]} \n Artist: {parts[1]} \n Genre: {parts[2]} \n Length: {int(parts[3])//60}:{int(parts[3])%60}")
        except FileNotFoundError:
            print("Playlist not found.")

    def autogen(self):
        print(" List generate \n 1. Generate by time  \n 2. Generate by genre \n 3. Exit")
        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                timelimit = int(input("Enter time limit in minutes: "))
                playlist = self.playlisttime(timelimit)
                if playlist:
                    self.create_playlist(f"autoplaylist_{timelimit}min", playlist)
            case "2":
                genre = input("Enter genre: ").strip()
                playlist = self.playlist_by_genre(genre)
                if playlist:
                    self.create_playlist(f"autoplaylist_{genre}", playlist)
            case "3":
                return
            case _:
                print("Invalid choice")
                return self.autogen()

    def playlisttime(self, timelimitminutes: int):
        timelimit = timelimitminutes * 60 
        total = 0
        playlist = []
        for song in self.musicdata:
            length = int(song[self.posindex["Length"]])
            if total + length <= timelimit:
                playlist.append(song)
                total += length
        return playlist

    def playlist_by_genre(self, genre):
        songs = [song for song in self.musicdata if song[self.posindex["Genre"]].lower() == genre.lower()]
        return songs[:5]  # limit to 5 songs

    def genresort(self):
        genre_stored = {}
        for song in self.musicdata:
            genre = song[self.posindex["Genre"]]
            length = int(song[self.posindex["Length"]])
            if genre not in genre_stored:
                genre_stored[genre] = []
            genre_stored[genre].append(length)

        print("Menu \n 1. View all genres \n 2. View one genre \n 3. Exit")
        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                print("\n All genre")
                for genre, lengths in genre_stored.items():
                    average_len = sum(lengths) / len(lengths)
                    mins, secs = average_len // 60, int(average_len % 60)
                    print(f"Genre: {genre} \n Average Length: {int(mins):02d}:{int(secs):02d}")
            case "2":
                search_genre = input("Enter genre to view: ").strip()
                if search_genre in genre_stored:
                    average_len = sum(genre_stored[search_genre]) / len(genre_stored[search_genre])
                    mins, secs = average_len // 60, int(average_len % 60)
                    print(f"Genre: {search_genre} \n Average Length: {int(mins):02d}:{int(secs):02d}")
                else:
                    print("Genre not found")
            case "3":
                return
            case _:
                print("Invalid choice")
                return self.genresort()


file = "musicdata.txt"
def main():
    user = UserAccount()
    library = Musiclibrary("musicdata.txt")
    print("1. Login \n 2. Create account")
    choice = input("Enter choice: ").strip()
    match choice:
        case "1":
            if not user.login():
                return
        case "2":
            user.createaccount()
        case _:
            print("Invalid choice")
            return
    user.displayinfo()
    while True:
        print("Main menu \n 1. Edit favourite \n 2. View song \n 3. Manage lists \n 4. List generator \n 5. Summary \n 6. Exit")
        option = input("Enter your choice: ").strip()
        match option:
            case "1":
                user.editfav()
            case "2":
                library.songoutput(library.musicdata)
            case "3":
                library.manageplaylist()
            case "4":
                library.autogen()
            case "5":
                library.genresort()
            case "6":
                break
            case _:
                print("invalid choice")
main()
