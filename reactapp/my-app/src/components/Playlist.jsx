import React, { useState } from 'react'
import './playlist.css'
import "./Room.css"
import axios from 'axios';
function Playlist() {
    const [playlist, setplaylist] = useState([])
    function fortest(){
        axios.get('http://localhost:8000/spotify/play-list',{withCredentials:true}).then((response)=>{
          console.log(response.data);
          setplaylist(response.data.success)
        })
    }

    function handlefun(name){
        alert(name)
        let data={name:name}
        axios.post('http://localhost:8000/spotify/download',data,{ responseType: 'blob',withCredentials:true},name).then((response)=>{
            console.log(response.data);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'song.mp3');
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
            alert(url)
        })
    
    }
   
    return (
        <div>
            <button className='musics' onClick={fortest}>Featch Playlist</button>
            {playlist && playlist.map((elem)=>{
                return(
                    <div class="spotify-widget">
                    <iframe src={`https://open.spotify.com/embed/album/${elem.album_id}?utm_source=generator`} width="50%" height="80" frameborder="0" allowfullscreen=""  loading="lazy"></iframe>
                    <button className='musics1' onClick={()=>{handlefun(elem.track_name)}}>Download</button>
                
                </div>
                )
            })}
            
          
          
        </div>

    )
}

export default Playlist