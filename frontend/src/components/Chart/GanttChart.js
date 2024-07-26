import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import TimelinesChart from 'timelines-chart';
import './GanttChart.css';

const GanttChart = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartData, setChartData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/static/files/best_schedule3.csv', {
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

              const formattedChartData = Object.keys(groupedData).map((group) => ({
                group,
                data: groupedData[group],
              }));

              console.log('Formatted Data for Chart:', formattedChartData); // Debugging: log the formatted data
              setChartData(formattedChartData);
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

  useEffect(() => {
    if (chartData && chartRef.current) {
      // Clear any existing chart
      chartRef.current.innerHTML = '';
      console.log('Initializing Chart'); // Debugging: log chart initialization

      // Create and store chart instance
      TimelinesChart()(chartRef.current)
        .data(chartData)
        .zScaleLabel('Percent Completion')
        .width(1000)
        .zQualitative(true);

      console.log('Chart initialized successfully'); // Debugging: log the chart initialization
    }
  }, [chartData]);

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
      <div ref={chartRef}></div> {/* Ensure the div has dimensions */}
    </div>
  );
};

export default GanttChart;
