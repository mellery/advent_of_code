#!/usr/bin/env python3
"""
Virtual Machine Components Library

Virtual machine and interpreter patterns extracted from AoC solutions.
Provides base classes and utilities for implementing custom VMs and assembly interpreters.

Key Features:
- VMBase class with common VM patterns
- Instruction decoding and parameter mode handling
- Memory management with automatic expansion
- I/O queue abstractions for inter-VM communication
- State management and debugging support
- Threading support for concurrent execution

Performance Targets:
- Instruction execution: < 1μs per instruction for simple operations
- Memory operations: < 10μs for typical memory sizes
- I/O operations: < 100μs for queue operations
"""

from typing import (
    Dict, List, Tuple, Optional, Callable, Any, Union,
    Iterator, Type, Protocol, Set
)
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from abc import ABC, abstractmethod
from collections import deque
import threading
import time

# Type definitions
Address = int
Value = int
InstructionPointer = int

class VMState(Enum):
    """Virtual machine execution states."""
    READY = "ready"
    RUNNING = "running"
    HALTED = "halted"
    WAITING_INPUT = "waiting_input"
    ERROR = "error"
    PAUSED = "paused"

class ParameterMode(IntEnum):
    """Parameter modes for instruction operands."""
    POSITION = 0      # Parameter is memory address
    IMMEDIATE = 1     # Parameter is literal value
    RELATIVE = 2      # Parameter is relative to base offset

@dataclass
class Instruction:
    """Decoded instruction with opcode and parameters."""
    opcode: int
    modes: List[ParameterMode]
    parameters: List[Value]
    length: int
    
    @classmethod
    def decode(cls, memory: List[Value], ip: InstructionPointer) -> 'Instruction':
        """
        Decode instruction from memory at given instruction pointer.
        
        Follows Intcode format: ABCDE where DE=opcode, C=mode1, B=mode2, A=mode3
        """
        full_opcode = memory[ip]
        opcode = full_opcode % 100
        
        # Extract parameter modes
        modes = []
        mode_value = full_opcode // 100
        for _ in range(3):  # Most instructions have at most 3 parameters
            modes.append(ParameterMode(mode_value % 10))
            mode_value //= 10
        
        # Determine instruction length based on opcode
        instruction_lengths = {
            1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2, 99: 1
        }
        length = instruction_lengths.get(opcode, 1)
        
        # Extract parameters
        parameters = []
        for i in range(1, length):
            if ip + i < len(memory):
                parameters.append(memory[ip + i])
            else:
                parameters.append(0)
        
        return cls(opcode, modes, parameters, length)

@dataclass  
class VMConfiguration:
    """Configuration for VM behavior."""
    memory_size: int = 10000
    auto_expand_memory: bool = True
    max_memory_size: int = 1000000
    enable_debugging: bool = False
    instruction_limit: Optional[int] = None
    io_timeout: float = 1.0

@dataclass
class VMStats:
    """Runtime statistics for VM execution."""
    instructions_executed: int = 0
    memory_accesses: int = 0
    io_operations: int = 0
    execution_time: float = 0.0
    memory_peak: int = 0

