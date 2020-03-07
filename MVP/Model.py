
from PyQt5 import QtCore

class Model(object):

    def writePathTolE(self, tree, source, model):
        path = model.filePath(tree.currentIndex())
        source.setText(path)

    def changeDir(self, source, tree, model):
        #Strip to avoid path like = ' ', that provides current folder (used a lot in this code)
        path = source.text().strip()   
        path_i = model.index(path)
        myComputerIndx = model.index('')

        if path == '':
            tree.setRootIndex(myComputerIndx)

        elif path_i.isValid():
            tree.setRootIndex(path_i)

        else:
            print('Path do not exist')

    def _inSameDir(self, src_i, dst_i, model):
        if src_i == dst_i:  #If trying to copy folder into itself
            return True

        parent_i = model.parent(dst_i)

        while(parent_i.isValid()):  #If any of parents of dst directory is a src path
            if parent_i == src_i:
                return True

            parent_i = model.parent(parent_i)

        return False

    def _copyDir(self, src, dst, dir_name, model):
        curr_dir = QtCore.QDir(src) #Object of current source dir
        filters = QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs | QtCore.QDir.Files
        curr_dir.setFilter(filters) 
        files_list = curr_dir.entryList()   #List of source dir content

        dst_directory = dst+'\\'+dir_name
        curr_dir.mkpath(dst_directory)  #Mkdir in destination folder

        for fileN in files_list:     #Loop through all content to find directories
            path = src+'\\'+fileN
            insideFile_ind = model.index(path) #Grabbing index of inner file

            if model.isDir(insideFile_ind): #Check if file of this index is dir
                files_list.remove(fileN)    #Removing dirs from list
                self._copyDir(path, dst_directory, model.fileName(insideFile_ind), model) #RECURSION
        
        file = QtCore.QFile()

        for fileN in files_list: #Creating copies of files from 'src' in directory inside of 'destination directory'
            path = src+'\\'+fileN
            file.copy(path, dst_directory+'\\'+fileN)

    def copyFunc(self, source, destination, model):
        file = QtCore.QFile()
        dst = destination.text().strip() #Path of destination directory
        src = source.text().strip() #Path of file / dir to copy 
        src_i = model.index(src)
        dst_i = model.index(dst)

        print('\nSorce path exist :', src_i.isValid(),'\nDestination path exist:', dst_i.isValid()) #DEBUG
        print('Is in the same dir :', self._inSameDir(src_i,dst_i, model)) #DEBUG


        if src_i.isValid() and dst_i.isValid(): #If paths exist
            fn = model.fileName(src_i) #Filename of file/dir to copy
            temp_ind = fn[::-1].find('.') #Finding index of '.' (need for extension)
            toDir = model.isDir(dst_i) #Destination is a directory

            if temp_ind != -1 and toDir:  #If file to dir
                if file.exists(dst+'\\'+fn):  #If file with this name exist in dst dir, then add -copy
                    ext = fn[-(temp_ind+1):]  #Point out the extension
                    fn = fn[:-(temp_ind+1)]+'-copy'+ext

                copied_dst = dst+'\\'+fn  
                file.copy(src, copied_dst) 

            elif (          #If dir to dir and not itself
                model.isDir(src_i)  
                and not self._inSameDir(src_i, dst_i, model)
                and toDir
            ):

                if file.exists(dst+'\\'+fn):  #If dir with this name exists in dst dir, then add -copy
                    fn+='-copy'  

                self._copyDir(src, dst, fn, model)

            else:
                print(
                    'Your destination is not a directory / cannot copy directory into itself / wrong panel choosed'
                )
        else:
            print('Path do not exist')
#####################################################
    def deleteDirFunc(self, directory):
        directory.removeRecursively()

    def deleteFileFunc(self, file):
        file.remove()

#########################################