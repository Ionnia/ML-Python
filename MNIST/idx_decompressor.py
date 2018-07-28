# Module that decompresses IDX File format


# Returns N-dimensional list from IDX file
def idx_decompress(filename):
    raw_bytes = open(filename, 'rb')
    data_type = None
    data_size = 0   # Size of each element in bytes
    # Skipping first two bytes in a magic number (first two bytes are always zero)
    raw_bytes.read(2)
    # Retrieving data type (3-rd byte)
    byte = int.from_bytes(raw_bytes.read(1), byteorder='big')
    if byte == 0x08:
        data_type = 'ubyte'     # 1 byte
        data_size = 1
    elif byte == 0x09:
        data_type = 'byte'      # 1 byte
        data_size = 1
    elif byte == 0x0b:
        data_type = 'short'     # 2 bytes
        data_size = 2
    elif byte == 0x0c:
        data_type = 'int'       # 2 bytes
        data_size = 2
    elif byte == 0x0d:
        data_type = 'float'     # 4 bytes
        data_size = 4
    elif byte == 0x0e:
        data_type = 'double'    # 8 bytes
        data_size = 8
    print('DataType: ' + data_type)
    print('DataSize: ' + str(data_size) + ' byte(s)')
    # Retrieving number of dimensions (4-th byte)
    num_of_dimensions = int.from_bytes(raw_bytes.read(1), byteorder='big')
    print('Dimensions: ' + str(num_of_dimensions))
    # Retrieving size of each dimensions
    dimensions_sizes = []
    data_amount = 1  # Amount of all elements
    for i in range(num_of_dimensions):
        # Size of each dimension is represented by 4-byte value
        byte = int.from_bytes(raw_bytes.read(4), byteorder='big')
        dimensions_sizes.append(byte)
        data_amount *= dimensions_sizes[i]
    print('Dimensions sizes: ' + str(dimensions_sizes))
    print('Size of data: ' + str(data_amount))
    print('Size of bytes: ' + str(data_amount * data_size))
    return _retrieve_data(raw_bytes, data_type, data_size, num_of_dimensions, dimensions_sizes)


# Recursively retrieving data from file into N-dimensional list
def _retrieve_data(file, dtype, dsize, num_of_dims, size_of_dims, cur_dim=None):
        # Default parameter cur_dim
        if cur_dim is None:
            cur_dim = 0
        # Default case where we in the last dimension
        if cur_dim == num_of_dims:
            if dtype == 'float' or dtype == 'double':
                # TODO: Don't know if this code is working correctly.
                return float.fromhex(file.read(dsize).hex())
            else:
                return int.from_bytes(file.read(dsize), byteorder='big')
        else:
            result = []
            for i in range(size_of_dims[cur_dim]):
                if cur_dim == 0:
                    percentage = (i/size_of_dims[0])*100
                    print('\rData retrieved %%%.2f' % percentage, end='')
                    if i == size_of_dims[0]-1:
                        print()
                result.append(_retrieve_data(file, dtype, dsize, num_of_dims, size_of_dims, cur_dim+1))
            return result
