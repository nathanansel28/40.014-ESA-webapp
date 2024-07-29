import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import TimelinesChart from 'timelines-chart';
import './GanttChart.css';

const GanttChart = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [dataUrl, setDataUrl] = useState('http://127.0.0.1:8000/static/files/best_schedule2.csv');
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  const fetchData = async (url) => {
    try {
      const response = await axios.get(url, {
        responseType: 'blob',
      });
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        Papa.parse(text, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
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

            setChartData(formattedChartData);
            localStorage.setItem('chartData', JSON.stringify(formattedChartData));
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

  useEffect(() => {
    const storedChartData = localStorage.getItem('chartData');
    if (storedChartData) {
      setChartData(JSON.parse(storedChartData));
      setLoading(false);
    } else {
      fetchData(dataUrl);
    }
  }, [dataUrl]);

  useEffect(() => {
    if (chartData && chartRef.current) {
      if (!chartInstanceRef.current) {
        chartInstanceRef.current = TimelinesChart()(chartRef.current)
          .zScaleLabel('Percent Completion')
          .width(1000)
          .zQualitative(true);
      }
      chartInstanceRef.current.data(chartData);
    }
  }, [chartData]);

  const handleUrlChange = () => {
    localStorage.removeItem('chartData');
    setChartData(null);
    setLoading(true);
    setError(null);
    setDataUrl('http://127.0.0.1:8000/static/files/best_schedule1.csv');
  };

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
        <button onClick={handleUrlChange}>Change Dataset</button>
      </header>
      <div ref={chartRef} style={{ width: '100%', height: '500px' }}></div>
    </div>
  );
};

export default GanttChart;
