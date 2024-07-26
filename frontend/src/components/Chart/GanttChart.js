// import React, { useState, useEffect } from 'react';
// import { Gantt, ViewMode } from 'gantt-task-react';
// import axios from 'axios';
// import 'gantt-task-react/dist/index.css';
// import Papa from 'papaparse';
// import './GanttChart.css';
// import ReactTooltip from 'react-tooltip';

// function GanttChart() {
//   const [tasks, setTasks] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await axios.get('http://127.0.0.1:8000/static/files/best_schedule1.csv', {
//           responseType: 'blob',
//         });
//         const reader = new FileReader();
//         reader.onload = (e) => {
//           const text = e.target.result;
//           Papa.parse(text, {
//             header: true,
//             skipEmptyLines: true,
//             complete: (results) => {
//               const parsedTasks = results.data.map((row) => {
//                 return {
//                   id: row.Operation,
//                   operation: row.Operation,
//                   start: new Date(row.Start * 24 * 60 * 60 * 1000), // Convert days to milliseconds
//                   end: new Date(row.End * 24 * 60 * 60 * 1000), // Convert days to milliseconds
//                   type: 'task',
//                   progress: parseInt(row.PercentCompletion, 10) || 0,
//                   dependencies: [], // Initialize empty dependencies
//                   workCenter: row.WorkCenter,
//                   machine: row.Machine,
//                   machineId: row.MachineIdx, // Add MachineId to the task
//                 };
//               });

//               const validTasks = parsedTasks.filter(task => task.start && task.end && !isNaN(task.progress));

//               if (validTasks.length === 0) {
//                 setError('No valid data found in CSV file.');
//               } else {
//                 // Sort tasks by work center, machine, and machine ID
//                 validTasks.sort((a, b) => {
//                   if (a.workCenter === b.workCenter) {
//                     if (a.machine === b.machine) {
//                       return a.machineId.localeCompare(b.machineId);
//                     }
//                     return a.machine.localeCompare(b.machine);
//                   }
//                   return a.workCenter.localeCompare(b.workCenter);
//                 });

//                 setTasks(validTasks);
//                 setError(null);
//               }
//               setLoading(false);
//             },
//             error: (error) => {
//               setError('Error parsing CSV file.');
//               setLoading(false);
//             },
//           });
//         };
//         reader.readAsText(response.data);
//       } catch (error) {
//         setError('Error fetching CSV file.');
//         setLoading(false);
//       }
//     };

//     fetchData();
//   }, []);

//   // Custom column renderer
//   const renderCustomColumn = (task) => (
//     <div>{`${task.operation} ${task.workCenter} (${task.machine}, ${task.machineId})`}</div>
//   );

//   return (
//     <div className="gantt-chart-container">
//       <header>
//         <h1><strong>Gantt Chart</strong></h1>
//       </header>
//       {loading && <div>Loading...</div>}
//       {error && <div style={{ color: 'purple' }}>{error}</div>}
//       {!loading && tasks.length > 0 && (
//         <div>
//           <Gantt
//             tasks={tasks.map(task => ({
//               ...task,
//               // Custom column data
//               name: renderCustomColumn(task), // Display only work center, machine, and machine ID
//             }))}
//             viewMode={ViewMode.Day}
//             columns={[{ name: 'name', label: 'Name', width: 300 }]} // Specify the columns to display
//             TooltipContent={({ task }) => (
//               <div className='custom-tooltip'>
//                 <p><strong>Task:</strong> Operation {task.operation}</p>
//                 <p><strong>Start Date:</strong> {task.start.toLocaleDateString()}</p>
//                 <p><strong>End Date:</strong> {task.end.toLocaleDateString()}</p>
//                 <p><strong>Progress:</strong> {task.progress}%</p>
//                 <p><strong>Work Center:</strong> {task.workCenter}</p>
//                 <p><strong>Machine:</strong> {task.machine}</p>
//                 <p><strong>Machine ID:</strong> {task.machineId}</p>
//               </div>
//             )}
//           />
//           <ReactTooltip id="task-tooltip" effect="solid" />
//         </div>
//       )}
//       {!loading && tasks.length === 0 && (
//         <div>No data to display</div>
//       )}
//     </div>
//   );
// }

// export default GanttChart;

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import TimelinesChart from 'timelines-chart';
import './GanttChart.css';

const GanttChart = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/static/files/best_schedule1.csv', {
          responseType: 'blob',
        });
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result;
          console.log('CSV Content:', text); // Debugging: log the CSV content
          Papa.parse(text, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
              console.log('Parsed Data:', results.data); // Debugging: log the parsed data

              // Transform the data to the format required by timelines-chart
              const groupedData = results.data.reduce((acc, row) => {
                const group = `${row.WorkCenter} ${row.Machine} (${row.MachineIdx})`;
                if (!acc[group]) {
                  acc[group] = [];
                }
                acc[group].push({
                  label: row.Operation,
                  data: [
                    {
                      timeRange: [
                        new Date(row.Start * 24 * 60 * 60 * 1000),
                        new Date(row.End * 24 * 60 * 60 * 1000),
                      ],
                      val: row.PercentCompletion,
                    },
                  ],
                });
                return acc;
              }, {});

              const chartData = Object.keys(groupedData).map((group) => ({
                group,
                data: groupedData[group],
              }));

              console.log('Formatted Data for Chart:', chartData); // Debugging: log the formatted data

              // Render the chart
              if (chartRef.current) {
                TimelinesChart()(chartRef.current)
                  .data(chartData)
                  .zScaleLabel('Percent Completion')
                  .width(1000)
                  .zQualitative(true);
              }
              setLoading(false);
            },
            error: (error) => {
              setError('Error parsing CSV file.');
              console.error('Error parsing CSV file:', error); // Debugging: log the error
              setLoading(false);
            },
          });
        };
        reader.readAsText(response.data);
      } catch (error) {
        setError('Error fetching CSV file.');
        console.error('Error fetching CSV file:', error); // Debugging: log the error
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div style={{ color: 'purple' }}>{error}</div>;
  }

  return (
    <div className="gantt-chart-container">
      <header>
        <h1><strong>Gantt Chart</strong></h1>
      </header>
      <div ref={chartRef}></div>
    </div>
  );
};

export default GanttChart;
