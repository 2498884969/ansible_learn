from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader


def main():
    loader = DataLoader()
    # sources 为hosts文件数组
    inv = InventoryManager(loader=loader, sources=['./ansible_etc/hosts'])
    """
    inv.get_groups_dict
    inv.add_host
    inv.get_hosts
    inv.get_host
    """