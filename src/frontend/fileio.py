#--------------------------------------------------------------------
# Basic File IO functions
#--------------------------------------------------------------------
class FileIO:
    #--------------------------------------------------------------------
    # Read the file at the specified path and returns all of the lines in a list of strings
    #--------------------------------------------------------------------
    @staticmethod
    def readLines(path):
        file = open(path)
        lines = file.readlines()
        file.close()
        return lines
    
    #--------------------------------------------------------------------
    # Writes the list of lines to a file at the specified path, inserting each entry in lines on a separate line in the file
    #--------------------------------------------------------------------
    @staticmethod
    def writeLines(path, lines):
        try:
            file = open(path, 'w')
        except Exception as err:
            print('Error opening file: ' + err.message)
            return False
        try:
            output = ''
            for line in lines:
                output += line + '\n' 
            file.writelines(output[:len(output) - 1])
        except Exception as err:
            print('Error writing lines: ' + err.message)
            file.close()
            return False
        file.close()
        return True

    #--------------------------------------------------------------------
    # Clears the contents of a file, creates if non existent
    #--------------------------------------------------------------------
    @staticmethod
    def clear(path):
        open(path, 'w').close()
