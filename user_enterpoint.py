#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/2/24
# @Author  : Jesson 
# @Blog    : http://www.cnblogs.com/hellojesson/
#

import getpass
import os
import subprocess

from django.contrib.auth import authenticate

class UserPortal(object):
    """用户命令行端交互入口"""
    def __init__(self):
        pass

    def user_auth(self):
        """完成用户 登录验证交互"""
        retry_count = 0
        while retry_count < 3:
            username = input("username:").strip()
            if len(username) == 0:continue
            password = getpass.getpass("Password:").strip()
            if len(password) == 0:
                print("Password cannot be null !!!")
                continue
            user = authenticate(username = username,password= password)
            # 如果user为真 则表示登录成功
            if user :
                self.user = user
                print("welcome login ...")
                # 用户验证登录成功后，跳出循环
                break
            else:
                print("Invalid Username or Password !!!")
            retry_count  += 1

        else:
            exit("Too many attempts!!!")


    def interactive(self):
        """交互函数"""
        self.user_auth()

        if self.user:
            exit_flag = False
            while not exit_flag:
                # 找到该用户 关联的所有主机 和 属组
                # print(self.user.bind_hosts.select_related())
                # print(self.user.bind_groups.select_related())

                User_bind_hosts_count = self.user.bind_hosts.select_related().count()
                User_host_groups = self.user.host_groups.all()
                User_host_groups_count = self.user.host_groups.select_related().count()

                for index, host_group in enumerate(User_host_groups):
                    print("%s,%s[%s]" % (index,host_group.name, User_host_groups_count))
                print("%s. Ungrouped[%s]" % (index+1, User_bind_hosts_count))

                user_input = input("Choose Group:").strip()
                if len(user_input) == 0:continue
                # 判断用户输入是否是数字
                if user_input.isdigit():
                    user_input = int(user_input)
                    # if user_input >= 0 and user_input < User_host_groups.count(): 或者下方的方式
                    if user_input >= 0 and user_input < User_host_groups_count:
                        selected_hostgroup = User_host_groups[user_input]

                    elif user_input == User_host_groups_count: # 选中了未分组的那组主机 （注意:上方用的Index+1,这里只是适用总共两个分组的情况）
                        selected_hostgroup = self.user

                    else:
                        print("invalid host group ！！！")
                        continue

                    # 获取 该用户所在主机组中的 所有机器
                    User_selected_hostgroup_hosts = selected_hostgroup.bind_hosts.all()

                    while True:
                        for index,bind_host in enumerate(User_selected_hostgroup_hosts):
                            print("%s,%s(%s user:%s)" % (index, bind_host.host_user,
                                                         bind_host.host.ip_addr,
                                                         bind_host.host_user.username))

                        user_input2 = input("Choose Host:").strip()
                        if len(user_input2) == 0: continue
                        # 判断用户输入是否是数字
                        if user_input2.isdigit():
                            user_input2 = int(user_input2)
                            # print(User_selected_hostgroup_hosts.count())
                            if user_input2 >= 0 and user_input2 < User_selected_hostgroup_hosts.count():
                                selected_bindhost = User_selected_hostgroup_hosts[user_input2]
                                print("logging host success!!!", selected_bindhost)
                                loggin_cmd = 'sshpass -p {password} ssh {user}@{ip_addr}  -o "StrictHostKeyChecking no"'.format(password=selected_bindhost.host_user.password,
                                                                                                                                user=selected_bindhost.host_user.username,
                                                                                                                                ip_addr=selected_bindhost.host.ip_addr)
                                print(loggin_cmd)
                                ssh_instance = subprocess.run(loggin_cmd,shell=True)
                                print("------------logging out --------------")
                                break

                        if user_input2 == "b":
                            break
                            exit_flag = True














if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyFort.settings")
    import django
    django.setup()

    from audit import models
    portal = UserPortal()
    portal.interactive()

