# Server class to simulate session storage
class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.sessions = {}  # Dictionary to store session data (simulates database/cache)

    def handle_request(self, request_id, session_id, data):
        # Check if session exists for this server
        if session_id in self.sessions and self.sessions[session_id]["server_id"] == self.server_id:
            # Valid session, access and update data
            self.sessions[session_id]["data"] = data
            print(f"Server {self.server_id}: Processing request {request_id} for session {session_id} (Data: {data})")
        else:
            # New session or invalid server for session
            print(f"Server {self.server_id}: Session {session_id} not found or not assigned to this server.")


# Simulate multiple servers
server1 = Server(1)
server2 = Server(2)
servers = {1: server1, 2: server2}

# Simulate a user session with a sticky session ID
user_session_id = "user_session_123"
server1.sessions[user_session_id] = {"server_id": 1, "data": "Initial data"}

# Simulate user requests with sticky session ID
for i in range(1, 4):
    request_data = f"Request data {i}"
    # Simulate load balancer routing (replace with actual load balancing logic)
    server = servers.get(user_session_id)  # Simple modulo for server selection
    if server:
        server.handle_request(i, user_session_id, request_data)
    else:
        print(f"Server not found for session {user_session_id}")
