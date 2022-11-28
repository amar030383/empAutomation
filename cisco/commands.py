wr = {'wr':1}
do_wr = {'do wr':1}
term_len = {'terminal len 0':1}
show_bootvar = {"show bootvar | in BOOT":1}
dir_flash_freeBytes = {"dir flash: | in bytes":1}
show_ip_int_brief = {'show ip interface brief':1}
show_cdp_nei_det = {'show cdp neighbors detail':2}
show_ip_ospf_nei = {"show ip ospf neighbor": 2}
show_ip_eigrp_nei = {"show ip eigrp neighbors":2}
show_ip_bgp_nei = {"show ip bgp neighbors":2}
show_ip_bgp_sum = { "show ip bgp summary":1}
show_run = {'show run':4}
show_clock = {'show clock' : 1} 

ios_upgrade_commands2 = [show_bootvar, dir_flash_freeBytes, show_clock]

ios_upgrade_commands = [wr, term_len, show_bootvar, dir_flash_freeBytes, show_ip_int_brief, show_cdp_nei_det, show_ip_ospf_nei, show_ip_eigrp_nei, show_ip_bgp_nei, show_ip_bgp_sum, show_clock]
ios_upgrade_commands1 = [wr, term_len, show_bootvar, dir_flash_freeBytes]