import React, { useEffect, useState } from 'react'
import './Room.css'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function CreateRoom() {
    const [vote_to_skip, setvote_to_skip] = useState(null)
    const [gust_can_pause, setgust_can_pause] = useState(null)
    let navigate=useNavigate()
    useEffect(() => {
        //let code='JXRPMK'
        axios.get(`http://localhost:8000/roomexist`,{withCredentials:true}).then((response)=>{
          console.log("sucess");
          if(response.data.status==true){
            navigate('/get-room',{state:{data:response.data.datas.code}})
          }else{
            navigate('/createroom')
          }
        })
    }, [])
    function handlesubmit() {
        let obj = {
            vote_to_skip: vote_to_skip,
            gust_can_pause: gust_can_pause
        }
        axios.post('http://localhost:8000/createroom/', obj, {
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials: true
          }).then((response)=>{
           navigate('/get-room',{state:{data:response.data.code}})
          })
    }

    return (
      <div className='homepage'>
      <div className='createroomhead'>
        <h1>Create Room</h1>
        <label>Guest control playback state</label>
        <div className='guest_control'>
          <input defaultChecked type="radio" onClick={(e) => { setgust_can_pause(true) }} name="gust_can_pause"></input>
          <label>Play/Pause</label>
          <input type="radio" onClick={() => { setgust_can_pause(false) }} name="gust_can_pause"></input>
          <label>No Control</label>
        </div>
        <input required onChange={(e) => { setvote_to_skip(e.target.value) }} type="text" name="vote_to_skip"></input>

        <label htmlFor="input">Vote required to skip</label>
        <button className='create' onClick={handlesubmit} >Create Room</button>
        <button className='create' >Back</button>

      </div>
    </div>
    )
}

export default CreateRoom