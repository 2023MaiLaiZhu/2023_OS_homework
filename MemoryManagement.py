import re


class MemoryManager:
    def __init__(self, allocator):
        self.allocator = allocator
    def allocate(self, process, request_size):
        memory_view = self.allocator.memory_view()
        # Find consecutive free blocks in the memory block list to meet the requested memory size here is "first fit"
        start = -1
        count = 0
        for i, block in enumerate(memory_view):
            if block is None:
                count += 1
                if count == request_size:#Enough space for put a process
                    start = i - request_size + 1
                    break
            else:
                count = 0
        if start != -1:# If a suitable block of memory is found, it is allocated to the process
            self.allocator.allocate_memory(start, request_size, process)
        else:#Could not find a suitable contiguous block of memory
            # Attempt to free the memory block and reallocate
            self.release_and_allocate()
            self.allocate(process, request_size)
    def release_and_allocate(self):
        memory_view = self.allocator.memory_view()
        # free memory block and reallocate
        for i, block in enumerate(memory_view):
            if block is not None:#If there is a process in this place
                #free the memory block
                self.allocator.free_memory(block)
                # Attempt to reallocate memory block
                request_size = block.get_memory()
                #print(request_size)
                self.allocate(block, request_size[1])


