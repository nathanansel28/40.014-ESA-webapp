import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import TimelinesChart from 'timelines-chart';
import './GanttChart.css';

const GanttChart = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching data...");
        const response = await axios.get('http://127.0.0.1:8000/static/files/best_schedule1.csv', {
          responseType: 'blob',
        });
        console.log("Data fetched successfully");
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result;
          console.log('CSV Content:', text); // Debugging: log the CSV content
          Papa.parse(text, {
            header: true,
            skipEmptyLines: false,
            complete: (results) => {
              console.log('Parsed Data:', results.data); // Debugging: log the parsed data

              // Transform the data to the format required by timelines-chart
              const groupedData = results.data.reduce((acc, row) => {
                const group = `${row.WorkCenter} ${row.Machine} (${row.MachineIdx})`;
                if (!acc[group]) {
                  acc[group] = [];
                }
                if (row.Start && row.End) {
                  acc[group].push({
                    label: row.Operation || 'N/A',
                    data: [
                      {
                        timeRange: [
                          new Date(row.Start * 24 * 60 * 60 * 1000),
                          new Date(row.End * 24 * 60 * 60 * 1000),
                        ],
                        val: row.PercentCompletion || 0,
                      },
                    ],
                  });
                } else {
                  // Add an empty task for rows with missing Start or End
                  acc[group].push({
                    label: row.Operation || 'N/A',
                    data: [],
                  });
                }
                return acc;
              }, {});

              const chartData = Object.keys(groupedData).map((group) => ({
                group,
                data: groupedData[group],
              }));

              console.log('Formatted Data for Chart:', chartData); // Debugging: log the formatted data

              // Render the chart
              if (chartRef.current) {
                // Clear any existing chart
                chartRef.current.innerHTML = '';
                console.log('Initializing Chart'); // Debugging: log chart initialization

                // Create and store chart instance
                chartInstanceRef.current = TimelinesChart()(chartRef.current)
                  .data(chartData)
                  .zScaleLabel('Percent Completion')
                  .width(1000)
                  .zQualitative(true);

                console.log('Chart initialized successfully'); // Debugging: log the chart initialization
              } else {
                console.error('chartRef.current is null'); // Debugging: log if chartRef is null
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
      <div ref={chartRef} ></div> {/* Ensure the div has dimensions */}
    </div>
  );
};

export default GanttChart;
