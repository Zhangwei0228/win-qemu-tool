import multiprocessing
import os
import random
import time
import tkinter as tk
from tkinter import filedialog
import pathlib
import configparser
import sys
import re


def get_home_dir_2():
    """
    获得当前用户家目录，支持windows，linux和macosx
    更新方法，更加简单
    :return:
    """
    homedir = str(pathlib.Path.home())
    return homedir


confige_path = os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf')


########################################################
#                      初始化工具                        #
########################################################


class status_env:
    status = None

    def __init__(self):
        self.status = False

    def set_status(self):
        self.status = True

    def show_status(self):
        return self.status


env_status = status_env()


def Environmental_testing():
    if os.path.exists(os.path.join(get_home_dir_2(), '.qemu_tools')):
        if os.path.exists(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf')):
            print("配置文件存在")
        else:
            with open(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'), 'w+', encoding='utf-8') as f:
                f.write('')
            print("没有配置文件正在创建")
    else:
        os.mkdir(os.path.join(get_home_dir_2(), '.qemu_tools'))
        with open(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'), 'w+', encoding='utf-8') as f:
            f.write('')
        print("没有配置文件正在创建")


def Select_the_Config(**args):
    cpu_slot = args['cpu_slot']  # cpu插槽
    cpu_core = args['cpu_core']  # cpu核心
    cpu_thread = args['cpu_thread']  # cpu 线程
    memory = args['memory']  # 内存
    network_mac = args['network_mac']  # 网卡mac
    guide_boot = args['guide_boot']  # boot引导
    drive = args['drive']  # 设备
    name = args['name']  # 设备名
    architecture = args['architecture']  # 架构
    network_command = args['network_command']
    iso_path = args['iso_path']
    # print(cpu_slot,cpu_core,cpu_thread,memory,network_command,name,network_mac,guide_boot,drive,architecture,iso_path)
    conf = configparser.ConfigParser()
    conf.read(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'))
    os.mkdir(os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), f'{name}'))
    try:
        conf.add_section(f"{name}")
    except configparser.DuplicateSectionError:
        print("已有同名虚拟机！！！！！")
        main()
    conf.set(f"{name}", "path",
             os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), f'{name}', f'{name}.conf'))
    with open(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'), 'w+') as ft:
        conf.write(ft)
    name_conf = configparser.ConfigParser()
    with open(os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), f'{name}', f'{name}.conf'), "w+") as wf:
        wf.write("")
    name_conf.read(os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), f'{name}', f'{name}.conf'))
    name_conf.add_section(f'{name}')
    name_conf.set(section=name, option='cpu_slot', value=f"{cpu_slot}")
    name_conf.set(section=name, option='cpu_core', value=f"{cpu_core}")
    name_conf.set(section=name, option='cpu_thread', value=f"{cpu_thread}")
    name_conf.set(section=name, option='memory', value=f"{memory}")
    name_conf.set(section=name, option='network_mac', value=network_mac)
    name_conf.set(section=name, option='guide_boot', value=guide_boot)
    name_conf.set(section=name, option='name', value=name)
    name_conf.set(section=name, option='architecture', value=architecture)
    name_conf.set(section=name, option='network_command', value=network_command)
    name_conf.set(section=name, option='iso_path', value=iso_path)
    count_drive = 0
    create_type = {'qcow2': 'qcow2', 'img': 'raw', 'vmdk': 'vmdk', "vdi": "vdi", "qed": "qed"}
    for i in drive:
        count_drive = count_drive + 1
        name_conf.set(section=name, option=f"drive{count_drive}_disk",
                      value=f"{os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), name, name + '.' + i['type'])}")
        name_conf.set(section=name, option=f'drive{count_drive}_disk_type', value=i['type'])
        name_conf.set(section=name, option=f'drive{count_drive}_disk_size', value=i['size'])
    with open(os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), f'{name}', f'{name}.conf'), "w+") as wtf:
        name_conf.write(wtf)
    clear()
    print(banner())
    for j in drive:
        print(f"***************************************创建第{j}个硬盘*******************************************")
        print("创建中。。。。。")
        # print(f"\"{os.path.join(conf.get('qemu_env', 'Program_of_execution'),'qemu-img')}\" create -f {create_type[j['type']]} -o size={j['size']} {os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'),name,name+'.'+j['type'])}")
        os.system(
            f"\"\"{os.path.join(conf.get('qemu_env', 'Program_of_execution'), 'qemu-img')}\"\" create -f {create_type[j['type']]} -o size={j['size']} {os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'), name, name + '.' + j['type'])}")
        print("创建成功。。。。。")
    time.sleep(0.7)
    main()


