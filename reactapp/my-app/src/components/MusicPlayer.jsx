import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BiSkipPrevious, BiSkipNext } from 'react-icons/bi';
import { AiFillPlayCircle, AiFillPauseCircle } from 'react-icons/ai';
import { IconContext } from 'react-icons';

function MusicPlayer() {
  const [songdetails, setSongDetails] = useState({});
  const [isPlaying, setIsPlaying] = useState(false);
  const [forrangetime, setForRangeTime] = useState(0);
  const [fordurationrange, setForDurationRange] = useState(0);
  const [fetchDataTimeout, setFetchDataTimeout] = useState(null);

  useEffect(() => {
    fetchSongDetails();

   
    return () => {
      if (fetchDataTimeout) {
        clearTimeout(fetchDataTimeout);
      }
    };
  }, []);

 
  const fetchSongDetails = () => {
    axios.get('http://localhost:8000/spotify/current-song', { withCredentials: true })
      .then(response => {
        const data = response.data.data;
        setSongDetails(data);
        setIsPlaying(data.is_playing);
        setForDurationRange(data.duration);
        setForRangeTime(data.time);
        if (data.is_playing) {
          startFetchInterval();
        }
      })
      .catch(error => console.error('Error fetching song details:', error));
  };


  const startFetchInterval = () => {
    const timeout = setTimeout(() => {
      fetchSongDetails();
    }, 2000);
    setFetchDataTimeout(timeout);
  };

  const togglePlayPause = () => {
    setIsPlaying(prev => !prev); 

    if (!isPlaying) {
      startFetchInterval();
      axios.get('http://localhost:8000/spotify/pause-song',{withCredentials:true}).then((response)=>{
        console.log(response.data.sucess.error.message);
      })
    } else {
      clearTimeout(fetchDataTimeout); 
      setFetchDataTimeout(null);
      axios.get('http://localhost:8000/spotify/play-song',{withCredentials:true}).then((response)=>{
        console.log(response.data.sucess.error.message);
      })
    }
  };


  const formatTime = (timeInMillis) => {
    const minutes = Math.floor(timeInMillis / 60000);
    const seconds = Math.floor((timeInMillis % 60000) / 1000);
    return { min: minutes, sec: seconds };
  };


  return (
    <div  className="component">
       {songdetails !=null ? 
      <div><h2>Playing Now</h2>
     
      <img className="musicCover" src={songdetails.image_url} alt="Music Cover" />
      <div>
        <h3 className="title">{songdetails.title}</h3>
        <p className="subTitle">{songdetails.artist}</p>
      </div>
      <div>
        <div className="time">
          <p>{formatTime(forrangetime).min}:{formatTime(forrangetime).sec}</p>
          <p>{formatTime(fordurationrange).min}:{formatTime(fordurationrange).sec}</p>
        </div>
        <input
          type="range"
          min="0"
          max={fordurationrange}
          step={1}
          value={forrangetime}
          className="timeline"
          disabled
          onChange={(e) => setForRangeTime(parseInt(e.target.value, 10))}
        />
      </div>
      <div>
        <button className="playButton">
          <IconContext.Provider value={{ size: "3em", color: "#27AE60" }}>
            <BiSkipPrevious />
          </IconContext.Provider>
        </button>
        <button className="playButton" onClick={togglePlayPause}>
          <IconContext.Provider value={{ size: "3em", color: "#27AE60" }}>
            {isPlaying ? <AiFillPauseCircle /> : <AiFillPlayCircle />}
          </IconContext.Provider>
        </button>
        <button onClick={()=>{
          axios.get('http://localhost:8000/spotify/play-next',{withCredentials:true}).then((response)=>{
            console.log(response.data.sucess.error.message);
          })
        }} className="playButton">
          <IconContext.Provider value={{ size: "3em", color: "#27AE60" }}>
            <BiSkipNext />
          </IconContext.Provider>
        </button>
      </div></div>
    
    
      :alert('You are the host please ensure that you are playing  songs in  spotify')}
      
    </div>
  );
}

export default MusicPlayer;
