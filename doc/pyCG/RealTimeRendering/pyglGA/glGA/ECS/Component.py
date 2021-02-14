"""
Component classes, part of the glGA SDK ECS
    
glGA SDK v2020.1 ECS (Entity Component System)
@Coopyright 2020 George Papagiannakis
    
The Compoment class is the dedicated to a specific type of data container in the glGA ECS.

The following is example restructured text doc example
:param file_loc: The file location of the spreadsheet
:type file_loc: str
:returns: a list of strings representing the header columns
:rtype: list

"""

from __future__         import annotations
from abc                import ABC, abstractmethod
from typing             import List
from collections.abc    import Iterable, Iterator

import System  
import utilities as util


class Component(ABC, Iterable):
    """
    The Interface Component class of our ECSS.
    
    Based on the Composite pattern, it is a data collection of specific
    class of data. 
    Concrete Subclass Components typically are e.g. BasicTransform, RenderMesh, Shader, RigidBody etc.
    """
    
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._parent = self
        self._children = None
    
    #define properties for id, name, type, parent
    @property #name
    def name(self) -> str:
        """ Get Component's name """
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
        
    @property #type
    def type(self) -> str:
        """ Get Component's type """
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
        
    @property #id
    def id(self) -> int:
        """ Get Component's id """
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
        
    @property #parent
    def parent(self) -> Component:
        """ Get Component's parent """
        return self._parent
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    def add(self, object: Component) ->None:
        pass

    def remove(self, object: Component) ->None:
        pass
        
    def getChild(self, index) ->Component:
        return None
    
    def getNumberOfChildren(self) -> int:
        return len(self._children)
    
    @classmethod
    def getClassName(cls):
        return cls.__name__
    
    @abstractmethod
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    @abstractmethod
    def update(self, **kwargs):
        """
        method to be subclassed for debuging purposes only, 
        in case we need some behavioral or logic computation within te Component. 
        This violates the ECS architecture and should be avoided.
        """
        pass
    
    @abstractmethod
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.update()
        
    def print(self):
        """
        prints out name, type, id, parent of this Component
        """
        print(f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}")
        print(f" ______________________________________________________________")
    
    def __iter__(self):
        """ Iterable method
        makes this abstract Component an iterable. It is meant to be overidden by subclasses.
        """
        return self 
    
    def __str__(self):
        return f"\n {self.getClassName()} name: {self._name}, type: {self._type}, id: {self._id}, parent: {self._parent._name}"


class ComponentIterator(ABC):
    """Abstract component Iterator class

    :param ABC: [description]
    :type ABC: [type]
    :return: [description]
    :rtype: [type]
    """
    pass

class CompNullIterator(Iterator, ComponentIterator):
    """
    The Default Null iterator for a Concrete Component class

    :param Iterator: [description]
    :type Iterator: [type]
    """
    def __init__(self, comp: Component):
        self._comp = comp
    
    def __next__(self):
        return None
    

class BasicTransform(Component):
    """
    An example of a concrete Component Transform class
    
    Contains a basic Euclidean Translation, Rotation and Scale Homogeneous matrices
    all-in-one TRS 4x4 matrix
    
    :param Component: [description]
    :type Component: [type]
    """
   
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._trs = util.identity()
        self._l2world = util.identity()
        self._l2cam = util.identity()
        self._parent = self
        self._children = []
         
    @property #trs
    def trs(self):
        """ Get Component's transform: translation, rotation ,scale """
        return self._trs
    @trs.setter
    def trs(self, value):
        self._trs = value

    @property #l2world
    def l2world(self):
        """ Get Component's local to world transform: translation, rotation ,scale """
        return self._l2world
    @l2world.setter
    def l2world(self, value):
        self._l2world = value
        
    @property #l2cam
    def l2cam(self):
        """ Get Component's local to camera transform: translation, rotation ,scale, projection """
        return self._l2cam
    @l2cam.setter
    def l2cam(self, value):
        self._l2cam = value                 
    
    def update(self, **kwargs):
        """ Local 2 world transformation calculation
        Traverses upwards whole scenegraph and multiply all transformations along this path
        
        Arguments could be "l2world=" or "trs=" or "l2cam=" to set respective matrices 
        """
        print(self.getClassName(), ": update() called")
        arg1 = "l2world"
        arg2 = "trs"
        arg3 = "l2cam"
        if arg1 in kwargs:
            print("Setting: ", arg1," with: ", kwargs[arg1])
            self._l2world = kwargs[arg1]
        if arg2 in kwargs:
            print("Setting: ", arg2," with: ", kwargs[arg2])
            self._trs = kwargs[arg2]
        if arg3 in kwargs:
            print("Setting: ", arg3," with: ", kwargs[arg3])
            self._l2cam = kwargs[arg3]
        
       
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        
        system.apply(self) #from TransformSystem
        system.applyCamera(self) #from CameraSystem
        """
        if (isinstance(system, System.TransformSystem)):
            system.apply(self)
        
        if (isinstance(system, System.CameraSystem)):
            system.applyCamera(self)
        """
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 


class Camera(Component):
    """
    An example of a concrete Component Camera class
    
    Contains a basic Projection matrices (otrhographic or perspective)
    
    :param Component: [description]
    :type Component: [type]
    """
   
    def __init__(self, projMatrix, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._projMat = projMatrix
        self._root2cam = util.identity()
        self._parent = self
         
    @property #projMat
    def projMat(self):
        """ Get Component's camera Projection matrix """
        return self._projMat
    @projMat.setter
    def projMat(self, value):
        self._projMat = value
    
    @property #_root2cam
    def root2cam(self):
        """ Get Component's root to camera matrix """
        return self._root2cam
    @root2cam.setter
    def orthoroot2camMat(self, value):
        self._root2cam = value                   
    
    def update(self, **kwargs):
        """ Update Camera matrices
        
        Arguments could be "root2cam=" to set respective matrices 
        """
        print(self.getClassName(), ": update() called")
        arg1 = "root2cam"
        if arg1 in kwargs:
            print("Setting: ", arg1," with: ", kwargs[arg1])
            self._root2cam = kwargs[arg1]
       
       
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        
        # In Python due to ducktyping, either call a System concrete method
        # or leave it generic as is and check within System apply() if the 
        #correct node is visited (there is no automatic inference which System to call 
        # due to its type. We need to call a System specific concrete method otherwise)
        system.apply(self)
    
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 

class RenderMesh(Component):
    """
    A concrete RenderMesh class

    :param Component: [description]
    :type Component: [type]
    """
    def __init__(self, name=None, type=None, id=None):
        self._name = name
        self._type = type
        self._id = id
        self._trs = util.identity()
        self._parent = self
        self._children = []
    
    def draw(self):
        print(self.getClassName(), ": draw() called")
        
    def update(self):
        print(self.getClassName(), ": update() called")
        self.draw()
   
    def accept(self, system: System):
        """
        Accepts a class object to operate on the Component, based on the Visitor pattern.

        :param system: [a System object]
        :type system: [System]
        """
        system.apply(self)
    
    def init(self):
        """
        abstract method to be subclassed for extra initialisation
        """
        pass
    
    def __iter__(self) ->CompNullIterator:
        """ A component does not have children to iterate, thus a NULL iterator
        """
        return CompNullIterator(self) 
    