# def get_config():
# Environmental_testing()

def ask_dir(ask_title: str):
    window = tk.Tk()
    window.title(ask_title)
    window.geometry('720x180')
    tk.Label(window, text="文件夹路径：").place(x=50, y=50)
    var_name = tk.StringVar()
    entry_name = tk.Entry(window, textvariable=var_name, width=55)
    entry_name.place(x=120, y=50)

    def select_path_dir():
        path_ = filedialog.askdirectory()
        var_name.set(path_)

    tk.Button(window, text=f"{ask_title}路径选择", command=select_path_dir).place(x=525, y=45)
    tk.Button(text="确认", command=window.destroy).place(x=525, y=120)
    window.mainloop()
    return str(var_name.get())


def ask_file(ask_title: str, types):
    window = tk.Tk()
    window.title(ask_title)
    window.geometry('720x180')
    tk.Label(window, text="文件夹路径：").place(x=50, y=50)
    var_name = tk.StringVar()
    entry_name = tk.Entry(window, textvariable=var_name, width=55)
    entry_name.place(x=120, y=50)

    def select_path_dir():
        path_ = filedialog.askopenfilename(filetypes=[(f"{ask_title}", types)])
        var_name.set(path_)

    tk.Button(window, text=f"{ask_title}路径选择", command=select_path_dir).place(x=525, y=45)
    tk.Button(text="确认", command=window.destroy).place(x=525, y=120)
    window.mainloop()
    return str(var_name.get())


