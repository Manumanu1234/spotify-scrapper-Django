import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

function UpdateRoom() {
    const [vote_to_skip, setvote_to_skip] = useState(null)
    const [gust_can_pause, setgust_can_pause] = useState(null)
    let navigate=useNavigate()
    const {state}=useLocation()
    function handlesubmit() {
        let obj = {
            vote_to_skip: vote_to_skip,
            gust_can_pause: gust_can_pause,
            code:state.data
        }
        axios.post('http://localhost:8000/updateroom/', obj, {
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials: true
          }).then((response)=>{
           alert(response.data.msg)
           if(response.data.data !=false){
            navigate('/get-room',{state:{data:response.data.data}})
           }
          
          })
    }
  return (
    <div className='createroomhead'>
    <h1>Crete Room</h1>
    <label>Gust control playback state</label>
    <div className='gust_control'>

        <input type="radio" onClick={(e) => { setgust_can_pause(true) }} name="gust_can_pause" ></input>
        <label htmlFor="">play/pause</label>
        <input type="radio" onClick={() => { setgust_can_pause(false) }} name="gust_can_pause" ></input>
        <label htmlFor="">no control</label>
    </div>
    <input onChange={(e) => { setvote_to_skip(e.target.value) }} className='vote' type="text" name="vote_to_skip"></input>
    <label htmlFor="input">vote required to skip</label>
    <button onClick={handlesubmit}>Update room</button>
    <button onClick={()=>{ navigate('/get-room',{state:{data:state.data}})}}>Back</button>
</div>
  )
}

export default UpdateRoom