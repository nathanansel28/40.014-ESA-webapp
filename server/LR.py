import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
import time
import ast
import heapq

# =====================================================================================
# CLASS DEFINITIONS
# =====================================================================================
class WorkCenter:
    def __init__(self, id, dict_machines={}):
        self.id = str(id)
        self.machines = dict_machines
        # dict_machines = {'M1': [ [], [], [] ] }

class Operation:
    def __init__(self, id, processing_time, workcenter, machine, due_date=None, successors=None, predecessors=None):
        self.id = str(id)
        self.successor = str(successors) if successors else None
        self.predecessors = predecessors if predecessors else []
        self.workcenter = str(workcenter)
        self.machine = str(machine)
        self.scheduled_machine_idx = None
        self.processing_time = processing_time
        self.start_time = None
        self.end_time = None
        self.due_date = due_date
        # self.due_date = None if due_date != due_date else due_date
        self.scheduled = False

    # Comparison methods
    def __lt__(self, other):
        return (self.due_date if self.due_date is not None else float('inf')) < (other.due_date if other.due_date is not None else float('inf'))

    def __le__(self, other):
        return (self.due_date if self.due_date is not None else float('inf')) <= (other.due_date if other.due_date is not None else float('inf'))

    def __eq__(self, other):
        return (self.due_date if self.due_date is not None else float('inf')) == (other.due_date if other.due_date is not None else float('inf'))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

def load_operations(df, LR=False):
    """
    Loads the operation information from the df_BOM
    Initializes an Operation object for each of the operation and stores it in the operations dictionary
    Inputs: 
        - df            : a dataframe consisting the BOM information  
        - filename      : 
    Outputs:
        - operations    : 
    """

    operations = {}

    for index, row in df.iterrows():
        op = Operation(
            id=str(row['operation']),
            processing_time=row['processing_time'],
            workcenter=row['workcenter'],
            machine=row['machine'],
            due_date=row['due_date'],
            predecessors=row['predecessor_operations']
        )
        operations[op.id] = op

    if LR: 
        for op_id, op in operations.items():
            if op.due_date == None: 
                op.due_date = 0

    for index, row in df.iterrows():
        current_op_id = row['operation']
        predecessor_ops = row['predecessor_operations']
        for predecessor in predecessor_ops:
            operations[predecessor].successor = current_op_id
    
    return operations

def load_factory(df_machine):
    factory = {}
    for idx, row in df_machine.iterrows():
        workcenter = row['workcenter']
        dict_machines = {}
        for machine in (df_machine.columns[2:]): 
            dict_machines[machine] = [[] for _ in range(row[machine])]
        # factory.append(WorkCenter(workcenter, dict_machines=dict_machines))
        factory[workcenter] = WorkCenter(workcenter, dict_machines=dict_machines)
    return factory 

def calculate_makespan(factory, scheduled_operations=None):
    if scheduled_operations: 
        list_intervals = []
        for operation in scheduled_operations: 
            list_intervals.append(operation.start_time)
            list_intervals.append(operation.start_time + operation.processing_time)
        _max = max(list_intervals)
        _min = min(list_intervals)
        return _max - _min

    list_schedules = []
    for workcenter_key in factory:
        for _, machine_schedule in factory[workcenter_key].machines.items():
            flattened_schedule = [item for sublist in machine_schedule for item in sublist]
            list_schedules += flattened_schedule

    _max = max(list_schedules, key=lambda x: x[1])[1]
    _min = min(list_schedules, key=lambda x: x[0])[0]

    return _max - _min

def format_schedule(scheduled_operations, factory):
    df_schedule = pd.DataFrame()
    for i, operation in enumerate(scheduled_operations): 
        df_schedule.at[i, "WorkCenter"] = operation.workcenter
        df_schedule.at[i, "Machine"] = operation.machine
        df_schedule.at[i, "MachineIdx"] = operation.scheduled_machine_idx+1
        df_schedule.at[i, "Operation"] = operation.id
        df_schedule.at[i, "Start"] = operation.start_time
        df_schedule.at[i, "End"] = operation.start_time + operation.processing_time
    df_schedule['PercentCompletion'] = 100  

    for workcenter_key in factory: 
        workcenter = factory[workcenter_key]
        for machine_type, machine_schedules in workcenter.machines.items():
            for machine_idx, machine_schedule in enumerate(machine_schedules): 
                if len(machine_schedule) == 0:
                    new_row = {
                        "WorkCenter": workcenter.id,
                        "Machine": machine_type,
                        "MachineIdx": machine_idx,
                        "Operation": None,
                        "Start": None,
                        "End": None,
                        "PercentCompletion": None
                    }
                    new_row_df = pd.DataFrame([new_row])
                    df_schedule = pd.concat([df_schedule, new_row_df], ignore_index=True)

    return df_schedule

