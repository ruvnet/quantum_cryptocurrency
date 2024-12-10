import os

WILLOW_QUBITS = int(os.getenv('WILLOW_QUBITS', '105'))
WILLOW_COHERENCE_TIME = int(os.getenv('WILLOW_COHERENCE_TIME', '100'))
ERROR_CORRECTION_ENABLED = (os.getenv('ERROR_CORRECTION_ENABLED', 'true').lower() == 'true')

P2P_PORT = int(os.getenv('P2P_PORT', '8333'))
NODE_NAME = os.getenv('NODE_NAME', 'QuantumNode1')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
