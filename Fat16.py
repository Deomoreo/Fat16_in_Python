import struct

with open("test.img", mode='rb') as file:
    fileContent = file.read()

Boot_Sector = bytearray()
for number in range(512):
    Boot_Sector.append(fileContent[number])

reserved_sectors = Boot_Sector[14] + Boot_Sector[15]
print("Reserved sectors", reserved_sectors)

sector_size = int(hex(Boot_Sector[12])[2] + hex(Boot_Sector[11])[2]+'0', 16)
print("sector size ", sector_size)

FAT_size = int(hex(Boot_Sector[22]), 16)
print("FAT size ", FAT_size)

FAT_copies_num = Boot_Sector[16]
print("FAT copies", FAT_copies_num)

Root_start_address = sector_size + FAT_size * FAT_copies_num * sector_size
print("Root Dir start Address", hex(Root_start_address))

dir_entries = int(hex(Boot_Sector[18])[2] + hex(Boot_Sector[17])[2]+'0', 16)
print("Root Dir Entries ", dir_entries)

dir_entry_size = 32

dir_total_size = dir_entry_size * dir_entries
print("Root Dir Size H", hex(dir_total_size))

dir_sector_number = dir_total_size / sector_size
print("Root Dir Sectors", dir_sector_number)

cluster_starting_address = Root_start_address+dir_total_size
print("Cluster zone start address (Root dir start + root dir size)",
      hex(cluster_starting_address))

dir_region = bytearray()
data_zone = bytearray()

for number in range(dir_total_size):
    dir_region.append(fileContent[Root_start_address + number])

for number in range(5120):
    data_zone.append(fileContent[cluster_starting_address + number])
    #print(fileContent[Root_start_address + number])
    # print(hex(dir_region[0]))
    # for number in range(dir_entries):
    #current_entry = Root_start_address+ number*16
dirRow = 0
for number in range(5):
    currentCell = dirRow * 16
    currentRow = currentCell
    if (dir_region[currentCell] == 0):
        dirRow += 1
        continue
    entry_name = ''
    for entry_name_length in range(8):
        string_toAdd = struct.pack(
            '<b', dir_region[dirRow * 16 + entry_name_length])
        string_toAdd = str(string_toAdd).removeprefix("b'")
        string_toAdd = str(string_toAdd).removesuffix("'")
        entry_name += string_toAdd
        currentCell += 1
    
    print(entry_name)
    #Entry a directory
    isDirectory = dir_region[currentRow + 11]
    if isDirectory != 16:
        dirRow += 2
        continue

    directory_cluster = dir_region[currentRow + 26] - 2
    directory_cluster_address = directory_cluster * 512
    #directory_cluster_address += 64
    directory_cluster_row = 0

    for dir_cluster_row in range(14):
        RowFirstCell = directory_cluster_row * 16 + directory_cluster_address
        fileName = ''
        for file_name_length in range(11):
            string_toAdd = struct.pack(
            '<b', data_zone[RowFirstCell + file_name_length])
            string_toAdd = str(string_toAdd).removeprefix("b'")
            string_toAdd = str(string_toAdd).removesuffix("'")
            fileName += string_toAdd
        if string_toAdd[0] != '\\':
            print(fileName)
        directory_cluster_row += 2        

    dirRow += 2
    # for file_extension_lenght in range(3):
    #     a

    # print(string_toAdd)
    #entry_name_unpack = struct.unpack('<b',string_toAdd)
    #entry_name += bytes.fromhex(entry_name).decode('utf-8')
    #entry_name = struct.pack('ci', b'*', dir_region[entry_name_length])
    #entry_name = struct.pack('<I',string_toAdd)
    #entry_name += string_toAdd
    #print (entry_name_unpack)
