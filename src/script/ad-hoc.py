# coding=utf-8
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.playbook.play import Play

Options = namedtuple('Options', ['forks'])
option = Options(forks=5)


"""
TaskQueueManager:
    资源资产清单：
        InventoryManager
        VariableManager
        
    执行选项：
        Options
        
    执行对象和模块：
        Play

"""