def read_conf():
    conf = configparser.ConfigParser()
    conf.read(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'))
    print('读取配置文件中')
    time.sleep(0.3)
    if len(conf.sections()) == 0:
        print("配置文件未找到相关环境")
        time.sleep(0.3)
        print('需要手动指定')
        time.sleep(0.6)
        Program_of_execution = ask_dir("qemu 执行程序目录")
        Storage_location_of_the_VM = ask_dir("虚拟机存放位置")
        conf.add_section('qemu_env')
        conf.set('qemu_env', 'Program_of_execution', Program_of_execution)
        conf.set('qemu_env', 'Storage_location_of_the_VM', Storage_location_of_the_VM)
        with open(os.path.join(get_home_dir_2(), '.qemu_tools', 'tools.conf'), 'w') as f:
            conf.write(f)
        print(f"qemu 安装路径：{Program_of_execution}")
        print(f"虚拟机存放路径：{Storage_location_of_the_VM}")
    else:
        Program_of_execution = conf.get('qemu_env', 'Program_of_execution')
        Storage_location_of_the_VM = conf.get('qemu_env', 'Storage_location_of_the_VM')
        print(f"qemu 安装路径：{Program_of_execution}")
        print(f"虚拟机存放路径：{Storage_location_of_the_VM}")


# def main():
def banner():
    text = '''
                                                    $$\                        $$\           
                                                    $$ |                       $$ |          
 $$$$$$\   $$$$$$\  $$$$$$\$$$$\  $$\   $$\       $$$$$$\   $$$$$$\   $$$$$$\  $$ | $$$$$$$\ 
$$  __$$\ $$  __$$\ $$  _$$  _$$\ $$ |  $$ |$$$$$$\_$$  _| $$  __$$\ $$  __$$\ $$ |$$  _____|
$$ /  $$ |$$$$$$$$ |$$ / $$ / $$ |$$ |  $$ |\______|$$ |   $$ /  $$ |$$ /  $$ |$$ |\$$$$$$\  
$$ |  $$ |$$   ____|$$ | $$ | $$ |$$ |  $$ |        $$ |$$\$$ |  $$ |$$ |  $$ |$$ | \____$$\ 
\$$$$$$$ |\$$$$$$$\ $$ | $$ | $$ |\$$$$$$  |        \$$$$  \$$$$$$  |\$$$$$$  |$$ |$$$$$$$  |
 \____$$ | \_______|\__| \__| \__| \______/          \____/ \______/  \______/ \__|\_______/ 
      $$ |                                                                                   
      $$ |                                                                                   
      \__|                                                                                 
*************************************欢迎使用qemu小工具******************************************      
###############################################################################################
##                               注意虚拟机存放位置路径不能有中文                                  ##
###############################################################################################
      '''
    return text


def get_os():
    return sys.platform


def clear():
    os_clear = get_os()
    if os_clear == "win32":
        os.system('cls')
    elif os_clear == "linux":
        os.system('clear')
    else:
        os.system('clear')


def Main_Screen():
    clear()
    print(banner())
    print("\n")
    print('[1].创建虚拟机   [2].查看虚拟机信息   [3].修改虚拟机配置   [4].启动虚拟机   [5].退出程序')
    print("\n")
    operation_bool = True
    operation_count = 0
    while operation_bool:
        try:
            operation_num = int(input("请输入对应的操作 (默认退出程序,输错5次退出程序): "))
            operation_bool = False
        except ValueError:
            operation_count = operation_count + 1
            print(f"您输入了错误类型的数值 输入错误{operation_count}次")
            if operation_count >= 5:
                break
    if operation_bool is False and operation_num != 5:
        main_control(operation_num)


def detection():
    clear()
    print(banner())
    print('******************************************检测环境***********************************************')
    Environmental_testing()
    read_conf()
    env_status.set_status()
    print('******************************************检测成功***********************************************')


def main():
    if env_status.show_status() is False:
        detection()
    time.sleep(1.3)
    clear()
    Main_Screen()


########################################################
#                   创建虚拟机工具                       #
########################################################
def create_VM():
    architecture_list = ['qemu-system-aarch64', 'qemu-system-alpha', 'qemu-system-arm', 'qemu-system-avr',
                         'qemu-system-cris', 'qemu-system-hppa', 'qemu-system-i386', 'qemu-system-loongarch64',
                         'qemu-system-m68k', 'qemu-system-microblaze', 'qemu-system-microblazeelw', 'qemu-system-mips',
                         'qemu-system-mips', 'qemu-system-x86_64', 'qemu-system-ppc64w', 'qemu-system-riscv32',
                         'qemu-system-riscv64w', 'qemu-system-sparc64w']
    clear()
    print(banner())
    count = 0
    print("**************************************选择虚拟系统架构*******************************************")
    for i in architecture_list:
        count = count + 1
        print(f"[{count}].{i}", end=" ")
        if count % 5 == 0:
            print("\n")
        if count == len(architecture_list):
            print("\n")
    print("*************************************************************************************************")
    select_architecture_count = 0
    while True:
        try:
            select_architecture = int(input("请输入要虚拟的架构: "))
            break
        except ValueError:
            select_architecture_count = select_architecture_count + 1
            print('输入的类型不对')
            if select_architecture_count >= 5:
                break
    architecture = architecture_list[select_architecture - 1]
    clear()
    print(banner())
    print("**************************************选择虚拟cpu插槽*******************************************")
    cpu_slot = int(input('请输入cpu插槽数：'))
    print("***************************************选择cpu核心数*******************************************")
    cpu_core = int(input('请输入cpu核心数：'))
    print("***************************************选择cpu线程数*******************************************")
    cpu_thread = int(input('请输入cpu线程数：'))
    print("**************************************选择虚拟内存大小*******************************************")
    print("例如： 1024m  2G 等")
    memory = input("请输入需要的内存大小：")
    print("****************************************选择MAC地址*********************************************")
    print("[1].使用自定义MAC   [2].使用随机MAC      (自定义例如 1E:4F:48:D1:1C:1E)")
    mac_op = int(input("输入操作: "))
    if mac_op != 1:
        mac = random_MAC()
    else:
        mac = input("请输入自定义MAC")
    clear()
    print(banner())
    print("***************************************选择boot启动项********************************************")
    print(" a c d a为软盘 d为cdrom c为硬盘  谁在前面就优先谁  例如cd 就是优先硬盘在是cdrom")
    guide_boot = input("请输入正确的启动项:  ")
    print("****************************************设置虚拟机名称********************************************")
    name = input("请输入虚拟机名称：  ")
    print("*****************************************设置硬盘数量*********************************************")
    disk_num = int(input("请输入硬盘个数: "))
    drive_disk = []
    disk_num_count = 0
    for k in range(disk_num):
        disk_num_count = disk_num_count + 1
        drive_disk.append(create_disk(disk_num_count))
        clear()
        print(banner())
    print("****************************************设置虚拟机网络********************************************")
    print("[1].需要tap网络    [2].不需要桥接网络        （tap网络可以直接和主机通信）")
    net_op = int(input("请输入要求(注意tap网络： windows 需要安装 tap虚拟网卡)： "))
    if net_op <= 0 or net_op >= 3:
        net = "-nic user"
    elif net_op == 1:
        tap = input("请输入tap网卡名： ")
        net = f"-nic user  -netdev type=tap,id=net0,ifname={tap} -device virtio-net-pci,mac={mac},netdev=net0"
    else:
        net = "-nic user"
    clear()
    print(banner())
    print("****************************************设置虚拟机iso********************************************")
    iso_path = ask_file('镜像文件', ['iso'])
    clear()
    print(banner())
    print("****************************************查看虚拟机信息********************************************")
    print(f"虚拟架构为： {architecture}")
    print(f"cpu插槽 {cpu_slot} 个")
    print(f"cpu核心 {cpu_core} 个")
    print(f"cpu线程 {cpu_thread * cpu_core * cpu_slot} 个")
    print(f"虚拟机内存 {memory} ")
    print(f"虚拟机硬盘 {disk_num} 个")
    for h in range(disk_num):
        print(f"第{h + 1}个硬盘 类型：{drive_disk[h]['type']} 大小：{drive_disk[h]['size']}")
    print(f"镜像文件： {iso_path}")
    print(f"mac地址： {mac}")
    if net_op <= 0 or net_op >= 3:
        print("网络详情： 用户网络")
    elif net_op == 1:
        print("网络详情： 用户网络+tap网络")
    else:
        print("网络详情： 用户网络")
    print("!!!!!!!!!! 是否确认配置 !!!!!!!!!!!")
    confirm = input("请输入（y/n）: ")
    if confirm.lower() == "y".lower():
        Select_the_Config(cpu_slot=cpu_slot, cpu_core=cpu_core, cpu_thread=cpu_thread, network_mac=mac,
                          iso_path=iso_path, memory=memory, drive=drive_disk, guide_boot=guide_boot,
                          architecture=architecture, name=name, network_command=net)
    else:
        print("用户未确定，返回主页")
        main()


def create_disk(count: int):
    print(f"*****************************************创建第{count}disk********************************************")
    print("选择创建的硬盘类型：")
    disk_list = ['qcow2', 'img', 'raw', 'VMDK', 'VDI', 'qed']
    disk_count = 0
    for j in disk_list:
        disk_count = disk_count + 1
        print(f"[{disk_count}].{j}", end="  ")
        if disk_count % 5 == 0:
            print("\n")
        if disk_count == len(disk_list):
            print("\n")
    print("***********************************************************************************************")
    select_disk_type_num = int(input("请输入想要的disk类型： "))
    if select_disk_type_num <= 0 or select_disk_type_num > len(disk_list):
        disk_type = disk_list[0]
    else:
        disk_type = disk_list[select_disk_type_num - 1]
    print("****************************************创建多大的disk*******************************************")
    print("例如 ：4G   89G   1T  512M 等")
    disk_size = input("请输入需要多大disk： ")
    return {"type": disk_type, "size": disk_size}


def random_MAC():
    Maclist = []
    for i in range(1, 7):
        RANDSTR = "".join(random.sample("0123456789ABCDEF", 2))
        Maclist.append(RANDSTR)
    RANDMAC = ":".join(Maclist)
    return RANDMAC

    # drive = args['drive']  # 设备


########################################################
#                    主页控制器工具                       #
########################################################
def main_control(operation_num):
    if operation_num == 1:
        create_VM()
    elif operation_num == 2:
        show_vm_info()
    elif operation_num == 3:
        edit_VM_main()
    elif operation_num == 4:
        start_VM()
    else:
        pass


def show_vm_info():
    clear()
    print(banner())
    print("***************************************查看对应虚拟机信息*******************************************")
    conf = configparser.ConfigParser()
    conf.read(confige_path)
    # print(conf.sections())
    VM_list_conf = conf.sections().copy()[1:]
    # print(VM_list_conf)
    count = 0
    if len(VM_list_conf) == 0:
        print("你还没有创建虚拟机")
    else:
        for i in VM_list_conf:
            count = count + 1
            print(f"[{count}].{VM_list_conf[count - 1]}", end=" ")
            if count % 5 == 0:
                print("\n")
            if count == len(VM_list_conf):
                print("\n")
    option_info = int(input("请输入对应虚拟机编号："))
    if option_info <= 0:
        print("输入错误！")
        Main_Screen()
    elif option_info > len(VM_list_conf):
        print("输入错误！")
        Main_Screen()
    else:
        clear()
        print(banner())
        print("****************************************查看虚拟机信息********************************************")
        print(f"虚拟机为：{VM_list_conf[option_info - 1]}")
        VM_conf_info_path = conf.get(VM_list_conf[option_info - 1], 'path')
        conf = configparser.ConfigParser()
        conf.read(VM_conf_info_path)
        print(f"虚拟架构为： {conf.get(VM_list_conf[option_info - 1], 'architecture')}")
        print(f"cpu插槽 {conf.get(VM_list_conf[option_info - 1], 'cpu_slot')} 个")
        print(f"cpu核心 {conf.get(VM_list_conf[option_info - 1], 'cpu_core')} 个")
        print(f"cpu线程 {conf.get(VM_list_conf[option_info - 1], 'cpu_thread')} 个")
        print(f"虚拟机内存 {conf.get(VM_list_conf[option_info - 1], 'memory')} ")
        print(f"网卡mac地址：{conf.get(VM_list_conf[option_info - 1], 'network_mac')}")
        disk_list = []
        for i in conf.options('fedroa'):
            a = re.findall(r'drive[1-99]_disk$', i)
            if len(a) != 0:
                disk_list = disk_list + a
        # print(disk_list)
        # print(disk_list_type)
        disk_count = 0
        for k in disk_list:
            disk_count = disk_count + 1
            print(
                f"第{disk_count}块 硬盘类型为：{conf.get(VM_list_conf[option_info - 1], f'{k}_type')} 大小为：{conf.get(VM_list_conf[option_info - 1], f'{k}_size')}")
        net = conf.get(VM_list_conf[option_info - 1], 'network_command')
        if '-netdev' in net:
            print("网络为： 用户网络+桥接网络")
        else:
            print("网络为： 用户网络")
        iso_list = []
        for s in conf.options('fedroa'):
            iso = re.findall(r'iso_path$|iso_path[1-99]', s)
            iso_list = iso_list + iso
        iso_count = 0
        for iso_ in iso_list:
            iso_count = iso_count + 1
            print(f'iso 镜像{iso_count}:  {conf.get(VM_list_conf[option_info - 1], iso_)}')
        print("按任意键退出查看配置。。。。。。。。")
        option = input("")
        Main_Screen()


def edit_VM_main():  # control
    clear()
    print(banner())
    print("****************************************修改虚拟机配置********************************************")
    conf = configparser.ConfigParser()
    conf.read(confige_path)
    # print(conf.sections())
    VM_list_conf = conf.sections().copy()[1:]
    # print(VM_list_conf)
    count = 0
    if len(VM_list_conf) == 0:
        print("你还没有创建虚拟机")
    else:
        for i in VM_list_conf:
            count = count + 1
            print(f"[{count}].{VM_list_conf[count - 1]}", end=" ")
            if count % 5 == 0:
                print("\n")
            if count == len(VM_list_conf):
                print("\n")
    option_info = int(input("请输入对应虚拟机编号："))
    if option_info <= 0:
        print("输入错误！")
        Main_Screen()
    elif option_info > len(VM_list_conf):
        print("输入错误！")
        Main_Screen()
    else:
        clear()
        print(banner())
        name = VM_list_conf[option_info - 1]
        print("1.修改插槽数量                                        7.修改 iso镜像")
        print("")
        print("2.修改cpu核心数                                       8.添加硬盘")
        print("")
        print("3.修改cpu线程数                                       9.删除硬盘")
        print("")
        print("4.修改内存大小                                        10.添加 iso 镜像")
        print("")
        print("5.修改 MAC 地址                                       11.删除 iso 镜像")
        print("")
        print("6.修改 boot 启动 顺序                                 12.修改网络")
        print("")
        try:
            option = int(input("请输入对应的操作："))
        except ValueError:
            print("输入错误！！！！")
            time.sleep(1.2)
            Main_Screen()
        VM_conf_info_path = conf.get(VM_list_conf[option_info - 1], 'path')
        dir_path = conf.get('qemu_env', 'storage_location_of_the_vm')
        exec_path = conf.get('qemu_env', 'program_of_execution')
        conf = configparser.ConfigParser()
        conf.read(VM_conf_info_path)
        if option == 1:
            cpu_slot_num = int(input("请输入修改的  插槽 个数： "))
            edit_cpu_slot(conf, cpu_slot_num, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 2:
            cpu_core_num = int(input("请输入修改的  核心  个数： "))
            edit_cpu_core(conf, cpu_core_num, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 3:
            cpu_thread_num = int(input("请输入修改的  线程  个数： "))
            edit_cpu_thread(conf, cpu_thread_num, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 4:
            memory_size = input("请输入修改的  内存  大小(例如：4G 2048m 等等)： ")
            edit_memory(conf, memory_size, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 5:
            print("[1].使用随机mac                      [2].使用自定义MAC")
            MAC_option = int(input("请输入操作： "))
            if MAC_option == 2:
                mac = input("请输入MAC地址 例如  82:03:AB:BE:7E:13   ：  ")
            else:
                mac = random_MAC()
            edit_network_mac(conf, mac, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 6:
            print("修改 boot 启动 顺序   ")
            print("a c d a为软盘 d为cdrom c为硬盘  谁在前面就优先谁  例如cd 就是优先硬盘在是cdrom")
            boot = input("请输入boot启动顺序：  ")
            edit_guide_boot(conf, boot, name, VM_conf_info_path)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 7:
            print("修改 iso 镜像位置")
            iso_list = []
            for i in conf.options(name):
                iso_ = re.findall(r'iso_path$|iso_path[1-99]', i)
                iso_list = iso_list + iso_
            iso_count = 0
            for k in iso_list:
                iso_count = iso_count + 1
                print(f"[{iso_count}].iso 镜像： {conf.get(name, k)}", end="  ")
                if iso_count % 2 == 0:
                    print("\n")
                if iso_count == len(iso_list):
                    print("\n")
            edit_iso_option = int(input("请输入要修改的镜像"))
            if edit_iso_option <= 0:
                print("输入错误！ ")
                time.sleep(0.6)
                Main_Screen()
            elif edit_iso_option > len(iso_list):
                print("输入错误！ ")
                time.sleep(0.6)
                Main_Screen()
            else:
                iso_path = ask_file("选择iso", ['iso'])
                edit_iso_path(conf, iso_path, name, VM_conf_info_path, iso_list[edit_iso_option - 1])
                print("修改成功! ")
                time.sleep(0.6)
                Main_Screen()
        elif option == 8:
            print("添加硬盘")
            diskinfo = create_disk(1)
            list_disk = [int(re.findall('drive[1-99]_disk$', disk)[0][5:-5]) for disk in conf.options(name) if
                         len(re.findall('drive[1-99]_disk$', disk)) != 0]
            print(list_disk)
            all_sequence = [seq for seq in range(1, 100)]
            Unused_sequence = [u_seq for u_seq in all_sequence if u_seq not in list_disk]
            # print(Unused_sequence)
            add_disk(conf, name, dir_path, diskinfo, f'drive{Unused_sequence[0]}_disk', exec_path, Unused_sequence[0])
            print("添加成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 9:
            print("删除硬盘")
            list_disk = [int(re.findall('drive[1-99]_disk$', disk)[0][5:-5]) for disk in conf.options(name) if
                         len(re.findall('drive[1-99]_disk$', disk)) != 0]
            disk_count = 0
            for disk_list_info in list_disk:
                disk_count = disk_count + 1
                print(
                    f"[{disk_count}].第{disk_count}硬盘：类型 {conf.get(name, f'drive{disk_list_info}_disk_type')} 大小：{conf.get(name, f'drive{disk_list_info}_disk_size')}")
            delete_disk_option = int(input("请输入要删除的硬盘："))
            if delete_disk_option <= 0:
                print("输入错误！ ")
                time.sleep(0.6)
                Main_Screen()
            elif delete_disk_option > len(list_disk):
                print("输入错误！ ")
                time.sleep(0.6)
                Main_Screen()
            else:
                disk_count_ = 0
                for disk_list_info_ in list_disk:
                    disk_count_ += 1
                    if disk_count_ == delete_disk_option:
                        delete_disk(conf, name, VM_conf_info_path, f'drive{disk_list_info_}_disk')
                print("删除成功! ")
                time.sleep(0.6)
                Main_Screen()
        elif option == 10:
            print("添加iso文件")
            add_iso(conf, name, VM_conf_info_path)
            print("添加成功! ")
            time.sleep(0.6)
            Main_Screen()
        elif option == 11:
            print("删除iso镜像")
            delete_iso(conf, name, VM_conf_info_path)
        elif option == 12:
            clear()
            print(banner())
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<修改网络！>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("[1].需要tap网络    [2].不需要桥接网络        （tap网络可以直接和主机通信）")
            net_op = int(input("请输入要求(注意tap网络： windows 需要安装 tap虚拟网卡)： "))
            if net_op <= 0 or net_op >= 3:
                net = "-nic user"
            elif net_op == 1:
                tap = input("请输入tap网卡名： ")
                mac = conf.get(name, 'network_mac')
                net = f"-nic user  -netdev type=tap,id=net0,ifname={tap} -device virtio-net-pci,mac={mac},netdev=net0"
            else:
                net = "-nic user"
            edit_network(conf, name, VM_conf_info_path, net)
            print("修改成功! ")
            time.sleep(0.6)
            Main_Screen()
        else:
            print("输入错误！ ")
            time.sleep(0.6)
            Main_Screen()


##########################################################
#                      修改函数                           #
##########################################################
'''
name 为配置节点名称
例如：   [hello]   <------- 代表name
        option = value    <------- key=value   
'''


def edit_cpu_slot(conf: object, num: int, name: str, path: str):
    conf.set(name, "cpu_slot", f"{num}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_cpu_core(conf: object, num: int, name: str, path: str):
    conf.set(name, "cpu_core", f"{num}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_cpu_thread(conf: object, num: int, name: str, path: str):
    conf.set(name, "cpu_thread", f"{num}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_memory(conf: object, memory: str, name: str, path: str):
    conf.set(name, "memory", f"{memory}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_network_mac(conf: object, mac: str, name: str, path: str):
    conf.set(name, "network_mac", f"{mac}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_guide_boot(conf: object, boot: str, name: str, path: str):
    conf.set(name, "guide_boot", f"{boot}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_network_command(conf: object, command: str, name: str, path: str):
    conf.set(name, "network_command", f"{command}")
    with open(path, 'w+') as f:
        conf.write(f)


def edit_iso_path(conf: object, iso_path, name: str, path: str, key: str):
    conf.set(name, key, f"{iso_path}")
    with open(path, 'w+') as f:
        conf.write(f)


def delete_disk(conf: object, name: str, path: str, key: str):
    # print(key)
    files = conf.get(name, key)
    conf.remove_option(name, key)
    conf.remove_option(name, f"{key}_type")
    conf.remove_option(name, f"{key}_size")
    with open(path, 'w+') as f:
        conf.write(f)
    os.remove(files)


def add_disk(conf: object, name: str, path: str, info: dict, key: str, exec_path: str, Unused_sequence: int):
    create_type = {'qcow2': 'qcow2', 'img': 'raw', 'vmdk': 'vmdk', "vdi": "vdi", "qed": "qed"}
    conf.set(section=name, option=f"{key}",
             value=f"{os.path.join(path, name, name + '.' + info['type'])}")
    conf.set(section=name, option=f'{key}_type', value=info['type'])
    conf.set(section=name, option=f'{key}_size', value=info['size'])
    with open(os.path.join(path, f'{name}', f'{name}.conf'), "w+") as wtf:
        conf.write(wtf)
    clear()
    print(banner())
    print(f"*****************************************创建硬盘*******************************************")
    print("创建中。。。。。")
    # print(f"\"{os.path.join(conf.get('qemu_env', 'Program_of_execution'),'qemu-img')}\" create -f {create_type[j['type']]} -o size={j['size']} {os.path.join(conf.get('qemu_env', 'Storage_location_of_the_VM'),name,name+'.'+j['type'])}")
    os.system(
        f"\"\"{os.path.join(exec_path, 'qemu-img')}\"\" create -f {create_type[info['type']]} -o size={info['size']} {os.path.join(path, name, name + f'{Unused_sequence}' + '.' + info['type'])}")
    print("创建成功。。。。。")


def delete_iso(conf: object, name: str, path: str):
    iso_list = [re.findall(r'iso_path$|iso_path[1-99]', disk)[0] for disk in conf.options(name) if
                len(re.findall(r'iso_path$|iso_path[1-99]', disk)) != 0]
    clear()
    print(banner())
    print(f"************************************请选择删除的iso文件**************************************")
    iso_count = 0
    for i in iso_list:
        iso_count += 1
        print(f"[{iso_count}].镜像文件：{conf.get(name, i)}")
    delete_iso_option = int(input('请输入需要删除的iso'))
    if delete_iso_option <= 0:
        print("输入错误！ ")
        time.sleep(0.6)
        Main_Screen()
    elif delete_iso_option > len(iso_list):
        print("输入错误！ ")
        time.sleep(0.6)
        Main_Screen()
    else:
        iso_c = 0
        for j in iso_list:
            iso_c += 1
            if delete_iso_option == iso_c:
                conf.remove_option(name, j)


def add_iso(conf: object, name: str, path: str):
    iso_list = [re.findall(r'iso_path$|iso_path[1-99]', disk)[0] for disk in conf.options(name) if
                len(re.findall(r'iso_path$|iso_path[1-99]', disk)) != 0]
    if 'iso_path' not in iso_list:
        key = 'iso_path'
    else:
        iso_list.remove('iso_path')
        iso_list_used = [int(i[8:]) for i in iso_list]
        iso_list_all = [j for j in range(1, 100)]
        iso_list_unused = [k for k in iso_list_all if k not in iso_list_used]
        key = f'iso_path{iso_list_unused[0]}'
    iso_path = ask_file('选择iso文件', ['iso'])
    conf.set(name, key, iso_path)
    with open(path, 'w+') as f:
        conf.write(f)


def edit_network(conf: object, name: str, path: str, command: str):
    conf.set(name, 'network_command', command)
    with open(path, 'w+') as f:
        conf.write(f)


##########################################################
#                     结束修改函数                         #
##########################################################

##########################################################
#                      启动VM函数                         #
##########################################################

def start_VM_func(path: str):
    conf = configparser.ConfigParser()
    conf.read(path)
    name = conf.sections()[0]
    exec_file = conf.get(name, 'architecture')
    cpu_slot = conf.get(name, 'cpu_slot')
    cpu_core = conf.get(name, 'cpu_core')
    cpu_thread = conf.get(name, 'cpu_thread')
    boot = conf.get(name, "guide_boot")
    memory = conf.get(name, 'memory')
    network_command = conf.get(name, 'network_command')
    list_disk = [re.findall('drive[1-99]_disk$', disk)[0] for disk in conf.options(name) if
                 len(re.findall('drive[1-99]_disk$', disk)) != 0]
    iso_list = [re.findall('iso_path$|iso_path[1-99]', iso)[0] for iso in conf.options(name) if
                len(re.findall('iso_path$|iso_path[1-99]', iso)) != 0]
    disk_command = ''
    for i in list_disk:
        disk_command = disk_command + f"-drive file={conf.get(name, i)},media=disk,if=virtio"
    iso_command = ''
    if len(iso_list) != 0:
        for j in iso_list:
            iso_command = iso_command + f"-drive file={conf.get(name, j)},media=cdrom"
    conf.read(confige_path)
    exec_path = conf.get('qemu_env', 'program_of_execution')
    # print(exec_path)
    start_command = f"\"{os.path.join(exec_path, exec_file)}\" -accel whpx -machine q35 -smp sockets={cpu_slot},cores={cpu_core},threads={cpu_thread} -m {memory} -usb -device usb-kbd -device usb-tablet -rtc base=localtime  {iso_command} {disk_command} -name {name} -boot {boot} {network_command}"
    print(start_command)
    os.popen(start_command)


def start_VM():
    clear()
    print(banner())
    print("******************************************启动虚拟机*********************************************")
    conf = configparser.ConfigParser()
    conf.read(confige_path)
    # print(conf.sections())
    VM_list_conf = conf.sections().copy()[1:]
    # print(VM_list_conf)
    count = 0
    if len(VM_list_conf) == 0:
        print("你还没有创建虚拟机")
    else:
        for i in VM_list_conf:
            count = count + 1
            print(f"[{count}].{VM_list_conf[count - 1]}", end=" ")
            if count % 5 == 0:
                print("\n")
            if count == len(VM_list_conf):
                print("\n")
    option_info = int(input("请输入对应虚拟机编号："))
    if option_info <= 0:
        print("输入错误！")
        Main_Screen()
    elif option_info > len(VM_list_conf):
        print("输入错误！")
        Main_Screen()
    else:
        print("正在启动虚拟机.........")
        time.sleep(1.2)
        VM_path = conf.get(VM_list_conf[option_info - 1], 'path')
        start_VM_porcess= multiprocessing.Process(target=start_VM_func,args=(VM_path,))
        start_VM_porcess.start()
        time.sleep(5)
        print("启动成功")
        time.sleep(0.6)
        clear()
        Main_Screen()


##########################################################
#                     结束启动VM函数                       #
##########################################################

if __name__ == '__main__':
    # read_conf()
    main()
    # show_vm_info()
