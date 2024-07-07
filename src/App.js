import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Services from './components/pages/Services';
import Products from './components/pages/Products';
import SignUp from './components/pages/SignUp';



// const Home = () => 
//   <div>
//     Home page
//   </div>;

// const About = () => 
//   <div>
//     About Page
//   </div>;

function App() {
  return (
    <>
    <Router>
    <Navbar />
    <Routes>
      <Route path = '/' exact />
      <Route path='/services' component={Services} />
      <Route path='/products' component={Products} />
      <Route path='/sign-up' component={SignUp} />
      {/* <Route path = '/' element = {<About />} /> */}
    </Routes>
    </Router>
 
    </>
  );
}

export default App;

console.log('Public URL:', process.env.PUBLIC_URL);
