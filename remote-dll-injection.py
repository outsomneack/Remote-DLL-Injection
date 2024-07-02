from ctypes import *
from ctypes import wintypes

OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
OpenProcess.restype = wintypes.HANDLE

VirtualAllocEx = windll.kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = (wintypes.HANDLE, wintypes.LPVOID, c_size_t, wintypes.DWORD, wintypes.DWORD)
VirtualAllocEx.restype = wintypes.LPVOID

WriteProcessMemory = windll.kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, c_size_t, POINTER(c_size_t))
WriteProcessMemory.restype = wintypes.BOOL

GetModuleHandleA = windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = (LPCSTR, )
GetModuleHandleA.restype = wintypes.HANDLE

GetProcAddress = windll.kernel32.GetProcAddress
GetProcAddress.argtypes = (wintypes.HANDLE, c_char_p)
GetProcAddress.restype = wintypes.LPVOID

class _SECURITY_ATTRIBUTES(Structure):
	_fields_ = [('nLength', wintypes.DWORD),
				('lpSecurityDescriptor', wintypes.LPVOID),
				('bInheritHandle', wintypes.BOOL),]

SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = POINTER(SECURITY_ATTRIBUTES)

CreateRemoteThread = windll.kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = (wintypes.HANDLE, LPSECURITY_ATTRIBUTES, c_size_t, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD) 
CreateRemoteThread.restype = wintypes.HANDLE

MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PAGE_READWRITE = 0x04
EXECUTE_IMMEDIATELY = 0x0
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0x00000FFF)

path_to_dll = b""

pid = 0

handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

remote_memory = VirtualAllocEx(handle, False, len(dll) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
print("Handle obtained => {0:X}".format(handle))

write = WriteProcessMemory(handle, remote_memory, dll, len(dll) + 1, None)
print("Memory allocated =>", hex(remote_memory))

load_lib = GetProcAddress(GetModuleHandle(b"kernel32.dll"), b"LoadLibraryA")
print("LoadLibrary address =>", hex(load_lib))

rthread = CreateRemoteThread(handle, None, 0, load_lib, remote_memory, EXECUTE_IMMEDIATELY, None)
