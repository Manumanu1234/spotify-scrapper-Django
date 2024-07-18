import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import MusicPlayer from './MusicPlayer'
import Playlist from './Playlist'
import "./Room.css"
function Newpage() {
    const { state } = useLocation()
    const [data, setdata] = useState({})

    const navigate = useNavigate()
    function leavingroom() {
        axios.get('http://localhost:8000/leavingroom', { withCredentials: true }).then((response) => {
            if (response.data.status) {
                navigate('/')
            }
        })
    }

    useEffect(() => {
        //let code='JXRPMK'
        // console.log(state);
        axios.get(`http://localhost:8000/getroom/?code=${state.data}`, { withCredentials: true }).then((response) => {
            let obj = {
                code: response.data.code,
                vote_to_skip: response.data.vote_to_skip,
                gust_can_pause: String(response.data.gust_can_pause),
                is_host: String(response.data.is_host)
            }
            setdata(obj)

        })
    }, [])
    useEffect(() => {
        if (data.is_host = 'true') {
            //console.log(data.is_host); 
            axios.get(`http://localhost:8000/spotify/isAuth`, { withCredentials: true }).then((response) => {
                console.log(response);
                if (response.data.isauth == false) {
                    //alert('inning')
                    axios.get(`http://localhost:8000/spotify/get-url-auth`, { withCredentials: true }).then((response) => {
                        console.log(response);
                        window.location.replace(response.data.url)
                    })
                }
            })
        }
    }, [])

    return (
        <div className='newpageblack'>

            <h1 style={{color:'white'}} className='roomcode'>Your room code:{data.code}</h1>

            <div className='leaveandsetting'>

                <div>
                    <button className='musics' onClick={leavingroom}>leave</button>
                </div>
                <div>
                    {data.is_host == "true" && <button className='musics' onClick={() => { navigate('/updateroom', { state: { data: data.code } }) }}>Setting</button>}
                </div>
            </div>







            <MusicPlayer />

            <div className='playistdownload'>
                <h1>Fetch and Download Playlist</h1>
                <Playlist />
            </div>


            <div>

            </div>
        </div>
    )
}

export default Newpage