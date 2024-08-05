import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
import time
import ast
import heapq
import logging
from EDD import safe_literal_eval

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        for machine in (df_machine.columns[1:]): 
            dict_machines[machine] = [[] for _ in range(int(row[machine]))]
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
# LETSA
# =====================================================================================
def LETSA_find_critical_path(operations, feasible_operations): 
    """
    Finds the critical path among the feasible operations.
    Inputs:
        - operations                    : dictionary {operation_id: Operation()}, a dictionary of all operations
        - feasible_operations           : list[operation_id],  a list of operation IDs that are currently feasible
    Output:
        - critical_path, critical_length
    """

    def dfs(operations, current_op_id, path, path_length, all_paths):
        """ 
        Performs recursive DFS on the operation network. 
        Inputs: 
            - operations                : dictionary {operation_id: Operation()}, dictionary of all operations 
            - current_op_id             : str, the ID of the node at which the DFS is performed
            - path                      : list, to keep track of current path
            - path_length               : float, to keep track of current path length
            - all_paths                 : list, to keep track of all possible paths 
        Output: 
            - None, perform in place
        """

        path.append(current_op_id)
        path_length += operations[current_op_id].processing_time
        
        if not operations[current_op_id].predecessors:
            all_paths.append((list(path), path_length))
        else:
            for pred in operations[current_op_id].predecessors:
                dfs(operations, pred, path, path_length, all_paths)
        
        path.pop()
        path_length -= operations[current_op_id].processing_time

    def find_all_paths(operations, feasible_operations):
        """
        Calls DFS on all the feasible operations. 
        Inputs: 
            - operations                : dictionary {operation_id: Operation()}, dictionary of all operations 
            - feasible_operations       : list [operation_id], list of all feasible operations to perform DFS on 
        """

        all_paths = []
        for op_id in feasible_operations:
            dfs(operations, op_id, [], 0, all_paths)
        return all_paths

    all_paths = find_all_paths(operations, feasible_operations)
    # print("     printing all paths")
    # for path in all_paths: 
        # print(path[0], path[1])
    critical_path, critical_length = max(all_paths, key=lambda x:x[1])

    return critical_path, critical_length

