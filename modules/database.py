from traceback import format_exc #for error handling
import ast #for parsing user data dictionary from string loaded from file
from os.path import exists as fileexists #used to check if user data dictionary file exists

class Database:
	#hidden functions
    def __init__(self, filename):
        self.__databasename__ = filename
        #if the file doesnt exist, create one.
        if fileexists(self.__databasename__) == False:
            self.__savefile__("{}")
    def __savefile__(self, data):
        '''Writes the data provided to the database.'''
        #open the file
        file = open(self.__databasename__,"w")
        #write the changes and close the file
        file.write(str(data))
        file.close()
    
    def __readfile__(self):
        '''Loads the database from disk and returns a dictionary object.'''
        #load the database from disk in read mode since we will only be reading.
        file = open(self.__databasename__,"r")
        data = file.readlines()
        file.close()
        data = data[0] #since the file.readlines() is an array, get the first line. this contains the data in the file.
        return ast.literal_eval(data) #parse the data and return this.
		
	#public functions
    def create_user(self,username):
        '''Creates a new user profile using the username provided.'''
        if self.check_user_existence(username) == False:
            #load the database from disk
            data = self.__readfile__()
            data[username] = {} #set the user data to nothing. this creates a user entry in the process.

            #save the new file
            self.__savefile__(data)
    def delete_user(self,username):
        '''Deletes a specifed user from the database.'''
        if self.check_user_existence(username):
            try:
                #load the database from disk
                data = self.__readfile__()

                #remove the entry and save it.
                data.pop(username)
                self.__savefile__(data)
            except:
                raise Exception("Unable to remove user from database!")
    def check_user_existence(self, username):
        '''Checks if a specified user exists in the database. Returns a boolean.'''
        try:
            #load the database from disk
            data = self.__readfile__()
            #check if user exists
            if data.__contains__(username):
                return True
            else:
                return False
        except:
            raise Exception("Error checking user existence in database!")
    def get_user_data(self, username, attribute):
        '''Retrieves stored data for an attribute associated with a user. Returns the data or 0 if there is no data.'''
        try:
            #load the database from disk
            data = self.__readfile__()
        except:
            raise Exception("Error reading database!")
        try:
            #read the entry and return it.
            datapoint = data[username][attribute]
            return datapoint
        except:
            error = format_exc()
            if "KeyError" not in error:
                raise Exception("Error reading database entry for user key!")
            else:
                #No entry with that name exists for that user. Return 0.
                return 0
    def set_user_data(self, username, attribute, newvalue):
        '''Sets the value of an attribute for a user. Returns nothing.'''
        try:
            #load the database from disk
            data = self.__readfile__()
        except:
            raise Exception("Error reading database!")
        try:
            subdata = data[username]
        except:
            subdata = {}
        try:
            #update the entry and save
            subdata[attribute] = newvalue
            data[username] = subdata
            self.__savefile__(data)
        except:
            raise Exception("Error writing database user key!")
    def rename_user(self, username, newusername):
        '''Changes a username for a user.'''
        try:
            #load the database from disk
            data = self.__readfile__()
        except:
            raise Exception("Error reading database!")
        try:
            data[newusername] = data.pop(username)
            self.__savefile__(data)
        except:
            raise Exception("Error writing database user key!")