# =====================================================================================
# LR
# =====================================================================================
def LR_solve_spm(V_Y, makespan_values):
    SPM_value = 0
    for V, Z in zip(V_Y, makespan_values):
        if V > 1:
            SPM_value += V * Z
        elif V == 1:
            SPM_value += Z
        else:
            SPM_value += 0
    return SPM_value

def LR_solve_spw(operations, workcenter, V_Y, U_ij):
    operations.sort(key=lambda op: (op.processing_time / (op.due_date if op.due_date else float('inf')), -op.processing_time))
    
    # Initialize completion times for each machine in the workcenter
    C = {machine: 0 for machine in workcenter.machines}
    
    Q = []
    # print(operations)
    for op in operations:
        # print(f"op.due_date: {op.due_date}")
        # print(f"op: {op}")
        heapq.heappush(Q, (op.due_date, op))
    
    L_Y = 0
    makespan = 0
    
    while Q:
        _, op = heapq.heappop(Q)
        available_machine = min(C, key=C.get)
        op.start_time = C[available_machine]
        op.end_time = op.start_time + op.processing_time
        C[available_machine] = op.end_time
        makespan = max(makespan, op.end_time)
        L_Y += V_Y * makespan
        if op.successor:
            succ = next((o for o in operations if o.id == op.successor), None)
            if succ and succ.end_time is not None and op.end_time is not None:
                L_Y += U_ij.get((op.id, succ.id), 0) * succ.end_time - U_ij.get((op.id, succ.id), 0) * op.end_time
    
    return L_Y, operations

def LR_subgradient_search(factory, operations, lambda_ij = {}, max_iterations=100, s=0.1):
    lambda_ij = {}
    for operation_id in operations: 
        predecessors = operations[operation_id].predecessors 
        for predecessor_id in predecessors:
            lambda_ij[(predecessor_id, operation_id)] = 1
    delta_Y = {wc.id: 1 for wc in factory.values()}  # Initialize delta_Y with correct keys from workcenters
    
    U_ij = {k: v for k, v in lambda_ij.items()}
    V_Y = {Y: delta_Y[Y] for Y in delta_Y}
    # if filename == "50_2_0.5_0.15_bottleneck.csv":
    #     print(f"U_ij: {U_ij}")
        # print(f"V_Y: {V_Y}")

    for k in range(1, max_iterations + 1):
        if sum(V_Y.values()) > 1:
            total = sum(V_Y.values())
            for Y in V_Y:
                V_Y[Y] = V_Y[Y] / total

        L_Y_total = 0
        makespan_values = []
        for wc in factory.values():
            L_Y, scheduled_operations = LR_solve_spw([op for op in operations.values() if op.workcenter == wc.id], wc, V_Y[wc.id], U_ij)
            L_Y_total += L_Y
            if len(scheduled_operations) == 0: 
                makespan_values.append(0)
            else: 
                makespan_values.append(max(op.end_time for op in scheduled_operations if op.end_time is not None))

        pseudo_lower_bound = L_Y_total
        
        norm_F_S = sum((next(op.end_time for op in operations.values() if op.id == j) - next(op.start_time for op in operations.values() if op.id == i))**2 for i, j in lambda_ij.keys())
        norm_Z_ZY = sum((max(makespan_values) - ZY)**2 for ZY in makespan_values)
        
        for (i, j) in U_ij.keys():
            S_i = next(op.start_time for op in operations.values() if op.id == i)
            F_j = next(op.end_time for op in operations.values() if op.id == j)
            U_ij[(i, j)] += s * k * (F_j - S_i) / (norm_F_S + norm_Z_ZY)**0.5
            if U_ij[(i, j)] <= 0:
                U_ij[(i, j)] = 0
        

        for Y in V_Y.keys():
            # if filename == "50_2_0.5_0.15_bottleneck.csv":
            #     print(f"norm_F_S, norm_Z_ZY: {norm_F_S, norm_Z_ZY}")

            Z = max(makespan_values)
            ZY = makespan_values[list(V_Y.keys()).index(Y)]
            V_Y[Y] += s * k * (Z - ZY) / (norm_F_S + norm_Z_ZY)**0.5
            
            
        if k >= 100:
            break

    return U_ij, V_Y

