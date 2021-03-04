"""
ECSSManager, part of the glGA SDK ECSS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import List, Dict
import pprint

from Entity import Entity
import Component
import System
import utilities as util


class ECSSManager():
    """
    Singleton Manager class to provide factory creation methods for
    all Entities, Components, Systems, as an alternative way and hide the scenegraph complexity.

    """
    _instance = None
    
    def __new__(cls):
        """
        Special singleton class method, returns single instance of ECSSManager

        :return: single class instance
        :rtype: ECSSManagger
        """
        if cls._instance is None:
            print('Creating Scene Singleton Object')
            cls._instance = super(ECSSManager, cls).__new__(cls)
            # add further init here
        return cls._instance

    def __init__(self):
        """
        Construct initial data structures for scenegraph elements
        """
        self._systems: List[System.System]=[] #list for all systems
        self._components: List[Component.Component]=[] #list with all scenegraph components
        self._entities: List[Entity]=[] #list of all scenegraph entities
        self._cameras: List[Component.Component]=[] # list of all scenegraph camera components
        self._entities_components = {} #dict with keys entities and values list of components per entity
        self._next_entity_id = 0
        self._root = None

        

    def createEntity(self, entity: Entity):
        """
        Creates an Entity in the underlying scenegraph and adds it in the ECSS data structures.
        
        Checks if the Entity's name is "root" to add it as root of the ECSS
        
        :param entity: Entity to add in the Scenegraph
        :type entity: Entity
        """
        if isinstance(entity, Entity):
            self._entities.append(entity) #add an empty list for components with the new Entity
            self._entities_components[entity]=[None]
        
            if entity.name.lower() == "root":
                self._root = entity
        
        return entity #if the method was called with an inline constructor e.g. 'createEntity(Entity())', 
                        # we return that created Entity in case it is needed
    
    
    def createSystem(self, system: System.System):
        """
        Creates a System and adds it in the ECSS data structures
        
        """
        if isinstance(system, System.System):
            self._systems.append(system)
        
        return system
    
    
    def createIterator(self, entity: Entity, dfs=True):
        """
        Creates and returns a scenegraph traversal node iterator

        :param entity: [description]
        :type entity: Entity
        """
        if isinstance(entity, Entity):
            if dfs:
                return iter(entity)
        

    
    def addComponent(self, entity: Entity, component: Component.Component):
        """
        Adds a component to an Entity in a scenegraph and in the ECSS data structures
        
        Checks if that Component is a Camera, to add it in the list of Cameras
        
        Checks if that Entity has already such a component of that type and replaces 
        it with the new one
        
        Checks that indeed only a component is added with this method. 
        If we need to add a child Entity to an Enity, we use addEntityChild()

        :param entity: Parent Entity
        :type entity: Entity
        :param component: The component to be added to this Entity
        :type component: Component
        """
        if isinstance(entity, Entity) and isinstance(component, Component.Component):
            if isinstance(component, Component.Camera):
                self._cameras.append(component)
            else: #add the component in the _components []
                self._components.append(component)
                
            # loop through all dictionary elements of _entities_components
            for key, value in self._entities_components.items():
                if key is entity: # find key [entity]
                    for el in value: #el are Components
                        # check if the value list() of that entity has already that component type
                        if isinstance(el, type(component)): # el.type == component.type
                            # if it has it, replace previous component with same type
                            # bur first remove previous from scenegraph and add new one
                            # GPTODO 
                            el = component
                        else: #otherwise add it in ECSSManager and in Scenegraph
                            key.add(component)
                            #check if there is a list of components and add it there otherwise create one
                            if isinstance(value, list):
                                #check if first element is None
                                if (value[0] == None):
                                    value[0] = component 
                                else:
                                    value.append(component)
                            else:
                                value = list(component)
                            return component
                                
            
            
    
    
    def addEntityChild(self, entity_parent: Entity, entity_child: Entity):
        """
        Adds a child Enity to a parent one and thus establishes a hierarchy 
        in the underlying scenegraph.
        
        Adds the child Entity also in the ECSS _entities_components dictionary 
        data structure, so that the hierarchy is also visible at ECSSManager level.

        :param entity_parent: [description]
        :type entity_parent: Entity
        :param entity_child: [description]
        :type entity_child: Entity
        """
        if isinstance(entity_parent, Entity) and isinstance(entity_child, Entity):
            # check if there is already a parent-child relationship between the Entities
            if entity_child.getParent() is not entity_parent:
                # if not, create one
                entity_parent.add(entity_child)
            # add entity_child in the _entities_components dictionary
            # GPTODO
            


    def traverse_visit(self, system: System.System, iterator: Iterator):
        """
        Traverse whole scenegraph by iterating every Entity/Component and calling 
        a specific System on each different element.   

        :param system: [description]
        :type system: System.System
        :param iterator: [description]
        :type iterator: Iterator
        """
        if isinstance(system, System.System) and issubclass(iterator, Iterator):
            pass

    
    def print(self):
        """
        pretty print the contents of the ECSS
        """
        print("_entities_components {}".center(100, '-'))
        #pprint.pprint(self._entities_components)
        for en, co in self._entities_components.items():
            print(f"{en.name}")
            for comp in co:
                if comp is not None:
                    print(f"\t :: {comp.name}")
        
        print("_entities []".center(100, '-'))
        for ent in self._entities:
            print(ent)
        print("_components []".center(100, '-'))
        for com in self._components:
            print(com.name,"--> ", com.parent.name)
        print("_systems []".center(100, '-'))
        for sys in self._systems:
            print(sys)
        print("_cameras []".center(100, '-'))
        for cam in self._cameras:
            print(cam)



if __name__ == "__main__":
    # The client code.

    s1 = ECSSManager()
    s2 = ECSSManager()
    
    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")