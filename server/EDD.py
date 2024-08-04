import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.dates as mdates
from datetime import datetime
import os
import time
import ast
import heapq
import matplotlib.patches as mpatches
import matplotlib.patches as mpatches
import matplotlib

import pandas as pd

import globals  # Import the globals module

def convert_to_dataframe(csv_data):
    """
    Convert parsed CSV data to a pandas DataFrame.

    :param csv_data: List of dictionaries containing CSV data.
    :return: pandas DataFrame
    """
    return pd.DataFrame(csv_data)

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
    
def safe_literal_eval(val):
    try:
        if pd.notnull(val):
            # Evaluate the string to a Python object
            result = ast.literal_eval(val)
            # Ensure the result is a list and contains only strings
            if isinstance(result, list) and all(isinstance(item, str) for item in result):
                return result
            else:
                # If not, handle it as an invalid case
                return []
        else:
            return []
    except (ValueError, SyntaxError):
        # Handle the case where literal_eval fails
        return []


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
# EDD
# =====================================================================================
def EDD_find_earliest_start_time(machine_usage, minimum_start_time, processing_time, print_button=False):
    """
    Finds the earliest start time on the given machine that avoids overlapping with existing jobs.
    Inputs: 
        - machine_usage         : [(3,4), (5,6)] 
        - desired_start_time    : start time must not be earlier than this 
        - processing_time       : operation processing time 
    """
   
    machine_usage.sort()
    start_time = None

    if len(machine_usage) == 0:
        start_time = minimum_start_time 
        # if print_button:
        #     print("A")
        return start_time

    for i in range(len(machine_usage)-1): 
        # if print_button: 
        #     print("B")
        tentative_start = machine_usage[i][1]
        tentative_end = machine_usage[i+1][0]
        if (tentative_end - tentative_start >= processing_time) and (tentative_start >= minimum_start_time):
            start_time = tentative_start 
            return start_time 
    
    if start_time is None: 
        # if print_button: 
        #     print("C")
        #     print(machine_usage)
        start_time = machine_usage[len(machine_usage)-1][1]
        if start_time < minimum_start_time:
            start_time = minimum_start_time
        return start_time

