
class Presenter(object):
    
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

        # Connecting custom signals
        self.__view.signal_copy.connect(self.copy_DirOrFile)
        #self.__view.signal_open.connect()
        #self.__view.signal_make.connect()
        self.__view.signal_delete.connect(self.delete_DirOrFile)

        self.__view.signal_changePath.connect(self.change_dir)
        self.__view.signal_writeToPath.connect(self.write_to_path)
    
    # Writing to path editor after selection item
    def write_to_path(self, sender, destination):
        file_model = self.__view.file_model
        self.__model.writePathTolE(sender, destination, file_model)

    # Changing directories after accepting (return pressed) the path in editor
    def change_dir(self, sender, destination):
        file_model = self.__view.file_model
        self.__model.changeDir(sender, destination, file_model)

    def copy_DirOrFile(self):
        source, destination = self.__view.checkWhichTree()
        file_model = self.__view.file_model
        self.__model.copyFunc(source, destination, file_model)
###################################
    def delete_DirOrFile(self):
        to_delete, is_dir = self.__view.prepare_del_dialog()

        if to_delete is not None:
            if is_dir:
                self.__model.deleteDirFunc(to_delete)

            else:
                self.__model.deleteFileFunc(to_delete)
#####################################        

    def test(self, sender):
        
        print('presenter sender')
        print(sender)