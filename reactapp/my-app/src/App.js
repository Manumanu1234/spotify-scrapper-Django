import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import { useState } from 'react';
import CreateRoom from './components/CreateRoom';
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import HomePage from './components/HomePage';
import Newpage from './components/Newpage';
import JoinRoom from './components/JoinRoom';
import UpdateRoom from './components/UpdateRoom';
let data = [
  {
    "name": "Abla Dilmurat",
    "language": "Uyghur",
    "version": 2.53
  },
  {
    "name": "Adil Eli",
    "language": "Uyghur",
    "version": 6.49
  }]



function App() {
  /* async function handlefun() {
     console.log("come");
     const response = await axios.get("http://localhost:8000/hello/", {
       headers: {
         'Content-Type': 'application/json',
       }
     });
     console.log(response.data);
     setfirst(response.data.complete)
   }
 
  async function handlefun2(e){
     e.preventDefault()
     console.log(image.raw);
     let formData = new FormData();
     formData.append('hotel_Main_Img', image.raw)
     formData.append('Name', 'manu');
     formData.append('Language', 'Malayalam');
     formData.append('Version', '5.0');
     let callback=await axios.post("http://localhost:8000/delete/",formData,{
       headers: {
         'Content-Type': 'multipart/form-data',
       },
     })
   }*/

  return (
    <div className="App">
      <Router>
      <Routes>
      <Route path='/' element={<HomePage />} />
          <Route path='/createroom' element={<CreateRoom />} />
          <Route path='/get-room' element={<Newpage />} />
          <Route path='/joinroom' element={<JoinRoom />} />
          <Route path='/updateroom' element={<UpdateRoom/>}></Route>
          </Routes>
      </Router>
     
      
    </div>
  );
}

export default App;