class IOQueue:
    """
    Thread-safe I/O queue for VM communication.
    
    Supports blocking and non-blocking operations with timeouts.
    """
    
    def __init__(self, max_size: Optional[int] = None):
        self._queue = deque()
        self._max_size = max_size
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)
    
    def put(self, value: Value, block: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Put value into queue.
        
        Args:
            value: Value to put
            block: Whether to block if queue is full
            timeout: Maximum time to wait
            
        Returns:
            True if value was added, False if queue full and not blocking
        """
        with self._not_full:
            if self._max_size is not None:
                while len(self._queue) >= self._max_size:
                    if not block:
                        return False
                    if not self._not_full.wait(timeout):
                        return False
            
            self._queue.append(value)
            self._not_empty.notify()
            return True
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Optional[Value]:
        """
        Get value from queue.
        
        Args:
            block: Whether to block if queue is empty
            timeout: Maximum time to wait
            
        Returns:
            Value from queue or None if empty and not blocking
        """
        with self._not_empty:
            while not self._queue:
                if not block:
                    return None
                if not self._not_empty.wait(timeout):
                    return None
            
            value = self._queue.popleft()
            if self._max_size is not None:
                self._not_full.notify()
            return value
    
    def empty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._queue) == 0
    
    def size(self) -> int:
        """Get current queue size."""
        with self._lock:
            return len(self._queue)
    
    def clear(self):
        """Clear all items from queue."""
        with self._lock:
            self._queue.clear()
            if self._max_size is not None:
                self._not_full.notify_all()

class VMBase(ABC):
    """
    Base class for virtual machine implementations.
    
    Provides common VM patterns extracted from Intcode and other AoC interpreters.
    """
    
    def __init__(self, 
                 program: List[Value],
                 config: Optional[VMConfiguration] = None):
        """
        Initialize VM with program and configuration.
        
        Args:
            program: Initial program/memory contents
            config: VM configuration options
        """
        self.config = config or VMConfiguration()
        
        # Initialize memory
        self.memory = program.copy()
        if len(self.memory) < self.config.memory_size:
            self.memory.extend([0] * (self.config.memory_size - len(self.memory)))
        
        # VM state
        self.ip = 0  # Instruction pointer
        self.relative_base = 0  # For relative mode addressing
        self.state = VMState.READY
        
        # I/O
        self.input_queue = IOQueue()
        self.output_queue = IOQueue()
        
        # Statistics and debugging
        self.stats = VMStats()
        self.breakpoints: Set[int] = set()
        self.debug_log: List[str] = []
        
        # Threading support
        self.thread: Optional[threading.Thread] = None
        self._stop_requested = False
    
    def reset(self, new_program: Optional[List[Value]] = None):
        """Reset VM to initial state."""
        if new_program:
            self.memory = new_program.copy()
        else:
            # Reset to original program
            self.memory = self.memory[:len(self.memory)]
        
        self.ip = 0
        self.relative_base = 0
        self.state = VMState.READY
        self.stats = VMStats()
        self.input_queue.clear()
        self.output_queue.clear()
        self._stop_requested = False
    
    def get_memory_value(self, address: Address) -> Value:
        """
        Get value from memory with automatic expansion.
        
        Args:
            address: Memory address to read
            
        Returns:
            Value at address (0 if beyond current memory)
        """
        self.stats.memory_accesses += 1
        
        if address < 0:
            raise ValueError(f"Invalid memory address: {address}")
        
        if address >= len(self.memory):
            if self.config.auto_expand_memory and address < self.config.max_memory_size:
                # Expand memory
                expansion_size = max(address - len(self.memory) + 1, 1000)
                self.memory.extend([0] * expansion_size)
                self.stats.memory_peak = max(self.stats.memory_peak, len(self.memory))
            else:
                return 0
        
        return self.memory[address]
    
    def set_memory_value(self, address: Address, value: Value):
        """
        Set value in memory with automatic expansion.
        
        Args:
            address: Memory address to write
            value: Value to write
        """
        self.stats.memory_accesses += 1
        
        if address < 0:
            raise ValueError(f"Invalid memory address: {address}")
        
        if address >= len(self.memory):
            if self.config.auto_expand_memory and address < self.config.max_memory_size:
                # Expand memory
                expansion_size = max(address - len(self.memory) + 1, 1000)
                self.memory.extend([0] * expansion_size)
                self.stats.memory_peak = max(self.stats.memory_peak, len(self.memory))
            else:
                raise ValueError(f"Memory address {address} beyond limits")
        
        self.memory[address] = value
    
    def get_parameter_value(self, param_index: int, instruction: Instruction) -> Value:
        """
        Get parameter value based on parameter mode.
        
        Args:
            param_index: Index of parameter (0-based)
            instruction: Decoded instruction
            
        Returns:
            Resolved parameter value
        """
        if param_index >= len(instruction.parameters):
            return 0
        
        param = instruction.parameters[param_index]
        mode = instruction.modes[param_index] if param_index < len(instruction.modes) else ParameterMode.POSITION
        
        if mode == ParameterMode.POSITION:
            return self.get_memory_value(param)
        elif mode == ParameterMode.IMMEDIATE:
            return param
        elif mode == ParameterMode.RELATIVE:
            return self.get_memory_value(self.relative_base + param)
        else:
            raise ValueError(f"Unknown parameter mode: {mode}")
    
    def get_parameter_address(self, param_index: int, instruction: Instruction) -> Address:
        """
        Get parameter address for write operations.
        
        Args:
            param_index: Index of parameter (0-based)
            instruction: Decoded instruction
            
        Returns:
            Memory address for parameter
        """
        if param_index >= len(instruction.parameters):
            raise ValueError(f"Parameter index {param_index} out of range")
        
        param = instruction.parameters[param_index]
        mode = instruction.modes[param_index] if param_index < len(instruction.modes) else ParameterMode.POSITION
        
        if mode == ParameterMode.POSITION:
            return param
        elif mode == ParameterMode.RELATIVE:
            return self.relative_base + param
        else:
            raise ValueError(f"Invalid parameter mode for write operation: {mode}")
    
    def input_value(self, block: bool = True) -> Optional[Value]:
        """
        Read value from input queue.
        
        Args:
            block: Whether to block waiting for input
            
        Returns:
            Input value or None if no input available and not blocking
        """
        self.stats.io_operations += 1
        return self.input_queue.get(block, self.config.io_timeout)
    
    def output_value(self, value: Value):
        """
        Write value to output queue.
        
        Args:
            value: Value to output
        """
        self.stats.io_operations += 1
        self.output_queue.put(value)
    
    def provide_input(self, *values: Value):
        """Provide input values to VM."""
        for value in values:
            self.input_queue.put(value)
    
    def get_output(self, block: bool = False) -> Optional[Value]:
        """Get output value from VM."""
        return self.output_queue.get(block)
    
    def get_all_output(self) -> List[Value]:
        """Get all available output values."""
        output = []
        while not self.output_queue.empty():
            value = self.output_queue.get(block=False)
            if value is not None:
                output.append(value)
        return output
    
    @abstractmethod
    def execute_instruction(self, instruction: Instruction) -> bool:
        """
        Execute single instruction.
        
        Args:
            instruction: Decoded instruction to execute
            
        Returns:
            True to continue execution, False to halt
        """
        pass
    
    def step(self) -> bool:
        """
        Execute single instruction step.
        
        Returns:
            True if execution should continue, False if halted
        """
        if self.state != VMState.RUNNING:
            return False
        
        # Check instruction limit
        if (self.config.instruction_limit is not None and 
            self.stats.instructions_executed >= self.config.instruction_limit):
            self.state = VMState.HALTED
            return False
        
        # Check for breakpoint
        if self.config.enable_debugging and self.ip in self.breakpoints:
            self.state = VMState.PAUSED
            return False
        
        # Decode instruction
        try:
            instruction = Instruction.decode(self.memory, self.ip)
        except (IndexError, ValueError) as e:
            self.state = VMState.ERROR
            if self.config.enable_debugging:
                self.debug_log.append(f"Error decoding instruction at {self.ip}: {e}")
            return False
        
        # Debug logging
        if self.config.enable_debugging:
            self.debug_log.append(f"IP:{self.ip} Opcode:{instruction.opcode} Params:{instruction.parameters}")
        
        # Execute instruction
        old_ip = self.ip
        try:
            continue_execution = self.execute_instruction(instruction)
            
            # Advance IP if instruction didn't modify it
            if self.ip == old_ip:
                self.ip += instruction.length
            
            self.stats.instructions_executed += 1
            return continue_execution
            
        except Exception as e:
            self.state = VMState.ERROR
            if self.config.enable_debugging:
                self.debug_log.append(f"Error executing instruction: {e}")
            return False
    
    def run(self) -> VMState:
        """
        Run VM until halted.
        
        Returns:
            Final VM state
        """
        start_time = time.time()
        self.state = VMState.RUNNING
        
        try:
            while self.state == VMState.RUNNING and not self._stop_requested:
                if not self.step():
                    break
        finally:
            self.stats.execution_time = time.time() - start_time
            if self.state == VMState.RUNNING:
                self.state = VMState.HALTED
        
        return self.state
    
    def run_async(self) -> threading.Thread:
        """
        Run VM in separate thread.
        
        Returns:
            Thread object for the running VM
        """
        if self.thread and self.thread.is_alive():
            raise RuntimeError("VM is already running in thread")
        
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        return self.thread
    
    def stop(self):
        """Stop VM execution."""
        self._stop_requested = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
    
    def add_breakpoint(self, address: Address):
        """Add breakpoint at address."""
        self.breakpoints.add(address)
    
    def remove_breakpoint(self, address: Address):
        """Remove breakpoint at address."""
        self.breakpoints.discard(address)
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get current debug information."""
        return {
            "ip": self.ip,
            "relative_base": self.relative_base,
            "state": self.state.value,
            "stats": self.stats,
            "memory_size": len(self.memory),
            "input_queue_size": self.input_queue.size(),
            "output_queue_size": self.output_queue.size(),
            "breakpoints": list(self.breakpoints)
        }

class IntcodeVM(VMBase):
    """
    Intcode Virtual Machine implementation.
    
    Complete implementation of AoC 2019 Intcode computer with all opcodes.
    Extracted from 2019 Days 2, 5, 7, 9 solutions.
    """
    
    def execute_instruction(self, instruction: Instruction) -> bool:
        """Execute Intcode instruction."""
        opcode = instruction.opcode
        
        if opcode == 1:  # Add
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            addr = self.get_parameter_address(2, instruction)
            self.set_memory_value(addr, val1 + val2)
            
        elif opcode == 2:  # Multiply
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            addr = self.get_parameter_address(2, instruction)
            self.set_memory_value(addr, val1 * val2)
            
        elif opcode == 3:  # Input
            value = self.input_value(block=True)
            if value is None:
                self.state = VMState.WAITING_INPUT
                return False
            addr = self.get_parameter_address(0, instruction)
            self.set_memory_value(addr, value)
            
        elif opcode == 4:  # Output
            value = self.get_parameter_value(0, instruction)
            self.output_value(value)
            
        elif opcode == 5:  # Jump-if-true
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            if val1 != 0:
                self.ip = val2
            
        elif opcode == 6:  # Jump-if-false
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            if val1 == 0:
                self.ip = val2
            
        elif opcode == 7:  # Less than
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            addr = self.get_parameter_address(2, instruction)
            self.set_memory_value(addr, 1 if val1 < val2 else 0)
            
        elif opcode == 8:  # Equals
            val1 = self.get_parameter_value(0, instruction)
            val2 = self.get_parameter_value(1, instruction)
            addr = self.get_parameter_address(2, instruction)
            self.set_memory_value(addr, 1 if val1 == val2 else 0)
            
        elif opcode == 9:  # Adjust relative base
            val1 = self.get_parameter_value(0, instruction)
            self.relative_base += val1
            
        elif opcode == 99:  # Halt
            self.state = VMState.HALTED
            return False
            
        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        return True

class SimpleAssemblyVM(VMBase):
    """
    Simple assembly VM for AoC problems.
    
    Based on patterns from 2020 Day 8 (Handheld Halting) and similar problems.
    """
    
    def __init__(self, program: List[str], config: Optional[VMConfiguration] = None):
        """
        Initialize with assembly program.
        
        Args:
            program: List of assembly instruction strings
            config: VM configuration
        """
        # Convert assembly to instruction tuples
        self.instructions = []
        for line in program:
            parts = line.strip().split()
            if len(parts) >= 2:
                self.instructions.append((parts[0], int(parts[1])))
            else:
                self.instructions.append((parts[0], 0))
        
        # Initialize with instruction count as memory
        super().__init__([0] * len(self.instructions), config)
        
        # Assembly VM specific state
        self.accumulator = 0
        self.executed_instructions: Set[int] = set()
    
    def execute_instruction(self, instruction: Instruction) -> bool:
        """Execute assembly instruction."""
        if self.ip >= len(self.instructions):
            self.state = VMState.HALTED
            return False
        
        # Check for infinite loop
        if self.ip in self.executed_instructions:
            self.state = VMState.ERROR
            return False
        
        self.executed_instructions.add(self.ip)
        
        opcode, operand = self.instructions[self.ip]
        
        if opcode == "acc":  # Accumulate
            self.accumulator += operand
            
        elif opcode == "jmp":  # Jump
            self.ip += operand
            return True  # Don't auto-increment IP
            
        elif opcode == "nop":  # No operation
            pass
            
        else:
            raise ValueError(f"Unknown assembly opcode: {opcode}")
        
        return True

# Utility functions for VM management

def run_intcode_program(program: List[Value], 
                       inputs: List[Value] = None,
                       config: Optional[VMConfiguration] = None) -> Tuple[List[Value], VMStats]:
    """
    Run Intcode program with inputs and return outputs.
    
    Convenience function for simple Intcode execution.
    """
    vm = IntcodeVM(program, config)
    
    if inputs:
        vm.provide_input(*inputs)
    
    final_state = vm.run()
    outputs = vm.get_all_output()
    
    return outputs, vm.stats

def create_intcode_network(programs: List[List[Value]], 
                          network_size: int) -> List[IntcodeVM]:
    """
    Create network of connected Intcode VMs.
    
    Used for problems like 2019 Day 23 (Category Six).
    """
    vms = []
    
    for i in range(network_size):
        vm = IntcodeVM(programs[i] if i < len(programs) else programs[0])
        vm.provide_input(i)  # Network address
        vms.append(vm)
    
    return vms