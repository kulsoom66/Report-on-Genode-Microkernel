#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:44:37 2021

@author: Mawada Khalfan Nasser Al-Husaini
         Marya Mohaamd Hamdoon Al Rahbi 
         Alzharaa Al-Sulimani
         Kalthoom Shouckt

version 3.6

Introduction to the program: This is a stand alone program that represents the
status information system program. Return some status inforamtion of the operating system.

This code has 5 processes and some of the 
process applies the multithreading.

We applied two features that are:
    - process creation
    - Multi-threading
    
    
"""
import psutil
import platform
from datetime import datetime
import multiprocessing
from threading import Thread


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getSystemInformataion():
    '''
    Purpose: Get the system information like:
        - Node name
        - Release
        - Version
        - Root
        - Machine
        - Processor
    '''
    print("="*40)
    print()
    print("System Information")
    print()
    print("="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    

def getBootTimeInformation():
    '''
    Get the boot time information like:
        - Boot time
        - Boot date
    '''
    print("="*40)
    print()
    print("Boot Time")
    print()
    print("="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    
    
def  getNumOfCores():
    '''
    Get the number of the phsical cores and total cores
    '''
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    
def getCPUfrequency():
    '''
    Get the frequency of the CPU
    '''
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    
def getCPUusage():
    '''
    Get the CPU usage
    '''
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    
    

def getCPUinformation():
    '''
    Get the CPU information using three threads
    '''
    print("="*40)
    print()
    print("CPU Info")
    print()
    print("="*40)
    
    #Create a thread to display the CPU information
    t_core = Thread(target= getNumOfCores)
    t_core.start()
    t_core.join()
    
    #Create a thread to get the CPU frequency
    t_f = Thread(target= getCPUfrequency)
    t_f.start()
    t_f.join()
    
    #Create a thread to get the CPU usage
    t_usage = Thread(target= getCPUusage)
    t_usage.start()
    t_usage.join()
    
def getSwap():
    '''
    get the swap memory details (if exists)
    '''
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    
def getMemoryInformation():
    '''
    Get the memory information
    '''
    print("="*40)
    print()
    print("Memory Information")
    print()
    print("="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    #print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    
    t_swap = Thread(target= getSwap)
    t_swap.start()
    t_swap.join()
    
    
def getDiskInformatione():
    '''
    Get the disk information
    '''
    print("="*40)
    print()
    print("Disk Information")
    print()
    print("="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")



if __name__ =='__main__': 

    #Create a process to get the current system information
    process_SI = multiprocessing.Process(target= getSystemInformataion)
    process_SI.start()
    process_SI.join()
    
    
    #Create a process to get the boot time of the machine
    process_BT = multiprocessing.Process(target= getBootTimeInformation)
    process_BT.start()
    process_BT.join()
    
    
    #Create a process to get the CPU information
    process_CPU = multiprocessing.Process(target= getCPUinformation)
    process_CPU.start()
    process_CPU.join()
    
    #Create a process to get the memory information
    process_memory = multiprocessing.Process(target= getMemoryInformation)
    process_memory.start()
    process_memory.join()
    
    #Create a process to get the memory information
    process_disk = multiprocessing.Process(target= getDiskInformatione)
    process_disk.start()
    process_disk.join()











