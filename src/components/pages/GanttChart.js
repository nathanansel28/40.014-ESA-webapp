import React, { useState, useEffect } from 'react';
import { Gantt, ViewMode } from 'gantt-task-react';
import 'gantt-task-react/dist/index.css';
import Papa from 'papaparse';

function GanttChart() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const parseDate = (dateString) => {
      if (!dateString) return null;
      const [year, month, day] = dateString.split('-');
      return new Date(year, month - 1, day); // month is 0-indexed in JavaScript Date
    };

    const fetchData = async () => {
      try {
        const response = await fetch('/5machines_0.15p_0.8D.csv'); // Adjust the path as needed
        if (!response.ok) {
          throw new Error(`Failed to fetch CSV file: ${response.statusText}`);
        }
        const csvText = await response.text();

        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const parsedTasks = results.data.map((row) => {
              return {
                id: row.operationID,
                name: `Operation ${row.operation}`,
                start: parseDate(row.startDate),
                end: parseDate(row.endDate),
                type: 'task',
                progress: parseInt(row.percentComplete, 10) || 0,
                dependencies: row.predecessors ? row.predecessors.split(',') : [],
              };
            });

            const validTasks = parsedTasks.filter(task => task.start && task.end && !isNaN(task.progress));

            if (validTasks.length === 0) {
              setError('No valid data found in CSV file.');
            } else {
              setTasks(validTasks);
              setError(null);
            }
            setLoading(false);
          },
          error: (error) => {
            console.error('Error parsing CSV: ', error);
            setError('Error parsing CSV file.');
            setLoading(false);
          },
        });
      } catch (error) {
        console.error('Error fetching CSV file:', error);
        setError('Error fetching CSV file.');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Gantt Chart</h1>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {!loading && tasks.length > 0 && (
        <Gantt
          tasks={tasks}
          viewMode={ViewMode.Month}
        />
      )}
      {!loading && tasks.length === 0 && (
        <div>No data to display</div>
      )}
    </div>
  );
}

export default GanttChart;
