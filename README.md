# Spotify Song Recommendations
This program allows you to input an artist's name and it will retrieve a table of 60 songs related to the artist(3 from each related artist)

### packages
- requests
- pandas
- sqlalchemy
- pprint
- tabulate

### Usage
1. Obtain Spotify API credentials:
	- Go to the Spotify Developer Dashboard at https://developer.spotify.com/ and create a new application
	- Copy the 'Client ID' and 'Client Secret' values
2. Replace the 'client id' and 'client secret' in the code with your Spotify API credentials
3. Run the program
4. Enter the Name of the desired Artist when prompted
5. The program will retrieve 20 related artists and make a table with 3 songs from each
6. The 60 songs will be posted in a table on the console
