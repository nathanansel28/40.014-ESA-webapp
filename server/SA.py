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

# =====================================================================================
# SA
# =====================================================================================
initial_temperature = 1000
cooling_rate = 0.85
min_temperature = 2
iterations_per_temp = 3

def SA_main(df_BOM, df_machine):
    # Create an initial schedule
    initial_schedule = SA_initial_solution(df_BOM)
    # print("Initial Schedule:", initial_schedule)

    # Test the revised evaluation function with machine availability
    initial_makespan, initial_usage = SA_calculate_makespan(initial_schedule, df_BOM, df_machine)
    # print("Initial Makespan with Machine Availability:", initial_makespan)

    # Run the simulated annealing algorithm
    best_schedule, best_makespan = simulated_annealing(df_BOM, df_machine, initial_schedule, initial_temperature, cooling_rate, min_temperature, iterations_per_temp)
    # print("Best Schedule:", best_schedule)
    # print("Best Makespan:", best_makespan)

    # Generate the Gantt chart for the best schedule
    # SA_generate_detailed_gantt_chart(best_schedule, df_BOM, best_makespan, df_machine)
    # SA_generate_beautified_gantt_chart(best_schedule, df_BOM, df_machine)

    # Export the best schedule to CSV
    df = SA_format_schedule(best_schedule, df_BOM, df_machine)
    return df, best_makespan

def SA_initial_solution(df_BOM):
    schedule = []
    remaining_operations = set(df_BOM['operation'].tolist())
    
    while remaining_operations:
        for op in list(remaining_operations):
            predecessors = df_BOM[df_BOM['operation'] == op]['predecessor_operations'].values[0]
            if all(pred in schedule for pred in predecessors):
                schedule.append(op)
                remaining_operations.remove(op)
    
    return schedule

def SA_calculate_makespan(schedule, df_BOM, df_machine):
    end_times = {}
    machine_availability = {
        workcenter: {machine: [0] * df_machine.loc[df_machine['workcenter'] == workcenter, machine].values[0]
                     for machine in df_machine.columns if machine != 'workcenter'}
        for workcenter in df_machine['workcenter']
    }
    workcenter_machine_usage = {
        workcenter: {machine: [] for machine in df_machine.columns if machine != 'workcenter'}
        for workcenter in df_machine['workcenter']
    }

    for op in schedule:
        machine = df_BOM[df_BOM['operation'] == op]['machine'].values[0]
        workcenter = df_BOM[df_BOM['operation'] == op]['workcenter'].values[0]
        processing_time = df_BOM[df_BOM['operation'] == op]['processing_time'].values[0]
        predecessors = df_BOM[df_BOM['operation'] == op]['predecessor_operations'].values[0]

        # Calculate the earliest start time considering both predecessors and machine availability
        start_time = max([end_times.get(pred, 0) for pred in predecessors], default=0)
        
        # Find the earliest available machine in the workcenter
        earliest_machine_idx = min(range(len(machine_availability[workcenter][machine])), key=lambda x: machine_availability[workcenter][machine][x])
        start_time = max(start_time, machine_availability[workcenter][machine][earliest_machine_idx])

        # Calculate the end time of the operation
        end_time = start_time + processing_time
        end_times[op] = end_time

        # Update the machine availability and usage
        machine_availability[workcenter][machine][earliest_machine_idx] = end_time
        workcenter_machine_usage[workcenter][machine].append((start_time, end_time, op, earliest_machine_idx))

    return max(end_times.values()), workcenter_machine_usage

def SA_check_precedence_constraints(schedule, df_BOM):
    # Function to check if the schedule respects precedence constraints
    operation_positions = {op: idx for idx, op in enumerate(schedule)}
    for _, row in df_BOM.iterrows():
        operation = row['operation']
        predecessors = row['predecessor_operations']
        for pred in predecessors:
            if operation_positions[pred] >= operation_positions[operation]:
                return False
    return True

def SA_generate_neighbor(schedule, df_BOM, max_retries=100):
    # Generate a neighbor solution by swapping two operations
    new_schedule = schedule[:]
    retries = 0
    while retries < max_retries:
        idx1, idx2 = random.sample(range(len(schedule)), 2)
        new_schedule[idx1], new_schedule[idx2] = new_schedule[idx2], new_schedule[idx1]
        if SA_check_precedence_constraints(new_schedule, df_BOM):
            return new_schedule
        else:
            new_schedule = schedule[:]
        retries += 1
    
    # If no valid neighbor found, return the original schedule
    # print("Warning: Could not find a valid neighbor within retry limit.")
    return schedule

def SA_accept_solution(current_makespan, new_makespan, temperature):
    if new_makespan < current_makespan:
        return True
    else:
        prob = np.exp((current_makespan - new_makespan) / temperature)
        return random.random() < prob

def simulated_annealing(df_BOM, df_machine, initial_schedule, initial_temperature, cooling_rate, min_temperature, iterations_per_temp):
    current_schedule = initial_schedule
    current_makespan, _ = SA_calculate_makespan(current_schedule, df_BOM, df_machine)
    best_schedule = current_schedule
    best_makespan = current_makespan
    temperature = initial_temperature
    # print(temperature)
    while temperature > min_temperature:
        for _ in range(iterations_per_temp):
            new_schedule = SA_generate_neighbor(current_schedule, df_BOM)
            new_makespan, _ = SA_calculate_makespan(new_schedule, df_BOM, df_machine)
            
            if SA_check_precedence_constraints(new_schedule, df_BOM) and SA_accept_solution(current_makespan, new_makespan, temperature):
                current_schedule = new_schedule
                current_makespan = new_makespan
                
                if new_makespan < best_makespan:
                    best_schedule = new_schedule
                    best_makespan = new_makespan
        # print(temperature)
        temperature *= cooling_rate
    return best_schedule, best_makespan

def SA_format_schedule(schedule, df_BOM, df_machine):
    max_makespan, workcenter_machine_usage = SA_calculate_makespan(schedule, df_BOM, df_machine)
    export_data = []

    # Gather utilized machines information
    used_machines = set()
    for wc in workcenter_machine_usage:
        for machine in workcenter_machine_usage[wc]:
            for (start, end, op, machine_idx) in workcenter_machine_usage[wc][machine]:
                used_machines.add((wc, machine, machine_idx))
                export_data.append({
                    'Operation': op,
                    'Start': start,
                    'End': end,
                    'Workcenter': wc,
                    'Machine': machine,
                    'MachineIdx': machine_idx + 1
                })



    # Add unused machines information
    for wc in df_machine['workcenter']:
        for machine in df_machine.columns:
            if machine != 'workcenter':
                num_machines = df_machine.loc[df_machine['workcenter'] == wc, machine].values[0]
                for idx in range(num_machines):
                    if (wc, machine, idx) not in used_machines:
                        export_data.append({
                            'Operation': None,
                            'Start': None,
                            'End': None,
                            'Workcenter': wc,
                            'Machine': machine,
                            'MachineIdx': idx + 1
                        })
    
    return pd.DataFrame(export_data)

