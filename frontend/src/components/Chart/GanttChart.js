import React, { useState, useEffect } from 'react';
import { Gantt, ViewMode } from 'gantt-task-react';
import axios from 'axios';
import 'gantt-task-react/dist/index.css';
import Papa from 'papaparse';
import './GanttChart.css';
import ReactTooltip from 'react-tooltip';

function GanttChart() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/static/files/best_schedule.csv', {
          responseType: 'blob',
        });
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result;
          Papa.parse(text, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
              const parsedTasks = results.data.map((row) => {
                return {
                  id: row.Operation,
                  operation: row.Operation,
                  start: new Date(row.Start * 24 * 60 * 60 * 1000), // Convert days to milliseconds
                  end: new Date(row.End * 24 * 60 * 60 * 1000), // Convert days to milliseconds
                  type: 'task',
                  progress: parseInt(row.PercentCompletion, 10) || 0,
                  dependencies: [], // Assuming no dependencies in the dataset
                  workCenter: row.WorkCenter,
                  machine: row.Machine,
                  machineId: row.MachineIdx // Add MachineId to the task
                };
              });

              const validTasks = parsedTasks.filter(task => task.start && task.end && !isNaN(task.progress));

              if (validTasks.length === 0) {
                setError('No valid data found in CSV file.');
              } else {
                // Sort tasks by work center, machine, and machine ID
                validTasks.sort((a, b) => {
                  if (a.workCenter === b.workCenter) {
                    if (a.machine === b.machine) {
                      return a.machineId.localeCompare(b.machineId);
                    }
                    return a.machine.localeCompare(b.machine);
                  }
                  return a.workCenter.localeCompare(b.workCenter);
                });

                setTasks(validTasks);
                setError(null);
              }
              setLoading(false);
            },
            error: (error) => {
              setError('Error parsing CSV file.');
              setLoading(false);
            },
          });
        };
        reader.readAsText(response.data);
      } catch (error) {
        setError('Error fetching CSV file.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const taskStyles = {
    bar: { fill: '#8A9B0F', stroke: '#8A9B0F' },
    progress: { fill: '#4D774E' },
  };

  return (
    <div className="gantt-chart-container">
      <header>
        <h1>Gantt Chart</h1>
      </header>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'purple' }}>{error}</div>}
      {!loading && tasks.length > 0 && (
        <div>
          <Gantt
            tasks={tasks.map(task => ({
              ...task,
              styles: taskStyles,
              name: `${task.operation} ${task.workCenter} (${task.machine}, ${task.machineId})`, // Display only work center, machine, and machine ID
            }))}
            viewMode={ViewMode.Day}
            TooltipContent={({ task }) => (
              <div className='custom-tooltip'>
                <p><strong>Task:</strong> Operation {task.operation}</p>
                <p><strong>Start Date:</strong> {task.start.toLocaleDateString()}</p>
                <p><strong>End Date:</strong> {task.end.toLocaleDateString()}</p>
                <p><strong>Progress:</strong> {task.progress}%</p>
                <p><strong>Work Center:</strong> {task.workCenter}</p>
                <p><strong>Machine:</strong> {task.machine}</p>
                <p><strong>Machine ID:</strong> {task.machineId}</p>
              </div>
            )}
          />
          <ReactTooltip id="task-tooltip" effect="solid" />
        </div>
      )}
      {!loading && tasks.length === 0 && (
        <div>No data to display</div>
      )}
    </div>
  );
}

export default GanttChart;