def LETSA_schedule_operations(operations, factory):
    """
    Solves the assembly scheduling problem (ASP) using the Longest End Time Scheduling Algorithm (LETSA).
    Inputs:
        - operations            : dictionary {operation_id: Operation()}, a dictionary of all operations.
        - factory               : list [WorkCenter()], a list of WorkCenter objects, containing machine information and availability
    Output:
        - scheduled_operations  : list [Operation()], a list of Operation objects with start and end time schedules.
    """

    scheduled_operations = []
    # [[Step 4]]
    i = 1
    while True:
        # print(f"Iteration {i}")
        # ================================================================================================================
        #  [[4.0]] Feasible operations = every operation that is 
        #                               (1) not scheduled, and 
        #                               (2) has all successors scheduled, OR does not have any successors
        # ================================================================================================================
        feasible_operations = [op_id for op_id, op in operations.items() if ((not op.scheduled) and (op.successor==None or operations[op.successor].scheduled))]
        # print(f"feasible operations: {feasible_operations}")
        if not feasible_operations:
            break # terminate if all operations have been scheduled

        # ===================================================================
        #  [[4.1 - 4.3]] Compute critical path only for feasible operations
        # ===================================================================
        critical_path, length = LETSA_find_critical_path(operations, feasible_operations)
        selected_operation_id = critical_path[0]
        selected_operation = operations[selected_operation_id]
        # print(f"critical path: {critical_path}, length: {length}")
        # print(f"selected operation: {selected_operation_id}")

        # =====================================================================
        # [[4.4]] Set completion/end time of the selected operation as
        #         (ii) the start time of the successor, if a successor exists
        #         (ii) the project deadline, otherwise 
        # =====================================================================
        if selected_operation.successor: 
            # if the operation has a successor 
            # then the tentative end time is the start time of the successor
            successor_id = selected_operation.successor
            tentative_completion_time = operations[successor_id].start_time
        else: 
            # else, the operation is an end product and its tentative completion time must be its own deadline
            tentative_completion_time = selected_operation.due_date

        # ============================================================================
        #   [[4.5]] For each identical machine incuded in the required work-center 
        # ============================================================================
        def check_availability(time, machine_usage): 
            """
            Returns True if the time interval does not overlap with any intervals in machine_usage, False otherwise.
                time            : (start, end)
                machine_usage   : list of tuples [(start1, end1), (start2, end2), ...]
            """
            start, end = time
            for interval in machine_usage:
                interval_start, interval_end = interval
                if not (end <= interval_start or start >= interval_end):
                    return False
            return True

        def find_latest_start_time(completion_time, processing_time, machine_usage):
            """
            completion_time : float
            processing_time : float
            machine_usage   : list of tuples [(start1, end1), (start2, end2), ...]
            
            Returns the latest possible start time such that the job can be completed
            before the completion time and does not overlap with any intervals in machine_usage.
            """
            latest_start_time = completion_time - processing_time

            # Sort the machine usage intervals by their start times
            machine_usage = sorted(machine_usage, key=lambda x: x[0])
            
            # Iterate over the machine usage intervals in reverse order
            for interval in reversed(machine_usage):
                interval_start, interval_end = interval
                
                # Check if there is a gap between the intervals where the job can fit
                if interval_end <= latest_start_time:
                    if check_availability((latest_start_time, latest_start_time + processing_time), machine_usage):
                        return latest_start_time
                latest_start_time = min(latest_start_time, interval_start - processing_time)
            
            # Check if the latest possible start time is valid
            if check_availability((latest_start_time, latest_start_time + processing_time), machine_usage):
                return latest_start_time
            
            return None

        current_workcenter_id = str(selected_operation.workcenter)
        # print(type(current_workcenter_id))
        # print(factory)
        current_workcenter = factory[current_workcenter_id]             # WorkCenter object 
        machine_type = str(selected_operation.machine)                  # machine id of required machine
        possible_machines = current_workcenter.machines[machine_type]   # [[], [], []]

        processing_time = selected_operation.processing_time
        tentative_start_time = tentative_completion_time - processing_time
        possible_start_times = []
        for machine_idx, machine_schedule in enumerate(possible_machines):
            # print(machine_idx, machine_schedule)
            # if not machine_schedule:  # If machine schedule is empty, then machine is immediately useable
            #     latest_available_start_time = tentative_completion_time - selected_operation.processing_time
            if check_availability((tentative_start_time, tentative_completion_time), machine_schedule) :
                start_time, end_time = tentative_start_time, tentative_completion_time
            else: 
                start_time = find_latest_start_time(tentative_completion_time, processing_time, machine_schedule) 
                end_time = start_time + processing_time
            possible_start_times.append((machine_idx, start_time, end_time))
            # print(start_time, end_time)

        # ============================================================================
        #   [[4.6]] Select a machine to schedule operation Jc  
        # ============================================================================
        selected_machine, finalized_start_time, finalized_end_time = max(possible_start_times, key=lambda x:x[1]) 
        current_workcenter.machines[machine_type][machine_idx].append((finalized_start_time, finalized_end_time))

        # ============================================================================
        #   [[4.7]] Delete operation Jc from the network
        #   [[4.8]] Add all eligible operations into the list of feasible operations     
        # ============================================================================
        selected_operation.start_time = start_time
        selected_operation.end_time = end_time
        selected_operation.scheduled = True
        selected_operation.scheduled_machine_idx = selected_machine
        scheduled_operations.append(selected_operation)

        i += 1 
        # print()
        
    return scheduled_operations

def execute_LETSA_schedule(df_bom, df_workcentre):
    try: 
        scheduled_csv_path = "static//files//scheduled.csv"
        logger.info("Starting the LETSA algorithm")
        df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(safe_literal_eval)

        operations = load_operations(df_bom)
        factory = load_factory(df_workcentre)
        LETSA_scheduled_operations = LETSA_schedule_operations(operations, factory)
        df_scheduled = format_schedule(LETSA_scheduled_operations, factory)
        logger.info(df_scheduled)
        df_scheduled.to_csv(scheduled_csv_path, index=False)
        return scheduled_csv_path
    except Exception as e:
        logger.error(f"Error in LETSA scheduling process: {str(e)}")
        raise

