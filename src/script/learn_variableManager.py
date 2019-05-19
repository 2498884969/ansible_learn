from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager


def main():
    loader = DataLoader()
    # sources 为hosts文件数组
    inv = InventoryManager(loader=loader, sources=['./ansible_etc/hosts'])
    varivaleManager = VariableManager(loader=loader, inventory=inv)
    """
    varivaleManager.get_vars()
    varivaleManager.get_vars(self, play=None, host=None, task=None, include_hostvars=True, include_delegate_to=True, use_cache=True)
    host.vars
    host.set_variable   
    """