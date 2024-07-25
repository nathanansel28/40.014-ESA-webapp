// GanttChart.js
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
    console.log("Component mounted");

    const parseDate = (dateString) => {
      if (!dateString) return null;
      const [year, month, day] = dateString.split('-');
      return new Date(year, month - 1, day); // month is 0-indexed in JavaScript Date
    };

    const fetchData = async () => {
      const controller = new AbortController();
      const signal = controller.signal;

      try {
        console.log("Fetching CSV file...");

        // Using axios to fetch the CSV file as a blob
        const axiosResponse = await axios.get(`http://127.0.0.1:8000/static/files/5machines_0.15p_0.8D.csv`, {
            responseType: 'blob',
        });

        // Reading the response text from axios
        const csvText = await axiosResponse.data.text();
        console.log("CSV file fetched successfully:", csvText);

        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            console.log("CSV file parsed successfully:", results.data);
            const parsedTasks = results.data.map((row) => {
              console.log("Parsing row:", row);
              return {
                id: row.operationID,
                name: `Operation ${row.operation}`,
                start: parseDate(row.startDate),
                end: parseDate(row.endDate),
                type: 'task',
                progress: parseInt(row.percentComplete, 10) || 0,
                dependencies: row.predecessors ? row.predecessors.split(',') : [],
                workCenter: row.workCenter, // Add work center information here
                machine: row.machine, // Add machine information here
              };
            });

            const validTasks = parsedTasks.filter(task => task.start && task.end && !isNaN(task.progress));
            console.log("Valid tasks:", validTasks);

            if (validTasks.length === 0) {
              setError('No valid data found in CSV file.');
            } else {
              setTasks(validTasks);
              setError(null);
            }
            setLoading(false);
          },
          error: (error) => {
            console.error('Error parsing CSV:', error);
            setError('Error parsing CSV file.');
            setLoading(false);
          },
        });
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Error fetching CSV file:', error);
          setError('Error fetching CSV file.');
          setLoading(false);
        }
      }

      return () => {
        console.log("Component unmounted, aborting fetch");
        controller.abort(); // Cleanup: abort fetch request if component unmounts
      };
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
              name: `${task.name} (${task.machine})`,
            }))}
            viewMode={ViewMode.Month}
            TooltipContent={({ task }) => (
              <div>
                <p><strong>Task:</strong> {task.name}</p>
                <p><strong>Start Date:</strong> {task.start.toLocaleDateString()}</p>
                <p><strong>End Date:</strong> {task.end.toLocaleDateString()}</p>
                <p><strong>Progress:</strong> {task.progress}%</p>
                <p><strong>Work Center:</strong> {task.workCenter}</p>
                <p><strong>Machine:</strong> {task.machine}</p>
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
