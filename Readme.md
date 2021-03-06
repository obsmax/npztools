# NPZTOOLS

Tools to manage npz files  

## install (conda)
```
conda activate myenv
cd /path/to/npztools

pip install -e .
```


## usage

### dictionary managment

to write a npz file :  
```
import numpy as np
from npztools.containers import Container

cont = Container(
    x = np.arange(10),
    y = np.arange(20),
    z = 3.0)
    
cont.savez('toto.npz', allow_pickle=False)
```

to load a npz file :

```
cont = Container()
    
cont.loadkeys('toto.npz', ["x", "z"])
# cont.loadkeys('toto.npz', "*")  # to load all fields
print(cont.x)
```

### Advanced usage

Containers can be used to store the internal data of a custom object without pickling.  
This makes the file fully independent from the system and from the class which created it.  
It can be easily saved, shared, reloaded and displayed, see below :  

```
import numpy as np
from npztools.containers import Container


class MyObject(Container):
    extension = ".xy.npz"
    
    def __init__(self, x=None, y=None):
        # initiate from x, y or nothing (default nothing)
        self.x = x
        self.y = y
        
    def load(self, filename):
        # initiate from filename
        if not filename.endswith(self.extension):
            raise IOError(f'{filename} does not end with .xy.npz')
        cont = Container()
        cont.loadkeys(filename, ['x', 'y'])
        MyObject.__init__(self, cont.x, cont.y)
            
    def savez(self, filename):
        if not filename.endswith(self.extension):
            raise IOError(f'{filename} must end with .xy.npz')
        Container.savez(self, filename, allow_pickle=False)

    def show(self, ax, *args, **kwargs):
        return ax.plot(self.x, self.y, *args, **kwargs)


if __name__ == "__main__:

    # === create an object and save it
    o = MyObject(
        x=np.arange(10),    
        y=np.arange(10))
    
    o.savez('toto.xy.npz')
    del o
    
    # === call "npzinfo toto.xy.npz" to see the file content from command line
    
    # === create an object from its saved version
    o = MyObject()
    o.load('toto.xy.npz')
    
    import matplotlib.pyplot as plt
    o.show(plt.gca(), 'ko')
    plt.show()
```

