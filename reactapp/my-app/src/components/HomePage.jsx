import axios from 'axios'
import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import "./Room.css"
function HomePage() {
  let navigate=useNavigate()
  useEffect(() => {
    //let code='JXRPMK'
    axios.get(`http://localhost:8000/roomexist`,{withCredentials:true}).then((response)=>{
      console.log("sucess");
      console.log(response);
      if(response.data.status==true){
        navigate('/get-room',{state:{data:response.data.datas.code}})
      }else{
        navigate('/')
      }
    })
}, [])
  
    return (
      <div className='homepage' >
      <div className='typewriter'>
        <h1 className='dark1'>Hey EveryOne enjoy this This music Player and download your playlist</h1>
      </div>
      <button className='create' onClick={() => { navigate('/joinroom') }}>Join Room</button>
      <button className='create' onClick={() => { navigate('/createroom') }}>CreateRoom</button>
    </div>
  )
}

export default HomePage