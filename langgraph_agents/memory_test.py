from workflow import store_agent_memory, get_latest_agent_memory

# Test storing memory
store_agent_memory("test_user", {"foo": "bar", "counter": 1})

# Test retrieving memory
memory = get_latest_agent_memory("test_user")
print(memory)  # Should print: {'foo': 'bar', 'counter': 1}