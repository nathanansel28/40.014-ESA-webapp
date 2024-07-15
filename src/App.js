import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Services from './components/pages/Services';
import Products from './components/pages/Products';
import AboutUs from './components/pages/AboutUs';
import Home from './components/pages/Home';
// import {Chart} from 'react-google-charts';


function App() {
  //   const data = [
  //       [
  //           { type: 'string', label: 'Task ID' },
  //           { type: 'string', label: 'Task Name' },
  //           { type: 'string', label: 'Resource' },
  //           { type: 'date', label: 'Start Date' },
  //           { type: 'date', label: 'End Date' },
  //           { type: 'number', label: 'Duration' },
  //           { type: 'number', label: 'Percent Complete' },
  //           { type: 'string', label: 'Dependencies' },
  //       ],
  // ['1', 'GeeksforGeeks Course Planning', 'Planning', new Date(2024, 5, 1), new Date(2024, 5, 5), null, 100, null],
  // ['2', 'Content Creation', 'Writing', new Date(2024, 5, 6), new Date(2024, 5, 20), null, 50, '1'],
  // ['3', 'Review and Editing', 'Editing', new Date(2024, 5, 21), new Date(2024, 5, 25), null, 25, '2'],
  // ['4', 'Final Approval', 'Approval', new Date(2024, 5, 26), new Date(2024, 5, 30), null, 0, '3'],
  //   ];
  
  //   const options = {
  //       height: 400,
  //       gantt: {
  //           criticalPathEnabled: true,
  //           criticalPathStyle: {
  //               stroke: '#e64a19',
  //               strokeWidth: 5,
  //           },
  //           trackHeight: 30,
  //       },
  //   };

  return (
    <>
    <Router>
    <Navbar />
    <Routes>
      <Route path = '/' element={<Home />} />
      <Route path='/services' element={<Services/>} />
      <Route path='/products' element={<Products />} />
      <Route path='/about-us' element={<AboutUs />} />
      {/* <Route path = '/' element = {<About />} /> */}
    </Routes>
    </Router>

    {/* <div style={{ fontFamily: 'Arial, sans-serif' }}>
        <h1 style={{ color: 'Black' }}>Gantt Chart</h1>
        <Chart
            chartType="Gantt"
            width="85%"
            data={data}
            options={options}
        />
    </div> */}
    </>
  );
}

export default App;
