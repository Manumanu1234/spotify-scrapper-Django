import axios from 'axios'
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function JoinRoom() {
  let navigate = useNavigate()
  const [code, setcode] = useState('')
  function handlesubmit() {
    let obj = { code: code }
    axios.post('http://localhost:8000/joinroom/', obj, {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    }).then((response) => {
      console.log(response.data);
      if (response.data.status == true) {
        navigate('/get-room', { state: { data: response.data.data } })
      } else {
        alert('no room is found')
      }
      //navigate('/get-room',{state:{data:response.data.code}})
    })
  }
  return (
    <div className='homepage'>
      <div>
        <h1 className='codes'>Paste Your Code Hear</h1>
      </div>
      <div class="form__group field">
        <input onChange={(e) => { setcode(e.target.value) }} value={code}  type="input" class="form__field" placeholder="Code" ></input>
        <label for="name" class="form__label">Code</label>
      </div>
      <button className='create' onClick={handlesubmit}>join room</button>
    </div>

  )
}

export default JoinRoom