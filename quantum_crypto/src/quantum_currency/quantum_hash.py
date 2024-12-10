from .quantum_resource_manager import QuantumResourceManager
from ...config.config import WILLOW_QUBITS, WILLOW_COHERENCE_TIME, ERROR_CORRECTION_ENABLED

qrm = QuantumResourceManager(
    qubits=WILLOW_QUBITS, 
    coherence_time=WILLOW_COHERENCE_TIME, 
    error_correction=ERROR_CORRECTION_ENABLED
)

def quantum_hash(transaction_data):
    quantum_state = qrm.initialize_quantum_state(transaction_data)
    transformed_state = qrm.apply_gates(quantum_state, ['H', 'CNOT', 'T', 'S'])
    return qrm.measure_state(transformed_state)