def LR_calculate_lower_bounds(factory, operations):
    lower_bounds = {}
    for wc in factory.values():
        op_list = [op for op in operations.values() if op.workcenter == wc.id]
        if not op_list:
            continue
        
        f_Y = len(wc.machines[list(wc.machines.keys())[0]])  # Number of machines in the work center
        
        # Calculate LB0_Y
        LB0_Y = max((op.due_date if op.due_date is not None else 0) + op.processing_time for op in op_list)
        
        # Calculate LB1_Y
        min_due_date = min((op.due_date if op.due_date is not None else 0) for op in op_list)
        total_processing_time = sum(op.processing_time for op in op_list)
        LB1_Y = min_due_date + (1 / f_Y) * total_processing_time
        
        # Calculate LB2_Y
        sorted_due_dates = sorted((op.due_date if op.due_date is not None else 0) for op in op_list)
        sum_r = sum(sorted_due_dates[:f_Y]) if len(sorted_due_dates) >= f_Y else sum(sorted_due_dates)
        LB2_Y = (1 / f_Y) * (sum_r + total_processing_time)
        
        lower_bounds[wc.id] = max(LB0_Y, LB1_Y, LB2_Y)
    
    overall_lower_bound = min(lower_bounds.values()) if lower_bounds else float('inf')
    return overall_lower_bound

def LR_schedule_operations(operations, factory):
    U_ij, V_Y = LR_subgradient_search(factory, operations, max_iterations=100, s=0.1)
    for wc in factory.values():
        LR_solve_spw([op for op in operations.values() if op.workcenter == wc.id], wc, V_Y[wc.id], U_ij)
    lower_bound = LR_calculate_lower_bounds(factory, operations)

    machine_completion_times = {wc.id: {machine: [0] * len(wc.machines[machine]) for machine in wc.machines} for wc in factory.values()}
    operations_sorted = sorted(operations.values(), key=lambda op: (op.processing_time / (op.due_date if op.due_date else float('inf')), -op.processing_time))
    
    for op in operations_sorted:
        # Determine the earliest start time based on predecessor completion times
        if op.predecessors:
            predecessor_end_times = [operations[pred_id].end_time for pred_id in op.predecessors]
            earliest_start_time = max(predecessor_end_times)
        else:
            earliest_start_time = 0
        
        # Determine the machine's next available time
        machine_times = machine_completion_times[op.workcenter][op.machine]
        machine_next_available_time = min(machine_times)
        machine_index = machine_times.index(machine_next_available_time)

        # Schedule the operation to start after the latest of the predecessor end times or machine availability
        op.start_time = max(earliest_start_time, machine_next_available_time)
        op.end_time = op.start_time + op.processing_time
        op.scheduled_machine_idx = machine_index

        # Update the machine's completion time
        machine_completion_times[op.workcenter][op.machine][machine_index] = op.end_time

    scheduled_operations = []
    for key in operations: 
        scheduled_operations.append(operations[key])
    
    return (scheduled_operations, lower_bound)


def execute_LR_schedule(df_bom, df_workcentre): 
    operations = load_operations(df_bom, LR=True)
    factory = load_factory(df_workcentre)
    LR_scheduled_operations, LR_lower_bound = LR_schedule_operations(operations, factory)
    df_scheduled = format_schedule(LR_scheduled_operations)
    scheduled_csv_path = "static//files//scheduled.csv"
    df_scheduled.to_csv(scheduled_csv_path, index=False)
    return scheduled_csv_path