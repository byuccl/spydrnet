from spydrnet.data_manager import DataManager
from spydrnet.ir import Environment

_current_netlist = None

def current_netlist(netlist = None):
    if netlist:
        global _current_netlist
        _current_netlist = netlist
        top_virtual_instance = netlist.top_virtual_instance
        if top_virtual_instance:
            current_virtual_instance(top_virtual_instance)
        return netlist
    else:
        return _current_netlist

_current_virtual_instance = None

def current_virtual_instance(virtual_instance = None):
    if virtual_instance:
        global _current_virtual_instance
        _current_virtual_instance = virtual_instance
        return virtual_instance
    else:
        return _current_virtual_instance

_netlists = list()

def get_netlists(*args, **kwargs):
    pass

def create_netlist():
    global _current_netlist
    new_netlist = Environment()
    _netlists.append(new_netlist)
    current_netlist(new_netlist)
    return new_netlist

class GlobalEnvironmentManager:
    """
    manage the global namespace for the tools
    use a singleton object that will manager the environments individually.
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
        '''
        register an environment with the environment manager.
        The environment must have a unique value on the metadata_key used while initializing with respect to all other environments.
        '''
        if not GlobalEnvironmentManager.instance:
            GlobalEnvironmentManager._uninitialized_error()
        GlobalEnvironmentManager.instance.register_environment(environment)

    @staticmethod
    def get_all_environments():
        '''
        Return all currently created environments
        '''
        return GlobalEnvironmentManager.instance.get_all_environments()

    @staticmethod
    def _uninitialized_error():
        '''
        handle alerting the user when an uninitialized singleton is used
        TODO change this to raise an exception
        '''
        print("An instance of the GlobalEnvironmentManager needs to be created before the static functions can be called")