def EDD_schedule_operations(operations, factory):
    def check_availability(start_time, processing_time, machine_usage):
        """
        Returns True if the time interval does not overlap with any intervals in machine_usage, False otherwise.
        """
        end_time = start_time + processing_time
        for interval in machine_usage:
            if len(interval) != 2:
                raise ValueError("Machine usage interval does not contain exactly 2 values")
            interval_start, interval_end = interval
            if not (end_time <= interval_start or start_time >= interval_end):
                return False
        return True

    # =====================
    #   Initialize Queue 
    # =====================
    scheduled_operations, Q = [], []
    unscheduled_dependencies = {op_id: len(op.predecessors) for op_id, op in operations.items()}
    # print(f"Unscheduled dependencies: {unscheduled_dependencies}")

    for op_id, count in unscheduled_dependencies.items():
        if count == 0:
            heapq.heappush(Q, (operations[op_id].due_date if operations[op_id].due_date is not None else float('inf'), 
                               operations[op_id].processing_time, op_id))

    i = 0
    while True:
        # ==================================
        #    POP OUT OPERATION USING EDD
        # ==================================
        i += 1
        if not Q: 
            break
        print_list = [item[2] for item in Q]
        print_list.sort()
        # print(f"Iteration {i}: {print_list}")
        _, _, operation_id = heapq.heappop(Q)
        operation = operations[operation_id]
        # print(f"{operation_id}")
        if operation.scheduled:
            continue

        # ==================================
        #        COMPUTE START TIME
        # ==================================
        # Compute (tentative) start time based on dependencies
        if operation.predecessors:
            predecessor_max_end_time = max(
                (operations[comp_id].end_time if operations[comp_id].end_time is not None else -float('inf'))
                for comp_id in operation.predecessors)
            minimum_start_time = predecessor_max_end_time
            # if operation.id == "J.6":
            #     print(operation.predecessors)
            #     print(predecessor_max_end_time)
        else:
            minimum_start_time = 0

        # Find the best machine and start time
        workcenter = factory[str(operation.workcenter)]
        machine_type = operation.machine
        best_start_time = float('inf')
        selected_machine = None

        # ==================================
        #           SELECT MACHINE
        # ==================================
        # Iterate through all functionally identical machine in the current workcenter
        # Find the best start time, which is the earliest possible start time
        list_machine_schedules = workcenter.machines[machine_type]
        if operation.id == "J.6":
            printer = True
        else:
            printer = False
        for machine_idx, machine_usage in enumerate(list_machine_schedules): 
            start_time = EDD_find_earliest_start_time(machine_usage, minimum_start_time, operation.processing_time, print_button=printer)
            if check_availability(start_time, operation.processing_time, machine_usage):
                if start_time < best_start_time:
                    # if operation.id == "J.6": 
                        # print(start_time)
                    best_start_time = start_time
                    selected_machine = machine_usage
                    selected_machine_idx = machine_idx 

        if selected_machine is None:
            # No available machine found; push operation back to recheck later
            heapq.heappush(Q, (operation.due_date if operation.due_date is not None else float('inf'), operation.processing_time, operation_id))
            # print(f"Operation {operation.id} not scheduled yet, re-adding to the queue")
            continue

        # ==================================
        #      SCHEDULE THE OPERATIONS
        # ==================================
        operation.start_time = best_start_time
        operation.end_time = operation.start_time + operation.processing_time
        operation.scheduled = True
        operation.scheduled_machine_idx = selected_machine_idx
        scheduled_operations.append(operation)
        # print(F"Selected {operation.id}")
        # print(f"Scheduled operations: {[op.id for op in scheduled_operations]}")
        # print("")
        workcenter.machines[machine_type][selected_machine_idx].append((operation.start_time, operation.end_time))

        # ==================================
        #           UPDATE QUEUE
        # ==================================
        # unscheduled_dependencies = {op_id: len(op.predecessors) for op_id, op in operations.items()}

        for op_id, op in operations.items(): 
            for comp_id in op.predecessors: 
                # print(f"my operation id: {operation.id}")
                # print(comp_id)
                if operation.id == comp_id: 
                    # print("yes")
                    # if the id of the previously scheduled operation is the same as the id of the iterated Op
                    # then we should reduce the unscheduled dependencies count by 1
                    unscheduled_dependencies[op_id] -= 1
                    # print(unscheduled_dependencies[op_id])
        # print(f"Unscheduled dependencies: {unscheduled_dependencies}")

        for op_id, count in unscheduled_dependencies.items():
            scheduled_operations_id = [scheduled_op.id for scheduled_op in scheduled_operations]
            list_Q = [queued_op[2] for queued_op in Q]
            if (count == 0) and (op_id not in scheduled_operations_id) and (op_id not in list_Q):
                heapq.heappush(Q, (operations[op_id].due_date if operations[op_id].due_date is not None else float('inf'), 
                                operations[op_id].processing_time, op_id))
                # print(f"Pushed {op_id} into Q")



        # for op_id, op in operations.items():
        #     if not op.scheduled and op_id in unscheduled_dependencies:
        #         # if the operation has not been scheduled, and is an unscheduled dependency
        #         # for each of the predecessors of this operation
        #         for comp_id in op.predecessors:
        #             if operations[comp_id].scheduled:
        #                 unscheduled_dependencies[op_id] -= 1
        #         if unscheduled_dependencies[op_id] == 0:
        #             heapq.heappush(Q, (op.due_date if op.due_date is not None else float('inf'), op.processing_time, op_id))
        #             # print(f"Operation {op_id} with no remaining dependencies added to the queue")

        # print("")
    return scheduled_operations

print(globals.df_bom["predecessor_operations"].dtype)
globals.df_bom['predecessor_operations'] = globals.df_bom['predecessor_operations'].apply(safe_literal_eval)
# df_bom['predecessor_operations'] = df_bom['predecessor_operations'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
print(globals.df_bom)
# operations = load_operations(df_bom)
# factory = load_factory(df_workcentre)
# EDD_scheduled_operations = EDD_schedule_operations(operations, factory)
# df_scheduled = format_schedule(EDD_scheduled_operations, factory)
# df_scheduled.to_csv("static\\files\\scheduled.csv")
