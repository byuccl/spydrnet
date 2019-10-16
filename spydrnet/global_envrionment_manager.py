from spydrnet.data_manager import DataManager
from spydrnet.ir import Environment

class GlobalEnvironmentManager:
    """
    manages the global namespace for the tools
    tasks include:
    tracking the namespace for the environments that are created
    """

    instance = None

    class _GlobalEnvironmentManager:
        '''
        Internal class within GlobalEnevironmentManager that holds the datamanager that is used to store the environments
        Singleton instance of the class because we want one global manager for all the environments
        Used within the GlobalEnvironmentManager to allow us to initialize and use this manager as an instance.
        '''
        
        def __init__(self, metadata_key):
            self.dm = DataManager.from_element_type_and_metadata_key(Environment, metadata_key)#'EDIF.identifier')
            self.dm.set_owner_and_populate_lookup(self)
            
        def register_environment(self, environment):
            self.dm.add_to_lookup(environment)

        def get_all_environments(self):
            return self.dm.get_all_children()

    def __init__(self,metadata_key):
        '''
        Initialize the environment manager. Must be called before the environment manager static classes are used.
        '''
        if not GlobalEnvironmentManager.instance:
            GlobalEnvironmentManager.instance = GlobalEnvironmentManager._GlobalEnvironmentManager(metadata_key)
        else:
            #do nothting because we already have our enivronment manager setup
            pass

    @staticmethod
    def register_environment(environment):
        if not GlobalEnvrionmentManager.instance:
            GlobalEnvironmentManager._uninitialized_error()
        GlobalEnvironmentManager.instance.register_environment(environment)

    @staticmethod
    def get_all_environments():
        return GlobalEnvironmentManager.instance.get_all_environments()

    @staticmethod
    def _uninitialized_error():
        print("An instance of the GlobalEnvironmentManager needs to be created before the static functions can be called")